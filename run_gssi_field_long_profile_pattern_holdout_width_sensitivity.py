#!/usr/bin/env python3
"""Check long-profile pattern-holdout support across anchor spatial widths."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import build_profile_windows, safe_float  # noqa: E402
from run_gssi_field_long_profile_pattern_holdout_qc import (  # noqa: E402
    SUPPORTED_CORRELATION_MIN,
    annotate_support,
    select_anchor_candidates,
)
from run_gssi_field_long_profile_pattern_visual_qc import (  # noqa: E402
    DEFAULT_SHIFT_SENSITIVITY_RUN,
    pattern_window_metric_row,
)
from run_gssi_field_long_profile_shift_scan import DEFAULT_APPLIED_RUN, DEFAULT_LONG_STACK_RUN  # noqa: E402
from run_gssi_field_long_profile_transfer_audit import crop_x_window, read_csv_rows  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def parse_widths(value: str) -> list[float]:
    widths: list[float] = []
    for item in str(value).split(","):
        item = item.strip()
        if not item:
            continue
        width = float(item)
        if width <= 0.0:
            raise ValueError(f"anchor half-width must be positive: {item!r}")
        widths.append(width)
    if not widths:
        raise ValueError("at least one anchor half-width is required")
    return sorted(set(widths))


def holdout_rows_for_widths(
    profile_windows: dict,
    anchors: list[dict],
    *,
    anchor_half_widths_m: list[float],
) -> list[dict]:
    rows: list[dict] = []
    for half_width_m in anchor_half_widths_m:
        crops = [
            crop_x_window(profile_windows, safe_float(anchor.get("x_m")), half_width_m)
            for anchor in anchors
        ]
        annotated = annotate_support([
            {
                "anchor_half_width_m": half_width_m,
                "anchor_half_width_mm": 1000.0 * half_width_m,
                **pattern_window_metric_row(anchor, crop),
            }
            for anchor, crop in zip(anchors, crops)
        ])
        rows.extend(annotated)
    return rows


def anchor_summary_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[int(safe_float(row.get("anchor_index"), -1))].append(row)
    out: list[dict] = []
    for anchor_index, group in sorted(grouped.items()):
        gains = [
            safe_float(row.get("pattern_shift_abs_correlation_gain"))
            for row in group
            if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation_gain")))
        ]
        correlations = [
            safe_float(row.get("pattern_shift_abs_correlation"))
            for row in group
            if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation")))
        ]
        support_count = sum(1 for row in group if bool(row.get("is_supported")))
        out.append({
            "anchor_index": anchor_index,
            "center_x_m": safe_float(group[0].get("center_x_m")),
            "center_x_mm": safe_float(group[0].get("center_x_mm")),
            "stability_label": group[0].get("stability_label", ""),
            "width_count": len(group),
            "supported_width_count": support_count,
            "all_widths_supported": support_count == len(group),
            "min_pattern_shift_gain": min(gains) if gains else math.nan,
            "mean_pattern_shift_gain": float(np.mean(gains)) if gains else math.nan,
            "min_pattern_shift_abs_correlation": min(correlations) if correlations else math.nan,
            "mean_pattern_shift_abs_correlation": float(np.mean(correlations)) if correlations else math.nan,
        })
    return out


def width_summary_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[float, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[safe_float(row.get("anchor_half_width_m"))].append(row)
    out: list[dict] = []
    for width_m, group in sorted(grouped.items()):
        gains = [
            safe_float(row.get("pattern_shift_abs_correlation_gain"))
            for row in group
            if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation_gain")))
        ]
        correlations = [
            safe_float(row.get("pattern_shift_abs_correlation"))
            for row in group
            if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation")))
        ]
        support_count = sum(1 for row in group if bool(row.get("is_supported")))
        out.append({
            "anchor_half_width_m": width_m,
            "anchor_half_width_mm": 1000.0 * width_m,
            "anchor_count": len(group),
            "supported_anchor_count": support_count,
            "all_anchors_supported": support_count == len(group),
            "min_pattern_shift_gain": min(gains) if gains else math.nan,
            "mean_pattern_shift_gain": float(np.mean(gains)) if gains else math.nan,
            "min_pattern_shift_abs_correlation": min(correlations) if correlations else math.nan,
            "mean_pattern_shift_abs_correlation": float(np.mean(correlations)) if correlations else math.nan,
        })
    return out


def summarize_width_sensitivity(
    rows: list[dict],
    anchor_rows: list[dict],
    width_rows: list[dict],
    *,
    pattern_shift_ns: float,
) -> dict:
    stable = [row for row in anchor_rows if row.get("stability_label") == "stable_stack_anchor"]
    repeat_limited = [row for row in anchor_rows if row.get("stability_label") == "repeat_limited_anchor"]
    all_width_supported = [row for row in anchor_rows if bool(row.get("all_widths_supported"))]
    row_gains = [
        safe_float(row.get("pattern_shift_abs_correlation_gain"))
        for row in rows
        if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation_gain")))
    ]
    row_corrs = [
        safe_float(row.get("pattern_shift_abs_correlation"))
        for row in rows
        if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation")))
    ]
    stable_all = sum(1 for row in stable if bool(row.get("all_widths_supported")))
    repeat_all = sum(1 for row in repeat_limited if bool(row.get("all_widths_supported")))
    width_all = sum(1 for row in width_rows if bool(row.get("all_anchors_supported")))
    if anchor_rows and len(all_width_supported) == len(anchor_rows) and width_all == len(width_rows):
        label = "long_profile_pattern_holdout_width_sensitivity_all_candidate_anchors_all_widths_supported"
    elif stable and stable_all == len(stable):
        label = "long_profile_pattern_holdout_width_sensitivity_stable_all_widths_repeat_limited_mixed"
    else:
        label = "long_profile_pattern_holdout_width_sensitivity_limited"
    return {
        "policy_label": label,
        "pattern_shift_ns": pattern_shift_ns,
        "width_count": len(width_rows),
        "candidate_anchor_count": len(anchor_rows),
        "all_width_supported_anchor_count": len(all_width_supported),
        "widths_all_anchors_supported_count": width_all,
        "stable_anchor_count": len(stable),
        "stable_all_width_supported_count": stable_all,
        "repeat_limited_anchor_count": len(repeat_limited),
        "repeat_limited_all_width_supported_count": repeat_all,
        "row_count": len(rows),
        "supported_row_count": sum(1 for row in rows if bool(row.get("is_supported"))),
        "min_pattern_shift_gain": min(row_gains) if row_gains else math.nan,
        "min_pattern_shift_abs_correlation": min(row_corrs) if row_corrs else math.nan,
        "support_correlation_min": SUPPORTED_CORRELATION_MIN,
        "gpu_priority": "none",
        "policy": (
            "Use this as spatial-window sensitivity evidence for long-profile "
            "pattern-only QC. It does not create phase-anchor, absolute "
            "time-zero, 3D, radius, cover-depth, or FWI evidence."
        ),
    }


def plot_width_sensitivity(anchor_rows: list[dict], width_rows: list[dict], summary: dict, save_path: Path) -> str:
    anchor_labels = [
        f"{int(row['anchor_index'])}\n{row['stability_label'].replace('_', ' ')}"
        for row in anchor_rows
    ]
    ax_x = np.arange(len(anchor_rows))
    anchor_support = np.asarray([safe_float(row.get("supported_width_count")) for row in anchor_rows], dtype=np.float64)
    anchor_gains = np.asarray([safe_float(row.get("min_pattern_shift_gain")) for row in anchor_rows], dtype=np.float64)
    anchor_colors = [
        "#2f9d55" if row.get("stability_label") == "stable_stack_anchor" else "#d99a19"
        for row in anchor_rows
    ]

    width_labels = [f"{row['anchor_half_width_mm']:.0f} mm" for row in width_rows]
    width_x = np.arange(len(width_rows))
    width_support = np.asarray([safe_float(row.get("supported_anchor_count")) for row in width_rows], dtype=np.float64)

    fig, axes = plt.subplots(3, 1, figsize=(12.0, 8.6), constrained_layout=True)
    axes[0].bar(ax_x, anchor_support, color=anchor_colors)
    axes[0].axhline(summary["width_count"], color="#555555", linestyle="--", linewidth=0.9)
    axes[0].set_xticks(ax_x, anchor_labels)
    axes[0].set_ylabel("supported widths")
    axes[0].set_title("All-anchor support across anchor half-widths")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(ax_x, anchor_gains, color=anchor_colors)
    axes[1].axhline(0.0, color="#555555", linewidth=0.8)
    axes[1].set_xticks(ax_x, anchor_labels)
    axes[1].set_ylabel("minimum gain")
    axes[1].set_title("Worst-case pattern-shift gain by anchor")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(width_x, width_support, color="#4c78a8")
    axes[2].axhline(summary["candidate_anchor_count"], color="#555555", linestyle="--", linewidth=0.9)
    axes[2].set_xticks(width_x, width_labels)
    axes[2].set_ylabel("supported anchors")
    axes[2].set_title("Support by spatial half-width")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Long-profile pattern holdout width sensitivity: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--long-stack-run", default=DEFAULT_LONG_STACK_RUN)
    parser.add_argument("--applied-run", default=DEFAULT_APPLIED_RUN)
    parser.add_argument("--shift-sensitivity-run", default=DEFAULT_SHIFT_SENSITIVITY_RUN)
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--anchor-half-widths-m", default="0.035,0.05,0.075")
    parser.add_argument("--run-name", default="gssi51600s_long_profile_pattern_holdout_width_sensitivity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    long_json = dataset_root / args.long_stack_run / "data" / "long_profile_stack_policy_summary.json"
    anchors_csv = dataset_root / args.long_stack_run / "data" / "long_profile_stack_anchor_candidates.csv"
    shift_json = (
        dataset_root
        / args.shift_sensitivity_run
        / "data"
        / "long_profile_shift_scan_sensitivity_summary.json"
    )
    long_root = json.loads(long_json.read_text(encoding="utf-8"))
    shift_summary = json.loads(shift_json.read_text(encoding="utf-8"))
    long_summary = long_root.get("summary", {})
    dx_m = safe_float(long_root.get("dx_m"))
    lag_mm = safe_float(long_summary.get("best_lag_mm"))
    lag_samples = int(round((lag_mm / 1000.0) / dx_m)) if math.isfinite(lag_mm) and dx_m > 0.0 else 0
    orientation = str(long_summary.get("best_orientation", "direct"))
    pattern_shift_ns = safe_float(shift_summary.get("best_offset_median_ns"))
    time_window = tuple(float(part.strip()) for part in args.time_window_ns.split(",", 1))
    widths_m = parse_widths(args.anchor_half_widths_m)

    profiles = load_profile_map(Path(args.input_dir))
    anchors = select_anchor_candidates(read_csv_rows(anchors_csv))
    profile_windows = build_profile_windows(
        profiles,
        reference_stem=str(long_root.get("reference_stem", "PROJECT001C__015")),
        comparison_stem=str(long_root.get("comparison_stem", "PROJECT001C__013")),
        time_window_ns=time_window,
        transfer_offset_ns=pattern_shift_ns,
        orientation=orientation,
        lag_samples=lag_samples,
    )
    rows = holdout_rows_for_widths(
        profile_windows,
        anchors,
        anchor_half_widths_m=widths_m,
    )
    anchor_rows = anchor_summary_rows(rows)
    width_rows = width_summary_rows(rows)
    summary = summarize_width_sensitivity(rows, anchor_rows, width_rows, pattern_shift_ns=pattern_shift_ns)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "long_profile_pattern_holdout_width_sensitivity_rows.csv"
    anchor_rows_csv = data_dir / "long_profile_pattern_holdout_width_sensitivity_anchor_rows.csv"
    width_rows_csv = data_dir / "long_profile_pattern_holdout_width_sensitivity_width_rows.csv"
    summary_json = data_dir / "long_profile_pattern_holdout_width_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_width_sensitivity(
        anchor_rows,
        width_rows,
        summary,
        figures_dir / "long_profile_pattern_holdout_width_sensitivity.png",
    ))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(anchor_rows_csv, [json_safe(row) for row in anchor_rows])
    write_csv(width_rows_csv, [json_safe(row) for row in width_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "input_long_stack_summary_json": str(long_json),
        "input_anchor_candidates_csv": str(anchors_csv),
        "input_shift_sensitivity_summary_json": str(shift_json),
        "time_window_min_ns": time_window[0],
        "time_window_max_ns": time_window[1],
        "anchor_half_widths_m": args.anchor_half_widths_m,
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "anchor_rows_csv": str(anchor_rows_csv),
            "width_rows_csv": str(width_rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_long_profile_pattern_holdout_width_sensitivity",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "anchor_rows_csv": str(anchor_rows_csv),
            "width_rows_csv": str(width_rows_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
