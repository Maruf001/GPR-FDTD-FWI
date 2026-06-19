#!/usr/bin/env python3
"""Synthesize detector rank-gated upper-bound policy without launching FWI."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_csv_rows, read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_HANDOFF_RUN = "029_local_2d_detector_handoff_budget"
DEFAULT_RANK_BUDGET_RUN = "034_local_2d_detector_rank_budget_diagnostic_post_alltriples_gate"
DEFAULT_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
DEFAULT_COMPONENT_SELECTOR_RUN = "037_local_2d_detector_component_selector_audit_post_component_gate"


def best_budget_row(rows: list[dict], budget: int) -> dict:
    budget_rows = [row for row in rows if safe_int(row.get("candidate_triple_budget")) == budget]
    if not budget_rows:
        return {}
    return max(
        budget_rows,
        key=lambda row: (
            safe_int(row.get("first_all_truth_case_count")),
            safe_float(row.get("case_fraction")),
            str(row.get("objective", "")),
        ),
    )


def minimal_all_case_budget(rows: list[dict]) -> tuple[int, str]:
    all_case_rows = [
        row
        for row in rows
        if safe_int(row.get("first_all_truth_case_count")) == safe_int(row.get("case_count"))
    ]
    if not all_case_rows:
        return 0, ""
    best = min(
        all_case_rows,
        key=lambda row: (
            safe_int(row.get("candidate_triple_budget")),
            str(row.get("objective", "")),
        ),
    )
    return safe_int(best.get("candidate_triple_budget")), str(best.get("objective", ""))


def policy_row(
    *,
    strategy: str,
    scope: str,
    case_count: int,
    all_truth_cases: int,
    triples_per_case: int,
    objective: str,
    deployable: bool,
    upper_bound_ready: bool,
    fwi_ready: bool,
    evidence: str,
    interpretation: str,
) -> dict:
    return {
        "strategy": strategy,
        "scope": scope,
        "case_count": case_count,
        "all_truth_case_count": all_truth_cases,
        "all_truth_fraction": all_truth_cases / case_count if case_count else math.nan,
        "candidate_triples_per_case": triples_per_case,
        "objective": objective,
        "deployable_top1_selector": deployable,
        "rank_gated_upper_bound_ready": upper_bound_ready,
        "ready_for_detector_seeded_fwi": fwi_ready,
        "evidence": evidence,
        "interpretation": interpretation,
    }


def build_policy_rows(
    *,
    handoff_summary: dict,
    rank_budget_rows: list[dict],
    component_budget_rows: list[dict],
    selector_summary: dict,
) -> list[dict]:
    case_count = safe_int(handoff_summary.get("case_count"), 12)
    simple_top50 = best_budget_row(rank_budget_rows, 50)
    simple_top200 = best_budget_row(rank_budget_rows, 200)
    component_top50 = best_budget_row(component_budget_rows, 50)
    component_top100 = best_budget_row(component_budget_rows, 100)
    component_top200 = best_budget_row(component_budget_rows, 200)
    component_all_budget, component_all_objective = minimal_all_case_budget(component_budget_rows)
    simple_all_budget, simple_all_objective = minimal_all_case_budget(rank_budget_rows)
    return [
        policy_row(
            strategy="component_selector_validated_top1",
            scope="truth_free_deployable_selector",
            case_count=case_count,
            all_truth_cases=safe_int(selector_summary.get("leave_one_case_all_truth_case_count")),
            triples_per_case=1,
            objective=str(selector_summary.get("best_in_sample_selector_label", "")),
            deployable=True,
            upper_bound_ready=False,
            fwi_ready=False,
            evidence="037_component_selector_leave_one_case",
            interpretation="validated top-1 selector fails; do not use as detector-seeded FWI initializer",
        ),
        policy_row(
            strategy="component_gate_top50_rank_gated",
            scope="rank_gated_partial_upper_bound",
            case_count=case_count,
            all_truth_cases=safe_int(component_top50.get("first_all_truth_case_count")),
            triples_per_case=50,
            objective=str(component_top50.get("objective", "")),
            deployable=False,
            upper_bound_ready=False,
            fwi_ready=False,
            evidence="035_component_gate_budget_curve",
            interpretation="useful partial recall context but not all-case coverage",
        ),
        policy_row(
            strategy="component_gate_top100_rank_gated",
            scope="rank_gated_partial_upper_bound",
            case_count=case_count,
            all_truth_cases=safe_int(component_top100.get("first_all_truth_case_count")),
            triples_per_case=100,
            objective=str(component_top100.get("objective", "")),
            deployable=False,
            upper_bound_ready=False,
            fwi_ready=False,
            evidence="035_component_gate_budget_curve",
            interpretation="near-complete upper-bound context but still misses at least one case",
        ),
        policy_row(
            strategy="component_gate_minimal_all_case_upper_bound",
            scope="rank_gated_all_case_upper_bound",
            case_count=case_count,
            all_truth_cases=safe_int(component_top200.get("first_all_truth_case_count")),
            triples_per_case=component_all_budget,
            objective=component_all_objective,
            deployable=False,
            upper_bound_ready=component_all_budget > 0,
            fwi_ready=False,
            evidence="035_component_gate_budget_curve",
            interpretation="minimal current all-case detector upper-bound; paper context only, not FWI queue",
        ),
        policy_row(
            strategy="simple_gate_minimal_all_case_upper_bound",
            scope="rank_gated_all_case_upper_bound",
            case_count=case_count,
            all_truth_cases=safe_int(simple_top200.get("first_all_truth_case_count")),
            triples_per_case=simple_all_budget,
            objective=simple_all_objective,
            deployable=False,
            upper_bound_ready=simple_all_budget > 0,
            fwi_ready=False,
            evidence="034_rank_budget_curve",
            interpretation="simple-gate all-case upper-bound matches 200 triples/case but is weaker at top50",
        ),
        policy_row(
            strategy="full_branch_top20_candidate_list",
            scope="exhaustive_candidate_list_upper_bound",
            case_count=case_count,
            all_truth_cases=case_count,
            triples_per_case=safe_int(handoff_summary.get("cheapest_full_candidate_triples_per_case")),
            objective=str(handoff_summary.get("cheapest_full_candidate_strategy", "")),
            deployable=False,
            upper_bound_ready=True,
            fwi_ready=False,
            evidence="029_handoff_budget",
            interpretation="complete candidate-list upper-bound but too broad for detector-seeded FWI",
        ),
    ]


def summarize_policy(rows: list[dict], selector_summary: dict, component_summary: dict) -> dict:
    all_case_upper_bounds = [
        row for row in rows
        if bool(row["rank_gated_upper_bound_ready"]) and safe_int(row["all_truth_case_count"]) == safe_int(row["case_count"])
    ]
    best_upper = min(all_case_upper_bounds, key=lambda row: safe_int(row["candidate_triples_per_case"]))
    deployable_rows = [row for row in rows if bool(row["deployable_top1_selector"])]
    best_deployable = max(deployable_rows, key=lambda row: safe_int(row["all_truth_case_count"]))
    return {
        "policy_label": "local_2d_detector_upper_bound_policy_cpu_no_fwi",
        "strategy_count": len(rows),
        "case_count": safe_int(rows[0]["case_count"]) if rows else 0,
        "best_rank_gated_upper_bound_strategy": best_upper["strategy"],
        "best_rank_gated_upper_bound_objective": best_upper["objective"],
        "minimal_all_case_rank_gated_triples_per_case": safe_int(best_upper["candidate_triples_per_case"]),
        "best_rank_gated_upper_bound_all_truth_case_count": safe_int(best_upper["all_truth_case_count"]),
        "component_gate_top50_case_count": safe_int(component_summary.get("best_top50_case_count")),
        "component_gate_top50_improvement_over_simple": safe_int(component_summary.get("top50_improvement_over_source")),
        "best_deployable_selector_strategy": best_deployable["strategy"],
        "best_deployable_selector_all_truth_case_count": safe_int(best_deployable["all_truth_case_count"]),
        "selector_leave_one_case_all_truth_case_count": safe_int(selector_summary.get("leave_one_case_all_truth_case_count")),
        "selector_candidate_count": safe_int(selector_summary.get("selector_candidate_count")),
        "ready_for_rank_gated_upper_bound_claim": True,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use detector evidence as a rank-gated upper-bound and baseline-context result. "
            "The validated truth-free selector has zero leave-one-case top-1 all-truth recoveries, "
            "so detector-seeded FWI remains blocked. The minimal current all-case upper-bound is "
            "component-gated top-200 candidate triples per case."
        ),
    }


def plot_policy(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["strategy"].replace("_", "\n") for row in rows]
    all_truth = [safe_int(row["all_truth_case_count"]) for row in rows]
    budgets = [safe_int(row["candidate_triples_per_case"]) for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(1, 2, figsize=(15.8, 5.4), constrained_layout=True)
    axes[0].bar(x, all_truth, color=["#59a14f" if row["rank_gated_upper_bound_ready"] else "#4e79a7" for row in rows])
    axes[0].set_xticks(x, labels, fontsize=7)
    axes[0].set_ylabel("all-truth cases")
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_title("Detector upper-bound recall")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, budgets, color="#f28e2b")
    axes[1].set_xticks(x, labels, fontsize=7)
    axes[1].set_yscale("log")
    axes[1].set_ylabel("candidate triples per case")
    axes[1].set_title("Budget before any downstream objective")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"upper bound={summary['minimal_all_case_rank_gated_triples_per_case']} triples/case\n"
        f"selector CV={summary['selector_leave_one_case_all_truth_case_count']}/{summary['case_count']}\n"
        "FWI=false",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector upper-bound policy", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_upper_bound_policy.png`",
                "",
                "This CPU-only policy synthesis separates detector rank-gated upper-bound",
                "evidence from deployable detector-seeded FWI readiness.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Best rank-gated upper-bound strategy: `{summary['best_rank_gated_upper_bound_strategy']}`.",
                f"Minimal all-case rank-gated triples per case: `{summary['minimal_all_case_rank_gated_triples_per_case']}`.",
                f"Selector leave-one-case all-truth cases: `{summary['selector_leave_one_case_all_truth_case_count']}`.",
                f"Ready for rank-gated upper-bound claim: `{summary['ready_for_rank_gated_upper_bound_claim']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Policy rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                "",
                "Scope boundary:",
                "",
                "This synthesis reads saved CPU summaries only. It does not run FDTD, FWI,",
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
    parser.add_argument("--handoff-run", default=DEFAULT_HANDOFF_RUN)
    parser.add_argument("--rank-budget-run", default=DEFAULT_RANK_BUDGET_RUN)
    parser.add_argument("--component-gate-run", default=DEFAULT_COMPONENT_GATE_RUN)
    parser.add_argument("--component-selector-run", default=DEFAULT_COMPONENT_SELECTOR_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_upper_bound_policy")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.summary_root)
    handoff_summary = read_json(root / args.handoff_run / "data/local_2d_detector_handoff_budget_summary.json")
    rank_budget_rows = read_csv_rows(root / args.rank_budget_run / "data/local_2d_detector_rank_budget_curve.csv")
    component_budget_rows = read_csv_rows(root / args.component_gate_run / "data/local_2d_detector_component_waveform_gate_budget_curve.csv")
    component_summary = read_json(root / args.component_gate_run / "data/local_2d_detector_component_waveform_gate_summary.json")
    selector_summary = read_json(root / args.component_selector_run / "data/local_2d_detector_component_selector_audit_summary.json")
    policy_rows = build_policy_rows(
        handoff_summary=handoff_summary,
        rank_budget_rows=rank_budget_rows,
        component_budget_rows=component_budget_rows,
        selector_summary=selector_summary,
    )
    summary = summarize_policy(policy_rows, selector_summary, component_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_upper_bound_policy_rows.csv"
    summary_json = data_dir / "local_2d_detector_upper_bound_policy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_upper_bound_policy.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in policy_rows])
    plot_policy(policy_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "policy_rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "handoff_summary_json": str(root / args.handoff_run / "data/local_2d_detector_handoff_budget_summary.json"),
        "rank_budget_curve_csv": str(root / args.rank_budget_run / "data/local_2d_detector_rank_budget_curve.csv"),
        "component_gate_budget_curve_csv": str(root / args.component_gate_run / "data/local_2d_detector_component_waveform_gate_budget_curve.csv"),
        "component_selector_summary_json": str(root / args.component_selector_run / "data/local_2d_detector_component_selector_audit_summary.json"),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_upper_bound_policy",
        {
            "handoff_run": args.handoff_run,
            "rank_budget_run": args.rank_budget_run,
            "component_gate_run": args.component_gate_run,
            "component_selector_run": args.component_selector_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
