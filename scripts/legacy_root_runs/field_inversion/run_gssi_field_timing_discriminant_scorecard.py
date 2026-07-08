#!/usr/bin/env python3
"""Build a timing-discriminant scorecard from existing local GSSI field timing rows."""

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


DEFAULT_EARLY_ANCHOR_RUN = "090_gssi51600s_field_early_time_anchor_audit"
DEFAULT_SHORT_PERTURBATION_RUN = "078_gssi51600s_field_time_zero_perturbation_sensitivity"
DEFAULT_LONG_SHIFT_SENSITIVITY_RUN = "055_gssi51600s_long_profile_shift_scan_sensitivity"
DEFAULT_TIMING_WINDOW_RUN = "101_gssi51600s_field_timing_window_family_classification"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def count_true(rows: list[dict], key: str) -> int:
    return sum(str(row.get(key, "")).strip().lower() == "true" for row in rows)


def fraction(numerator: float, denominator: float) -> float:
    denominator = safe_float(denominator, 0.0)
    if denominator <= 0:
        return math.nan
    return safe_float(numerator, 0.0) / denominator


def classify_early_rows(rows: list[dict]) -> dict:
    strict = [row for row in rows if str(row.get("window_label", "")).startswith("early_")]
    all_rows = list(rows)
    strict_near_zero = [
        row
        for row in strict
        if abs(safe_float(row.get("comparison_minus_reference_shift_ns"), 999.0))
        <= safe_float(row.get("dt_ns"), 0.0) + 1e-12
    ]
    all_near_zero = [
        row
        for row in all_rows
        if abs(safe_float(row.get("comparison_minus_reference_shift_ns"), 999.0))
        <= safe_float(row.get("dt_ns"), 0.0) + 1e-12
    ]
    min_margin = min(
        (safe_float(row.get("best_minus_second_correlation")) for row in strict),
        default=math.nan,
    )
    max_abs_shift = max(
        (abs(safe_float(row.get("comparison_minus_reference_shift_ns"), 0.0)) for row in strict),
        default=math.nan,
    )
    return {
        "row_count": len(all_rows),
        "strict_row_count": len(strict),
        "strict_near_zero_count": len(strict_near_zero),
        "all_near_zero_count": len(all_near_zero),
        "strict_near_zero_fraction": fraction(len(strict_near_zero), len(strict)),
        "all_near_zero_fraction": fraction(len(all_near_zero), len(all_rows)),
        "max_strict_abs_shift_ns": max_abs_shift,
        "min_strict_best_minus_second_correlation": min_margin,
        "has_low_uniqueness_margin": bool(math.isfinite(min_margin) and min_margin < 5e-4),
    }


def classify_short_rows(rows: list[dict]) -> dict:
    raw = [row for row in rows if row.get("offset_family") == "raw_baseline"]
    nonraw = [row for row in rows if row.get("offset_family") != "raw_baseline"]
    nominal = [row for row in rows if row.get("offset_family") == "nominal"]
    supported_nonraw = [row for row in nonraw if str(row.get("offset_window_supported", "")).lower() == "true"]
    supported_raw = [row for row in raw if str(row.get("offset_window_supported", "")).lower() == "true"]
    min_nonraw_improvement = min(
        (safe_float(row.get("matrix_abs_correlation_improvement")) for row in nonraw),
        default=math.nan,
    )
    min_nonraw_corrected = min(
        (safe_float(row.get("corrected_matrix_abs_correlation")) for row in nonraw),
        default=math.nan,
    )
    min_nominal_improvement = min(
        (safe_float(row.get("matrix_abs_correlation_improvement")) for row in nominal),
        default=math.nan,
    )
    max_raw_improvement = max(
        (safe_float(row.get("matrix_abs_correlation_improvement")) for row in raw),
        default=math.nan,
    )
    nominal_offset = next(
        (safe_float(row.get("offset_ns")) for row in nominal if math.isfinite(safe_float(row.get("offset_ns")))),
        math.nan,
    )
    return {
        "row_count": len(rows),
        "raw_row_count": len(raw),
        "raw_supported_count": len(supported_raw),
        "nonraw_row_count": len(nonraw),
        "nonraw_supported_count": len(supported_nonraw),
        "nonraw_supported_fraction": fraction(len(supported_nonraw), len(nonraw)),
        "raw_supported_fraction": fraction(len(supported_raw), len(raw)),
        "nominal_offset_ns": nominal_offset,
        "min_nonraw_matrix_improvement": min_nonraw_improvement,
        "min_nonraw_corrected_abs_correlation": min_nonraw_corrected,
        "min_nominal_matrix_improvement": min_nominal_improvement,
        "max_raw_matrix_improvement": max_raw_improvement,
    }


def classify_long_rows(rows: list[dict], short_offset_ns: float) -> dict:
    reject_short = [
        row for row in rows if safe_float(row.get("short_pair_offset_gain_vs_zero"), 1.0) < 0.0
    ]
    best_offsets = [safe_float(row.get("best_matrix_offset_ns")) for row in rows]
    best_offsets = [value for value in best_offsets if math.isfinite(value)]
    best_gains = [safe_float(row.get("best_matrix_gain_vs_zero")) for row in rows]
    best_gains = [value for value in best_gains if math.isfinite(value)]
    short_gains = [safe_float(row.get("short_pair_offset_gain_vs_zero")) for row in rows]
    short_gains = [value for value in short_gains if math.isfinite(value)]
    return {
        "row_count": len(rows),
        "reject_short_transfer_count": len(reject_short),
        "reject_short_transfer_fraction": fraction(len(reject_short), len(rows)),
        "best_offset_median_ns": float(np.median(best_offsets)) if best_offsets else math.nan,
        "best_offset_spread_ns": max(best_offsets) - min(best_offsets) if best_offsets else math.nan,
        "best_offset_distance_from_short_ns": (
            abs(float(np.median(best_offsets)) - short_offset_ns)
            if best_offsets and math.isfinite(short_offset_ns)
            else math.nan
        ),
        "min_best_gain_vs_zero": min(best_gains) if best_gains else math.nan,
        "max_short_gain_vs_zero": max(short_gains) if short_gains else math.nan,
    }


def build_score_rows(
    *,
    early: dict,
    short: dict,
    long: dict,
) -> list[dict]:
    return [
        {
            "timing_discriminant": "early_common_mode",
            "support_count": early["strict_near_zero_count"],
            "row_count": early["strict_row_count"],
            "support_fraction": early["strict_near_zero_fraction"],
            "representative_offset_ns": 0.0,
            "strength_metric": early["min_strict_best_minus_second_correlation"],
            "strength_label": (
                "near_zero_with_low_uniqueness_margin"
                if early["has_low_uniqueness_margin"]
                else "near_zero_common_mode"
            ),
            "allowed_use": "early/direct-wave common-mode timing QC",
            "blocked_use": "absolute time-zero calibration",
        },
        {
            "timing_discriminant": "short_content_relative",
            "support_count": short["nonraw_supported_count"],
            "row_count": short["nonraw_row_count"],
            "support_fraction": short["nonraw_supported_fraction"],
            "representative_offset_ns": short["nominal_offset_ns"],
            "strength_metric": short["min_nonraw_matrix_improvement"],
            "strength_label": "robust_relative_timing_support",
            "allowed_use": "short-pair relative timing and corrected-stack QC",
            "blocked_use": "absolute time-zero, field FWI, 3D, radius, or cover-depth recovery",
        },
        {
            "timing_discriminant": "raw_no_correction",
            "support_count": short["raw_supported_count"],
            "row_count": short["raw_row_count"],
            "support_fraction": short["raw_supported_fraction"],
            "representative_offset_ns": 0.0,
            "strength_metric": short["max_raw_matrix_improvement"],
            "strength_label": "raw_alignment_rejected",
            "allowed_use": "negative-control baseline",
            "blocked_use": "uncorrected short-pair timing support",
        },
        {
            "timing_discriminant": "long_pattern_only",
            "support_count": long["reject_short_transfer_count"],
            "row_count": long["row_count"],
            "support_fraction": long["reject_short_transfer_fraction"],
            "representative_offset_ns": long["best_offset_median_ns"],
            "strength_metric": long["min_best_gain_vs_zero"],
            "strength_label": "stable_pattern_shift_rejects_short_transfer",
            "allowed_use": "long-profile pattern-only visual QC",
            "blocked_use": "phase time-zero, short-transfer timing, field FWI, or 3D inversion",
        },
    ]


def summarize_scorecard(score_rows: list[dict], early: dict, short: dict, long: dict, timing_window: dict) -> dict:
    ready = (
        early["strict_near_zero_count"] == early["strict_row_count"]
        and short["nonraw_supported_count"] == short["nonraw_row_count"]
        and short["raw_supported_count"] == 0
        and long["reject_short_transfer_count"] == long["row_count"]
        and not bool(timing_window.get("absolute_time_zero_ready", False))
        and not bool(timing_window.get("field_fwi_ready", False))
    )
    return {
        "policy_label": (
            "field_timing_discriminant_scorecard_ready_not_absolute"
            if ready
            else "field_timing_discriminant_scorecard_review_required"
        ),
        "score_row_count": len(score_rows),
        "early_strict_near_zero_count": early["strict_near_zero_count"],
        "early_strict_row_count": early["strict_row_count"],
        "early_min_uniqueness_margin": early["min_strict_best_minus_second_correlation"],
        "early_has_low_uniqueness_margin": early["has_low_uniqueness_margin"],
        "short_nonraw_supported_count": short["nonraw_supported_count"],
        "short_nonraw_row_count": short["nonraw_row_count"],
        "short_raw_supported_count": short["raw_supported_count"],
        "short_raw_row_count": short["raw_row_count"],
        "short_nominal_offset_ns": short["nominal_offset_ns"],
        "short_min_nonraw_matrix_improvement": short["min_nonraw_matrix_improvement"],
        "short_min_nonraw_corrected_abs_correlation": short["min_nonraw_corrected_abs_correlation"],
        "long_reject_short_transfer_count": long["reject_short_transfer_count"],
        "long_row_count": long["row_count"],
        "long_best_offset_median_ns": long["best_offset_median_ns"],
        "long_best_offset_distance_from_short_ns": long["best_offset_distance_from_short_ns"],
        "long_min_best_gain_vs_zero": long["min_best_gain_vs_zero"],
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "gpu_priority": "none",
        "ready_for_manuscript_timing_scorecard": ready,
        "decision": (
            "Use this scorecard to report timing discriminants: early windows are common-mode, "
            "short non-raw windows support relative timing, raw/no-correction is rejected, and "
            "long windows stay pattern-only. It does not create absolute time-zero or field FWI claims."
        ),
    }


def plot_scorecard(score_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["timing_discriminant"].replace("_", "\n") for row in score_rows]
    support = [safe_float(row["support_fraction"], 0.0) for row in score_rows]
    offsets = [safe_float(row["representative_offset_ns"], 0.0) for row in score_rows]
    strength = [safe_float(row["strength_metric"], 0.0) for row in score_rows]

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.6), constrained_layout=True)
    x = np.arange(len(score_rows))
    axes[0].bar(x, support, color="#2f9d55", width=0.62)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylim(0, 1.05)
    axes[0].set_title("Timing support fraction")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, offsets, color="#4c78a8", width=0.62)
    axes[1].set_xticks(x, labels, fontsize=8)
    axes[1].set_ylabel("offset [ns]")
    axes[1].set_title("Representative offsets")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(x, strength, color="#8c564b", width=0.62)
    axes[2].set_xticks(x, labels, fontsize=8)
    axes[2].set_title("Strength metric")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(f"Field timing discriminant scorecard: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, score_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_timing_discriminant_scorecard.png`",
                "",
                "This is a CPU-only scorecard built from existing measured-field",
                "timing rows: early lag windows, short-pair time-zero perturbation",
                "windows, long-profile shift sensitivity, and the timing-window",
                "family classification summary.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Early strict near-zero windows: `{summary['early_strict_near_zero_count']}/{summary['early_strict_row_count']}`.",
                f"Short non-raw supported windows: `{summary['short_nonraw_supported_count']}/{summary['short_nonraw_row_count']}`.",
                f"Raw/no-correction supported windows: `{summary['short_raw_supported_count']}/{summary['short_raw_row_count']}`.",
                f"Long windows rejecting short transfer: `{summary['long_reject_short_transfer_count']}/{summary['long_row_count']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Score rows: `{score_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The scorecard supports field timing-claim discipline only. It",
                "does not create absolute time-zero, field FWI, 3D, radius, or",
                "cover-depth claims.",
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
    parser.add_argument("--early-anchor-run", default=DEFAULT_EARLY_ANCHOR_RUN)
    parser.add_argument("--short-perturbation-run", default=DEFAULT_SHORT_PERTURBATION_RUN)
    parser.add_argument("--long-shift-sensitivity-run", default=DEFAULT_LONG_SHIFT_SENSITIVITY_RUN)
    parser.add_argument("--timing-window-run", default=DEFAULT_TIMING_WINDOW_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_timing_discriminant_scorecard")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    early_dir = dataset_root / args.early_anchor_run
    short_dir = dataset_root / args.short_perturbation_run
    long_dir = dataset_root / args.long_shift_sensitivity_run
    timing_dir = dataset_root / args.timing_window_run

    early_rows = read_csv_rows(early_dir / "data/field_early_time_pair_lags.csv")
    short_rows = read_csv_rows(short_dir / "data/field_time_zero_perturbation_windows.csv")
    long_rows = read_csv_rows(long_dir / "data/long_profile_shift_scan_sensitivity_rows.csv")
    timing_summary = read_json(timing_dir / "data/field_timing_window_family_classification_summary.json")

    early = classify_early_rows(early_rows)
    short = classify_short_rows(short_rows)
    long = classify_long_rows(long_rows, short["nominal_offset_ns"])
    score_rows = build_score_rows(early=early, short=short, long=long)
    summary = summarize_scorecard(score_rows, early, short, long, timing_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    score_csv = data_dir / "field_timing_discriminant_scorecard_rows.csv"
    summary_json = data_dir / "field_timing_discriminant_scorecard_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_timing_discriminant_scorecard.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(score_csv, [json_safe(row) for row in score_rows])
    plot_scorecard(score_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "score_rows_csv": str(score_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, score_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "gssi_field_timing_discriminant_scorecard",
        {
            "dataset_id": args.dataset_id,
            "early_anchor_run": args.early_anchor_run,
            "short_perturbation_run": args.short_perturbation_run,
            "long_shift_sensitivity_run": args.long_shift_sensitivity_run,
            "timing_window_run": args.timing_window_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
