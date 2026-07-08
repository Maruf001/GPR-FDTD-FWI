#!/usr/bin/env python3
"""Derive spatial support intervals for the corrected short-profile stack."""

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
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SENSITIVITY_RUN = "045_gssi51600s_corrected_profile_stack_sensitivity"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def grouped_column_rows(
    sensitivity_rows: list[dict],
    *,
    min_improvement: float,
    min_corrected_abs_correlation: float,
    majority_fraction: float,
) -> list[dict]:
    grouped: dict[int, list[dict]] = {}
    for row in sensitivity_rows:
        idx = int(safe_float(row.get("column_index"), -1))
        if idx < 0:
            continue
        grouped.setdefault(idx, []).append(row)

    out: list[dict] = []
    for idx, rows in sorted(grouped.items()):
        windows = len(rows)
        supported = [
            row for row in rows
            if safe_float(row.get("abs_correlation_improvement")) >= min_improvement
            and safe_float(row.get("corrected_abs_correlation")) >= min_corrected_abs_correlation
        ]
        support_count = len(supported)
        required_majority = int(math.ceil(float(majority_fraction) * windows)) if windows else math.inf
        x_values = [safe_float(row.get("x_m")) for row in rows if math.isfinite(safe_float(row.get("x_m")))]
        improvements = [
            safe_float(row.get("abs_correlation_improvement"))
            for row in rows
            if math.isfinite(safe_float(row.get("abs_correlation_improvement")))
        ]
        corrected = [
            safe_float(row.get("corrected_abs_correlation"))
            for row in rows
            if math.isfinite(safe_float(row.get("corrected_abs_correlation")))
        ]
        out.append({
            "column_index": idx,
            "x_m": float(np.mean(x_values)) if x_values else math.nan,
            "x_mm": 1000.0 * float(np.mean(x_values)) if x_values else math.nan,
            "window_count": windows,
            "supported_window_count": support_count,
            "majority_supported": bool(support_count >= required_majority and windows > 0),
            "all_window_supported": bool(support_count == windows and windows > 0),
            "mean_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
            "min_abs_correlation_improvement": min(improvements) if improvements else math.nan,
            "mean_corrected_abs_correlation": float(np.mean(corrected)) if corrected else math.nan,
            "min_corrected_abs_correlation": min(corrected) if corrected else math.nan,
        })
    return out


def support_intervals(column_rows: list[dict], support_key: str, *, min_columns: int = 3) -> list[dict]:
    intervals: list[dict] = []
    current: list[dict] = []
    previous_idx: int | None = None
    for row in sorted(column_rows, key=lambda item: int(item["column_index"])):
        idx = int(row["column_index"])
        supported = bool(row.get(support_key))
        if not supported:
            if len(current) >= min_columns:
                intervals.append(_interval_row(current, support_key))
            current = []
            previous_idx = None
            continue
        if previous_idx is not None and idx != previous_idx + 1:
            if len(current) >= min_columns:
                intervals.append(_interval_row(current, support_key))
            current = []
        current.append(row)
        previous_idx = idx
    if len(current) >= min_columns:
        intervals.append(_interval_row(current, support_key))
    for rank, row in enumerate(sorted(intervals, key=lambda item: item["length_m"], reverse=True), start=1):
        row["length_rank"] = rank
    return sorted(intervals, key=lambda item: item["start_x_m"])


def _interval_row(rows: list[dict], support_key: str) -> dict:
    x_values = [safe_float(row.get("x_m")) for row in rows]
    improvements = [safe_float(row.get("mean_abs_correlation_improvement")) for row in rows]
    corrected = [safe_float(row.get("mean_corrected_abs_correlation")) for row in rows]
    start = min(x_values)
    stop = max(x_values)
    return {
        "support_key": support_key,
        "start_column_index": int(rows[0]["column_index"]),
        "end_column_index": int(rows[-1]["column_index"]),
        "column_count": len(rows),
        "start_x_m": start,
        "end_x_m": stop,
        "start_x_mm": 1000.0 * start,
        "end_x_mm": 1000.0 * stop,
        "length_m": stop - start,
        "mean_column_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "mean_corrected_abs_correlation": float(np.mean(corrected)) if corrected else math.nan,
    }


def summarize_spatial_support(column_rows: list[dict], interval_rows: list[dict]) -> dict:
    finite_rows = [
        row for row in column_rows
        if math.isfinite(safe_float(row.get("mean_abs_correlation_improvement")))
    ]
    majority_count = sum(1 for row in finite_rows if bool(row.get("majority_supported")))
    all_count = sum(1 for row in finite_rows if bool(row.get("all_window_supported")))
    largest_majority = max(
        [row for row in interval_rows if row["support_key"] == "majority_supported"],
        key=lambda row: safe_float(row.get("length_m")),
        default={},
    )
    majority_fraction = majority_count / len(finite_rows) if finite_rows else math.nan
    all_fraction = all_count / len(finite_rows) if finite_rows else math.nan
    largest_length = safe_float(largest_majority.get("length_m"))
    if math.isfinite(majority_fraction) and majority_fraction >= 0.45 and largest_length >= 0.08:
        label = "corrected_stack_spatial_support_limited_but_usable"
    elif majority_count > 0:
        label = "corrected_stack_spatial_support_sparse"
    else:
        label = "corrected_stack_spatial_support_not_supported"
    return {
        "policy_label": label,
        "finite_column_count": len(finite_rows),
        "majority_supported_column_count": majority_count,
        "majority_supported_column_fraction": majority_fraction,
        "all_window_supported_column_count": all_count,
        "all_window_supported_column_fraction": all_fraction,
        "support_interval_count": len(interval_rows),
        "largest_majority_interval_length_m": largest_length,
        "largest_majority_interval_start_x_m": safe_float(largest_majority.get("start_x_m")),
        "largest_majority_interval_end_x_m": safe_float(largest_majority.get("end_x_m")),
        "policy": (
            "Use the spatial-support mask to limit corrected-stack visual QC to "
            "supported profile regions. Unsupported columns should not be used "
            "for field inversion, radius, cover-depth, or 3D claims."
        ),
    }


def plot_spatial_support(column_rows: list[dict], interval_rows: list[dict], summary: dict, save_path: Path) -> str:
    rows = sorted(column_rows, key=lambda row: safe_float(row.get("x_m")))
    x = np.asarray([safe_float(row.get("x_m")) for row in rows], dtype=np.float64)
    support = np.asarray([safe_float(row.get("supported_window_count"), 0.0) for row in rows], dtype=np.float64)
    mean_gain = np.asarray([safe_float(row.get("mean_abs_correlation_improvement"), 0.0) for row in rows], dtype=np.float64)
    min_corr = np.asarray([safe_float(row.get("min_corrected_abs_correlation"), 0.0) for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(3, 1, figsize=(13.2, 8.6), constrained_layout=True)
    axes[0].bar(x, support, width=0.0027, color="#4c78a8")
    axes[0].axhline(2.0, color="#555555", linestyle="--", linewidth=0.9)
    axes[0].set_ylabel("supported windows")
    axes[0].set_title("Corrected-stack support count by profile position")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].plot(x, mean_gain, color="#2f9d55", linewidth=1.3)
    axes[1].axhline(0.05, color="#555555", linestyle="--", linewidth=0.9)
    axes[1].set_ylabel("mean corr gain")
    axes[1].set_title("Mean corrected-stack gain across windows")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].plot(x, min_corr, color="#f58518", linewidth=1.3)
    axes[2].axhline(0.65, color="#555555", linestyle="--", linewidth=0.9)
    axes[2].set_xlabel("profile distance after alignment [m]")
    axes[2].set_ylabel("min corrected corr")
    axes[2].set_title("Minimum corrected agreement across windows")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    for interval in interval_rows:
        if interval["support_key"] != "majority_supported":
            continue
        for ax in axes:
            ax.axvspan(
                safe_float(interval["start_x_m"]),
                safe_float(interval["end_x_m"]),
                color="#2f9d55",
                alpha=0.12,
                linewidth=0,
            )

    fig.suptitle(
        f"Corrected-stack spatial support: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--sensitivity-run", default=DEFAULT_SENSITIVITY_RUN)
    parser.add_argument("--min-improvement", type=float, default=0.05)
    parser.add_argument("--min-corrected-abs-correlation", type=float, default=0.65)
    parser.add_argument("--majority-fraction", type=float, default=2.0 / 3.0)
    parser.add_argument("--run-name", default="gssi51600s_corrected_stack_spatial_support")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    sensitivity_csv = (
        dataset_root
        / args.sensitivity_run
        / "data"
        / "corrected_profile_stack_sensitivity_columns.csv"
    )
    sensitivity_rows = read_csv_rows(sensitivity_csv)
    column_rows = grouped_column_rows(
        sensitivity_rows,
        min_improvement=args.min_improvement,
        min_corrected_abs_correlation=args.min_corrected_abs_correlation,
        majority_fraction=args.majority_fraction,
    )
    interval_rows = support_intervals(column_rows, "majority_supported") + support_intervals(
        column_rows,
        "all_window_supported",
    )
    summary = summarize_spatial_support(column_rows, interval_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    columns_csv = data_dir / "corrected_stack_spatial_support_columns.csv"
    intervals_csv = data_dir / "corrected_stack_spatial_support_intervals.csv"
    summary_json = data_dir / "corrected_stack_spatial_support_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_spatial_support(column_rows, interval_rows, summary, figures_dir / "corrected_stack_spatial_support.png"))

    write_csv(columns_csv, [json_safe(row) for row in column_rows])
    write_csv(intervals_csv, [json_safe(row) for row in interval_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "input_sensitivity_csv": str(sensitivity_csv),
        "thresholds": {
            "min_improvement": args.min_improvement,
            "min_corrected_abs_correlation": args.min_corrected_abs_correlation,
            "majority_fraction": args.majority_fraction,
        },
        "paths": {
            "columns_csv": str(columns_csv),
            "intervals_csv": str(intervals_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_corrected_stack_spatial_support",
        {
            "summary_json": str(summary_json),
            "columns_csv": str(columns_csv),
            "intervals_csv": str(intervals_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
