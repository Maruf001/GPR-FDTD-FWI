#!/usr/bin/env python3
"""Audit short-anchor spatial consistency for GSSI 51600S field timing claims."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CUE_SUPPORT_RUN = "113_gssi51600s_field_cue_support_catalog"
DEFAULT_ANCHOR_INTERVAL_RUN = "117_gssi51600s_field_anchor_interval_reconciliation_post_spatial_transfer"
DEFAULT_SHORT_ANCHOR_LEAVE_ONE_RUN = "120_gssi51600s_field_short_anchor_leave_one_audit"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def sign_label(value: float, tolerance: float = 1e-9) -> str:
    if not math.isfinite(value) or abs(value) <= tolerance:
        return "zero"
    return "positive" if value > 0 else "negative"


def short_anchor_rows(support_rows: list[dict], interval_rows: list[dict]) -> list[dict]:
    interval_by_id = {str(row.get("support_anchor_id", "")): row for row in interval_rows}
    outputs = []
    for row in support_rows:
        if row.get("support_family") != "short_relative_timing":
            continue
        anchor_id = str(row.get("support_anchor_id", ""))
        interval = interval_by_id.get(anchor_id, {})
        residual = safe_float(row.get("aligned_x_residual_mm"))
        offset = safe_float(row.get("offset_ns"))
        outputs.append(
            {
                "support_anchor_id": anchor_id,
                "support_category": row.get("support_category", ""),
                "support_label": row.get("support_label", ""),
                "is_claim_supporting": parse_bool(row.get("is_claim_supporting")),
                "anchor_x_mm": safe_float(row.get("anchor_x_mm")),
                "comparison_aligned_x_mm": safe_float(row.get("comparison_aligned_x_mm")),
                "aligned_x_residual_mm": residual,
                "abs_aligned_x_residual_mm": abs(residual) if math.isfinite(residual) else math.nan,
                "residual_sign": sign_label(residual),
                "offset_ns": offset,
                "quality_metric_value": safe_float(row.get("quality_metric_value")),
                "inside_all_window_supported_interval": parse_bool(
                    interval.get("inside_all_window_supported_interval")
                ),
                "margin_to_supported_interval_edge_mm": safe_float(
                    interval.get("margin_to_supported_interval_edge_mm")
                ),
                "allowed_use": row.get("allowed_use", ""),
                "blocked_use": row.get("blocked_use", ""),
            }
        )
    return sorted(outputs, key=lambda row: row["support_anchor_id"])


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def summarize_spatial_consistency(
    rows: list[dict],
    anchor_interval_summary: dict,
    leave_one_summary: dict,
) -> dict:
    content_rows = [
        row for row in rows
        if row["support_category"] == "short_content_backed_time_zero_anchor"
        and row["is_claim_supporting"]
    ]
    timing_only_rows = [
        row for row in rows
        if row["support_category"] == "short_timing_only_limited_cue"
    ]
    residuals = _finite([safe_float(row.get("aligned_x_residual_mm")) for row in rows])
    content_residuals = _finite([safe_float(row.get("aligned_x_residual_mm")) for row in content_rows])
    content_offsets = _finite([safe_float(row.get("offset_ns")) for row in content_rows])
    content_margins = _finite([safe_float(row.get("margin_to_supported_interval_edge_mm")) for row in content_rows])
    content_mean_residual = float(np.mean(content_residuals)) if content_residuals else math.nan
    content_residual_half_range = (
        (max(content_residuals) - min(content_residuals)) / 2.0 if len(content_residuals) >= 2 else 0.0
    )
    content_max_deviation_from_mean = (
        max(abs(value - content_mean_residual) for value in content_residuals)
        if content_residuals and math.isfinite(content_mean_residual)
        else math.nan
    )
    content_signs = {
        sign_label(value)
        for value in content_residuals
        if sign_label(value) != "zero"
    }
    min_content_margin = min(content_margins) if content_margins else math.nan
    content_single_translation_inside_margin = (
        len(content_residuals) >= 2
        and math.isfinite(content_max_deviation_from_mean)
        and math.isfinite(min_content_margin)
        and content_max_deviation_from_mean <= min_content_margin
    )
    content_residual_sign_consistent = len(content_signs) <= 1
    content_single_translation_supported = (
        content_single_translation_inside_margin and content_residual_sign_consistent
    )
    return {
        "policy_label": "gssi51600s_field_short_anchor_spatial_consistency_timing_qc_only",
        "short_anchor_count": len(rows),
        "content_anchor_count": len(content_rows),
        "timing_only_anchor_count": len(timing_only_rows),
        "content_anchor_inside_supported_interval_count": sum(
            row["inside_all_window_supported_interval"] for row in content_rows
        ),
        "content_residual_min_mm": min(content_residuals) if content_residuals else math.nan,
        "content_residual_max_mm": max(content_residuals) if content_residuals else math.nan,
        "content_residual_range_mm": max(content_residuals) - min(content_residuals)
        if len(content_residuals) >= 2
        else 0.0,
        "content_residual_half_range_mm": content_residual_half_range,
        "content_abs_residual_max_mm": max([abs(value) for value in content_residuals] or [math.nan]),
        "content_mean_residual_mm": content_mean_residual,
        "content_max_deviation_from_mean_residual_mm": content_max_deviation_from_mean,
        "content_min_supported_interval_margin_mm": min_content_margin,
        "content_residual_sign_consistent": content_residual_sign_consistent,
        "content_single_translation_inside_margin": content_single_translation_inside_margin,
        "content_single_translation_supported": content_single_translation_supported,
        "all_short_residual_range_mm": max(residuals) - min(residuals) if len(residuals) >= 2 else 0.0,
        "content_offset_half_range_ns": (max(content_offsets) - min(content_offsets)) / 2.0
        if len(content_offsets) >= 2
        else 0.0,
        "anchor_interval_ready_for_short_qc": bool(
            anchor_interval_summary.get("ready_for_short_relative_timing_qc", False)
        ),
        "leave_one_ready_for_short_qc": bool(
            leave_one_summary.get("ready_for_short_relative_timing_qc", False)
        ),
        "ready_for_short_relative_timing_qc": bool(
            anchor_interval_summary.get("ready_for_short_relative_timing_qc", False)
        )
        and bool(leave_one_summary.get("ready_for_short_relative_timing_qc", False)),
        "ready_for_profile_spatial_calibration": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "The short content-backed anchors support relative timing QC, but their signed spatial residuals "
            "do not support a single calibrated profile-to-profile translation. Keep field use at short-profile "
            "timing/visual QC, not cover-depth, radius, field FWI, 3D/HPC, or absolute time-zero."
        ),
    }


def plot_spatial_consistency(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["support_anchor_id"] for row in rows]
    residuals = [safe_float(row.get("aligned_x_residual_mm"), 0.0) for row in rows]
    offsets = [safe_float(row.get("offset_ns"), 0.0) for row in rows]
    colors = [
        "#4e79a7" if row["support_category"] == "short_content_backed_time_zero_anchor" else "#f28e2b"
        for row in rows
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    axes[0].bar(np.arange(len(rows)), residuals, color=colors, edgecolor="#333333", linewidth=0.5)
    axes[0].axhline(0.0, color="#333333", linewidth=0.8)
    axes[0].axhline(
        summary["content_mean_residual_mm"],
        color="#59a14f",
        linestyle="--",
        linewidth=1.2,
    )
    axes[0].set_xticks(np.arange(len(rows)), labels, rotation=20, ha="right")
    axes[0].set_ylabel("aligned x residual (mm)")
    axes[0].set_title("Short-anchor spatial residuals")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(np.arange(len(rows)), offsets, color=colors, edgecolor="#333333", linewidth=0.5)
    axes[1].set_xticks(np.arange(len(rows)), labels, rotation=20, ha="right")
    axes[1].set_ylabel("relative offset (ns)")
    axes[1].set_title("Short-anchor timing offsets")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"content residual range={summary['content_residual_range_mm']:.3f} mm\n"
        f"content half-range={summary['content_residual_half_range_mm']:.3f} mm\n"
        f"min interval margin={summary['content_min_supported_interval_margin_mm']:.3f} mm\n"
        f"single translation={summary['content_single_translation_supported']}\n"
        f"ready spatial calibration={summary['ready_for_profile_spatial_calibration']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S short-anchor timing versus spatial consistency", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_spatial_consistency_audit.png`",
                "",
                "This CPU-only figure compares short-anchor relative timing support",
                "against profile-to-profile spatial residual consistency.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Content anchor count: `{summary['content_anchor_count']}`.",
                f"Content residual range: `{summary['content_residual_range_mm']}` mm.",
                f"Content residual half-range: `{summary['content_residual_half_range_mm']}` mm.",
                f"Content minimum supported-interval margin: `{summary['content_min_supported_interval_margin_mm']}` mm.",
                f"Single translation supported: `{summary['content_single_translation_supported']}`.",
                f"Ready for short relative timing QC: `{summary['ready_for_short_relative_timing_qc']}`.",
                f"Ready for profile spatial calibration: `{summary['ready_for_profile_spatial_calibration']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Short-anchor rows: `{rows_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved field support-anchor summaries only. It does not",
                "run FDTD, FWI, GPU kernels, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--cue-support-run", default=DEFAULT_CUE_SUPPORT_RUN)
    parser.add_argument("--anchor-interval-run", default=DEFAULT_ANCHOR_INTERVAL_RUN)
    parser.add_argument("--short-anchor-leave-one-run", default=DEFAULT_SHORT_ANCHOR_LEAVE_ONE_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_spatial_consistency_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    cue_support_dir = field_root / args.cue_support_run
    anchor_interval_dir = field_root / args.anchor_interval_run
    leave_one_dir = field_root / args.short_anchor_leave_one_run

    support_rows = read_csv_rows(cue_support_dir / "data/field_support_anchor_catalog.csv")
    interval_rows = read_csv_rows(anchor_interval_dir / "data/field_anchor_interval_reconciliation_rows.csv")
    anchor_interval_summary = read_json(
        anchor_interval_dir / "data/field_anchor_interval_reconciliation_summary.json"
    )
    leave_one_summary = read_json(leave_one_dir / "data/field_short_anchor_leave_one_summary.json")
    rows = short_anchor_rows(support_rows, interval_rows)
    summary = summarize_spatial_consistency(rows, anchor_interval_summary, leave_one_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(field_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_short_anchor_spatial_consistency_rows.csv"
    summary_json = data_dir / "field_short_anchor_spatial_consistency_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_spatial_consistency_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_spatial_consistency(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv)
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "source_support_anchor_csv": str(cue_support_dir / "data/field_support_anchor_catalog.csv"),
        "source_anchor_interval_rows_csv": str(
            anchor_interval_dir / "data/field_anchor_interval_reconciliation_rows.csv"
        ),
        "source_anchor_interval_summary_json": str(
            anchor_interval_dir / "data/field_anchor_interval_reconciliation_summary.json"
        ),
        "source_short_anchor_leave_one_summary_json": str(
            leave_one_dir / "data/field_short_anchor_leave_one_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_short_anchor_spatial_consistency_audit",
        {
            "dataset_id": args.dataset_id,
            "cue_support_run": args.cue_support_run,
            "anchor_interval_run": args.anchor_interval_run,
            "short_anchor_leave_one_run": args.short_anchor_leave_one_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
