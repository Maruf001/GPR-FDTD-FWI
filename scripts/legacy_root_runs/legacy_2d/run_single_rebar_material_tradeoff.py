#!/usr/bin/env python3
"""Evaluate radius/material tradeoffs for the one-rebar problem."""

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
from core.materials import MaterialModel  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import ricker_wavelet  # noqa: E402
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.radius_confidence import radius_interval_from_curve  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import (  # noqa: E402
    _add_noise_by_frequency,
    format_metric,
    format_mm_value,
    observed_wavelet,
    source_profiled_multifrequency_ls,
)
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def parse_float_values(text):
    """Parse comma-separated floats."""
    values = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    return values


def parse_log10_sigma_values(text):
    """Parse comma-separated log10 conductivity values into S/m."""
    return [10.0 ** value for value in parse_float_values(text)]


def build_single_rebar_material_model(
        x_center,
        z_center,
        radius,
        concrete_epsr=cfg.CONCRETE_EPSR,
        concrete_sigma=cfg.CONCRETE_SIGMA,
        rebar_epsr=cfg.REBAR_EPSR,
        rebar_sigma=cfg.REBAR_SIGMA,
        geometry_mode="hard",
        subcell_samples=5):
    """Build a one-rebar model with explicit material values."""
    model = MaterialModel(
        cfg.NZ,
        cfg.NX,
        eps_r_bg=cfg.AIR_EPSR,
        sigma_bg=cfg.AIR_SIGMA,
        mu_r_bg=cfg.MU_R,
    )
    iz_concrete_top = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
    model.set_region(
        slice(iz_concrete_top, cfg.NZ),
        slice(0, cfg.NX),
        eps_r=concrete_epsr,
        sigma=concrete_sigma,
    )
    if geometry_mode == "hard":
        model.add_circle(
            z_center_m=z_center,
            x_center_m=x_center,
            radius_m=radius,
            eps_r=rebar_epsr,
            sigma=rebar_sigma,
            dz=cfg.DZ,
            dx=cfg.DX,
            npml=cfg.NPML,
        )
    elif geometry_mode == "subcell":
        model.add_circle_subcell(
            z_center_m=z_center,
            x_center_m=x_center,
            radius_m=radius,
            eps_r=rebar_epsr,
            sigma=rebar_sigma,
            dz=cfg.DZ,
            dx=cfg.DX,
            npml=cfg.NPML,
            samples=subcell_samples,
        )
    else:
        raise ValueError(f"unsupported geometry mode: {geometry_mode}")
    return model


def _params(x_mm, z_mm, radius_mm):
    return SingleRebarParams(
        x=x_mm / 1000.0,
        z=z_mm / 1000.0,
        radius=radius_mm / 1000.0,
    )


def evaluate_tradeoff_grid(
        engine,
        observed_by_frequency,
        x_mm,
        z_mm,
        radius_values_mm,
        concrete_epsr_values,
        rebar_sigma_values,
        modeled_frequency_scales=(1.0,),
        time_shift_values_s=(0.0,),
        fit_amplitude=False,
        geometry_mode="hard",
        subcell_samples=5,
        progress_every=10):
    """Evaluate candidate material/radius combinations at fixed x/z."""
    candidates = []
    total = len(radius_values_mm) * len(concrete_epsr_values) * len(rebar_sigma_values)
    started = time.time()
    count = 0
    for concrete_epsr in concrete_epsr_values:
        for rebar_sigma in rebar_sigma_values:
            for radius_mm in radius_values_mm:
                params = _params(x_mm, z_mm, radius_mm)
                model = build_single_rebar_material_model(
                    params.x,
                    params.z,
                    params.radius,
                    concrete_epsr=concrete_epsr,
                    rebar_sigma=rebar_sigma,
                    geometry_mode=geometry_mode,
                    subcell_samples=subcell_samples,
                )
                synthetic_by_frequency_scale = {}
                for frequency in engine.frequencies:
                    synthetic_by_frequency_scale[frequency] = {}
                    for scale in modeled_frequency_scales:
                        wavelet = ricker_wavelet(engine.time, frequency * float(scale))
                        synthetic = engine._simulate_bscan(model, wavelet)
                        synthetic_by_frequency_scale[frequency][float(scale)] = (
                            engine._apply_objective_filter(synthetic)
                        )
                source_profile = source_profiled_multifrequency_ls(
                    observed_by_frequency,
                    synthetic_by_frequency_scale,
                    engine.mute,
                    cfg.DT,
                    time_shift_values_s=time_shift_values_s,
                    fit_amplitude=fit_amplitude,
                )
                candidates.append({
                    "misfit": float(source_profile["misfit"]),
                    "params": {
                        "x_mm": float(x_mm),
                        "z_mm": float(z_mm),
                        "radius_mm": float(radius_mm),
                    },
                    "material": {
                        "concrete_epsr": float(concrete_epsr),
                        "rebar_sigma": float(rebar_sigma),
                        "rebar_log10_sigma": float(np.log10(rebar_sigma)),
                    },
                    "source_profile": source_profile,
                })
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  Material tradeoff grid: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def best_curve_by_radius(candidates):
    """Return best material choice at each radius."""
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        current = best.get(radius)
        if current is None or candidate["misfit"] < current["misfit"]:
            best[radius] = candidate
    return [best[radius] for radius in sorted(best)]


def write_csv(path, candidates):
    """Write material tradeoff candidates."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "misfit",
                "x_mm",
                "z_mm",
                "radius_mm",
                "concrete_epsr",
                "rebar_sigma",
                "rebar_log10_sigma",
                "source_frequency_scale",
                "source_time_shift_ps",
                "source_amplitude_scale",
            ],
        )
        writer.writeheader()
        for candidate in candidates:
            source_profile = candidate.get("source_profile", {})
            writer.writerow({
                "misfit": candidate["misfit"],
                "x_mm": candidate["params"]["x_mm"],
                "z_mm": candidate["params"]["z_mm"],
                "radius_mm": candidate["params"]["radius_mm"],
                "concrete_epsr": candidate["material"]["concrete_epsr"],
                "rebar_sigma": candidate["material"]["rebar_sigma"],
                "rebar_log10_sigma": candidate["material"]["rebar_log10_sigma"],
                "source_frequency_scale": source_profile.get("frequency_scale"),
                "source_time_shift_ps": source_profile.get("time_shift_ps"),
                "source_amplitude_scale": source_profile.get("amplitude_scale"),
            })


def plot_radius_profile(candidates, save_path):
    """Plot best-over-material objective versus radius."""
    curve = best_curve_by_radius(candidates)
    fig, ax = plt.subplots(figsize=(8.5, 5.0), constrained_layout=True)
    radius = [item["params"]["radius_mm"] for item in curve]
    misfit = [item["misfit"] for item in curve]
    ax.plot(radius, misfit, marker="o", linewidth=1.8, markersize=4.5)
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
    ax.set_title("Best Material-Profiled Radius Evidence")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Best objective over material grid")
    ax.grid(True, alpha=0.25)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def build_observed_by_frequency(
        engine,
        observed_frequency_scale=1.0,
        observed_time_shift_ps=0.0,
        observed_amplitude_scale=1.0,
        observed_noise_rms_fraction=0.0,
        noise_seed=13):
    """Build objective-filtered observed data with controlled source mismatch."""
    clean_by_frequency = {}
    for frequency in engine.frequencies:
        wavelet = observed_wavelet(
            engine.time,
            frequency,
            frequency_scale=observed_frequency_scale,
            time_shift_ps=observed_time_shift_ps,
            amplitude_scale=observed_amplitude_scale,
        )
        clean_by_frequency[frequency] = engine._simulate_bscan(engine.true_model, wavelet)
    observed_raw_by_frequency, noise_stats = _add_noise_by_frequency(
        clean_by_frequency,
        observed_noise_rms_fraction,
        noise_seed,
    )
    observed_by_frequency = {
        frequency: engine._apply_objective_filter(observed)
        for frequency, observed in observed_raw_by_frequency.items()
    }
    return observed_by_frequency, noise_stats


def write_figure_notes(path, summary):
    """Write plain-language notes for material tradeoff figures."""
    best = summary["top_candidates"][0] if summary.get("top_candidates") else None
    margin = summary.get("margin", {})
    weak_interval = summary.get("radius_ambiguity", {}).get("weak_interval", {})
    best_text = "No top candidate was recorded."
    if best is not None:
        best_text = (
            "Main result: the best candidate is "
            f"r={format_mm_value(best['params']['radius_mm'])} mm, "
            f"concrete relative permittivity={best['material']['concrete_epsr']:.3g}, "
            f"and rebar log10 conductivity={best['material']['rebar_log10_sigma']:.3g}. "
            f"The best-radius margin is {format_metric(margin.get('radius_margin_abs'))}."
        )
    text = f"""# Figure Notes

## 1. `material_profiled_radius.png` - material-profiled radius evidence

This plot shows the best waveform objective value at each tested rebar radius
after profiling over a small material grid. Profiling means the code tries
several concrete permittivity and rebar conductivity values for each radius
and keeps the best material choice at that radius.

The objective is still a full-waveform inversion (FWI) comparison: simulated
radar traces are compared with observed traces. Source profiling is also
included when enabled by the command, so frequency scale, time shift, and
amplitude can be treated as nuisance parameters rather than hidden geometry
errors.

{best_text} The weak radius interval is
`{weak_interval.get('radius_min_mm')}-{weak_interval.get('radius_max_mm')}` mm.
A broad interval means material/source freedom can mimic radius changes closely
enough that the size should be reported as an interval.
"""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--truth-x-mm", type=float, default=250.0)
    parser.add_argument("--truth-z-mm", type=float, default=90.0)
    parser.add_argument("--truth-radius-mm", type=float, default=6.0)
    parser.add_argument("--x-mm", type=float, default=250.0)
    parser.add_argument("--z-mm", type=float, default=90.0)
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--concrete-epsr-values", type=parse_float_values, default=parse_float_values("5.5,6.0,6.5"))
    parser.add_argument("--rebar-log10-sigma-values", type=parse_log10_sigma_values, default=parse_log10_sigma_values("5,6,7"))
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("1.0"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("0"))
    parser.add_argument("--fit-amplitude", action="store_true")
    parser.add_argument("--observed-frequency-scale", type=float, default=1.0)
    parser.add_argument("--observed-time-shift-ps", type=float, default=0.0)
    parser.add_argument("--observed-amplitude-scale", type=float, default=1.0)
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--run-name", default="single_rebar_material_tradeoff")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    truth_params = _params(args.truth_x_mm, args.truth_z_mm, args.truth_radius_mm)
    engine = SingleRebarInversionEngine(
        true_params=truth_params,
        initial_params=_params(args.x_mm, args.z_mm, args.truth_radius_mm + 0.8),
        frequencies=(args.frequency_ghz * 1e9,),
        n_sources=args.sources,
        backend=args.backend,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    observed_by_frequency, noise_stats = build_observed_by_frequency(
        engine,
        observed_frequency_scale=args.observed_frequency_scale,
        observed_time_shift_ps=args.observed_time_shift_ps,
        observed_amplitude_scale=args.observed_amplitude_scale,
        observed_noise_rms_fraction=args.observed_noise_rms_fraction,
        noise_seed=args.noise_seed,
    )
    candidates = evaluate_tradeoff_grid(
        engine,
        observed_by_frequency,
        args.x_mm,
        args.z_mm,
        args.radius_values_mm,
        args.concrete_epsr_values,
        args.rebar_log10_sigma_values,
        modeled_frequency_scales=args.source_frequency_scales,
        time_shift_values_s=[value * 1e-12 for value in args.source_time_shift_ps_values],
        fit_amplitude=args.fit_amplitude,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        progress_every=args.progress_every,
    )
    ranked = sorted(candidates, key=lambda item: item["misfit"])
    top_candidates = ranked[:args.top_k]
    curve = best_curve_by_radius(candidates)
    margin = radius_margin_from_ranked(ranked)
    radius_ambiguity = {
        "exact_tie": radius_interval_from_curve(curve, abs_tolerance=1e-12, rel_tolerance=0.0),
        "weak_interval": radius_interval_from_curve(curve, abs_tolerance=1e-3, rel_tolerance=5e-3),
    }

    csv_path = os.path.join(data_dir, "material_tradeoff_matrix.csv")
    plot_path = os.path.join(figures_dir, "material_profiled_radius.png")
    notes_path = os.path.join(figures_dir, "FIGURE_NOTES.md")
    write_csv(csv_path, candidates)
    plot_radius_profile(candidates, plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "truth_params": truth_params.as_mm(),
        "x_mm": args.x_mm,
        "z_mm": args.z_mm,
        "radius_values_mm": args.radius_values_mm,
        "concrete_epsr_values": args.concrete_epsr_values,
        "rebar_sigma_values": args.rebar_log10_sigma_values,
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
        "geometry_mode": args.geometry_mode,
        "subcell_samples": int(args.subcell_samples),
        "candidate_count": len(candidates),
        "margin": margin,
        "radius_ambiguity": radius_ambiguity,
        "top_candidates": top_candidates,
        "best_curve_by_radius": curve,
        "paths": {
            "csv": csv_path,
            "plot": plot_path,
            "figure_notes": notes_path,
        },
    }
    summary_path = os.path.join(data_dir, "material_tradeoff_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    write_figure_notes(notes_path, summary)
    write_run_manifest(
        outdir,
        "single_rebar_material_tradeoff",
        {
            "summary_path": summary_path,
            "csv": csv_path,
            "plot": plot_path,
            "figure_notes": notes_path,
        },
    )
    print(
        f"Best r={margin['best_radius_mm']} mm, "
        f"next r={margin['next_radius_mm']} mm, "
        f"margin={margin['radius_margin_abs']}"
    )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
