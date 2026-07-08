#!/usr/bin/env python3
"""Quantify detector-to-FWI handoff candidate budgets from saved detector outputs."""

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
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RANK_SUMMARY_JSON = (
    "outputs/summary_tables/021_local_2d_detector_candidate_rank_policy_post_sensitivity/"
    "data/local_2d_detector_candidate_rank_policy_summary.json"
)
DEFAULT_BRANCH_RANK_CSV = (
    "outputs/summary_tables/021_local_2d_detector_candidate_rank_policy_post_sensitivity/"
    "data/local_2d_detector_candidate_rank_policy_branch_summary.csv"
)
DEFAULT_ASSIGNMENT_SUMMARY_JSON = (
    "outputs/summary_tables/023_local_2d_detector_blind_assignment_policy_with_span_bonus/"
    "data/local_2d_detector_blind_assignment_policy_summary.json"
)
DEFAULT_ORACLE_SUMMARY_JSON = (
    "outputs/summary_tables/025_local_2d_detector_assignment_failure_taxonomy_policy_oracle/"
    "data/local_2d_detector_assignment_failure_taxonomy_summary.json"
)
DEFAULT_SELECTOR_SUMMARY_JSON = (
    "outputs/summary_tables/026_local_2d_detector_assignment_selector_truth_free_feature_grid/"
    "data/local_2d_detector_assignment_selector_summary.json"
)
DEFAULT_IMAGE_GATE_SUMMARY_JSON = (
    "outputs/summary_tables/027_local_2d_detector_image_objective_gate_saved_bscan/"
    "data/local_2d_detector_image_objective_gate_summary.json"
)


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


def safe_int(value, default: int = 0) -> int:
    number = safe_float(value)
    if not math.isfinite(number):
        return default
    return int(number)


def n_choose_k(n: int, k: int) -> int:
    if n < k:
        return 0
    return math.comb(n, k)


def best_case_count_by_rank(rank_summary: dict, rank_cap: int) -> int:
    values = rank_summary.get("best_case_count_by_rank_cap", {})
    return safe_int(values.get(f"top{rank_cap}"), 0)


def branch_best_case_count(branch_rows: list[dict], rank_cap: int) -> int:
    return sum(safe_int(row.get(f"best_top{rank_cap}_case_count"), 0) for row in branch_rows)


def handoff_row(
    *,
    strategy_key: str,
    strategy_type: str,
    all_truth_case_count: int,
    case_count: int,
    candidate_budget_per_case: int,
    candidate_triples_per_case: int,
    total_candidate_triples: int,
    deployability: str,
    status: str,
    gpu_priority: str,
    interpretation: str,
) -> dict:
    return {
        "strategy_key": strategy_key,
        "strategy_type": strategy_type,
        "all_truth_case_count": all_truth_case_count,
        "case_count": case_count,
        "all_truth_fraction": all_truth_case_count / case_count if case_count else math.nan,
        "candidate_budget_per_case": candidate_budget_per_case,
        "candidate_triples_per_case": candidate_triples_per_case,
        "total_candidate_triples": total_candidate_triples,
        "deployability": deployability,
        "status": status,
        "gpu_priority": gpu_priority,
        "interpretation": interpretation,
    }


def build_handoff_rows(
    *,
    rank_summary: dict,
    branch_rank_rows: list[dict],
    assignment_summary: dict,
    oracle_summary: dict,
    selector_summary: dict,
    image_gate_summary: dict,
) -> list[dict]:
    case_count = safe_int(rank_summary.get("case_count"), 0)
    top10_cases = best_case_count_by_rank(rank_summary, 10)
    top20_branch_cases = branch_best_case_count(branch_rank_rows, 20)
    top40_cases = best_case_count_by_rank(rank_summary, 40)
    return [
        handoff_row(
            strategy_key="shared_top10_candidate_list",
            strategy_type="candidate_list_upper_bound",
            all_truth_case_count=top10_cases,
            case_count=case_count,
            candidate_budget_per_case=10,
            candidate_triples_per_case=n_choose_k(10, 3),
            total_candidate_triples=n_choose_k(10, 3) * case_count,
            deployability="shared_config_candidate_list",
            status="too_low_recall",
            gpu_priority="none",
            interpretation="Top10 is computationally smaller but recovers too few cases.",
        ),
        handoff_row(
            strategy_key="branch_top20_candidate_list",
            strategy_type="candidate_list_upper_bound",
            all_truth_case_count=top20_branch_cases,
            case_count=case_count,
            candidate_budget_per_case=20,
            candidate_triples_per_case=n_choose_k(20, 3),
            total_candidate_triples=n_choose_k(20, 3) * case_count,
            deployability="branch_specific_candidate_list",
            status="truth_containing_but_too_broad_for_fwi",
            gpu_priority="none",
            interpretation="Branch-specific top20 candidate lists cover all cases but imply 1140 triples per case.",
        ),
        handoff_row(
            strategy_key="shared_top40_candidate_list",
            strategy_type="candidate_list_upper_bound",
            all_truth_case_count=top40_cases,
            case_count=case_count,
            candidate_budget_per_case=40,
            candidate_triples_per_case=n_choose_k(40, 3),
            total_candidate_triples=n_choose_k(40, 3) * case_count,
            deployability="shared_config_candidate_list",
            status="truth_containing_but_combinatorial",
            gpu_priority="none",
            interpretation="Shared top40 covers all cases but is far too broad as an ungated FWI handoff.",
        ),
        handoff_row(
            strategy_key="shared_blind_assignment",
            strategy_type="single_triple_selector",
            all_truth_case_count=safe_int(
                assignment_summary.get(
                    "best_unique_all_truth_case_count",
                    assignment_summary.get("best_all_truth_case_count", assignment_summary.get("all_truth_case_count")),
                )
            ),
            case_count=case_count,
            candidate_budget_per_case=1,
            candidate_triples_per_case=1,
            total_candidate_triples=case_count,
            deployability="shared_policy",
            status="deployable_but_low_recall",
            gpu_priority="none",
            interpretation="A deployable shared blind assignment is cheap but recovers too few all-truth cases.",
        ),
        handoff_row(
            strategy_key="per_case_policy_oracle",
            strategy_type="single_triple_selector",
            all_truth_case_count=safe_int(oracle_summary.get("oracle_all_truth_case_count")),
            case_count=case_count,
            candidate_budget_per_case=1,
            candidate_triples_per_case=1,
            total_candidate_triples=case_count,
            deployability="per_case_oracle_not_deployable",
            status="upper_bound_not_policy",
            gpu_priority="none",
            interpretation="The per-case oracle proves exploitable signal, but it is not a blind handoff policy.",
        ),
        handoff_row(
            strategy_key="truth_free_rank_span_selector",
            strategy_type="single_triple_selector",
            all_truth_case_count=safe_int(selector_summary.get("best_in_sample_all_truth_case_count")),
            case_count=case_count,
            candidate_budget_per_case=1,
            candidate_triples_per_case=1,
            total_candidate_triples=case_count,
            deployability="truth_free_selector",
            status="selector_failed",
            gpu_priority="none",
            interpretation="Rank/span/center features did not learn a useful blind assignment selector.",
        ),
        handoff_row(
            strategy_key="saved_bscan_image_objective_gate",
            strategy_type="single_triple_selector",
            all_truth_case_count=safe_int(image_gate_summary.get("primary_objective_all_truth_case_count")),
            case_count=case_count,
            candidate_budget_per_case=1,
            candidate_triples_per_case=1,
            total_candidate_triples=case_count,
            deployability="truth_free_image_gate",
            status="objective_gate_failed",
            gpu_priority="none",
            interpretation="The shallow saved-B-scan image objective chases high-energy central/right cues.",
        ),
    ]


def summarize_handoff(rows: list[dict], rank_summary: dict, oracle_summary: dict, image_gate_summary: dict) -> dict:
    case_count = safe_int(rank_summary.get("case_count"), 0)
    full_candidate_rows = [
        row for row in rows
        if row["all_truth_case_count"] == case_count and row["strategy_type"] == "candidate_list_upper_bound"
    ]
    cheapest_full_candidate = min(
        full_candidate_rows,
        key=lambda row: row["total_candidate_triples"],
        default={},
    )
    deployable_rows = [row for row in rows if row["deployability"] in {"shared_policy", "truth_free_selector", "truth_free_image_gate"}]
    best_deployable = max(
        deployable_rows,
        key=lambda row: row["all_truth_case_count"],
        default={},
    )
    return {
        "policy_label": "local_2d_detector_handoff_budget_cpu_no_fwi",
        "case_count": case_count,
        "strategy_count": len(rows),
        "cheapest_full_candidate_strategy": cheapest_full_candidate.get("strategy_key", ""),
        "cheapest_full_candidate_triples_per_case": safe_int(cheapest_full_candidate.get("candidate_triples_per_case"), 0),
        "cheapest_full_candidate_total_triples": safe_int(cheapest_full_candidate.get("total_candidate_triples"), 0),
        "best_deployable_strategy": best_deployable.get("strategy_key", ""),
        "best_deployable_all_truth_case_count": safe_int(best_deployable.get("all_truth_case_count"), 0),
        "oracle_all_truth_case_count": safe_int(oracle_summary.get("oracle_all_truth_case_count")),
        "image_gate_all_truth_case_count": safe_int(image_gate_summary.get("primary_objective_all_truth_case_count")),
        "minimal_rank_cap_for_full_case_recovery": safe_int(rank_summary.get("minimal_rank_cap_for_full_case_recovery")),
        "ready_for_detector_seeded_fwi": False,
        "immediate_gpu_candidate_count": 0,
        "conditional_gpu_candidate_count": 0,
        "gpu_priority": "none",
        "decision": (
            "Do not launch detector-seeded FWI from the current handoff. The saved detector can "
            "make truth-containing candidate lists, but the cheapest all-case candidate-list handoff "
            "still implies 1140 candidate triples per case under branch-specific top20 settings. "
            "Deployable single-triple selectors are cheap but low-recall, while the per-case oracle "
            "is not deployable. A stronger CPU waveform/objective gate must shrink the candidate "
            "triple set before any GPU/FWI run."
        ),
    }


def strategy_color(row: dict) -> str:
    status = str(row.get("status", ""))
    if status in {"too_low_recall", "deployable_but_low_recall", "selector_failed", "objective_gate_failed"}:
        return "#c7302b"
    if status in {"truth_containing_but_too_broad_for_fwi", "truth_containing_but_combinatorial"}:
        return "#d98c20"
    if status == "upper_bound_not_policy":
        return "#9467bd"
    return "#4c78a8"


def plot_handoff(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["strategy_key"].replace("_", "\n") for row in rows]
    all_truth = [row["all_truth_case_count"] for row in rows]
    triples = [max(1, row["total_candidate_triples"]) for row in rows]
    colors = [strategy_color(row) for row in rows]
    x = np.arange(len(rows))

    fig, axes = plt.subplots(1, 2, figsize=(16.0, 5.7), constrained_layout=True)
    axes[0].bar(x, all_truth, color=colors, width=0.64)
    axes[0].axhline(summary["case_count"], color="#333333", linestyle="--", linewidth=0.9)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylabel("all-truth cases")
    axes[0].set_title("Handoff recall")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, triples, color=colors, width=0.64)
    axes[1].set_yscale("log")
    axes[1].set_xticks(x, labels, fontsize=8)
    axes[1].set_ylabel("candidate triples, log scale")
    axes[1].set_title("FWI handoff budget")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        (
            f"cheapest full candidate set:\n"
            f"{summary['cheapest_full_candidate_strategy']}\n"
            f"{summary['cheapest_full_candidate_total_triples']} total triples\n"
            "GPU priority: none"
        ),
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("Local 2D detector-to-FWI handoff budget", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_handoff_budget.png`",
                "",
                "This CPU-only synthesis compares detector candidate-list recall,",
                "blind assignment, per-case oracle assignment, and saved-B-scan",
                "image-objective gating as possible detector-to-FWI handoffs.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Strategies: `{summary['strategy_count']}`.",
                f"Cheapest full candidate strategy: `{summary['cheapest_full_candidate_strategy']}`.",
                f"Cheapest full candidate triples per case: `{summary['cheapest_full_candidate_triples_per_case']}`.",
                f"Best deployable all-truth cases: `{summary['best_deployable_all_truth_case_count']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Strategy rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The budget reads saved detector summaries only. It does not run",
                "detectors, FDTD, FWI, GPU kernels, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-summary-json", default=DEFAULT_RANK_SUMMARY_JSON)
    parser.add_argument("--branch-rank-csv", default=DEFAULT_BRANCH_RANK_CSV)
    parser.add_argument("--assignment-summary-json", default=DEFAULT_ASSIGNMENT_SUMMARY_JSON)
    parser.add_argument("--oracle-summary-json", default=DEFAULT_ORACLE_SUMMARY_JSON)
    parser.add_argument("--selector-summary-json", default=DEFAULT_SELECTOR_SUMMARY_JSON)
    parser.add_argument("--image-gate-summary-json", default=DEFAULT_IMAGE_GATE_SUMMARY_JSON)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="local_2d_detector_handoff_budget")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rank_summary = read_json(Path(args.rank_summary_json))
    branch_rank_rows = read_csv_rows(Path(args.branch_rank_csv))
    assignment_summary = read_json(Path(args.assignment_summary_json))
    oracle_summary = read_json(Path(args.oracle_summary_json))
    selector_summary = read_json(Path(args.selector_summary_json))
    image_gate_summary = read_json(Path(args.image_gate_summary_json))

    rows = build_handoff_rows(
        rank_summary=rank_summary,
        branch_rank_rows=branch_rank_rows,
        assignment_summary=assignment_summary,
        oracle_summary=oracle_summary,
        selector_summary=selector_summary,
        image_gate_summary=image_gate_summary,
    )
    summary = summarize_handoff(rows, rank_summary, oracle_summary, image_gate_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_handoff_budget_rows.csv"
    summary_json = data_dir / "local_2d_detector_handoff_budget_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_handoff_budget.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_handoff(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_handoff_budget",
        {
            "rank_summary_json": args.rank_summary_json,
            "branch_rank_csv": args.branch_rank_csv,
            "assignment_summary_json": args.assignment_summary_json,
            "oracle_summary_json": args.oracle_summary_json,
            "selector_summary_json": args.selector_summary_json,
            "image_gate_summary_json": args.image_gate_summary_json,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
