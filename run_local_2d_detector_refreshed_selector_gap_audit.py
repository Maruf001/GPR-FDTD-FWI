#!/usr/bin/env python3
"""Audit residual rank gaps for the refreshed local 2D detector selector."""

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


DEFAULT_SEPARABILITY_RUN = "105_local_2d_detector_feature_separability_audit_post_upper_bound"
DEFAULT_FEATURE_FAMILY_RUN = "107_local_2d_detector_selector_feature_family_audit_post_blocker_triage"
BUDGETS = (1, 10, 50, 100, 200)
TARGET_FIELDS = ("top_target0_hit", "top_target1_hit", "top_target2_hit")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def rank_value(value) -> float:
    return safe_float(value, math.inf)


def rank_gate_label(rank: float) -> str:
    if not math.isfinite(rank):
        return "truth_missing"
    if rank <= 1:
        return "top1"
    if rank <= 10:
        return "top10"
    if rank <= 50:
        return "top50"
    if rank <= 100:
        return "top100"
    if rank <= 200:
        return "top200"
    return "deeper_than_top200"


def missing_targets(row: dict) -> str:
    misses = []
    for index, field in enumerate(TARGET_FIELDS):
        if not boolish(row.get(field)):
            misses.append(f"target{index}")
    return ",".join(misses) if misses else "none"


def objective_lookup(objective_rows: list[dict]) -> dict[tuple[str, str], dict]:
    return {(str(row["case_label"]), str(row["feature"])): row for row in objective_rows}


def best_objective_by_case(objective_rows: list[dict]) -> dict[str, dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in objective_rows:
        grouped[str(row["case_label"])].append(row)
    return {
        label: min(
            rows,
            key=lambda row: (
                rank_value(row.get("first_all_truth_rank")),
                safe_float(row.get("best_false_minus_best_truth_score_gap"), math.inf),
                str(row.get("feature", "")),
            ),
        )
        for label, rows in grouped.items()
    }


def selected_policy_rows(selector_rows: list[dict], selector_summary: dict) -> list[dict]:
    family = str(selector_summary["best_feature_family"])
    strategy = str(selector_summary["best_selector_strategy"])
    rows = [
        row
        for row in selector_rows
        if str(row["feature_family"]) == family and str(row["selector_strategy"]) == strategy
    ]
    return sorted(rows, key=lambda row: str(row["case_label"]))


def build_gap_rows(selector_rows: list[dict], objective_rows: list[dict], selector_summary: dict) -> list[dict]:
    by_feature = objective_lookup(objective_rows)
    by_case_best = best_objective_by_case(objective_rows)
    out = []
    for selected in selected_policy_rows(selector_rows, selector_summary):
        label = str(selected["case_label"])
        feature = str(selected["selected_feature"])
        objective = by_feature[(label, feature)]
        best = by_case_best[label]
        selected_rank = rank_value(objective.get("first_all_truth_rank"))
        best_rank = rank_value(best.get("first_all_truth_rank"))
        penalty = selected_rank - best_rank if math.isfinite(selected_rank) and math.isfinite(best_rank) else math.nan
        false_minus_truth = safe_float(objective.get("best_false_minus_best_truth_score_gap"), math.nan)
        out.append(
            {
                "case_label": label,
                "branch_key": selected["branch_key"],
                "seed": safe_int(selected["seed"]),
                "case_variant": selected["case_variant"],
                "run_name": selected["run_name"],
                "feature_family": selected["feature_family"],
                "selector_strategy": selected["selector_strategy"],
                "selected_feature": feature,
                "selected_first_all_truth_rank": selected_rank,
                "selected_rank_gate_label": rank_gate_label(selected_rank),
                "selected_best_false_minus_truth_score_gap": false_minus_truth,
                "selected_positive_false_truth_gap": false_minus_truth > 0.0 if math.isfinite(false_minus_truth) else False,
                "selected_top_unique_truth_hit_count": safe_int(objective.get("top_unique_truth_hit_count")),
                "selected_top_missing_targets": missing_targets(objective),
                "selected_top_candidate_x_values_mm": objective.get("top_candidate_x_values_mm", ""),
                "selected_top_candidate_ranks": objective.get("top_candidate_ranks", ""),
                "case_best_feature": best.get("feature", ""),
                "case_best_first_all_truth_rank": best_rank,
                "case_best_rank_gate_label": rank_gate_label(best_rank),
                "rank_penalty_vs_case_best": penalty,
                "selected_matches_case_best_feature": feature == str(best.get("feature", "")),
                "all_truth_triple_count": safe_int(objective.get("all_truth_triple_count")),
                "candidate_triple_count": safe_int(objective.get("candidate_triple_count")),
            }
        )
    return out


def branch_summary_rows(gap_rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in gap_rows}):
        rows = [row for row in gap_rows if row["branch_key"] == branch]
        ranks = [rank_value(row["selected_first_all_truth_rank"]) for row in rows]
        penalties = [
            safe_float(row["rank_penalty_vs_case_best"])
            for row in rows
            if math.isfinite(safe_float(row["rank_penalty_vs_case_best"]))
        ]
        labels = Counter(row["selected_rank_gate_label"] for row in rows)
        misses = Counter(row["selected_top_missing_targets"] for row in rows)
        result = {
            "branch_key": branch,
            "case_count": len(rows),
            "top1_case_count": sum(rank <= 1 for rank in ranks),
            "top10_case_count": sum(rank <= 10 for rank in ranks),
            "top50_case_count": sum(rank <= 50 for rank in ranks),
            "top100_case_count": sum(rank <= 100 for rank in ranks),
            "top200_case_count": sum(rank <= 200 for rank in ranks),
            "median_selected_first_all_truth_rank": float(np.median([rank for rank in ranks if math.isfinite(rank)])) if ranks else math.nan,
            "max_selected_first_all_truth_rank": max([rank for rank in ranks if math.isfinite(rank)], default=math.nan),
            "median_rank_penalty_vs_case_best": float(np.median(penalties)) if penalties else math.nan,
            "dominant_rank_gate_label": labels.most_common(1)[0][0] if labels else "",
            "dominant_top_missing_targets": misses.most_common(1)[0][0] if misses else "",
        }
        out.append(result)
    return out


def summarize_gap_audit(gap_rows: list[dict], branch_rows: list[dict], selector_summary: dict) -> dict:
    ranks = [rank_value(row["selected_first_all_truth_rank"]) for row in gap_rows]
    best_ranks = [rank_value(row["case_best_first_all_truth_rank"]) for row in gap_rows]
    penalties = [
        safe_float(row["rank_penalty_vs_case_best"])
        for row in gap_rows
        if math.isfinite(safe_float(row["rank_penalty_vs_case_best"]))
    ]
    misses = Counter(row["selected_top_missing_targets"] for row in gap_rows)
    features = Counter(row["selected_feature"] for row in gap_rows)
    rank_penalty_cases = sum(value > 0.0 for value in penalties)
    return {
        "policy_label": "local_2d_detector_refreshed_selector_gap_audit_cpu_no_fwi",
        "source_selector_policy_label": selector_summary.get("policy_label", ""),
        "case_count": len(gap_rows),
        "branch_row_count": len(branch_rows),
        "selected_feature_family": selector_summary.get("best_feature_family", ""),
        "selected_selector_strategy": selector_summary.get("best_selector_strategy", ""),
        "selected_feature_count": len(features),
        "dominant_selected_feature": features.most_common(1)[0][0] if features else "",
        "selected_top1_case_count": sum(rank <= 1 for rank in ranks),
        "selected_top10_case_count": sum(rank <= 10 for rank in ranks),
        "selected_top50_case_count": sum(rank <= 50 for rank in ranks),
        "selected_top100_case_count": sum(rank <= 100 for rank in ranks),
        "selected_top200_case_count": sum(rank <= 200 for rank in ranks),
        "selected_deeper_than_top200_case_count": sum(rank > 200 for rank in ranks),
        "case_oracle_top1_case_count": sum(rank <= 1 for rank in best_ranks),
        "case_oracle_top50_case_count": sum(rank <= 50 for rank in best_ranks),
        "case_oracle_top200_case_count": sum(rank <= 200 for rank in best_ranks),
        "selected_matches_case_best_feature_count": sum(bool(row["selected_matches_case_best_feature"]) for row in gap_rows),
        "rank_penalty_vs_case_best_case_count": rank_penalty_cases,
        "median_selected_first_all_truth_rank": float(np.median([rank for rank in ranks if math.isfinite(rank)])) if ranks else math.nan,
        "max_selected_first_all_truth_rank": max([rank for rank in ranks if math.isfinite(rank)], default=math.nan),
        "median_case_best_first_all_truth_rank": float(np.median([rank for rank in best_ranks if math.isfinite(rank)])) if best_ranks else math.nan,
        "max_case_best_first_all_truth_rank": max([rank for rank in best_ranks if math.isfinite(rank)], default=math.nan),
        "median_rank_penalty_vs_case_best": float(np.median(penalties)) if penalties else math.nan,
        "max_rank_penalty_vs_case_best": max(penalties, default=math.nan),
        "positive_false_minus_truth_gap_case_count": sum(bool(row["selected_positive_false_truth_gap"]) for row in gap_rows),
        "dominant_top_missing_targets": misses.most_common(1)[0][0] if misses else "",
        "ready_for_rank_gated_selector_claim": sum(rank <= 200 for rank in ranks) == len(gap_rows),
        "ready_for_detector_seeded_fwi": sum(rank <= 1 for rank in ranks) == len(gap_rows),
        "gpu_priority": "none",
        "decision": (
            "The refreshed component-only selector is useful as a rank-gated candidate-list result, "
            "but it remains a top-1 failure across all cases. Use this audit to explain residual "
            "false-vs-truth dominance and missing-target signatures; do not launch detector-seeded FWI."
        ),
    }


def plot_gap_audit(summary: dict, gap_rows: list[dict], save_path: Path) -> str:
    rows = sorted(gap_rows, key=lambda row: rank_value(row["selected_first_all_truth_rank"]), reverse=True)
    labels = [row["case_label"].replace("target2_", "").replace("|", "\n") for row in rows]
    ranks = [rank_value(row["selected_first_all_truth_rank"]) for row in rows]
    penalties = [safe_float(row["rank_penalty_vs_case_best"], 0.0) for row in rows]
    color_map = {
        "top10": "#59a14f",
        "top50": "#f2cf5b",
        "top100": "#f28e2b",
        "top200": "#e15759",
        "deeper_than_top200": "#8b1a1a",
        "truth_missing": "#8b1a1a",
        "top1": "#2f7d32",
    }
    colors = [color_map.get(row["selected_rank_gate_label"], "#bab0ac") for row in rows]
    x = np.arange(len(rows))

    fig, axes = plt.subplots(1, 2, figsize=(16.2, 5.8), constrained_layout=True)
    axes[0].bar(x, ranks, color=colors)
    for budget in (10, 50, 100, 200):
        axes[0].axhline(budget, color="#777777", linewidth=0.7, linestyle="--")
        axes[0].text(len(rows) - 0.35, budget, f"top{budget}", va="bottom", ha="right", fontsize=7)
    axes[0].set_xticks(x, labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("first all-truth rank")
    axes[0].set_title("Refreshed selector rank gaps")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, penalties, color="#4e79a7")
    axes[1].set_xticks(x, labels, rotation=45, ha="right", fontsize=7)
    axes[1].set_ylabel("rank penalty vs per-case best feature")
    axes[1].set_title("Feature-choice penalty")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.98,
        0.96,
        f"top1={summary['selected_top1_case_count']}/{summary['case_count']}\n"
        f"top50={summary['selected_top50_case_count']}/{summary['case_count']}\n"
        f"top200={summary['selected_top200_case_count']}/{summary['case_count']}\n"
        f"dominant miss={summary['dominant_top_missing_targets']}\n"
        f"FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="right",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D refreshed detector selector gap audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_refreshed_selector_gap_audit.png`",
                "",
                "This CPU-only audit explains residual rank gaps after the refreshed detector",
                "selector feature-family audit. It reads saved rank/separability outputs only.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Selected policy: `{summary['selected_feature_family']}` / `{summary['selected_selector_strategy']}`.",
                f"Dominant feature: `{summary['dominant_selected_feature']}`.",
                f"Selected top50 cases: `{summary['selected_top50_case_count']}` / `{summary['case_count']}`.",
                f"Selected top200 cases: `{summary['selected_top200_case_count']}` / `{summary['case_count']}`.",
                f"Dominant top missing targets: `{summary['dominant_top_missing_targets']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                summary["decision"],
                "",
                "Scope boundary: no FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or",
                "neural-network training is performed by this audit.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--separability-run", default=DEFAULT_SEPARABILITY_RUN)
    parser.add_argument("--feature-family-run", default=DEFAULT_FEATURE_FAMILY_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_refreshed_selector_gap_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    separability_data = summary_root / args.separability_run / "data"
    feature_family_data = summary_root / args.feature_family_run / "data"
    objective_rows = read_csv_rows(separability_data / "local_2d_detector_feature_separability_objective_cases.csv")
    selector_rows = read_csv_rows(feature_family_data / "local_2d_detector_selector_feature_family_cases.csv")
    selector_summary = read_json(feature_family_data / "local_2d_detector_selector_feature_family_summary.json")

    gap_rows = build_gap_rows(selector_rows, objective_rows, selector_summary)
    branch_rows = branch_summary_rows(gap_rows)
    summary = summarize_gap_audit(gap_rows, branch_rows, selector_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_refreshed_selector_gap_cases.csv"
    branch_csv = data_dir / "local_2d_detector_refreshed_selector_gap_branch_summary.csv"
    summary_json = data_dir / "local_2d_detector_refreshed_selector_gap_summary.json"
    figure_path = figures_dir / "local_2d_detector_refreshed_selector_gap_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(case_csv, [json_safe(row) for row in gap_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    plot_gap_audit(summary, gap_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_objective_cases_csv": str(separability_data / "local_2d_detector_feature_separability_objective_cases.csv"),
        "source_selector_cases_csv": str(feature_family_data / "local_2d_detector_selector_feature_family_cases.csv"),
        "source_selector_summary_json": str(feature_family_data / "local_2d_detector_selector_feature_family_summary.json"),
        "case_csv": str(case_csv),
        "branch_summary_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_refreshed_selector_gap_audit",
        {
            "separability_run": args.separability_run,
            "feature_family_run": args.feature_family_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "summary": json_safe(summary),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
