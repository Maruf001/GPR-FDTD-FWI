#!/usr/bin/env python3
"""Diagnose radius quantization in one-rebar material geometry."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
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

from core.geometry import build_rebar_model, build_single_rebar_model  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def log_sigma(model, floor=1e-12):
    """Return log10 conductivity with a floor for air cells."""
    return np.log10(np.maximum(model.sigma, float(floor)))


def material_distance(model_a, model_b):
    """Return material-space distances between two models."""
    return {
        "epsilon_l1": float(np.sum(np.abs(model_a.epsilon_r - model_b.epsilon_r))),
        "log_sigma_l1": float(np.sum(np.abs(log_sigma(model_a) - log_sigma(model_b)))),
    }


def material_contrast_metrics(model, baseline):
    """Return material contrast metrics relative to the no-rebar baseline."""
    distances = material_distance(model, baseline)
    eps_delta = np.abs(model.epsilon_r - baseline.epsilon_r)
    sigma_delta = np.abs(log_sigma(model) - log_sigma(baseline))
    active = (eps_delta > 1e-12) | (sigma_delta > 1e-12)
    return {
        "active_cell_count": int(np.count_nonzero(active)),
        "epsilon_l1_contrast": distances["epsilon_l1"],
        "log_sigma_l1_contrast": distances["log_sigma_l1"],
    }


def geometry_quantization_rows(
        radii_mm,
        x_mm,
        z_mm,
        geometry_modes=("hard", "subcell"),
        subcell_samples=5):
    """Build geometry quantization rows for hard and subcell circle models."""
    rows = []
    for geometry_mode in geometry_modes:
        baseline = build_rebar_model(rebars=[], geometry_mode=geometry_mode, subcell_samples=subcell_samples)
        previous_model = None
        for radius_mm in radii_mm:
            model = build_single_rebar_model(
                x_mm / 1000.0,
                z_mm / 1000.0,
                radius_mm / 1000.0,
                geometry_mode=geometry_mode,
                subcell_samples=subcell_samples,
            )
            metrics = material_contrast_metrics(model, baseline)
            if previous_model is None:
                adjacent = {"epsilon_l1": np.nan, "log_sigma_l1": np.nan}
            else:
                adjacent = material_distance(model, previous_model)
            rows.append({
                "geometry_mode": geometry_mode,
                "radius_mm": float(radius_mm),
                "active_cell_count": metrics["active_cell_count"],
                "epsilon_l1_contrast": metrics["epsilon_l1_contrast"],
                "log_sigma_l1_contrast": metrics["log_sigma_l1_contrast"],
                "adjacent_epsilon_l1_delta": adjacent["epsilon_l1"],
                "adjacent_log_sigma_l1_delta": adjacent["log_sigma_l1"],
            })
            previous_model = model
    return rows


def write_rows_csv(path, rows):
    """Write geometry quantization rows to CSV."""
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_quantization(rows, save_path):
    """Plot material quantization metrics across radius."""
    modes = list(dict.fromkeys(row["geometry_mode"] for row in rows))
    colors = {"hard": "#4C78A8", "subcell": "#E45756"}
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 8.0), constrained_layout=True, sharex=True)
    for mode in modes:
        mode_rows = [row for row in rows if row["geometry_mode"] == mode]
        radii = [row["radius_mm"] for row in mode_rows]
        axes[0].plot(
            radii,
            [row["active_cell_count"] for row in mode_rows],
            marker="o",
            linewidth=1.8,
            color=colors.get(mode),
            label=mode,
        )
        axes[1].plot(
            radii,
            [row["log_sigma_l1_contrast"] for row in mode_rows],
            marker="o",
            linewidth=1.8,
            color=colors.get(mode),
            label=mode,
        )
        axes[2].plot(
            radii,
            [row["adjacent_log_sigma_l1_delta"] for row in mode_rows],
            marker="o",
            linewidth=1.8,
            color=colors.get(mode),
            label=mode,
        )

    axes[0].set_title("Material Geometry Quantization Across Radius")
    axes[0].set_ylabel("Changed cells")
    axes[1].set_ylabel("Log-conductivity contrast")
    axes[2].set_ylabel("Adjacent log-conductivity delta")
    axes[2].set_xlabel("Radius [mm]")
    for ax in axes:
        ax.grid(True, alpha=0.25)
        ax.legend(loc="best", fontsize=8, frameon=True)
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, rows, grid_step_mm):
    """Write plain-language notes for the quantization figure."""
    hard_rows = {row["radius_mm"]: row for row in rows if row["geometry_mode"] == "hard"}
    subcell_rows = {row["radius_mm"]: row for row in rows if row["geometry_mode"] == "subcell"}
    hard_41_delta = hard_rows.get(4.1, {}).get("adjacent_log_sigma_l1_delta", np.nan)
    subcell_41_delta = subcell_rows.get(4.1, {}).get("adjacent_log_sigma_l1_delta", np.nan)
    text = f"""# Figure Notes

## 1. `geometry_quantization_metrics.png` - radius rasterization check

This figure checks whether changing the requested rebar radius actually changes
the material model used by the finite-difference time-domain solver. FDTD means
finite-difference time-domain: the wave simulation only sees the gridded
permittivity and conductivity arrays, not the continuous circle requested by
the command line.

The top panel counts grid cells whose material differs from a no-rebar
baseline. The middle panel sums the log-conductivity contrast relative to that
baseline. The bottom panel compares each radius to the previous radius; a zero
adjacent delta means those two radius settings produced identical conductivity
geometry on the grid.

Main result: at the `{float(grid_step_mm):.3g} mm` grid, the hard-grid
`4.0 -> 4.1 mm` adjacent log-conductivity delta is `{hard_41_delta:.3f}`. The
subcell `4.0 -> 4.1 mm` delta is `{subcell_41_delta:.3f}`. A zero hard-grid
delta means no waveform objective can distinguish those two radii unless the
geometry representation changes.
"""
    Path(path).write_text(text, encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--x-mm", type=float, default=250.0)
    parser.add_argument("--z-mm", type=float, default=70.0)
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("3.7:4.3:0.1"))
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--run-name", default="single_rebar_geometry_quantization_diagnostic")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    _override_grid(args.grid_step_mm)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    rows = geometry_quantization_rows(
        args.radius_values_mm,
        args.x_mm,
        args.z_mm,
        subcell_samples=args.subcell_samples,
    )
    csv_path = data_dir / "geometry_quantization_metrics.csv"
    json_path = data_dir / "geometry_quantization_metrics.json"
    plot_path = figures_dir / "geometry_quantization_metrics.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_rows_csv(csv_path, rows)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({"rows": rows}, handle, indent=2)
    plot_quantization(rows, plot_path)
    plt.close("all")
    write_figure_notes(notes_path, rows, args.grid_step_mm)
    write_run_manifest(
        str(outdir),
        "single_rebar_geometry_quantization_diagnostic",
        {
            "csv": str(csv_path),
            "json": str(json_path),
            "plot": str(plot_path),
        },
    )
    hard_zeros = [
        row["radius_mm"]
        for row in rows
        if row["geometry_mode"] == "hard" and row["adjacent_log_sigma_l1_delta"] == 0.0
    ]
    print(f"Hard-grid zero adjacent deltas at radii: {hard_zeros}")
    print(f"Wrote CSV: {csv_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
