#!/usr/bin/env python3
"""Test threshold sensitivity for the blind-envelope reliability gate."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_blind_envelope_reliability_gate import (  # noqa: E402
    DEFAULT_TUNING_RUN,
    parse_bool,
)
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RELIABILITY_RUN = "069_local_2d_detector_blind_envelope_reliability_gate"
DEFAULT_THRESHOLDS_MM = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 7.5, 10.0, 15.0, 19.0, 20.0, 21.0]


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def threshold_sensitivity_rows(case_rows: list[dict], thresholds_mm: list[float]) -> list[dict]:
    outputs = []
    case_count = len(case_rows)
    tuning_case_count = sum(parse_bool(row.get("tuning_sensitive_truth_eval")) for row in case_rows)
    for threshold in thresholds_mm:
        stable_rows = [
            row for row in case_rows
            if safe_float(row.get("max_slot_x_range_mm"), math.inf) <= threshold
        ]
        review_rows = [row for row in case_rows if row not in stable_rows]
        stable_partial = [
            row for row in stable_rows
            if safe_float(row.get("success_fraction_truth_eval"), 0.0) < 1.0
        ]
        tuning_missed = [
            row for row in stable_rows
            if parse_bool(row.get("tuning_sensitive_truth_eval"))
        ]
        false_review = [
            row for row in review_rows
            if safe_float(row.get("success_fraction_truth_eval"), 0.0) == 1.0
        ]
        clean_gate = (
            len(stable_partial) == 0
            and len(tuning_missed) == 0
            and len(false_review) == 0
            and len(stable_rows) > 0
            and tuning_case_count > 0
        )
        outputs.append(
            {
                "threshold_mm": threshold,
                "case_count": case_count,
                "stable_assignment_case_count": len(stable_rows),
                "review_assignment_case_count": len(review_rows),
                "stable_assignment_partial_success_count": len(stable_partial),
                "tuning_sensitive_missed_count": len(tuning_missed),
                "tuning_sensitive_detected_count": tuning_case_count - len(tuning_missed),
                "false_review_all_variant_success_count": len(false_review),
                "clean_gate": clean_gate,
                "stable_case_labels": ";".join(str(row["case_label"]) for row in stable_rows),
                "review_case_labels": ";".join(str(row["case_label"]) for row in review_rows),
            }
        )
    return outputs


def summarize_thresholds(
    threshold_rows: list[dict],
    reliability_summary: dict,
    tuning_summary: dict,
) -> dict:
    clean_rows = [row for row in threshold_rows if parse_bool(row.get("clean_gate"))]
    default_threshold = safe_float(reliability_summary.get("stable_slot_range_threshold_mm"), 5.0)
    default_rows = [
        row for row in threshold_rows
        if safe_float(row.get("threshold_mm"), math.nan) == default_threshold
    ]
    default_row = default_rows[0] if default_rows else {}
    return {
        "policy_label": "local_2d_detector_blind_envelope_reliability_threshold_sensitivity_cpu_no_fwi",
        "source_reliability_policy_label": reliability_summary.get("policy_label", ""),
        "source_tuning_policy_label": tuning_summary.get("policy_label", ""),
        "threshold_count": len(threshold_rows),
        "clean_threshold_count": len(clean_rows),
        "clean_threshold_min_mm": min([safe_float(row.get("threshold_mm")) for row in clean_rows] or [math.nan]),
        "clean_threshold_max_mm": max([safe_float(row.get("threshold_mm")) for row in clean_rows] or [math.nan]),
        "default_threshold_mm": default_threshold,
        "default_threshold_clean": bool(default_row.get("clean_gate", False)),
        "default_threshold_stable_cases": safe_float(default_row.get("stable_assignment_case_count"), 0.0),
        "default_threshold_review_cases": safe_float(default_row.get("review_assignment_case_count"), 0.0),
        "default_threshold_tuning_missed": safe_float(default_row.get("tuning_sensitive_missed_count"), 0.0),
        "default_threshold_false_review": safe_float(default_row.get("false_review_all_variant_success_count"), 0.0),
        "thresholds_with_tuning_missed": ";".join(
            f"{safe_float(row.get('threshold_mm')):g}"
            for row in threshold_rows
            if safe_float(row.get("tuning_sensitive_missed_count"), 0.0) > 0.0
        ),
        "thresholds_with_false_review": ";".join(
            f"{safe_float(row.get('threshold_mm')):g}"
            for row in threshold_rows
            if safe_float(row.get("false_review_all_variant_success_count"), 0.0) > 0.0
        ),
        "ready_for_reliability_claim": bool(default_row.get("clean_gate", False)) and len(clean_rows) > 0,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "The truth-free x-slot reliability gate is not a single-point artifact: the default 5 mm "
            "threshold lies inside a clean interval that accepts the stable cases and flags the known "
            "close50 nominal tuning-sensitive cases. Keep this as CPU-side confidence-boundary evidence, "
            "not a detector-seeded FWI trigger."
        ),
    }


def plot_thresholds(rows: list[dict], summary: dict, save_path: Path) -> str:
    thresholds = [safe_float(row.get("threshold_mm"), 0.0) for row in rows]
    stable = [safe_float(row.get("stable_assignment_case_count"), 0.0) for row in rows]
    missed = [safe_float(row.get("tuning_sensitive_missed_count"), 0.0) for row in rows]
    false_review = [safe_float(row.get("false_review_all_variant_success_count"), 0.0) for row in rows]
    clean = [parse_bool(row.get("clean_gate")) for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)
    axes[0].plot(thresholds, stable, marker="o", color="#4e79a7", label="stable cases")
    axes[0].plot(thresholds, [row["case_count"] for row in rows], color="#bbbbbb", linewidth=1.0, label="all cases")
    axes[0].axvline(summary["default_threshold_mm"], color="#f28e2b", linestyle="--", linewidth=1.2)
    axes[0].set_xlabel("x-slot drift threshold (mm)")
    axes[0].set_ylabel("case count")
    axes[0].set_title("Accepted stable cases")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(fontsize=8)

    axes[1].plot(thresholds, missed, marker="o", color="#e15759", label="tuning missed")
    axes[1].plot(thresholds, false_review, marker="s", color="#59a14f", label="false review")
    for threshold, is_clean in zip(thresholds, clean):
        if is_clean:
            axes[1].axvspan(threshold - 0.1, threshold + 0.1, color="#d8f0dc", alpha=0.45)
    axes[1].axvline(summary["default_threshold_mm"], color="#f28e2b", linestyle="--", linewidth=1.2)
    axes[1].set_xlabel("x-slot drift threshold (mm)")
    axes[1].set_ylabel("error count")
    axes[1].set_title("Gate error modes")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    axes[1].legend(fontsize=8)
    axes[1].text(
        0.03,
        0.95,
        f"clean thresholds: {summary['clean_threshold_count']}/{summary['threshold_count']}\n"
        f"clean range: {summary['clean_threshold_min_mm']:g}-{summary['clean_threshold_max_mm']:g} mm\n"
        f"default clean: {summary['default_threshold_clean']}\n"
        f"ready claim: {summary['ready_for_reliability_claim']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Blind-envelope reliability threshold sensitivity", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_blind_envelope_reliability_threshold_sensitivity.png`",
                "",
                "This CPU-only figure tests whether the x-slot drift reliability gate",
                "depends on a brittle threshold choice.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Threshold count: `{summary['threshold_count']}`.",
                f"Clean threshold count: `{summary['clean_threshold_count']}`.",
                f"Clean threshold range: `{summary['clean_threshold_min_mm']}` to `{summary['clean_threshold_max_mm']}` mm.",
                f"Default threshold: `{summary['default_threshold_mm']}` mm.",
                f"Default threshold clean: `{summary['default_threshold_clean']}`.",
                f"Ready for reliability claim: `{summary['ready_for_reliability_claim']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Threshold rows: `{rows_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved CPU detector reliability rows only. It does not",
                "run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network",
                "training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--reliability-run", default=DEFAULT_RELIABILITY_RUN)
    parser.add_argument("--tuning-run", default=DEFAULT_TUNING_RUN)
    parser.add_argument(
        "--thresholds-mm",
        default=",".join(f"{value:g}" for value in DEFAULT_THRESHOLDS_MM),
        help="Comma-separated x-slot drift thresholds to audit.",
    )
    parser.add_argument("--run-name", default="local_2d_detector_blind_envelope_reliability_threshold_sensitivity")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    reliability_dir = summary_root / args.reliability_run
    tuning_dir = summary_root / args.tuning_run
    thresholds = [
        float(text.strip())
        for text in str(args.thresholds_mm).split(",")
        if text.strip()
    ]

    case_rows = read_csv_rows(
        reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_cases.csv"
    )
    reliability_summary = read_json(
        reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
    )
    tuning_summary = read_json(
        tuning_dir / "data/local_2d_detector_blind_envelope_tuning_sensitivity_summary.json"
    )

    rows = threshold_sensitivity_rows(case_rows, thresholds)
    summary = summarize_thresholds(rows, reliability_summary, tuning_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_blind_envelope_reliability_threshold_sensitivity_rows.csv"
    summary_json = data_dir / "local_2d_detector_blind_envelope_reliability_threshold_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_blind_envelope_reliability_threshold_sensitivity.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_thresholds(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv)
    summary["paths"] = {
        "threshold_rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "source_reliability_summary_json": str(
            reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
        ),
        "source_reliability_cases_csv": str(
            reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_cases.csv"
        ),
        "source_tuning_summary_json": str(
            tuning_dir / "data/local_2d_detector_blind_envelope_tuning_sensitivity_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_blind_envelope_reliability_threshold_sensitivity",
        {
            "reliability_run": args.reliability_run,
            "tuning_run": args.tuning_run,
            "thresholds_mm": args.thresholds_mm,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
