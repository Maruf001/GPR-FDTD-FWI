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
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    default_single_rebar_truth,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
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
        x_mm,
        z_mm,
        radius_values_mm,
        concrete_epsr_values,
        rebar_sigma_values,
        progress_every=10):
    """Evaluate candidate material/radius combinations at fixed x/z."""
    frequency = engine.frequencies[0]
    observed = engine.d_obs_objective_by_frequency[frequency]
    obs_norm = engine.obs_norm_by_frequency[frequency]
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
                )
                synthetic = engine._simulate_bscan(model, engine.wavelets[frequency])
                synthetic = engine._apply_objective_filter(synthetic)
                residual = (synthetic - observed) * engine.mute[:, None]
                misfit = 0.5 * float(np.sum(residual ** 2)) / obs_norm
                candidates.append({
                    "misfit": float(misfit),
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
            ],
        )
        writer.writeheader()
        for candidate in candidates:
            writer.writerow({
                "misfit": candidate["misfit"],
                "x_mm": candidate["params"]["x_mm"],
                "z_mm": candidate["params"]["z_mm"],
                "radius_mm": candidate["params"]["radius_mm"],
                "concrete_epsr": candidate["material"]["concrete_epsr"],
                "rebar_sigma": candidate["material"]["rebar_sigma"],
                "rebar_log10_sigma": candidate["material"]["rebar_log10_sigma"],
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--x-mm", type=float, default=250.0)
    parser.add_argument("--z-mm", type=float, default=90.0)
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--concrete-epsr-values", type=parse_float_values, default=parse_float_values("5.5,6.0,6.5"))
    parser.add_argument("--rebar-log10-sigma-values", type=parse_log10_sigma_values, default=parse_log10_sigma_values("5,6,7"))
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--run-name", default="single_rebar_material_tradeoff")
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
        initial_params=_params(args.x_mm, args.z_mm, 6.8),
        frequencies=(args.frequency_ghz * 1e9,),
        n_sources=args.sources,
        backend=args.backend,
    )
    candidates = evaluate_tradeoff_grid(
        engine,
        args.x_mm,
        args.z_mm,
        args.radius_values_mm,
        args.concrete_epsr_values,
        args.rebar_log10_sigma_values,
        progress_every=args.progress_every,
    )
    ranked = sorted(candidates, key=lambda item: item["misfit"])
    top_candidates = ranked[:args.top_k]
    curve = best_curve_by_radius(candidates)
    margin = radius_margin_from_ranked(ranked)

    csv_path = os.path.join(data_dir, "material_tradeoff_matrix.csv")
    plot_path = os.path.join(figures_dir, "material_profiled_radius.png")
    write_csv(csv_path, candidates)
    plot_radius_profile(candidates, plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "x_mm": args.x_mm,
        "z_mm": args.z_mm,
        "radius_values_mm": args.radius_values_mm,
        "concrete_epsr_values": args.concrete_epsr_values,
        "rebar_sigma_values": args.rebar_log10_sigma_values,
        "candidate_count": len(candidates),
        "margin": margin,
        "top_candidates": top_candidates,
        "best_curve_by_radius": curve,
        "paths": {
            "csv": csv_path,
            "plot": plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "material_tradeoff_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    write_run_manifest(
        outdir,
        "single_rebar_material_tradeoff",
        {
            "summary_path": summary_path,
            "csv": csv_path,
            "plot": plot_path,
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
