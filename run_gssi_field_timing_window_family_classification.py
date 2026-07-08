#!/usr/bin/env python3
"""Classify field timing support by early, short-content, and long-pattern windows."""

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
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_EARLY_TIME_ANCHOR_RUN = "090_gssi51600s_field_early_time_anchor_audit"
DEFAULT_TIME_ZERO_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_TIME_ZERO_PERTURBATION_RUN = "078_gssi51600s_field_time_zero_perturbation_sensitivity"
DEFAULT_LONG_SHIFT_SENSITIVITY_RUN = "055_gssi51600s_long_profile_shift_scan_sensitivity"
DEFAULT_TIMING_CONFLICT_RUN = "097_gssi51600s_field_timing_anchor_conflict_synthesis"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def boolish(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_strict_early_window(row: dict) -> bool:
    return safe_float(row.get("window_max_ns")) <= 0.70


def is_near_zero_lag(row: dict) -> bool:
    shift = abs(safe_float(row.get("comparison_minus_reference_shift_ns")))
    dt_ns = safe_float(row.get("dt_ns"))
    return math.isfinite(shift) and math.isfinite(dt_ns) and shift <= dt_ns + 1.0e-12


def classify_early_rows(rows: list[dict]) -> dict:
    strict = [row for row in rows if is_strict_early_window(row)]
    all_rows = list(rows)
    zero_count = sum(int(safe_float(row.get("lag_samples"), 999.0)) == 0 for row in all_rows)
    near_zero_count = sum(is_near_zero_lag(row) for row in all_rows)
    strict_near_zero_count = sum(is_near_zero_lag(row) for row in strict)
    strict_shift_abs = [
        abs(safe_float(row.get("comparison_minus_reference_shift_ns")))
        for row in strict
        if math.isfinite(safe_float(row.get("comparison_minus_reference_shift_ns")))
    ]
    all_shift_abs = [
        abs(safe_float(row.get("comparison_minus_reference_shift_ns")))
        for row in all_rows
        if math.isfinite(safe_float(row.get("comparison_minus_reference_shift_ns")))
    ]
    return {
        "row_count": len(all_rows),
        "strict_early_row_count": len(strict),
        "zero_lag_row_count": zero_count,
        "near_zero_lag_row_count": near_zero_count,
        "strict_early_near_zero_lag_row_count": strict_near_zero_count,
        "max_strict_early_abs_shift_ns": max(strict_shift_abs) if strict_shift_abs else math.nan,
        "max_all_early_abs_shift_ns": max(all_shift_abs) if all_shift_abs else math.nan,
    }


def classify_short_content_rows(rows: list[dict]) -> dict:
    raw = [row for row in rows if row.get("offset_family") == "raw_baseline"]
    nonraw = [row for row in rows if row.get("offset_family") != "raw_baseline"]
    nominal = [row for row in rows if row.get("offset_family") == "nominal"]
    supported = [row for row in nonraw if boolish(row.get("offset_window_supported"))]
    raw_supported = [row for row in raw if boolish(row.get("offset_window_supported"))]
    min_improvement = min(
        [
            safe_float(row.get("matrix_abs_correlation_improvement"))
            for row in nonraw
            if math.isfinite(safe_float(row.get("matrix_abs_correlation_improvement")))
        ],
        default=math.nan,
    )
    min_corrected = min(
        [
            safe_float(row.get("corrected_matrix_abs_correlation"))
            for row in nonraw
            if math.isfinite(safe_float(row.get("corrected_matrix_abs_correlation")))
        ],
        default=math.nan,
    )
    return {
        "row_count": len(rows),
        "raw_row_count": len(raw),
        "raw_supported_count": len(raw_supported),
        "nonraw_row_count": len(nonraw),
        "nonraw_supported_count": len(supported),
        "nominal_supported_count": sum(boolish(row.get("offset_window_supported")) for row in nominal),
        "nominal_row_count": len(nominal),
        "min_nonraw_matrix_improvement": min_improvement,
        "min_nonraw_corrected_abs_correlation": min_corrected,
    }


def classify_long_pattern_rows(rows: list[dict]) -> dict:
    reject_rows = [
        row for row in rows
        if "rejects_short_transfer" in str(row.get("policy_label") or row.get("policy", ""))
    ]
    best_offsets = [
        safe_float(row.get("best_matrix_offset_ns"))
        for row in rows
        if math.isfinite(safe_float(row.get("best_matrix_offset_ns")))
    ]
    distances = [
        safe_float(row.get("best_matrix_offset_distance_from_short_pair_ns"))
        for row in rows
        if math.isfinite(safe_float(row.get("best_matrix_offset_distance_from_short_pair_ns")))
    ]
    gains = [
        safe_float(row.get("best_matrix_gain_vs_zero"))
        for row in rows
        if math.isfinite(safe_float(row.get("best_matrix_gain_vs_zero")))
    ]
    short_transfer_gains = [
        safe_float(row.get("short_pair_offset_gain_vs_zero"))
        for row in rows
        if math.isfinite(safe_float(row.get("short_pair_offset_gain_vs_zero")))
    ]
    return {
        "row_count": len(rows),
        "reject_short_transfer_row_count": len(reject_rows),
        "best_offset_median_ns": float(np.median(best_offsets)) if best_offsets else math.nan,
        "best_offset_distance_from_short_pair_median_ns": (
            float(np.median(distances)) if distances else math.nan
        ),
        "min_best_gain_vs_zero": min(gains, default=math.nan),
        "max_short_transfer_gain_vs_zero": max(short_transfer_gains, default=math.nan),
    }


def family_rows(early: dict, short_content: dict, long_pattern: dict, timing: dict) -> list[dict]:
    short_offset = safe_float(timing.get("short_content_offset_ns"))
    early_offset = safe_float(timing.get("early_common_mode_shift_ns"))
    long_offset = safe_float(timing.get("long_pattern_offset_ns"))
    half_width = safe_float(timing.get("short_content_half_width_ns"))

    def delta_half_widths(offset: float) -> float:
        if not (math.isfinite(offset) and math.isfinite(short_offset) and math.isfinite(half_width) and half_width > 0):
            return math.nan
        return abs(offset - short_offset) / half_width

    return [
        {
            "timing_family": "early_common_mode",
            "pair_scope": "short_and_long_profiles",
            "representative_offset_ns": early_offset,
            "window_support_summary": (
                f"strict_near_zero={early['strict_early_near_zero_lag_row_count']}/"
                f"{early['strict_early_row_count']}; all_near_zero={early['near_zero_lag_row_count']}/"
                f"{early['row_count']}"
            ),
            "delta_to_short_content_half_widths": delta_half_widths(early_offset),
            "classification": "common_mode_negative_control_not_absolute_time_zero",
            "allowed_use": "early/direct-wave repeatability QC",
            "not_allowed": "absolute time-zero calibration or replacement for content-backed timing",
        },
        {
            "timing_family": "short_content_relative",
            "pair_scope": "short_014_016",
            "representative_offset_ns": short_offset,
            "window_support_summary": (
                f"nonraw_supported={short_content['nonraw_supported_count']}/"
                f"{short_content['nonraw_row_count']}; raw_supported={short_content['raw_supported_count']}/"
                f"{short_content['raw_row_count']}"
            ),
            "delta_to_short_content_half_widths": 0.0,
            "classification": "relative_content_timing_supported_not_absolute",
            "allowed_use": "short-pair relative time-zero uncertainty and stack QC",
            "not_allowed": "absolute time-zero, field FWI, 3D, radius, or cover-depth recovery",
        },
        {
            "timing_family": "long_pattern_only",
            "pair_scope": "long_015_013",
            "representative_offset_ns": long_offset,
            "window_support_summary": (
                f"reject_short_transfer={long_pattern['reject_short_transfer_row_count']}/"
                f"{long_pattern['row_count']}; best_offset_median={long_pattern['best_offset_median_ns']:.6g} ns"
            ),
            "delta_to_short_content_half_widths": delta_half_widths(long_offset),
            "classification": "stable_pattern_shift_not_phase_time_zero",
            "allowed_use": "long-profile shallow pattern-only visual QC",
            "not_allowed": "phase anchor, absolute time-zero, field FWI, or 3D inversion",
        },
    ]


def summarize(early: dict, short_content: dict, long_pattern: dict, timing: dict) -> dict:
    early_strict_ready = early["strict_early_near_zero_lag_row_count"] == early["strict_early_row_count"]
    short_ready = (
        short_content["nonraw_supported_count"] == short_content["nonraw_row_count"]
        and short_content["raw_supported_count"] == 0
    )
    long_ready = (
        long_pattern["reject_short_transfer_row_count"] == long_pattern["row_count"]
        and safe_float(long_pattern["max_short_transfer_gain_vs_zero"], 1.0) < 0.0
    )
    ready = early_strict_ready and short_ready and long_ready
    return {
        "policy_label": (
            "field_timing_window_family_classification_ready_not_absolute"
            if ready
            else "field_timing_window_family_classification_review_required"
        ),
        "early_row_count": early["row_count"],
        "early_strict_row_count": early["strict_early_row_count"],
        "early_strict_near_zero_lag_row_count": early["strict_early_near_zero_lag_row_count"],
        "early_near_zero_lag_row_count": early["near_zero_lag_row_count"],
        "early_max_strict_abs_shift_ns": early["max_strict_early_abs_shift_ns"],
        "short_nonraw_supported_count": short_content["nonraw_supported_count"],
        "short_nonraw_row_count": short_content["nonraw_row_count"],
        "short_raw_supported_count": short_content["raw_supported_count"],
        "short_raw_row_count": short_content["raw_row_count"],
        "short_min_nonraw_matrix_improvement": short_content["min_nonraw_matrix_improvement"],
        "long_reject_short_transfer_row_count": long_pattern["reject_short_transfer_row_count"],
        "long_row_count": long_pattern["row_count"],
        "long_best_offset_median_ns": long_pattern["best_offset_median_ns"],
        "long_best_offset_distance_from_short_pair_median_ns": (
            long_pattern["best_offset_distance_from_short_pair_median_ns"]
        ),
        "early_vs_short_delta_half_widths": safe_float(timing.get("early_vs_short_delta_half_widths")),
        "long_vs_short_delta_half_widths": safe_float(timing.get("long_vs_short_delta_half_widths")),
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "gpu_priority": "none",
        "ready_for_manuscript_field_timing_boundary": ready,
        "decision": (
            "Use this as a window-family timing classification: strict early "
            "windows are common-mode near-zero lag, short content windows support "
            "the relative correction envelope while raw/no-correction is rejected, "
            "and long shallow windows reject short-pair transfer in favor of a "
            "separate pattern-only shift. This remains field QC, not absolute "
            "time-zero, FWI, 3D, radius, or cover-depth evidence."
        ),
    }


def plot_classification(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["timing_family"].replace("_", "\n") for row in rows]
    offsets = [safe_float(row["representative_offset_ns"], 0.0) for row in rows]
    deltas = [safe_float(row["delta_to_short_content_half_widths"], 0.0) for row in rows]
    support = [
        summary["early_strict_near_zero_lag_row_count"] / max(summary["early_strict_row_count"], 1),
        summary["short_nonraw_supported_count"] / max(summary["short_nonraw_row_count"], 1),
        summary["long_reject_short_transfer_row_count"] / max(summary["long_row_count"], 1),
    ]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(1, 3, figsize=(14.4, 4.8), constrained_layout=True)
    axes[0].bar(x, offsets, color=["#6b6b6b", "#2f6f9f", "#c77d2a"], width=0.55)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("offset (ns)")
    axes[0].set_title("Representative timing offsets")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, support, color=["#6b6b6b", "#4c9f70", "#7b5aa6"], width=0.55)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_ylabel("supported fraction")
    axes[1].set_title("Window-family support")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(x, deltas, color=["#9a4d45", "#2f6f9f", "#9a4d45"], width=0.55)
    axes[2].axhline(1.0, color="#333333", linestyle="--", linewidth=1.0)
    axes[2].set_xticks(x, labels)
    axes[2].set_ylabel("delta from short content (half-widths)")
    axes[2].set_title("Conflict against short relative timing")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Field timing window-family classification: {summary['policy_label']}",
        fontsize=12,
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_timing_window_family_classification.png`",
                "",
                "This figure classifies existing field timing evidence by window family.",
                "It compares early common-mode lag rows, short-pair content timing",
                "perturbation rows, and long-profile pattern-only shift rows.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Strict early near-zero lag rows: `{summary['early_strict_near_zero_lag_row_count']}` of `{summary['early_strict_row_count']}`.",
                f"Short nonraw supported rows: `{summary['short_nonraw_supported_count']}` of `{summary['short_nonraw_row_count']}`.",
                f"Long short-transfer rejection rows: `{summary['long_reject_short_transfer_row_count']}` of `{summary['long_row_count']}`.",
                "",
                "This is a CPU-only synthesis of existing QC rows. It does not run",
                "FDTD/FWI and does not create absolute time-zero, cover-depth, radius,",
                "field FWI, or 3D claims.",
                "",
                f"Family rows are stored in `{rows_csv.name}`. Image-validation metrics",
                f"for this figure are stored in `{validation_csv.name}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--early-time-anchor-run", default=DEFAULT_EARLY_TIME_ANCHOR_RUN)
    parser.add_argument("--time-zero-budget-run", default=DEFAULT_TIME_ZERO_BUDGET_RUN)
    parser.add_argument("--time-zero-perturbation-run", default=DEFAULT_TIME_ZERO_PERTURBATION_RUN)
    parser.add_argument("--long-shift-sensitivity-run", default=DEFAULT_LONG_SHIFT_SENSITIVITY_RUN)
    parser.add_argument("--timing-conflict-run", default=DEFAULT_TIMING_CONFLICT_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_timing_window_family_classification")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    early_dir = dataset_root / args.early_time_anchor_run
    perturbation_dir = dataset_root / args.time_zero_perturbation_run
    long_dir = dataset_root / args.long_shift_sensitivity_run
    timing_dir = dataset_root / args.timing_conflict_run

    early_rows = read_csv_rows(early_dir / "data/field_early_time_pair_lags.csv")
    perturbation_rows = read_csv_rows(perturbation_dir / "data/field_time_zero_perturbation_windows.csv")
    long_rows = read_csv_rows(long_dir / "data/long_profile_shift_scan_sensitivity_rows.csv")
    timing_summary = read_json(timing_dir / "data/field_timing_anchor_conflict_summary.json")

    early = classify_early_rows(early_rows)
    short_content = classify_short_content_rows(perturbation_rows)
    long_pattern = classify_long_pattern_rows(long_rows)
    rows = family_rows(early, short_content, long_pattern, timing_summary)
    summary = summarize(early, short_content, long_pattern, timing_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_timing_window_family_rows.csv"
    summary_json = data_dir / "field_timing_window_family_classification_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(
        plot_classification(rows, summary, figures_dir / "field_timing_window_family_classification.png")
    )
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv, validation_csv)
    output_summary = {
        "runs": {
            "early_time_anchor": args.early_time_anchor_run,
            "time_zero_budget": args.time_zero_budget_run,
            "time_zero_perturbation": args.time_zero_perturbation_run,
            "long_shift_sensitivity": args.long_shift_sensitivity_run,
            "timing_conflict": args.timing_conflict_run,
        },
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_timing_window_family_classification",
        {
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
