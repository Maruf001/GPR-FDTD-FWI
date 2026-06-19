#!/usr/bin/env python3
"""Summarize failure modes from saved local 2D detector assignment policies."""

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
from run_local_2d_detector_baseline_synthesis import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ASSIGNMENT_RUN = "023_local_2d_detector_blind_assignment_policy_with_span_bonus"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


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


def hit_tuple(row: dict) -> tuple[bool, bool, bool]:
    return (
        parse_bool(row.get("unique_target0_hit")),
        parse_bool(row.get("unique_target1_hit")),
        parse_bool(row.get("unique_target2_hit")),
    )


def failure_label(row: dict) -> str:
    if row.get("assignment_status") != "assigned":
        return str(row.get("assignment_status", "not_assigned"))
    hits = hit_tuple(row)
    if hits == (True, True, True):
        return "all_truth"
    if hits == (False, False, False):
        return "no_truth"
    missed = [f"target{idx}" for idx, hit in enumerate(hits) if not hit]
    if hits == (False, True, False):
        return "middle_only_target0_target2_missed"
    return "_".join(missed) + "_missed"


def row_score(row: dict) -> tuple:
    assigned_ranks = parse_int_list(row.get("assigned_detection_ranks"))
    max_rank = max(assigned_ranks) if assigned_ranks else 10_000
    return (
        int(row.get("assignment_status") == "assigned"),
        int(parse_bool(row.get("unique_all_truths_within_tolerance"))),
        int(safe_float(row.get("unique_truth_hit_count"), 0.0)),
        int(parse_bool(row.get("unique_target0_hit"))),
        int(parse_bool(row.get("unique_target2_hit"))),
        int(parse_bool(row.get("unique_target1_hit"))),
        -max_rank,
        -int(safe_float(row.get("candidate_budget"), 0.0)),
        -safe_float(row.get("min_x_separation_mm"), 0.0),
    )


def best_case_rows(rows: list[dict]) -> list[dict]:
    out = []
    case_keys = sorted({(row["branch_key"], row["seed"], row["case_variant"], row["run_name"]) for row in rows})
    for branch, seed, variant, run_name in case_keys:
        case_rows = [
            row
            for row in rows
            if row["branch_key"] == branch
            and row["seed"] == seed
            and row["case_variant"] == variant
            and row["run_name"] == run_name
        ]
        best = max(case_rows, key=row_score)
        assigned_x = parse_float_list(best.get("assigned_x_values_mm"))
        assigned_ranks = parse_int_list(best.get("assigned_detection_ranks"))
        hits = hit_tuple(best)
        out.append({
            "branch_key": branch,
            "seed": int(seed),
            "case_variant": variant,
            "run_name": run_name,
            "best_config_key": best["config_key"],
            "best_assignment_policy_key": best["assignment_policy_key"],
            "best_assignment_method": best.get("assignment_method", "score"),
            "best_candidate_budget": int(safe_float(best.get("candidate_budget"), 0.0)),
            "best_min_x_separation_mm": safe_float(best.get("min_x_separation_mm")),
            "best_assignment_status": best.get("assignment_status", ""),
            "best_unique_truth_hit_count": int(safe_float(best.get("unique_truth_hit_count"), 0.0)),
            "best_unique_all_truths_within_tolerance": parse_bool(best.get("unique_all_truths_within_tolerance")),
            "best_unique_target0_hit": hits[0],
            "best_unique_target1_hit": hits[1],
            "best_unique_target2_hit": hits[2],
            "failure_label": failure_label(best),
            "assigned_x_values_mm": best.get("assigned_x_values_mm", ""),
            "assigned_detection_ranks": best.get("assigned_detection_ranks", ""),
            "assigned_x_span_mm": (max(assigned_x) - min(assigned_x)) if assigned_x else math.nan,
            "max_assigned_detection_rank": max(assigned_ranks) if assigned_ranks else math.nan,
        })
    return out


def branch_summary_rows(case_rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in case_rows}):
        rows = [row for row in case_rows if row["branch_key"] == branch]
        labels = Counter(row["failure_label"] for row in rows)
        out.append({
            "branch_key": branch,
            "case_count": len(rows),
            "all_truth_case_count": sum(bool(row["best_unique_all_truths_within_tolerance"]) for row in rows),
            "target0_hit_count": sum(bool(row["best_unique_target0_hit"]) for row in rows),
            "target1_hit_count": sum(bool(row["best_unique_target1_hit"]) for row in rows),
            "target2_hit_count": sum(bool(row["best_unique_target2_hit"]) for row in rows),
            "mean_unique_truth_hit_count": float(np.mean([row["best_unique_truth_hit_count"] for row in rows])),
            "dominant_failure_label": labels.most_common(1)[0][0] if labels else "",
            "failure_label_counts": json.dumps(dict(sorted(labels.items()))),
            "mean_assigned_x_span_mm": float(np.nanmean([row["assigned_x_span_mm"] for row in rows])),
            "mean_max_assigned_detection_rank": float(np.nanmean([row["max_assigned_detection_rank"] for row in rows])),
        })
    return out


def method_summary_rows(case_rows: list[dict]) -> list[dict]:
    out = []
    for method in sorted({row["best_assignment_method"] for row in case_rows}):
        rows = [row for row in case_rows if row["best_assignment_method"] == method]
        out.append({
            "assignment_method": method,
            "best_case_count": len(rows),
            "all_truth_case_count": sum(bool(row["best_unique_all_truths_within_tolerance"]) for row in rows),
            "mean_unique_truth_hit_count": float(np.mean([row["best_unique_truth_hit_count"] for row in rows])),
        })
    return out


def summarize(
    case_rows: list[dict],
    branch_rows: list[dict],
    method_rows: list[dict],
    shared_policy_summary: dict | None = None,
) -> dict:
    case_count = len(case_rows)
    all_truth = sum(bool(row["best_unique_all_truths_within_tolerance"]) for row in case_rows)
    dominant = Counter(row["failure_label"] for row in case_rows).most_common(1)
    shared_policy_summary = shared_policy_summary or {}
    shared_all_truth = shared_policy_summary.get("best_unique_all_truth_case_count")
    shared_mean_hits = shared_policy_summary.get("best_mean_unique_truth_hit_count")
    return {
        "policy_label": "local_2d_detector_assignment_failure_taxonomy_per_case_policy_oracle",
        "selection_scope": "per_case_best_assignment_policy_oracle",
        "case_count": case_count,
        "oracle_all_truth_case_count": all_truth,
        "all_truth_case_count": all_truth,
        "target0_hit_count": sum(bool(row["best_unique_target0_hit"]) for row in case_rows),
        "target1_hit_count": sum(bool(row["best_unique_target1_hit"]) for row in case_rows),
        "target2_hit_count": sum(bool(row["best_unique_target2_hit"]) for row in case_rows),
        "mean_unique_truth_hit_count": float(np.mean([row["best_unique_truth_hit_count"] for row in case_rows])),
        "deployable_shared_policy_all_truth_case_count": shared_all_truth,
        "deployable_shared_policy_mean_unique_truth_hit_count": shared_mean_hits,
        "deployable_shared_policy_config_key": shared_policy_summary.get("best_config_key"),
        "deployable_shared_assignment_policy_key": shared_policy_summary.get("best_assignment_policy_key"),
        "dominant_failure_label": dominant[0][0] if dominant else "",
        "dominant_failure_count": dominant[0][1] if dominant else 0,
        "branch_row_count": len(branch_rows),
        "method_row_count": len(method_rows),
        "gpu_used": False,
        "backend": "saved_assignment_rows_cpu_taxonomy",
        "decision": (
            "This is a per-case policy-oracle over saved blind-assignment rows, not a deployable shared "
            "policy. It shows exploitable signal in the candidate lists, but the best shared blind policy "
            "still fails most cases. Use this taxonomy to design a stronger assignment-policy selector or "
            "downstream objective gate before any detector-to-FWI handoff."
        ),
    }


def plot_taxonomy(case_rows: list[dict], branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    branches = [row["branch_key"] for row in branch_rows]
    target0 = [row["target0_hit_count"] for row in branch_rows]
    target1 = [row["target1_hit_count"] for row in branch_rows]
    target2 = [row["target2_hit_count"] for row in branch_rows]

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.2), constrained_layout=True)
    x = np.arange(len(branches))
    width = 0.25
    axes[0].bar(x - width, target0, width=width, label="target0")
    axes[0].bar(x, target1, width=width, label="target1")
    axes[0].bar(x + width, target2, width=width, label="target2")
    axes[0].set_xticks(x, [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[0].set_ylim(0, max([row["case_count"] for row in branch_rows] + [1]) + 1)
    axes[0].set_title("Per-case policy-oracle target hits by branch")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    labels = sorted({row["failure_label"] for row in case_rows})
    counts = [sum(row["failure_label"] == label for row in case_rows) for label in labels]
    axes[1].bar(np.arange(len(labels)), counts, color="#9c755f", width=0.58)
    axes[1].set_xticks(np.arange(len(labels)), [label.replace("_", "\n") for label in labels], fontsize=8)
    axes[1].set_title("Per-case policy-oracle failure labels")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector assignment policy-oracle taxonomy", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_assignment_failure_taxonomy.png`",
                "",
                "This figure summarizes a per-case policy-oracle: for each saved",
                "close14/close50 detector case, it picks the best row from the saved",
                "blind-assignment grid. It is not a deployable shared policy result.",
                "It reads saved assignment rows only and does not rerun FDTD, FWI,",
                "GPU kernels, field FWI, or 3D/HPC work.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Selection scope: `{summary['selection_scope']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Per-case oracle all-truth cases: `{summary['oracle_all_truth_case_count']}`.",
                "Best deployable shared-policy all-truth cases: "
                f"`{summary['deployable_shared_policy_all_truth_case_count']}`.",
                f"Dominant failure: `{summary['dominant_failure_label']}`.",
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
    parser.add_argument("--run-name", default="local_2d_detector_assignment_failure_taxonomy")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    assignment_dir = Path(args.summary_root) / args.assignment_run
    rows = read_csv_rows(assignment_dir / "data/local_2d_detector_blind_assignment_policy_rows.csv")
    shared_summary_path = assignment_dir / "data/local_2d_detector_blind_assignment_policy_summary.json"
    shared_summary = {}
    if shared_summary_path.exists():
        shared_summary = json.loads(shared_summary_path.read_text(encoding="utf-8"))
    case_rows = best_case_rows(rows)
    branch_rows = branch_summary_rows(case_rows)
    method_rows = method_summary_rows(case_rows)
    summary = summarize(case_rows, branch_rows, method_rows, shared_summary)
    summary["source_assignment_run"] = args.assignment_run

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_assignment_failure_taxonomy_cases.csv"
    branch_csv = data_dir / "local_2d_detector_assignment_failure_taxonomy_branch_summary.csv"
    method_csv = data_dir / "local_2d_detector_assignment_failure_taxonomy_method_summary.csv"
    summary_json = data_dir / "local_2d_detector_assignment_failure_taxonomy_summary.json"
    figure_path = figures_dir / "local_2d_detector_assignment_failure_taxonomy.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(case_csv, [json_safe(row) for row in case_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(method_csv, [json_safe(row) for row in method_rows])
    plot_taxonomy(case_rows, branch_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "case_csv": str(case_csv),
        "branch_csv": str(branch_csv),
        "method_csv": str(method_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_assignment_failure_taxonomy",
        {
            "assignment_run": args.assignment_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
