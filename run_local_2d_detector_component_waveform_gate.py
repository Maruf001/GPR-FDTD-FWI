#!/usr/bin/env python3
"""Test component-wise waveform gates for detector candidate triples on saved B-scans."""

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
from run_local_2d_detector_image_objective_gate import (  # noqa: E402
    image_objective_score,
    normalized_envelope,
    time_offsets_s,
)
from run_local_2d_detector_parameter_sensitivity import (  # noqa: E402
    DEFAULT_COMMAND_PLAN_RUN,
    config_rows,
    detection_npz_path,
)
from run_local_2d_detector_rank_budget_diagnostic import (  # noqa: E402
    BUDGETS,
    TARGET_FIELDS,
    boolish,
    build_budget_rows,
    group_by_case,
    read_csv_rows,
    read_json,
    safe_float,
    safe_int,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ALLTRIPLES_RUN = "030_local_2d_detector_alltriples_gate_pilot"
COMPONENT_OBJECTIVES = (
    "component_sum",
    "component_min",
    "component_mean_min",
    "component_floor_span",
    "component_balanced",
    "component_left_floor",
    "hybrid_span_component",
)


def parse_float_list(text: str) -> list[float]:
    return [float(value) for value in str(text).split(",") if value.strip()]


def component_variant_scores(row: dict, component_scores: list[float]) -> dict:
    scores = component_scores or [0.0]
    total = float(sum(scores))
    floor = float(min(scores))
    mean = total / len(scores)
    x_span = safe_float(row.get("x_span_mm"), 0.0)
    gap_balance = safe_float(row.get("gap_balance_mm"), 0.0)
    left_score = float(scores[0])
    return {
        "component_score_values": ",".join(f"{value:.6g}" for value in scores),
        "score_component_sum": total,
        "score_component_min": floor,
        "score_component_mean_min": mean + floor,
        "score_component_floor_span": floor + 0.25 * x_span / 100.0,
        "score_component_balanced": total + floor + 0.4 * x_span / 100.0 - 0.05 * gap_balance / 100.0,
        "score_component_left_floor": left_score + floor + 0.3 * x_span / 100.0,
        "score_hybrid_span_component": safe_float(row.get("score_span_bonus"), 0.0) + floor,
    }


def load_case_image(
    run_name: str,
    background_mode: str,
    plan_by_run: dict[str, dict],
    image_cache: dict[tuple[str, str], tuple[np.ndarray, np.ndarray, np.ndarray, float]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    key = (run_name, background_mode)
    if key not in image_cache:
        plan_row = plan_by_run[run_name]
        with np.load(detection_npz_path(plan_row)) as npz:
            observed = np.asarray(npz["observed_bscan"], dtype=np.float64)
            image_cache[key] = (
                normalized_envelope(observed, background_mode),
                np.asarray(npz["scan_x"], dtype=np.float64),
                np.asarray(npz["time"], dtype=np.float64),
                safe_float(plan_row["tx_rx_offset_mm"]) / 1000.0,
            )
    return image_cache[key]


def component_scores_for_row(
    row: dict,
    plan_by_run: dict[str, dict],
    configs: dict[str, dict],
    image_cache: dict[tuple[str, str], tuple[np.ndarray, np.ndarray, np.ndarray, float]],
    score_cache: dict[tuple, float],
) -> list[float]:
    config = configs[row["config_key"]]
    background_mode = str(config["background_mode"])
    image, scan_x, time_values, tx_rx_offset_m = load_case_image(
        row["run_name"],
        background_mode,
        plan_by_run,
        image_cache,
    )
    scores = []
    for x_mm, z_mm in zip(
        parse_float_list(row.get("candidate_x_values_mm", "")),
        parse_float_list(row.get("candidate_z_values_mm", "")),
    ):
        key = (
            row["run_name"],
            background_mode,
            str(config["time_offset_family"]),
            round(x_mm, 6),
            round(z_mm, 6),
        )
        if key not in score_cache:
            score = image_objective_score(
                image,
                scan_x,
                time_values,
                [x_mm],
                [z_mm],
                tx_rx_offset_m,
                time_offsets_s(str(config["time_offset_family"])),
                60.0,
            )
            score_cache[key] = safe_float(score.get("image_objective_score"), 0.0)
        scores.append(score_cache[key])
    return scores


def score_component_rows(
    combo_rows: list[dict],
    plan_rows: list[dict],
    configs: dict[str, dict],
) -> tuple[list[dict], int]:
    plan_by_run = {row["run_name"]: row for row in plan_rows}
    image_cache: dict[tuple[str, str], tuple[np.ndarray, np.ndarray, np.ndarray, float]] = {}
    score_cache: dict[tuple, float] = {}
    out = []
    for row in combo_rows:
        scored = dict(row)
        scored.update(
            component_variant_scores(
                row,
                component_scores_for_row(row, plan_by_run, configs, image_cache, score_cache),
            )
        )
        out.append(scored)
    return out, len(score_cache)


def objective_value(row: dict, objective: str) -> float:
    return safe_float(row.get(f"score_{objective}"), -math.inf)


def ranked_rows(case_rows: list[dict], objective: str) -> list[dict]:
    return sorted(case_rows, key=lambda row: objective_value(row, objective), reverse=True)


def first_truth_rank(case_rows: list[dict], objective: str) -> float:
    for rank, row in enumerate(ranked_rows(case_rows, objective), start=1):
        if boolish(row.get("unique_all_truths_within_tolerance")):
            return float(rank)
    return math.inf


def build_case_objective_rows(
    scored_rows: list[dict],
    objectives: tuple[str, ...] = COMPONENT_OBJECTIVES,
) -> list[dict]:
    out = []
    for case_label, case_rows in sorted(group_by_case(scored_rows).items()):
        first = case_rows[0]
        for objective in objectives:
            ordered = ranked_rows(case_rows, objective)
            top = ordered[0] if ordered else {}
            out.append(
                {
                    "case_label": case_label,
                    "branch_key": first.get("branch_key", ""),
                    "seed": safe_int(first.get("seed")),
                    "case_variant": first.get("case_variant", ""),
                    "objective": objective,
                    "combo_count": len(case_rows),
                    "first_all_truth_rank": first_truth_rank(case_rows, objective),
                    "top_unique_all_truths": boolish(top.get("unique_all_truths_within_tolerance")),
                    "top_unique_truth_hit_count": safe_int(top.get("unique_truth_hit_count")),
                    "top_target0_hit": boolish(top.get("unique_target0_hit")),
                    "top_target1_hit": boolish(top.get("unique_target1_hit")),
                    "top_target2_hit": boolish(top.get("unique_target2_hit")),
                    "top_candidate_ranks": top.get("candidate_ranks", ""),
                    "top_candidate_x_values_mm": top.get("candidate_x_values_mm", ""),
                }
            )
    return out


def build_objective_rows(case_objective_rows: list[dict]) -> list[dict]:
    out = []
    for objective in COMPONENT_OBJECTIVES:
        rows = [row for row in case_objective_rows if row["objective"] == objective]
        ranks = [safe_float(row["first_all_truth_rank"]) for row in rows]
        finite = [rank for rank in ranks if math.isfinite(rank)]
        objective_row = {
            "objective": objective,
            "case_count": len(rows),
            "top1_all_truth_case_count": sum(boolish(row["top_unique_all_truths"]) for row in rows),
            "top1_target0_hit_count": sum(boolish(row["top_target0_hit"]) for row in rows),
            "top1_target1_hit_count": sum(boolish(row["top_target1_hit"]) for row in rows),
            "top1_target2_hit_count": sum(boolish(row["top_target2_hit"]) for row in rows),
            "median_first_all_truth_rank": float(np.median(finite)) if finite else math.nan,
            "max_first_all_truth_rank": max(finite) if finite else math.nan,
        }
        for budget in BUDGETS:
            objective_row[f"first_truth_top{budget}_case_count"] = sum(rank <= budget for rank in ranks)
        out.append(objective_row)
    return sorted(
        out,
        key=lambda row: (
            -safe_int(row["top1_all_truth_case_count"]),
            -safe_int(row["first_truth_top10_case_count"]),
            -safe_int(row["first_truth_top50_case_count"]),
            safe_float(row["median_first_all_truth_rank"], math.inf),
        ),
    )


def best_count_at_budget(objective_rows: list[dict], budget: int) -> tuple[str, int]:
    key = f"first_truth_top{budget}_case_count"
    best = max(objective_rows, key=lambda row: safe_int(row.get(key)))
    return str(best["objective"]), safe_int(best.get(key))


def summarize(
    scored_rows: list[dict],
    case_objective_rows: list[dict],
    objective_rows: list[dict],
    budget_rows: list[dict],
    *,
    component_candidate_count: int,
    source_summary: dict,
) -> dict:
    case_count = len({row["case_label"] for row in scored_rows})
    best_top10_objective, best_top10_count = best_count_at_budget(objective_rows, 10)
    best_top50_objective, best_top50_count = best_count_at_budget(objective_rows, 50)
    best_top100_objective, best_top100_count = best_count_at_budget(objective_rows, 100)
    best_top200_objective, best_top200_count = best_count_at_budget(objective_rows, 200)
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
    source_best_top10 = safe_int(source_summary.get("best_top10_case_count"))
    source_best_top50 = safe_int(source_summary.get("best_top50_case_count"))
    return {
        "policy_label": "local_2d_detector_component_waveform_gate_cpu_no_fwi",
        "source_policy_label": source_summary.get("policy_label", ""),
        "case_count": case_count,
        "combo_row_count": len(scored_rows),
        "case_objective_row_count": len(case_objective_rows),
        "objective_count": len(objective_rows),
        "component_candidate_count": component_candidate_count,
        "best_top1_all_truth_case_count": max(safe_int(row["top1_all_truth_case_count"]) for row in objective_rows),
        "best_top10_objective": best_top10_objective,
        "best_top10_case_count": best_top10_count,
        "best_top50_objective": best_top50_objective,
        "best_top50_case_count": best_top50_count,
        "best_top100_objective": best_top100_objective,
        "best_top100_case_count": best_top100_count,
        "best_top200_objective": best_top200_objective,
        "best_top200_case_count": best_top200_count,
        "source_best_top10_case_count": source_best_top10,
        "source_best_top50_case_count": source_best_top50,
        "top10_improvement_over_source": best_top10_count - source_best_top10,
        "top50_improvement_over_source": best_top50_count - source_best_top50,
        "minimal_all_case_candidate_triple_budget": minimal_all_case_budget,
        "minimal_all_case_objectives": minimal_all_case_objectives,
        "max_top1_target0_hit_count": max(safe_int(row["top1_target0_hit_count"]) for row in objective_rows),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "The component-wise waveform gate improves rank-budget recall over the prior simple "
            "all-triples gate, but it still selects zero all-truth triples at rank 1 and needs up "
            "to 200 ranked triples per case for full coverage. Continue CPU-side waveform-gate "
            "development or treat this as an upper-bound analysis; do not launch detector-seeded FWI."
        ),
    }


def plot_component_gate(objective_rows: list[dict], budget_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.4), constrained_layout=True)
    for objective in [row["objective"] for row in objective_rows]:
        rows = [row for row in budget_rows if row["objective"] == objective]
        axes[0].plot(
            [safe_int(row["candidate_triple_budget"]) for row in rows],
            [safe_int(row["first_all_truth_case_count"]) for row in rows],
            marker="o",
            linewidth=1.25,
            label=objective.replace("component_", "c_"),
        )
    axes[0].set_xscale("log")
    axes[0].set_xticks([1, 3, 5, 10, 20, 50, 100, 200, 500, 1140])
    axes[0].get_xaxis().set_major_formatter(plt.ScalarFormatter())
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_xlabel("candidate triples per case")
    axes[0].set_ylabel("cases with first all-truth triple within budget")
    axes[0].set_title("Component waveform-gate rank curve")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=7, ncol=2)

    labels = [row["objective"].replace("component_", "c_").replace("_", "\n") for row in objective_rows]
    x = np.arange(len(objective_rows))
    width = 0.25
    axes[1].bar(x - width, [safe_int(row["top1_target0_hit_count"]) for row in objective_rows], width=width, label="target0")
    axes[1].bar(x, [safe_int(row["top1_target1_hit_count"]) for row in objective_rows], width=width, label="target1")
    axes[1].bar(x + width, [safe_int(row["top1_target2_hit_count"]) for row in objective_rows], width=width, label="target2")
    axes[1].set_xticks(x, labels, fontsize=7)
    axes[1].set_ylim(0, summary["case_count"] + 1)
    axes[1].set_ylabel("top-ranked case count")
    axes[1].set_title("Top-ranked component-gate target hits")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.02,
        0.96,
        f"top10 gain: {summary['top10_improvement_over_source']}\n"
        f"top50 gain: {summary['top50_improvement_over_source']}\n"
        f"top1 all-truth: {summary['best_top1_all_truth_case_count']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector component waveform-gate pilot", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(
    path: Path,
    summary: dict,
    scored_csv: Path,
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
                "## `local_2d_detector_component_waveform_gate.png`",
                "",
                "This CPU-only pilot scores detector candidate triples with component-wise",
                "hyperbola waveform-mask support on saved B-scans.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Candidate-triple rows: `{summary['combo_row_count']}`.",
                f"Component candidates scored: `{summary['component_candidate_count']}`.",
                f"Best top-10 objective: `{summary['best_top10_objective']}` with `{summary['best_top10_case_count']}` cases.",
                f"Best top-50 objective: `{summary['best_top50_objective']}` with `{summary['best_top50_case_count']}` cases.",
                f"Best top-1 all-truth cases: `{summary['best_top1_all_truth_case_count']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Scored triples: `{scored_csv.name}`.",
                f"- Case/objective rows: `{case_csv.name}`.",
                f"- Objective summary: `{objective_csv.name}`.",
                f"- Budget curve: `{budget_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                "",
                "Scope boundary:",
                "",
                "This pilot reads saved B-scans and runs CPU image scoring only. It does not",
                "run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--alltriples-run", default=DEFAULT_ALLTRIPLES_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_component_waveform_gate")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    source_root = summary_root / args.alltriples_run
    combo_csv = source_root / "data/local_2d_detector_alltriples_gate_rows.csv"
    source_summary_json = source_root / "data/local_2d_detector_alltriples_gate_summary.json"
    plan_csv = summary_root / args.command_plan_run / "data/local_2d_detector_baseline_command_plan_rows.csv"
    combo_rows = read_csv_rows(combo_csv)
    source_summary = read_json(source_summary_json)
    plan_rows = read_csv_rows(plan_csv)
    configs = {row["config_key"]: row for row in config_rows()}

    scored_rows, component_candidate_count = score_component_rows(combo_rows, plan_rows, configs)
    case_objective_rows = build_case_objective_rows(scored_rows)
    objective_rows = build_objective_rows(case_objective_rows)
    budget_rows = build_budget_rows(objective_rows)
    summary = summarize(
        scored_rows,
        case_objective_rows,
        objective_rows,
        budget_rows,
        component_candidate_count=component_candidate_count,
        source_summary=source_summary,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    scored_csv = data_dir / "local_2d_detector_component_waveform_gate_rows.csv"
    case_csv = data_dir / "local_2d_detector_component_waveform_gate_case_objective_summary.csv"
    objective_csv = data_dir / "local_2d_detector_component_waveform_gate_objective_summary.csv"
    budget_csv = data_dir / "local_2d_detector_component_waveform_gate_budget_curve.csv"
    summary_json = data_dir / "local_2d_detector_component_waveform_gate_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_component_waveform_gate.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(scored_csv, [json_safe(row) for row in scored_rows])
    write_csv(case_csv, [json_safe(row) for row in case_objective_rows])
    write_csv(objective_csv, [json_safe(row) for row in objective_rows])
    write_csv(budget_csv, [json_safe(row) for row in budget_rows])
    plot_component_gate(objective_rows, budget_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_combo_csv": str(combo_csv),
        "source_summary_json": str(source_summary_json),
        "command_plan_csv": str(plan_csv),
        "scored_rows_csv": str(scored_csv),
        "case_objective_csv": str(case_csv),
        "objective_summary_csv": str(objective_csv),
        "budget_curve_csv": str(budget_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, scored_csv, case_csv, objective_csv, budget_csv, summary_json)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_component_waveform_gate",
        {
            "alltriples_run": args.alltriples_run,
            "command_plan_run": args.command_plan_run,
            "source_combo_csv": str(combo_csv),
            "source_summary_json": str(source_summary_json),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
