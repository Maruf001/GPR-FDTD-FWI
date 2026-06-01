#!/usr/bin/env python3
"""Run B-scan hyperbola detection as the seed stage before FWI refinement."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array  # noqa: E402
from inversion.rebar_detection import (  # noqa: E402
    candidate_window,
    detect_rebar_candidates,
    hyperbola_times,
)
from run_multi_rebar_common_radius_profile import (  # noqa: E402
    build_scan_positions,
    simulate_bscan,
)
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    build_variable_geometry_model,
    parse_vector_mm,
)
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import observed_wavelet  # noqa: E402
from visualization.plot_style import safe_symmetric_limits, save_validated_figure, scan_extent_mm_ns  # noqa: E402


def parse_mm_range(text):
    """Parse start:stop:step or comma-separated millimeter values."""
    text = str(text)
    if ":" in text:
        parts = [float(part.strip()) for part in text.split(":") if part.strip()]
        if len(parts) != 3:
            raise argparse.ArgumentTypeError("range must be start:stop:step")
        start, stop, step = parts
        if step <= 0.0 or stop < start:
            raise argparse.ArgumentTypeError("range requires stop >= start and step > 0")
        count = int(np.floor((stop - start) / step + 1e-9)) + 1
        return [float(start + i * step) for i in range(count)]
    return parse_vector_mm(text)


def parse_ps_values(text):
    """Parse comma-separated picosecond values."""
    values = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("at least one time offset is required")
    return values


def add_noise(clean, noise_fraction, seed):
    """Add Gaussian noise as a fraction of clean RMS."""
    clean = np.asarray(clean, dtype=np.float64)
    if noise_fraction <= 0.0:
        return clean.copy(), {"clean_rms": float(np.sqrt(np.mean(clean ** 2))), "noise_std": 0.0}
    rng = np.random.default_rng(int(seed))
    clean_rms = float(np.sqrt(np.mean(clean ** 2)))
    noise_std = float(noise_fraction) * clean_rms
    noise = rng.normal(0.0, noise_std, clean.shape)
    return clean + noise, {
        "clean_rms": clean_rms,
        "noise_std": noise_std,
        "actual_noise_rms": float(np.sqrt(np.mean(noise ** 2))),
    }


def truth_match_metrics(candidates, truth_x_values_mm, truth_z_values_mm, tolerance_x_mm, tolerance_z_mm):
    """Return nearest-error metrics for truth points and detection candidates."""
    metrics = []
    for truth_x, truth_z in zip(truth_x_values_mm, truth_z_values_mm):
        distances = [
            (
                abs(candidate.x_m * 1000.0 - truth_x),
                abs(candidate.z_m * 1000.0 - truth_z),
                index,
            )
            for index, candidate in enumerate(candidates, start=1)
        ]
        if not distances:
            metrics.append({
                "truth_x_mm": float(truth_x),
                "truth_z_mm": float(truth_z),
                "matched_rank": None,
                "x_error_mm": None,
                "z_error_mm": None,
                "within_tolerance": False,
            })
            continue
        best = min(distances, key=lambda item: (item[0] + item[1], item[2]))
        x_error, z_error, rank = best
        metrics.append({
            "truth_x_mm": float(truth_x),
            "truth_z_mm": float(truth_z),
            "matched_rank": int(rank),
            "x_error_mm": float(x_error),
            "z_error_mm": float(z_error),
            "within_tolerance": bool(x_error <= tolerance_x_mm and z_error <= tolerance_z_mm),
        })
    return metrics


def write_candidates_csv(path, candidates, window_half_x_mm, window_half_z_mm):
    """Write detection candidates to CSV."""
    fieldnames = [
        "rank",
        "x_mm",
        "z_mm",
        "score",
        "normalized_score",
        "support_fraction",
        "time_offset_ps",
        "x_min_mm",
        "x_max_mm",
        "z_min_mm",
        "z_max_mm",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for rank, candidate in enumerate(candidates, start=1):
            window = candidate_window(candidate, window_half_x_mm, window_half_z_mm)
            writer.writerow({
                "rank": rank,
                **candidate.as_mm(),
                **window,
            })


def plot_detection_overlay(
        bscan,
        scan_x,
        time_values,
        candidates,
        truth_x_values_mm,
        truth_z_values_mm,
        save_path):
    """Plot B-scan with detected candidate hyperbolas and truth markers."""
    bscan = np.asarray(bscan, dtype=np.float64)
    fig, ax = plt.subplots(figsize=(11.0, 7.0), constrained_layout=True)
    vmin, vmax = safe_symmetric_limits(bscan, percentile=99.2)
    image = ax.imshow(
        bscan,
        cmap="RdBu_r",
        aspect="auto",
        interpolation="nearest",
        extent=scan_extent_mm_ns(scan_x, time_values),
        vmin=vmin,
        vmax=vmax,
    )
    for rank, candidate in enumerate(candidates, start=1):
        curve = hyperbola_times(
            scan_x,
            candidate.x_m,
            candidate.z_m,
            time_offset_s=candidate.time_offset_s,
        ) * 1e9
        ax.plot(scan_x * 1000.0, curve, linewidth=1.2, label=f"#{rank} det")
        ax.scatter(
            [candidate.x_m * 1000.0 - cfg.TX_RX_OFFSET * 500.0],
            [np.min(curve)],
            s=32,
            marker="o",
            edgecolor="black",
            linewidth=0.4,
            zorder=3,
        )
    truth_time_offset_s = candidates[0].time_offset_s if candidates else 0.0
    for truth_x, truth_z in zip(truth_x_values_mm, truth_z_values_mm):
        curve = hyperbola_times(
            scan_x,
            truth_x / 1000.0,
            truth_z / 1000.0,
            time_offset_s=truth_time_offset_s,
        ) * 1e9
        ax.plot(scan_x * 1000.0, curve, color="black", linestyle="--", linewidth=1.0)
    ax.set_xlabel("Scan source x [mm]")
    ax.set_ylabel("Two-way travel time [ns]")
    ax.set_title("B-scan Detection Seeds", fontsize=14, fontweight="bold")
    ax.set_ylim(float(time_values[-1] * 1e9), float(time_values[0] * 1e9))
    if candidates:
        ax.legend(loc="upper right", fontsize=8, frameon=True)
    fig.colorbar(image, ax=ax, shrink=0.88, label="Amplitude")
    return save_validated_figure(fig, save_path)


def _format_mm_values(values):
    return ", ".join(f"{float(value):g}" for value in values)


def write_detection_figure_notes(path, summary):
    """Write plain-language notes for detector figures."""
    candidates = summary.get("candidates", [])
    candidate_lines = []
    for candidate in candidates[:5]:
        candidate_lines.append(
            f"- rank {candidate['rank']}: x={float(candidate['x_mm']):g} mm, "
            f"z={float(candidate['z_mm']):g} mm"
        )
    if not candidate_lines:
        candidate_lines.append("- no detector candidates were returned")

    text = f"""# Figure Notes

## 1. detection_overlay.png

This figure shows the observed B-scan, meaning the radar amplitude recorded
as the antenna is moved along the scan line. B-scan is short for brightness
scan: the horizontal axis is antenna position, the vertical axis is two-way
travel time, and color is signal amplitude.

Colored curves are the detector's proposed rebar hyperbolas. Dashed black
curves mark the known synthetic truth used to generate the data. These
 detector candidates are the seed points that later feed Full-waveform inversion
(FWI), which means matching the complete simulated and observed waveform
instead of only matching a picked travel-time curve.

Truth positions: x={_format_mm_values(summary['truth_x_values_mm'])} mm,
z={_format_mm_values(summary['truth_z_values_mm'])} mm; truth radii: {_format_mm_values(summary['truth_radius_values_mm'])} mm.

First candidates to inspect:

{chr(10).join(candidate_lines)}

All truth points within the configured detector tolerance:
{bool(summary.get('all_truths_within_tolerance'))}.
"""
    Path(path).write_text(text, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=2.0)
    parser.add_argument("--scan-step-mm", type=float, default=4.0)
    parser.add_argument("--sources", type=int, default=None)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--truth-x-values-mm", type=parse_vector_mm, default=parse_vector_mm("250"))
    parser.add_argument("--truth-z-values-mm", type=parse_vector_mm, default=parse_vector_mm("90"))
    parser.add_argument("--truth-radius-values-mm", type=parse_vector_mm, default=parse_vector_mm("6"))
    parser.add_argument("--frequency-scale", type=float, default=1.0)
    parser.add_argument("--time-shift-ps", type=float, default=0.0)
    parser.add_argument("--amplitude-scale", type=float, default=1.0)
    parser.add_argument("--noise-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--detector-x-values-mm", type=parse_mm_range, default=parse_mm_range("50:450:4"))
    parser.add_argument("--detector-z-values-mm", type=parse_mm_range, default=parse_mm_range("55:180:5"))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--background-mode", choices=["none", "mean", "median"], default="median")
    parser.add_argument(
        "--detector-time-offset-ps",
        type=float,
        default=None,
        help="Hyperbola time offset. Defaults to source Ricker delay 1/frequency.",
    )
    parser.add_argument(
        "--detector-time-offset-ps-values",
        type=parse_ps_values,
        default=None,
        help="Comma-separated hyperbola time offsets to search. Overrides --detector-time-offset-ps.",
    )
    parser.add_argument("--x-min-separation-mm", type=float, default=35.0)
    parser.add_argument("--z-min-separation-mm", type=float, default=12.0)
    parser.add_argument("--window-half-x-mm", type=float, default=24.0)
    parser.add_argument("--window-half-z-mm", type=float, default=24.0)
    parser.add_argument("--truth-tolerance-x-mm", type=float, default=12.0)
    parser.add_argument("--truth-tolerance-z-mm", type=float, default=12.0)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--run-name", default="rebar_detection_pipeline")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    if len(args.truth_x_values_mm) != len(args.truth_z_values_mm):
        raise ValueError("truth x/z list lengths must match")
    if len(args.truth_x_values_mm) != len(args.truth_radius_values_mm):
        raise ValueError("truth x/z/radius list lengths must match")
    if args.noise_fraction < 0.0:
        raise ValueError("--noise-fraction must be non-negative")

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = Path(outdir) / "data"
    figures_dir = Path(outdir) / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    scan_positions, scan_x = build_scan_positions(args.scan_step_mm / 1000.0, args.sources)
    time_values = generate_time_array(cfg.NT, cfg.DT)
    model = build_variable_geometry_model(
        args.truth_x_values_mm,
        args.truth_z_values_mm,
        args.truth_radius_values_mm,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    wavelet = observed_wavelet(
        time_values,
        args.frequency_ghz * 1e9,
        frequency_scale=args.frequency_scale,
        time_shift_ps=args.time_shift_ps,
        amplitude_scale=args.amplitude_scale,
    )

    started = time.time()
    clean = simulate_bscan(model, wavelet, scan_positions, args.backend)
    observed, noise_stats = add_noise(clean, args.noise_fraction, args.noise_seed)
    detector_time_offset_s = (
        1.0 / (args.frequency_ghz * 1e9)
        if args.detector_time_offset_ps is None
        else args.detector_time_offset_ps * 1e-12
    )
    detector_time_offsets_s = (
        None
        if args.detector_time_offset_ps_values is None
        else [value * 1e-12 for value in args.detector_time_offset_ps_values]
    )
    candidates = detect_rebar_candidates(
        observed,
        scan_x,
        time_values,
        x_values_mm=args.detector_x_values_mm,
        z_values_mm=args.detector_z_values_mm,
        top_k=args.top_k,
        background_mode=args.background_mode,
        x_min_separation_mm=args.x_min_separation_mm,
        z_min_separation_mm=args.z_min_separation_mm,
        time_offset_s=detector_time_offset_s,
        time_offsets_s=detector_time_offsets_s,
    )
    elapsed_s = time.time() - started

    csv_path = data_dir / "detection_candidates.csv"
    write_candidates_csv(csv_path, candidates, args.window_half_x_mm, args.window_half_z_mm)
    npz_path = data_dir / "detection_bscan.npz"
    np.savez(
        npz_path,
        observed_bscan=observed,
        clean_bscan=clean,
        scan_x=scan_x,
        time=time_values,
        truth_x_values_mm=np.asarray(args.truth_x_values_mm),
        truth_z_values_mm=np.asarray(args.truth_z_values_mm),
        truth_radius_values_mm=np.asarray(args.truth_radius_values_mm),
    )
    plot_path = figures_dir / "detection_overlay.png"
    plot_detection_overlay(
        observed,
        scan_x,
        time_values,
        candidates,
        args.truth_x_values_mm,
        args.truth_z_values_mm,
        plot_path,
    )

    match_metrics = truth_match_metrics(
        candidates,
        args.truth_x_values_mm,
        args.truth_z_values_mm,
        args.truth_tolerance_x_mm,
        args.truth_tolerance_z_mm,
    )
    summary = {
        "backend": args.backend,
        "grid_step_mm": float(args.grid_step_mm),
        "scan_step_mm": float(args.scan_step_mm),
        "sources": int(len(scan_positions)),
        "frequency_ghz": float(args.frequency_ghz),
        "truth_x_values_mm": args.truth_x_values_mm,
        "truth_z_values_mm": args.truth_z_values_mm,
        "truth_radius_values_mm": args.truth_radius_values_mm,
        "source": {
            "frequency_scale": float(args.frequency_scale),
            "time_shift_ps": float(args.time_shift_ps),
            "amplitude_scale": float(args.amplitude_scale),
        },
        "noise": noise_stats,
        "detector": {
            "x_values_mm": args.detector_x_values_mm,
            "z_values_mm": args.detector_z_values_mm,
            "top_k": int(args.top_k),
            "background_mode": args.background_mode,
            "time_offset_ps": float(detector_time_offset_s * 1e12),
            "time_offset_values_ps": (
                None
                if args.detector_time_offset_ps_values is None
                else args.detector_time_offset_ps_values
            ),
            "x_min_separation_mm": float(args.x_min_separation_mm),
            "z_min_separation_mm": float(args.z_min_separation_mm),
        },
        "candidates": [
            {
                "rank": rank,
                **candidate.as_mm(),
                "window": candidate_window(candidate, args.window_half_x_mm, args.window_half_z_mm),
            }
            for rank, candidate in enumerate(candidates, start=1)
        ],
        "match_metrics": match_metrics,
        "all_truths_within_tolerance": all(item["within_tolerance"] for item in match_metrics),
        "elapsed_time_s": float(elapsed_s),
        "paths": {
            "csv": str(csv_path),
            "npz": str(npz_path),
            "plot": str(plot_path),
        },
    }
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_detection_figure_notes(notes_path, summary)
    summary["paths"]["figure_notes"] = str(notes_path)
    summary_path = data_dir / "detection_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    write_run_manifest(
        outdir,
        "rebar_detection_pipeline",
        {
            "summary_path": str(summary_path),
            "csv": str(csv_path),
            "plot": str(plot_path),
            "figure_notes": str(notes_path),
        },
    )

    print(f"Detections: {len(candidates)}")
    for rank, candidate in enumerate(candidates, start=1):
        print(
            f"  #{rank}: x={candidate.x_m * 1000.0:.1f} mm, "
            f"z={candidate.z_m * 1000.0:.1f} mm, "
            f"score={candidate.normalized_score:.3f}"
        )
    print(f"All truths within tolerance: {summary['all_truths_within_tolerance']}")
    print(f"Wrote summary: {summary_path}")


if __name__ == "__main__":
    main()
