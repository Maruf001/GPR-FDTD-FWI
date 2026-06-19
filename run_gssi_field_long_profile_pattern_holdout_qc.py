#!/usr/bin/env python3
"""Evaluate long-profile pattern shift on stable and repeat-limited anchors."""

from __future__ import annotations

import argparse
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import build_profile_windows, safe_float  # noqa: E402
from run_gssi_field_long_profile_pattern_visual_qc import (  # noqa: E402
    DEFAULT_SHIFT_SENSITIVITY_RUN,
    pattern_window_metric_row,
)
from run_gssi_field_long_profile_shift_scan import DEFAULT_APPLIED_RUN, DEFAULT_LONG_STACK_RUN  # noqa: E402
from run_gssi_field_long_profile_transfer_audit import crop_x_window, read_csv_rows  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


SUPPORTED_CORRELATION_MIN = 0.75


def select_anchor_candidates(anchor_rows: list[dict], labels: set[str] | None = None) -> list[dict]:
    selected: list[dict] = []
    for row in anchor_rows:
        label = str(row.get("stability_label", ""))
        if labels is not None and label not in labels:
            continue
        if math.isfinite(safe_float(row.get("x_m"))):
            selected.append(row)
    return sorted(selected, key=lambda row: safe_float(row.get("x_m")))


def annotate_support(rows: list[dict], *, corr_min: float = SUPPORTED_CORRELATION_MIN) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        gain = safe_float(row.get("pattern_shift_abs_correlation_gain"))
        corr = safe_float(row.get("pattern_shift_abs_correlation"))
        supported = math.isfinite(gain) and math.isfinite(corr) and gain > 0.0 and corr >= corr_min
        annotated = dict(row)
        annotated["support_label"] = "supported" if supported else "not_supported"
        annotated["is_supported"] = supported
        out.append(annotated)
    return out


def summarize_holdout_qc(rows: list[dict], *, pattern_shift_ns: float) -> dict:
    stable = [row for row in rows if row.get("stability_label") == "stable_stack_anchor"]
    repeat_limited = [row for row in rows if row.get("stability_label") == "repeat_limited_anchor"]

    def supported_count(group: list[dict]) -> int:
        return sum(1 for row in group if bool(row.get("is_supported")))

    def min_gain(group: list[dict]) -> float:
        values = [safe_float(row.get("pattern_shift_abs_correlation_gain")) for row in group]
        values = [value for value in values if math.isfinite(value)]
        return min(values) if values else math.nan

    def min_corr(group: list[dict]) -> float:
        values = [safe_float(row.get("pattern_shift_abs_correlation")) for row in group]
        values = [value for value in values if math.isfinite(value)]
        return min(values) if values else math.nan

    stable_supported = supported_count(stable)
    repeat_supported = supported_count(repeat_limited)
    if rows and stable_supported == len(stable) and repeat_supported == len(repeat_limited):
        label = "long_profile_pattern_holdout_qc_all_candidate_anchors_supported"
    elif stable and stable_supported == len(stable):
        label = "long_profile_pattern_holdout_qc_stable_supported_repeat_limited_mixed"
    else:
        label = "long_profile_pattern_holdout_qc_stable_not_fully_supported"

    return {
        "policy_label": label,
        "pattern_shift_ns": pattern_shift_ns,
        "candidate_anchor_count": len(rows),
        "stable_anchor_count": len(stable),
        "stable_supported_anchor_count": stable_supported,
        "repeat_limited_anchor_count": len(repeat_limited),
        "repeat_limited_supported_anchor_count": repeat_supported,
        "min_stable_pattern_shift_gain": min_gain(stable),
        "min_stable_pattern_shift_abs_correlation": min_corr(stable),
        "min_repeat_limited_pattern_shift_gain": min_gain(repeat_limited),
        "min_repeat_limited_pattern_shift_abs_correlation": min_corr(repeat_limited),
        "gpu_priority": "none",
        "policy": (
            "Use this as holdout stress QC for the long-profile pattern shift. "
            "Stable anchors remain the claim-bearing support; repeat-limited "
            "anchors are diagnostic only and do not create phase-anchor, "
            "absolute time-zero, 3D, radius, cover-depth, or FWI evidence."
        ),
    }


def plot_holdout_qc(rows: list[dict], summary: dict, save_path: Path) -> str:
    x_m = np.asarray([safe_float(row.get("center_x_m")) for row in rows], dtype=np.float64)
    gain = np.asarray([safe_float(row.get("pattern_shift_abs_correlation_gain")) for row in rows], dtype=np.float64)
    corr = np.asarray([safe_float(row.get("pattern_shift_abs_correlation")) for row in rows], dtype=np.float64)
    raw_corr = np.asarray([safe_float(row.get("zero_shift_abs_correlation")) for row in rows], dtype=np.float64)
    colors = [
        "#2f9d55" if row.get("stability_label") == "stable_stack_anchor" else "#d99a19"
        for row in rows
    ]
    markers = [
        "o" if row.get("support_label") == "supported" else "x"
        for row in rows
    ]

    fig, axes = plt.subplots(2, 1, figsize=(11.6, 7.0), constrained_layout=True)
    axes[0].bar(x_m, gain, width=0.045, color=colors, edgecolor="#333333", linewidth=0.5)
    axes[0].axhline(0.0, color="#555555", linewidth=0.8)
    axes[0].set_ylabel("gain vs zero-shift |corr|")
    axes[0].set_xlabel("profile distance [m]")
    axes[0].set_title("Pattern-shift correlation gain at all candidate anchors")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    for value_x, value_corr, value_raw, marker, color in zip(x_m, corr, raw_corr, markers, colors):
        axes[1].scatter(value_x, value_corr, marker=marker, color=color, s=48)
        axes[1].plot([value_x, value_x], [value_raw, value_corr], color=color, alpha=0.45, linewidth=1.0)
    axes[1].axhline(SUPPORTED_CORRELATION_MIN, color="#555555", linestyle="--", linewidth=0.9)
    axes[1].set_ylabel("abs correlation")
    axes[1].set_xlabel("profile distance [m]")
    axes[1].set_title("Zero-shift to pattern-shift absolute correlation")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.01,
        0.04,
        "green=stable anchor, amber=repeat-limited holdout; x marker=not supported",
        transform=axes[1].transAxes,
        fontsize=8,
        ha="left",
        va="bottom",
    )

    fig.suptitle(
        (
            "Long-profile pattern holdout QC: "
            f"{summary['policy_label']}, shift=+{summary['pattern_shift_ns']:.3f} ns"
        ),
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
    parser.add_argument("--anchor-half-width-m", type=float, default=0.05)
    parser.add_argument("--run-name", default="gssi51600s_long_profile_pattern_holdout_qc")
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

    profiles = load_profile_map(Path(args.input_dir))
    windows = build_profile_windows(
        profiles,
        reference_stem=str(long_root.get("reference_stem", "PROJECT001C__015")),
        comparison_stem=str(long_root.get("comparison_stem", "PROJECT001C__013")),
        time_window_ns=time_window,
        transfer_offset_ns=pattern_shift_ns,
        orientation=orientation,
        lag_samples=lag_samples,
    )
    selected_anchors = select_anchor_candidates(read_csv_rows(anchors_csv))
    crops = [crop_x_window(windows, safe_float(anchor.get("x_m")), args.anchor_half_width_m) for anchor in selected_anchors]
    rows = annotate_support([
        pattern_window_metric_row(anchor, crop)
        for anchor, crop in zip(selected_anchors, crops)
    ])
    summary = summarize_holdout_qc(rows, pattern_shift_ns=pattern_shift_ns)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "long_profile_pattern_holdout_qc_rows.csv"
    summary_json = data_dir / "long_profile_pattern_holdout_qc_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_holdout_qc(rows, summary, figures_dir / "long_profile_pattern_holdout_qc.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "input_long_stack_summary_json": str(long_json),
        "input_anchor_candidates_csv": str(anchors_csv),
        "input_shift_sensitivity_summary_json": str(shift_json),
        "time_window_min_ns": time_window[0],
        "time_window_max_ns": time_window[1],
        "anchor_half_width_m": args.anchor_half_width_m,
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_long_profile_pattern_holdout_qc",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
