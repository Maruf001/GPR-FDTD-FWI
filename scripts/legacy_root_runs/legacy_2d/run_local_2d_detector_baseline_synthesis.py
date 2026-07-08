#!/usr/bin/env python3
"""Synthesize local 2D same-case detector-baseline outputs."""

from __future__ import annotations

import argparse
import csv
import itertools
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


DEFAULT_COMMAND_PLAN_RUN = "017_local_2d_detector_baseline_command_plan_post_interface_patch"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def join_mm(values: list[float]) -> str:
    return ",".join(f"{float(value):g}" for value in values)


def candidate_position_row(candidate, index: int) -> tuple[int, float, float]:
    if isinstance(candidate, dict):
        return (
            int(candidate.get("rank", index + 1)),
            safe_float(candidate.get("x_mm")),
            safe_float(candidate.get("z_mm")),
        )
    if hasattr(candidate, "as_mm"):
        candidate_mm = candidate.as_mm()
        return (
            int(candidate_mm.get("rank", index + 1)),
            safe_float(candidate_mm.get("x_mm")),
            safe_float(candidate_mm.get("z_mm")),
        )
    return (
        int(getattr(candidate, "rank", index + 1)),
        safe_float(getattr(candidate, "x_mm", getattr(candidate, "x_m", math.nan) * 1000.0)),
        safe_float(getattr(candidate, "z_mm", getattr(candidate, "z_m", math.nan) * 1000.0)),
    )


def detection_summary_path(plan_row: dict) -> Path:
    return Path(plan_row["existing_output_dir"]) / "data" / "detection_summary.json"


def case_outcome(branch_key: str, truth_hits: list[bool]) -> str:
    if all(truth_hits):
        return "all_truths_detected"
    if branch_key == "target2_close14" and truth_hits[1:3] == [True, True] and not truth_hits[0]:
        return "close_pair_detected_left_target_missed"
    if truth_hits[1] and not truth_hits[0] and not truth_hits[2]:
        return "middle_target_only_detected"
    if any(truth_hits):
        return "partial_truth_detected"
    return "no_truth_detected"


def unique_truth_assignment(candidates: list[dict], metrics: list[dict], tolerance_x_mm: float = 8.0, tolerance_z_mm: float = 8.0) -> dict:
    truth = [
        (safe_float(metric.get("truth_x_mm")), safe_float(metric.get("truth_z_mm")))
        for metric in metrics
    ]
    if not truth or len(candidates) < len(truth):
        return {
            "unique_truth_hit_count": 0,
            "unique_truth_hits": [False for _ in truth],
            "assigned_candidate_ranks": [],
        }

    candidate_rows = [candidate_position_row(candidate, index) for index, candidate in enumerate(candidates)]
    best = None
    for assigned in itertools.permutations(candidate_rows, len(truth)):
        hits = []
        total_error = 0.0
        for (truth_x, truth_z), (_rank, cand_x, cand_z) in zip(truth, assigned):
            x_error = abs(cand_x - truth_x)
            z_error = abs(cand_z - truth_z)
            hits.append(x_error <= tolerance_x_mm and z_error <= tolerance_z_mm)
            total_error += x_error + z_error
        score = (sum(hits), -total_error)
        if best is None or score > best[0]:
            best = (score, hits, [rank for rank, _x, _z in assigned])
    assert best is not None
    return {
        "unique_truth_hit_count": int(best[0][0]),
        "unique_truth_hits": [bool(hit) for hit in best[1]],
        "assigned_candidate_ranks": best[2],
    }


def build_case_row(plan_row: dict, detection_summary: dict) -> dict:
    metrics = detection_summary.get("match_metrics", [])
    candidates = detection_summary.get("candidates", [])
    truth_hits = [bool(metric.get("within_tolerance")) for metric in metrics]
    unique_assignment = unique_truth_assignment(candidates, metrics)
    unique_hits = unique_assignment["unique_truth_hits"]
    truth_x = [safe_float(metric.get("truth_x_mm")) for metric in metrics]
    truth_z = [safe_float(metric.get("truth_z_mm")) for metric in metrics]
    x_errors = [safe_float(metric.get("x_error_mm")) for metric in metrics]
    z_errors = [safe_float(metric.get("z_error_mm")) for metric in metrics]
    candidate_x = [safe_float(candidate.get("x_mm")) for candidate in candidates]
    candidate_z = [safe_float(candidate.get("z_mm")) for candidate in candidates]
    best = candidates[0] if candidates else {}
    hit_truth_x = [x for x, hit in zip(truth_x, truth_hits) if hit]
    missed_truth_x = [x for x, hit in zip(truth_x, truth_hits) if not hit]
    branch_key = plan_row["branch_key"]
    return {
        "branch_key": branch_key,
        "seed": int(plan_row["seed"]),
        "case_variant": plan_row["case_variant"],
        "case_label": plan_row["case_label"],
        "run_name": plan_row["run_name"],
        "output_dir": plan_row["existing_output_dir"],
        "detected_candidate_count": len(candidates),
        "all_truths_within_tolerance": bool(detection_summary.get("all_truths_within_tolerance")),
        "truth_hit_count": sum(truth_hits),
        "truth_count": len(truth_hits),
        "target0_hit": truth_hits[0] if len(truth_hits) > 0 else False,
        "target1_hit": truth_hits[1] if len(truth_hits) > 1 else False,
        "target2_hit": truth_hits[2] if len(truth_hits) > 2 else False,
        "unique_truth_hit_count": unique_assignment["unique_truth_hit_count"],
        "unique_all_truths_within_tolerance": unique_assignment["unique_truth_hit_count"] == len(metrics),
        "unique_target0_hit": unique_hits[0] if len(unique_hits) > 0 else False,
        "unique_target1_hit": unique_hits[1] if len(unique_hits) > 1 else False,
        "unique_target2_hit": unique_hits[2] if len(unique_hits) > 2 else False,
        "assigned_candidate_ranks": ",".join(str(rank) for rank in unique_assignment["assigned_candidate_ranks"]),
        "matched_truth_x_values_mm": join_mm(hit_truth_x),
        "missed_truth_x_values_mm": join_mm(missed_truth_x),
        "best_candidate_x_mm": safe_float(best.get("x_mm")),
        "best_candidate_z_mm": safe_float(best.get("z_mm")),
        "best_candidate_score": safe_float(best.get("normalized_score")),
        "candidate_x_min_mm": float(np.nanmin(candidate_x)) if candidate_x else math.nan,
        "candidate_x_max_mm": float(np.nanmax(candidate_x)) if candidate_x else math.nan,
        "candidate_x_median_mm": float(np.nanmedian(candidate_x)) if candidate_x else math.nan,
        "candidate_z_median_mm": float(np.nanmedian(candidate_z)) if candidate_z else math.nan,
        "candidate_x_span_mm": (
            float(np.nanmax(candidate_x) - np.nanmin(candidate_x)) if candidate_x else math.nan
        ),
        "max_truth_x_error_mm": float(np.nanmax(x_errors)) if x_errors else math.nan,
        "max_truth_z_error_mm": float(np.nanmax(z_errors)) if z_errors else math.nan,
        "elapsed_time_s": safe_float(detection_summary.get("elapsed_time_s")),
        "outcome": case_outcome(branch_key, truth_hits),
    }


def branch_summary_rows(rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in rows}):
        branch_rows = [row for row in rows if row["branch_key"] == branch]
        count = len(branch_rows)
        all_truth = sum(bool(row["all_truths_within_tolerance"]) for row in branch_rows)
        out.append({
            "branch_key": branch,
            "case_count": count,
            "all_truth_case_count": all_truth,
            "all_truth_case_fraction": all_truth / count if count else 0.0,
            "target0_hit_count": sum(bool(row["target0_hit"]) for row in branch_rows),
            "target1_hit_count": sum(bool(row["target1_hit"]) for row in branch_rows),
            "target2_hit_count": sum(bool(row["target2_hit"]) for row in branch_rows),
            "unique_all_truth_case_count": sum(bool(row["unique_all_truths_within_tolerance"]) for row in branch_rows),
            "unique_target0_hit_count": sum(bool(row["unique_target0_hit"]) for row in branch_rows),
            "unique_target1_hit_count": sum(bool(row["unique_target1_hit"]) for row in branch_rows),
            "unique_target2_hit_count": sum(bool(row["unique_target2_hit"]) for row in branch_rows),
            "mean_truth_hit_count": float(np.mean([row["truth_hit_count"] for row in branch_rows])) if branch_rows else 0.0,
            "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count"] for row in branch_rows])) if branch_rows else 0.0,
            "median_best_candidate_x_mm": float(np.median([row["best_candidate_x_mm"] for row in branch_rows])),
            "median_candidate_x_span_mm": float(np.median([row["candidate_x_span_mm"] for row in branch_rows])),
            "mean_elapsed_time_s": float(np.mean([row["elapsed_time_s"] for row in branch_rows])),
        })
    return out


def summarize(rows: list[dict], branch_rows: list[dict], plan_summary: dict) -> dict:
    case_count = len(rows)
    all_truth = sum(bool(row["all_truths_within_tolerance"]) for row in rows)
    target0_hits = sum(bool(row["target0_hit"]) for row in rows)
    target1_hits = sum(bool(row["target1_hit"]) for row in rows)
    target2_hits = sum(bool(row["target2_hit"]) for row in rows)
    unique_all_truth = sum(bool(row["unique_all_truths_within_tolerance"]) for row in rows)
    return {
        "policy_label": "local_2d_detector_baseline_synthesis_simple_detector_under_resolves",
        "source_command_plan_policy_label": plan_summary.get("policy_label", ""),
        "case_count": case_count,
        "all_truth_case_count": all_truth,
        "all_truth_case_fraction": all_truth / case_count if case_count else 0.0,
        "target0_hit_count": target0_hits,
        "target1_hit_count": target1_hits,
        "target2_hit_count": target2_hits,
        "unique_all_truth_case_count": unique_all_truth,
        "unique_target0_hit_count": sum(bool(row["unique_target0_hit"]) for row in rows),
        "unique_target1_hit_count": sum(bool(row["unique_target1_hit"]) for row in rows),
        "unique_target2_hit_count": sum(bool(row["unique_target2_hit"]) for row in rows),
        "branch_count": len(branch_rows),
        "gpu_used": False,
        "backend": "cpu",
        "max_parallel_processes": 1,
        "mean_elapsed_time_s": float(np.mean([row["elapsed_time_s"] for row in rows])) if rows else 0.0,
        "max_elapsed_time_s": float(np.max([row["elapsed_time_s"] for row in rows])) if rows else 0.0,
        "detector_baseline_status": "completed_but_not_positive_comparator",
        "decision": (
            "The same-case simple hyperbola detector baseline does not recover all three truth positions "
            "in any close14 or close50 case. It is useful as a weak image-feature baseline showing that "
            "the controlled FWI/coordinate objective is doing substantially more than naive detector seeding, "
            "but it should not be framed as a competitive detector that tracks the optimizer's clean versus "
            "x-ambiguous distinction."
        ),
    }


def plot_synthesis(rows: list[dict], branch_rows: list[dict], save_path: Path) -> str:
    branches = [row["branch_key"] for row in branch_rows]
    case_counts = np.asarray([row["case_count"] for row in branch_rows], dtype=float)
    all_truth = np.asarray([row["all_truth_case_count"] for row in branch_rows], dtype=float)

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.0), constrained_layout=True)
    x = np.arange(len(branches))
    axes[0].bar(x, case_counts, color="#d9d9d9", label="cases")
    axes[0].bar(x, all_truth, color="#2f9d55", label="all truth detected")
    axes[0].set_xticks(x, [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[0].set_ylabel("case count")
    axes[0].set_title("Detector all-truth recovery")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    truth_labels = ["target0", "target1", "target2"]
    width = 0.24
    for offset, label in zip([-width, 0.0, width], truth_labels):
        values = [row[f"{label}_hit_count"] for row in branch_rows]
        axes[1].bar(x + offset, values, width=width, label=label)
    axes[1].set_xticks(x, [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[1].set_ylabel("truth hits in top-20 detector candidates")
    axes[1].set_title("Which truth points survived")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle("Local 2D detector baseline synthesis: simple detector under-resolves", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, branch_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_baseline_synthesis.png`",
                "",
                "This figure consolidates the 12 CPU same-case detector-baseline runs.",
                "The detector is a simple hyperbola-energy seed generator, not FWI.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"All-truth cases: `{summary['all_truth_case_count']}`.",
                f"Target0 hits: `{summary['target0_hit_count']}`.",
                f"Target1 hits: `{summary['target1_hit_count']}`.",
                f"Target2 hits: `{summary['target2_hit_count']}`.",
                f"GPU used: `{summary['gpu_used']}`.",
                "",
                "Outputs:",
                "",
                f"- Case rows: `{rows_csv.name}`.",
                f"- Branch rows: `{branch_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
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
    parser.add_argument("--run-name", default="local_2d_detector_baseline_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    plan_dir = summary_root / args.command_plan_run
    plan_summary = read_json(plan_dir / "data/local_2d_detector_baseline_command_plan_summary.json")
    plan_rows = read_csv_rows(plan_dir / "data/local_2d_detector_baseline_command_plan_rows.csv")
    missing = [row["run_name"] for row in plan_rows if not parse_bool(row.get("skip_existing"))]
    if missing:
        raise RuntimeError(f"detector baseline outputs are missing: {missing}")

    rows = [build_case_row(row, read_json(detection_summary_path(row))) for row in plan_rows]
    branch_rows = branch_summary_rows(rows)
    summary = summarize(rows, branch_rows, plan_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_baseline_synthesis_rows.csv"
    branch_csv = data_dir / "local_2d_detector_baseline_branch_summary.csv"
    summary_json = data_dir / "local_2d_detector_baseline_synthesis_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_baseline_synthesis.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    plot_synthesis(rows, branch_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "branch_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, branch_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_baseline_synthesis",
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
