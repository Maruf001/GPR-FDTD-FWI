#!/usr/bin/env python3
"""Audit truth-vs-false separability in saved local 2D detector triples."""

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
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
CASE_FIELDS = ("branch_key", "seed", "case_variant", "run_name")
BUDGETS = (1, 3, 5, 10, 20, 50, 100, 200)
TARGET_FIELDS = ("unique_target0_hit", "unique_target1_hit", "unique_target2_hit")

SCORE_FEATURES = (
    "score_sum",
    "score_span_bonus",
    "score_min",
    "score_min_span",
    "score_balanced",
    "score_mask",
    "score_component_sum",
    "score_component_min",
    "score_component_mean_min",
    "score_component_floor_span",
    "score_component_balanced",
    "score_component_left_floor",
    "score_hybrid_span_component",
)

DERIVED_FEATURES = (
    "rank_sum_inverse",
    "max_rank_inverse",
    "x_span_width",
    "x_span_target70_inverse",
    "x_span_target80_inverse",
    "x_span_target90_inverse",
    "x_span_target110_inverse",
    "gap_balance_inverse",
    "center250_inverse",
)

FEATURES = SCORE_FEATURES + DERIVED_FEATURES


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_float_list(value) -> list[float]:
    if value in (None, ""):
        return []
    out = []
    for part in str(value).split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(float(part))
        except ValueError:
            continue
    return out


def parse_int_list(value) -> list[int]:
    return [int(round(item)) for item in parse_float_list(value)]


def case_key(row: dict) -> tuple[str, str, str, str]:
    return tuple(str(row[field]) for field in CASE_FIELDS)


def case_label(row: dict) -> str:
    return str(row.get("case_label") or f"{row['branch_key']}|seed{row['seed']}|{row['case_variant']}")


def target_hits(row: dict) -> tuple[bool, bool, bool]:
    return tuple(boolish(row.get(field)) for field in TARGET_FIELDS)


def truth_label(row: dict) -> bool:
    return boolish(row.get("unique_all_truths_within_tolerance"))


def rank_sum(row: dict) -> int:
    ranks = parse_int_list(row.get("candidate_ranks", ""))
    return sum(ranks) if ranks else 10_000


def max_rank(row: dict) -> int:
    ranks = parse_int_list(row.get("candidate_ranks", ""))
    return max(ranks) if ranks else 10_000


def x_values(row: dict) -> list[float]:
    return parse_float_list(row.get("candidate_x_values_mm", ""))


def x_center(row: dict) -> float:
    xs = x_values(row)
    return float(np.mean(xs)) if xs else math.nan


def x_span(row: dict) -> float:
    value = safe_float(row.get("x_span_mm"))
    if math.isfinite(value):
        return value
    xs = x_values(row)
    return max(xs) - min(xs) if xs else math.nan


def gap_balance(row: dict) -> float:
    value = safe_float(row.get("gap_balance_mm"))
    if math.isfinite(value):
        return value
    xs = sorted(x_values(row))
    if len(xs) < 3:
        return math.nan
    return abs((xs[2] - xs[1]) - (xs[1] - xs[0]))


def score_value(row: dict, feature: str) -> float:
    if feature in SCORE_FEATURES:
        return safe_float(row.get(feature), -math.inf)
    if feature == "rank_sum_inverse":
        return -float(rank_sum(row))
    if feature == "max_rank_inverse":
        return -float(max_rank(row))
    if feature == "x_span_width":
        return safe_float(x_span(row), -math.inf)
    if feature.startswith("x_span_target") and feature.endswith("_inverse"):
        target = safe_float(feature.removeprefix("x_span_target").removesuffix("_inverse"))
        span = x_span(row)
        return -abs(span - target) if math.isfinite(span) and math.isfinite(target) else -math.inf
    if feature == "gap_balance_inverse":
        value = gap_balance(row)
        return -value if math.isfinite(value) else -math.inf
    if feature == "center250_inverse":
        center = x_center(row)
        return -abs(center - 250.0) if math.isfinite(center) else -math.inf
    raise KeyError(feature)


def enriched_row(row: dict) -> dict:
    out = dict(row)
    out["case_label"] = case_label(row)
    out["rank_sum_numeric"] = rank_sum(row)
    out["max_rank_numeric"] = max_rank(row)
    out["x_span_mm_numeric"] = x_span(row)
    out["gap_balance_mm_numeric"] = gap_balance(row)
    out["x_center_mm_numeric"] = x_center(row)
    out["unique_all_truths_bool"] = truth_label(row)
    out["unique_target0_bool"], out["unique_target1_bool"], out["unique_target2_bool"] = target_hits(row)
    return out


def group_by_case(rows: list[dict]) -> dict[tuple[str, str, str, str], list[dict]]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[case_key(row)].append(row)
    return dict(grouped)


def ranked_rows(case_rows: list[dict], feature: str) -> list[dict]:
    return sorted(
        case_rows,
        key=lambda row: (
            score_value(row, feature),
            -safe_int(row.get("max_rank_numeric")),
            -safe_int(row.get("rank_sum_numeric")),
            str(row.get("candidate_x_values_mm", "")),
        ),
        reverse=True,
    )


def truth_ranks_for_feature(case_rows: list[dict], feature: str) -> list[int]:
    ranks = []
    for rank, row in enumerate(ranked_rows(case_rows, feature), start=1):
        if bool(row.get("unique_all_truths_bool", truth_label(row))):
            ranks.append(rank)
    return ranks


def best_truth_false_gap(case_rows: list[dict], feature: str) -> float:
    truth_scores = [score_value(row, feature) for row in case_rows if bool(row.get("unique_all_truths_bool", truth_label(row)))]
    false_scores = [score_value(row, feature) for row in case_rows if not bool(row.get("unique_all_truths_bool", truth_label(row)))]
    if not truth_scores or not false_scores:
        return math.nan
    return max(false_scores) - max(truth_scores)


def build_objective_case_rows(rows: list[dict], features: tuple[str, ...] = FEATURES) -> list[dict]:
    out = []
    for key, case_rows in sorted(group_by_case(rows).items()):
        first = case_rows[0]
        truth_count = sum(bool(row.get("unique_all_truths_bool", truth_label(row))) for row in case_rows)
        for feature in features:
            ordered = ranked_rows(case_rows, feature)
            top = ordered[0] if ordered else {}
            truth_ranks = truth_ranks_for_feature(case_rows, feature)
            first_truth_rank = float(truth_ranks[0]) if truth_ranks else math.inf
            out.append(
                {
                    "case_label": case_label(first),
                    "branch_key": key[0],
                    "seed": safe_int(key[1]),
                    "case_variant": key[2],
                    "run_name": key[3],
                    "feature": feature,
                    "candidate_triple_count": len(case_rows),
                    "all_truth_triple_count": truth_count,
                    "first_all_truth_rank": first_truth_rank,
                    "best_false_minus_best_truth_score_gap": best_truth_false_gap(case_rows, feature),
                    "top_unique_all_truths": bool(top.get("unique_all_truths_bool", truth_label(top))) if top else False,
                    "top_unique_truth_hit_count": safe_int(top.get("unique_truth_hit_count")),
                    "top_target0_hit": bool(top.get("unique_target0_bool", boolish(top.get("unique_target0_hit")))) if top else False,
                    "top_target1_hit": bool(top.get("unique_target1_bool", boolish(top.get("unique_target1_hit")))) if top else False,
                    "top_target2_hit": bool(top.get("unique_target2_bool", boolish(top.get("unique_target2_hit")))) if top else False,
                    "top_candidate_ranks": top.get("candidate_ranks", ""),
                    "top_candidate_x_values_mm": top.get("candidate_x_values_mm", ""),
                }
            )
    return out


def summarize_objectives(objective_case_rows: list[dict], features: tuple[str, ...] = FEATURES) -> list[dict]:
    grouped_by_feature: dict[str, list[dict]] = defaultdict(list)
    for row in objective_case_rows:
        grouped_by_feature[str(row["feature"])].append(row)

    out = []
    for feature in features:
        rows = grouped_by_feature.get(feature, [])
        ranks = [safe_float(row["first_all_truth_rank"], math.inf) for row in rows]
        finite_ranks = [rank for rank in ranks if math.isfinite(rank)]
        gaps = [safe_float(row["best_false_minus_best_truth_score_gap"]) for row in rows]
        finite_gaps = [gap for gap in gaps if math.isfinite(gap)]
        result = {
            "feature": feature,
            "case_count": len(rows),
            "top1_all_truth_case_count": sum(boolish(row["top_unique_all_truths"]) for row in rows),
            "top1_target0_hit_count": sum(boolish(row["top_target0_hit"]) for row in rows),
            "top1_target1_hit_count": sum(boolish(row["top_target1_hit"]) for row in rows),
            "top1_target2_hit_count": sum(boolish(row["top_target2_hit"]) for row in rows),
            "median_first_all_truth_rank": float(np.median(finite_ranks)) if finite_ranks else math.nan,
            "max_first_all_truth_rank": max(finite_ranks) if finite_ranks else math.nan,
            "median_false_minus_truth_score_gap": float(np.median(finite_gaps)) if finite_gaps else math.nan,
            "positive_gap_case_count": sum(gap > 0.0 for gap in finite_gaps),
        }
        for budget in BUDGETS:
            result[f"first_truth_top{budget}_case_count"] = sum(rank <= budget for rank in ranks)
        out.append(result)
    return sorted(out, key=objective_sort_key)


def objective_sort_key(row: dict) -> tuple:
    return (
        -safe_int(row.get("top1_all_truth_case_count")),
        -safe_int(row.get("first_truth_top10_case_count")),
        -safe_int(row.get("first_truth_top20_case_count")),
        -safe_int(row.get("first_truth_top50_case_count")),
        -safe_int(row.get("first_truth_top100_case_count")),
        safe_float(row.get("median_first_all_truth_rank"), math.inf),
        safe_float(row.get("max_first_all_truth_rank"), math.inf),
        str(row.get("feature", "")),
    )


def best_budget_row(objective_rows: list[dict], budget: int) -> dict:
    key = f"first_truth_top{budget}_case_count"
    return max(
        objective_rows,
        key=lambda row: (
            safe_int(row.get(key)),
            safe_int(row.get("top1_all_truth_case_count")),
            -safe_float(row.get("median_first_all_truth_rank"), math.inf),
        ),
    )


def minimal_all_case_budget(objective_rows: list[dict], case_count: int) -> tuple[int | None, str]:
    for budget in BUDGETS:
        rows = [
            row
            for row in objective_rows
            if safe_int(row.get(f"first_truth_top{budget}_case_count")) == case_count
        ]
        if rows:
            best = sorted(rows, key=objective_sort_key)[0]
            return budget, str(best["feature"])
    return None, ""


def best_feature_from_training_rows(training_rows: list[dict]) -> str:
    return str(summarize_objectives(training_rows)[0]["feature"])


def cv_splits(objective_case_rows: list[dict], strategy: str) -> list[tuple[str, set[tuple[str, str, str, str]]]]:
    keys = sorted(
        {
            (str(row["branch_key"]), str(row["seed"]), str(row["case_variant"]), str(row["run_name"]))
            for row in objective_case_rows
        }
    )
    if strategy == "leave_one_case":
        return [(key[3], {key}) for key in keys]
    if strategy == "leave_one_seed":
        seeds = sorted({key[1] for key in keys}, key=lambda value: int(value))
        return [(f"seed{seed}", {key for key in keys if key[1] == seed}) for seed in seeds]
    if strategy == "leave_one_branch":
        branches = sorted({key[0] for key in keys})
        return [(branch, {key for key in keys if key[0] == branch}) for branch in branches]
    raise ValueError(f"unknown strategy: {strategy}")


def cross_validate_objectives(objective_case_rows: list[dict], strategy: str) -> tuple[dict, list[dict]]:
    out_rows = []
    all_keys = {
        (str(row["branch_key"]), str(row["seed"]), str(row["case_variant"]), str(row["run_name"]))
        for row in objective_case_rows
    }
    for holdout_label, test_keys in cv_splits(objective_case_rows, strategy):
        train_keys = all_keys - test_keys
        train_rows = [
            row
            for row in objective_case_rows
            if (str(row["branch_key"]), str(row["seed"]), str(row["case_variant"]), str(row["run_name"])) in train_keys
        ]
        selected_feature = best_feature_from_training_rows(train_rows)
        for row in objective_case_rows:
            key = (str(row["branch_key"]), str(row["seed"]), str(row["case_variant"]), str(row["run_name"]))
            if key in test_keys and row["feature"] == selected_feature:
                out = dict(row)
                out["cv_strategy"] = strategy
                out["holdout_label"] = holdout_label
                out["trained_feature"] = selected_feature
                out_rows.append(out)

    ranks = [safe_float(row["first_all_truth_rank"], math.inf) for row in out_rows]
    labels = Counter(row["trained_feature"] for row in out_rows)
    summary = {
        "cv_strategy": strategy,
        "case_count": len(out_rows),
        "top1_all_truth_case_count": sum(rank <= 1 for rank in ranks),
        "top1_target0_hit_count": sum(boolish(row["top_target0_hit"]) for row in out_rows),
        "top1_target1_hit_count": sum(boolish(row["top_target1_hit"]) for row in out_rows),
        "top1_target2_hit_count": sum(boolish(row["top_target2_hit"]) for row in out_rows),
        "median_first_all_truth_rank": float(np.median([rank for rank in ranks if math.isfinite(rank)])) if ranks else math.nan,
        "max_first_all_truth_rank": max([rank for rank in ranks if math.isfinite(rank)], default=math.nan),
        "selected_feature_count": len(labels),
        "dominant_trained_feature": labels.most_common(1)[0][0] if labels else "",
    }
    for budget in BUDGETS:
        summary[f"first_truth_top{budget}_case_count"] = sum(rank <= budget for rank in ranks)
    return summary, out_rows


def rank_budget_label(rank: float) -> str:
    if not math.isfinite(rank):
        return "truth_missing"
    if rank <= 1:
        return "top1_possible"
    if rank <= 10:
        return "top10_rank_gate"
    if rank <= 50:
        return "top50_rank_gate"
    if rank <= 200:
        return "top200_rank_gate"
    return "too_deep_for_current_gate"


def build_case_summary_rows(objective_case_rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in objective_case_rows:
        key = (str(row["branch_key"]), str(row["seed"]), str(row["case_variant"]), str(row["run_name"]))
        grouped[key].append(row)

    out = []
    for key, rows in sorted(grouped.items()):
        best = min(
            rows,
            key=lambda row: (
                safe_float(row["first_all_truth_rank"], math.inf),
                safe_float(row["best_false_minus_best_truth_score_gap"], math.inf),
                str(row["feature"]),
            ),
        )
        rank = safe_float(best["first_all_truth_rank"], math.inf)
        gaps = [safe_float(row["best_false_minus_best_truth_score_gap"]) for row in rows]
        finite_gaps = [gap for gap in gaps if math.isfinite(gap)]
        out.append(
            {
                "case_label": best["case_label"],
                "branch_key": key[0],
                "seed": safe_int(key[1]),
                "case_variant": key[2],
                "run_name": key[3],
                "candidate_triple_count": safe_int(best["candidate_triple_count"]),
                "all_truth_triple_count": safe_int(best["all_truth_triple_count"]),
                "best_feature": best["feature"],
                "best_first_all_truth_rank": rank,
                "best_budget_label": rank_budget_label(rank),
                "best_false_minus_truth_score_gap": safe_float(best["best_false_minus_best_truth_score_gap"]),
                "positive_gap_feature_count": sum(gap > 0.0 for gap in finite_gaps),
                "feature_count": len(rows),
            }
        )
    return out


def branch_summary_rows(case_rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in case_rows}):
        rows = [row for row in case_rows if row["branch_key"] == branch]
        ranks = [safe_float(row["best_first_all_truth_rank"], math.inf) for row in rows]
        labels = Counter(row["best_budget_label"] for row in rows)
        out.append(
            {
                "branch_key": branch,
                "case_count": len(rows),
                "top1_possible_case_count": sum(rank <= 1 for rank in ranks),
                "top10_possible_case_count": sum(rank <= 10 for rank in ranks),
                "top50_possible_case_count": sum(rank <= 50 for rank in ranks),
                "top200_possible_case_count": sum(rank <= 200 for rank in ranks),
                "median_best_first_all_truth_rank": float(np.median([rank for rank in ranks if math.isfinite(rank)])) if ranks else math.nan,
                "dominant_budget_label": labels.most_common(1)[0][0] if labels else "",
            }
        )
    return out


def summarize_audit(
    rows: list[dict],
    objective_rows: list[dict],
    case_rows: list[dict],
    branch_rows: list[dict],
    cv_rows: list[dict],
    source_summary: dict | None = None,
) -> dict:
    case_count = len(case_rows)
    budget, budget_feature = minimal_all_case_budget(objective_rows, case_count)
    best_by_budget = {
        f"top{budget_value}": {
            "feature": best_budget_row(objective_rows, budget_value)["feature"],
            "case_count": safe_int(best_budget_row(objective_rows, budget_value).get(f"first_truth_top{budget_value}_case_count")),
        }
        for budget_value in BUDGETS
    }
    best_top1 = best_budget_row(objective_rows, 1)
    leave_one_case = next((row for row in cv_rows if row["cv_strategy"] == "leave_one_case"), {})
    all_truth_count = sum(bool(row.get("unique_all_truths_bool", truth_label(row))) for row in rows)
    positive_fraction = all_truth_count / len(rows) if rows else math.nan
    ready_for_fwi = safe_int(leave_one_case.get("top1_all_truth_case_count")) == case_count
    rank_gate_ready = budget is not None and budget <= 200
    source_summary = source_summary or {}
    return {
        "policy_label": "local_2d_detector_feature_separability_audit_cpu_no_fwi",
        "case_count": case_count,
        "candidate_triple_row_count": len(rows),
        "all_truth_triple_count": all_truth_count,
        "all_truth_triple_fraction": positive_fraction,
        "feature_count": len(objective_rows),
        "branch_row_count": len(branch_rows),
        "best_top1_feature": best_top1["feature"],
        "best_top1_all_truth_case_count": safe_int(best_top1.get("top1_all_truth_case_count")),
        "best_case_count_by_budget": best_by_budget,
        "minimal_all_case_rank_gated_budget": budget,
        "minimal_all_case_rank_gated_feature": budget_feature,
        "leave_one_case_top1_all_truth_case_count": safe_int(leave_one_case.get("top1_all_truth_case_count")),
        "leave_one_case_top50_case_count": safe_int(leave_one_case.get("first_truth_top50_case_count")),
        "leave_one_case_top200_case_count": safe_int(leave_one_case.get("first_truth_top200_case_count")),
        "median_best_first_all_truth_rank": float(np.median([safe_float(row["best_first_all_truth_rank"], math.inf) for row in case_rows])),
        "max_best_first_all_truth_rank": max(safe_float(row["best_first_all_truth_rank"], math.inf) for row in case_rows),
        "source_component_gate_best_top50_case_count": source_summary.get("best_top50_case_count"),
        "source_component_gate_minimal_all_case_budget": source_summary.get("minimal_all_case_candidate_triple_budget"),
        "ready_for_rank_gated_upper_bound_claim": rank_gate_ready,
        "ready_for_detector_seeded_fwi": ready_for_fwi,
        "gpu_priority": "none",
        "backend": "saved_component_gate_rows_cpu_feature_separability",
        "decision": (
            "Truth triples are present but rare, and no cross-validated top-1 truth-free feature "
            "selector is ready. Treat detector evidence as rank-gated upper-bound/context evidence; "
            "do not launch detector-seeded FWI from this selector state."
        ),
    }


def plot_audit(case_rows: list[dict], objective_rows: list[dict], cv_rows: list[dict], summary: dict, save_path: Path) -> str:
    budgets = list(BUDGETS)
    best_counts = [summary["best_case_count_by_budget"][f"top{budget}"]["case_count"] for budget in budgets]
    cv_case = next((row for row in cv_rows if row["cv_strategy"] == "leave_one_case"), {})
    cv_counts = [safe_int(cv_case.get(f"first_truth_top{budget}_case_count")) for budget in budgets]

    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.4), constrained_layout=True)

    x = np.arange(len(budgets))
    axes[0].plot(x, best_counts, marker="o", linewidth=2.0, label="best in-sample feature", color="#4c78a8")
    axes[0].plot(x, cv_counts, marker="s", linewidth=2.0, label="leave-one-case feature", color="#f58518")
    axes[0].set_xticks(x, [str(budget) for budget in budgets])
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_xlabel("candidate-triple budget")
    axes[0].set_ylabel("cases with all-truth triple")
    axes[0].set_title("Rank-gated truth recovery")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    ordered_cases = sorted(case_rows, key=lambda row: (str(row["branch_key"]), safe_int(row["seed"]), str(row["case_variant"])))
    ranks = [safe_float(row["best_first_all_truth_rank"], math.nan) for row in ordered_cases]
    labels = [f"{row['branch_key'].replace('target', 't')} s{row['seed']}" for row in ordered_cases]
    colors = ["#54a24b" if rank <= 10 else "#eeca3b" if rank <= 50 else "#e45756" for rank in ranks]
    axes[1].bar(np.arange(len(ordered_cases)), ranks, color=colors, width=0.62)
    axes[1].axhline(50, color="#666666", linestyle="--", linewidth=1.0)
    axes[1].axhline(200, color="#999999", linestyle=":", linewidth=1.0)
    axes[1].set_xticks(np.arange(len(ordered_cases)), labels, rotation=45, ha="right", fontsize=7)
    axes[1].set_ylabel("best first all-truth rank")
    axes[1].set_title("Best possible case ranks across features")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector feature separability audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_feature_separability_audit.png`",
                "",
                "This figure audits saved detector/component-gate candidate triples. It",
                "does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or",
                "neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Candidate triples: `{summary['candidate_triple_row_count']}`.",
                f"All-truth triples: `{summary['all_truth_triple_count']}`.",
                f"Best top-1 feature: `{summary['best_top1_feature']}`.",
                f"Best top-1 all-truth cases: `{summary['best_top1_all_truth_case_count']}`.",
                f"Minimal all-case rank-gated budget: `{summary['minimal_all_case_rank_gated_budget']}`.",
                f"Leave-one-case top-1 all-truth cases: `{summary['leave_one_case_top1_all_truth_case_count']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                summary["decision"],
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--component-gate-run", default=DEFAULT_COMPONENT_GATE_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_feature_separability_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    component_dir = Path(args.summary_root) / args.component_gate_run
    rows = [
        enriched_row(row)
        for row in read_csv_rows(component_dir / "data/local_2d_detector_component_waveform_gate_rows.csv")
    ]
    source_summary = read_json(component_dir / "data/local_2d_detector_component_waveform_gate_summary.json")

    objective_case_rows = build_objective_case_rows(rows)
    objective_rows = summarize_objectives(objective_case_rows)
    case_rows = build_case_summary_rows(objective_case_rows)
    branch_rows = branch_summary_rows(case_rows)
    cv_summaries = []
    cv_case_rows = []
    for strategy in ("leave_one_case", "leave_one_seed", "leave_one_branch"):
        cv_summary, rows_for_strategy = cross_validate_objectives(objective_case_rows, strategy)
        cv_summaries.append(cv_summary)
        cv_case_rows.extend(rows_for_strategy)
    summary = summarize_audit(rows, objective_rows, case_rows, branch_rows, cv_summaries, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    write_csv(data_dir / "local_2d_detector_feature_separability_objective_cases.csv", objective_case_rows)
    write_csv(data_dir / "local_2d_detector_feature_separability_objective_summary.csv", objective_rows)
    write_csv(data_dir / "local_2d_detector_feature_separability_case_summary.csv", case_rows)
    write_csv(data_dir / "local_2d_detector_feature_separability_branch_summary.csv", branch_rows)
    write_csv(data_dir / "local_2d_detector_feature_separability_cv_summary.csv", cv_summaries)
    write_csv(data_dir / "local_2d_detector_feature_separability_cv_cases.csv", cv_case_rows)
    (data_dir / "local_2d_detector_feature_separability_summary.json").write_text(
        json.dumps(json_safe(summary), indent=2) + "\n",
        encoding="utf-8",
    )

    fig_path = figures_dir / "local_2d_detector_feature_separability_audit.png"
    plot_audit(case_rows, objective_rows, cv_summaries, summary, fig_path)
    write_figure_notes(figures_dir / "FIGURE_NOTES.md", summary)
    write_csv(data_dir / "figure_validation.csv", [figure_stats(fig_path)])
    write_run_manifest(
        str(outdir),
        "local_2d_detector_feature_separability_audit",
        {
            "summary": json_safe(summary),
            "paths": {
                "source_component_gate_rows_csv": str(component_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
                "summary_json": str(data_dir / "local_2d_detector_feature_separability_summary.json"),
                "figure": str(fig_path),
            },
        },
    )

    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
