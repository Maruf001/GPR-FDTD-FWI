#!/usr/bin/env python3
"""Report coordinate optimizer objective-variant diagnostics."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
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


def load_summary(path):
    """Load one coordinate optimizer summary JSON."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _truth_fields(summary, target_index):
    truth_radii = summary.get("truth_radius_values_mm")
    truth_radius_mm = (
        float(truth_radii[target_index])
        if truth_radii is not None
        else float(summary["truth_radius_mm"])
    )
    return {
        "truth_x_mm": float(summary["true_x_values_mm"][target_index]),
        "truth_z_mm": float(summary["true_z_values_mm"][target_index]),
        "truth_radius_mm": truth_radius_mm,
    }


def _is_close(a, b, tol=1.0e-9):
    return abs(float(a) - float(b)) <= tol


def enrich_objective_rows(summary, summary_path=None):
    """Add truth-match fields to objective diagnostic rows."""
    rows = []
    for row in summary.get("objective_diagnostic_rows", []):
        enriched = dict(row)
        target_index = int(enriched["step_target_index"])
        truth = _truth_fields(summary, target_index)
        best_x = float(enriched["best_x_mm"])
        best_z = float(enriched["best_z_mm"])
        best_r = float(enriched["best_radius_mm"])
        enriched.update(truth)
        enriched["summary_path"] = summary_path
        enriched["x_abs_error_mm"] = abs(best_x - truth["truth_x_mm"])
        enriched["z_abs_error_mm"] = abs(best_z - truth["truth_z_mm"])
        enriched["radius_abs_error_mm"] = abs(best_r - truth["truth_radius_mm"])
        enriched["is_truth_geometry"] = (
            _is_close(best_x, truth["truth_x_mm"])
            and _is_close(best_z, truth["truth_z_mm"])
            and _is_close(best_r, truth["truth_radius_mm"])
        )
        rows.append(enriched)
    return rows


def diagnostic_group_key(row):
    """Return key shared by base and diagnostic objective rows."""
    return (
        row["run_name"],
        int(row["pass_index"]),
        row["step_kind"],
        int(row["step_target_index"]),
        row["case_label"],
    )


def geometry_tuple(row):
    """Return best x/z/r tuple for geometry comparison."""
    return (
        float(row["best_x_mm"]),
        float(row["best_z_mm"]),
        float(row["best_radius_mm"]),
    )


def float_or_nan(value):
    """Return a float, using NaN for missing/non-numeric values."""
    try:
        if value is None:
            return np.nan
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def build_ratio_rows(rows):
    """Compare each diagnostic objective row against the matching base row."""
    base_by_key = {
        diagnostic_group_key(row): row
        for row in rows
        if row.get("objective_label") == "base"
    }
    ratio_rows = []
    for row in rows:
        if row.get("objective_label") == "base":
            continue
        base = base_by_key.get(diagnostic_group_key(row))
        if base is None:
            continue
        base_margin = float_or_nan(base.get("radius_margin_abs"))
        variant_margin = float_or_nan(row.get("radius_margin_abs"))
        ratio = np.nan
        if np.isfinite(base_margin) and np.isfinite(variant_margin) and base_margin > 0.0:
            ratio = variant_margin / base_margin
        ratio_rows.append({
            "run_name": row["run_name"],
            "case_label": row["case_label"],
            "step_kind": row["step_kind"],
            "target_index": int(row["step_target_index"]),
            "objective_label": row["objective_label"],
            "base_best_x_mm": float(base["best_x_mm"]),
            "base_best_z_mm": float(base["best_z_mm"]),
            "base_best_radius_mm": float(base["best_radius_mm"]),
            "variant_best_x_mm": float(row["best_x_mm"]),
            "variant_best_z_mm": float(row["best_z_mm"]),
            "variant_best_radius_mm": float(row["best_radius_mm"]),
            "truth_x_mm": float(row["truth_x_mm"]),
            "truth_z_mm": float(row["truth_z_mm"]),
            "truth_radius_mm": float(row["truth_radius_mm"]),
            "base_is_truth_geometry": bool(base["is_truth_geometry"]),
            "variant_is_truth_geometry": bool(row["is_truth_geometry"]),
            "variant_changes_geometry": geometry_tuple(row) != geometry_tuple(base),
            "base_margin_abs": base_margin,
            "variant_margin_abs": variant_margin,
            "margin_ratio_to_base": ratio,
        })
    return ratio_rows


def summarize_ratio_rows(rows):
    """Return aggregate counts for objective diagnostic ratio rows."""
    rows = list(rows)
    by_objective = {}
    for objective in sorted(set(row["objective_label"] for row in rows)):
        objective_rows = [row for row in rows if row["objective_label"] == objective]
        ratios = [
            float(row["margin_ratio_to_base"])
            for row in objective_rows
            if np.isfinite(float(row["margin_ratio_to_base"]))
        ]
        by_objective[objective] = {
            "row_count": len(objective_rows),
            "variant_truth_count": sum(row["variant_is_truth_geometry"] for row in objective_rows),
            "base_truth_count": sum(row["base_is_truth_geometry"] for row in objective_rows),
            "geometry_change_count": sum(row["variant_changes_geometry"] for row in objective_rows),
            "margin_ratio_min": None if not ratios else min(ratios),
            "margin_ratio_mean": None if not ratios else sum(ratios) / len(ratios),
            "margin_ratio_max": None if not ratios else max(ratios),
        }
    return {
        "row_count": len(rows),
        "objective_counts": dict(Counter(row["objective_label"] for row in rows)),
        "by_objective": by_objective,
    }


def write_rows_csv(path, rows):
    """Write rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_ratio_rows(rows, save_path):
    """Plot diagnostic margin ratios to the base objective."""
    rows = list(rows)
    labels = [
        f"t{row['target_index']} {row['step_kind']}\n{row['case_label']}\n{row['objective_label']}"
        for row in rows
    ]
    values = np.asarray([float_or_nan(row["margin_ratio_to_base"]) for row in rows], dtype=np.float64)
    finite_values = values[np.isfinite(values)]
    plot_values = np.nan_to_num(values, nan=0.0)
    colors = [
        "#7F7F7F" if not np.isfinite(float_or_nan(row["margin_ratio_to_base"]))
        else
        "#2E7D32" if row["variant_is_truth_geometry"]
        else "#C62828"
        for row in rows
    ]
    width = max(12.0, 0.62 * len(rows))
    fig, ax = plt.subplots(figsize=(width, 5.8), constrained_layout=True)
    x = np.arange(len(rows))
    ax.bar(x, plot_values, color=colors, edgecolor="#333333", linewidth=0.5)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1.0, label="same margin as base")
    ymax = max(1.2, 1.2 * float(finite_values.max())) if finite_values.size else 1.2
    ax.set_ylim(0.0, ymax)
    if finite_values.size != values.size:
        ax.text(
            0.01,
            0.92,
            f"{values.size - finite_values.size} row(s) have unavailable margin ratios",
            transform=ax.transAxes,
            fontsize=9,
            ha="left",
            va="top",
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#B0B0B0"},
        )
    ax.set_ylabel("Diagnostic margin / base margin")
    ax.set_title("Coordinate Objective Diagnostic Margin Ratios")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper left", fontsize=8, frameon=True)
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, summary):
    """Write plain-language notes for the diagnostic objective report."""
    by_objective = summary["by_objective"]
    lines = [
        "# Figure Notes",
        "",
        "## 1. `coordinate_objective_diagnostic_ratios.png` - objective diagnostic margins",
        "",
        "This figure compares each diagnostic objective against the base objective",
        "for the same coordinate step, target, and observed case. A ratio above",
        "1.0 means the diagnostic objective increased the best-versus-next-radius",
        "margin relative to the base objective.",
        "",
        "Green bars mean the diagnostic objective's best x/z/r matched the known",
        "synthetic truth. Red bars mean it strengthened a wrong geometry branch.",
        "That distinction is essential: a larger margin is useful only when it",
        "supports the correct branch.",
        "",
        "Aggregate by objective:",
    ]
    for objective, data in by_objective.items():
        lines.append(
            "- "
            f"{objective}: rows={data['row_count']}, "
            f"truth rows={data['variant_truth_count']}, "
            f"geometry changes={data['geometry_change_count']}, "
            f"mean margin ratio={data['margin_ratio_mean']:.3g}"
        )
    lines.extend([
        "",
        "Use this report to choose diagnostic objectives for reporting. It should",
        "not be used to change the coordinate update rule unless the diagnostic",
        "also preserves or improves truth-geometry selection across stress cases.",
    ])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", nargs="+")
    parser.add_argument("--run-name", default="coordinate_objective_diagnostic_report")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    objective_rows = []
    for summary_path in args.summary_json:
        summary = load_summary(summary_path)
        objective_rows.extend(enrich_objective_rows(summary, summary_path))
    ratio_rows = build_ratio_rows(objective_rows)
    if not ratio_rows:
        raise ValueError("no diagnostic objective rows found")
    aggregate = summarize_ratio_rows(ratio_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / "coordinate_objective_diagnostic_ratios.csv"
    json_path = data_dir / "coordinate_objective_diagnostic_report.json"
    plot_path = figures_dir / "coordinate_objective_diagnostic_ratios.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_rows_csv(csv_path, ratio_rows)
    plot_ratio_rows(ratio_rows, plot_path)
    write_figure_notes(notes_path, aggregate)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({
            "input_summary_json": args.summary_json,
            "aggregate": aggregate,
            "rows": ratio_rows,
        }, handle, indent=2)
    write_run_manifest(
        str(outdir),
        "coordinate_objective_diagnostic_report",
        {
            "csv": str(csv_path),
            "json": str(json_path),
            "plot": str(plot_path),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps(aggregate, indent=2))
    print(f"Wrote CSV: {csv_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
