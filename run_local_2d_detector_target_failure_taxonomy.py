#!/usr/bin/env python3
"""Summarize target-level failure modes for the local 2D detector selector."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter
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
from run_local_2d_detector_rank_budget_diagnostic import read_csv_rows, read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SELECTOR_GAP_RUN = "045_local_2d_detector_selector_gap_decomposition"
TARGETS = ("target0", "target1", "target2")


def boolish(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def missing_targets(label: str) -> list[str]:
    if not label or label == "all_truth":
        return []
    return [target for target in TARGETS if target in label]


def target_failure_scope(missing: list[str], selected_all_truth: bool) -> str:
    if selected_all_truth:
        return "selected_truth"
    if not missing:
        return "unclassified_failure"
    if len(missing) == 1:
        return "single_target_missing"
    return "multi_target_missing"


def build_target_failure_rows(gap_rows: list[dict]) -> list[dict]:
    rows = []
    for raw in gap_rows:
        selected_all_truth = boolish(raw.get("selected_all_truth"))
        missing = missing_targets(str(raw.get("selected_failure_label", "")))
        rows.append(
            {
                "case_label": raw.get("case_label", ""),
                "branch_key": raw.get("branch_key", ""),
                "seed": safe_int(raw.get("seed")),
                "case_variant": raw.get("case_variant", ""),
                "selected_all_truth": selected_all_truth,
                "selected_failure_label": raw.get("selected_failure_label", ""),
                "target_failure_scope": target_failure_scope(missing, selected_all_truth),
                "missing_target_count": len(missing),
                "missing_target0": "target0" in missing,
                "missing_target1": "target1" in missing,
                "missing_target2": "target2" in missing,
                "selected_unique_truth_hit_count": safe_int(raw.get("selected_unique_truth_hit_count")),
                "best_truth_unique_truth_hit_count": safe_int(raw.get("best_truth_unique_truth_hit_count")),
                "all_truth_triple_count": safe_int(raw.get("all_truth_triple_count")),
                "required_selector_gain_to_choose_truth": safe_float(
                    raw.get("required_selector_gain_to_choose_truth"), 0.0
                ),
                "dominant_loss_feature": raw.get("dominant_loss_feature", ""),
                "selected_candidate_ranks": raw.get("selected_candidate_ranks", ""),
                "selected_candidate_x_values_mm": raw.get("selected_candidate_x_values_mm", ""),
                "selected_candidate_z_values_mm": raw.get("selected_candidate_z_values_mm", ""),
                "best_truth_candidate_ranks": raw.get("best_truth_candidate_ranks", ""),
                "best_truth_candidate_x_values_mm": raw.get("best_truth_candidate_x_values_mm", ""),
                "best_truth_candidate_z_values_mm": raw.get("best_truth_candidate_z_values_mm", ""),
            }
        )
    return rows


def summarize_branches(rows: list[dict]) -> list[dict]:
    branch_rows = []
    for branch in sorted({row["branch_key"] for row in rows}):
        current = [row for row in rows if row["branch_key"] == branch]
        failed = [row for row in current if not row["selected_all_truth"]]
        miss_counts = {target: sum(bool(row[f"missing_{target}"]) for row in failed) for target in TARGETS}
        dominant_missing = max(miss_counts.items(), key=lambda item: (item[1], item[0]))[0] if failed else "none"
        required = [
            safe_float(row["required_selector_gain_to_choose_truth"])
            for row in failed
            if math.isfinite(safe_float(row["required_selector_gain_to_choose_truth"]))
        ]
        branch_rows.append(
            {
                "branch_key": branch,
                "case_count": len(current),
                "selected_all_truth_case_count": sum(row["selected_all_truth"] for row in current),
                "failed_selector_case_count": len(failed),
                "single_target_missing_case_count": sum(
                    row["target_failure_scope"] == "single_target_missing" for row in failed
                ),
                "multi_target_missing_case_count": sum(
                    row["target_failure_scope"] == "multi_target_missing" for row in failed
                ),
                "missing_target0_case_count": miss_counts["target0"],
                "missing_target1_case_count": miss_counts["target1"],
                "missing_target2_case_count": miss_counts["target2"],
                "dominant_missing_target": dominant_missing,
                "median_required_selector_gain_to_choose_truth": float(np.median(required)) if required else 0.0,
                "max_required_selector_gain_to_choose_truth": float(max(required)) if required else 0.0,
            }
        )
    return branch_rows


def summarize_target_failures(rows: list[dict], branch_rows: list[dict], source_summary: dict | None = None) -> dict:
    source_summary = source_summary or {}
    failed = [row for row in rows if not row["selected_all_truth"]]
    miss_counts = {target: sum(bool(row[f"missing_{target}"]) for row in failed) for target in TARGETS}
    dominant_missing = max(miss_counts.items(), key=lambda item: (item[1], item[0]))[0] if failed else "none"
    target1_required = [
        safe_float(row["required_selector_gain_to_choose_truth"])
        for row in failed
        if row["missing_target1"] and math.isfinite(safe_float(row["required_selector_gain_to_choose_truth"]))
    ]
    return {
        "policy_label": "local_2d_detector_target_failure_taxonomy_cpu_no_fwi",
        "source_gap_policy_label": source_summary.get("policy_label", ""),
        "case_count": len(rows),
        "selected_all_truth_case_count": sum(row["selected_all_truth"] for row in rows),
        "failed_selector_case_count": len(failed),
        "best_truth_available_case_count": sum(safe_int(row["all_truth_triple_count"]) > 0 for row in rows),
        "single_target_missing_case_count": sum(
            row["target_failure_scope"] == "single_target_missing" for row in failed
        ),
        "multi_target_missing_case_count": sum(
            row["target_failure_scope"] == "multi_target_missing" for row in failed
        ),
        "missing_target0_case_count": miss_counts["target0"],
        "missing_target1_case_count": miss_counts["target1"],
        "missing_target2_case_count": miss_counts["target2"],
        "dominant_missing_target": dominant_missing,
        "target1_missing_median_required_selector_gain": float(np.median(target1_required))
        if target1_required
        else 0.0,
        "target1_missing_max_required_selector_gain": float(max(target1_required)) if target1_required else 0.0,
        "close14_failed_selector_case_count": next(
            (row["failed_selector_case_count"] for row in branch_rows if row["branch_key"] == "target2_close14"),
            0,
        ),
        "close50_failed_selector_case_count": next(
            (
                row["failed_selector_case_count"]
                for row in branch_rows
                if row["branch_key"] == "target2_close50_linear29p5"
            ),
            0,
        ),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "next_selector_hypothesis": (
            "A stronger detector handoff should enforce target-coverage or target-conditioned waveform evidence; "
            "scalar signed-gap/score reweighting is insufficient because the dominant practical failure is dropping "
            "target1 and often multiple targets despite an all-truth triple being available."
        ),
        "decision": (
            "Use this taxonomy as CPU-only detector failure analysis. It sharpens the next synthetic 2D modeling "
            "direction but does not justify detector-seeded FWI."
        ),
    }


def plot_target_failures(summary: dict, branch_rows: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)

    target_labels = ["target0", "target1", "target2"]
    target_counts = [summary[f"missing_{target}_case_count"] for target in target_labels]
    axes[0].bar(np.arange(len(target_labels)), target_counts, color=["#6b9ac4", "#d95f59", "#63a866"])
    axes[0].set_xticks(np.arange(len(target_labels)), target_labels)
    axes[0].set_ylim(0, max(target_counts + [1]) + 1)
    axes[0].set_ylabel("failed cases")
    axes[0].set_title("Targets missing from selected wrong triples")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    branches = [row["branch_key"].replace("target2_", "").replace("_", "\n") for row in branch_rows]
    failed = [row["failed_selector_case_count"] for row in branch_rows]
    selected = [row["selected_all_truth_case_count"] for row in branch_rows]
    x = np.arange(len(branches))
    axes[1].bar(x, selected, color="#59a14f", label="selected all-truth")
    axes[1].bar(x, failed, bottom=selected, color="#e15759", label="selector failed")
    axes[1].set_xticks(x, branches, fontsize=8)
    axes[1].set_ylabel("cases")
    axes[1].set_title("Branch-level selector outcome")
    axes[1].legend(loc="upper right", fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.95,
        f"failed={summary['failed_selector_case_count']}/{summary['case_count']}\n"
        f"dominant missing={summary['dominant_missing_target']}\n"
        f"multi-target failures={summary['multi_target_missing_case_count']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector selector target-failure taxonomy", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, cases_csv: Path, branch_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_target_failure_taxonomy.png`",
                "",
                "This CPU-only figure summarizes which target locations are dropped by",
                "the current truth-free detector selector when the selected triple is wrong.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Failed selector cases: `{summary['failed_selector_case_count']}` of `{summary['case_count']}`.",
                f"Dominant missing target: `{summary['dominant_missing_target']}`.",
                f"Target1 missing cases: `{summary['missing_target1_case_count']}`.",
                f"Multi-target failure cases: `{summary['multi_target_missing_case_count']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case taxonomy: `{cases_csv.name}`.",
                f"- Branch taxonomy: `{branch_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads existing selector gap rows only. It does not run FDTD, FWI,",
                "GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--selector-gap-run", default=DEFAULT_SELECTOR_GAP_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_target_failure_taxonomy")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.summary_root) / args.selector_gap_run
    gap_rows = read_csv_rows(source_dir / "data/local_2d_detector_selector_gap_decomposition_cases.csv")
    source_summary = read_json(source_dir / "data/local_2d_detector_selector_gap_decomposition_summary.json")

    case_rows = build_target_failure_rows(gap_rows)
    branch_rows = summarize_branches(case_rows)
    summary = summarize_target_failures(case_rows, branch_rows, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    cases_csv = data_dir / "local_2d_detector_target_failure_taxonomy_cases.csv"
    branch_csv = data_dir / "local_2d_detector_target_failure_taxonomy_branch_summary.csv"
    summary_json = data_dir / "local_2d_detector_target_failure_taxonomy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_target_failure_taxonomy.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(cases_csv, [json_safe(row) for row in case_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    plot_target_failures(summary, branch_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, cases_csv, branch_csv)
    summary["paths"] = {
        "case_taxonomy_csv": str(cases_csv),
        "branch_summary_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "source_gap_summary_json": str(source_dir / "data/local_2d_detector_selector_gap_decomposition_summary.json"),
        "source_gap_cases_csv": str(source_dir / "data/local_2d_detector_selector_gap_decomposition_cases.csv"),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_target_failure_taxonomy",
        {
            "selector_gap_run": args.selector_gap_run,
            "source_gap_summary_json": str(
                source_dir / "data/local_2d_detector_selector_gap_decomposition_summary.json"
            ),
            "source_gap_cases_csv": str(source_dir / "data/local_2d_detector_selector_gap_decomposition_cases.csv"),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
