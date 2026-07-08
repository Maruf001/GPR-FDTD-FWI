#!/usr/bin/env python3
"""Evaluate radius margins under observed/source wavelet mismatch."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time

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
from core.source import ricker_wavelet  # noqa: E402
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    build_model_from_single_params,
    default_single_rebar_truth,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CASES = (
    "nominal:1.0,0.0,1.0|"
    "fc_low10:0.9,0.0,1.0|"
    "fc_high10:1.1,0.0,1.0|"
    "delay_plus50ps:1.0,50.0,1.0|"
    "delay_minus50ps:1.0,-50.0,1.0|"
    "amp_low10:1.0,0.0,0.9|"
    "amp_high10:1.0,0.0,1.1"
)


def parse_wavelet_cases(text):
    """
    Parse wavelet mismatch cases.

    Format:

    ```text
    label:frequency_scale,time_shift_ps,amplitude_scale|...
    ```
    """
    cases = []
    labels = set()
    for item in str(text).split("|"):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError("each wavelet case must be label:freq_scale,time_shift_ps,amp_scale")
        label, values_text = item.split(":", 1)
        label = label.strip()
        if not label or label in labels:
            raise ValueError("wavelet case labels must be non-empty and unique")
        values = [float(part.strip()) for part in values_text.split(",") if part.strip()]
        if len(values) != 3:
            raise ValueError("wavelet case requires three numeric values")
        frequency_scale, time_shift_ps, amplitude_scale = values
        if frequency_scale <= 0.0 or amplitude_scale <= 0.0:
            raise ValueError("frequency and amplitude scales must be positive")
        labels.add(label)
        cases.append({
            "label": label,
            "frequency_scale": float(frequency_scale),
            "time_shift_ps": float(time_shift_ps),
            "amplitude_scale": float(amplitude_scale),
        })
    if not cases:
        raise ValueError("at least one wavelet case is required")
    return cases


def shift_wavelet_zero_fill(wavelet, dt, shift_s):
    """Shift a wavelet in time with interpolation and no wraparound."""
    data = np.asarray(wavelet, dtype=np.float64)
    if data.ndim != 1:
        raise ValueError("wavelet must be one-dimensional")
    if dt <= 0.0:
        raise ValueError("dt must be positive")
    time = np.arange(data.size, dtype=np.float64) * float(dt)
    return np.interp(time - float(shift_s), time, data, left=0.0, right=0.0)


def shift_traces_zero_fill(traces, dt, shift_s):
    """Shift trace matrix columns in time with interpolation and no wraparound."""
    data = np.asarray(traces, dtype=np.float64)
    if data.ndim == 1:
        return shift_wavelet_zero_fill(data, dt, shift_s)
    if data.ndim != 2:
        raise ValueError("traces must have shape (nt,) or (nt, n_traces)")
    shifted = np.empty_like(data)
    for index in range(data.shape[1]):
        shifted[:, index] = shift_wavelet_zero_fill(data[:, index], dt, shift_s)
    return shifted


def build_case_wavelet(time, frequency_hz, case):
    """Build the observed wavelet for one mismatch case."""
    wavelet = ricker_wavelet(time, frequency_hz * case["frequency_scale"])
    if case["time_shift_ps"] != 0.0:
        wavelet = shift_wavelet_zero_fill(wavelet, cfg.DT, case["time_shift_ps"] * 1e-12)
    return case["amplitude_scale"] * wavelet


def _candidate_params(x_mm, z_mm, radius_mm):
    return SingleRebarParams(
        x=float(x_mm) / 1000.0,
        z=float(z_mm) / 1000.0,
        radius=float(radius_mm) / 1000.0,
    )


def best_amplitude_scale(observed, synthetic, mute):
    """Return least-squares scalar multiplying synthetic toward observed."""
    weight = mute[:, None]
    observed_w = observed * weight
    synthetic_w = synthetic * weight
    denominator = float(np.sum(synthetic_w ** 2))
    if denominator <= 1e-30:
        return 1.0
    return float(np.sum(observed_w * synthetic_w) / denominator)


def _objective_value(observed, synthetic, mute, fit_amplitude=False, time_shift_s=0.0):
    if time_shift_s != 0.0:
        synthetic = shift_traces_zero_fill(synthetic, cfg.DT, time_shift_s)
    if fit_amplitude:
        synthetic = best_amplitude_scale(observed, synthetic, mute) * synthetic
    residual = (synthetic - observed) * mute[:, None]
    numerator = 0.5 * float(np.sum(residual ** 2))
    denominator = max(0.5 * float(np.sum((observed * mute[:, None]) ** 2)), 1e-30)
    return numerator / denominator


def _objective_value_over_shifts(observed, synthetic, mute, fit_amplitude=False, time_shift_values_s=None):
    shifts = list(time_shift_values_s or [0.0])
    values = [
        _objective_value(
            observed,
            synthetic,
            mute,
            fit_amplitude=fit_amplitude,
            time_shift_s=shift_s,
        )
        for shift_s in shifts
    ]
    return float(min(values))


def parse_shift_values_ps(text):
    """Parse comma-separated source time-shift values in picoseconds."""
    values = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("at least one shift value is required")
    return values


def parse_positive_values(text):
    """Parse comma-separated positive floats."""
    values = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    if any(value <= 0.0 for value in values):
        raise argparse.ArgumentTypeError("values must be positive")
    return values


def rank_case(candidates, case_label, top_k=None):
    """Rank candidates for one wavelet mismatch case."""
    ranked = [
        {
            "misfit": float(candidate["misfit_by_case"][case_label]),
            "params": dict(candidate["params"]),
        }
        for candidate in candidates
    ]
    ranked.sort(key=lambda item: item["misfit"])
    if top_k is None:
        return ranked
    return ranked[:max(0, int(top_k))]


def best_curve_by_radius(candidates, case_label):
    """Return best objective at each radius, minimizing over x/z."""
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        value = float(candidate["misfit_by_case"][case_label])
        current = best.get(radius)
        if current is None or value < current["misfit"]:
            best[radius] = {
                "radius_mm": radius,
                "misfit": value,
                "params": dict(candidate["params"]),
            }
    return [best[radius] for radius in sorted(best)]


def evaluate_mismatch_grid(
        engine,
        observed_by_case,
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        progress_every=5,
        fit_amplitude=False,
        fit_time_shift_values_s=None,
        fit_frequency_scales=None):
    """Evaluate nominal-wavelet candidates against each observed-wavelet case."""
    frequency = engine.frequencies[0]
    frequency_scales = list(fit_frequency_scales or [1.0])
    observed_objective_by_case = {
        label: engine._apply_objective_filter(observed)
        for label, observed in observed_by_case.items()
    }
    candidates = []
    total = len(x_values_mm) * len(z_values_mm) * len(radius_values_mm)
    started = time.time()
    count = 0
    for x_mm in x_values_mm:
        for z_mm in z_values_mm:
            for radius_mm in radius_values_mm:
                params = _candidate_params(x_mm, z_mm, radius_mm)
                model = build_model_from_single_params(
                    params.as_array(),
                    geometry_mode=engine.geometry_mode,
                    subcell_samples=engine.subcell_samples,
                )
                synthetic_objective_by_scale = []
                for scale in frequency_scales:
                    if np.isclose(scale, 1.0, rtol=0.0, atol=1e-12):
                        wavelet = engine.wavelets[frequency]
                    else:
                        wavelet = ricker_wavelet(engine.time, frequency * scale)
                    synthetic = engine._simulate_bscan(model, wavelet)
                    synthetic_objective_by_scale.append(engine._apply_objective_filter(synthetic))
                misfit_by_case = {
                    label: min(
                        _objective_value_over_shifts(
                            observed,
                            synthetic_objective,
                            engine.mute,
                            fit_amplitude=fit_amplitude,
                            time_shift_values_s=fit_time_shift_values_s,
                        )
                        for synthetic_objective in synthetic_objective_by_scale
                    )
                    for label, observed in observed_objective_by_case.items()
                }
                candidates.append({
                    "params": params.as_mm(),
                    "misfit_by_case": misfit_by_case,
                })
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  Wavelet mismatch grid: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def write_csv(path, candidates, case_labels):
    """Write candidate grid with per-case objectives."""
    fieldnames = ["x_mm", "z_mm", "radius_mm", *[f"objective_{label}" for label in case_labels]]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            row = {
                "x_mm": candidate["params"]["x_mm"],
                "z_mm": candidate["params"]["z_mm"],
                "radius_mm": candidate["params"]["radius_mm"],
            }
            for label in case_labels:
                row[f"objective_{label}"] = candidate["misfit_by_case"][label]
            writer.writerow(row)


def plot_radius_profiles(results, save_path):
    """Plot best-over-depth radius profiles for mismatch cases."""
    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    for label, result in results.items():
        curve = result["best_curve_by_radius"]
        radius = [item["radius_mm"] for item in curve]
        values = [item["misfit"] for item in curve]
        ax.plot(radius, values, marker="o", linewidth=1.6, markersize=3.8, label=label)
    ax.set_title("Radius Evidence Under Wavelet Mismatch")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Best objective over x/z")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--wavelet-cases", type=parse_wavelet_cases, default=parse_wavelet_cases(DEFAULT_CASES))
    parser.add_argument("--x-values-mm", type=parse_values_mm, default=parse_values_mm("250.0"))
    parser.add_argument("--z-values-mm", type=parse_values_mm, default=parse_values_mm("90.0,90.5,91.0,91.5"))
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--progress-every", type=int, default=5)
    parser.add_argument("--fit-amplitude", action="store_true",
                        help="Fit one scalar synthetic amplitude per candidate/case before residuals")
    parser.add_argument("--fit-time-shift-ps-values", type=parse_shift_values_ps, default=None,
                        help="Comma-separated synthetic trace shifts to profile over, in picoseconds")
    parser.add_argument("--fit-frequency-scales", type=parse_positive_values, default=None,
                        help="Comma-separated modeled source center-frequency scales to profile over")
    parser.add_argument("--run-name", default="single_rebar_wavelet_mismatch")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    frequency = args.frequency_ghz * 1e9
    engine = SingleRebarInversionEngine(
        true_params=default_single_rebar_truth(),
        initial_params=_candidate_params(250.0, 90.0, 6.8),
        frequencies=(frequency,),
        n_sources=args.sources,
        backend=args.backend,
    )
    observed_by_case = {}
    for case in args.wavelet_cases:
        wavelet = build_case_wavelet(engine.time, frequency, case)
        observed_by_case[case["label"]] = engine._simulate_bscan(engine.true_model, wavelet)

    candidates = evaluate_mismatch_grid(
        engine,
        observed_by_case,
        args.x_values_mm,
        args.z_values_mm,
        args.radius_values_mm,
        progress_every=args.progress_every,
        fit_amplitude=args.fit_amplitude,
        fit_time_shift_values_s=None if args.fit_time_shift_ps_values is None else [
            value * 1e-12 for value in args.fit_time_shift_ps_values
        ],
        fit_frequency_scales=args.fit_frequency_scales,
    )
    case_labels = [case["label"] for case in args.wavelet_cases]
    results = {}
    for label in case_labels:
        ranked = rank_case(candidates, label)
        results[label] = {
            "margin": radius_margin_from_ranked(ranked),
            "top_candidates": ranked[:args.top_k],
            "best_curve_by_radius": best_curve_by_radius(candidates, label),
        }

    csv_path = os.path.join(data_dir, "wavelet_mismatch_matrix.csv")
    plot_path = os.path.join(figures_dir, "wavelet_mismatch_radius_profiles.png")
    write_csv(csv_path, candidates, case_labels)
    plot_radius_profiles(results, plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "wavelet_cases": args.wavelet_cases,
        "x_values_mm": args.x_values_mm,
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
        "fit_amplitude": args.fit_amplitude,
        "fit_time_shift_ps_values": args.fit_time_shift_ps_values,
        "fit_frequency_scales": args.fit_frequency_scales,
        "candidate_count": len(candidates),
        "results": results,
        "paths": {
            "csv": csv_path,
            "plot": plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "wavelet_mismatch_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    write_run_manifest(
        outdir,
        "single_rebar_wavelet_mismatch",
        {
            "summary_path": summary_path,
            "csv": csv_path,
            "plot": plot_path,
        },
    )
    for label, result in results.items():
        margin = result["margin"]
        print(
            f"{label}: best r={margin['best_radius_mm']} mm, "
            f"next r={margin['next_radius_mm']} mm, "
            f"margin={margin['radius_margin_abs']}"
        )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
