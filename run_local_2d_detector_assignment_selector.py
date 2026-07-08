#!/usr/bin/env python3
"""Evaluate truth-free detector assignment selectors over saved policy rows."""

from __future__ import annotations

import argparse
import csv
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
from run_local_2d_detector_assignment_failure_taxonomy import (  # noqa: E402
    failure_label,
    parse_bool,
    parse_float_list,
    parse_int_list,
)
from run_local_2d_detector_baseline_synthesis import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ASSIGNMENT_RUN = "023_local_2d_detector_blind_assignment_policy_with_span_bonus"
DEFAULT_ORACLE_RUN = "025_local_2d_detector_assignment_failure_taxonomy_policy_oracle"
CASE_FIELDS = ("branch_key", "seed", "case_variant", "run_name")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def case_key(row: dict) -> tuple[str, str, str, str]:
    return tuple(str(row[field]) for field in CASE_FIELDS)


def case_label(row: dict) -> str:
    branch, seed, variant, _run_name = case_key(row)
    return f"{branch}|seed{seed}|{variant}"


def enrich_row(row: dict) -> dict:
    xs = parse_float_list(row.get("assigned_x_values_mm"))
    zs = parse_float_list(row.get("assigned_z_values_mm"))
    ranks = parse_int_list(row.get("assigned_detection_ranks"))
    gaps = [right - left for left, right in zip(sorted(xs)[:-1], sorted(xs)[1:])]
    out = dict(row)
    out["case_label"] = case_label(row)
    out["assigned_candidate_count_numeric"] = int(safe_float(row.get("assigned_candidate_count"), 0.0))
    out["assigned_x_span_mm_numeric"] = (max(xs) - min(xs)) if xs else math.nan
    out["assigned_x_center_mm_numeric"] = float(np.mean(xs)) if xs else math.nan
    out["assigned_min_x_gap_mm_numeric"] = min(gaps) if gaps else math.nan
    out["assigned_gap_imbalance_mm_numeric"] = abs(gaps[1] - gaps[0]) if len(gaps) >= 2 else math.nan
    out["assigned_z_std_mm_numeric"] = float(np.std(zs)) if zs else math.nan
    out["rank_sum_numeric"] = sum(ranks) if ranks else 10_000
    out["max_rank_numeric"] = max(ranks) if ranks else 10_000
    out["candidate_budget_numeric"] = int(safe_float(row.get("candidate_budget"), 0.0))
    out["top_k_numeric"] = int(safe_float(row.get("top_k"), 0.0))
    out["unique_truth_hit_count_numeric"] = int(safe_float(row.get("unique_truth_hit_count"), 0.0))
    out["unique_all_truths_bool"] = parse_bool(row.get("unique_all_truths_within_tolerance"))
    out["unique_target0_bool"] = parse_bool(row.get("unique_target0_hit"))
    out["unique_target1_bool"] = parse_bool(row.get("unique_target1_hit"))
    out["unique_target2_bool"] = parse_bool(row.get("unique_target2_hit"))
    return out


def selector_grid() -> list[dict]:
    selectors = [
        {
            "selector_label": "lowest_max_rank",
            "rank_sum_weight": 0.2,
            "max_rank_weight": 2.0,
            "span_width_bonus": 0.0,
            "span_target_mm": None,
            "span_target_weight": 0.0,
            "center_target_mm": 250.0,
            "center_weight": 0.0,
            "gap_imbalance_weight": 0.0,
            "z_std_weight": 0.0,
            "budget_penalty": 0.02,
        },
        {
            "selector_label": "lowest_rank_sum",
            "rank_sum_weight": 1.0,
            "max_rank_weight": 0.5,
            "span_width_bonus": 0.0,
            "span_target_mm": None,
            "span_target_weight": 0.0,
            "center_target_mm": 250.0,
            "center_weight": 0.0,
            "gap_imbalance_weight": 0.0,
            "z_std_weight": 0.0,
            "budget_penalty": 0.02,
        },
        {
            "selector_label": "widest_span_rank_lite",
            "rank_sum_weight": 0.15,
            "max_rank_weight": 0.3,
            "span_width_bonus": 1.0,
            "span_target_mm": None,
            "span_target_weight": 0.0,
            "center_target_mm": 250.0,
            "center_weight": 0.02,
            "gap_imbalance_weight": 0.0,
            "z_std_weight": 0.0,
            "budget_penalty": 0.02,
        },
        {
            "selector_label": "balanced_span_rank",
            "rank_sum_weight": 0.35,
            "max_rank_weight": 0.7,
            "span_width_bonus": 0.45,
            "span_target_mm": None,
            "span_target_weight": 0.0,
            "center_target_mm": 250.0,
            "center_weight": 0.05,
            "gap_imbalance_weight": 0.03,
            "z_std_weight": 0.02,
            "budget_penalty": 0.02,
        },
    ]
    rank_profiles = (
        ("rank_lite", 0.2, 0.4),
        ("rank_medium", 0.45, 0.9),
    )
    for target in (70.0, 75.0, 80.0, 85.0, 90.0, 100.0, 110.0, 115.0, 120.0):
        for span_weight in (0.5, 1.0, 2.0):
            for rank_name, rank_sum_weight, max_rank_weight in rank_profiles:
                for center_weight in (0.0, 0.06):
                    for gap_weight in (0.0, 0.06):
                        selectors.append({
                            "selector_label": (
                                f"span_target{target:g}_w{span_weight:g}_{rank_name}"
                                f"_center{center_weight:g}_gap{gap_weight:g}"
                            ),
                            "rank_sum_weight": rank_sum_weight,
                            "max_rank_weight": max_rank_weight,
                            "span_width_bonus": 0.0,
                            "span_target_mm": target,
                            "span_target_weight": span_weight,
                            "center_target_mm": 250.0,
                            "center_weight": center_weight,
                            "gap_imbalance_weight": gap_weight,
                            "z_std_weight": 0.02,
                            "budget_penalty": 0.02,
                        })
    return selectors


def finite_or(value: float, fallback: float) -> float:
    return float(value) if math.isfinite(float(value)) else float(fallback)


def selector_score(row: dict, selector: dict) -> float:
    assigned_count = int(row["assigned_candidate_count_numeric"])
    if row.get("assignment_status") != "assigned" or assigned_count <= 0:
        return -1.0e12 + assigned_count
    span = finite_or(row["assigned_x_span_mm_numeric"], 0.0)
    center = finite_or(row["assigned_x_center_mm_numeric"], 250.0)
    gap_imbalance = finite_or(row["assigned_gap_imbalance_mm_numeric"], 200.0)
    z_std = finite_or(row["assigned_z_std_mm_numeric"], 200.0)
    score = 1000.0 + 100.0 * assigned_count
    score -= float(selector["rank_sum_weight"]) * float(row["rank_sum_numeric"])
    score -= float(selector["max_rank_weight"]) * float(row["max_rank_numeric"])
    score += float(selector["span_width_bonus"]) * span
    if selector.get("span_target_mm") is not None:
        score -= float(selector["span_target_weight"]) * abs(span - float(selector["span_target_mm"]))
    score -= float(selector["center_weight"]) * abs(center - float(selector["center_target_mm"]))
    score -= float(selector["gap_imbalance_weight"]) * gap_imbalance
    score -= float(selector["z_std_weight"]) * z_std
    score -= float(selector["budget_penalty"]) * float(row["candidate_budget_numeric"])
    return score


def select_rows_for_selector(rows: list[dict], selector: dict) -> list[dict]:
    selected = []
    for key in sorted({case_key(row) for row in rows}):
        case_rows = [row for row in rows if case_key(row) == key]
        best = max(
            case_rows,
            key=lambda row: (
                selector_score(row, selector),
                int(row["assigned_candidate_count_numeric"]),
                -int(row["max_rank_numeric"]),
                -int(row["rank_sum_numeric"]),
                -int(row["candidate_budget_numeric"]),
                str(row["config_key"]),
                str(row["assignment_policy_key"]),
            ),
        )
        out = dict(best)
        out["selector_label"] = selector["selector_label"]
        out["selector_score"] = selector_score(best, selector)
        out["failure_label"] = failure_label(best)
        selected.append(out)
    return selected


def summarize_selected(selector: dict, selected_rows: list[dict]) -> dict:
    labels = Counter(row["failure_label"] for row in selected_rows)
    return {
        "selector_label": selector["selector_label"],
        "case_count": len(selected_rows),
        "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in selected_rows),
        "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in selected_rows),
        "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in selected_rows),
        "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in selected_rows),
        "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count_numeric"] for row in selected_rows])),
        "dominant_failure_label": labels.most_common(1)[0][0] if labels else "",
        "rank_sum_weight": selector["rank_sum_weight"],
        "max_rank_weight": selector["max_rank_weight"],
        "span_width_bonus": selector["span_width_bonus"],
        "span_target_mm": selector["span_target_mm"],
        "span_target_weight": selector["span_target_weight"],
        "center_weight": selector["center_weight"],
        "gap_imbalance_weight": selector["gap_imbalance_weight"],
        "z_std_weight": selector["z_std_weight"],
    }


def sort_selector_summaries(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -int(row["all_truth_case_count"]),
            -float(row["mean_unique_truth_hit_count"]),
            -int(row["target0_hit_count"]),
            -int(row["target2_hit_count"]),
            str(row["selector_label"]),
        ),
    )


def best_selector_for_cases(
    selector_summaries: dict[str, dict],
    selected_by_selector: dict[str, list[dict]],
    train_case_keys: set[tuple[str, str, str, str]],
) -> str:
    train_summaries = []
    selector_by_label = {summary["selector_label"]: summary for summary in selector_summaries.values()}
    for label, selected in selected_by_selector.items():
        train_rows = [row for row in selected if case_key(row) in train_case_keys]
        selector_stub = selector_by_label[label]
        train_summaries.append(summarize_selected(selector_stub, train_rows))
    return sort_selector_summaries(train_summaries)[0]["selector_label"]


def cross_validate(
    selector_summaries: dict[str, dict],
    selected_by_selector: dict[str, list[dict]],
    strategy: str,
) -> tuple[dict, list[dict]]:
    all_keys = sorted({case_key(row) for rows in selected_by_selector.values() for row in rows})
    if strategy == "leave_one_case":
        splits = [(case[3], {case}) for case in all_keys]
    elif strategy == "leave_one_seed":
        seeds = sorted({case[1] for case in all_keys}, key=lambda value: int(value))
        splits = [(f"seed{seed}", {case for case in all_keys if case[1] == seed}) for seed in seeds]
    elif strategy == "leave_one_branch":
        branches = sorted({case[0] for case in all_keys})
        splits = [(branch, {case for case in all_keys if case[0] == branch}) for branch in branches]
    else:
        raise ValueError(f"unknown cross-validation strategy: {strategy}")

    cv_rows = []
    for holdout_label, test_keys in splits:
        train_keys = set(all_keys) - set(test_keys)
        selected_label = best_selector_for_cases(selector_summaries, selected_by_selector, train_keys)
        selected_lookup = {case_key(row): row for row in selected_by_selector[selected_label]}
        for key in sorted(test_keys):
            row = dict(selected_lookup[key])
            row["cv_strategy"] = strategy
            row["holdout_label"] = holdout_label
            row["trained_selector_label"] = selected_label
            cv_rows.append(row)

    labels = Counter(row["failure_label"] for row in cv_rows)
    summary = {
        "cv_strategy": strategy,
        "case_count": len(cv_rows),
        "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in cv_rows),
        "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in cv_rows),
        "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in cv_rows),
        "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in cv_rows),
        "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count_numeric"] for row in cv_rows])),
        "selected_selector_count": len({row["trained_selector_label"] for row in cv_rows}),
        "dominant_failure_label": labels.most_common(1)[0][0] if labels else "",
    }
    return summary, cv_rows


def branch_summary(selected_rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in selected_rows}):
        rows = [row for row in selected_rows if row["branch_key"] == branch]
        out.append({
            "branch_key": branch,
            "case_count": len(rows),
            "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in rows),
            "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in rows),
            "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in rows),
            "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in rows),
            "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count_numeric"] for row in rows])),
        })
    return out


def plot_selector(summary: dict, branch_rows: list[dict], save_path: Path) -> str:
    labels = ["shared\npolicy", "best\nselector", "case\nCV", "seed\nCV", "branch\nCV", "policy\noracle"]
    values = [
        summary["shared_policy_all_truth_case_count"],
        summary["best_in_sample_all_truth_case_count"],
        summary["leave_one_case_all_truth_case_count"],
        summary["leave_one_seed_all_truth_case_count"],
        summary["leave_one_branch_all_truth_case_count"],
        summary["oracle_all_truth_case_count"],
    ]
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.2), constrained_layout=True)
    axes[0].bar(np.arange(len(labels)), values, color=["#bab0ab", "#4e79a7", "#59a14f", "#76b7b2", "#f28e2b", "#9c755f"])
    axes[0].set_xticks(np.arange(len(labels)), labels, fontsize=8)
    axes[0].set_ylabel("all-truth cases")
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_title("Truth-free selector versus oracle")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    branches = [row["branch_key"] for row in branch_rows]
    branch_values = [row["all_truth_case_count"] for row in branch_rows]
    axes[1].bar(np.arange(len(branches)), branch_values, color="#4e79a7", width=0.58)
    axes[1].set_xticks(np.arange(len(branches)), [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[1].set_ylim(0, max([row["case_count"] for row in branch_rows] + [1]) + 1)
    axes[1].set_title("Best selector by branch")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector assignment selector audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_assignment_selector.png`",
                "",
                "This figure compares truth-free selector heuristics against the fixed",
                "shared blind-assignment policy and the per-case policy oracle. It reads",
                "saved assignment rows only and does not rerun FDTD, FWI, GPU kernels,",
                "field FWI, or 3D/HPC work.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Selector candidates: `{summary['selector_candidate_count']}`.",
                f"Best in-sample selector: `{summary['best_in_sample_selector_label']}`.",
                f"Best in-sample all-truth cases: `{summary['best_in_sample_all_truth_case_count']}`.",
                f"Leave-one-case all-truth cases: `{summary['leave_one_case_all_truth_case_count']}`.",
                f"Shared-policy all-truth cases: `{summary['shared_policy_all_truth_case_count']}`.",
                f"Per-case oracle all-truth cases: `{summary['oracle_all_truth_case_count']}`.",
                f"GPU used: `{summary['gpu_used']}`.",
                "",
                summary["decision"],
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--assignment-run", default=DEFAULT_ASSIGNMENT_RUN)
    parser.add_argument("--oracle-run", default=DEFAULT_ORACLE_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_assignment_selector")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    assignment_dir = Path(args.summary_root) / args.assignment_run
    assignment_rows = [
        enrich_row(row)
        for row in read_csv_rows(assignment_dir / "data/local_2d_detector_blind_assignment_policy_rows.csv")
    ]
    shared_summary = read_json(assignment_dir / "data/local_2d_detector_blind_assignment_policy_summary.json")
    oracle_summary = read_json(
        Path(args.summary_root) / args.oracle_run / "data/local_2d_detector_assignment_failure_taxonomy_summary.json"
    )
    selectors = selector_grid()
    selected_by_selector = {
        selector["selector_label"]: select_rows_for_selector(assignment_rows, selector)
        for selector in selectors
    }
    selector_summaries_by_label = {
        selector["selector_label"]: summarize_selected(selector, selected_by_selector[selector["selector_label"]])
        for selector in selectors
    }
    selector_summary = sort_selector_summaries(list(selector_summaries_by_label.values()))
    best_selector_label = selector_summary[0]["selector_label"]
    best_selected_rows = selected_by_selector[best_selector_label]
    best_branch_rows = branch_summary(best_selected_rows)

    cv_summaries = []
    cv_case_rows = []
    for strategy in ("leave_one_case", "leave_one_seed", "leave_one_branch"):
        cv_summary, rows = cross_validate(selector_summaries_by_label, selected_by_selector, strategy)
        cv_summaries.append(cv_summary)
        cv_case_rows.extend(rows)
    cv_by_strategy = {row["cv_strategy"]: row for row in cv_summaries}

    shared_all_truth = int(shared_summary.get("best_unique_all_truth_case_count", 0))
    oracle_all_truth = int(oracle_summary.get("oracle_all_truth_case_count", oracle_summary.get("all_truth_case_count", 0)))
    case_count = len({case_key(row) for row in assignment_rows})
    best_all_truth = int(selector_summary[0]["all_truth_case_count"])
    leave_one_case_all_truth = int(cv_by_strategy["leave_one_case"]["all_truth_case_count"])
    if leave_one_case_all_truth > shared_all_truth:
        decision = (
            "A truth-free feature selector improves on the fixed shared policy under leave-one-case validation, "
            "but it remains below the per-case policy oracle. This supports a narrow selector/objective-gate "
            "development path before detector-seeded FWI."
        )
    else:
        decision = (
            "The truth-free selector grid does not improve on the fixed shared policy under leave-one-case "
            "validation. The policy-oracle gap should be treated as evidence for missing selector features or "
            "the need for downstream objective gating, not as a ready detector-to-FWI initializer."
        )
    summary = {
        "policy_label": "local_2d_detector_assignment_selector_truth_free_feature_grid",
        "case_count": case_count,
        "assignment_row_count": len(assignment_rows),
        "selector_candidate_count": len(selectors),
        "best_in_sample_selector_label": best_selector_label,
        "best_in_sample_all_truth_case_count": best_all_truth,
        "best_in_sample_mean_unique_truth_hit_count": selector_summary[0]["mean_unique_truth_hit_count"],
        "leave_one_case_all_truth_case_count": leave_one_case_all_truth,
        "leave_one_case_mean_unique_truth_hit_count": cv_by_strategy["leave_one_case"]["mean_unique_truth_hit_count"],
        "leave_one_seed_all_truth_case_count": int(cv_by_strategy["leave_one_seed"]["all_truth_case_count"]),
        "leave_one_seed_mean_unique_truth_hit_count": cv_by_strategy["leave_one_seed"]["mean_unique_truth_hit_count"],
        "leave_one_branch_all_truth_case_count": int(cv_by_strategy["leave_one_branch"]["all_truth_case_count"]),
        "leave_one_branch_mean_unique_truth_hit_count": cv_by_strategy["leave_one_branch"]["mean_unique_truth_hit_count"],
        "shared_policy_all_truth_case_count": shared_all_truth,
        "shared_policy_mean_unique_truth_hit_count": shared_summary.get("best_mean_unique_truth_hit_count"),
        "oracle_all_truth_case_count": oracle_all_truth,
        "oracle_mean_unique_truth_hit_count": oracle_summary.get("mean_unique_truth_hit_count"),
        "source_assignment_run": args.assignment_run,
        "source_oracle_run": args.oracle_run,
        "gpu_used": False,
        "backend": "saved_assignment_rows_cpu_selector_grid",
        "decision": decision,
    }

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    selector_csv = data_dir / "local_2d_detector_assignment_selector_summary.csv"
    best_cases_csv = data_dir / "local_2d_detector_assignment_selector_best_cases.csv"
    best_branch_csv = data_dir / "local_2d_detector_assignment_selector_branch_summary.csv"
    cv_summary_csv = data_dir / "local_2d_detector_assignment_selector_cv_summary.csv"
    cv_cases_csv = data_dir / "local_2d_detector_assignment_selector_cv_cases.csv"
    summary_json = data_dir / "local_2d_detector_assignment_selector_summary.json"
    figure_path = figures_dir / "local_2d_detector_assignment_selector.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(selector_csv, [json_safe(row) for row in selector_summary])
    write_csv(best_cases_csv, [json_safe(row) for row in best_selected_rows])
    write_csv(best_branch_csv, [json_safe(row) for row in best_branch_rows])
    write_csv(cv_summary_csv, [json_safe(row) for row in cv_summaries])
    write_csv(cv_cases_csv, [json_safe(row) for row in cv_case_rows])
    plot_selector(summary, best_branch_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "selector_csv": str(selector_csv),
        "best_cases_csv": str(best_cases_csv),
        "best_branch_csv": str(best_branch_csv),
        "cv_summary_csv": str(cv_summary_csv),
        "cv_cases_csv": str(cv_cases_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_assignment_selector",
        {
            "assignment_run": args.assignment_run,
            "oracle_run": args.oracle_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
