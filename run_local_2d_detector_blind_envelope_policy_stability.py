#!/usr/bin/env python3
"""Audit case-level stability of blind envelope detector assignment policies."""

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
from run_local_2d_detector_blind_envelope_robustness_audit import (  # noqa: E402
    DEFAULT_BLIND_ENVELOPE_RUN,
    parse_bool,
)
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ROBUSTNESS_RUN = "061_local_2d_detector_blind_envelope_robustness_audit"
FRAGILE_SUCCESS_FRACTION_THRESHOLD = 0.90
CONSENSUS_FRACTION_THRESHOLD = 0.95


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def case_sort_key(row: dict) -> tuple[str, int, str]:
    return (str(row.get("branch_key", "")), safe_int(row.get("seed"), 0), str(row.get("case_variant", "")))


def stability_label(success_fraction: float, unique_success_selection_count: int, dominant_fraction: float) -> str:
    if success_fraction < FRAGILE_SUCCESS_FRACTION_THRESHOLD:
        return "tuning_sensitive_partial_success"
    if success_fraction < 1.0:
        return "near_stable_partial_success"
    if unique_success_selection_count == 1:
        return "full_success_single_selection"
    if dominant_fraction >= CONSENSUS_FRACTION_THRESHOLD:
        return "full_success_dominant_consensus"
    return "full_success_multi_selection"


def case_stability_rows(selected_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in selected_rows:
        grouped[str(row.get("case_label", ""))].append(row)

    outputs = []
    for case_label, rows in grouped.items():
        first = rows[0]
        variant_count = len(rows)
        success_rows = [row for row in rows if parse_bool(row.get("all_target_slots_hit"))]
        success_count = len(success_rows)
        failed_count = variant_count - success_count
        success_fraction = success_count / variant_count if variant_count else 0.0
        success_selection_counts = Counter(row.get("selected_x_values_mm", "") for row in success_rows)
        all_selection_counts = Counter(row.get("selected_x_values_mm", "") for row in rows)
        dominant_selection, dominant_count = (
            success_selection_counts.most_common(1)[0] if success_selection_counts else ("", 0)
        )
        dominant_fraction_of_success = dominant_count / success_count if success_count else 0.0
        dominant_fraction_of_all = dominant_count / variant_count if variant_count else 0.0
        outputs.append(
            {
                "case_label": case_label,
                "branch_key": first.get("branch_key", ""),
                "seed": safe_int(first.get("seed"), 0),
                "case_variant": first.get("case_variant", ""),
                "variant_count": variant_count,
                "all_target_slot_variant_count": success_count,
                "failed_variant_count": failed_count,
                "success_fraction": success_fraction,
                "unique_success_selection_count": len(success_selection_counts),
                "unique_all_selection_count": len(all_selection_counts),
                "dominant_success_selection": dominant_selection,
                "dominant_success_selection_count": dominant_count,
                "dominant_success_fraction_of_success": dominant_fraction_of_success,
                "dominant_success_fraction_of_all": dominant_fraction_of_all,
                "max_target_slot_abs_error_median_mm": float(
                    np.median([safe_float(row.get("max_target_slot_abs_error_mm"), math.nan) for row in success_rows])
                )
                if success_rows
                else math.nan,
                "stability_label": stability_label(
                    success_fraction,
                    len(success_selection_counts),
                    dominant_fraction_of_success,
                ),
            }
        )
    return sorted(outputs, key=case_sort_key)


def branch_stability_rows(case_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in case_rows:
        grouped[str(row.get("branch_key", ""))].append(row)
    outputs = []
    for branch_key, rows in grouped.items():
        outputs.append(
            {
                "branch_key": branch_key,
                "case_count": len(rows),
                "all_variant_success_case_count": sum(safe_float(row["success_fraction"], 0.0) == 1.0 for row in rows),
                "partial_success_case_count": sum(safe_float(row["success_fraction"], 0.0) < 1.0 for row in rows),
                "tuning_sensitive_case_count": sum(
                    row["stability_label"] == "tuning_sensitive_partial_success" for row in rows
                ),
                "min_success_fraction": min([safe_float(row["success_fraction"], 0.0) for row in rows] or [0.0]),
                "median_success_fraction": float(np.median([safe_float(row["success_fraction"], 0.0) for row in rows]))
                if rows
                else 0.0,
                "max_unique_success_selection_count": max(
                    [safe_int(row["unique_success_selection_count"], 0) for row in rows] or [0]
                ),
            }
        )
    return sorted(outputs, key=lambda row: row["branch_key"])


def summarize_stability(
    case_rows: list[dict],
    branch_rows: list[dict],
    source_summary: dict,
    robustness_summary: dict,
) -> dict:
    case_count = len(case_rows)
    success_fractions = [safe_float(row["success_fraction"], 0.0) for row in case_rows]
    all_variant_cases = sum(value == 1.0 for value in success_fractions)
    partial_cases = case_count - all_variant_cases
    tuning_sensitive_cases = [
        row for row in case_rows if row["stability_label"] == "tuning_sensitive_partial_success"
    ]
    consensus_cases = sum(safe_int(row["unique_success_selection_count"], 0) == 1 for row in case_rows)
    return {
        "policy_label": "local_2d_detector_blind_envelope_policy_stability_cpu_no_fwi",
        "source_policy_label": source_summary.get("policy_label", ""),
        "robustness_policy_label": robustness_summary.get("policy_label", ""),
        "case_count": case_count,
        "variant_count": safe_int(source_summary.get("variant_count"), 0),
        "all_variant_success_case_count": all_variant_cases,
        "partial_success_case_count": partial_cases,
        "tuning_sensitive_case_count": len(tuning_sensitive_cases),
        "consensus_single_selection_case_count": consensus_cases,
        "multi_selection_case_count": case_count - consensus_cases,
        "min_success_fraction": min(success_fractions) if success_fractions else 0.0,
        "median_success_fraction": float(np.median(success_fractions)) if success_fractions else 0.0,
        "min_dominant_success_fraction_of_all": min(
            [safe_float(row["dominant_success_fraction_of_all"], 0.0) for row in case_rows] or [0.0]
        ),
        "max_unique_success_selection_count": max(
            [safe_int(row["unique_success_selection_count"], 0) for row in case_rows] or [0]
        ),
        "tuning_sensitive_case_labels": ";".join(row["case_label"] for row in tuning_sensitive_cases),
        "tuning_sensitive_branch_keys": ";".join(sorted({str(row["branch_key"]) for row in tuning_sensitive_cases})),
        "close50_partial_success_case_count": sum(
            row.get("branch_key") == "target2_close50_linear29p5"
            and safe_float(row.get("success_fraction"), 0.0) < 1.0
            for row in case_rows
        ),
        "close14_partial_success_case_count": sum(
            row.get("branch_key") == "target2_close14"
            and safe_float(row.get("success_fraction"), 0.0) < 1.0
            for row in case_rows
        ),
        "robustness_boundary": robustness_summary.get("robustness_boundary", ""),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Most saved cases are stable under the entire blind-envelope policy grid, but two close50 nominal "
            "cases are policy-sensitive. This strengthens the manuscript detector handoff by separating stable "
            "seed/condition evidence from the close50 branch-family stability limit; it does not justify "
            "detector-seeded FWI."
        ),
    }


def plot_stability(case_rows: list[dict], branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["case_label"].replace("|", "\n") for row in case_rows]
    success = [safe_float(row["success_fraction"], 0.0) for row in case_rows]
    unique = [safe_int(row["unique_success_selection_count"], 0) for row in case_rows]

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)
    colors = ["#e15759" if value < FRAGILE_SUCCESS_FRACTION_THRESHOLD else "#59a14f" for value in success]
    axes[0].bar(np.arange(len(labels)), success, color=colors)
    axes[0].axhline(FRAGILE_SUCCESS_FRACTION_THRESHOLD, color="#f28e2b", linestyle="--", linewidth=1.0)
    axes[0].set_xticks(np.arange(len(labels)), labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylim(0, 1.05)
    axes[0].set_ylabel("successful variant fraction")
    axes[0].set_title("Case stability across blind-envelope grid")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(np.arange(len(labels)), unique, color="#4e79a7")
    axes[1].set_xticks(np.arange(len(labels)), labels, rotation=45, ha="right", fontsize=7)
    axes[1].set_ylabel("unique successful selections")
    axes[1].set_title("Selection multiplicity")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.96,
        f"all-variant cases: {summary['all_variant_success_case_count']}/{summary['case_count']}\n"
        f"tuning-sensitive: {summary['tuning_sensitive_case_count']}\n"
        f"min success fraction: {summary['min_success_fraction']:.3f}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D blind-envelope detector policy stability", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, case_csv: Path, branch_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_blind_envelope_policy_stability.png`",
                "",
                "This CPU-only figure audits how stable the blind-envelope detector",
                "assignment is across the saved 288-policy grid.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"All-variant success cases: `{summary['all_variant_success_case_count']}`.",
                f"Partial-success cases: `{summary['partial_success_case_count']}`.",
                f"Tuning-sensitive cases: `{summary['tuning_sensitive_case_count']}`.",
                f"Minimum success fraction: `{summary['min_success_fraction']}`.",
                f"Tuning-sensitive case labels: `{summary['tuning_sensitive_case_labels']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case stability rows: `{case_csv.name}`.",
                f"- Branch stability rows: `{branch_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved blind-envelope selected-case rows only. It does",
                "not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or",
                "neural-network training.",
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
    parser.add_argument("--robustness-run", default=DEFAULT_ROBUSTNESS_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_blind_envelope_policy_stability")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    source_dir = summary_root / args.blind_envelope_run
    robustness_dir = summary_root / args.robustness_run

    source_summary = read_json(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
    )
    robustness_summary = read_json(
        robustness_dir / "data/local_2d_detector_blind_envelope_robustness_summary.json"
    )
    selected_rows = read_csv_rows(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
    )

    case_rows = case_stability_rows(selected_rows)
    branch_rows = branch_stability_rows(case_rows)
    summary = summarize_stability(case_rows, branch_rows, source_summary, robustness_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_blind_envelope_policy_stability_cases.csv"
    branch_csv = data_dir / "local_2d_detector_blind_envelope_policy_stability_branches.csv"
    summary_json = data_dir / "local_2d_detector_blind_envelope_policy_stability_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_blind_envelope_policy_stability.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(case_csv, [json_safe(row) for row in case_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    plot_stability(case_rows, branch_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, case_csv, branch_csv)
    summary["paths"] = {
        "case_stability_csv": str(case_csv),
        "branch_stability_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "source_blind_envelope_summary_json": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
        ),
        "source_blind_envelope_selected_cases_csv": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
        ),
        "source_robustness_summary_json": str(
            robustness_dir / "data/local_2d_detector_blind_envelope_robustness_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_blind_envelope_policy_stability",
        {
            "blind_envelope_run": args.blind_envelope_run,
            "robustness_run": args.robustness_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
