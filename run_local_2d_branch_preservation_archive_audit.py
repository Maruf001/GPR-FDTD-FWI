#!/usr/bin/env python3
"""Audit saved coordinate candidate surfaces for branch-preservation evidence."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def candidate_surface_rows(path: Path, case_label: str | None = None) -> list[dict]:
    rows = read_csv_rows(path)
    if case_label:
        selected = [row for row in rows if row.get("case_label") == case_label]
        if selected:
            rows = selected
    for row in rows:
        row["misfit"] = safe_float(row.get("misfit"))
        row["target_index"] = safe_int(row.get("target_index"), -1)
        row["x_mm"] = safe_float(row.get("x_mm"))
        row["z_mm"] = safe_float(row.get("z_mm"))
        row["radius_mm"] = safe_float(row.get("radius_mm"))
    return sorted(rows, key=lambda row: row["misfit"])


def candidate_summary_paths(root: Path) -> list[Path]:
    return sorted(root.glob("*/data/multi_rebar_coordinate_optimizer_summary.json"))


def step_case_label(summary: dict, step: dict) -> str | None:
    return (
        step.get("case_label")
        or summary.get("update_case_label")
        or (summary.get("replication_cases") or [{}])[0].get("label")
    )


def resolve_candidate_path(raw_path: str, summary_path: Path) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    if path.exists():
        return path
    return summary_path.parents[1] / path.name


def target_truth(summary: dict, target_index: int) -> tuple[float, float]:
    return (
        safe_float(summary["true_x_values_mm"][target_index]),
        safe_float(summary["true_z_values_mm"][target_index]),
    )


def audit_candidate_step(
    summary_path: Path,
    summary: dict,
    step: dict,
    *,
    abs_gap_cutoff: float,
    rel_gap_cutoff: float,
) -> dict | None:
    target_index = safe_int(step.get("target_index"), -1)
    raw_candidate_csv = step.get("candidate_csv")
    if not raw_candidate_csv or target_index < 0:
        return None
    candidate_csv = resolve_candidate_path(str(raw_candidate_csv), summary_path)
    if not candidate_csv.exists():
        return {
            "source_summary_json": str(summary_path),
            "run_dir": summary_path.parents[1].name,
            "run_name": summary.get("run_name", ""),
            "target_index": target_index,
            "candidate_csv": str(candidate_csv),
            "candidate_csv_exists": False,
            "audited": False,
            "reason": "missing_candidate_csv",
        }

    case_label = step_case_label(summary, step)
    rows = candidate_surface_rows(candidate_csv, case_label)
    if not rows:
        return {
            "source_summary_json": str(summary_path),
            "run_dir": summary_path.parents[1].name,
            "run_name": summary.get("run_name", ""),
            "target_index": target_index,
            "candidate_csv": str(candidate_csv),
            "candidate_csv_exists": True,
            "audited": False,
            "reason": "empty_candidate_surface",
        }

    truth_x, truth_z = target_truth(summary, target_index)
    best = rows[0]
    best_misfit = safe_float(best.get("misfit"))
    truth_lateral_rows = [row for row in rows if math.isclose(row["x_mm"], truth_x, abs_tol=1.0e-9)]
    truth_lateral_best = min(truth_lateral_rows, key=lambda row: row["misfit"]) if truth_lateral_rows else {}
    truth_misfit = safe_float(truth_lateral_best.get("misfit"), math.nan)
    gap_abs = truth_misfit - best_misfit if math.isfinite(truth_misfit) else math.nan
    gap_rel = gap_abs / best_misfit if best_misfit and math.isfinite(gap_abs) else math.nan
    retained = bool(truth_lateral_rows) and (
        math.isclose(gap_abs, 0.0, abs_tol=1.0e-12)
        or (gap_abs <= abs_gap_cutoff and gap_rel <= rel_gap_cutoff)
    )
    selected_truth_lateral = math.isclose(best["x_mm"], truth_x, abs_tol=1.0e-9)
    return {
        "source_summary_json": str(summary_path),
        "run_dir": summary_path.parents[1].name,
        "run_name": summary.get("run_name", ""),
        "target_index": target_index,
        "case_label": case_label or "",
        "candidate_csv": str(candidate_csv),
        "candidate_csv_exists": True,
        "audited": True,
        "reason": "ok",
        "candidate_count": len(rows),
        "truth_x_mm": truth_x,
        "truth_z_mm": truth_z,
        "best_x_mm": safe_float(best.get("x_mm")),
        "best_z_mm": safe_float(best.get("z_mm")),
        "best_misfit": best_misfit,
        "selected_truth_lateral": selected_truth_lateral,
        "truth_lateral_available": bool(truth_lateral_rows),
        "truth_lateral_candidate_count": len(truth_lateral_rows),
        "truth_lateral_best_x_mm": safe_float(truth_lateral_best.get("x_mm"), math.nan),
        "truth_lateral_best_z_mm": safe_float(truth_lateral_best.get("z_mm"), math.nan),
        "truth_lateral_best_misfit": truth_misfit,
        "truth_lateral_gap_abs": gap_abs,
        "truth_lateral_gap_rel": gap_rel,
        "truth_lateral_retained_by_rule": retained,
        "truth_lateral_retained_but_not_selected": retained and not selected_truth_lateral,
        "best_lateral_error_mm": abs(safe_float(best.get("x_mm")) - truth_x),
        "truth_lateral_best_depth_error_mm": (
            abs(safe_float(truth_lateral_best.get("z_mm"), math.nan) - truth_z)
            if truth_lateral_rows
            else math.nan
        ),
    }


def audit_archive(root: Path, *, abs_gap_cutoff: float, rel_gap_cutoff: float, limit: int | None = None) -> list[dict]:
    rows: list[dict] = []
    seen_steps: set[tuple[str, str, int, str]] = set()
    paths = candidate_summary_paths(root)
    if limit is not None:
        paths = paths[: int(limit)]
    for summary_path in paths:
        try:
            summary = read_json(summary_path)
        except (OSError, json.JSONDecodeError):
            rows.append({
                "source_summary_json": str(summary_path),
                "run_dir": summary_path.parents[1].name,
                "audited": False,
                "reason": "unreadable_summary",
            })
            continue
        for step in summary.get("steps", []):
            row = audit_candidate_step(
                summary_path,
                summary,
                step,
                abs_gap_cutoff=abs_gap_cutoff,
                rel_gap_cutoff=rel_gap_cutoff,
            )
            if row is not None:
                dedupe_key = (
                    str(row.get("source_summary_json", "")),
                    str(row.get("candidate_csv", "")),
                    safe_int(row.get("target_index"), -1),
                    str(row.get("case_label", "")),
                )
                if dedupe_key in seen_steps:
                    continue
                seen_steps.add(dedupe_key)
                rows.append(row)
    return rows


def summarize_by_target(rows: list[dict]) -> list[dict]:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("audited"):
            grouped[safe_int(row.get("target_index"), -1)].append(row)
    target_rows = []
    for target_index, group in sorted(grouped.items()):
        available = [row for row in group if row.get("truth_lateral_available")]
        retained = [row for row in group if row.get("truth_lateral_retained_by_rule")]
        selected = [row for row in group if row.get("selected_truth_lateral")]
        missed = [row for row in group if row.get("truth_lateral_retained_but_not_selected")]
        target_rows.append({
            "target_index": target_index,
            "audited_step_count": len(group),
            "truth_lateral_available_count": len(available),
            "truth_lateral_retained_count": len(retained),
            "selected_truth_lateral_count": len(selected),
            "retained_but_not_selected_count": len(missed),
            "retained_but_not_selected_fraction": len(missed) / len(group) if group else math.nan,
            "median_truth_lateral_gap_abs": float(
                np.nanmedian([safe_float(row.get("truth_lateral_gap_abs")) for row in group])
            ),
        })
    return target_rows


def summarize_archive(rows: list[dict], target_rows: list[dict], *, abs_gap_cutoff: float, rel_gap_cutoff: float) -> dict:
    audited = [row for row in rows if row.get("audited")]
    available = [row for row in audited if row.get("truth_lateral_available")]
    retained = [row for row in audited if row.get("truth_lateral_retained_by_rule")]
    selected = [row for row in audited if row.get("selected_truth_lateral")]
    missed = [row for row in audited if row.get("truth_lateral_retained_but_not_selected")]
    if missed:
        policy_label = "local_2d_branch_preservation_archive_audit_near_tie_missed_truth_lateral"
    else:
        policy_label = "local_2d_branch_preservation_archive_audit_no_missed_retained_truth_lateral"
    return {
        "policy_label": policy_label,
        "abs_gap_cutoff": abs_gap_cutoff,
        "rel_gap_cutoff": rel_gap_cutoff,
        "candidate_step_row_count": len(rows),
        "audited_step_count": len(audited),
        "truth_lateral_available_count": len(available),
        "truth_lateral_retained_count": len(retained),
        "selected_truth_lateral_count": len(selected),
        "retained_but_not_selected_count": len(missed),
        "retained_but_not_selected_fraction": len(missed) / len(audited) if audited else math.nan,
        "target_count": len(target_rows),
        "target_retained_but_not_selected_counts": ";".join(
            f"target{row['target_index']}={row['retained_but_not_selected_count']}" for row in target_rows
        ),
        "ready_for_branch_preservation_policy_claim": bool(missed),
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as a CPU archive audit of saved coordinate candidate surfaces. "
            "Missed-but-retained truth-lateral branches indicate where branch preservation "
            "may matter, but this scan does not launch broad GPU work or FWI."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "branch_preservation_policy_claim",
            "ready": summary["ready_for_branch_preservation_policy_claim"],
            "allowed_use": "CPU evidence for preserving near-tie lateral branches",
            "blocked_use": "general deployable selector guarantee",
            "evidence": f"retained-but-not-selected={summary['retained_but_not_selected_count']}",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch broad branch-preserving GPU queue",
            "evidence": "archive scan is CPU-only and does not size a GPU queue",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "candidate-surface audit only; no detector/FWI handoff contract",
        },
    ]


def plot_archive(target_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"target {row['target_index']}" for row in target_rows]
    selected = [row["selected_truth_lateral_count"] for row in target_rows]
    retained_missed = [row["retained_but_not_selected_count"] for row in target_rows]
    available = [row["truth_lateral_available_count"] for row in target_rows]

    fig, axes = plt.subplots(1, 2, figsize=(13.6, 4.8), constrained_layout=True)
    x = np.arange(len(labels))
    width = 0.26
    axes[0].bar(x - width, available, width=width, color="#607d8b", label="truth lateral available")
    axes[0].bar(x, selected, width=width, color="#2f9d55", label="selected truth lateral")
    axes[0].bar(x + width, retained_missed, width=width, color="#d8a03d", label="retained but not selected")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].set_ylabel("step count")
    axes[0].set_title("Archive Candidate-Surface Branch Outcomes")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(fontsize=8)

    fractions = [row["retained_but_not_selected_fraction"] for row in target_rows]
    axes[1].bar(labels, fractions, color="#d8a03d")
    axes[1].set_ylim(0, max([0.05, *fractions]) * 1.25)
    axes[1].set_ylabel("retained-but-not-selected fraction")
    axes[1].set_title("Missed Near-Tie Truth-Lateral Branch Rate")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].text(
        0.02,
        0.94,
        f"missed={summary['retained_but_not_selected_count']}\n"
        f"audited={summary['audited_step_count']}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D Branch-Preservation Archive Audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_branch_preservation_archive_audit.png`",
                "",
                "This figure summarizes a CPU-only scan of saved coordinate optimizer",
                "candidate surfaces for truth-lateral branches inside the preservation",
                "window.",
                "",
                f"Audited candidate steps: `{summary['audited_step_count']}`.",
                f"Truth-lateral branches retained but not selected: `{summary['retained_but_not_selected_count']}`.",
                f"Branch-preservation claim ready: `{summary['ready_for_branch_preservation_policy_claim']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This is an archive audit over saved candidate CSVs. It does not",
                "evaluate new coupled candidates, run FDTD/FWI, launch GPU work,",
                "or define a deployable detector-to-FWI handoff.",
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
    parser.add_argument("--abs-gap-cutoff", type=float, default=0.01)
    parser.add_argument("--rel-gap-cutoff", type=float, default=0.10)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--run-name", default="local_2d_branch_preservation_archive_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    rows = audit_archive(
        Path(args.experiment_root),
        abs_gap_cutoff=args.abs_gap_cutoff,
        rel_gap_cutoff=args.rel_gap_cutoff,
        limit=args.limit,
    )
    target_rows = summarize_by_target(rows)
    summary = summarize_archive(
        rows,
        target_rows,
        abs_gap_cutoff=args.abs_gap_cutoff,
        rel_gap_cutoff=args.rel_gap_cutoff,
    )
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_branch_preservation_archive_audit_rows.csv"
    target_csv = data_dir / "local_2d_branch_preservation_archive_audit_target_rows.csv"
    gates_csv = data_dir / "local_2d_branch_preservation_archive_audit_gates.csv"
    summary_json = data_dir / "local_2d_branch_preservation_archive_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_branch_preservation_archive_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_archive(target_rows, summary, figure_path)
    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(target_csv, [json_safe(row) for row in target_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "target_rows_csv": str(target_csv),
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
        "local_2d_branch_preservation_archive_audit",
        {
            "experiment_root": args.experiment_root,
            "abs_gap_cutoff": args.abs_gap_cutoff,
            "rel_gap_cutoff": args.rel_gap_cutoff,
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "target_rows_csv": str(target_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
