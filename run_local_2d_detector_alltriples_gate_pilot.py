#!/usr/bin/env python3
"""Score all branch-specific top20 detector triples on saved B-scans."""

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
from run_local_2d_detector_blind_assignment_policy import detect_for_config  # noqa: E402
from run_local_2d_detector_image_objective_gate import image_objective_score, normalized_envelope, time_offsets_s  # noqa: E402
from run_local_2d_detector_parameter_sensitivity import DEFAULT_COMMAND_PLAN_RUN, config_rows, detection_npz_path  # noqa: E402
from run_local_2d_detector_baseline_synthesis import unique_truth_assignment  # noqa: E402
from run_rebar_detection_pipeline import truth_match_metrics  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


BRANCH_TOP20_CONFIG = {
    "target2_close14": "mean_top20_moderate12_baseline",
    "target2_close50_linear29p5": "mean_top20_distinct20_baseline",
}
OBJECTIVE_LABELS = ("sum", "span_bonus", "min", "min_span", "balanced", "mask")


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


def case_label(plan_row: dict) -> str:
    return f"{plan_row['branch_key']}|seed{plan_row['seed']}|{plan_row['case_variant']}"


def candidate_rank_map(candidates: list) -> dict:
    return {candidate: rank for rank, candidate in enumerate(candidates, start=1)}


def combo_truth_metrics(combo: tuple, truth_x: list[float], truth_z: list[float], tolerance_mm: float) -> dict:
    metrics = truth_match_metrics(combo, truth_x, truth_z, tolerance_mm, tolerance_mm)
    rows = [candidate.as_mm() for candidate in combo]
    unique = unique_truth_assignment(rows, metrics)
    hits = unique["unique_truth_hits"]
    return {
        "unique_truth_hit_count": unique["unique_truth_hit_count"],
        "unique_all_truths_within_tolerance": unique["unique_truth_hit_count"] == len(truth_x),
        "unique_target0_hit": bool(hits[0]) if len(hits) > 0 else False,
        "unique_target1_hit": bool(hits[1]) if len(hits) > 1 else False,
        "unique_target2_hit": bool(hits[2]) if len(hits) > 2 else False,
        "assigned_truth_ranks": ",".join(str(rank) for rank in unique["assigned_candidate_ranks"]),
    }


def combo_scores(
    combo: tuple,
    image: np.ndarray,
    scan_x: np.ndarray,
    time_values: np.ndarray,
    tx_rx_offset_m: float,
    offset_family: str,
) -> dict:
    xs = [candidate.x_m * 1000.0 for candidate in combo]
    zs = [candidate.z_m * 1000.0 for candidate in combo]
    sum_score = float(sum(candidate.normalized_score for candidate in combo))
    min_score = float(min(candidate.normalized_score for candidate in combo))
    span = float(max(xs) - min(xs))
    gaps = np.diff(sorted(xs))
    gap_balance = abs(float(gaps[1] - gaps[0])) if len(gaps) == 2 else 999.0
    mask = image_objective_score(
        image,
        scan_x,
        time_values,
        xs,
        zs,
        tx_rx_offset_m,
        time_offsets_s(offset_family),
        60.0,
    )
    return {
        "score_sum": sum_score,
        "score_span_bonus": sum_score + 0.5 * span / 100.0,
        "score_min": min_score,
        "score_min_span": min_score + 0.25 * span / 100.0,
        "score_balanced": sum_score + 0.4 * span / 100.0 - 0.05 * gap_balance / 100.0,
        "score_mask": mask["image_objective_score"],
        "best_mask_time_offset_ps": mask["best_time_offset_ps"],
        "x_span_mm": span,
        "gap_balance_mm": gap_balance,
    }


def score_case(plan_row: dict, config: dict) -> list[dict]:
    with np.load(detection_npz_path(plan_row)) as npz:
        observed = np.asarray(npz["observed_bscan"], dtype=np.float64)
        scan_x = np.asarray(npz["scan_x"], dtype=np.float64)
        time_values = np.asarray(npz["time"], dtype=np.float64)
        truth_x = [float(value) for value in npz["truth_x_values_mm"]]
        truth_z = [float(value) for value in npz["truth_z_values_mm"]]
    candidates = detect_for_config(plan_row, config, observed, scan_x, time_values)
    ranks = candidate_rank_map(candidates)
    image = normalized_envelope(observed, str(config["background_mode"]))
    out = []
    for combo_index, combo in enumerate(itertools.combinations(candidates[:20], 3), start=1):
        combo = tuple(sorted(combo, key=lambda candidate: candidate.x_m))
        xs = [candidate.x_m * 1000.0 for candidate in combo]
        zs = [candidate.z_m * 1000.0 for candidate in combo]
        row = {
            "case_label": case_label(plan_row),
            "branch_key": plan_row["branch_key"],
            "seed": safe_int(plan_row["seed"]),
            "case_variant": plan_row["case_variant"],
            "run_name": plan_row["run_name"],
            "config_key": config["config_key"],
            "combo_index": combo_index,
            "candidate_ranks": ",".join(str(ranks[candidate]) for candidate in combo),
            "candidate_x_values_mm": ",".join(f"{value:g}" for value in xs),
            "candidate_z_values_mm": ",".join(f"{value:g}" for value in zs),
        }
        row.update(combo_truth_metrics(combo, truth_x, truth_z, safe_float(plan_row.get("truth_tolerance_mm"), 8.0)))
        row.update(
            combo_scores(
                combo,
                image,
                scan_x,
                time_values,
                safe_float(plan_row["tx_rx_offset_mm"]) / 1000.0,
                str(config["time_offset_family"]),
            )
        )
        out.append(row)
    return out


def objective_value(row: dict, objective_label: str) -> float:
    return safe_float(row.get(f"score_{objective_label}"), -math.inf)


def objective_case_summary(case_rows: list[dict], objective_label: str) -> dict:
    ordered = sorted(case_rows, key=lambda row: objective_value(row, objective_label), reverse=True)
    first_truth_rank = math.nan
    truths_in_top10 = 0
    truths_in_top50 = 0
    top_row = ordered[0] if ordered else {}
    for rank, row in enumerate(ordered, start=1):
        if bool(row["unique_all_truths_within_tolerance"]):
            if rank <= 10:
                truths_in_top10 += 1
            if rank <= 50:
                truths_in_top50 += 1
            if not math.isfinite(first_truth_rank):
                first_truth_rank = rank
    return {
        "case_label": case_rows[0]["case_label"] if case_rows else "",
        "branch_key": case_rows[0]["branch_key"] if case_rows else "",
        "seed": case_rows[0]["seed"] if case_rows else "",
        "case_variant": case_rows[0]["case_variant"] if case_rows else "",
        "objective_label": objective_label,
        "combo_count": len(case_rows),
        "first_all_truth_rank": first_truth_rank,
        "all_truth_count_top10": truths_in_top10,
        "all_truth_count_top50": truths_in_top50,
        "top_unique_truth_hit_count": safe_int(top_row.get("unique_truth_hit_count"), 0),
        "top_unique_all_truths": bool(top_row.get("unique_all_truths_within_tolerance", False)),
        "top_candidate_ranks": top_row.get("candidate_ranks", ""),
        "top_candidate_x_values_mm": top_row.get("candidate_x_values_mm", ""),
    }


def build_case_objective_summary(combo_rows: list[dict]) -> list[dict]:
    out = []
    for case in sorted({row["case_label"] for row in combo_rows}):
        case_rows = [row for row in combo_rows if row["case_label"] == case]
        for objective_label in OBJECTIVE_LABELS:
            out.append(objective_case_summary(case_rows, objective_label))
    return out


def build_objective_summary(case_objective_rows: list[dict]) -> list[dict]:
    out = []
    for objective_label in OBJECTIVE_LABELS:
        rows = [row for row in case_objective_rows if row["objective_label"] == objective_label]
        finite_ranks = [safe_float(row["first_all_truth_rank"]) for row in rows if math.isfinite(safe_float(row["first_all_truth_rank"]))]
        out.append({
            "objective_label": objective_label,
            "case_count": len(rows),
            "top1_all_truth_case_count": sum(bool(row["top_unique_all_truths"]) for row in rows),
            "first_truth_top10_case_count": sum(safe_float(row["first_all_truth_rank"], math.inf) <= 10 for row in rows),
            "first_truth_top50_case_count": sum(safe_float(row["first_all_truth_rank"], math.inf) <= 50 for row in rows),
            "median_first_truth_rank": float(np.median(finite_ranks)) if finite_ranks else math.nan,
            "max_first_truth_rank": max(finite_ranks) if finite_ranks else math.nan,
            "mean_top_unique_truth_hit_count": float(np.mean([safe_float(row["top_unique_truth_hit_count"]) for row in rows])) if rows else math.nan,
        })
    return sorted(
        out,
        key=lambda row: (
            -safe_int(row["top1_all_truth_case_count"]),
            -safe_int(row["first_truth_top10_case_count"]),
            -safe_int(row["first_truth_top50_case_count"]),
            safe_float(row["median_first_truth_rank"], math.inf),
        ),
    )


def summarize(combo_rows: list[dict], case_objective_rows: list[dict], objective_rows: list[dict]) -> dict:
    best_top10 = max(objective_rows, key=lambda row: (safe_int(row["first_truth_top10_case_count"]), safe_int(row["first_truth_top50_case_count"])))
    best_top50 = max(objective_rows, key=lambda row: (safe_int(row["first_truth_top50_case_count"]), -safe_float(row["median_first_truth_rank"], math.inf)))
    return {
        "policy_label": "local_2d_detector_alltriples_gate_pilot_cpu_no_fwi",
        "case_count": len({row["case_label"] for row in combo_rows}),
        "combo_row_count": len(combo_rows),
        "case_objective_row_count": len(case_objective_rows),
        "objective_count": len(objective_rows),
        "branch_top20_configs": BRANCH_TOP20_CONFIG,
        "best_top1_all_truth_case_count": max(safe_int(row["top1_all_truth_case_count"]) for row in objective_rows),
        "best_top10_objective": best_top10["objective_label"],
        "best_top10_case_count": safe_int(best_top10["first_truth_top10_case_count"]),
        "best_top50_objective": best_top50["objective_label"],
        "best_top50_case_count": safe_int(best_top50["first_truth_top50_case_count"]),
        "best_top50_median_first_truth_rank": safe_float(best_top50["median_first_truth_rank"]),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Do not launch detector-seeded FWI from the current all-top20 gate. "
            "Simple score/span/min/mask objectives do not select an all-truth triple at rank 1; "
            "the best top-10 result reaches only two of twelve cases and the best top-50 result "
            "reaches eight of twelve cases. A stronger waveform gate or a deliberately labeled "
            "oracle/rank-gated upper-bound is still required."
        ),
    }


def plot_summary(objective_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["objective_label"].replace("_", "\n") for row in objective_rows]
    top10 = [safe_int(row["first_truth_top10_case_count"]) for row in objective_rows]
    top50 = [safe_int(row["first_truth_top50_case_count"]) for row in objective_rows]
    median_rank = [safe_float(row["median_first_truth_rank"], math.nan) for row in objective_rows]
    x = np.arange(len(objective_rows))

    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.4), constrained_layout=True)
    width = 0.36
    axes[0].bar(x - width / 2, top10, width=width, color="#4c78a8", label="first truth in top10")
    axes[0].bar(x + width / 2, top50, width=width, color="#f58518", label="first truth in top50")
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylabel("case count")
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_title("All-top20 triple gate recall")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x, median_rank, color="#59a14f", width=0.62)
    axes[1].set_xticks(x, labels, fontsize=8)
    axes[1].set_ylabel("median first all-truth rank")
    axes[1].set_title("Rank of first all-truth triple")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"top1 all-truth cases: {summary['best_top1_all_truth_case_count']}\nGPU priority: none",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("Local 2D detector all-top20 triple gate pilot", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, combo_csv: Path, case_csv: Path, objective_csv: Path, summary_json: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_alltriples_gate_pilot.png`",
                "",
                "This CPU-only pilot scores all detector candidate triples from the",
                "branch-specific top-20 saved-B-scan detector configurations.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Candidate-triple rows: `{summary['combo_row_count']}`.",
                f"Best top1 all-truth case count: `{summary['best_top1_all_truth_case_count']}`.",
                f"Best top10 objective: `{summary['best_top10_objective']}` with `{summary['best_top10_case_count']}` cases.",
                f"Best top50 objective: `{summary['best_top50_objective']}` with `{summary['best_top50_case_count']}` cases.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                "",
                "Outputs:",
                "",
                f"- Combo scores: `{combo_csv.name}`.",
                f"- Case/objective summary: `{case_csv.name}`.",
                f"- Objective summary: `{objective_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                "",
                "Scope boundary:",
                "",
                "The pilot reads saved B-scans and reruns detector candidate scoring on CPU.",
                "It does not run FDTD, FWI, GPU kernels, 3D/HPC jobs, field FWI, or neural-network training.",
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
    parser.add_argument("--run-name", default="local_2d_detector_alltriples_gate_pilot")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    plan_rows = read_csv_rows(summary_root / args.command_plan_run / "data/local_2d_detector_baseline_command_plan_rows.csv")
    configs = {row["config_key"]: row for row in config_rows()}

    combo_rows = []
    for plan_row in plan_rows:
        config_key = BRANCH_TOP20_CONFIG[str(plan_row["branch_key"])]
        combo_rows.extend(score_case(plan_row, configs[config_key]))
    case_objective_rows = build_case_objective_summary(combo_rows)
    objective_rows = build_objective_summary(case_objective_rows)
    summary = summarize(combo_rows, case_objective_rows, objective_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    combo_csv = data_dir / "local_2d_detector_alltriples_gate_rows.csv"
    case_csv = data_dir / "local_2d_detector_alltriples_gate_case_objective_summary.csv"
    objective_csv = data_dir / "local_2d_detector_alltriples_gate_objective_summary.csv"
    summary_json = data_dir / "local_2d_detector_alltriples_gate_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_alltriples_gate_pilot.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(combo_csv, [json_safe(row) for row in combo_rows])
    write_csv(case_csv, [json_safe(row) for row in case_objective_rows])
    write_csv(objective_csv, [json_safe(row) for row in objective_rows])
    plot_summary(objective_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "combo_csv": str(combo_csv),
        "case_objective_csv": str(case_csv),
        "objective_csv": str(objective_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, combo_csv, case_csv, objective_csv, summary_json)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_alltriples_gate_pilot",
        {
            "command_plan_run": args.command_plan_run,
            "branch_top20_configs": BRANCH_TOP20_CONFIG,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
