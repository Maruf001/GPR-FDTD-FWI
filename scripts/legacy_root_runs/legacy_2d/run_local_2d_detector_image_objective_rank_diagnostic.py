#!/usr/bin/env python3
"""Rank-budget diagnostic for saved-B-scan detector image-objective rows."""

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
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_IMAGE_OBJECTIVE_RUN = "027_local_2d_detector_image_objective_gate_saved_bscan"
CASE_FIELDS = ("branch_key", "seed", "case_variant", "run_name")
BUDGETS = (1, 10, 50, 200, 1000, 2000)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def case_key(row: dict) -> tuple[str, str, str, str]:
    return tuple(str(row[field]) for field in CASE_FIELDS)


def case_label(row: dict) -> str:
    return f"{row['branch_key']}|seed{row['seed']}|{row['case_variant']}"


def image_score(row: dict) -> float:
    return safe_float(row.get("image_objective_score"), -math.inf)


def build_case_rank_rows(rows: list[dict]) -> list[dict]:
    out = []
    objectives = sorted({row["objective_label"] for row in rows})
    for objective in objectives:
        objective_rows = [row for row in rows if row["objective_label"] == objective]
        for key in sorted({case_key(row) for row in objective_rows}):
            case_rows = [row for row in objective_rows if case_key(row) == key]
            ordered = sorted(
                case_rows,
                key=lambda row: (
                    image_score(row),
                    -safe_float(row.get("assigned_max_rank"), 100_000.0),
                    -safe_float(row.get("assigned_rank_sum"), 100_000.0),
                ),
                reverse=True,
            )
            top = ordered[0] if ordered else {}
            first_truth_rank = math.inf
            first_truth_score = math.nan
            for rank, row in enumerate(ordered, start=1):
                if boolish(row.get("unique_all_truths_within_tolerance")):
                    first_truth_rank = float(rank)
                    first_truth_score = image_score(row)
                    break
            out.append(
                {
                    "objective_label": objective,
                    "case_label": case_label(top) if top else "|".join(key[:3]),
                    "branch_key": key[0],
                    "seed": safe_int(key[1]),
                    "case_variant": key[2],
                    "run_name": key[3],
                    "scored_row_count": len(ordered),
                    "first_all_truth_rank": first_truth_rank,
                    "first_all_truth_score": first_truth_score,
                    "top_unique_all_truths": boolish(top.get("unique_all_truths_within_tolerance")),
                    "top_unique_truth_hit_count": safe_int(top.get("unique_truth_hit_count")),
                    "top_candidate_x_values_mm": top.get("assigned_x_values_mm", ""),
                    "top_candidate_ranks": top.get("assigned_detection_ranks", ""),
                    **{f"first_truth_top{budget}": first_truth_rank <= budget for budget in BUDGETS},
                }
            )
    return out


def build_objective_rows(case_rows: list[dict]) -> list[dict]:
    out = []
    for objective in sorted({row["objective_label"] for row in case_rows}):
        rows = [row for row in case_rows if row["objective_label"] == objective]
        ranks = [safe_float(row["first_all_truth_rank"]) for row in rows]
        finite = [rank for rank in ranks if math.isfinite(rank)]
        objective_row = {
            "objective_label": objective,
            "case_count": len(rows),
            "top1_all_truth_case_count": sum(boolish(row["top_unique_all_truths"]) for row in rows),
            "median_first_all_truth_rank": float(np.median(finite)) if finite else math.nan,
            "max_first_all_truth_rank": float(max(finite)) if finite else math.nan,
        }
        for budget in BUDGETS:
            objective_row[f"first_truth_top{budget}_case_count"] = sum(rank <= budget for rank in ranks)
        out.append(objective_row)
    return sorted(
        out,
        key=lambda row: (
            -safe_int(row["first_truth_top1000_case_count"]),
            -safe_int(row["first_truth_top200_case_count"]),
            safe_float(row["median_first_all_truth_rank"], math.inf),
            str(row["objective_label"]),
        ),
    )


def summarize_rank_diagnostic(case_rows: list[dict], objective_rows: list[dict], source_summary: dict) -> dict:
    best = objective_rows[0]
    ready = False
    return {
        "policy_label": "local_2d_detector_image_objective_rank_diagnostic_cpu_no_fwi",
        "source_image_objective_policy_label": source_summary.get("policy_label", ""),
        "objective_variant_count": len(objective_rows),
        "case_count": safe_int(best["case_count"]),
        "scored_row_count": safe_int(source_summary.get("scored_row_count"), 0),
        "best_objective_label": best["objective_label"],
        "best_top1_all_truth_case_count": safe_int(best["top1_all_truth_case_count"]),
        "best_top10_all_truth_case_count": safe_int(best["first_truth_top10_case_count"]),
        "best_top50_all_truth_case_count": safe_int(best["first_truth_top50_case_count"]),
        "best_top200_all_truth_case_count": safe_int(best["first_truth_top200_case_count"]),
        "best_top1000_all_truth_case_count": safe_int(best["first_truth_top1000_case_count"]),
        "best_median_first_all_truth_rank": safe_float(best["median_first_all_truth_rank"]),
        "best_max_first_all_truth_rank": safe_float(best["max_first_all_truth_rank"]),
        "previous_primary_top1_all_truth_case_count": safe_int(
            source_summary.get("primary_objective_all_truth_case_count"), 0
        ),
        "previous_oracle_all_truth_case_count": safe_int(source_summary.get("oracle_all_truth_case_count"), 0),
        "ready_for_detector_seeded_fwi": ready,
        "gpu_priority": "none",
        "decision": (
            "Use this CPU-only rank diagnostic to close the saved-B-scan image-objective gate as a "
            "detector handoff route. The scored image objective does not place all-truth rows in a "
            "practical shallow rank budget, so detector-seeded FWI still requires a stronger downstream "
            "objective or an explicitly rank-gated upper-bound framing."
        ),
    }


def plot_rank_diagnostic(summary: dict, objective_rows: list[dict], save_path: Path) -> str:
    objectives = [row["objective_label"].replace("_", "\n") for row in objective_rows]
    x = np.arange(len(objective_rows))
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    width = 0.18
    for offset, budget, color in [
        (-1.5 * width, 50, "#4e79a7"),
        (-0.5 * width, 200, "#59a14f"),
        (0.5 * width, 1000, "#f28e2b"),
        (1.5 * width, 2000, "#9c755f"),
    ]:
        axes[0].bar(
            x + offset,
            [safe_int(row[f"first_truth_top{budget}_case_count"]) for row in objective_rows],
            width=width,
            label=f"top{budget}",
            color=color,
        )
    axes[0].set_xticks(x, objectives, fontsize=8)
    axes[0].set_ylabel("cases with first all-truth inside budget")
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_title("Image-objective rank coverage")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(
        x,
        [safe_float(row["median_first_all_truth_rank"], 0.0) for row in objective_rows],
        color="#e15759",
    )
    axes[1].set_xticks(x, objectives, fontsize=8)
    axes[1].set_ylabel("median first all-truth rank")
    axes[1].set_title("Rank depth remains large")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.98,
        0.95,
        f"best={summary['best_objective_label']}\n"
        f"top50={summary['best_top50_all_truth_case_count']}/{summary['case_count']}\n"
        f"top1000={summary['best_top1000_all_truth_case_count']}/{summary['case_count']}\n"
        f"FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="right",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector image-objective rank diagnostic", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, case_csv: Path, objective_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_image_objective_rank_diagnostic.png`",
                "",
                "This CPU-only diagnostic reads saved image-objective rows from run 027",
                "and asks how deep the first all-truth row appears under each objective.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Best objective: `{summary['best_objective_label']}`.",
                f"Best top-50 all-truth cases: `{summary['best_top50_all_truth_case_count']}`.",
                f"Best top-1000 all-truth cases: `{summary['best_top1000_all_truth_case_count']}`.",
                f"Best median first all-truth rank: `{summary['best_median_first_all_truth_rank']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case ranks: `{case_csv.name}`.",
                f"- Objective summary: `{objective_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved image-objective rows only. It does not run FDTD, FWI,",
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
    parser.add_argument("--image-objective-run", default=DEFAULT_IMAGE_OBJECTIVE_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_image_objective_rank_diagnostic")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.summary_root) / args.image_objective_run
    rows = read_csv_rows(source_dir / "data/local_2d_detector_image_objective_gate_rows.csv")
    source_summary = read_json(source_dir / "data/local_2d_detector_image_objective_gate_summary.json")
    case_rows = build_case_rank_rows(rows)
    objective_rows = build_objective_rows(case_rows)
    summary = summarize_rank_diagnostic(case_rows, objective_rows, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_image_objective_rank_cases.csv"
    objective_csv = data_dir / "local_2d_detector_image_objective_rank_summary.csv"
    summary_json = data_dir / "local_2d_detector_image_objective_rank_diagnostic_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_image_objective_rank_diagnostic.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(case_csv, [json_safe(row) for row in case_rows])
    write_csv(objective_csv, [json_safe(row) for row in objective_rows])
    plot_rank_diagnostic(summary, objective_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_image_objective_rows_csv": str(source_dir / "data/local_2d_detector_image_objective_gate_rows.csv"),
        "source_image_objective_summary_json": str(
            source_dir / "data/local_2d_detector_image_objective_gate_summary.json"
        ),
        "case_csv": str(case_csv),
        "objective_summary_csv": str(objective_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, case_csv, objective_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_image_objective_rank_diagnostic",
        {
            "image_objective_run": args.image_objective_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
