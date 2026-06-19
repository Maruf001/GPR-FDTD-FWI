#!/usr/bin/env python3
"""Evaluate blind multi-rebar assignment policies over saved detector B-scans."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
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
from inversion.rebar_detection import assign_rebar_candidates, detect_rebar_candidates  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_baseline_synthesis import unique_truth_assignment  # noqa: E402
from run_local_2d_detector_parameter_sensitivity import (  # noqa: E402
    DEFAULT_COMMAND_PLAN_RUN,
    config_rows,
    detection_npz_path,
    parse_bool,
    safe_float,
)
from run_rebar_detection_pipeline import parse_mm_range, truth_match_metrics  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


CANDIDATE_BUDGETS = (10, 20, 40)
MIN_X_SEPARATIONS_MM = (8.0, 12.0, 20.0, 45.0)
ASSIGNMENT_METHODS = (
    ("score", 0.0),
    ("span0p5", 0.5),
    ("span1", 1.0),
    ("span2", 2.0),
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def assignment_policy_rows() -> list[dict]:
    rows = []
    for method, span_bonus in ASSIGNMENT_METHODS:
        for budget in CANDIDATE_BUDGETS:
            for min_x_sep in MIN_X_SEPARATIONS_MM:
                key = f"top{budget}_minx{min_x_sep:g}"
                if method != "score":
                    key = f"{key}_{method}"
                rows.append({
                    "assignment_policy_key": key,
                    "assignment_method": method,
                    "span_bonus_weight": float(span_bonus),
                    "candidate_budget": int(budget),
                    "min_x_separation_mm": float(min_x_sep),
                })
    return rows


def candidate_row(candidate, rank: int) -> dict:
    row = candidate.as_mm()
    row["rank"] = int(rank)
    return row


def assignment_score(combo, span_bonus_weight: float) -> float:
    base_score = sum(float(candidate.normalized_score) for candidate in combo)
    if float(span_bonus_weight) == 0.0:
        return base_score
    xs_mm = [float(candidate.x_m) * 1000.0 for candidate in combo]
    span_score = (max(xs_mm) - min(xs_mm)) / 100.0
    return base_score + float(span_bonus_weight) * span_score


def try_assign_candidates(
    candidates,
    target_count: int,
    candidate_budget: int,
    min_x_separation_mm: float,
    span_bonus_weight: float = 0.0,
) -> tuple[list, str]:
    subset = list(candidates[: int(candidate_budget)])
    if len(subset) < int(target_count):
        return [], "not_enough_candidates"
    if float(span_bonus_weight) != 0.0:
        best_combo = None
        best_score = None
        min_x_m = float(min_x_separation_mm) / 1000.0
        for combo in itertools.combinations(subset, int(target_count)):
            xs = sorted(candidate.x_m for candidate in combo)
            if any((right - left) < min_x_m for left, right in zip(xs[:-1], xs[1:])):
                continue
            score = assignment_score(combo, float(span_bonus_weight))
            if best_score is None or score > best_score:
                best_combo = combo
                best_score = score
        if best_combo is None:
            return [], "no_assignment_satisfies_separation"
        return sorted(best_combo, key=lambda candidate: candidate.x_m), "assigned"
    try:
        assigned = assign_rebar_candidates(
            subset,
            int(target_count),
            min_x_separation_mm=float(min_x_separation_mm),
        )
    except ValueError:
        return [], "no_assignment_satisfies_separation"
    return list(assigned), "assigned"


def detect_for_config(
    plan_row: dict,
    config: dict,
    observed: np.ndarray,
    scan_x: np.ndarray,
    time_values: np.ndarray,
) -> list:
    return detect_rebar_candidates(
        observed,
        scan_x,
        time_values,
        x_values_mm=parse_mm_range(plan_row["detector_x_values_mm"]),
        z_values_mm=parse_mm_range(plan_row["detector_z_values_mm"]),
        top_k=int(config["top_k"]),
        background_mode=config["background_mode"],
        x_min_separation_mm=float(config["x_min_separation_mm"]),
        z_min_separation_mm=float(config["z_min_separation_mm"]),
        tx_rx_offset=float(plan_row["tx_rx_offset_mm"]) / 1000.0,
        time_offsets_s=config["time_offsets_s"],
    )


def evaluate_detected_assignment(
    plan_row: dict,
    config: dict,
    assignment_policy: dict,
    candidates: list,
    truth_x: list[float],
    truth_z: list[float],
) -> dict:
    started = time.time()
    assigned, assignment_status = try_assign_candidates(
        candidates,
        len(truth_x),
        int(assignment_policy["candidate_budget"]),
        float(assignment_policy["min_x_separation_mm"]),
        float(assignment_policy.get("span_bonus_weight", 0.0)),
    )
    assigned_rows = [candidate_row(candidate, rank) for rank, candidate in enumerate(assigned, start=1)]
    metrics = truth_match_metrics(
        assigned,
        truth_x,
        truth_z,
        safe_float(plan_row["truth_tolerance_mm"], 8.0),
        safe_float(plan_row["truth_tolerance_mm"], 8.0),
    )
    truth_hits = [bool(metric["within_tolerance"]) for metric in metrics]
    unique_assignment = unique_truth_assignment(assigned_rows, metrics)
    unique_hits = unique_assignment["unique_truth_hits"]
    return {
        "branch_key": plan_row["branch_key"],
        "seed": int(plan_row["seed"]),
        "case_variant": plan_row["case_variant"],
        "run_name": plan_row["run_name"],
        "config_key": config["config_key"],
        "background_mode": config["background_mode"],
        "top_k": int(config["top_k"]),
        "separation_profile": config["separation_profile"],
        "time_offset_family": config["time_offset_family"],
        "assignment_policy_key": assignment_policy["assignment_policy_key"],
        "assignment_method": assignment_policy.get("assignment_method", "score"),
        "span_bonus_weight": float(assignment_policy.get("span_bonus_weight", 0.0)),
        "candidate_budget": int(assignment_policy["candidate_budget"]),
        "min_x_separation_mm": float(assignment_policy["min_x_separation_mm"]),
        "detected_candidate_count": len(candidates),
        "assignment_status": assignment_status,
        "assigned_candidate_count": len(assigned),
        "assigned_x_values_mm": ",".join(f"{candidate.x_m * 1000.0:g}" for candidate in assigned),
        "assigned_z_values_mm": ",".join(f"{candidate.z_m * 1000.0:g}" for candidate in assigned),
        "assigned_detection_ranks": ",".join(
            str(next((rank for rank, candidate in enumerate(candidates, start=1) if candidate == assigned_candidate), ""))
            for assigned_candidate in assigned
        ),
        "all_truths_within_tolerance": all(truth_hits),
        "truth_hit_count": sum(truth_hits),
        "target0_hit": truth_hits[0] if len(truth_hits) > 0 else False,
        "target1_hit": truth_hits[1] if len(truth_hits) > 1 else False,
        "target2_hit": truth_hits[2] if len(truth_hits) > 2 else False,
        "unique_truth_hit_count": unique_assignment["unique_truth_hit_count"],
        "unique_all_truths_within_tolerance": unique_assignment["unique_truth_hit_count"] == len(metrics),
        "unique_target0_hit": unique_hits[0] if len(unique_hits) > 0 else False,
        "unique_target1_hit": unique_hits[1] if len(unique_hits) > 1 else False,
        "unique_target2_hit": unique_hits[2] if len(unique_hits) > 2 else False,
        "assigned_truth_ranks": ",".join(str(rank) for rank in unique_assignment["assigned_candidate_ranks"]),
        "elapsed_time_s": float(time.time() - started),
    }


def evaluate_case(plan_row: dict, configs: list[dict], assignment_policies: list[dict]) -> list[dict]:
    with np.load(detection_npz_path(plan_row)) as npz:
        observed = np.asarray(npz["observed_bscan"], dtype=np.float64)
        scan_x = np.asarray(npz["scan_x"], dtype=np.float64)
        time_values = np.asarray(npz["time"], dtype=np.float64)
        truth_x = [float(value) for value in npz["truth_x_values_mm"]]
        truth_z = [float(value) for value in npz["truth_z_values_mm"]]

    rows = []
    for config in configs:
        candidates = detect_for_config(plan_row, config, observed, scan_x, time_values)
        for assignment_policy in assignment_policies:
            rows.append(evaluate_detected_assignment(
                plan_row,
                config,
                assignment_policy,
                candidates,
                truth_x,
                truth_z,
            ))
    return rows


def sort_rows(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            str(row["branch_key"]),
            int(row["seed"]),
            str(row["case_variant"]),
            str(row["run_name"]),
            str(row["config_key"]),
            str(row["assignment_policy_key"]),
        ),
    )


def summarize_by_policy(rows: list[dict]) -> list[dict]:
    out = []
    for key in sorted({(row["config_key"], row["assignment_policy_key"]) for row in rows}):
        config_key, policy_key = key
        policy_rows = [
            row for row in rows
            if row["config_key"] == config_key and row["assignment_policy_key"] == policy_key
        ]
        first = policy_rows[0]
        out.append({
            "config_key": config_key,
            "assignment_policy_key": policy_key,
            "assignment_method": first.get("assignment_method", "score"),
            "span_bonus_weight": float(first.get("span_bonus_weight", 0.0)),
            "background_mode": first["background_mode"],
            "top_k": int(first["top_k"]),
            "separation_profile": first["separation_profile"],
            "time_offset_family": first["time_offset_family"],
            "candidate_budget": int(first["candidate_budget"]),
            "min_x_separation_mm": float(first["min_x_separation_mm"]),
            "case_count": len(policy_rows),
            "assigned_case_count": sum(row["assignment_status"] == "assigned" for row in policy_rows),
            "all_truth_case_count": sum(bool(row["all_truths_within_tolerance"]) for row in policy_rows),
            "unique_all_truth_case_count": sum(bool(row["unique_all_truths_within_tolerance"]) for row in policy_rows),
            "unique_target0_hit_count": sum(bool(row["unique_target0_hit"]) for row in policy_rows),
            "unique_target1_hit_count": sum(bool(row["unique_target1_hit"]) for row in policy_rows),
            "unique_target2_hit_count": sum(bool(row["unique_target2_hit"]) for row in policy_rows),
            "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count"] for row in policy_rows])),
            "mean_elapsed_time_s": float(np.mean([row["elapsed_time_s"] for row in policy_rows])),
        })
    return sorted(
        out,
        key=lambda row: (
            -int(row["unique_all_truth_case_count"]),
            -float(row["mean_unique_truth_hit_count"]),
            int(row["candidate_budget"]),
            float(row["min_x_separation_mm"]),
            str(row["config_key"]),
        ),
    )


def summarize_by_branch(rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in rows}):
        branch_rows = [row for row in rows if row["branch_key"] == branch]
        best = max(
            summarize_by_policy(branch_rows),
            key=lambda row: (
                int(row["unique_all_truth_case_count"]),
                float(row["mean_unique_truth_hit_count"]),
                -int(row["candidate_budget"]),
                -float(row["min_x_separation_mm"]),
            ),
        )
        out.append({
            "branch_key": branch,
            "case_count": len({(row["seed"], row["case_variant"], row["run_name"]) for row in branch_rows}),
            "best_config_key": best["config_key"],
            "best_assignment_policy_key": best["assignment_policy_key"],
            "best_unique_all_truth_case_count": best["unique_all_truth_case_count"],
            "best_mean_unique_truth_hit_count": best["mean_unique_truth_hit_count"],
            "best_candidate_budget": best["candidate_budget"],
            "best_min_x_separation_mm": best["min_x_separation_mm"],
        })
    return out


def summarize(rows: list[dict], policy_summary: list[dict], branch_summary: list[dict]) -> dict:
    case_count = len({(row["branch_key"], row["seed"], row["case_variant"], row["run_name"]) for row in rows})
    best = policy_summary[0] if policy_summary else {}
    full_policy_count = sum(int(row["unique_all_truth_case_count"]) == case_count for row in policy_summary)
    if full_policy_count:
        decision = (
            "At least one blind score/diversity assignment policy recovers all cases. A bounded detector-to-FWI "
            "pilot can use that assignment as a non-oracle initialization candidate."
        )
    elif best:
        decision = (
            "No blind score/diversity assignment policy recovers all cases. The detector still supplies useful "
            "candidate lists, but detector-to-FWI should be framed as rank-gated or oracle/upper-bound unless "
            "a stronger assignment rule is introduced."
        )
    else:
        decision = "No assignment policies were evaluated."
    return {
        "policy_label": "local_2d_detector_blind_assignment_policy_saved_bscan_cpu",
        "case_count": case_count,
        "case_policy_row_count": len(rows),
        "config_assignment_policy_count": len(policy_summary),
        "full_recovery_policy_count": full_policy_count,
        "best_config_key": best.get("config_key", ""),
        "best_assignment_policy_key": best.get("assignment_policy_key", ""),
        "best_unique_all_truth_case_count": best.get("unique_all_truth_case_count", 0),
        "best_mean_unique_truth_hit_count": best.get("mean_unique_truth_hit_count", 0.0),
        "branch_row_count": len(branch_summary),
        "gpu_used": False,
        "backend": "saved_bscan_cpu_detector_assignment",
        "decision": decision,
    }


def plot_assignment_policy(policy_summary: list[dict], branch_summary: list[dict], summary: dict, save_path: Path) -> str:
    top = policy_summary[:12]
    labels = [f"{row['config_key']}\n{row['assignment_policy_key']}".replace("_", "\n") for row in top]
    values = [row["unique_all_truth_case_count"] for row in top]

    fig, axes = plt.subplots(1, 2, figsize=(16.0, 5.4), constrained_layout=True)
    x = np.arange(len(top))
    axes[0].bar(x, values, color="#4c78a8", edgecolor="#333333", linewidth=0.4)
    axes[0].set_xticks(x, labels, fontsize=6)
    axes[0].set_ylabel("all-truth cases")
    axes[0].set_title("Best blind assignment policies")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    branches = [row["branch_key"] for row in branch_summary]
    branch_values = [row["best_unique_all_truth_case_count"] for row in branch_summary]
    axes[1].bar(np.arange(len(branches)), branch_values, color="#59a14f", width=0.58)
    axes[1].set_xticks(np.arange(len(branches)), [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[1].set_ylim(0, max([row["case_count"] for row in branch_summary] + [1]) + 1)
    axes[1].set_title("Branch-best blind assignment recovery")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector blind-assignment policy", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_blind_assignment_policy.png`",
                "",
                "This figure summarizes blind score/diversity assignment policies over saved",
                "detector B-scans. It does not rerun FDTD, FWI, GPU kernels, field FWI,",
                "or 3D/HPC work.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Case/policy rows: `{summary['case_policy_row_count']}`.",
                f"Best config: `{summary['best_config_key']}`.",
                f"Best assignment policy: `{summary['best_assignment_policy_key']}`.",
                f"Best all-truth cases: `{summary['best_unique_all_truth_case_count']}`.",
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
    parser.add_argument("--command-plan-run", default=DEFAULT_COMMAND_PLAN_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_blind_assignment_policy")
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--workers", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plan_dir = Path(args.summary_root) / args.command_plan_run
    plan_rows = read_csv_rows(plan_dir / "data/local_2d_detector_baseline_command_plan_rows.csv")
    missing = [row["run_name"] for row in plan_rows if not parse_bool(row.get("skip_existing"))]
    if missing:
        raise RuntimeError(f"saved detector B-scans are missing: {missing}")

    configs = config_rows()
    assignment_policies = assignment_policy_rows()
    started = time.time()
    rows = []
    if int(args.workers) <= 1:
        for plan_row in plan_rows:
            rows.extend(evaluate_case(plan_row, configs, assignment_policies))
    else:
        with ProcessPoolExecutor(max_workers=int(args.workers)) as executor:
            futures = [
                executor.submit(evaluate_case, plan_row, configs, assignment_policies)
                for plan_row in plan_rows
            ]
            for future in as_completed(futures):
                rows.extend(future.result())
    rows = sort_rows(rows)
    policy_summary = summarize_by_policy(rows)
    branch_summary = summarize_by_branch(rows)
    summary = summarize(rows, policy_summary, branch_summary)
    summary["elapsed_time_s"] = float(time.time() - started)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_blind_assignment_policy_rows.csv"
    policy_csv = data_dir / "local_2d_detector_blind_assignment_policy_summary.csv"
    branch_csv = data_dir / "local_2d_detector_blind_assignment_policy_branch_summary.csv"
    summary_json = data_dir / "local_2d_detector_blind_assignment_policy_summary.json"
    figure_path = figures_dir / "local_2d_detector_blind_assignment_policy.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(policy_csv, [json_safe(row) for row in policy_summary])
    write_csv(branch_csv, [json_safe(row) for row in branch_summary])
    plot_assignment_policy(policy_summary, branch_summary, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "policy_csv": str(policy_csv),
        "branch_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_blind_assignment_policy",
        {
            "command_plan_run": args.command_plan_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
