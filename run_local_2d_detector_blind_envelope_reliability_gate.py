#!/usr/bin/env python3
"""Build a truth-free reliability gate for blind-envelope detector assignments."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
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
from run_local_2d_detector_blind_envelope_robustness_audit import parse_bool  # noqa: E402
from run_local_2d_detector_blind_envelope_policy_stability import (  # noqa: E402
    DEFAULT_BLIND_ENVELOPE_RUN,
    DEFAULT_ROBUSTNESS_RUN,
    read_csv_rows,
)
from run_local_2d_detector_blind_envelope_tuning_sensitivity import DEFAULT_STABILITY_RUN  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TUNING_RUN = "066_local_2d_detector_blind_envelope_tuning_sensitivity"
STABLE_SLOT_RANGE_THRESHOLD_MM = 5.0


def parse_number_list(value: object) -> list[float]:
    if value is None:
        return []
    numbers = []
    for part in str(value).split(","):
        text = part.strip()
        if not text:
            continue
        try:
            number = float(text)
        except ValueError:
            continue
        if math.isfinite(number):
            numbers.append(number)
    return numbers


def _slot_ranges(values: list[list[float]], slot_count: int = 3) -> list[float]:
    ranges = []
    for slot_index in range(slot_count):
        slot_values = [row[slot_index] for row in values if len(row) > slot_index]
        ranges.append(max(slot_values) - min(slot_values) if slot_values else math.nan)
    return ranges


def _iqr(values: list[float]) -> float:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return math.nan
    return float(np.percentile(finite, 75) - np.percentile(finite, 25))


def reliability_label(max_slot_x_range_mm: float, threshold_mm: float = STABLE_SLOT_RANGE_THRESHOLD_MM) -> str:
    if not math.isfinite(max_slot_x_range_mm):
        return "review_missing_selection_values"
    if max_slot_x_range_mm <= threshold_mm:
        return "stable_truth_free_assignment"
    return "review_policy_grid_position_drift"


def case_reliability_rows(
    selected_rows: list[dict],
    threshold_mm: float = STABLE_SLOT_RANGE_THRESHOLD_MM,
) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in selected_rows:
        grouped[str(row.get("case_label", ""))].append(row)

    outputs = []
    for case_label, rows in grouped.items():
        first = rows[0]
        x_values = [parse_number_list(row.get("selected_x_values_mm")) for row in rows]
        z_values = [parse_number_list(row.get("selected_z_values_mm")) for row in rows]
        x_ranges = _slot_ranges(x_values)
        z_ranges = _slot_ranges(z_values)
        selections = Counter(str(row.get("selected_x_values_mm", "")) for row in rows)
        dominant_selection, dominant_count = selections.most_common(1)[0] if selections else ("", 0)
        success_count = sum(parse_bool(row.get("all_target_slots_hit")) for row in rows)
        variant_count = len(rows)
        max_x_range = max([value for value in x_ranges if math.isfinite(value)] or [math.nan])
        max_z_range = max([value for value in z_ranges if math.isfinite(value)] or [math.nan])
        scores = [safe_float(row.get("selection_score"), math.nan) for row in rows]
        label = reliability_label(max_x_range, threshold_mm)
        outputs.append(
            {
                "case_label": case_label,
                "branch_key": first.get("branch_key", ""),
                "seed": safe_int(first.get("seed"), 0),
                "case_variant": first.get("case_variant", ""),
                "variant_count": variant_count,
                "unique_selection_count": len(selections),
                "dominant_selection": dominant_selection,
                "dominant_selection_count": dominant_count,
                "dominant_selection_fraction": dominant_count / variant_count if variant_count else 0.0,
                "slot0_x_range_mm": x_ranges[0],
                "slot1_x_range_mm": x_ranges[1],
                "slot2_x_range_mm": x_ranges[2],
                "max_slot_x_range_mm": max_x_range,
                "median_slot_x_range_mm": float(np.nanmedian(x_ranges)),
                "max_slot_z_range_mm": max_z_range,
                "selection_score_iqr": _iqr(scores),
                "truth_free_reliability_label": label,
                "truth_free_stable_assignment": label == "stable_truth_free_assignment",
                "all_target_slot_variant_count_truth_eval": success_count,
                "success_fraction_truth_eval": success_count / variant_count if variant_count else 0.0,
                "tuning_sensitive_truth_eval": (success_count / variant_count if variant_count else 0.0) < 0.90,
            }
        )
    return sorted(outputs, key=lambda row: (row["branch_key"], row["seed"], row["case_variant"]))


def branch_reliability_rows(case_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in case_rows:
        grouped[str(row.get("branch_key", ""))].append(row)

    outputs = []
    for branch_key, rows in grouped.items():
        stable_rows = [row for row in rows if row["truth_free_stable_assignment"]]
        review_rows = [row for row in rows if not row["truth_free_stable_assignment"]]
        outputs.append(
            {
                "branch_key": branch_key,
                "case_count": len(rows),
                "stable_assignment_case_count": len(stable_rows),
                "review_assignment_case_count": len(review_rows),
                "tuning_sensitive_case_count_truth_eval": sum(
                    parse_bool(row.get("tuning_sensitive_truth_eval")) for row in rows
                ),
                "max_slot_x_range_mm": max([safe_float(row.get("max_slot_x_range_mm")) for row in rows] or [0.0]),
                "median_slot_x_range_mm": float(
                    np.median([safe_float(row.get("max_slot_x_range_mm"), 0.0) for row in rows])
                )
                if rows
                else 0.0,
                "review_case_labels": ";".join(str(row["case_label"]) for row in review_rows),
            }
        )
    return sorted(outputs, key=lambda row: row["branch_key"])


def summarize_reliability(
    case_rows: list[dict],
    branch_rows: list[dict],
    source_summary: dict,
    stability_summary: dict,
    tuning_summary: dict,
    threshold_mm: float = STABLE_SLOT_RANGE_THRESHOLD_MM,
) -> dict:
    stable_rows = [row for row in case_rows if row["truth_free_stable_assignment"]]
    review_rows = [row for row in case_rows if not row["truth_free_stable_assignment"]]
    tuning_rows = [row for row in case_rows if parse_bool(row.get("tuning_sensitive_truth_eval"))]
    stable_partial_rows = [
        row for row in stable_rows
        if safe_float(row.get("success_fraction_truth_eval"), 0.0) < 1.0
    ]
    tuning_detected = [
        row for row in tuning_rows
        if not parse_bool(row.get("truth_free_stable_assignment"))
    ]
    false_review = [
        row for row in review_rows
        if safe_float(row.get("success_fraction_truth_eval"), 0.0) == 1.0
    ]
    ready_for_reliability_claim = (
        len(stable_partial_rows) == 0
        and len(tuning_detected) == len(tuning_rows)
        and len(review_rows) > 0
    )
    return {
        "policy_label": "local_2d_detector_blind_envelope_reliability_gate_cpu_no_fwi",
        "source_policy_label": source_summary.get("policy_label", ""),
        "stability_policy_label": stability_summary.get("policy_label", ""),
        "tuning_policy_label": tuning_summary.get("policy_label", ""),
        "case_count": len(case_rows),
        "branch_count": len(branch_rows),
        "variant_count": safe_int(source_summary.get("variant_count"), 0),
        "stable_slot_range_threshold_mm": threshold_mm,
        "stable_assignment_case_count": len(stable_rows),
        "review_assignment_case_count": len(review_rows),
        "stable_assignment_all_variant_success_count": len(stable_rows) - len(stable_partial_rows),
        "stable_assignment_partial_success_count": len(stable_partial_rows),
        "tuning_sensitive_case_count_truth_eval": len(tuning_rows),
        "tuning_sensitive_detected_by_gate_count": len(tuning_detected),
        "tuning_sensitive_missed_by_gate_count": len(tuning_rows) - len(tuning_detected),
        "false_review_all_variant_success_count": len(false_review),
        "stable_assignment_min_success_fraction_truth_eval": min(
            [safe_float(row.get("success_fraction_truth_eval"), 0.0) for row in stable_rows] or [0.0]
        ),
        "review_assignment_max_slot_x_range_mm": max(
            [safe_float(row.get("max_slot_x_range_mm"), 0.0) for row in review_rows] or [0.0]
        ),
        "stable_assignment_max_slot_x_range_mm": max(
            [safe_float(row.get("max_slot_x_range_mm"), 0.0) for row in stable_rows] or [0.0]
        ),
        "review_case_labels": ";".join(str(row["case_label"]) for row in review_rows),
        "stable_case_labels": ";".join(str(row["case_label"]) for row in stable_rows),
        "truth_free_gate_uses_truth": False,
        "truth_evaluation_used_for_audit": True,
        "ready_for_reliability_claim": ready_for_reliability_claim,
        "ready_for_global_policy_tuning_fix": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "A truth-free x-slot drift gate separates stable blind-envelope detector assignments from the "
            "known close50 nominal policy-sensitive cases. Use this as detector reliability/ambiguity-boundary "
            "evidence; it does not justify detector-seeded FWI."
        ),
    }


def plot_reliability(case_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["case_label"].replace("|", "\n") for row in case_rows]
    x_ranges = [safe_float(row.get("max_slot_x_range_mm"), 0.0) for row in case_rows]
    success = [safe_float(row.get("success_fraction_truth_eval"), 0.0) for row in case_rows]

    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    colors = ["#4e79a7" if row["truth_free_stable_assignment"] else "#e15759" for row in case_rows]
    axes[0].bar(np.arange(len(case_rows)), x_ranges, color=colors, edgecolor="#333333", linewidth=0.5)
    axes[0].axhline(
        summary["stable_slot_range_threshold_mm"],
        color="#f28e2b",
        linestyle="--",
        linewidth=1.2,
    )
    axes[0].set_xticks(np.arange(len(case_rows)), labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("max sorted x-slot range (mm)")
    axes[0].set_title("Truth-free policy-grid position drift")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(np.arange(len(case_rows)), success, color=colors, edgecolor="#333333", linewidth=0.5)
    axes[1].axhline(0.90, color="#f28e2b", linestyle="--", linewidth=1.2)
    axes[1].set_xticks(np.arange(len(case_rows)), labels, rotation=45, ha="right", fontsize=7)
    axes[1].set_ylim(0, 1.05)
    axes[1].set_ylabel("success fraction, audit only")
    axes[1].set_title("Truth evaluation of the gate")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"stable cases: {summary['stable_assignment_case_count']}/{summary['case_count']}\n"
        f"review cases: {summary['review_assignment_case_count']}\n"
        f"tuning detected: {summary['tuning_sensitive_detected_by_gate_count']}/"
        f"{summary['tuning_sensitive_case_count_truth_eval']}\n"
        f"ready claim: {summary['ready_for_reliability_claim']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Blind-envelope detector reliability gate", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, case_csv: Path, branch_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_blind_envelope_reliability_gate.png`",
                "",
                "This CPU-only figure builds a truth-free reliability gate from",
                "policy-grid x-slot drift across blind-envelope detector selections.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Stable slot-range threshold: `{summary['stable_slot_range_threshold_mm']}` mm.",
                f"Stable assignments: `{summary['stable_assignment_case_count']}`.",
                f"Review assignments: `{summary['review_assignment_case_count']}`.",
                f"Tuning-sensitive cases detected: `{summary['tuning_sensitive_detected_by_gate_count']}`.",
                f"Ready for reliability claim: `{summary['ready_for_reliability_claim']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case reliability rows: `{case_csv.name}`.",
                f"- Branch reliability rows: `{branch_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved CPU detector-policy rows only. The gate itself",
                "uses no truth labels, while the success fractions are used only for",
                "post-hoc evaluation. It does not run FDTD, FWI, GPU kernels, field",
                "FWI, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--blind-envelope-run", default=DEFAULT_BLIND_ENVELOPE_RUN)
    parser.add_argument("--stability-run", default=DEFAULT_STABILITY_RUN)
    parser.add_argument("--robustness-run", default=DEFAULT_ROBUSTNESS_RUN)
    parser.add_argument("--tuning-run", default=DEFAULT_TUNING_RUN)
    parser.add_argument("--stable-slot-range-threshold-mm", type=float, default=STABLE_SLOT_RANGE_THRESHOLD_MM)
    parser.add_argument("--run-name", default="local_2d_detector_blind_envelope_reliability_gate")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    source_dir = summary_root / args.blind_envelope_run
    stability_dir = summary_root / args.stability_run
    robustness_dir = summary_root / args.robustness_run
    tuning_dir = summary_root / args.tuning_run

    selected_rows = read_csv_rows(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
    )
    source_summary = read_json(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
    )
    stability_summary = read_json(
        stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_summary.json"
    )
    robustness_summary = read_json(
        robustness_dir / "data/local_2d_detector_blind_envelope_robustness_summary.json"
    )
    tuning_summary = read_json(
        tuning_dir / "data/local_2d_detector_blind_envelope_tuning_sensitivity_summary.json"
    )

    case_rows = case_reliability_rows(selected_rows, args.stable_slot_range_threshold_mm)
    branch_rows = branch_reliability_rows(case_rows)
    summary = summarize_reliability(
        case_rows,
        branch_rows,
        source_summary,
        stability_summary,
        tuning_summary,
        args.stable_slot_range_threshold_mm,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_blind_envelope_reliability_gate_cases.csv"
    branch_csv = data_dir / "local_2d_detector_blind_envelope_reliability_gate_branches.csv"
    summary_json = data_dir / "local_2d_detector_blind_envelope_reliability_gate_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_blind_envelope_reliability_gate.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(case_csv, [json_safe(row) for row in case_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    plot_reliability(case_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, case_csv, branch_csv)
    summary["paths"] = {
        "case_reliability_csv": str(case_csv),
        "branch_reliability_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "source_blind_envelope_summary_json": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
        ),
        "source_blind_envelope_selected_cases_csv": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
        ),
        "source_stability_summary_json": str(
            stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_summary.json"
        ),
        "source_robustness_summary_json": str(
            robustness_dir / "data/local_2d_detector_blind_envelope_robustness_summary.json"
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
        "local_2d_detector_blind_envelope_reliability_gate",
        {
            "blind_envelope_run": args.blind_envelope_run,
            "stability_run": args.stability_run,
            "robustness_run": args.robustness_run,
            "tuning_run": args.tuning_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
