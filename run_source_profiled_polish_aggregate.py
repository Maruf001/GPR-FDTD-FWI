#!/usr/bin/env python3
"""Aggregate source-profiled polish summaries."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
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

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


SUMMARY_RELATIVE_PATH = Path("data") / "source_profiled_polish_summary.json"


def run_id_from_path(path):
    """Return the leading numbered experiment id when present."""
    path = Path(path)
    for part in (path.name, path.parent.name, path.parent.parent.name):
        match = re.match(r"^(\d{3,})_", part)
        if match:
            return match.group(1)
    return path.name


def first_noise_seed(summary):
    """Return the first observed-noise seed from a source-profiled summary."""
    noise = summary.get("observed_source", {}).get("noise", {})
    if isinstance(noise, dict):
        for item in noise.values():
            if isinstance(item, dict) and "seed" in item:
                return int(item["seed"])
    return 0


def interval_width(interval):
    """Return a non-negative radius interval width."""
    lower = float(interval.get("radius_min_mm", np.nan))
    upper = float(interval.get("radius_max_mm", np.nan))
    if not np.isfinite(lower) or not np.isfinite(upper):
        return np.nan
    return max(0.0, upper - lower)


def summarize_source_profiled_summary(summary, run_dir):
    """Flatten one source-profiled polish summary into one aggregate row."""
    margin = summary.get("margin", {})
    ambiguity = summary.get("radius_ambiguity", {})
    exact = ambiguity.get("exact_tie", {})
    weak = ambiguity.get("weak_interval", {})
    truth = summary.get("truth_params", {})
    frequency_weights = summary.get("frequency_weights", {})
    source_grid = summary.get("source_profile_grid", {})
    return {
        "run_id": run_id_from_path(run_dir),
        "run_dir": str(run_dir),
        "noise_seed": first_noise_seed(summary),
        "sources": int(summary.get("sources", 0)),
        "frequencies_ghz": ",".join(str(value) for value in summary.get("frequencies_ghz", [])),
        "frequency_weights": ",".join(
            f"{key}:{frequency_weights[key]}"
            for key in sorted(frequency_weights)
        ),
        "fit_amplitude": bool(source_grid.get("fit_amplitude", False)),
        "geometry_mode": summary.get("geometry_mode", ""),
        "subcell_samples": int(summary.get("subcell_samples", 0)),
        "truth_radius_mm": float(truth.get("radius_mm", np.nan)),
        "best_radius_mm": float(margin.get("best_radius_mm", np.nan)),
        "next_radius_mm": float(margin.get("next_radius_mm", np.nan)),
        "radius_error_mm": float(abs(float(margin.get("best_radius_mm", np.nan)) - float(truth.get("radius_mm", np.nan)))),
        "radius_margin_abs": float(margin.get("radius_margin_abs", 0.0)),
        "radius_margin_rel": float(margin.get("radius_margin_rel", 0.0)),
        "exact_radius_min_mm": float(exact.get("radius_min_mm", np.nan)),
        "exact_radius_max_mm": float(exact.get("radius_max_mm", np.nan)),
        "exact_radius_count": int(exact.get("radius_count", 0)),
        "weak_radius_min_mm": float(weak.get("radius_min_mm", np.nan)),
        "weak_radius_max_mm": float(weak.get("radius_max_mm", np.nan)),
        "weak_radius_count": int(weak.get("radius_count", 0)),
        "exact_interval_width_mm": interval_width(exact),
        "weak_interval_width_mm": interval_width(weak),
        "elapsed_time_s": float(summary.get("elapsed_time_s", 0.0)),
    }


def write_rows_csv(path, rows):
    """Write aggregate rows to CSV."""
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_aggregate(rows, save_path):
    """Plot source-profiled polish aggregate metrics."""
    labels = [row["run_id"] for row in rows]
    x = np.arange(len(rows))
    best_radius = np.asarray([row["best_radius_mm"] for row in rows], dtype=np.float64)
    truth_radius = np.asarray([row["truth_radius_mm"] for row in rows], dtype=np.float64)
    margins = np.asarray([row["radius_margin_abs"] for row in rows], dtype=np.float64)
    weak_width = np.asarray([row["weak_interval_width_mm"] for row in rows], dtype=np.float64)
    runtime_min = np.asarray([row["elapsed_time_s"] / 60.0 for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(4, 1, figsize=(9.8, 9.2), constrained_layout=True, sharex=True)
    axes[0].plot(x, best_radius, marker="o", linewidth=1.8, label="best radius")
    axes[0].plot(x, truth_radius, color="black", linestyle="--", linewidth=1.2, label="truth radius")
    axes[0].set_ylabel("Radius [mm]")
    axes[0].set_title("Source-Profiled Polish Aggregate")
    axes[0].legend(loc="best", fontsize=8, frameon=True)

    axes[1].bar(x, margins, color="#4C78A8")
    axes[1].axhline(1.0e-3, color="black", linestyle="--", linewidth=1.0, label="strong abs threshold")
    axes[1].set_ylabel("Radius margin")
    axes[1].legend(loc="best", fontsize=8, frameon=True)

    axes[2].bar(x, weak_width, color="#E45756")
    axes[2].set_ylabel("Weak interval width [mm]")

    axes[3].bar(x, runtime_min, color="#2E7D32")
    axes[3].set_ylabel("Runtime [min]")
    axes[3].set_xlabel("Experiment")

    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=35, ha="right")
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, rows):
    """Write plain-language notes for the aggregate figure."""
    best_radii = sorted(set(row["best_radius_mm"] for row in rows))
    truth_radii = sorted(set(row["truth_radius_mm"] for row in rows))
    weak_ranges = sorted(set((row["weak_radius_min_mm"], row["weak_radius_max_mm"]) for row in rows))
    frequencies = sorted(set(row["frequencies_ghz"] for row in rows))
    weight_modes = sorted(set(row["frequency_weights"] for row in rows))
    geometries = sorted(set(row["geometry_mode"] for row in rows))
    amplitude_modes = sorted(set(row["fit_amplitude"] for row in rows))
    shifted = [
        (row["run_id"], row["best_radius_mm"], row["radius_error_mm"])
        for row in rows
        if row["radius_error_mm"] > 0.0
    ]
    if not shifted:
        conclusion = (
            "All variants keep zero point-radius error. When weak intervals are nonzero, "
            "the report should include both the point estimate and the interval support "
            "rather than only a single-size claim."
        )
    else:
        conclusion = (
            f"Best radius is not consistent across all variants. Shifted runs are `{shifted}`. "
            "Treat any variant that improves margin by moving away from truth as a diagnostic "
            "failure, not an improved inversion result."
        )
    text = f"""# Figure Notes

## 1. `source_profiled_polish_aggregate.png` - fixed-location radius robustness

This figure compares source-profiled radius-polish runs. Source-profiled means
the waveform comparison fits small source-wavelet changes, such as frequency
scale, time shift, and amplitude, while testing geometry. FWI means
full-waveform inversion: simulated radar traces are compared with observed
traces.

The first panel shows the best radius for each run against the known synthetic
truth. The second panel shows the best-radius margin, meaning the objective
gap between the best radius and the next tested radius. The third panel shows
the weak interval width: the radius range close enough to the best objective
that a single confident size would be misleading. The fourth panel shows
runtime.

Main result: truth radii are `{truth_radii}` mm and best radii across these
runs are `{best_radii}` mm. Frequencies are `{frequencies}` GHz and geometry
modes are `{geometries}`. Frequency-weight modes are `{weight_modes}`.
Amplitude-fit modes are `{amplitude_modes}`. Weak intervals across these runs
are `{weak_ranges}` mm.

{conclusion}
"""
    Path(path).write_text(text, encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dirs", nargs="+", required=True)
    parser.add_argument("--run-name", default="source_profiled_polish_aggregate")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    rows = []
    for run_dir in args.run_dirs:
        summary_path = Path(run_dir) / SUMMARY_RELATIVE_PATH
        with summary_path.open("r", encoding="utf-8") as handle:
            summary = json.load(handle)
        rows.append(summarize_source_profiled_summary(summary, run_dir))
    rows.sort(key=lambda row: row["run_id"])

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    csv_path = data_dir / "source_profiled_polish_aggregate.csv"
    json_path = data_dir / "source_profiled_polish_aggregate.json"
    plot_path = figures_dir / "source_profiled_polish_aggregate.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_rows_csv(csv_path, rows)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({"rows": rows}, handle, indent=2)
    plot_aggregate(rows, plot_path)
    plt.close("all")
    write_figure_notes(notes_path, rows)
    write_run_manifest(
        str(outdir),
        "source_profiled_polish_aggregate",
        {"csv": str(csv_path), "json": str(json_path), "plot": str(plot_path)},
    )
    print(f"Rows: {len(rows)}")
    print(f"Best radii: {[row['best_radius_mm'] for row in rows]}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
