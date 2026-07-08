#!/usr/bin/env python3
"""Compare LS and Softplus/Sinkhorn W2 on a local one-rebar grid."""

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
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    build_model_from_single_params,
    default_single_rebar_truth,
)
from inversion.trace_wasserstein import softplus_sinkhorn_distance  # noqa: E402
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def _candidate_params(x_mm, z_mm, radius_mm):
    return SingleRebarParams(
        x=float(x_mm) / 1000.0,
        z=float(z_mm) / 1000.0,
        radius=float(radius_mm) / 1000.0,
    )


def rank_by_objective(candidates, objective_key, top_k=None):
    """Rank landscape candidates by one objective key."""
    ranked = [
        {
            "misfit": float(candidate[objective_key]),
            "params": dict(candidate["params"]),
            "ls_misfit": float(candidate["ls_misfit"]),
            "w2_misfit": float(candidate["w2_misfit"]),
        }
        for candidate in candidates
    ]
    ranked.sort(key=lambda item: item["misfit"])
    if top_k is None:
        return ranked
    return ranked[:max(0, int(top_k))]


def best_curve_by_radius(candidates, objective_key):
    """Return best objective value at each radius, minimizing over x/z."""
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        value = float(candidate[objective_key])
        current = best.get(radius)
        if current is None or value < current["misfit"]:
            best[radius] = {
                "radius_mm": radius,
                "misfit": value,
                "params": dict(candidate["params"]),
            }
    return [best[radius] for radius in sorted(best)]


def evaluate_landscape(
        engine,
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        beta=8.0,
        epsilon=0.02,
        downsample=16,
        progress_every=5):
    """Evaluate LS and W2 scores on a local geometry grid."""
    frequency = engine.frequencies[0]
    observed = engine.d_obs_by_frequency[frequency]
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
                synthetic = engine._simulate_bscan(model, engine.wavelets[frequency])
                ls_by_frequency = engine._objective_misfit_by_frequency({frequency: synthetic})
                w2_value = softplus_sinkhorn_distance(
                    observed,
                    synthetic,
                    beta=beta,
                    epsilon=epsilon,
                    dt=cfg.DT,
                    mute=engine.mute,
                    downsample=downsample,
                )
                candidates.append({
                    "params": params.as_mm(),
                    "ls_misfit": float(ls_by_frequency[frequency]),
                    "w2_misfit": float(w2_value),
                })
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  W2 landscape grid: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def write_csv(path, candidates):
    """Write landscape candidates to CSV."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["x_mm", "z_mm", "radius_mm", "ls_misfit", "w2_misfit"],
        )
        writer.writeheader()
        for candidate in candidates:
            row = {
                "x_mm": candidate["params"]["x_mm"],
                "z_mm": candidate["params"]["z_mm"],
                "radius_mm": candidate["params"]["radius_mm"],
                "ls_misfit": candidate["ls_misfit"],
                "w2_misfit": candidate["w2_misfit"],
            }
            writer.writerow(row)


def plot_radius_profiles(candidates, save_path):
    """Plot LS and W2 best-over-depth radius profiles."""
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6), constrained_layout=True)
    specs = [
        ("ls_misfit", "Normalized L2"),
        ("w2_misfit", "Softplus Sinkhorn W2"),
    ]
    for ax, (key, title) in zip(axes, specs):
        curve = best_curve_by_radius(candidates, key)
        radii = [item["radius_mm"] for item in curve]
        values = [item["misfit"] for item in curve]
        ax.plot(radii, values, marker="o", linewidth=1.8, markersize=4.5)
        if curve:
            best = min(curve, key=lambda item: item["misfit"])
            ax.scatter(
                [best["radius_mm"]],
                [best["misfit"]],
                s=50,
                edgecolors="black",
                linewidths=0.8,
                zorder=4,
            )
        ax.set_title(title)
        ax.set_xlabel("Radius [mm]")
        ax.set_ylabel("Best objective over x/z")
        ax.grid(True, alpha=0.25)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--x-values-mm", type=parse_values_mm, default=parse_values_mm("250.0"))
    parser.add_argument("--z-values-mm", type=parse_values_mm, default=parse_values_mm("90.0,90.5,91.0,91.5"))
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--beta", type=float, default=8.0)
    parser.add_argument("--epsilon", type=float, default=0.02)
    parser.add_argument("--downsample", type=int, default=16)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--progress-every", type=int, default=5)
    parser.add_argument("--run-name", default="single_rebar_w2_landscape")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    engine = SingleRebarInversionEngine(
        true_params=default_single_rebar_truth(),
        initial_params=_candidate_params(250.0, 90.0, 6.8),
        frequencies=(args.frequency_ghz * 1e9,),
        n_sources=args.sources,
        backend=args.backend,
        observed_noise_rms_fraction=args.observed_noise_rms_fraction,
        noise_seed=args.noise_seed,
    )

    started = time.time()
    candidates = evaluate_landscape(
        engine,
        args.x_values_mm,
        args.z_values_mm,
        args.radius_values_mm,
        beta=args.beta,
        epsilon=args.epsilon,
        downsample=args.downsample,
        progress_every=args.progress_every,
    )
    elapsed = time.time() - started
    csv_path = os.path.join(data_dir, "w2_landscape.csv")
    plot_path = os.path.join(figures_dir, "w2_radius_profiles.png")
    write_csv(csv_path, candidates)
    plot_radius_profiles(candidates, plot_path)

    ls_ranked = rank_by_objective(candidates, "ls_misfit")
    w2_ranked = rank_by_objective(candidates, "w2_misfit")
    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "x_values_mm": args.x_values_mm,
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
        "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
        "noise_seed": args.noise_seed,
        "w2_config": {
            "beta": args.beta,
            "epsilon": args.epsilon,
            "downsample": args.downsample,
        },
        "elapsed_time_s": float(elapsed),
        "candidate_count": len(candidates),
        "ls": {
            "margin": radius_margin_from_ranked(ls_ranked),
            "top_candidates": ls_ranked[:args.top_k],
            "best_curve_by_radius": best_curve_by_radius(candidates, "ls_misfit"),
        },
        "w2": {
            "margin": radius_margin_from_ranked(w2_ranked),
            "top_candidates": w2_ranked[:args.top_k],
            "best_curve_by_radius": best_curve_by_radius(candidates, "w2_misfit"),
        },
        "paths": {
            "csv": csv_path,
            "plot": plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "w2_landscape_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "single_rebar_w2_landscape",
        {
            "summary_path": summary_path,
            "csv": csv_path,
            "plot": plot_path,
        },
    )
    print(
        "LS: "
        f"best r={summary['ls']['margin']['best_radius_mm']} mm, "
        f"margin={summary['ls']['margin']['radius_margin_abs']}"
    )
    print(
        "W2: "
        f"best r={summary['w2']['margin']['best_radius_mm']} mm, "
        f"margin={summary['w2']['margin']['radius_margin_abs']}"
    )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
