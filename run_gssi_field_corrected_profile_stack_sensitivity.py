#!/usr/bin/env python3
"""Window-sensitivity check for the corrected short-profile B-scan stack."""

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
from run_gssi_field_corrected_profile_stack import (  # noqa: E402
    DEFAULT_APPLIED_RUN,
    DEFAULT_STACK_RUN,
    build_profile_windows,
    column_agreement_rows,
    compare_matrices,
    safe_float,
    summarize_corrected_stack,
)
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_WINDOWS = "0.35:1.10,0.45:1.25,0.55:1.45"


def parse_window_configs(text: str) -> list[dict]:
    configs: list[dict] = []
    for item in str(text).split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split(":")
        if len(parts) != 2:
            raise argparse.ArgumentTypeError("window configs must be min:max")
        try:
            start = float(parts[0])
            stop = float(parts[1])
        except ValueError as exc:
            raise argparse.ArgumentTypeError("window configs must be numeric min:max") from exc
        if start < 0.0 or stop <= start:
            raise argparse.ArgumentTypeError("window max must be greater than min")
        configs.append({
            "window_label": f"{start:g}_{stop:g}ns",
            "time_window_min_ns": start,
            "time_window_max_ns": stop,
        })
    if not configs:
        raise argparse.ArgumentTypeError("expected at least one window config")
    return configs


def build_sensitivity_rows(
    profiles: dict,
    window_configs: list[dict],
    *,
    reference_stem: str,
    comparison_stem: str,
    transfer_offset_ns: float,
    orientation: str,
    lag_samples: int,
    lag_mm: float,
) -> tuple[list[dict], list[dict]]:
    window_rows: list[dict] = []
    column_rows: list[dict] = []
    for config in window_configs:
        windows = build_profile_windows(
            profiles,
            reference_stem=reference_stem,
            comparison_stem=comparison_stem,
            time_window_ns=(config["time_window_min_ns"], config["time_window_max_ns"]),
            transfer_offset_ns=transfer_offset_ns,
            orientation=orientation,
            lag_samples=lag_samples,
        )
        raw_compare = compare_matrices(windows["reference_window"], windows["raw_aligned_comparison"])
        corrected_compare = compare_matrices(
            windows["reference_window"],
            windows["corrected_aligned_comparison"],
        )
        rows = column_agreement_rows(
            windows["x_m"],
            windows["reference_window"],
            windows["raw_aligned_comparison"],
            windows["corrected_aligned_comparison"],
        )
        summary = summarize_corrected_stack(
            rows,
            raw_compare,
            corrected_compare,
            transfer_offset_ns=transfer_offset_ns,
            orientation=orientation,
            lag_samples=lag_samples,
            lag_mm=lag_mm,
        )
        window_rows.append({
            **config,
            **summary,
        })
        for row in rows:
            column_rows.append({
                **config,
                "column_index": row["column_index"],
                "x_m": row["x_m"],
                "raw_abs_correlation": row["raw_abs_correlation"],
                "corrected_abs_correlation": row["corrected_abs_correlation"],
                "abs_correlation_improvement": row["abs_correlation_improvement"],
            })
    return window_rows, column_rows


def summarize_sensitivity(window_rows: list[dict]) -> dict:
    robust_rows = [
        row for row in window_rows
        if safe_float(row.get("matrix_abs_correlation_improvement")) > 0.05
        and safe_float(row.get("corrected_matrix_abs_correlation")) >= 0.65
        and safe_float(row.get("improved_column_fraction")) >= 0.55
    ]
    matrix_improvements = [
        safe_float(row.get("matrix_abs_correlation_improvement"))
        for row in window_rows
        if math.isfinite(safe_float(row.get("matrix_abs_correlation_improvement")))
    ]
    corrected_corr = [
        safe_float(row.get("corrected_matrix_abs_correlation"))
        for row in window_rows
        if math.isfinite(safe_float(row.get("corrected_matrix_abs_correlation")))
    ]
    column_fractions = [
        safe_float(row.get("improved_column_fraction"))
        for row in window_rows
        if math.isfinite(safe_float(row.get("improved_column_fraction")))
    ]
    if window_rows and len(robust_rows) == len(window_rows):
        label = "corrected_profile_stack_window_robust"
    elif robust_rows:
        label = "corrected_profile_stack_window_mixed"
    else:
        label = "corrected_profile_stack_window_not_robust"
    return {
        "policy_label": label,
        "window_count": len(window_rows),
        "robust_window_count": len(robust_rows),
        "min_matrix_abs_correlation_improvement": min(matrix_improvements) if matrix_improvements else math.nan,
        "mean_matrix_abs_correlation_improvement": float(np.mean(matrix_improvements)) if matrix_improvements else math.nan,
        "min_corrected_matrix_abs_correlation": min(corrected_corr) if corrected_corr else math.nan,
        "mean_corrected_matrix_abs_correlation": float(np.mean(corrected_corr)) if corrected_corr else math.nan,
        "min_improved_column_fraction": min(column_fractions) if column_fractions else math.nan,
        "mean_improved_column_fraction": float(np.mean(column_fractions)) if column_fractions else math.nan,
        "policy": (
            "Use the corrected profile-stack sensitivity as B-scan-level timing "
            "QC robustness evidence only. It remains separate from field FWI, "
            "3D, radius, cover-depth, or absolute time-zero claims."
        ),
    }


def plot_sensitivity(window_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [str(row["window_label"]).replace("_", "-") for row in window_rows]
    x = np.arange(len(window_rows))
    raw = [safe_float(row.get("raw_matrix_abs_correlation"), 0.0) for row in window_rows]
    corrected = [safe_float(row.get("corrected_matrix_abs_correlation"), 0.0) for row in window_rows]
    improvement = [safe_float(row.get("matrix_abs_correlation_improvement"), 0.0) for row in window_rows]
    improved_fraction = [safe_float(row.get("improved_column_fraction"), 0.0) for row in window_rows]

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.8), constrained_layout=True)
    axes[0].bar(x - 0.18, raw, width=0.36, color="#c7302b", label="raw")
    axes[0].bar(x + 0.18, corrected, width=0.36, color="#2f9d55", label="corrected")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_ylabel("matrix abs correlation")
    axes[0].set_title("B-scan agreement by window")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, improvement, color="#4c78a8", width=0.55)
    axes[1].axhline(0.05, color="#555555", linestyle="--", linewidth=0.9)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("corrected - raw abs corr")
    axes[1].set_title("Matrix improvement")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(x, improved_fraction, color="#f58518", width=0.55)
    axes[2].axhline(0.55, color="#555555", linestyle="--", linewidth=0.9)
    axes[2].set_xticks(x, labels)
    axes[2].set_ylim(0.0, 1.05)
    axes[2].set_ylabel("improved column fraction")
    axes[2].set_title("Column-level support")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Corrected profile-stack sensitivity: {summary['policy_label']}",
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
    parser.add_argument("--reference-stem", default="PROJECT001C__014")
    parser.add_argument("--comparison-stem", default="PROJECT001C__016")
    parser.add_argument("--windows", default=DEFAULT_WINDOWS)
    parser.add_argument("--run-name", default="gssi51600s_corrected_profile_stack_sensitivity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    stack_json = dataset_root / args.stack_run / "data" / "short_profile_stack_policy_summary.json"
    applied_json = dataset_root / args.applied_run / "data" / "short_profile_time_zero_application_summary.json"
    stack_root = json.loads(stack_json.read_text(encoding="utf-8"))
    applied_root = json.loads(applied_json.read_text(encoding="utf-8"))
    stack_summary = stack_root.get("summary", {})
    applied_summary = applied_root.get("summary", {})
    dx_m = safe_float(stack_root.get("dx_m"))
    lag_mm = safe_float(stack_summary.get("best_lag_mm"))
    lag_samples = int(round((lag_mm / 1000.0) / dx_m)) if math.isfinite(lag_mm) and dx_m > 0.0 else 0
    orientation = str(stack_summary.get("best_orientation", "direct"))
    transfer_offset_ns = safe_float(applied_summary.get("applied_transfer_offset_ns"))
    window_configs = parse_window_configs(args.windows)

    profiles = load_profile_map(Path(args.input_dir))
    window_rows, column_rows = build_sensitivity_rows(
        profiles,
        window_configs,
        reference_stem=args.reference_stem,
        comparison_stem=args.comparison_stem,
        transfer_offset_ns=transfer_offset_ns,
        orientation=orientation,
        lag_samples=lag_samples,
        lag_mm=lag_mm,
    )
    summary = summarize_sensitivity(window_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    windows_csv = data_dir / "corrected_profile_stack_sensitivity_windows.csv"
    columns_csv = data_dir / "corrected_profile_stack_sensitivity_columns.csv"
    summary_json = data_dir / "corrected_profile_stack_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_sensitivity(window_rows, summary, figures_dir / "corrected_profile_stack_sensitivity.png"))

    write_csv(windows_csv, [json_safe(row) for row in window_rows])
    write_csv(columns_csv, [json_safe(row) for row in column_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "window_configs": window_configs,
        "input_stack_summary_json": str(stack_json),
        "input_applied_summary_json": str(applied_json),
        "paths": {
            "windows_csv": str(windows_csv),
            "columns_csv": str(columns_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_corrected_profile_stack_sensitivity",
        {
            "summary_json": str(summary_json),
            "windows_csv": str(windows_csv),
            "columns_csv": str(columns_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
