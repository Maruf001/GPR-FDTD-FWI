#!/usr/bin/env python3
"""Evaluate local radius margins under cumulative frequency weight choices."""

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
from inversion.frequency_weighting import (  # noqa: E402
    best_curve_by_radius,
    frequency_key,
    parse_frequency_list_ghz,
    parse_weight_sets,
    radius_margin_from_ranked,
    rank_weighted_candidates,
    weighted_misfit,
)
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    build_model_from_single_params,
    default_single_rebar_truth,
)
from run_single_rebar_inversion import _override_grid, _parse_ghz_bandpass  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def parse_values_mm(text):
    """Parse comma values or inclusive min:max:step ranges in millimeters."""
    values = []
    for item in str(text).split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            parts = [float(part.strip()) for part in item.split(":") if part.strip()]
            if len(parts) != 3:
                raise argparse.ArgumentTypeError("ranges must use min:max:step")
            start, stop, step = parts
            if step <= 0.0 or start > stop:
                raise argparse.ArgumentTypeError("range requires positive step and start <= stop")
            count = int(np.floor((stop - start) / step + 1e-9)) + 1
            values.extend((start + step * np.arange(count)).tolist())
        else:
            values.append(float(item))
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    return sorted({round(float(value), 10) for value in values})


def _format_frequency_map(values_by_frequency):
    return {
        frequency_key(freq_hz): float(value)
        for freq_hz, value in values_by_frequency.items()
    }


def _candidate_params(x_mm, z_mm, radius_mm):
    return SingleRebarParams(
        x=float(x_mm) / 1000.0,
        z=float(z_mm) / 1000.0,
        radius=float(radius_mm) / 1000.0,
    )


def evaluate_candidate_grid(engine, x_values_mm, z_values_mm, radius_values_mm, progress_every=5):
    """Evaluate per-frequency misfits on a local candidate grid."""
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
                d_syn_by_frequency = {
                    freq_hz: engine._simulate_bscan(model, engine.wavelets[freq_hz])
                    for freq_hz in engine.frequencies
                }
                misfit_by_frequency = engine._objective_misfit_by_frequency(d_syn_by_frequency)
                candidates.append({
                    "params": params.as_mm(),
                    "misfit_by_frequency": _format_frequency_map(misfit_by_frequency),
                })
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  Candidate grid: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def build_weight_results(candidates, weight_sets, top_k):
    """Rank candidates and compute radius margins for each weight set."""
    results = {}
    for label, weights in weight_sets.items():
        ranked_all = rank_weighted_candidates(candidates, weights, top_k=len(candidates))
        results[label] = {
            "weights_by_frequency": weights,
            "margin": radius_margin_from_ranked(ranked_all),
            "top_candidates": ranked_all[:top_k],
            "best_curve_by_radius": best_curve_by_radius(candidates, weights),
        }
    return results


def write_candidate_csv(path, candidates, weight_sets):
    """Write candidate grid with per-frequency and weighted objectives."""
    frequency_keys = list(next(iter(candidates))["misfit_by_frequency"].keys())
    fieldnames = [
        "x_mm",
        "z_mm",
        "radius_mm",
        *[f"misfit_{key}" for key in frequency_keys],
        *[f"objective_{label}" for label in weight_sets],
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            row = {
                "x_mm": candidate["params"]["x_mm"],
                "z_mm": candidate["params"]["z_mm"],
                "radius_mm": candidate["params"]["radius_mm"],
            }
            for key in frequency_keys:
                row[f"misfit_{key}"] = candidate["misfit_by_frequency"][key]
            for label, weights in weight_sets.items():
                row[f"objective_{label}"] = weighted_misfit(
                    candidate["misfit_by_frequency"],
                    weights,
                )
            writer.writerow(row)


def plot_radius_profiles(results, save_path):
    """Plot best-over-depth objective curves for each weight set."""
    fig, ax = plt.subplots(figsize=(8.6, 5.1), constrained_layout=True)
    for label, result in results.items():
        curve = result["best_curve_by_radius"]
        radius = [item["radius_mm"] for item in curve]
        misfit = [item["misfit"] for item in curve]
        ax.plot(radius, misfit, marker="o", linewidth=1.8, markersize=4.5, label=label)
        if curve:
            best = min(curve, key=lambda item: item["misfit"])
            ax.scatter(
                [best["radius_mm"]],
                [best["misfit"]],
                s=46,
                zorder=4,
                edgecolors="black",
                linewidths=0.8,
            )

    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Best objective over x/z")
    ax.set_title("Frequency-Weighted Radius Evidence")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", frameon=True, fontsize=8)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequencies-ghz", default="1.0,1.5")
    parser.add_argument(
        "--weight-sets",
        default="low_only:1,0|onepointfive_only:0,1|unweighted:1,1|carry_low_25:0.25,1|carry_low_50:0.5,1",
    )
    parser.add_argument("--x-values-mm", type=parse_values_mm, default=parse_values_mm("250.0"))
    parser.add_argument("--z-values-mm", type=parse_values_mm, default=parse_values_mm("90.0,90.5,91.0,91.5"))
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--objective-bandpass-ghz", type=_parse_ghz_bandpass, default=None)
    parser.add_argument("--objective-bandpass-taper-ghz", type=float, default=0.05)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--progress-every", type=int, default=5)
    parser.add_argument("--run-name", default="single_rebar_frequency_weight_matrix")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    frequencies_hz = parse_frequency_list_ghz(args.frequencies_ghz)
    frequency_keys = [frequency_key(freq_hz) for freq_hz in frequencies_hz]
    weight_sets = parse_weight_sets(args.weight_sets, frequency_keys)

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")
    print(f"Frequencies GHz: {[freq / 1e9 for freq in frequencies_hz]}")
    print(f"Weight sets: {list(weight_sets.keys())}")
    print(
        "Candidate grid: "
        f"{len(args.x_values_mm)} x values, "
        f"{len(args.z_values_mm)} z values, "
        f"{len(args.radius_values_mm)} radius values"
    )

    engine = SingleRebarInversionEngine(
        true_params=default_single_rebar_truth(),
        initial_params=_candidate_params(250.0, 90.0, 6.8),
        frequencies=frequencies_hz,
        n_sources=args.sources,
        backend=args.backend,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        observed_noise_rms_fraction=args.observed_noise_rms_fraction,
        noise_seed=args.noise_seed,
        objective_bandpass_hz=args.objective_bandpass_ghz,
        objective_bandpass_taper_hz=args.objective_bandpass_taper_ghz * 1e9,
    )

    started = time.time()
    candidates = evaluate_candidate_grid(
        engine,
        args.x_values_mm,
        args.z_values_mm,
        args.radius_values_mm,
        progress_every=args.progress_every,
    )
    elapsed = time.time() - started
    results = build_weight_results(candidates, weight_sets, args.top_k)

    csv_path = os.path.join(data_dir, "frequency_weight_matrix.csv")
    write_candidate_csv(csv_path, candidates, weight_sets)
    plot_path = os.path.join(figures_dir, "frequency_weight_radius_profiles.png")
    plot_radius_profiles(results, plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequencies_ghz": [float(freq / 1e9) for freq in frequencies_hz],
        "frequency_keys": frequency_keys,
        "weight_sets": weight_sets,
        "x_values_mm": args.x_values_mm,
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
        "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
        "noise_seed": args.noise_seed,
        "objective_bandpass": None if args.objective_bandpass_ghz is None else {
            "low_hz": float(args.objective_bandpass_ghz[0]),
            "high_hz": float(args.objective_bandpass_ghz[1]),
            "taper_hz": float(args.objective_bandpass_taper_ghz * 1e9),
        },
        "geometry_mode": args.geometry_mode,
        "subcell_samples": args.subcell_samples,
        "candidate_count": len(candidates),
        "elapsed_time_s": float(elapsed),
        "results": results,
        "paths": {
            "candidate_csv": csv_path,
            "radius_profile_plot": plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "frequency_weight_matrix_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "single_rebar_frequency_weight_matrix",
        {
            "summary_path": summary_path,
            "candidate_csv": csv_path,
            "radius_profile_plot": plot_path,
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
