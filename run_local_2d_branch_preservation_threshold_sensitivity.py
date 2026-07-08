#!/usr/bin/env python3
"""Sweep branch-preservation thresholds over saved coordinate candidate surfaces."""

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
from run_local_2d_branch_preservation_archive_audit import (  # noqa: E402
    candidate_summary_paths,
    candidate_surface_rows,
    resolve_candidate_path,
    step_case_label,
    target_truth,
)
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def parse_float_csv(value: str) -> list[float]:
    return [float(item.strip()) for item in str(value).split(",") if item.strip()]


def build_step_records(root: Path, limit: int | None = None) -> list[dict]:
    records = []
    seen_steps: set[tuple[str, str, int, str]] = set()
    paths = candidate_summary_paths(root)
    if limit is not None:
        paths = paths[: int(limit)]
    for summary_path in paths:
        summary = read_json(summary_path)
        for step in summary.get("steps", []):
            target_index = safe_int(step.get("target_index"), -1)
            raw_candidate_csv = step.get("candidate_csv")
            if target_index < 0 or not raw_candidate_csv:
                continue
            candidate_csv = resolve_candidate_path(str(raw_candidate_csv), summary_path)
            case_label = step_case_label(summary, step) or ""
            dedupe_key = (str(summary_path), str(candidate_csv), target_index, case_label)
            if dedupe_key in seen_steps or not candidate_csv.exists():
                continue
            seen_steps.add(dedupe_key)
            rows = candidate_surface_rows(candidate_csv, case_label)
            if not rows:
                continue
            best = rows[0]
            best_misfit = safe_float(best.get("misfit"))
            truth_x, truth_z = target_truth(summary, target_index)
            truth_lateral = [row for row in rows if math.isclose(safe_float(row.get("x_mm")), truth_x, abs_tol=1.0e-9)]
            truth_lateral_best = min(truth_lateral, key=lambda row: safe_float(row.get("misfit"))) if truth_lateral else {}
            truth_lateral_misfit = safe_float(truth_lateral_best.get("misfit"), math.nan)
            truth_lateral_gap_abs = truth_lateral_misfit - best_misfit if math.isfinite(truth_lateral_misfit) else math.nan
            truth_lateral_gap_rel = (
                truth_lateral_gap_abs / best_misfit
                if best_misfit and math.isfinite(truth_lateral_gap_abs)
                else math.nan
            )
            candidate_gaps = []
            for row in rows:
                misfit = safe_float(row.get("misfit"))
                gap_abs = misfit - best_misfit
                gap_rel = gap_abs / best_misfit if best_misfit else math.inf
                candidate_gaps.append((gap_abs, gap_rel))
            records.append({
                "run_dir": summary_path.parents[1].name,
                "run_name": summary.get("run_name", ""),
                "target_index": target_index,
                "case_label": case_label,
                "candidate_csv": str(candidate_csv),
                "candidate_step_name": candidate_csv.name,
                "candidate_count": len(rows),
                "truth_x_mm": truth_x,
                "truth_z_mm": truth_z,
                "best_x_mm": safe_float(best.get("x_mm")),
                "best_z_mm": safe_float(best.get("z_mm")),
                "best_misfit": best_misfit,
                "selected_truth_lateral": math.isclose(safe_float(best.get("x_mm")), truth_x, abs_tol=1.0e-9),
                "truth_lateral_available": bool(truth_lateral),
                "truth_lateral_gap_abs": truth_lateral_gap_abs,
                "truth_lateral_gap_rel": truth_lateral_gap_rel,
                "candidate_gaps": candidate_gaps,
            })
    return records


def retained_count(candidate_gaps: list[tuple[float, float]], abs_cutoff: float, rel_cutoff: float) -> int:
    count = 0
    for index, (gap_abs, gap_rel) in enumerate(candidate_gaps):
        if index == 0 or (gap_abs <= abs_cutoff and gap_rel <= rel_cutoff):
            count += 1
    return count


def summarize_threshold(records: list[dict], abs_cutoff: float, rel_cutoff: float) -> dict:
    audited = len(records)
    missed_available = [
        row for row in records if row["truth_lateral_available"] and not row["selected_truth_lateral"]
    ]
    missed_recovered = [
        row
        for row in missed_available
        if safe_float(row.get("truth_lateral_gap_abs"), math.inf) <= abs_cutoff
        and safe_float(row.get("truth_lateral_gap_rel"), math.inf) <= rel_cutoff
    ]
    retained_counts = [
        retained_count(row["candidate_gaps"], abs_cutoff=abs_cutoff, rel_cutoff=rel_cutoff) for row in records
    ]
    extra_counts = [max(0, count - 1) for count in retained_counts]
    target2_recovered = [row for row in missed_recovered if safe_int(row.get("target_index"), -1) == 2]
    return {
        "abs_gap_cutoff": abs_cutoff,
        "rel_gap_cutoff": rel_cutoff,
        "audited_step_count": audited,
        "missed_truth_lateral_available_count": len(missed_available),
        "missed_truth_lateral_recovered_count": len(missed_recovered),
        "missed_truth_lateral_recovery_fraction": (
            len(missed_recovered) / len(missed_available) if missed_available else math.nan
        ),
        "target2_missed_truth_lateral_recovered_count": len(target2_recovered),
        "mean_retained_candidates_per_step": float(np.mean(retained_counts)) if retained_counts else math.nan,
        "p95_retained_candidates_per_step": float(np.percentile(retained_counts, 95)) if retained_counts else math.nan,
        "max_retained_candidates_per_step": max(retained_counts) if retained_counts else 0,
        "mean_extra_candidates_per_step": float(np.mean(extra_counts)) if extra_counts else math.nan,
        "total_extra_candidates_retained": int(sum(extra_counts)),
    }


def build_threshold_rows(records: list[dict], abs_values: list[float], rel_values: list[float]) -> list[dict]:
    rows = []
    for abs_cutoff in abs_values:
        for rel_cutoff in rel_values:
            rows.append(summarize_threshold(records, abs_cutoff, rel_cutoff))
    return rows


def summarize_sensitivity(rows: list[dict], default_abs: float, default_rel: float) -> dict:
    default_row = next(
        (
            row
            for row in rows
            if math.isclose(row["abs_gap_cutoff"], default_abs)
            and math.isclose(row["rel_gap_cutoff"], default_rel)
        ),
        {},
    )
    recovered_counts = [safe_int(row.get("missed_truth_lateral_recovered_count"), 0) for row in rows]
    extra_counts = [safe_float(row.get("mean_extra_candidates_per_step"), math.nan) for row in rows]
    efficient_rows = [
        row
        for row in rows
        if safe_int(row.get("missed_truth_lateral_recovered_count"), 0) == max(recovered_counts)
    ]
    efficient = min(efficient_rows, key=lambda row: safe_float(row.get("mean_extra_candidates_per_step"))) if efficient_rows else {}
    default_recovered = safe_int(default_row.get("missed_truth_lateral_recovered_count"), 0)
    return {
        "policy_label": "local_2d_branch_preservation_threshold_sensitivity_cpu_no_gpu",
        "threshold_combo_count": len(rows),
        "default_abs_gap_cutoff": default_abs,
        "default_rel_gap_cutoff": default_rel,
        "default_recovered_count": default_recovered,
        "default_mean_extra_candidates_per_step": safe_float(default_row.get("mean_extra_candidates_per_step"), math.nan),
        "max_recovered_count": max(recovered_counts) if recovered_counts else 0,
        "min_mean_extra_candidates_per_step": min(extra_counts) if extra_counts else math.nan,
        "most_efficient_max_recovery_abs_gap_cutoff": safe_float(efficient.get("abs_gap_cutoff"), math.nan),
        "most_efficient_max_recovery_rel_gap_cutoff": safe_float(efficient.get("rel_gap_cutoff"), math.nan),
        "most_efficient_max_recovery_mean_extra_candidates_per_step": safe_float(
            efficient.get("mean_extra_candidates_per_step"), math.nan
        ),
        "default_recovers_max_count": default_recovered == (max(recovered_counts) if recovered_counts else 0),
        "ready_for_default_threshold_policy": bool(default_row) and default_recovered > 0,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as CPU threshold sensitivity for branch preservation. "
            "Thresholds can support manuscript policy wording, but this does not "
            "launch GPU work or detector-seeded FWI."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "default_threshold_policy",
            "ready": summary["ready_for_default_threshold_policy"],
            "allowed_use": "branch-preservation threshold wording",
            "blocked_use": "deployable selector guarantee",
            "evidence": (
                f"default recovered={summary['default_recovered_count']}; "
                f"default extra/step={summary['default_mean_extra_candidates_per_step']:.3f}"
            ),
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch broad branch-preserving queue",
            "evidence": "threshold sensitivity is CPU-only",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "no detector-to-FWI contract",
        },
    ]


def matrix_from_rows(rows: list[dict], key: str) -> tuple[list[float], list[float], np.ndarray]:
    abs_values = sorted({safe_float(row["abs_gap_cutoff"]) for row in rows})
    rel_values = sorted({safe_float(row["rel_gap_cutoff"]) for row in rows})
    matrix = np.full((len(rel_values), len(abs_values)), np.nan, dtype=float)
    abs_index = {value: index for index, value in enumerate(abs_values)}
    rel_index = {value: index for index, value in enumerate(rel_values)}
    for row in rows:
        matrix[rel_index[safe_float(row["rel_gap_cutoff"])], abs_index[safe_float(row["abs_gap_cutoff"])]] = safe_float(
            row.get(key)
        )
    return abs_values, rel_values, matrix


def plot_sensitivity(rows: list[dict], summary: dict, save_path: Path) -> str:
    abs_values, rel_values, recovered = matrix_from_rows(rows, "missed_truth_lateral_recovered_count")
    _, _, extra = matrix_from_rows(rows, "mean_extra_candidates_per_step")
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.2), constrained_layout=True)
    for ax, matrix, title, label in [
        (axes[0], recovered, "Recovered Missed Truth-Lateral Branches", "count"),
        (axes[1], extra, "Mean Extra Retained Candidates Per Step", "extra candidates"),
    ]:
        image = ax.imshow(matrix, origin="lower", aspect="auto", cmap="viridis")
        ax.set_xticks(range(len(abs_values)))
        ax.set_xticklabels([f"{value:g}" for value in abs_values])
        ax.set_yticks(range(len(rel_values)))
        ax.set_yticklabels([f"{value:g}" for value in rel_values])
        ax.set_xlabel("absolute gap cutoff")
        ax.set_ylabel("relative gap cutoff")
        ax.set_title(title)
        cbar = fig.colorbar(image, ax=ax, shrink=0.85)
        cbar.set_label(label)
        for y in range(matrix.shape[0]):
            for x in range(matrix.shape[1]):
                value = matrix[y, x]
                ax.text(x, y, f"{value:.2g}", ha="center", va="center", color="white", fontsize=8)
    axes[0].text(
        0.02,
        0.95,
        f"default recovered={summary['default_recovered_count']}\n"
        f"default extra/step={summary['default_mean_extra_candidates_per_step']:.3f}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[0].transAxes,
        ha="left",
        va="top",
        fontsize=8.8,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D Branch-Preservation Threshold Sensitivity", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_branch_preservation_threshold_sensitivity.png`",
                "",
                "This figure sweeps absolute and relative branch-preservation gap cutoffs",
                "over saved coordinate optimizer candidate surfaces.",
                "",
                f"Default recovered branches: `{summary['default_recovered_count']}`.",
                f"Default extra candidates per step: `{summary['default_mean_extra_candidates_per_step']:.3f}`.",
                f"Default recovers max count: `{summary['default_recovers_max_count']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This is CPU-only threshold sensitivity over saved candidate CSVs.",
                "It does not run FDTD/FWI, launch GPU work, or define a deployable",
                "detector-to-FWI handoff.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--abs-values", default="0.001,0.002,0.005,0.01,0.02")
    parser.add_argument("--rel-values", default="0.01,0.02,0.05,0.1,0.2")
    parser.add_argument("--default-abs", type=float, default=0.01)
    parser.add_argument("--default-rel", type=float, default=0.10)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--run-name", default="local_2d_branch_preservation_threshold_sensitivity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    records = build_step_records(Path(args.experiment_root), limit=args.limit)
    threshold_rows = build_threshold_rows(records, parse_float_csv(args.abs_values), parse_float_csv(args.rel_values))
    summary = summarize_sensitivity(threshold_rows, args.default_abs, args.default_rel)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    threshold_csv = data_dir / "local_2d_branch_preservation_threshold_sensitivity_rows.csv"
    gates_csv = data_dir / "local_2d_branch_preservation_threshold_sensitivity_gates.csv"
    summary_json = data_dir / "local_2d_branch_preservation_threshold_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_branch_preservation_threshold_sensitivity.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_sensitivity(threshold_rows, summary, figure_path)
    write_csv(threshold_csv, [json_safe(row) for row in threshold_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "threshold_rows_csv": str(threshold_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_branch_preservation_threshold_sensitivity",
        {
            "experiment_root": args.experiment_root,
            "abs_values": args.abs_values,
            "rel_values": args.rel_values,
            "default_abs": args.default_abs,
            "default_rel": args.default_rel,
            "summary_json": str(summary_json),
            "threshold_rows_csv": str(threshold_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
