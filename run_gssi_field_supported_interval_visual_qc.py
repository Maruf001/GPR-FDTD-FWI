#!/usr/bin/env python3
"""Create visual-QC panels restricted to supported corrected-stack intervals."""

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
    DEFAULT_APPLIED_RUN,
    DEFAULT_STACK_RUN,
    build_profile_windows,
    compare_matrices,
    safe_float,
)
from run_gssi_field_preprocess_feature_qc import imshow_extent, json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from run_gssi_field_synthetic_waveform_probe import robust_normalize  # noqa: E402
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_SUPPORT_RUN = "047_gssi51600s_corrected_stack_spatial_support"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select_supported_intervals(
    interval_rows: list[dict],
    *,
    support_key: str = "all_window_supported",
    max_intervals: int = 3,
    min_length_m: float = 0.02,
) -> list[dict]:
    candidates = [
        row for row in interval_rows
        if str(row.get("support_key")) == support_key
        and safe_float(row.get("length_m")) >= min_length_m
    ]
    if not candidates and support_key != "majority_supported":
        candidates = [
            row for row in interval_rows
            if str(row.get("support_key")) == "majority_supported"
            and safe_float(row.get("length_m")) >= min_length_m
        ]
    selected = sorted(
        candidates,
        key=lambda row: (
            safe_float(row.get("length_m")),
            safe_float(row.get("mean_corrected_abs_correlation")),
            safe_float(row.get("mean_column_improvement")),
        ),
        reverse=True,
    )[: int(max_intervals)]
    selected = sorted(selected, key=lambda row: safe_float(row.get("start_x_m")))
    return [
        {
            **row,
            "selected_interval_index": idx,
        }
        for idx, row in enumerate(selected, start=1)
    ]


def crop_interval(windows: dict, interval: dict, *, pad_columns: int = 1) -> dict:
    x_m = np.asarray(windows["x_m"], dtype=np.float64)
    start = safe_float(interval.get("start_x_m"))
    stop = safe_float(interval.get("end_x_m"))
    idx = np.where((x_m >= start) & (x_m <= stop))[0]
    if idx.size == 0:
        raise ValueError(f"interval has no columns: {start}..{stop} m")
    first = max(0, int(idx[0]) - int(pad_columns))
    last = min(x_m.size - 1, int(idx[-1]) + int(pad_columns))
    sl = slice(first, last + 1)
    return {
        "x_m": x_m[sl],
        "time_ns": np.asarray(windows["time_ns"], dtype=np.float64),
        "reference_window": np.asarray(windows["reference_window"], dtype=np.float64)[:, sl],
        "raw_aligned_comparison": np.asarray(windows["raw_aligned_comparison"], dtype=np.float64)[:, sl],
        "corrected_aligned_comparison": np.asarray(windows["corrected_aligned_comparison"], dtype=np.float64)[:, sl],
        "column_start": first,
        "column_end": last,
    }


def interval_metric_row(interval: dict, cropped: dict) -> dict:
    reference = cropped["reference_window"]
    raw = cropped["raw_aligned_comparison"]
    corrected = cropped["corrected_aligned_comparison"]
    raw_metrics = compare_matrices(reference, raw)
    corrected_metrics = compare_matrices(reference, corrected)
    raw_abs = safe_float(raw_metrics.get("absolute_correlation"))
    corrected_abs = safe_float(corrected_metrics.get("absolute_correlation"))
    return {
        **interval,
        "crop_column_start": int(cropped["column_start"]),
        "crop_column_end": int(cropped["column_end"]),
        "crop_column_count": int(cropped["column_end"]) - int(cropped["column_start"]) + 1,
        "crop_start_x_m": float(cropped["x_m"][0]),
        "crop_end_x_m": float(cropped["x_m"][-1]),
        "raw_interval_abs_correlation": raw_abs,
        "corrected_interval_abs_correlation": corrected_abs,
        "interval_abs_correlation_improvement": (
            corrected_abs - raw_abs if math.isfinite(raw_abs) and math.isfinite(corrected_abs) else math.nan
        ),
        "raw_interval_residual_rms": safe_float(raw_metrics.get("normalized_residual_rms")),
        "corrected_interval_residual_rms": safe_float(corrected_metrics.get("normalized_residual_rms")),
        "valid_interval_sample_count": int(corrected_metrics.get("valid_sample_count", 0)),
    }


def summarize_visual_qc(rows: list[dict], *, requested_support_key: str) -> dict:
    improvements = [
        safe_float(row.get("interval_abs_correlation_improvement"))
        for row in rows
        if math.isfinite(safe_float(row.get("interval_abs_correlation_improvement")))
    ]
    corrected = [
        safe_float(row.get("corrected_interval_abs_correlation"))
        for row in rows
        if math.isfinite(safe_float(row.get("corrected_interval_abs_correlation")))
    ]
    lengths = [
        safe_float(row.get("length_m"))
        for row in rows
        if math.isfinite(safe_float(row.get("length_m")))
    ]
    supported_count = sum(
        1 for row in rows
        if safe_float(row.get("corrected_interval_abs_correlation")) >= 0.75
        and safe_float(row.get("interval_abs_correlation_improvement")) > 0.0
    )
    if rows and supported_count == len(rows):
        label = "supported_interval_visual_qc_ready"
    elif supported_count:
        label = "supported_interval_visual_qc_limited"
    else:
        label = "supported_interval_visual_qc_not_supported"
    return {
        "policy_label": label,
        "requested_support_key": requested_support_key,
        "selected_interval_count": len(rows),
        "supported_interval_count": supported_count,
        "total_selected_interval_length_m": float(np.sum(lengths)) if lengths else math.nan,
        "min_interval_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "mean_interval_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "min_corrected_interval_abs_correlation": min(corrected) if corrected else math.nan,
        "mean_corrected_interval_abs_correlation": float(np.mean(corrected)) if corrected else math.nan,
        "policy": (
            "Use these panels as the supported field visual-QC endpoint. They "
            "are restricted to intervals supported by the corrected-stack "
            "spatial mask and remain timing/repeatability QC only."
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


def plot_supported_intervals(crops: list[dict], rows: list[dict], summary: dict, save_path: Path) -> str:
    row_count = max(1, len(crops))
    fig, axes = plt.subplots(row_count, 4, figsize=(15.0, 3.4 * row_count), constrained_layout=True)
    axes = np.asarray(axes).reshape(row_count, 4)
    limits = _panel_limits(crops)

    for row_idx, (crop, row) in enumerate(zip(crops, rows)):
        reference = crop["reference_window"]
        raw = crop["raw_aligned_comparison"]
        corrected = crop["corrected_aligned_comparison"]
        stack = 0.5 * (robust_normalize(reference) + robust_normalize(corrected))
        residual = robust_normalize(reference) - robust_normalize(corrected)
        extent = imshow_extent(crop["x_m"], crop["time_ns"])
        panels = [
            (reference, "014 reference", "seismic", limits),
            (raw, f"016 before |corr|={row['raw_interval_abs_correlation']:.3f}", "seismic", limits),
            (corrected, f"016 after |corr|={row['corrected_interval_abs_correlation']:.3f}", "seismic", limits),
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
            fig.colorbar(image, ax=axes[row_idx, col_idx], shrink=0.72)
        axes[row_idx, 0].text(
            0.01,
            0.98,
            (
                f"interval {int(row['selected_interval_index'])}: "
                f"{safe_float(row['start_x_m']):.3f}-{safe_float(row['end_x_m']):.3f} m"
            ),
            transform=axes[row_idx, 0].transAxes,
            va="top",
            ha="left",
            fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.8, "pad": 2},
        )

    fig.suptitle(
        (
            "Supported corrected-stack visual QC: "
            f"{summary['policy_label']}, selected={summary['selected_interval_count']}"
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
    parser.add_argument("--stack-run", default=DEFAULT_STACK_RUN)
    parser.add_argument("--applied-run", default=DEFAULT_APPLIED_RUN)
    parser.add_argument("--support-run", default=DEFAULT_SUPPORT_RUN)
    parser.add_argument("--reference-stem", default="PROJECT001C__014")
    parser.add_argument("--comparison-stem", default="PROJECT001C__016")
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--support-key", default="all_window_supported")
    parser.add_argument("--max-intervals", type=int, default=3)
    parser.add_argument("--min-length-m", type=float, default=0.02)
    parser.add_argument("--pad-columns", type=int, default=1)
    parser.add_argument("--run-name", default="gssi51600s_supported_interval_visual_qc")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    stack_json = dataset_root / args.stack_run / "data" / "short_profile_stack_policy_summary.json"
    applied_json = dataset_root / args.applied_run / "data" / "short_profile_time_zero_application_summary.json"
    intervals_csv = dataset_root / args.support_run / "data" / "corrected_stack_spatial_support_intervals.csv"
    stack_root = json.loads(stack_json.read_text(encoding="utf-8"))
    applied_root = json.loads(applied_json.read_text(encoding="utf-8"))
    stack_summary = stack_root.get("summary", {})
    applied_summary = applied_root.get("summary", {})
    dx_m = safe_float(stack_root.get("dx_m"))
    lag_mm = safe_float(stack_summary.get("best_lag_mm"))
    lag_samples = int(round((lag_mm / 1000.0) / dx_m)) if math.isfinite(lag_mm) and dx_m > 0.0 else 0
    orientation = str(stack_summary.get("best_orientation", "direct"))
    transfer_offset_ns = safe_float(applied_summary.get("applied_transfer_offset_ns"))
    time_window = tuple(float(part.strip()) for part in args.time_window_ns.split(",", 1))

    selected = select_supported_intervals(
        read_csv_rows(intervals_csv),
        support_key=args.support_key,
        max_intervals=args.max_intervals,
        min_length_m=args.min_length_m,
    )
    if not selected:
        raise ValueError("no supported intervals selected")
    profiles = load_profile_map(Path(args.input_dir))
    windows = build_profile_windows(
        profiles,
        reference_stem=args.reference_stem,
        comparison_stem=args.comparison_stem,
        time_window_ns=time_window,
        transfer_offset_ns=transfer_offset_ns,
        orientation=orientation,
        lag_samples=lag_samples,
    )
    crops = [crop_interval(windows, row, pad_columns=args.pad_columns) for row in selected]
    rows = [interval_metric_row(interval, crop) for interval, crop in zip(selected, crops)]
    summary = summarize_visual_qc(rows, requested_support_key=args.support_key)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    intervals_out_csv = data_dir / "supported_interval_visual_qc_rows.csv"
    summary_json = data_dir / "supported_interval_visual_qc_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_supported_intervals(crops, rows, summary, figures_dir / "supported_interval_visual_qc.png"))

    write_csv(intervals_out_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "reference_stem": args.reference_stem,
        "comparison_stem": args.comparison_stem,
        "time_window_min_ns": time_window[0],
        "time_window_max_ns": time_window[1],
        "input_intervals_csv": str(intervals_csv),
        **summary,
        "paths": {
            "intervals_csv": str(intervals_out_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_supported_interval_visual_qc",
        {
            "summary_json": str(summary_json),
            "intervals_csv": str(intervals_out_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
