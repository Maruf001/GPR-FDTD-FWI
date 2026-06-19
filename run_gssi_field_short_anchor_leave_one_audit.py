#!/usr/bin/env python3
"""Audit short field timing-anchor redundancy by leave-one/content-only subsets."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SUPPORT_CATALOG_RUN = "113_gssi51600s_field_cue_support_catalog"
DEFAULT_ANCHOR_INTERVAL_RUN = "117_gssi51600s_field_anchor_interval_reconciliation_post_spatial_transfer"
DEFAULT_LADDER_RUN = "119_gssi51600s_field_time_zero_evidence_ladder"


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
    return str(value).strip().lower() in {"1", "true", "yes", "y", "supported"}


def short_support_anchors(support_rows: list[dict], reconciliation_rows: list[dict]) -> list[dict]:
    """Join short support-catalog anchors to interval-reconciliation evidence."""
    interval_by_id = {
        str(row.get("support_anchor_id", "")): row
        for row in reconciliation_rows
        if str(row.get("support_anchor_id", ""))
    }
    anchors = []
    for row in support_rows:
        if str(row.get("support_family", "")) != "short_relative_timing":
            continue
        anchor_id = str(row.get("support_anchor_id", ""))
        interval = interval_by_id.get(anchor_id, {})
        category = str(row.get("support_category", ""))
        anchors.append(
            {
                "support_anchor_id": anchor_id,
                "support_category": category,
                "is_content_backed": category == "short_content_backed_time_zero_anchor",
                "is_claim_supporting": boolish(row.get("is_claim_supporting")),
                "anchor_x_mm": safe_float(row.get("anchor_x_mm")),
                "offset_ns": safe_float(row.get("offset_ns")),
                "quality_metric_value": safe_float(row.get("quality_metric_value")),
                "inside_supported_interval": boolish(interval.get("inside_all_window_supported_interval")),
                "margin_to_supported_interval_edge_mm": safe_float(
                    interval.get("margin_to_supported_interval_edge_mm")
                ),
                "allowed_use": row.get("allowed_use", ""),
                "blocked_use": row.get("blocked_use", ""),
            }
        )
    return sorted(anchors, key=lambda row: row["anchor_x_mm"])


def _subset_metrics(
    *,
    case_key: str,
    selection_rule: str,
    selected: list[dict],
    nominal_offset_ns: float,
    conservative_half_width_ns: float,
) -> dict:
    offsets = [
        safe_float(row.get("offset_ns"))
        for row in selected
        if math.isfinite(safe_float(row.get("offset_ns")))
    ]
    margins = [
        safe_float(row.get("margin_to_supported_interval_edge_mm"))
        for row in selected
        if math.isfinite(safe_float(row.get("margin_to_supported_interval_edge_mm")))
    ]
    qualities = [
        safe_float(row.get("quality_metric_value"))
        for row in selected
        if math.isfinite(safe_float(row.get("quality_metric_value")))
    ]
    content_count = sum(bool(row.get("is_content_backed")) for row in selected)
    inside_count = sum(bool(row.get("inside_supported_interval")) for row in selected)
    all_inside = bool(selected) and inside_count == len(selected)
    offset_span = max(offsets) - min(offsets) if len(offsets) >= 2 else 0.0
    half_range = offset_span / 2.0 if len(offsets) >= 2 else 0.0
    median_offset = float(np.median(offsets)) if offsets else math.nan
    if math.isfinite(median_offset) and math.isfinite(nominal_offset_ns):
        nominal_delta = abs(median_offset - nominal_offset_ns)
    else:
        nominal_delta = math.nan
    if math.isfinite(nominal_delta) and conservative_half_width_ns > 0:
        nominal_delta_half_widths = nominal_delta / conservative_half_width_ns
    else:
        nominal_delta_half_widths = math.nan

    content_redundant = content_count >= 2
    enough_offsets = len(offsets) >= 2
    within_conservative = (
        math.isfinite(half_range)
        and math.isfinite(conservative_half_width_ns)
        and half_range <= conservative_half_width_ns
    )
    supported = bool(selected) and enough_offsets and content_redundant and all_inside and within_conservative
    if supported:
        status = "content_redundant_supported"
    elif enough_offsets and all_inside and within_conservative:
        status = "degraded_single_content_anchor"
    elif not all_inside:
        status = "blocked_interval_support"
    else:
        status = "review"

    return {
        "case_key": case_key,
        "selection_rule": selection_rule,
        "selected_anchor_ids": ";".join(str(row.get("support_anchor_id", "")) for row in selected),
        "selected_anchor_count": len(selected),
        "content_anchor_count": content_count,
        "timing_only_anchor_count": len(selected) - content_count,
        "inside_supported_interval_count": inside_count,
        "all_inside_supported_intervals": all_inside,
        "offset_count": len(offsets),
        "median_offset_ns": median_offset,
        "min_offset_ns": min(offsets) if offsets else math.nan,
        "max_offset_ns": max(offsets) if offsets else math.nan,
        "offset_span_ns": offset_span,
        "offset_half_range_ns": half_range,
        "conservative_half_width_ns": conservative_half_width_ns,
        "median_delta_from_ladder_nominal_ns": nominal_delta,
        "median_delta_from_ladder_nominal_half_widths": nominal_delta_half_widths,
        "min_quality_metric_value": min(qualities) if qualities else math.nan,
        "min_margin_to_supported_interval_edge_mm": min(margins) if margins else math.nan,
        "content_redundant": content_redundant,
        "within_conservative_half_width": within_conservative,
        "short_relative_timing_supported": supported,
        "status": status,
    }


def build_leave_one_rows(
    anchors: list[dict],
    *,
    nominal_offset_ns: float,
    conservative_half_width_ns: float,
) -> list[dict]:
    rows = [
        _subset_metrics(
            case_key="all_short_anchors",
            selection_rule="all short anchors including timing-only cue",
            selected=anchors,
            nominal_offset_ns=nominal_offset_ns,
            conservative_half_width_ns=conservative_half_width_ns,
        ),
        _subset_metrics(
            case_key="content_backed_only",
            selection_rule="content-backed short anchors only",
            selected=[row for row in anchors if row["is_content_backed"]],
            nominal_offset_ns=nominal_offset_ns,
            conservative_half_width_ns=conservative_half_width_ns,
        ),
    ]
    for anchor in anchors:
        rows.append(
            _subset_metrics(
                case_key=f"leave_out_{anchor['support_anchor_id']}",
                selection_rule=f"all short anchors except {anchor['support_anchor_id']}",
                selected=[row for row in anchors if row["support_anchor_id"] != anchor["support_anchor_id"]],
                nominal_offset_ns=nominal_offset_ns,
                conservative_half_width_ns=conservative_half_width_ns,
            )
        )
    return rows


def summarize_leave_one(rows: list[dict], anchors: list[dict]) -> dict:
    by_key = {row["case_key"]: row for row in rows}
    leave_one_rows = [row for row in rows if row["case_key"].startswith("leave_out_")]
    content_only = by_key.get("content_backed_only", {})
    all_short = by_key.get("all_short_anchors", {})
    supported_leave_one = [
        row for row in leave_one_rows
        if bool(row.get("short_relative_timing_supported"))
    ]
    degraded_leave_one = [
        row for row in leave_one_rows
        if str(row.get("status")) == "degraded_single_content_anchor"
    ]
    timing_only_removal_supported = [
        row for row in supported_leave_one
        if row.get("timing_only_anchor_count") == 0
    ]
    content_only_half = safe_float(content_only.get("offset_half_range_ns"))
    all_half = safe_float(all_short.get("offset_half_range_ns"))
    content_only_tighter = (
        math.isfinite(content_only_half)
        and math.isfinite(all_half)
        and content_only_half < all_half
    )
    return {
        "policy_label": "gssi51600s_field_short_anchor_leave_one_content_redundancy_qc_only",
        "short_anchor_count": len(anchors),
        "short_content_anchor_count": sum(bool(row.get("is_content_backed")) for row in anchors),
        "short_timing_only_anchor_count": sum(not bool(row.get("is_content_backed")) for row in anchors),
        "audit_case_count": len(rows),
        "content_only_supported": bool(content_only.get("short_relative_timing_supported")),
        "content_only_offset_half_range_ns": content_only_half,
        "all_short_offset_half_range_ns": all_half,
        "content_only_tighter_than_all_short": content_only_tighter,
        "leave_one_case_count": len(leave_one_rows),
        "leave_one_supported_count": len(supported_leave_one),
        "leave_one_degraded_single_content_count": len(degraded_leave_one),
        "timing_only_removal_supported_count": len(timing_only_removal_supported),
        "ready_for_short_relative_timing_qc": bool(content_only.get("short_relative_timing_supported")),
        "ready_for_leave_one_content_anchor_claim": len(supported_leave_one) == len(leave_one_rows),
        "ready_for_absolute_time_zero": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this audit to sharpen the short-profile field claim: the timing-only "
            "short anchor can be removed and the two content-backed anchors still support "
            "a narrow relative timing interval, but removing either content-backed anchor "
            "leaves only one content anchor. This supports short relative timing QC only, "
            "not absolute time-zero, cover-depth/radius recovery, field FWI, 3D, or HPC."
        ),
    }


def plot_leave_one(rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    labels = [
        row["case_key"]
        .replace("all_short_anchors", "all\nshort")
        .replace("content_backed_only", "content\nonly")
        .replace("leave_out_", "drop\n")
        .replace("short_pair_", "pair ")
        for row in rows
    ]
    half_ranges = [safe_float(row.get("offset_half_range_ns"), 0.0) for row in rows]
    colors = [
        "#2f9d55" if row["short_relative_timing_supported"] else "#d99a19"
        for row in rows
    ]
    x = np.arange(len(rows))
    axes[0].bar(x, half_ranges, color=colors, edgecolor="#333333", linewidth=0.6)
    axes[0].axhline(
        safe_float(rows[0].get("conservative_half_width_ns"), 0.0),
        color="#444444",
        linestyle="--",
        linewidth=1.0,
        label="conservative half-width",
    )
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylabel("offset half-range (ns)")
    axes[0].set_title("Short-anchor subset stability")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(fontsize=8, loc="upper left")

    decision_labels = [
        "content\nonly",
        "all\nleave-one",
        "absolute\nt0",
        "field\nFWI",
        "3D\nHPC",
    ]
    decision_values = [
        summary["content_only_supported"],
        summary["ready_for_leave_one_content_anchor_claim"],
        summary["ready_for_absolute_time_zero"],
        summary["ready_for_field_fwi"],
        summary["ready_for_3d_hpc"],
    ]
    axes[1].bar(
        np.arange(len(decision_labels)),
        [1 if value else 0 for value in decision_values],
        color=["#2f9d55" if value else "#c7302b" for value in decision_values],
    )
    axes[1].set_xticks(np.arange(len(decision_labels)), decision_labels, fontsize=9)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_title("Field claim gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"anchors={summary['short_anchor_count']}\n"
        f"content={summary['short_content_anchor_count']}\n"
        f"content-only half-range={summary['content_only_offset_half_range_ns']:.6f} ns\n"
        f"leave-one supported={summary['leave_one_supported_count']}/{summary['leave_one_case_count']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local GSSI short time-zero anchor redundancy audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, anchors_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_leave_one_audit.png`",
                "",
                "This CPU-only field figure audits short-profile relative time-zero anchor redundancy.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Content-only supported: `{summary['content_only_supported']}`.",
                f"Leave-one supported cases: `{summary['leave_one_supported_count']}` / `{summary['leave_one_case_count']}`.",
                f"Ready for short relative timing QC: `{summary['ready_for_short_relative_timing_qc']}`.",
                f"Ready for absolute time-zero: `{summary['ready_for_absolute_time_zero']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"Ready for 3D/HPC: `{summary['ready_for_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Audit rows: `{rows_csv.name}`.",
                f"- Joined short-anchor rows: `{anchors_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads existing measured-field summaries only. It does not run FDTD, FWI,",
                "GPU kernels, 3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--support-catalog-run", default=DEFAULT_SUPPORT_CATALOG_RUN)
    parser.add_argument("--anchor-interval-run", default=DEFAULT_ANCHOR_INTERVAL_RUN)
    parser.add_argument("--ladder-run", default=DEFAULT_LADDER_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_leave_one_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    support_csv = dataset_root / args.support_catalog_run / "data/field_support_anchor_catalog.csv"
    reconciliation_csv = (
        dataset_root / args.anchor_interval_run / "data/field_anchor_interval_reconciliation_rows.csv"
    )
    ladder_summary_json = dataset_root / args.ladder_run / "data/field_time_zero_evidence_ladder_summary.json"

    support_rows = read_csv_rows(support_csv)
    reconciliation_rows = read_csv_rows(reconciliation_csv)
    ladder = read_json(ladder_summary_json)
    anchors = short_support_anchors(support_rows, reconciliation_rows)
    rows = build_leave_one_rows(
        anchors,
        nominal_offset_ns=safe_float(ladder.get("short_relative_offset_ns")),
        conservative_half_width_ns=safe_float(ladder.get("short_conservative_half_width_ns")),
    )
    summary = summarize_leave_one(rows, anchors)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_short_anchor_leave_one_rows.csv"
    anchors_csv = data_dir / "field_short_anchor_joined_rows.csv"
    summary_json = data_dir / "field_short_anchor_leave_one_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_leave_one_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(anchors_csv, [json_safe(row) for row in anchors])
    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_leave_one(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "joined_anchors_csv": str(anchors_csv),
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, anchors_csv)
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_leave_one_audit",
        {
            "support_catalog_run": args.support_catalog_run,
            "anchor_interval_run": args.anchor_interval_run,
            "ladder_run": args.ladder_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
