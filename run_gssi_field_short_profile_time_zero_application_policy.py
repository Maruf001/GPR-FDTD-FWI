#!/usr/bin/env python3
"""Apply and stress-test the short-profile relative time-zero transfer."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import read_csv_rows, safe_float  # noqa: E402
from run_gssi_field_short_profile_time_zero_transfer_policy import robust_sigma  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def _finite(values: list[float]) -> list[float]:
    return [float(value) for value in values if math.isfinite(float(value))]


def median_or_nan(values: list[float]) -> float:
    finite = _finite(values)
    return float(np.median(finite)) if finite else math.nan


def mean_abs_or_nan(values: list[float]) -> float:
    finite = _finite(values)
    return float(np.mean(np.abs(finite))) if finite else math.nan


def max_abs_or_nan(values: list[float]) -> float:
    finite = _finite(values)
    return float(np.max(np.abs(finite))) if finite else math.nan


def applied_transfer_rows(event_pairs: list[dict], transfer_offset_ns: float) -> list[dict]:
    rows = []
    for row in event_pairs:
        raw_delta = safe_float(row.get("comparison_minus_reference_phase_time_ns"))
        corrected_delta = raw_delta - transfer_offset_ns if math.isfinite(raw_delta) else math.nan
        rows.append({
            **row,
            "applied_transfer_offset_ns": transfer_offset_ns,
            "corrected_comparison_minus_reference_phase_time_ns": corrected_delta,
            "abs_raw_phase_residual_ns": abs(raw_delta) if math.isfinite(raw_delta) else math.nan,
            "abs_corrected_phase_residual_ns": abs(corrected_delta) if math.isfinite(corrected_delta) else math.nan,
        })
    return rows


def leave_one_out_transfer_rows(event_pairs: list[dict]) -> list[dict]:
    deltas = [safe_float(row.get("comparison_minus_reference_phase_time_ns")) for row in event_pairs]
    rows = []
    for idx, row in enumerate(event_pairs):
        holdout_delta = deltas[idx]
        training_deltas = [value for jdx, value in enumerate(deltas) if jdx != idx]
        fitted_offset = median_or_nan(training_deltas)
        holdout_residual = holdout_delta - fitted_offset if math.isfinite(holdout_delta) else math.nan
        rows.append({
            "holdout_pair_index": row.get("pair_index", idx + 1),
            "training_pair_count": len(_finite(training_deltas)),
            "loo_fitted_transfer_offset_ns": fitted_offset,
            "holdout_raw_phase_delta_ns": holdout_delta,
            "holdout_corrected_phase_residual_ns": holdout_residual,
            "abs_holdout_corrected_phase_residual_ns": (
                abs(holdout_residual) if math.isfinite(holdout_residual) else math.nan
            ),
        })
    return rows


def summarize_applied_transfer(
    event_pairs: list[dict],
    transfer_summary: dict,
    *,
    max_corrected_abs_residual_ns: float,
    max_loo_abs_residual_ns: float,
    min_residual_reduction_factor: float,
) -> dict:
    transfer_offset = safe_float(transfer_summary.get("median_comparison_minus_reference_phase_time_ns"))
    applied_rows = applied_transfer_rows(event_pairs, transfer_offset)
    loo_rows = leave_one_out_transfer_rows(event_pairs)

    raw_residuals = [safe_float(row.get("comparison_minus_reference_phase_time_ns")) for row in event_pairs]
    corrected_residuals = [
        safe_float(row.get("corrected_comparison_minus_reference_phase_time_ns"))
        for row in applied_rows
    ]
    loo_residuals = [
        safe_float(row.get("holdout_corrected_phase_residual_ns"))
        for row in loo_rows
    ]

    raw_mean_abs = mean_abs_or_nan(raw_residuals)
    corrected_mean_abs = mean_abs_or_nan(corrected_residuals)
    reduction_factor = (
        raw_mean_abs / corrected_mean_abs
        if math.isfinite(raw_mean_abs) and math.isfinite(corrected_mean_abs) and corrected_mean_abs > 0
        else math.inf if math.isfinite(raw_mean_abs) and corrected_mean_abs == 0
        else math.nan
    )
    corrected_max_abs = max_abs_or_nan(corrected_residuals)
    loo_max_abs = max_abs_or_nan(loo_residuals)
    event_count = len(event_pairs)
    prior_policy = str(transfer_summary.get("policy_label", ""))
    application_consistent = (
        prior_policy == "relative_time_zero_transfer_limited_qc"
        and event_count >= 3
        and math.isfinite(corrected_max_abs)
        and corrected_max_abs <= max_corrected_abs_residual_ns
        and math.isfinite(loo_max_abs)
        and loo_max_abs <= max_loo_abs_residual_ns
        and math.isfinite(reduction_factor)
        and reduction_factor >= min_residual_reduction_factor
    )
    if application_consistent:
        policy_label = "applied_relative_time_zero_transfer_qc"
    elif math.isfinite(reduction_factor) and reduction_factor > 1.0:
        policy_label = "applied_relative_time_zero_transfer_limited"
    else:
        policy_label = "applied_relative_time_zero_transfer_unstable"

    return {
        "event_pair_count": event_count,
        "prior_transfer_policy_label": prior_policy,
        "applied_transfer_offset_ns": transfer_offset,
        "raw_mean_abs_phase_residual_ns": raw_mean_abs,
        "raw_max_abs_phase_residual_ns": max_abs_or_nan(raw_residuals),
        "raw_robust_sigma_phase_residual_ns": robust_sigma(raw_residuals),
        "corrected_mean_abs_phase_residual_ns": corrected_mean_abs,
        "corrected_max_abs_phase_residual_ns": corrected_max_abs,
        "corrected_robust_sigma_phase_residual_ns": robust_sigma(corrected_residuals),
        "mean_abs_residual_reduction_factor": reduction_factor,
        "leave_one_out_max_abs_residual_ns": loo_max_abs,
        "leave_one_out_mean_abs_residual_ns": mean_abs_or_nan(loo_residuals),
        "application_consistent": application_consistent,
        "policy_label": policy_label,
        "policy": (
            "Apply the 014/016 relative transfer only as repeatability/time-zero QC. "
            "This is not an absolute time-zero calibration and does not support "
            "field radius, cover-depth, geometry, 3D, or FWI claims."
        ),
    }


def plot_applied_transfer(
    applied_rows: list[dict],
    loo_rows: list[dict],
    summary: dict,
    save_path: Path,
) -> str:
    pair_ids = [str(row.get("pair_index", idx + 1)) for idx, row in enumerate(applied_rows)]
    raw = [safe_float(row.get("comparison_minus_reference_phase_time_ns")) for row in applied_rows]
    corrected = [safe_float(row.get("corrected_comparison_minus_reference_phase_time_ns")) for row in applied_rows]
    loo = [safe_float(row.get("holdout_corrected_phase_residual_ns")) for row in loo_rows]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    x = np.arange(len(applied_rows))
    width = 0.36
    axes[0].bar(x - width / 2, raw, width=width, color="#4c78a8", label="raw 016 - 014")
    axes[0].bar(x + width / 2, corrected, width=width, color="#2f9d55", label="after transfer")
    axes[0].axhline(0.0, color="#222222", linewidth=0.8)
    axes[0].set_xticks(x, pair_ids)
    axes[0].set_xlabel("reversed event pair")
    axes[0].set_ylabel("phase residual [ns]")
    axes[0].set_title("Applied transfer removes the common phase offset")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x, loo, color="#f58518", width=0.55)
    axes[1].axhline(0.0, color="#222222", linewidth=0.8)
    axes[1].set_xticks(x, pair_ids)
    axes[1].set_xlabel("holdout event pair")
    axes[1].set_ylabel("holdout residual [ns]")
    axes[1].set_title("Leave-one-event-out transfer stress test")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        "Short-profile applied relative time-zero transfer: "
        f"{summary['policy_label']}, reduction={summary['mean_abs_residual_reduction_factor']:.2f}x",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--stack-policy-dir", default=None)
    parser.add_argument("--transfer-policy-dir", default=None)
    parser.add_argument("--max-corrected-abs-residual-ns", type=float, default=0.06)
    parser.add_argument("--max-loo-abs-residual-ns", type=float, default=0.07)
    parser.add_argument("--min-residual-reduction-factor", type=float, default=3.0)
    parser.add_argument("--run-name", default="gssi51600s_short_profile_time_zero_application_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    stack_dir = (
        Path(args.stack_policy_dir)
        if args.stack_policy_dir
        else dataset_root / "021_gssi51600s_short_profile_stack_policy"
    )
    transfer_dir = (
        Path(args.transfer_policy_dir)
        if args.transfer_policy_dir
        else dataset_root / "024_gssi51600s_short_profile_time_zero_transfer_policy"
    )
    event_pairs_csv = stack_dir / "data" / "short_profile_reversed_event_pairs.csv"
    transfer_summary_json = transfer_dir / "data" / "short_profile_time_zero_transfer_summary.json"
    event_pairs = read_csv_rows(event_pairs_csv)
    transfer_root = json.loads(transfer_summary_json.read_text(encoding="utf-8"))
    transfer_summary = transfer_root.get("summary", {})

    summary = summarize_applied_transfer(
        event_pairs,
        transfer_summary,
        max_corrected_abs_residual_ns=args.max_corrected_abs_residual_ns,
        max_loo_abs_residual_ns=args.max_loo_abs_residual_ns,
        min_residual_reduction_factor=args.min_residual_reduction_factor,
    )
    applied_rows = applied_transfer_rows(event_pairs, safe_float(summary.get("applied_transfer_offset_ns")))
    loo_rows = leave_one_out_transfer_rows(event_pairs)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    applied_csv = data_dir / "short_profile_time_zero_applied_event_residuals.csv"
    loo_csv = data_dir / "short_profile_time_zero_leave_one_out.csv"
    summary_json = data_dir / "short_profile_time_zero_application_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(
        plot_applied_transfer(
            applied_rows,
            loo_rows,
            summary,
            figures_dir / "short_profile_time_zero_application.png",
        )
    )

    write_csv(applied_csv, [json_safe(row) for row in applied_rows])
    write_csv(loo_csv, [json_safe(row) for row in loo_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "stack_policy_dir": str(stack_dir),
        "transfer_policy_dir": str(transfer_dir),
        "input_event_pairs_csv": str(event_pairs_csv),
        "input_transfer_summary_json": str(transfer_summary_json),
        "thresholds": {
            "max_corrected_abs_residual_ns": args.max_corrected_abs_residual_ns,
            "max_loo_abs_residual_ns": args.max_loo_abs_residual_ns,
            "min_residual_reduction_factor": args.min_residual_reduction_factor,
        },
        "summary": summary,
        "paths": {
            "applied_event_residuals_csv": str(applied_csv),
            "leave_one_out_csv": str(loo_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_profile_time_zero_application_policy",
        {
            "summary_json": str(summary_json),
            "applied_event_residuals_csv": str(applied_csv),
            "leave_one_out_csv": str(loo_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
