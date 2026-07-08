#!/usr/bin/env python3
"""Triage detector separability blockers from saved feature-audit outputs."""

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
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SEPARABILITY_RUN = "105_local_2d_detector_feature_separability_audit_post_upper_bound"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def budget_label(rank: float) -> str:
    if not math.isfinite(rank):
        return "truth_missing"
    if rank <= 1:
        return "top1"
    if rank <= 10:
        return "top10"
    if rank <= 50:
        return "top50"
    if rank <= 200:
        return "top200"
    return "deeper_than_top200"


def blocker_label(best_rank: float, cv_rank: float) -> str:
    if best_rank > 200 or not math.isfinite(best_rank):
        return "candidate_space_gap"
    if cv_rank <= 1:
        return "no_blocker_top1_cv"
    if cv_rank <= 50:
        return "top1_selector_gap_rank_gate_ok"
    if cv_rank <= 200:
        return "cv_rank_gate_deep_but_bounded"
    return "feature_generalization_failure"


def recommended_next(row: dict) -> str:
    label = row["blocker_label"]
    if label == "feature_generalization_failure":
        return "branch_conditioned_cpu_selector_or_holdout_robustness_audit"
    if label == "cv_rank_gate_deep_but_bounded":
        return "keep_as_rank_gated_upper_bound_do_not_launch_fwi"
    if label == "top1_selector_gap_rank_gate_ok":
        return "report_detector_as_candidate_list_baseline"
    if label == "candidate_space_gap":
        return "do_not_use_detector_handoff_without_new_candidate_generation"
    return "no_detector_followup_needed"


def leave_one_case_lookup(cv_rows: list[dict]) -> dict[str, dict]:
    return {row["case_label"]: row for row in cv_rows if row.get("cv_strategy") == "leave_one_case"}


def build_case_triage_rows(case_rows: list[dict], cv_rows: list[dict]) -> list[dict]:
    cv_lookup = leave_one_case_lookup(cv_rows)
    out = []
    for row in case_rows:
        cv = cv_lookup.get(row["case_label"], {})
        best_rank = safe_float(row.get("best_first_all_truth_rank"), math.inf)
        cv_rank = safe_float(cv.get("first_all_truth_rank"), math.inf)
        triage = {
            "case_label": row["case_label"],
            "branch_key": row["branch_key"],
            "seed": safe_int(row["seed"]),
            "case_variant": row["case_variant"],
            "all_truth_triple_count": safe_int(row["all_truth_triple_count"]),
            "best_feature": row["best_feature"],
            "best_first_all_truth_rank": best_rank,
            "best_budget_label": budget_label(best_rank),
            "leave_one_feature": cv.get("trained_feature", ""),
            "leave_one_first_all_truth_rank": cv_rank,
            "leave_one_budget_label": budget_label(cv_rank),
            "leave_one_top_truth_hit_count": safe_int(cv.get("top_unique_truth_hit_count")),
            "leave_one_top_candidate_x_values_mm": cv.get("top_candidate_x_values_mm", ""),
            "best_false_minus_truth_score_gap": safe_float(row.get("best_false_minus_truth_score_gap")),
            "positive_gap_feature_count": safe_int(row.get("positive_gap_feature_count")),
            "blocker_label": blocker_label(best_rank, cv_rank),
        }
        triage["recommended_next"] = recommended_next(triage)
        out.append(triage)
    return sorted(
        out,
        key=lambda item: (
            item["blocker_label"] != "feature_generalization_failure",
            -safe_float(item["leave_one_first_all_truth_rank"], -math.inf),
            str(item["case_label"]),
        ),
    )


def build_branch_rows(case_rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in case_rows}):
        rows = [row for row in case_rows if row["branch_key"] == branch]
        cv_ranks = [safe_float(row["leave_one_first_all_truth_rank"], math.inf) for row in rows]
        best_ranks = [safe_float(row["best_first_all_truth_rank"], math.inf) for row in rows]
        blockers = Counter(row["blocker_label"] for row in rows)
        out.append(
            {
                "branch_key": branch,
                "case_count": len(rows),
                "best_top10_case_count": sum(rank <= 10 for rank in best_ranks),
                "best_top50_case_count": sum(rank <= 50 for rank in best_ranks),
                "best_top200_case_count": sum(rank <= 200 for rank in best_ranks),
                "leave_one_top50_case_count": sum(rank <= 50 for rank in cv_ranks),
                "leave_one_top200_case_count": sum(rank <= 200 for rank in cv_ranks),
                "feature_generalization_failure_count": blockers["feature_generalization_failure"],
                "dominant_blocker_label": blockers.most_common(1)[0][0] if blockers else "",
                "median_leave_one_rank": float(np.median([rank for rank in cv_ranks if math.isfinite(rank)])) if cv_ranks else math.nan,
                "max_leave_one_rank": max([rank for rank in cv_ranks if math.isfinite(rank)], default=math.nan),
            }
        )
    return out


def summarize_triage(case_rows: list[dict], branch_rows: list[dict], source_summary: dict) -> dict:
    blockers = Counter(row["blocker_label"] for row in case_rows)
    feature_failures = [row for row in case_rows if row["blocker_label"] == "feature_generalization_failure"]
    ready_for_fwi = False
    return {
        "policy_label": "local_2d_detector_separability_blocker_triage_cpu_no_fwi",
        "source_policy_label": source_summary.get("policy_label", ""),
        "case_count": len(case_rows),
        "branch_count": len(branch_rows),
        "all_truth_triple_count": source_summary.get("all_truth_triple_count"),
        "best_top10_case_count": sum(safe_float(row["best_first_all_truth_rank"], math.inf) <= 10 for row in case_rows),
        "best_top50_case_count": sum(safe_float(row["best_first_all_truth_rank"], math.inf) <= 50 for row in case_rows),
        "best_top200_case_count": sum(safe_float(row["best_first_all_truth_rank"], math.inf) <= 200 for row in case_rows),
        "leave_one_top1_case_count": sum(safe_float(row["leave_one_first_all_truth_rank"], math.inf) <= 1 for row in case_rows),
        "leave_one_top50_case_count": sum(safe_float(row["leave_one_first_all_truth_rank"], math.inf) <= 50 for row in case_rows),
        "leave_one_top200_case_count": sum(safe_float(row["leave_one_first_all_truth_rank"], math.inf) <= 200 for row in case_rows),
        "feature_generalization_failure_count": len(feature_failures),
        "feature_generalization_failure_cases": ";".join(row["case_label"] for row in feature_failures),
        "blocker_label_counts": dict(sorted(blockers.items())),
        "ready_for_rank_gated_upper_bound_claim": boolish(source_summary.get("ready_for_rank_gated_upper_bound_claim")),
        "ready_for_detector_seeded_fwi": ready_for_fwi,
        "gpu_priority": "none",
        "decision": (
            "The detector candidate space is sufficient for a rank-gated upper-bound, but the "
            "truth-free feature choice does not generalize. The hardest blockers are close50 "
            "source-mismatch cases where per-case features rank truth within top-10/top-50, but "
            "leave-one-case feature choice pushes truth deeper than top-200. Do not launch "
            "detector-seeded FWI from this selector state."
        ),
    }


def plot_triage(case_rows: list[dict], branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(case_rows, key=lambda row: (row["branch_key"], safe_int(row["seed"]), row["case_variant"]))
    labels = [row["case_label"].replace("target2_", "").replace("|", "\n") for row in ordered]
    best = [safe_float(row["best_first_all_truth_rank"], math.nan) for row in ordered]
    cv = [safe_float(row["leave_one_first_all_truth_rank"], math.nan) for row in ordered]

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.6), constrained_layout=True)
    x = np.arange(len(ordered))
    axes[0].plot(x, best, marker="o", linewidth=2.0, color="#4c78a8", label="best per-case feature")
    axes[0].plot(x, cv, marker="s", linewidth=2.0, color="#e45756", label="leave-one-case feature")
    axes[0].axhline(50, color="#666666", linestyle="--", linewidth=1.0)
    axes[0].axhline(200, color="#999999", linestyle=":", linewidth=1.0)
    axes[0].set_xticks(x, labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("first all-truth rank")
    axes[0].set_title("Best-case vs cross-validated rank")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    branches = [row["branch_key"].replace("target2_", "") for row in branch_rows]
    top50 = [safe_int(row["leave_one_top50_case_count"]) for row in branch_rows]
    top200 = [safe_int(row["leave_one_top200_case_count"]) for row in branch_rows]
    failures = [safe_int(row["feature_generalization_failure_count"]) for row in branch_rows]
    bx = np.arange(len(branches))
    width = 0.25
    axes[1].bar(bx - width, top50, width=width, label="CV top50", color="#54a24b")
    axes[1].bar(bx, top200, width=width, label="CV top200", color="#4c78a8")
    axes[1].bar(bx + width, failures, width=width, label="feature failures", color="#e45756")
    axes[1].set_xticks(bx, branches, fontsize=8)
    axes[1].set_ylim(0, max([row["case_count"] for row in branch_rows] + [1]) + 1)
    axes[1].set_title("Branch-level triage")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle("Local 2D detector separability blocker triage", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_separability_blocker_triage.png`",
                "",
                "This figure triages saved detector feature-separability outputs. It",
                "does not run FDTD, FWI, detector scoring, GPU kernels, field FWI,",
                "3D/HPC work, or neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Best top-50 cases: `{summary['best_top50_case_count']}`.",
                f"Leave-one top-50 cases: `{summary['leave_one_top50_case_count']}`.",
                f"Leave-one top-200 cases: `{summary['leave_one_top200_case_count']}`.",
                f"Feature-generalization failures: `{summary['feature_generalization_failure_count']}`.",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--separability-run", default=DEFAULT_SEPARABILITY_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_separability_blocker_triage")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.summary_root) / args.separability_run / "data"
    case_rows = read_csv_rows(source_dir / "local_2d_detector_feature_separability_case_summary.csv")
    cv_rows = read_csv_rows(source_dir / "local_2d_detector_feature_separability_cv_cases.csv")
    source_summary = read_json(source_dir / "local_2d_detector_feature_separability_summary.json")

    triage_rows = build_case_triage_rows(case_rows, cv_rows)
    branch_rows = build_branch_rows(triage_rows)
    summary = summarize_triage(triage_rows, branch_rows, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    write_csv(data_dir / "local_2d_detector_separability_blocker_cases.csv", triage_rows)
    write_csv(data_dir / "local_2d_detector_separability_blocker_branch_summary.csv", branch_rows)
    summary_path = data_dir / "local_2d_detector_separability_blocker_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    fig_path = figures_dir / "local_2d_detector_separability_blocker_triage.png"
    plot_triage(triage_rows, branch_rows, summary, fig_path)
    write_figure_notes(figures_dir / "FIGURE_NOTES.md", summary)
    write_csv(data_dir / "figure_validation.csv", [figure_stats(fig_path)])
    write_run_manifest(
        str(outdir),
        "local_2d_detector_separability_blocker_triage",
        {
            "summary": json_safe(summary),
            "paths": {
                "source_separability_summary_json": str(source_dir / "local_2d_detector_feature_separability_summary.json"),
                "summary_json": str(summary_path),
                "figure": str(fig_path),
            },
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
