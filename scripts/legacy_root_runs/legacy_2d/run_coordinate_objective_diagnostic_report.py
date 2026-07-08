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
from inversion.candidate_confidence import summarize_case_confidence  # noqa: E402
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


def _finite_or_none(value):
    numeric = float_or_nan(value)
    return None if not np.isfinite(numeric) else float(numeric)


def enrich_objective_rows(summary, summary_path=None):
    """Add truth-match fields to objective diagnostic rows."""
    rows = []
    for row in summary.get("objective_diagnostic_rows", []):
        enriched = dict(row)
        target_index = int(enriched["step_target_index"])
        truth = _truth_fields(summary, target_index)
        best_x = float_or_nan(enriched.get("best_x_mm"))
        best_z = float_or_nan(enriched.get("best_z_mm"))
        best_r = float_or_nan(enriched.get("best_radius_mm"))
        has_complete_geometry = (
            np.isfinite(best_x)
            and np.isfinite(best_z)
            and np.isfinite(best_r)
        )
        enriched.update(truth)
        enriched["summary_path"] = summary_path
        enriched["x_abs_error_mm"] = (
            None if not np.isfinite(best_x) else abs(best_x - truth["truth_x_mm"])
        )
        enriched["z_abs_error_mm"] = (
            None if not np.isfinite(best_z) else abs(best_z - truth["truth_z_mm"])
        )
        enriched["radius_abs_error_mm"] = (
            None if not np.isfinite(best_r) else abs(best_r - truth["truth_radius_mm"])
        )
        enriched["is_truth_geometry"] = bool(
            has_complete_geometry
            and _is_close(best_x, truth["truth_x_mm"])
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
    values = (
        float_or_nan(row.get("best_x_mm")),
        float_or_nan(row.get("best_z_mm")),
        float_or_nan(row.get("best_radius_mm")),
    )
    if not all(np.isfinite(value) for value in values):
        return None
    return values


def float_or_nan(value):
    """Return a float, using NaN for missing/non-numeric values."""
    try:
        if value is None:
            return np.nan
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def format_optional_float(value, fmt=".3g"):
    """Format optional numeric values for human-readable notes."""
    numeric = float_or_nan(value)
    if not np.isfinite(numeric):
        return "not_recorded"
    return f"{numeric:{fmt}}"


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
        ratio = None
        if np.isfinite(base_margin) and np.isfinite(variant_margin) and base_margin > 0.0:
            ratio = variant_margin / base_margin
        base_geometry = geometry_tuple(base)
        variant_geometry = geometry_tuple(row)
        geometry_comparison_available = base_geometry is not None and variant_geometry is not None
        ratio_rows.append({
            "run_name": row["run_name"],
            "case_label": row["case_label"],
            "step_kind": row["step_kind"],
            "target_index": int(row["step_target_index"]),
            "objective_label": row["objective_label"],
            "base_best_x_mm": _finite_or_none(base.get("best_x_mm")),
            "base_best_z_mm": _finite_or_none(base.get("best_z_mm")),
            "base_best_radius_mm": _finite_or_none(base.get("best_radius_mm")),
            "variant_best_x_mm": _finite_or_none(row.get("best_x_mm")),
            "variant_best_z_mm": _finite_or_none(row.get("best_z_mm")),
            "variant_best_radius_mm": _finite_or_none(row.get("best_radius_mm")),
            "truth_x_mm": float(row["truth_x_mm"]),
            "truth_z_mm": float(row["truth_z_mm"]),
            "truth_radius_mm": float(row["truth_radius_mm"]),
            "base_is_truth_geometry": bool(base["is_truth_geometry"]),
            "variant_is_truth_geometry": bool(row["is_truth_geometry"]),
            "geometry_comparison_available": geometry_comparison_available,
            "variant_changes_geometry": (
                None
                if not geometry_comparison_available
                else variant_geometry != base_geometry
            ),
            "base_margin_abs": _finite_or_none(base.get("radius_margin_abs")),
            "variant_margin_abs": _finite_or_none(row.get("radius_margin_abs")),
            "margin_ratio_to_base": ratio,
        })
    return ratio_rows


def _objective_result_key(pass_index, step_kind, target_index, case_label, objective_label):
    return (
        int(pass_index),
        str(step_kind),
        int(target_index),
        str(case_label),
        str(objective_label),
    )


def _diagnostic_meta_by_key(summary):
    """Return diagnostic row metadata keyed by step/case/objective."""
    meta = {}
    for row in summary.get("objective_diagnostic_rows", []):
        key = _objective_result_key(
            row.get("pass_index"),
            row.get("step_kind", "main"),
            row.get("step_target_index"),
            row.get("case_label"),
            row.get("objective_label"),
        )
        meta[key] = row
    return meta


def objective_confidence_rows(summary, summary_path=None):
    """Build confidence/ambiguity rows for every saved objective variant."""
    rows = []
    diagnostic_meta = _diagnostic_meta_by_key(summary)
    run_name = summary.get("run_name")
    for step in summary.get("steps", []):
        objective_results = step.get("objective_results") or {}
        if not objective_results:
            continue
        pass_index = int(step.get("pass_index", 0))
        step_kind = step.get("step_kind", "main")
        target_index = int(step["target_index"])
        update_case_label = step.get("update_case_label", summary.get("update_case_label"))
        truth = _truth_fields(summary, target_index)
        for case_label, by_objective in objective_results.items():
            for objective_label, result in by_objective.items():
                key = _objective_result_key(
                    pass_index,
                    step_kind,
                    target_index,
                    case_label,
                    objective_label,
                )
                diagnostic = diagnostic_meta.get(key, {})
                meta = {
                    "backend": diagnostic.get("backend", summary.get("backend")),
                    "grid_step_mm": diagnostic.get("grid_step_mm", summary.get("grid_step_mm")),
                    "target_rebar_index": target_index,
                    "candidate_count": diagnostic.get("candidate_count"),
                    "case_count": diagnostic.get("case_count", len(objective_results)),
                }
                row = summarize_case_confidence(run_name, case_label, result, meta)
                best_x = float_or_nan(row.get("best_x_mm"))
                best_z = float_or_nan(row.get("best_z_mm"))
                best_radius = float_or_nan(row.get("best_radius_mm"))
                has_complete_geometry = (
                    np.isfinite(best_x)
                    and np.isfinite(best_z)
                    and np.isfinite(best_radius)
                )
                row.update({
                    "objective_label": objective_label,
                    "pass_index": pass_index,
                    "step_target_index": target_index,
                    "step_kind": step_kind,
                    "update_case_label": update_case_label,
                    "truth_x_mm": truth["truth_x_mm"],
                    "truth_z_mm": truth["truth_z_mm"],
                    "truth_radius_mm": truth["truth_radius_mm"],
                    "summary_path": summary_path,
                    "x_abs_error_mm": (
                        None if not np.isfinite(best_x) else abs(best_x - truth["truth_x_mm"])
                    ),
                    "z_abs_error_mm": (
                        None if not np.isfinite(best_z) else abs(best_z - truth["truth_z_mm"])
                    ),
                    "radius_abs_error_mm": (
                        None
                        if not np.isfinite(best_radius)
                        else abs(best_radius - truth["truth_radius_mm"])
                    ),
                    "is_truth_geometry": bool(
                        has_complete_geometry
                        and
                        _is_close(best_x, truth["truth_x_mm"])
                        and _is_close(best_z, truth["truth_z_mm"])
                        and _is_close(best_radius, truth["truth_radius_mm"])
                    ),
                })
                rows.append(row)
    return rows


def _width(row, min_key, max_key):
    lower = float_or_nan(row.get(min_key))
    upper = float_or_nan(row.get(max_key))
    if not np.isfinite(lower) or not np.isfinite(upper):
        return None
    return upper - lower


def _finite_values(rows, key):
    values = []
    for row in rows:
        value = float_or_nan(row.get(key))
        if np.isfinite(value):
            values.append(value)
    return values


def summarize_objective_confidence(rows):
    """Return aggregate confidence counts by objective label."""
    rows = list(rows)
    by_objective = {}
    for objective in sorted(set(row["objective_label"] for row in rows)):
        objective_rows = [row for row in rows if row["objective_label"] == objective]
        x_widths = [
            width for width in (_width(row, "ambiguity_x_min_mm", "ambiguity_x_max_mm") for row in objective_rows)
            if width is not None
        ]
        z_widths = [
            width for width in (_width(row, "ambiguity_z_min_mm", "ambiguity_z_max_mm") for row in objective_rows)
            if width is not None
        ]
        radius_widths = [
            width
            for width in (
                _width(row, "ambiguity_radius_min_mm", "ambiguity_radius_max_mm")
                for row in objective_rows
            )
            if width is not None
        ]
        margins = _finite_values(objective_rows, "radius_margin_abs")
        by_objective[objective] = {
            "row_count": len(objective_rows),
            "truth_geometry_count": sum(row["is_truth_geometry"] for row in objective_rows),
            "confidence_label_counts": dict(Counter(row["confidence_label"] for row in objective_rows)),
            "radius_margin_abs_min": None if not margins else min(margins),
            "radius_margin_abs_mean": None if not margins else sum(margins) / len(margins),
            "radius_margin_abs_max": None if not margins else max(margins),
            "ambiguity_x_width_max_mm": None if not x_widths else max(x_widths),
            "ambiguity_z_width_max_mm": None if not z_widths else max(z_widths),
            "ambiguity_radius_width_max_mm": None if not radius_widths else max(radius_widths),
        }
    return {
        "row_count": len(rows),
        "objective_counts": dict(Counter(row["objective_label"] for row in rows)),
        "by_objective": by_objective,
    }


def summarize_ratio_rows(rows):
    """Return aggregate counts for objective diagnostic ratio rows."""
    rows = list(rows)
    by_objective = {}
    for objective in sorted(set(row["objective_label"] for row in rows)):
        objective_rows = [row for row in rows if row["objective_label"] == objective]
        ratios = _finite_values(objective_rows, "margin_ratio_to_base")
        by_objective[objective] = {
            "row_count": len(objective_rows),
            "variant_truth_count": sum(row["variant_is_truth_geometry"] for row in objective_rows),
            "base_truth_count": sum(row["base_is_truth_geometry"] for row in objective_rows),
            "geometry_change_count": sum(
                1 for row in objective_rows
                if row.get("variant_changes_geometry") is True
            ),
            "geometry_comparison_unavailable_count": sum(
                1 for row in objective_rows
                if row.get("variant_changes_geometry") is None
            ),
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
            f"mean margin ratio={format_optional_float(data['margin_ratio_mean'])}"
        )
    confidence = summary.get("objective_confidence")
    if confidence:
        lines.extend([
            "",
            "Objective-specific confidence rows:",
        ])
        for objective, data in confidence["by_objective"].items():
            labels = ", ".join(
                f"{label}={count}"
                for label, count in sorted(data["confidence_label_counts"].items())
            )
            lines.append(
                "- "
                f"{objective}: rows={data['row_count']}, "
                f"truth rows={data['truth_geometry_count']}, "
                f"labels={labels}, "
                "max x/z/r ambiguity widths="
                f"{format_optional_float(data['ambiguity_x_width_max_mm'])}/"
                f"{format_optional_float(data['ambiguity_z_width_max_mm'])}/"
                f"{format_optional_float(data['ambiguity_radius_width_max_mm'])} mm"
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
    objective_confidence = []
    for summary_path in args.summary_json:
        summary = load_summary(summary_path)
        objective_rows.extend(enrich_objective_rows(summary, summary_path))
        objective_confidence.extend(objective_confidence_rows(summary, summary_path))
    ratio_rows = build_ratio_rows(objective_rows)
    if not ratio_rows:
        raise ValueError("no diagnostic objective rows found")
    aggregate = summarize_ratio_rows(ratio_rows)
    confidence_summary = summarize_objective_confidence(objective_confidence) if objective_confidence else None

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / "coordinate_objective_diagnostic_ratios.csv"
    confidence_csv_path = data_dir / "coordinate_objective_confidence_rows.csv"
    json_path = data_dir / "coordinate_objective_diagnostic_report.json"
    plot_path = figures_dir / "coordinate_objective_diagnostic_ratios.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_rows_csv(csv_path, ratio_rows)
    if objective_confidence:
        write_rows_csv(confidence_csv_path, objective_confidence)
    plot_ratio_rows(ratio_rows, plot_path)
    report_summary = dict(aggregate)
    if confidence_summary is not None:
        report_summary["objective_confidence"] = confidence_summary
    write_figure_notes(notes_path, report_summary)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({
            "input_summary_json": args.summary_json,
            "aggregate": aggregate,
            "objective_confidence": confidence_summary,
            "rows": ratio_rows,
            "objective_confidence_rows": objective_confidence,
        }, handle, indent=2)
    manifest_artifacts = {
        "csv": str(csv_path),
        "json": str(json_path),
        "plot": str(plot_path),
        "figure_notes": str(notes_path),
    }
    if objective_confidence:
        manifest_artifacts["confidence_csv"] = str(confidence_csv_path)
    write_run_manifest(
        str(outdir),
        "coordinate_objective_diagnostic_report",
        manifest_artifacts,
    )
    print(json.dumps(aggregate, indent=2))
    print(f"Wrote CSV: {csv_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
