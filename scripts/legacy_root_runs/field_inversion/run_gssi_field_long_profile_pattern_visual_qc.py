#!/usr/bin/env python3
"""Create long-profile pattern-only visual QC panels at the robust shift."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import (  # noqa: E402
    build_profile_windows,
    compare_matrices,
    safe_float,
)
from run_gssi_field_long_profile_shift_scan import DEFAULT_APPLIED_RUN, DEFAULT_LONG_STACK_RUN  # noqa: E402
from run_gssi_field_long_profile_transfer_audit import crop_x_window, read_csv_rows  # noqa: E402
from run_gssi_field_preprocess_feature_qc import imshow_extent, json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from run_gssi_field_synthetic_waveform_probe import robust_normalize  # noqa: E402
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_SHIFT_SENSITIVITY_RUN = "055_gssi51600s_long_profile_shift_scan_sensitivity"


def select_stable_anchors(anchor_rows: list[dict], *, max_anchor_windows: int) -> list[dict]:
    stable = [row for row in anchor_rows if str(row.get("stability_label")) == "stable_stack_anchor"]
    if max_anchor_windows > 0 and len(stable) > max_anchor_windows:
        stable = sorted(
            stable,
            key=lambda row: safe_float(row.get("candidate_rank_score"), -math.inf),
            reverse=True,
        )[:max_anchor_windows]
    return sorted(stable, key=lambda row: safe_float(row.get("x_m")))


def pattern_window_metric_row(anchor: dict, crop: dict) -> dict:
    raw_metrics = compare_matrices(crop["reference_window"], crop["raw_aligned_comparison"])
    shifted_metrics = compare_matrices(crop["reference_window"], crop["corrected_aligned_comparison"])
    raw_abs = safe_float(raw_metrics.get("absolute_correlation"))
    shifted_abs = safe_float(shifted_metrics.get("absolute_correlation"))
    center = safe_float(anchor.get("x_m"))
    return {
        "anchor_index": int(safe_float(anchor.get("candidate_index"), 0)),
        "center_x_m": center,
        "center_x_mm": 1000.0 * center,
        "stability_label": str(anchor.get("stability_label", "")),
        "window_start_x_m": float(crop["x_m"][0]),
        "window_end_x_m": float(crop["x_m"][-1]),
        "window_length_m": float(crop["x_m"][-1] - crop["x_m"][0]),
        "zero_shift_abs_correlation": raw_abs,
        "pattern_shift_abs_correlation": shifted_abs,
        "pattern_shift_abs_correlation_gain": (
            shifted_abs - raw_abs if math.isfinite(raw_abs) and math.isfinite(shifted_abs) else math.nan
        ),
        "zero_shift_residual_rms": safe_float(raw_metrics.get("normalized_residual_rms")),
        "pattern_shift_residual_rms": safe_float(shifted_metrics.get("normalized_residual_rms")),
        "valid_sample_count": int(shifted_metrics.get("valid_sample_count", 0)),
    }


def summarize_pattern_visual_qc(rows: list[dict], *, pattern_shift_ns: float) -> dict:
    gains = [
        safe_float(row.get("pattern_shift_abs_correlation_gain"))
        for row in rows
        if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation_gain")))
    ]
    shifted = [
        safe_float(row.get("pattern_shift_abs_correlation"))
        for row in rows
        if math.isfinite(safe_float(row.get("pattern_shift_abs_correlation")))
    ]
    supported_count = sum(
        1 for row in rows
        if safe_float(row.get("pattern_shift_abs_correlation_gain")) > 0.0
        and safe_float(row.get("pattern_shift_abs_correlation")) >= 0.75
    )
    if rows and supported_count == len(rows):
        label = "long_profile_pattern_visual_qc_ready"
    elif supported_count:
        label = "long_profile_pattern_visual_qc_limited"
    else:
        label = "long_profile_pattern_visual_qc_not_supported"
    return {
        "policy_label": label,
        "pattern_shift_ns": pattern_shift_ns,
        "selected_anchor_window_count": len(rows),
        "supported_anchor_window_count": supported_count,
        "min_pattern_shift_gain": min(gains) if gains else math.nan,
        "mean_pattern_shift_gain": float(np.mean(gains)) if gains else math.nan,
        "min_pattern_shift_abs_correlation": min(shifted) if shifted else math.nan,
        "mean_pattern_shift_abs_correlation": float(np.mean(shifted)) if shifted else math.nan,
        "policy": (
            "Use these panels as long-profile pattern-QC visualization only. "
            "The shift is not a phase anchor or absolute time-zero calibration "
            "because profile 013 lacks phase-anchor picks."
        ),
    }


def _panel_limits(crops: list[dict]) -> tuple[float, float]:
    values: list[np.ndarray] = []
    for crop in crops:
        for key in ("reference_window", "raw_aligned_comparison", "corrected_aligned_comparison"):
            matrix = np.asarray(crop[key], dtype=np.float64)
            if np.any(np.isfinite(matrix)):
                values.append(matrix[np.isfinite(matrix)])
    if not values:
        return (-1.0, 1.0)
    return safe_symmetric_limits(np.concatenate(values), percentile=98.0, floor=1.0)


def plot_pattern_visual_qc(crops: list[dict], rows: list[dict], summary: dict, save_path: Path) -> str:
    row_count = max(1, len(crops))
    fig, axes = plt.subplots(row_count, 4, figsize=(15.2, 2.8 * row_count), constrained_layout=True)
    axes = np.asarray(axes).reshape(row_count, 4)
    limits = _panel_limits(crops)
    shift_ns = safe_float(summary.get("pattern_shift_ns"))

    for row_idx, (crop, row) in enumerate(zip(crops, rows)):
        reference = crop["reference_window"]
        raw = crop["raw_aligned_comparison"]
        shifted = crop["corrected_aligned_comparison"]
        residual = robust_normalize(reference) - robust_normalize(shifted)
        extent = imshow_extent(crop["x_m"], crop["time_ns"])
        panels = [
            (reference, "015 reference", "seismic", limits),
            (raw, f"013 zero |corr|={row['zero_shift_abs_correlation']:.3f}", "seismic", limits),
            (shifted, f"013 +{shift_ns:.3f} ns |corr|={row['pattern_shift_abs_correlation']:.3f}", "seismic", limits),
            (residual, "normalized residual", "coolwarm", (-2.5, 2.5)),
        ]
        for col_idx, (matrix, title, cmap, clim) in enumerate(panels):
            image = axes[row_idx, col_idx].imshow(
                matrix,
                aspect="auto",
                extent=extent,
                cmap=cmap,
                vmin=clim[0],
                vmax=clim[1],
            )
            axes[row_idx, col_idx].set_title(title, fontsize=9)
            axes[row_idx, col_idx].set_xlabel("aligned x [m]")
            axes[row_idx, col_idx].set_ylabel("time [ns]")
            fig.colorbar(image, ax=axes[row_idx, col_idx], shrink=0.68)
        axes[row_idx, 0].text(
            0.01,
            0.98,
            f"anchor {int(row['anchor_index'])}: x={safe_float(row['center_x_m']):.3f} m",
            transform=axes[row_idx, 0].transAxes,
            va="top",
            ha="left",
            fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.8, "pad": 2},
        )

    fig.suptitle(
        (
            "Long-profile pattern visual QC: "
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
    parser.add_argument("--max-anchor-windows", type=int, default=6)
    parser.add_argument("--run-name", default="gssi51600s_long_profile_pattern_visual_qc")
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
    selected_anchors = select_stable_anchors(
        read_csv_rows(anchors_csv),
        max_anchor_windows=args.max_anchor_windows,
    )
    crops = [crop_x_window(windows, safe_float(anchor.get("x_m")), args.anchor_half_width_m) for anchor in selected_anchors]
    rows = [pattern_window_metric_row(anchor, crop) for anchor, crop in zip(selected_anchors, crops)]
    summary = summarize_pattern_visual_qc(rows, pattern_shift_ns=pattern_shift_ns)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "long_profile_pattern_visual_qc_rows.csv"
    summary_json = data_dir / "long_profile_pattern_visual_qc_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_pattern_visual_qc(crops, rows, summary, figures_dir / "long_profile_pattern_visual_qc.png"))

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
        "gssi_field_long_profile_pattern_visual_qc",
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
