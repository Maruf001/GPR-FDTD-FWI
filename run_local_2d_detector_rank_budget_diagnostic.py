#!/usr/bin/env python3
"""Diagnose detector all-triples rank budgets before any FWI handoff."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
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
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ALLTRIPLES_RUN = "030_local_2d_detector_alltriples_gate_pilot"
OBJECTIVES = ("sum", "span_bonus", "min", "min_span", "balanced", "mask")
BUDGETS = (1, 3, 5, 10, 20, 50, 100, 200, 500, 1140)
TARGET_FIELDS = ("unique_target0_hit", "unique_target1_hit", "unique_target2_hit")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def safe_int(value, default: int = 0) -> int:
    number = safe_float(value)
    if not math.isfinite(number):
        return default
    return int(number)


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def group_by_case(rows: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("case_label", ""))].append(row)
    return dict(grouped)


def objective_score(row: dict, objective: str) -> float:
    return safe_float(row.get(f"score_{objective}"), -math.inf)


def ranked_case_rows(case_rows: list[dict], objective: str) -> list[dict]:
    return sorted(case_rows, key=lambda row: objective_score(row, objective), reverse=True)


def first_all_truth_rank(case_rows: list[dict], objective: str) -> float:
    for rank, row in enumerate(ranked_case_rows(case_rows, objective), start=1):
        if boolish(row.get("unique_all_truths_within_tolerance")):
            return float(rank)
    return math.inf


def budget_label(rank: float) -> str:
    if not math.isfinite(rank):
        return "not_in_candidate_space"
    if rank <= 10:
        return "top10_candidate"
    if rank <= 50:
        return "top50_candidate"
    if rank <= 100:
        return "top100_candidate"
    if rank <= 200:
        return "top200_candidate"
    return "deep_candidate_space"


def all_truth_manifold_label(all_truth_count: int) -> str:
    if all_truth_count <= 0:
        return "missing_all_truth_combo"
    if all_truth_count <= 2:
        return "sparse_all_truth_manifold"
    if all_truth_count <= 8:
        return "narrow_all_truth_manifold"
    return "broad_all_truth_manifold"


def build_case_rows(combo_rows: list[dict], objectives: tuple[str, ...] = OBJECTIVES) -> list[dict]:
    out = []
    for case_label, case_rows in sorted(group_by_case(combo_rows).items()):
        first_ranks = {objective: first_all_truth_rank(case_rows, objective) for objective in objectives}
        best_objective, best_rank = min(first_ranks.items(), key=lambda item: item[1])
        all_truth_count = sum(boolish(row.get("unique_all_truths_within_tolerance")) for row in case_rows)
        target_counts = {
            field: sum(boolish(row.get(field)) for row in case_rows)
            for field in TARGET_FIELDS
        }
        first = case_rows[0]
        row = {
            "case_label": case_label,
            "branch_key": first.get("branch_key", ""),
            "seed": safe_int(first.get("seed")),
            "case_variant": first.get("case_variant", ""),
            "combo_count": len(case_rows),
            "all_truth_combo_count": all_truth_count,
            "target0_combo_count": target_counts["unique_target0_hit"],
            "target1_combo_count": target_counts["unique_target1_hit"],
            "target2_combo_count": target_counts["unique_target2_hit"],
            "best_objective": best_objective,
            "best_first_all_truth_rank": best_rank,
            "best_budget_label": budget_label(best_rank),
            "all_truth_manifold_label": all_truth_manifold_label(all_truth_count),
        }
        for objective, rank in first_ranks.items():
            row[f"{objective}_first_all_truth_rank"] = rank
        out.append(row)
    return out


def build_objective_rows(combo_rows: list[dict], objectives: tuple[str, ...] = OBJECTIVES) -> list[dict]:
    grouped = group_by_case(combo_rows)
    out = []
    for objective in objectives:
        first_ranks = []
        top_target_counts = [0, 0, 0]
        top_all_truth = 0
        for case_rows in grouped.values():
            ordered = ranked_case_rows(case_rows, objective)
            top = ordered[0] if ordered else {}
            top_all_truth += boolish(top.get("unique_all_truths_within_tolerance"))
            for idx, field in enumerate(TARGET_FIELDS):
                top_target_counts[idx] += boolish(top.get(field))
            first_ranks.append(first_all_truth_rank(case_rows, objective))
        finite_ranks = [rank for rank in first_ranks if math.isfinite(rank)]
        objective_row = {
            "objective": objective,
            "case_count": len(grouped),
            "top1_all_truth_case_count": top_all_truth,
            "top1_target0_hit_count": top_target_counts[0],
            "top1_target1_hit_count": top_target_counts[1],
            "top1_target2_hit_count": top_target_counts[2],
            "median_first_all_truth_rank": float(np.median(finite_ranks)) if finite_ranks else math.nan,
            "max_first_all_truth_rank": max(finite_ranks) if finite_ranks else math.nan,
        }
        for budget in BUDGETS:
            objective_row[f"first_truth_top{budget}_case_count"] = sum(rank <= budget for rank in first_ranks)
        out.append(objective_row)
    return out


def build_budget_rows(objective_rows: list[dict], budgets: tuple[int, ...] = BUDGETS) -> list[dict]:
    out = []
    for row in objective_rows:
        for budget in budgets:
            count = safe_int(row.get(f"first_truth_top{budget}_case_count"))
            case_count = safe_int(row.get("case_count"))
            out.append(
                {
                    "objective": row["objective"],
                    "candidate_triple_budget": budget,
                    "first_all_truth_case_count": count,
                    "case_count": case_count,
                    "case_fraction": count / case_count if case_count else math.nan,
                }
            )
    return out


def summarize(
    combo_rows: list[dict],
    case_rows: list[dict],
    objective_rows: list[dict],
    budget_rows: list[dict],
    source_summary: dict | None = None,
) -> dict:
    case_count = len(case_rows)
    def best_budget_count(budget: int) -> tuple[str, int]:
        rows = [row for row in budget_rows if safe_int(row["candidate_triple_budget"]) == budget]
        best = max(rows, key=lambda row: safe_int(row["first_all_truth_case_count"]))
        return str(best["objective"]), safe_int(best["first_all_truth_case_count"])

    best_top20_objective, best_top20_count = best_budget_count(20)
    best_top50_objective, best_top50_count = best_budget_count(50)
    best_top100_objective, best_top100_count = best_budget_count(100)
    best_top200_objective, best_top200_count = best_budget_count(200)
    all_case_budget_rows = [
        row for row in budget_rows if safe_int(row["first_all_truth_case_count"]) == case_count
    ]
    minimal_all_case_budget = (
        min(safe_int(row["candidate_triple_budget"]) for row in all_case_budget_rows)
        if all_case_budget_rows
        else math.nan
    )
    minimal_all_case_objectives = sorted(
        {
            str(row["objective"])
            for row in all_case_budget_rows
            if safe_int(row["candidate_triple_budget"]) == minimal_all_case_budget
        }
    )
    max_left_target_top1 = max(safe_int(row["top1_target0_hit_count"]) for row in objective_rows)
    sparse_all_truth_cases = sum(
        row["all_truth_manifold_label"] == "sparse_all_truth_manifold" for row in case_rows
    )
    ready_for_upper_bound = math.isfinite(minimal_all_case_budget) and minimal_all_case_budget <= 200
    return {
        "policy_label": "local_2d_detector_rank_budget_diagnostic_cpu_no_fwi",
        "source_policy_label": (source_summary or {}).get("policy_label", ""),
        "case_count": case_count,
        "combo_row_count": len(combo_rows),
        "objective_count": len(objective_rows),
        "budget_row_count": len(budget_rows),
        "all_truth_combo_available_case_count": sum(safe_int(row["all_truth_combo_count"]) > 0 for row in case_rows),
        "sparse_all_truth_case_count": sparse_all_truth_cases,
        "best_top20_objective": best_top20_objective,
        "best_top20_case_count": best_top20_count,
        "best_top50_objective": best_top50_objective,
        "best_top50_case_count": best_top50_count,
        "best_top100_objective": best_top100_objective,
        "best_top100_case_count": best_top100_count,
        "best_top200_objective": best_top200_objective,
        "best_top200_case_count": best_top200_count,
        "minimal_all_case_candidate_triple_budget": minimal_all_case_budget,
        "minimal_all_case_objectives": minimal_all_case_objectives,
        "max_top1_all_truth_case_count": max(safe_int(row["top1_all_truth_case_count"]) for row in objective_rows),
        "max_top1_target0_hit_count": max_left_target_top1,
        "ready_for_rank_gated_upper_bound_study": ready_for_upper_bound,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as a CPU-only detector handoff diagnostic. All cases contain at least one "
            "all-truth triple inside the branch-specific top-20 candidate space, but current "
            "objectives need a rank budget up to 200 candidate triples per case to cover all cases "
            "and never select an all-truth triple at rank 1. This supports a rank-gated upper-bound "
            "study or a stronger waveform gate, not detector-seeded FWI."
        ),
    }


def plot_diagnostic(objective_rows: list[dict], budget_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.4), constrained_layout=True)
    for objective in [row["objective"] for row in objective_rows]:
        rows = [row for row in budget_rows if row["objective"] == objective]
        budgets = [safe_int(row["candidate_triple_budget"]) for row in rows]
        counts = [safe_int(row["first_all_truth_case_count"]) for row in rows]
        axes[0].plot(budgets, counts, marker="o", linewidth=1.4, label=objective)
    axes[0].set_xscale("log")
    axes[0].set_xticks([1, 3, 5, 10, 20, 50, 100, 200, 500, 1140])
    axes[0].get_xaxis().set_major_formatter(plt.ScalarFormatter())
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_xlabel("candidate triples per case")
    axes[0].set_ylabel("cases with first all-truth triple within budget")
    axes[0].set_title("Rank budget required before FWI")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8, ncol=2)

    labels = [row["objective"].replace("_", "\n") for row in objective_rows]
    x = np.arange(len(objective_rows))
    width = 0.25
    axes[1].bar(x - width, [safe_int(row["top1_target0_hit_count"]) for row in objective_rows], width=width, label="target0")
    axes[1].bar(x, [safe_int(row["top1_target1_hit_count"]) for row in objective_rows], width=width, label="target1")
    axes[1].bar(x + width, [safe_int(row["top1_target2_hit_count"]) for row in objective_rows], width=width, label="target2")
    axes[1].set_xticks(x, labels, fontsize=8)
    axes[1].set_ylim(0, summary["case_count"] + 1)
    axes[1].set_ylabel("top-ranked case count")
    axes[1].set_title("Top-ranked triples under-select the left target")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.02,
        0.96,
        f"top1 all-truth max: {summary['max_top1_all_truth_case_count']}\n"
        f"all-case budget: {summary['minimal_all_case_candidate_triple_budget']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("Local 2D detector rank-budget diagnostic", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(
    path: Path,
    summary: dict,
    case_csv: Path,
    objective_csv: Path,
    budget_csv: Path,
    summary_json: Path,
) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_rank_budget_diagnostic.png`",
                "",
                "This CPU-only diagnostic reads the saved all-triples detector gate rows",
                "and summarizes how many candidate triples per case are needed before",
                "an all-truth detector triple appears under each objective.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Candidate-triple rows: `{summary['combo_row_count']}`.",
                f"Best top-20 objective: `{summary['best_top20_objective']}` with `{summary['best_top20_case_count']}` cases.",
                f"Best top-50 objective: `{summary['best_top50_objective']}` with `{summary['best_top50_case_count']}` cases.",
                f"Minimal all-case budget: `{summary['minimal_all_case_candidate_triple_budget']}` candidate triples per case.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case diagnostics: `{case_csv.name}`.",
                f"- Objective diagnostics: `{objective_csv.name}`.",
                f"- Budget curve: `{budget_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                "",
                "Scope boundary:",
                "",
                "This diagnostic does not run FDTD, FWI, GPU kernels, field FWI,",
                "3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--alltriples-run", default=DEFAULT_ALLTRIPLES_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_rank_budget_diagnostic")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_root = Path(args.summary_root) / args.alltriples_run
    combo_csv = source_root / "data/local_2d_detector_alltriples_gate_rows.csv"
    source_summary_json = source_root / "data/local_2d_detector_alltriples_gate_summary.json"
    combo_rows = read_csv_rows(combo_csv)
    source_summary = read_json(source_summary_json)

    case_rows = build_case_rows(combo_rows)
    objective_rows = build_objective_rows(combo_rows)
    budget_rows = build_budget_rows(objective_rows)
    summary = summarize(combo_rows, case_rows, objective_rows, budget_rows, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_out = data_dir / "local_2d_detector_rank_budget_case_diagnostic.csv"
    objective_out = data_dir / "local_2d_detector_rank_budget_objective_summary.csv"
    budget_out = data_dir / "local_2d_detector_rank_budget_curve.csv"
    summary_out = data_dir / "local_2d_detector_rank_budget_diagnostic_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_rank_budget_diagnostic.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(case_out, [json_safe(row) for row in case_rows])
    write_csv(objective_out, [json_safe(row) for row in objective_rows])
    write_csv(budget_out, [json_safe(row) for row in budget_rows])
    plot_diagnostic(objective_rows, budget_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_combo_csv": str(combo_csv),
        "source_summary_json": str(source_summary_json),
        "case_diagnostic_csv": str(case_out),
        "objective_summary_csv": str(objective_out),
        "budget_curve_csv": str(budget_out),
        "summary_json": str(summary_out),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_out.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, case_out, objective_out, budget_out, summary_out)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_rank_budget_diagnostic",
        {
            "alltriples_run": args.alltriples_run,
            "combo_csv": str(combo_csv),
            "source_summary_json": str(source_summary_json),
            "summary_json": str(summary_out),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
