#!/usr/bin/env python3
"""Aggregate reporting-first coordinate optimizer confidence summaries."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.candidate_confidence import ConfidenceThresholds  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


LABEL_COLORS = {
    "strong": "#1b7837",
    "moderate": "#4575b4",
    "weak": "#d73027",
    "ambiguous": "#7f7f7f",
    "missing": "#bdbdbd",
}

OPTIONAL_NUMERIC_ROW_FIELDS = (
    "best_x_mm",
    "best_z_mm",
    "best_radius_mm",
    "next_radius_mm",
    "radius_margin_abs",
    "radius_margin_rel",
    "best_misfit",
    "next_radius_misfit",
    "competing_geometry_x_mm",
    "competing_geometry_z_mm",
    "competing_geometry_radius_mm",
    "competing_geometry_misfit",
    "source_frequency_scale",
    "source_time_shift_ps",
    "source_amplitude_scale",
    "source_ringdown_scale",
    "source_ringdown_delay_ps",
    "source_ringdown_frequency_scale",
    "source_primary_coefficient",
    "source_ringdown_coefficient",
    "ambiguity_misfit_threshold",
    "ambiguity_x_min_mm",
    "ambiguity_x_max_mm",
    "ambiguity_z_min_mm",
    "ambiguity_z_max_mm",
    "ambiguity_radius_min_mm",
    "ambiguity_radius_max_mm",
)


def _float_or_none(value):
    if value in ("", None):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return numeric if math.isfinite(numeric) else None


def _format_optional_float(value, fmt=".3g"):
    numeric = _float_or_none(value)
    if numeric is None:
        return "not_recorded"
    return f"{numeric:{fmt}}"


def _validated_default_tx_rx_offset(value):
    if value is None:
        return None
    numeric = _float_or_none(value)
    if numeric is None or numeric < 0.0:
        raise ValueError("--default-missing-tx-rx-offset-mm must be a finite non-negative number")
    return numeric


def _exact_match(value, truth, tol=1.0e-9):
    numeric = _float_or_none(value)
    truth_numeric = _float_or_none(truth)
    if numeric is None or truth_numeric is None:
        return False
    return abs(numeric - truth_numeric) <= tol


def _interval_width(row, min_key, max_key):
    lower = _float_or_none(row.get(min_key))
    upper = _float_or_none(row.get(max_key))
    if lower is None or upper is None:
        return None
    return max(0.0, float(upper) - float(lower))


def _row_plot_label(row):
    sources = _float_or_none(row.get("sources"))
    source_prefix = "" if sources is None else f"s{int(sources)} "
    tx_rx_offset = _float_or_none(row.get("tx_rx_offset_mm"))
    offset_prefix = "" if tx_rx_offset is None else f"tx{tx_rx_offset:.3g} "
    return f"{row['run_name']}\n{source_prefix}{offset_prefix}t{row['step_target_index']} {row['case_label']}"


def _acquisition_key(row):
    sources = _float_or_none(row.get("sources"))
    tx_rx_offset = _float_or_none(row.get("tx_rx_offset_mm"))
    if sources is None and tx_rx_offset is None:
        return None
    source_text = "sources=unknown" if sources is None else f"sources={int(sources)}"
    offset_text = (
        "tx_rx_offset_mm=not_recorded"
        if tx_rx_offset is None
        else f"tx_rx_offset_mm={tx_rx_offset:.3g}"
    )
    tx_rx_source = row.get("tx_rx_offset_source")
    source_suffix = (
        ""
        if tx_rx_source in (None, "summary", "missing")
        else f"|tx_rx_offset_source={tx_rx_source}"
    )
    return f"{source_text}|{offset_text}{source_suffix}"


def _acquisition_label(row):
    sources = _float_or_none(row.get("sources"))
    tx_rx_offset = _float_or_none(row.get("tx_rx_offset_mm"))
    source_text = "sources not recorded" if sources is None else f"{int(sources)} sources"
    offset_text = (
        "Tx/Rx offset not recorded"
        if tx_rx_offset is None
        else f"Tx/Rx offset {tx_rx_offset:.3g} mm"
    )
    if row.get("tx_rx_offset_inferred"):
        offset_text += " (filled default)"
    return f"{source_text}, {offset_text}"


def load_summary(path):
    """Load one coordinate optimizer summary JSON."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def enrich_coordinate_rows(summary, summary_path=None, default_missing_tx_rx_offset_mm=None):
    """Add truth/error fields to coordinate confidence rows."""
    default_missing_tx_rx_offset_mm = _validated_default_tx_rx_offset(
        default_missing_tx_rx_offset_mm
    )
    truth_x = list(summary["true_x_values_mm"])
    truth_z = list(summary["true_z_values_mm"])
    truth_radii = summary.get("truth_radius_values_mm")
    sources = _float_or_none(summary.get("sources"))
    frequency_ghz = _float_or_none(summary.get("frequency_ghz"))
    tx_rx_offset_mm = _float_or_none(summary.get("tx_rx_offset_mm"))
    tx_rx_offset_inferred = False
    tx_rx_offset_source = "summary"
    if tx_rx_offset_mm is None:
        tx_rx_offset_source = "missing"
        if default_missing_tx_rx_offset_mm is not None:
            tx_rx_offset_mm = default_missing_tx_rx_offset_mm
            tx_rx_offset_inferred = True
            tx_rx_offset_source = "default_missing"
    rows = []
    for row in summary.get("confidence_rows", []):
        enriched = dict(row)
        for key in OPTIONAL_NUMERIC_ROW_FIELDS:
            if key in enriched:
                enriched[key] = _float_or_none(enriched.get(key))
        target_index = int(enriched["step_target_index"])
        best_x = _float_or_none(enriched.get("best_x_mm"))
        best_z = _float_or_none(enriched.get("best_z_mm"))
        best_r = _float_or_none(enriched.get("best_radius_mm"))
        target_truth_x = float(truth_x[target_index])
        target_truth_z = float(truth_z[target_index])
        target_truth_r = (
            float(truth_radii[target_index])
            if truth_radii is not None
            else float(summary["truth_radius_mm"])
        )
        enriched.update({
            "summary_path": summary_path,
            "sources": sources,
            "frequency_ghz": frequency_ghz,
            "tx_rx_offset_mm": tx_rx_offset_mm,
            "tx_rx_offset_inferred": tx_rx_offset_inferred,
            "tx_rx_offset_source": tx_rx_offset_source,
            "truth_x_mm": target_truth_x,
            "truth_z_mm": target_truth_z,
            "truth_radius_mm": target_truth_r,
            "x_abs_error_mm": None if best_x is None else abs(best_x - target_truth_x),
            "z_abs_error_mm": None if best_z is None else abs(best_z - target_truth_z),
            "radius_abs_error_mm": None if best_r is None else abs(best_r - target_truth_r),
            "ambiguity_x_width_mm": _interval_width(enriched, "ambiguity_x_min_mm", "ambiguity_x_max_mm"),
            "ambiguity_z_width_mm": _interval_width(enriched, "ambiguity_z_min_mm", "ambiguity_z_max_mm"),
            "ambiguity_radius_width_mm": _interval_width(
                enriched,
                "ambiguity_radius_min_mm",
                "ambiguity_radius_max_mm",
            ),
            "is_truth_x": _exact_match(best_x, target_truth_x),
            "is_truth_z": _exact_match(best_z, target_truth_z),
            "is_truth_radius": _exact_match(best_r, target_truth_r),
        })
        enriched["is_truth_geometry"] = (
            enriched["is_truth_x"]
            and enriched["is_truth_z"]
            and enriched["is_truth_radius"]
        )
        rows.append(enriched)
    return rows


def _finite_values(rows, key):
    values = []
    for row in rows:
        value = _float_or_none(row.get(key))
        if value is not None:
            values.append(value)
    return values


def _positive_value_count(rows, key):
    count = 0
    for row in rows:
        value = _float_or_none(row.get(key))
        if value is not None and value > 0.0:
            count += 1
    return count


def _plot_value(value):
    numeric = _float_or_none(value)
    return 0.0 if numeric is None else numeric


def aggregate_rows(rows):
    """Compute aggregate confidence and accuracy counts."""
    rows = list(rows)
    label_counts = Counter(row.get("confidence_label") for row in rows)
    warning_count = sum(1 for row in rows if row.get("fallback_warning"))
    exact_count = sum(1 for row in rows if row.get("is_truth_geometry"))
    margins = _finite_values(rows, "radius_margin_abs")
    ambiguity_x_widths = _finite_values(rows, "ambiguity_x_width_mm")
    ambiguity_z_widths = _finite_values(rows, "ambiguity_z_width_mm")
    ambiguity_radius_widths = _finite_values(rows, "ambiguity_radius_width_mm")
    by_target = defaultdict(list)
    by_sources = defaultdict(list)
    by_acquisition = defaultdict(list)
    for row in rows:
        by_target[int(row["step_target_index"])].append(row)
        if row.get("sources") is not None:
            by_sources[int(row["sources"])].append(row)
        acquisition_key = _acquisition_key(row)
        if acquisition_key is not None:
            by_acquisition[acquisition_key].append(row)

    target_summary = {}
    for target_index, target_rows in sorted(by_target.items()):
        target_margins = _finite_values(target_rows, "radius_margin_abs")
        target_summary[str(target_index)] = {
            "row_count": len(target_rows),
            "truth_geometry_count": sum(1 for row in target_rows if row.get("is_truth_geometry")),
            "confidence_label_counts": dict(Counter(row.get("confidence_label") for row in target_rows)),
            "fallback_warning_count": sum(1 for row in target_rows if row.get("fallback_warning")),
            "radius_margin_abs_min": None if not target_margins else min(target_margins),
            "radius_margin_abs_mean": None if not target_margins else sum(target_margins) / len(target_margins),
            "radius_margin_abs_max": None if not target_margins else max(target_margins),
            "x_ambiguity_row_count": _positive_value_count(target_rows, "ambiguity_x_width_mm"),
        }

    source_summary = {}
    for sources, source_rows in sorted(by_sources.items()):
        source_margins = _finite_values(source_rows, "radius_margin_abs")
        source_summary[str(sources)] = {
            "row_count": len(source_rows),
            "truth_geometry_count": sum(1 for row in source_rows if row.get("is_truth_geometry")),
            "x_ambiguity_row_count": _positive_value_count(source_rows, "ambiguity_x_width_mm"),
            "radius_margin_abs_min": None if not source_margins else min(source_margins),
            "radius_margin_abs_mean": (
                None if not source_margins else sum(source_margins) / len(source_margins)
            ),
            "radius_margin_abs_max": None if not source_margins else max(source_margins),
        }

    acquisition_summary = {}
    for acquisition_key, acquisition_rows in sorted(by_acquisition.items()):
        acquisition_margins = _finite_values(acquisition_rows, "radius_margin_abs")
        first = acquisition_rows[0]
        acquisition_summary[acquisition_key] = {
            "label": _acquisition_label(first),
            "sources": first.get("sources"),
            "tx_rx_offset_mm": first.get("tx_rx_offset_mm"),
            "row_count": len(acquisition_rows),
            "truth_geometry_count": sum(1 for row in acquisition_rows if row.get("is_truth_geometry")),
            "x_ambiguity_row_count": _positive_value_count(acquisition_rows, "ambiguity_x_width_mm"),
            "radius_margin_abs_min": None if not acquisition_margins else min(acquisition_margins),
            "radius_margin_abs_mean": (
                None if not acquisition_margins else sum(acquisition_margins) / len(acquisition_margins)
            ),
            "radius_margin_abs_max": None if not acquisition_margins else max(acquisition_margins),
        }

    return {
        "row_count": len(rows),
        "truth_geometry_count": exact_count,
        "confidence_label_counts": dict(label_counts),
        "fallback_warning_count": warning_count,
        "radius_margin_abs_min": None if not margins else min(margins),
        "radius_margin_abs_mean": None if not margins else sum(margins) / len(margins),
        "radius_margin_abs_max": None if not margins else max(margins),
        "ambiguity_x_width_max_mm": None if not ambiguity_x_widths else max(ambiguity_x_widths),
        "ambiguity_z_width_max_mm": None if not ambiguity_z_widths else max(ambiguity_z_widths),
        "ambiguity_radius_width_max_mm": (
            None if not ambiguity_radius_widths else max(ambiguity_radius_widths)
        ),
        "x_ambiguity_row_count": _positive_value_count(rows, "ambiguity_x_width_mm"),
        "target_summary": target_summary,
        "source_summary": source_summary,
        "acquisition_summary": acquisition_summary,
    }


def write_rows_csv(rows, path):
    """Write enriched aggregate rows."""
    rows = list(rows)
    if not rows:
        raise ValueError("no rows to write")
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def plot_coordinate_aggregate(rows, save_path):
    """Plot aggregate radius margins without dense text annotations."""
    rows = list(rows)
    if not rows:
        raise ValueError("no rows to plot")
    labels = [_row_plot_label(row) for row in rows]
    values = [_plot_value(row.get("radius_margin_abs")) for row in rows]
    colors = [LABEL_COLORS.get(row.get("confidence_label"), "#7f7f7f") for row in rows]
    thresholds = ConfidenceThresholds()
    width = max(10.0, 0.72 * len(rows))
    fig, ax = plt.subplots(figsize=(width, 5.6), constrained_layout=True)
    ax.bar(range(len(rows)), values, color=colors, edgecolor="#333333", linewidth=0.5)
    ax.axhline(
        thresholds.moderate_abs,
        color="#555555",
        linestyle="--",
        linewidth=1.0,
        label="moderate abs threshold",
    )
    ax.axhline(
        thresholds.strong_abs,
        color="#111111",
        linestyle=":",
        linewidth=1.2,
        label="strong abs threshold",
    )
    ax.set_title("Coordinate Optimizer Radius Confidence Across Seeds")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=7)
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ymax = max(max(values) * 1.25, thresholds.strong_abs * 1.2)
    ax.set_ylim(0.0, ymax)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def plot_ambiguity_widths(rows, save_path):
    """Plot x/z/r ambiguity interval widths for aggregate rows."""
    rows = list(rows)
    if not rows:
        raise ValueError("no rows to plot")
    labels = [_row_plot_label(row) for row in rows]
    x_widths = [_plot_value(row.get("ambiguity_x_width_mm")) for row in rows]
    z_widths = [_plot_value(row.get("ambiguity_z_width_mm")) for row in rows]
    radius_widths = [_plot_value(row.get("ambiguity_radius_width_mm")) for row in rows]
    width = max(10.0, 0.72 * len(rows))
    x_positions = list(range(len(rows)))
    bar_width = 0.25
    fig, ax = plt.subplots(figsize=(width, 5.6), constrained_layout=True)
    ax.bar(
        [value - bar_width for value in x_positions],
        x_widths,
        width=bar_width,
        color="#4C78A8",
        label="x interval width",
    )
    ax.bar(
        x_positions,
        z_widths,
        width=bar_width,
        color="#F58518",
        label="z interval width",
    )
    ax.bar(
        [value + bar_width for value in x_positions],
        radius_widths,
        width=bar_width,
        color="#54A24B",
        label="radius interval width",
    )
    ax.set_title("Coordinate Optimizer Ambiguity Interval Widths")
    ax.set_ylabel("Interval width [mm]")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=7)
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ymax = max(max(x_widths + z_widths + radius_widths) * 1.25, 0.25)
    ax.set_ylim(0.0, ymax)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def write_figure_notes(path, aggregate):
    """Write plain-language notes for the coordinate aggregate plot."""
    label_counts = aggregate.get("confidence_label_counts", {})
    label_text = ", ".join(
        f"{label}={count}"
        for label, count in sorted(label_counts.items())
    ) or "none"
    target_bits = []
    for target_index, target_summary in sorted(aggregate.get("target_summary", {}).items()):
        target_bits.append(
            f"target {target_index}: rows={target_summary['row_count']}, "
            f"truth-geometry rows={target_summary['truth_geometry_count']}"
        )
    target_text = "; ".join(target_bits) or "none"
    source_bits = []
    for sources, source_summary in sorted(aggregate.get("source_summary", {}).items()):
        source_bits.append(
            f"{sources} sources: rows={source_summary['row_count']}, "
            f"x-ambiguity rows={source_summary['x_ambiguity_row_count']}"
        )
    source_text = "; ".join(source_bits) or "not available"
    acquisition_bits = []
    for _, acquisition_summary in sorted(aggregate.get("acquisition_summary", {}).items()):
        acquisition_bits.append(
            f"{acquisition_summary['label']}: rows={acquisition_summary['row_count']}, "
            f"x-ambiguity rows={acquisition_summary['x_ambiguity_row_count']}"
        )
    acquisition_text = "; ".join(acquisition_bits) or "not available"
    lines = [
        "# Figure Notes",
        "",
        "## 1. `coordinate_confidence_aggregate.png` - coordinate confidence across runs",
        "",
        "This figure aggregates coordinate optimizer confidence rows across one or",
        "more experiments. Each bar is the best-versus-next-radius objective gap",
        "for one target, case, and coordinate-update step. Larger bars mean the",
        "selected radius is better separated from the next tested radius.",
        "",
        "Colors are the confidence labels used by the coordinate reporting code:",
        "strong, moderate, weak, ambiguous, or missing. Missing usually means the",
        "radius was not varied in that run, so no radius margin can be computed.",
        "",
        f"Rows: {aggregate['row_count']}. Truth-geometry rows: "
        f"{aggregate['truth_geometry_count']}. Confidence counts: {label_text}.",
        "",
        f"Per-target summary: {target_text}.",
        "",
        f"Per-source-count summary: {source_text}.",
        "",
        f"Per-acquisition summary: {acquisition_text}.",
        "",
        "## 2. `coordinate_ambiguity_widths.png` - coordinate ambiguity intervals",
        "",
        "This figure shows the width of the near-best candidate interval for x, z,",
        "and radius. A nonzero x bar means multiple lateral positions remain within",
        "the configured ambiguity threshold even when the selected radius is strong.",
        "",
        f"Rows with nonzero x ambiguity: {aggregate.get('x_ambiguity_row_count', 0)}. "
        f"Maximum x/z/r ambiguity widths: "
        f"{_format_optional_float(aggregate.get('ambiguity_x_width_max_mm'))} / "
        f"{_format_optional_float(aggregate.get('ambiguity_z_width_max_mm'))} / "
        f"{_format_optional_float(aggregate.get('ambiguity_radius_width_max_mm'))} mm.",
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", nargs="+", help="coordinate optimizer summary JSON paths")
    parser.add_argument("--run-name", default="coordinate_confidence_aggregate")
    parser.add_argument("--outdir", default=None)
    parser.add_argument(
        "--default-missing-tx-rx-offset-mm",
        type=float,
        default=None,
        help=(
            "Fill summaries that predate tx_rx_offset_mm with this explicit "
            "Tx/Rx offset value. Rows are marked as inferred."
        ),
    )
    args = parser.parse_args()
    default_missing_tx_rx_offset_mm = _validated_default_tx_rx_offset(
        args.default_missing_tx_rx_offset_mm
    )

    rows = []
    for summary_path in args.summary_json:
        summary = load_summary(summary_path)
        rows.extend(
            enrich_coordinate_rows(
                summary,
                summary_path,
                default_missing_tx_rx_offset_mm=default_missing_tx_rx_offset_mm,
            )
        )
    aggregate = aggregate_rows(rows)

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, "coordinate_confidence_aggregate.csv")
    json_path = os.path.join(data_dir, "coordinate_confidence_aggregate.json")
    plot_path = os.path.join(figures_dir, "coordinate_confidence_aggregate.png")
    ambiguity_plot_path = os.path.join(figures_dir, "coordinate_ambiguity_widths.png")
    notes_path = os.path.join(figures_dir, "FIGURE_NOTES.md")
    write_rows_csv(rows, csv_path)
    plot_coordinate_aggregate(rows, plot_path)
    plot_ambiguity_widths(rows, ambiguity_plot_path)
    write_figure_notes(notes_path, aggregate)

    report = {
        "run_name": args.run_name,
        "input_summary_json": args.summary_json,
        "default_missing_tx_rx_offset_mm": default_missing_tx_rx_offset_mm,
        "aggregate": aggregate,
        "rows": rows,
        "paths": {
            "csv": csv_path,
            "json": json_path,
            "plot": plot_path,
            "ambiguity_plot": ambiguity_plot_path,
            "figure_notes": notes_path,
        },
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    write_run_manifest(
        outdir,
        "coordinate_confidence_aggregate",
        {
            "csv": csv_path,
            "json": json_path,
            "plot": plot_path,
            "ambiguity_plot": ambiguity_plot_path,
            "figure_notes": notes_path,
            "default_missing_tx_rx_offset_mm": default_missing_tx_rx_offset_mm,
        },
    )
    print(json.dumps(aggregate, indent=2))
    print(f"Wrote CSV: {csv_path}")
    print(f"Wrote JSON: {json_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
