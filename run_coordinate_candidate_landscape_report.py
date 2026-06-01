#!/usr/bin/env python3
"""Plot z/radius objective landscapes from coordinate optimizer candidates."""

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

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def read_candidate_rows(path):
    """Read a coordinate candidate CSV."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def filter_case_rows(rows, case_label):
    """Return rows for one observed case."""
    selected = [row for row in rows if row.get("case_label") == case_label]
    if not selected:
        raise ValueError(f"no candidate rows found for case_label={case_label!r}")
    return selected


def best_candidate(rows):
    """Return the lowest-misfit candidate row."""
    return min(rows, key=lambda row: float(row["misfit"]))


def landscape_rows(rows):
    """Reduce candidate rows to the best x value for each z/radius pair."""
    best_by_z_radius = {}
    for row in rows:
        key = (float(row["z_mm"]), float(row["radius_mm"]))
        current = best_by_z_radius.get(key)
        if current is None or float(row["misfit"]) < float(current["misfit"]):
            best_by_z_radius[key] = dict(row)
    return [
        best_by_z_radius[key]
        for key in sorted(best_by_z_radius, key=lambda item: (item[0], item[1]))
    ]


def write_landscape_csv(path, rows):
    """Write reduced landscape rows."""
    fieldnames = [
        "z_mm",
        "radius_mm",
        "best_x_mm",
        "misfit",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "z_mm": float(row["z_mm"]),
                "radius_mm": float(row["radius_mm"]),
                "best_x_mm": float(row["x_mm"]),
                "misfit": float(row["misfit"]),
                "source_frequency_scale": row.get("source_frequency_scale"),
                "source_time_shift_ps": row.get("source_time_shift_ps"),
                "source_amplitude_scale": row.get("source_amplitude_scale"),
            })


def axis_edges(values, fallback_step=0.5):
    """Return monotone bin edges for pcolormesh-like heatmaps."""
    values = np.asarray(sorted({float(value) for value in values}), dtype=np.float64)
    if values.size == 0:
        raise ValueError("at least one axis value is required")
    if values.size == 1:
        half = 0.5 * float(fallback_step)
        return np.asarray([values[0] - half, values[0] + half], dtype=np.float64)
    edges = np.empty(values.size + 1, dtype=np.float64)
    edges[1:-1] = 0.5 * (values[:-1] + values[1:])
    edges[0] = values[0] - 0.5 * (values[1] - values[0])
    edges[-1] = values[-1] + 0.5 * (values[-1] - values[-2])
    return edges


def landscape_matrix(rows):
    """Return sorted z/radius values and a misfit matrix indexed by z, radius."""
    z_values = sorted({float(row["z_mm"]) for row in rows})
    radius_values = sorted({float(row["radius_mm"]) for row in rows})
    matrix = np.full((len(z_values), len(radius_values)), np.nan, dtype=np.float64)
    z_index = {value: index for index, value in enumerate(z_values)}
    radius_index = {value: index for index, value in enumerate(radius_values)}
    for row in rows:
        matrix[z_index[float(row["z_mm"])], radius_index[float(row["radius_mm"])]] = float(row["misfit"])
    return z_values, radius_values, matrix


def truth_rank(rows, truth_z_mm, truth_radius_mm):
    """Return rank and row for the exact truth z/radius pair, if sampled."""
    if truth_z_mm is None or truth_radius_mm is None:
        return None
    ranked = sorted(rows, key=lambda row: float(row["misfit"]))
    for index, row in enumerate(ranked, start=1):
        if (
            abs(float(row["z_mm"]) - float(truth_z_mm)) <= 1.0e-9
            and abs(float(row["radius_mm"]) - float(truth_radius_mm)) <= 1.0e-9
        ):
            return {"rank": index, "row": row}
    return {"rank": None, "row": None}


def plot_landscape(
        rows,
        case_label,
        save_path,
        truth_z_mm=None,
        truth_radius_mm=None,
        title_suffix=""):
    """Plot best-over-x misfit for each z/radius pair."""
    z_values, radius_values, matrix = landscape_matrix(rows)
    best = best_candidate(rows)
    radius_edges = axis_edges(radius_values)
    z_edges = axis_edges(z_values)

    fig, ax = plt.subplots(figsize=(8.8, 6.2), constrained_layout=True)
    mesh = ax.pcolormesh(
        radius_edges,
        z_edges,
        matrix,
        shading="auto",
        cmap="viridis",
    )
    colorbar = fig.colorbar(mesh, ax=ax, pad=0.02, shrink=0.88)
    colorbar.set_label("Source-profiled misfit")
    ax.scatter(
        [float(best["radius_mm"])],
        [float(best["z_mm"])],
        s=90,
        marker="o",
        facecolor="none",
        edgecolor="white",
        linewidth=1.8,
        label="best sampled pair",
    )
    if truth_z_mm is not None and truth_radius_mm is not None:
        ax.scatter(
            [float(truth_radius_mm)],
            [float(truth_z_mm)],
            s=120,
            marker="x",
            color="#E31A1C",
            linewidth=2.0,
            label="truth",
        )
    ax.set_xlabel("Target radius [mm]")
    ax.set_ylabel("Target depth z [mm]")
    ax.set_title(f"Coordinate Candidate z/radius Landscape: {case_label}{title_suffix}")
    ax.invert_yaxis()
    ax.grid(color="white", alpha=0.18, linewidth=0.8)
    ax.legend(loc="best", fontsize=8, frameon=True)
    return save_validated_figure(fig, save_path)


def append_figure_notes(path, section):
    """Append a report section to FIGURE_NOTES.md, creating it if needed."""
    notes_path = Path(path)
    if notes_path.exists():
        existing = notes_path.read_text(encoding="utf-8").rstrip()
        notes_path.write_text(existing + "\n\n" + section.rstrip() + "\n", encoding="utf-8")
    else:
        notes_path.write_text("# Figure Notes\n\n" + section.rstrip() + "\n", encoding="utf-8")


def write_report_summary(path, payload):
    """Write JSON report summary."""
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def build_report(rows, case_label, truth_z_mm=None, truth_radius_mm=None):
    """Build a compact summary from reduced landscape rows."""
    best = best_candidate(rows)
    rank = truth_rank(rows, truth_z_mm, truth_radius_mm)
    return {
        "case_label": case_label,
        "candidate_count_after_reducing_x": len(rows),
        "best": {
            "x_mm": float(best["x_mm"]),
            "z_mm": float(best["z_mm"]),
            "radius_mm": float(best["radius_mm"]),
            "misfit": float(best["misfit"]),
            "source_frequency_scale": float(best.get("source_frequency_scale", np.nan)),
            "source_time_shift_ps": float(best.get("source_time_shift_ps", np.nan)),
            "source_amplitude_scale": float(best.get("source_amplitude_scale", np.nan)),
        },
        "truth_z_mm": None if truth_z_mm is None else float(truth_z_mm),
        "truth_radius_mm": None if truth_radius_mm is None else float(truth_radius_mm),
        "truth_rank": None if rank is None else rank["rank"],
        "truth_misfit": None if rank is None or rank["row"] is None else float(rank["row"]["misfit"]),
    }


def figure_notes_section(figure_name, summary):
    """Return plain-language notes for the z/radius landscape plot."""
    truth_text = "Truth was not provided for this report."
    if summary["truth_z_mm"] is not None and summary["truth_radius_mm"] is not None:
        if summary["truth_rank"] is None:
            truth_text = (
                f"The truth pair z={summary['truth_z_mm']:g} mm and "
                f"r={summary['truth_radius_mm']:g} mm was not sampled."
            )
        else:
            truth_text = (
                f"The truth pair z={summary['truth_z_mm']:g} mm and "
                f"r={summary['truth_radius_mm']:g} mm ranked "
                f"{summary['truth_rank']} among the reduced z/radius pairs."
            )
    best = summary["best"]
    return f"""## `{figure_name}` - coordinate z/radius objective landscape

This heatmap shows the coordinate optimizer's objective after reducing the
candidate grid to the best x position for each depth/radius pair. Here,
"objective" means the source-profiled waveform misfit: lower values mean the
synthetic B-scan better matches the observed B-scan. A B-scan is the radar
image formed by collecting one received trace at each scan position. The
source-profiled comparison fits the source wavelet frequency, time shift, and
amplitude before computing the mismatch.

The white circle marks the best sampled depth/radius pair. The red x marks the
known synthetic truth when it was provided. This plot is useful because a point
optimizer result can hide whether the true pair was clearly rejected, nearly
tied, or never sampled.

Best sampled pair: x={best['x_mm']:g} mm, z={best['z_mm']:g} mm,
r={best['radius_mm']:g} mm, misfit={best['misfit']:.6g}.

{truth_text}
"""


def resolve_output_dirs(args):
    """Resolve output data/figure dirs for allocated or in-experiment reports."""
    if args.experiment_dir:
        root = Path(args.experiment_dir)
    else:
        root = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = root / "data"
    figures_dir = root / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    return root, data_dir, figures_dir


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_csv")
    parser.add_argument("--case-label", required=True)
    parser.add_argument("--truth-z-mm", type=float, default=None)
    parser.add_argument("--truth-radius-mm", type=float, default=None)
    parser.add_argument("--figure-prefix", default="coordinate_candidate_landscape")
    parser.add_argument("--experiment-dir", default=None)
    parser.add_argument("--run-name", default="coordinate_candidate_landscape_report")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    root, data_dir, figures_dir = resolve_output_dirs(args)
    rows = landscape_rows(filter_case_rows(read_candidate_rows(args.candidate_csv), args.case_label))
    summary = build_report(rows, args.case_label, args.truth_z_mm, args.truth_radius_mm)

    landscape_csv = data_dir / f"{args.figure_prefix}_z_radius_landscape.csv"
    summary_path = data_dir / f"{args.figure_prefix}_z_radius_landscape_summary.json"
    figure_path = figures_dir / f"{args.figure_prefix}_z_radius_landscape.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_landscape_csv(landscape_csv, rows)
    plot_landscape(
        rows,
        args.case_label,
        figure_path,
        truth_z_mm=args.truth_z_mm,
        truth_radius_mm=args.truth_radius_mm,
    )
    summary["paths"] = {
        "candidate_csv": str(args.candidate_csv),
        "landscape_csv": str(landscape_csv),
        "summary": str(summary_path),
        "figure": str(figure_path),
        "figure_notes": str(notes_path),
    }
    write_report_summary(summary_path, summary)
    append_figure_notes(notes_path, figure_notes_section(figure_path.name, summary))
    if not args.experiment_dir:
        write_run_manifest(
            str(root),
            "coordinate_candidate_landscape_report",
            {
                "summary": str(summary_path),
                "landscape_csv": str(landscape_csv),
                "figure": str(figure_path),
                "figure_notes": str(notes_path),
            },
        )
    print(f"Output directory: {root}")
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote figure: {figure_path}")


if __name__ == "__main__":
    main()
