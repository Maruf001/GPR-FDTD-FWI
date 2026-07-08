#!/usr/bin/env python3
"""Stress-test short-profile stack QC under time-zero uncertainty perturbations."""

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
    DEFAULT_STACK_RUN,
    build_profile_windows,
    column_agreement_rows,
    compare_matrices,
    safe_float,
    summarize_corrected_stack,
)
from run_gssi_field_corrected_profile_stack_sensitivity import parse_window_configs  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TIME_ZERO_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_WINDOWS = "0.35:1.10,0.45:1.25,0.55:1.45"


def unique_offset_configs(budget: dict) -> list[dict]:
    nominal = safe_float(budget.get("relative_anchor_offset_ns"))
    conservative_half_width = safe_float(budget.get("conservative_half_width_ns"), 0.0)
    raw_configs = [
        {
            "offset_label": "no_correction",
            "offset_family": "raw_baseline",
            "offset_ns": 0.0,
        },
        {
            "offset_label": "conservative_lower",
            "offset_family": "conservative_envelope",
            "offset_ns": nominal - conservative_half_width,
        },
        {
            "offset_label": "bootstrap_ci_lower",
            "offset_family": "bootstrap_ci",
            "offset_ns": safe_float(budget.get("bootstrap_ci_lower_ns")),
        },
        {
            "offset_label": "bootstrap_median",
            "offset_family": "bootstrap_ci",
            "offset_ns": safe_float(budget.get("bootstrap_observed_median_offset_ns")),
        },
        {
            "offset_label": "nominal_relative_anchor",
            "offset_family": "nominal",
            "offset_ns": nominal,
        },
        {
            "offset_label": "bootstrap_ci_upper",
            "offset_family": "bootstrap_ci",
            "offset_ns": safe_float(budget.get("bootstrap_ci_upper_ns")),
        },
        {
            "offset_label": "conservative_upper",
            "offset_family": "conservative_envelope",
            "offset_ns": nominal + conservative_half_width,
        },
    ]
    seen: set[tuple[str, float]] = set()
    configs = []
    for item in raw_configs:
        offset = safe_float(item.get("offset_ns"))
        if not math.isfinite(offset):
            continue
        key = (str(item["offset_label"]), round(offset, 12))
        if key in seen:
            continue
        seen.add(key)
        configs.append({
            **item,
            "offset_ns": offset,
            "offset_delta_from_nominal_ns": offset - nominal if math.isfinite(nominal) else math.nan,
        })
    return sorted(configs, key=lambda row: safe_float(row.get("offset_ns")))


def is_supported_row(row: dict) -> bool:
    return (
        safe_float(row.get("matrix_abs_correlation_improvement")) > 0.05
        and safe_float(row.get("corrected_matrix_abs_correlation")) >= 0.65
        and safe_float(row.get("improved_column_fraction")) >= 0.55
    )


def build_perturbation_rows(
    profiles: dict,
    window_configs: list[dict],
    offset_configs: list[dict],
    *,
    reference_stem: str,
    comparison_stem: str,
    orientation: str,
    lag_samples: int,
    lag_mm: float,
) -> tuple[list[dict], list[dict]]:
    window_rows: list[dict] = []
    column_rows: list[dict] = []
    for offset_config in offset_configs:
        offset = safe_float(offset_config.get("offset_ns"))
        for window_config in window_configs:
            windows = build_profile_windows(
                profiles,
                reference_stem=reference_stem,
                comparison_stem=comparison_stem,
                time_window_ns=(window_config["time_window_min_ns"], window_config["time_window_max_ns"]),
                transfer_offset_ns=offset,
                orientation=orientation,
                lag_samples=lag_samples,
            )
            raw_compare = compare_matrices(windows["reference_window"], windows["raw_aligned_comparison"])
            corrected_compare = compare_matrices(
                windows["reference_window"],
                windows["corrected_aligned_comparison"],
            )
            columns = column_agreement_rows(
                windows["x_m"],
                windows["reference_window"],
                windows["raw_aligned_comparison"],
                windows["corrected_aligned_comparison"],
            )
            stack_summary = summarize_corrected_stack(
                columns,
                raw_compare,
                corrected_compare,
                transfer_offset_ns=offset,
                orientation=orientation,
                lag_samples=lag_samples,
                lag_mm=lag_mm,
            )
            row = {
                **offset_config,
                **window_config,
                **stack_summary,
            }
            row["offset_window_supported"] = is_supported_row(row)
            window_rows.append(row)
            for column in columns:
                column_rows.append({
                    **offset_config,
                    **window_config,
                    "column_index": column["column_index"],
                    "x_m": column["x_m"],
                    "raw_abs_correlation": column["raw_abs_correlation"],
                    "corrected_abs_correlation": column["corrected_abs_correlation"],
                    "abs_correlation_improvement": column["abs_correlation_improvement"],
                })
    return window_rows, column_rows


def summarize_perturbations(window_rows: list[dict]) -> dict:
    offsets = sorted({str(row["offset_label"]) for row in window_rows})
    window_count = len({str(row["window_label"]) for row in window_rows})
    supported_rows = [row for row in window_rows if bool(row.get("offset_window_supported"))]

    def family_rows(family: str) -> list[dict]:
        return [row for row in window_rows if row.get("offset_family") == family]

    def supported_count(rows: list[dict]) -> int:
        return sum(1 for row in rows if bool(row.get("offset_window_supported")))

    bootstrap_rows = family_rows("bootstrap_ci")
    conservative_rows = family_rows("conservative_envelope")
    nominal_rows = family_rows("nominal")
    raw_rows = family_rows("raw_baseline")
    bootstrap_supported = supported_count(bootstrap_rows)
    conservative_supported = supported_count(conservative_rows)
    nominal_supported = supported_count(nominal_rows)
    raw_supported = supported_count(raw_rows)
    matrix_improvements = [
        safe_float(row.get("matrix_abs_correlation_improvement"))
        for row in window_rows
        if row.get("offset_family") != "raw_baseline"
        and math.isfinite(safe_float(row.get("matrix_abs_correlation_improvement")))
    ]
    corrected_corr = [
        safe_float(row.get("corrected_matrix_abs_correlation"))
        for row in window_rows
        if row.get("offset_family") != "raw_baseline"
        and math.isfinite(safe_float(row.get("corrected_matrix_abs_correlation")))
    ]
    fractions = [
        safe_float(row.get("improved_column_fraction"))
        for row in window_rows
        if row.get("offset_family") != "raw_baseline"
        and math.isfinite(safe_float(row.get("improved_column_fraction")))
    ]
    bootstrap_total = len(bootstrap_rows)
    conservative_total = len(conservative_rows)
    nominal_total = len(nominal_rows)
    if bootstrap_total and bootstrap_supported == bootstrap_total and nominal_supported == nominal_total:
        policy_label = "field_time_zero_ci_perturbation_stack_robust"
    elif nominal_supported == nominal_total and bootstrap_supported > 0:
        policy_label = "field_time_zero_perturbation_stack_nominal_supported_ci_mixed"
    elif nominal_supported > 0:
        policy_label = "field_time_zero_perturbation_stack_nominal_limited"
    else:
        policy_label = "field_time_zero_perturbation_stack_not_supported"
    if conservative_total and conservative_supported < conservative_total and policy_label.endswith("_robust"):
        policy_label = "field_time_zero_ci_perturbation_stack_robust_conservative_mixed"
    return {
        "policy_label": policy_label,
        "offset_count": len(offsets),
        "window_count": window_count,
        "row_count": len(window_rows),
        "supported_row_count": len(supported_rows),
        "raw_baseline_supported_count": raw_supported,
        "nominal_supported_count": nominal_supported,
        "nominal_row_count": nominal_total,
        "bootstrap_ci_supported_count": bootstrap_supported,
        "bootstrap_ci_row_count": bootstrap_total,
        "conservative_supported_count": conservative_supported,
        "conservative_row_count": conservative_total,
        "min_nonraw_matrix_improvement": min(matrix_improvements) if matrix_improvements else math.nan,
        "mean_nonraw_matrix_improvement": float(np.mean(matrix_improvements)) if matrix_improvements else math.nan,
        "min_nonraw_corrected_abs_correlation": min(corrected_corr) if corrected_corr else math.nan,
        "mean_nonraw_corrected_abs_correlation": float(np.mean(corrected_corr)) if corrected_corr else math.nan,
        "min_nonraw_improved_column_fraction": min(fractions) if fractions else math.nan,
        "mean_nonraw_improved_column_fraction": float(np.mean(fractions)) if fractions else math.nan,
        "field_fwi_ready": False,
        "field_gpu_fwi_priority": "none",
        "ready_for_manuscript_uncertainty_sensitivity": (
            bootstrap_total > 0
            and nominal_total > 0
            and bootstrap_supported == bootstrap_total
            and nominal_supported == nominal_total
        ),
        "decision": (
            "Use this as a perturbation sensitivity check for the short 014/016 "
            "relative time-zero budget only. Bootstrap-CI and conservative-envelope "
            "offsets stress the measured B-scan stack QC; the result remains field "
            "QC, not absolute time-zero calibration, field FWI, 3D inversion, "
            "radius, or cover-depth evidence."
        ),
    }


def plot_perturbations(window_rows: list[dict], summary: dict, save_path: Path) -> str:
    rows = sorted(
        window_rows,
        key=lambda row: (str(row.get("window_label")), safe_float(row.get("offset_ns"))),
    )
    window_labels = sorted({str(row["window_label"]) for row in rows})
    fig, axes = plt.subplots(1, 3, figsize=(16.2, 5.0), constrained_layout=True)
    palette = ["#4c78a8", "#f58518", "#2f9d55", "#b279a2", "#6b6b6b"]
    for idx, label in enumerate(window_labels):
        subset = [row for row in rows if row["window_label"] == label]
        x = [safe_float(row.get("offset_ns")) for row in subset]
        color = palette[idx % len(palette)]
        axes[0].plot(
            x,
            [safe_float(row.get("corrected_matrix_abs_correlation")) for row in subset],
            marker="o",
            color=color,
            label=label.replace("_", "-"),
        )
        axes[1].plot(
            x,
            [safe_float(row.get("matrix_abs_correlation_improvement")) for row in subset],
            marker="o",
            color=color,
        )
        axes[2].plot(
            x,
            [safe_float(row.get("improved_column_fraction")) for row in subset],
            marker="o",
            color=color,
        )
    axes[0].axhline(0.65, color="#555555", linestyle="--", linewidth=0.9)
    axes[0].set_ylabel("corrected matrix abs corr")
    axes[0].set_title("B-scan agreement")
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].axhline(0.05, color="#555555", linestyle="--", linewidth=0.9)
    axes[1].set_ylabel("corrected - raw abs corr")
    axes[1].set_title("Matrix improvement")
    axes[2].axhline(0.55, color="#555555", linestyle="--", linewidth=0.9)
    axes[2].set_ylabel("improved column fraction")
    axes[2].set_title("Column support")
    for ax in axes:
        ax.set_xlabel("applied relative offset [ns]")
        ax.grid(axis="both", color="#dddddd", linewidth=0.6)
    fig.suptitle(
        f"Short-profile time-zero perturbation sensitivity: {summary['policy_label']}",
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
    parser.add_argument("--time-zero-budget-run", default=DEFAULT_TIME_ZERO_BUDGET_RUN)
    parser.add_argument("--reference-stem", default="PROJECT001C__014")
    parser.add_argument("--comparison-stem", default="PROJECT001C__016")
    parser.add_argument("--windows", default=DEFAULT_WINDOWS)
    parser.add_argument("--run-name", default="gssi51600s_field_time_zero_perturbation_sensitivity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    stack_json = dataset_root / args.stack_run / "data" / "short_profile_stack_policy_summary.json"
    budget_json = (
        dataset_root
        / args.time_zero_budget_run
        / "data"
        / "field_time_zero_uncertainty_budget_summary.json"
    )
    stack_root = json.loads(stack_json.read_text(encoding="utf-8"))
    budget = json.loads(budget_json.read_text(encoding="utf-8"))
    stack_summary = stack_root.get("summary", {})
    dx_m = safe_float(stack_root.get("dx_m"))
    lag_mm = safe_float(stack_summary.get("best_lag_mm"))
    lag_samples = int(round((lag_mm / 1000.0) / dx_m)) if math.isfinite(lag_mm) and dx_m > 0.0 else 0
    orientation = str(stack_summary.get("best_orientation", "direct"))
    window_configs = parse_window_configs(args.windows)
    offset_configs = unique_offset_configs(budget)

    profiles = load_profile_map(Path(args.input_dir))
    window_rows, column_rows = build_perturbation_rows(
        profiles,
        window_configs,
        offset_configs,
        reference_stem=args.reference_stem,
        comparison_stem=args.comparison_stem,
        orientation=orientation,
        lag_samples=lag_samples,
        lag_mm=lag_mm,
    )
    summary = summarize_perturbations(window_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    windows_csv = data_dir / "field_time_zero_perturbation_windows.csv"
    columns_csv = data_dir / "field_time_zero_perturbation_columns.csv"
    summary_json = data_dir / "field_time_zero_perturbation_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(
        plot_perturbations(
            window_rows,
            summary,
            figures_dir / "field_time_zero_perturbation_sensitivity.png",
        )
    )

    write_csv(windows_csv, [json_safe(row) for row in window_rows])
    write_csv(columns_csv, [json_safe(row) for row in column_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "reference_stem": args.reference_stem,
        "comparison_stem": args.comparison_stem,
        "input_stack_summary_json": str(stack_json),
        "input_time_zero_budget_summary_json": str(budget_json),
        "window_configs": window_configs,
        "offset_configs": offset_configs,
        "paths": {
            "windows_csv": str(windows_csv),
            "columns_csv": str(columns_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
        "readgssi_version": readgssi_version(),
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_time_zero_perturbation_sensitivity",
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
