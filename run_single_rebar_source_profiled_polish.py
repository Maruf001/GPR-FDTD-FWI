#!/usr/bin/env python3
"""Run source-profiled local radius polish for one rebar."""

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
from inversion.source_profile import shift_traces_zero_fill, source_profiled_ls  # noqa: E402
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def _params_from_mm(x_mm, z_mm, radius_mm):
    return SingleRebarParams(
        x=float(x_mm) / 1000.0,
        z=float(z_mm) / 1000.0,
        radius=float(radius_mm) / 1000.0,
    )


def _add_noise(data, fraction, seed):
    if fraction <= 0.0:
        return data.copy(), {
            "rms_fraction": 0.0,
            "seed": int(seed),
            "clean_rms": float(np.sqrt(np.mean(data ** 2))),
            "noise_std": 0.0,
            "actual_noise_rms": 0.0,
        }
    rng = np.random.default_rng(seed)
    clean_rms = float(np.sqrt(np.mean(data ** 2)))
    noise_std = float(fraction) * clean_rms
    noise = rng.normal(loc=0.0, scale=noise_std, size=data.shape)
    return data + noise, {
        "rms_fraction": float(fraction),
        "seed": int(seed),
        "clean_rms": clean_rms,
        "noise_std": float(noise_std),
        "actual_noise_rms": float(np.sqrt(np.mean(noise ** 2))),
    }


def observed_wavelet(time, frequency_hz, frequency_scale=1.0, time_shift_ps=0.0, amplitude_scale=1.0):
    """Build a controlled observed source wavelet."""
    wavelet = ricker_wavelet(time, frequency_hz * float(frequency_scale))
    if time_shift_ps != 0.0:
        wavelet = shift_traces_zero_fill(wavelet, cfg.DT, float(time_shift_ps) * 1e-12)
    return float(amplitude_scale) * wavelet


def rank_candidates(candidates, top_k=None):
    ranked = sorted(candidates, key=lambda item: item["misfit"])
    if top_k is None:
        return ranked
    return ranked[:max(0, int(top_k))]


def best_curve_by_radius(candidates):
    """Return the best source-profiled candidate at each radius."""
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        current = best.get(radius)
        if current is None or candidate["misfit"] < current["misfit"]:
            best[radius] = candidate
    return [best[radius] for radius in sorted(best)]


def evaluate_source_profiled_grid(
        engine,
        observed,
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        modeled_frequency_scales,
        time_shift_values_s,
        fit_amplitude=True,
        progress_every=10):
    """Evaluate local x/z/r grid with source nuisance profiling."""
    frequency = engine.frequencies[0]
    observed_objective = engine._apply_objective_filter(observed)
    candidates = []
    total = len(x_values_mm) * len(z_values_mm) * len(radius_values_mm)
    started = time.time()
    count = 0
    for x_mm in x_values_mm:
        for z_mm in z_values_mm:
            for radius_mm in radius_values_mm:
                params = _params_from_mm(x_mm, z_mm, radius_mm)
                model = build_model_from_single_params(
                    params.as_array(),
                    geometry_mode=engine.geometry_mode,
                    subcell_samples=engine.subcell_samples,
                )
                synthetic_by_scale = {}
                for scale in modeled_frequency_scales:
                    wavelet = (
                        engine.wavelets[frequency]
                        if np.isclose(scale, 1.0, rtol=0.0, atol=1e-12)
                        else ricker_wavelet(engine.time, frequency * float(scale))
                    )
                    synthetic = engine._simulate_bscan(model, wavelet)
                    synthetic_by_scale[float(scale)] = engine._apply_objective_filter(synthetic)

                profile = source_profiled_ls(
                    observed_objective,
                    synthetic_by_scale,
                    engine.mute,
                    cfg.DT,
                    time_shift_values_s=time_shift_values_s,
                    fit_amplitude=fit_amplitude,
                )
                candidates.append({
                    "misfit": float(profile.misfit),
                    "params": params.as_mm(),
                    "source_profile": profile.as_dict(),
                })
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  Source-profiled polish: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def write_candidate_csv(path, candidates):
    """Write source-profiled candidates to CSV."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "misfit",
                "x_mm",
                "z_mm",
                "radius_mm",
                "source_frequency_scale",
                "source_time_shift_ps",
                "source_amplitude_scale",
            ],
        )
        writer.writeheader()
        for candidate in candidates:
            profile = candidate["source_profile"]
            writer.writerow({
                "misfit": candidate["misfit"],
                "x_mm": candidate["params"]["x_mm"],
                "z_mm": candidate["params"]["z_mm"],
                "radius_mm": candidate["params"]["radius_mm"],
                "source_frequency_scale": profile["frequency_scale"],
                "source_time_shift_ps": profile["time_shift_ps"],
                "source_amplitude_scale": profile["amplitude_scale"],
            })


def plot_radius_profile(candidates, save_path):
    """Plot best source-profiled objective by radius."""
    curve = best_curve_by_radius(candidates)
    fig, ax = plt.subplots(figsize=(8.8, 5.1), constrained_layout=True)
    radii = [item["params"]["radius_mm"] for item in curve]
    values = [item["misfit"] for item in curve]
    ax.plot(radii, values, marker="o", linewidth=1.8, markersize=4.5)
    if curve:
        best = min(curve, key=lambda item: item["misfit"])
        ax.scatter(
            [best["params"]["radius_mm"]],
            [best["misfit"]],
            s=54,
            edgecolors="black",
            linewidths=0.8,
            zorder=4,
        )
    ax.set_title("Source-Profiled Radius Polish")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Best objective over x/z/source profile")
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
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("1.0"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("0"))
    parser.add_argument("--fit-amplitude", action="store_true")
    parser.add_argument("--observed-frequency-scale", type=float, default=1.0)
    parser.add_argument("--observed-time-shift-ps", type=float, default=0.0)
    parser.add_argument("--observed-amplitude-scale", type=float, default=1.0)
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--run-name", default="single_rebar_source_profiled_polish")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    frequency_hz = args.frequency_ghz * 1e9
    engine = SingleRebarInversionEngine(
        true_params=default_single_rebar_truth(),
        initial_params=_params_from_mm(250.0, 90.0, 6.8),
        frequencies=(frequency_hz,),
        n_sources=args.sources,
        backend=args.backend,
    )
    obs_wavelet = observed_wavelet(
        engine.time,
        frequency_hz,
        frequency_scale=args.observed_frequency_scale,
        time_shift_ps=args.observed_time_shift_ps,
        amplitude_scale=args.observed_amplitude_scale,
    )
    observed_clean = engine._simulate_bscan(engine.true_model, obs_wavelet)
    observed, noise_stats = _add_noise(
        observed_clean,
        args.observed_noise_rms_fraction,
        args.noise_seed,
    )

    started = time.time()
    candidates = evaluate_source_profiled_grid(
        engine,
        observed,
        args.x_values_mm,
        args.z_values_mm,
        args.radius_values_mm,
        args.source_frequency_scales,
        [value * 1e-12 for value in args.source_time_shift_ps_values],
        fit_amplitude=args.fit_amplitude,
        progress_every=args.progress_every,
    )
    elapsed = time.time() - started
    ranked = rank_candidates(candidates)
    top_candidates = ranked[:args.top_k]
    margin = radius_margin_from_ranked(ranked)
    radius_curve = best_curve_by_radius(candidates)

    csv_path = os.path.join(data_dir, "source_profiled_polish_candidates.csv")
    plot_path = os.path.join(figures_dir, "source_profiled_radius_profile.png")
    write_candidate_csv(csv_path, candidates)
    plot_radius_profile(candidates, plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "x_values_mm": args.x_values_mm,
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
        "source_profile_grid": {
            "frequency_scales": args.source_frequency_scales,
            "time_shift_ps_values": args.source_time_shift_ps_values,
            "fit_amplitude": bool(args.fit_amplitude),
        },
        "observed_source": {
            "frequency_scale": float(args.observed_frequency_scale),
            "time_shift_ps": float(args.observed_time_shift_ps),
            "amplitude_scale": float(args.observed_amplitude_scale),
            "noise": noise_stats,
        },
        "elapsed_time_s": float(elapsed),
        "candidate_count": len(candidates),
        "margin": margin,
        "top_candidates": top_candidates,
        "best_curve_by_radius": radius_curve,
        "paths": {
            "candidate_csv": csv_path,
            "radius_profile_plot": plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "source_profiled_polish_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "single_rebar_source_profiled_polish",
        {
            "summary_path": summary_path,
            "candidate_csv": csv_path,
            "radius_profile_plot": plot_path,
        },
    )
    print(
        f"Best r={margin['best_radius_mm']} mm, "
        f"next r={margin['next_radius_mm']} mm, "
        f"margin={margin['radius_margin_abs']}"
    )
    if top_candidates:
        print(f"Best source profile: {top_candidates[0]['source_profile']}")
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
