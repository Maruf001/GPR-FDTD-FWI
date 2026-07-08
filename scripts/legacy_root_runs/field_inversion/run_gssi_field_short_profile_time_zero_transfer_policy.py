#!/usr/bin/env python3
"""Relative time-zero transfer policy for the short local GSSI profile pair."""

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
from visualization.plot_style import save_validated_figure  # noqa: E402


def _finite(values: list[float]) -> list[float]:
    return [float(value) for value in values if math.isfinite(float(value))]


def robust_sigma(values: list[float]) -> float:
    finite = _finite(values)
    if not finite:
        return math.nan
    median = float(np.median(finite))
    mad = float(np.median([abs(value - median) for value in finite]))
    return 1.4826 * mad


def summarize_time_zero_transfer(
    event_pairs: list[dict],
    stack_summary: dict,
    *,
    max_time_range_ns: float,
    max_x_residual_mm: float,
    min_correlation: float,
) -> dict:
    deltas = _finite([
        safe_float(row.get("comparison_minus_reference_phase_time_ns"))
        for row in event_pairs
    ])
    residuals = _finite([abs(safe_float(row.get("aligned_x_residual_mm"))) for row in event_pairs])
    radius_match_count = sum(1 for row in event_pairs if str(row.get("radius_match")).lower() == "true")
    event_count = len(event_pairs)
    stable_stack_anchor_count = int(stack_summary.get("stable_stack_anchor_count", 0))
    correlation = safe_float(stack_summary.get("best_normalized_correlation"))
    delta_range = max(deltas) - min(deltas) if deltas else math.nan
    median_delta = float(np.median(deltas)) if deltas else math.nan
    mean_delta = float(np.mean(deltas)) if deltas else math.nan
    max_residual = max(residuals) if residuals else math.nan
    all_positive = bool(deltas and all(value > 0.0 for value in deltas))
    timing_consistent = (
        event_count >= 3
        and math.isfinite(delta_range)
        and delta_range <= max_time_range_ns
        and math.isfinite(max_residual)
        and max_residual <= max_x_residual_mm
        and math.isfinite(correlation)
        and correlation >= min_correlation
        and all_positive
    )
    if timing_consistent and stable_stack_anchor_count >= 2:
        policy_label = "relative_time_zero_transfer_limited_qc"
    elif event_count >= 2 and math.isfinite(correlation) and correlation >= min_correlation:
        policy_label = "relative_time_zero_transfer_pattern_only"
    else:
        policy_label = "relative_time_zero_transfer_not_stable"
    return {
        "event_pair_count": event_count,
        "stable_stack_anchor_count": stable_stack_anchor_count,
        "best_normalized_correlation": correlation,
        "median_comparison_minus_reference_phase_time_ns": median_delta,
        "mean_comparison_minus_reference_phase_time_ns": mean_delta,
        "min_comparison_minus_reference_phase_time_ns": min(deltas) if deltas else math.nan,
        "max_comparison_minus_reference_phase_time_ns": max(deltas) if deltas else math.nan,
        "range_comparison_minus_reference_phase_time_ns": delta_range,
        "robust_sigma_comparison_minus_reference_phase_time_ns": robust_sigma(deltas),
        "mean_abs_aligned_x_residual_mm": float(np.mean(residuals)) if residuals else math.nan,
        "max_abs_aligned_x_residual_mm": max_residual,
        "radius_match_count": radius_match_count,
        "radius_match_fraction": radius_match_count / event_count if event_count else math.nan,
        "all_phase_deltas_positive": all_positive,
        "timing_consistent": timing_consistent,
        "policy_label": policy_label,
        "policy": (
            "Use the 014/016 reversed short-profile pair as relative timing-transfer QC only. "
            "The offset is not a calibrated absolute time zero and does not support field "
            "radius, cover-depth, geometry, 3D, or FWI claims."
        ),
    }


def pair_rows_with_summary(event_pairs: list[dict], median_delta_ns: float) -> list[dict]:
    rows = []
    for row in event_pairs:
        delta = safe_float(row.get("comparison_minus_reference_phase_time_ns"))
        rows.append({
            **row,
            "offset_from_median_ns": delta - median_delta_ns if math.isfinite(delta) else math.nan,
            "abs_offset_from_median_ns": abs(delta - median_delta_ns) if math.isfinite(delta) else math.nan,
        })
    return rows


def plot_time_zero_transfer(rows: list[dict], summary: dict, save_path: Path) -> str:
    pair_ids = [str(row.get("pair_index", idx + 1)) for idx, row in enumerate(rows)]
    deltas = [safe_float(row.get("comparison_minus_reference_phase_time_ns")) for row in rows]
    residuals = [safe_float(row.get("aligned_x_residual_mm")) for row in rows]
    median_delta = safe_float(summary.get("median_comparison_minus_reference_phase_time_ns"))
    robust = safe_float(summary.get("robust_sigma_comparison_minus_reference_phase_time_ns"))

    fig, axes = plt.subplots(2, 1, figsize=(10.5, 7.2), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, deltas, color="#4c78a8", width=0.55)
    axes[0].axhline(median_delta, color="#222222", linestyle="--", linewidth=1.1, label="median offset")
    if math.isfinite(robust):
        axes[0].axhspan(median_delta - robust, median_delta + robust, color="#4c78a8", alpha=0.14, label="robust sigma")
    axes[0].set_xticks(x, pair_ids)
    axes[0].set_ylabel("016 - 014 phase time [ns]")
    axes[0].set_title("Relative phase-time offset after reversed short-profile alignment")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x, residuals, color="#f58518", width=0.55)
    axes[1].axhline(0.0, color="#222222", linewidth=0.8)
    axes[1].set_xticks(x, pair_ids)
    axes[1].set_xlabel("reversed event pair")
    axes[1].set_ylabel("aligned x residual [mm]")
    axes[1].set_title("Position residuals for the same event pairs")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        "Short-profile relative timing transfer: "
        f"{summary['policy_label']}, median={median_delta:.3f} ns",
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
    parser.add_argument("--max-time-range-ns", type=float, default=0.10)
    parser.add_argument("--max-x-residual-mm", type=float, default=25.0)
    parser.add_argument("--min-correlation", type=float, default=0.90)
    parser.add_argument("--run-name", default="gssi51600s_short_profile_time_zero_transfer_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    stack_dir = (
        Path(args.stack_policy_dir)
        if args.stack_policy_dir
        else dataset_root / "021_gssi51600s_short_profile_stack_policy"
    )
    event_pairs_csv = stack_dir / "data" / "short_profile_reversed_event_pairs.csv"
    stack_summary_json = stack_dir / "data" / "short_profile_stack_policy_summary.json"
    event_pairs = read_csv_rows(event_pairs_csv)
    stack_summary_root = json.loads(stack_summary_json.read_text(encoding="utf-8"))
    stack_summary = stack_summary_root.get("summary", {})

    summary = summarize_time_zero_transfer(
        event_pairs,
        stack_summary,
        max_time_range_ns=args.max_time_range_ns,
        max_x_residual_mm=args.max_x_residual_mm,
        min_correlation=args.min_correlation,
    )
    rows = pair_rows_with_summary(
        event_pairs,
        safe_float(summary.get("median_comparison_minus_reference_phase_time_ns")),
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    pair_csv = data_dir / "short_profile_time_zero_event_offsets.csv"
    summary_json = data_dir / "short_profile_time_zero_transfer_summary.json"
    figure_path = Path(plot_time_zero_transfer(rows, summary, figures_dir / "short_profile_time_zero_transfer.png"))
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(pair_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "stack_policy_dir": str(stack_dir),
        "input_event_pairs_csv": str(event_pairs_csv),
        "input_stack_summary_json": str(stack_summary_json),
        "thresholds": {
            "max_time_range_ns": args.max_time_range_ns,
            "max_x_residual_mm": args.max_x_residual_mm,
            "min_correlation": args.min_correlation,
        },
        "summary": summary,
        "paths": {
            "event_offsets_csv": str(pair_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_profile_time_zero_transfer_policy",
        {
            "summary_json": str(summary_json),
            "event_offsets_csv": str(pair_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
