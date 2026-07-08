#!/usr/bin/env python3
"""Reconcile current field timing anchors with supported short-profile intervals."""

from __future__ import annotations

import argparse
import csv
import json
import math
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TIMING_ENVELOPE_RUN = "115_gssi51600s_field_cue_timing_envelope_post_cue_support_catalog"
DEFAULT_SUPPORTED_INTERVAL_RUN = "049_gssi51600s_supported_interval_visual_qc"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def short_anchor_rows(timing_rows: list[dict]) -> list[dict]:
    return [
        row for row in timing_rows
        if str(row.get("support_family", "")) == "short_relative_timing"
    ]


def interval_contains_x(interval: dict, x_mm: float) -> bool:
    start = safe_float(interval.get("start_x_mm"))
    end = safe_float(interval.get("end_x_mm"))
    return math.isfinite(x_mm) and math.isfinite(start) and math.isfinite(end) and start <= x_mm <= end


def interval_margin_mm(interval: dict, x_mm: float) -> float:
    if not interval_contains_x(interval, x_mm):
        return math.nan
    return min(x_mm - safe_float(interval.get("start_x_mm")), safe_float(interval.get("end_x_mm")) - x_mm)


def nearest_interval(intervals: list[dict], x_mm: float) -> tuple[dict | None, float]:
    if not intervals or not math.isfinite(x_mm):
        return None, math.nan
    best = min(
        intervals,
        key=lambda interval: min(
            abs(x_mm - safe_float(interval.get("start_x_mm"))),
            abs(x_mm - safe_float(interval.get("end_x_mm"))),
            0.0 if interval_contains_x(interval, x_mm) else math.inf,
        ),
    )
    if interval_contains_x(best, x_mm):
        return best, 0.0
    distance = min(
        abs(x_mm - safe_float(best.get("start_x_mm"))),
        abs(x_mm - safe_float(best.get("end_x_mm"))),
    )
    return best, distance


def build_reconciliation_rows(timing_rows: list[dict], interval_rows: list[dict]) -> list[dict]:
    intervals = [
        row for row in interval_rows
        if str(row.get("support_key", "")) == "all_window_supported"
    ]
    out = []
    for anchor in short_anchor_rows(timing_rows):
        x_mm = safe_float(anchor.get("anchor_x_mm"))
        matched, distance = nearest_interval(intervals, x_mm)
        inside = bool(matched and interval_contains_x(matched, x_mm))
        margin = interval_margin_mm(matched, x_mm) if matched else math.nan
        out.append(
            {
                "support_anchor_id": anchor.get("support_anchor_id", ""),
                "support_category": anchor.get("support_category", ""),
                "support_label": anchor.get("support_label", ""),
                "is_claim_supporting": boolish(anchor.get("is_claim_supporting")),
                "anchor_x_mm": x_mm,
                "delta_to_short_content_half_widths": safe_float(anchor.get("delta_to_short_content_half_widths")),
                "timing_envelope_class": anchor.get("timing_envelope_class", ""),
                "matched_interval_index": matched.get("selected_interval_index", "") if matched else "",
                "matched_interval_start_x_mm": safe_float(matched.get("start_x_mm")) if matched else math.nan,
                "matched_interval_end_x_mm": safe_float(matched.get("end_x_mm")) if matched else math.nan,
                "inside_all_window_supported_interval": inside,
                "distance_to_nearest_supported_interval_mm": distance,
                "margin_to_supported_interval_edge_mm": margin,
                "interval_abs_correlation_improvement": safe_float(
                    matched.get("interval_abs_correlation_improvement")
                ) if matched else math.nan,
                "corrected_interval_abs_correlation": safe_float(
                    matched.get("corrected_interval_abs_correlation")
                ) if matched else math.nan,
                "allowed_use": anchor.get("allowed_use", ""),
                "blocked_use": anchor.get("blocked_use", ""),
            }
        )
    return out


def summarize(
    rows: list[dict],
    timing_summary: dict,
    supported_interval_summary: dict,
) -> dict:
    content_rows = [
        row for row in rows
        if row["support_category"] == "short_content_backed_time_zero_anchor"
    ]
    timing_only_rows = [
        row for row in rows
        if row["support_category"] == "short_timing_only_limited_cue"
    ]
    inside = lambda row: bool(row.get("inside_all_window_supported_interval"))
    margins = [
        safe_float(row.get("margin_to_supported_interval_edge_mm"))
        for row in rows
        if math.isfinite(safe_float(row.get("margin_to_supported_interval_edge_mm")))
    ]
    ready_short = (
        bool(rows)
        and all(inside(row) for row in rows)
        and bool(timing_summary.get("ready_for_short_relative_timing_qc", False))
        and str(supported_interval_summary.get("policy_label", "")) == "supported_interval_visual_qc_ready"
    )
    return {
        "policy_label": "gssi51600s_field_anchor_interval_reconciliation_short_qc_supported",
        "short_anchor_count": len(rows),
        "short_anchor_inside_supported_interval_count": sum(inside(row) for row in rows),
        "short_content_anchor_count": len(content_rows),
        "short_content_anchor_inside_supported_interval_count": sum(inside(row) for row in content_rows),
        "short_timing_only_anchor_count": len(timing_only_rows),
        "short_timing_only_anchor_inside_supported_interval_count": sum(inside(row) for row in timing_only_rows),
        "min_margin_to_supported_interval_edge_mm": min(margins) if margins else math.nan,
        "median_margin_to_supported_interval_edge_mm": float(np.median(margins)) if margins else math.nan,
        "supported_interval_visual_qc_policy_label": supported_interval_summary.get("policy_label", ""),
        "ready_for_short_relative_timing_qc": ready_short,
        "ready_for_absolute_time_zero": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as positive support for short-pair relative timing QC: the current short "
            "timing anchors fall inside the all-window-supported corrected-stack intervals. "
            "This remains short-profile visual/timing QC only and does not create absolute "
            "time-zero, cover-depth, radius, field FWI, 3D, or HPC readiness."
        ),
    }


def plot_reconciliation(rows: list[dict], intervals: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)

    ax = axes[0]
    for idx, interval in enumerate(intervals):
        if str(interval.get("support_key", "")) != "all_window_supported":
            continue
        start = safe_float(interval.get("start_x_mm"))
        end = safe_float(interval.get("end_x_mm"))
        ax.fill_betweenx([idx - 0.25, idx + 0.25], start, end, color="#8ab6d6", alpha=0.75)
        ax.text((start + end) / 2.0, idx + 0.3, f"interval {interval.get('selected_interval_index')}", ha="center", fontsize=8)
    for row in rows:
        color = "#4c9f70" if row["support_category"] == "short_content_backed_time_zero_anchor" else "#d08a2e"
        ax.scatter(row["anchor_x_mm"], safe_float(row.get("matched_interval_index"), 0.0) - 1.0, color=color, s=70, edgecolor="#333333", zorder=5)
        ax.text(row["anchor_x_mm"], safe_float(row.get("matched_interval_index"), 0.0) - 0.82, str(row["support_anchor_id"]), ha="center", fontsize=8)
    ax.set_xlabel("x (mm)")
    ax.set_yticks([])
    ax.set_title("Short timing anchors inside supported intervals")
    ax.grid(axis="x", color="#dddddd", linewidth=0.6)

    labels = [str(row["support_anchor_id"]).replace("_", "\n") for row in rows]
    margins = [safe_float(row.get("margin_to_supported_interval_edge_mm"), 0.0) for row in rows]
    colors = ["#4c9f70" if row["support_category"] == "short_content_backed_time_zero_anchor" else "#d08a2e" for row in rows]
    axes[1].bar(np.arange(len(rows)), margins, color=colors, edgecolor="#333333")
    axes[1].set_xticks(np.arange(len(rows)), labels, fontsize=8)
    axes[1].set_ylabel("margin to interval edge (mm)")
    axes[1].set_title("Anchor support margin")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"inside={summary['short_anchor_inside_supported_interval_count']}/{summary['short_anchor_count']}\n"
        f"content={summary['short_content_anchor_inside_supported_interval_count']}/{summary['short_content_anchor_count']}\n"
        "field FWI=false",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S short timing anchors reconcile with supported intervals", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_anchor_interval_reconciliation.png`",
                "",
                "This figure reconciles current short timing anchors with all-window-supported",
                "corrected-stack visual-QC intervals.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Short anchors inside supported intervals: `{summary['short_anchor_inside_supported_interval_count']}` / `{summary['short_anchor_count']}`.",
                f"Content-backed anchors inside supported intervals: `{summary['short_content_anchor_inside_supported_interval_count']}` / `{summary['short_content_anchor_count']}`.",
                f"Minimum margin to interval edge: `{summary['min_margin_to_supported_interval_edge_mm']}` mm.",
                f"Ready for short relative timing QC: `{summary['ready_for_short_relative_timing_qc']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Reconciliation rows: `{rows_csv.name}`.",
                f"- Summary JSON: `{summary_json.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved field timing-envelope and supported-interval rows only.",
                "It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or",
                "neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--timing-envelope-run", default=DEFAULT_TIMING_ENVELOPE_RUN)
    parser.add_argument("--supported-interval-run", default=DEFAULT_SUPPORTED_INTERVAL_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_anchor_interval_reconciliation")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_root = field_dataset_output_root(args.field_root, args.dataset_id)
    timing_dir = output_root / args.timing_envelope_run
    interval_dir = output_root / args.supported_interval_run
    timing_rows = read_csv_rows(timing_dir / "data/field_cue_timing_envelope_rows.csv")
    timing_summary = read_json(timing_dir / "data/field_cue_timing_envelope_summary.json")
    interval_rows = read_csv_rows(interval_dir / "data/supported_interval_visual_qc_rows.csv")
    interval_summary = read_json(interval_dir / "data/supported_interval_visual_qc_summary.json")
    reconciliation_rows = build_reconciliation_rows(timing_rows, interval_rows)
    summary = summarize(reconciliation_rows, timing_summary, interval_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(output_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_anchor_interval_reconciliation_rows.csv"
    summary_json = data_dir / "field_anchor_interval_reconciliation_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_anchor_interval_reconciliation.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in reconciliation_rows])
    plot_reconciliation(reconciliation_rows, interval_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_timing_envelope_rows_csv": str(timing_dir / "data/field_cue_timing_envelope_rows.csv"),
        "source_timing_envelope_summary_json": str(timing_dir / "data/field_cue_timing_envelope_summary.json"),
        "source_supported_interval_rows_csv": str(interval_dir / "data/supported_interval_visual_qc_rows.csv"),
        "source_supported_interval_summary_json": str(interval_dir / "data/supported_interval_visual_qc_summary.json"),
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json)
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_anchor_interval_reconciliation",
        {
            "timing_envelope_run": args.timing_envelope_run,
            "supported_interval_run": args.supported_interval_run,
            "dataset_id": args.dataset_id,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
