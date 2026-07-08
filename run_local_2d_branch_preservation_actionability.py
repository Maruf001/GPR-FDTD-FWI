#!/usr/bin/env python3
"""Rank missed-but-retained branch-preservation archive rows by actionability."""

from __future__ import annotations

import argparse
import ast
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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_AUDIT_ROWS = (
    "outputs/summary_tables/094_local_2d_branch_preservation_archive_audit/"
    "data/local_2d_branch_preservation_archive_audit_rows.csv"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float_list(value: object) -> list[float]:
    if isinstance(value, list):
        return [safe_float(item) for item in value]
    parsed = ast.literal_eval(str(value))
    if not isinstance(parsed, list):
        raise ValueError(f"expected list literal, got {value!r}")
    return [safe_float(item) for item in parsed]


def linf_error_mm(truth_x: list[float], truth_z: list[float], x_values: list[float], z_values: list[float]) -> float:
    truth_x_arr = np.asarray(truth_x, dtype=float)
    truth_z_arr = np.asarray(truth_z, dtype=float)
    x_arr = np.asarray(x_values, dtype=float)
    z_arr = np.asarray(z_values, dtype=float)
    return float(max(np.max(np.abs(x_arr - truth_x_arr)), np.max(np.abs(z_arr - truth_z_arr))))


def candidate_rows(path: Path, case_label: str) -> list[dict]:
    rows = [row for row in read_csv_rows(path) if not case_label or row.get("case_label") == case_label]
    for row in rows:
        row["misfit"] = safe_float(row.get("misfit"))
        row["x_mm"] = safe_float(row.get("x_mm"))
        row["z_mm"] = safe_float(row.get("z_mm"))
    return sorted(rows, key=lambda row: row["misfit"])


def find_step_index(summary: dict, candidate_csv: str, target_index: int) -> int:
    candidate_name = Path(candidate_csv).name
    for index, step in enumerate(summary.get("steps", [])):
        if safe_int(step.get("target_index"), -1) != int(target_index):
            continue
        if Path(str(step.get("candidate_csv", ""))).name == candidate_name:
            return index
    return -1


def choose_truth_lateral_row(rows: list[dict], truth_x_mm: float) -> dict:
    matching = [row for row in rows if math.isclose(safe_float(row.get("x_mm")), truth_x_mm, abs_tol=1.0e-9)]
    if not matching:
        return {}
    return min(matching, key=lambda row: safe_float(row.get("misfit"), math.inf))


def actionability_label(row: dict) -> str:
    improvement = safe_float(row.get("candidate_linf_improvement_mm"), 0.0)
    has_downstream = boolish(row.get("has_downstream_steps"))
    already_coupled = str(row.get("run_dir", "")).startswith("1341_")
    if improvement > 0.0 and has_downstream and not already_coupled:
        return "candidate_for_narrow_coupled_probe"
    if improvement > 0.0:
        return "candidate_surface_selectable_improvement"
    if math.isclose(improvement, 0.0, abs_tol=1.0e-12):
        return "objective_near_tie_same_coordinate_error"
    return "truth_lateral_worse_coordinate_error"


def build_actionability_rows(audit_rows: list[dict]) -> list[dict]:
    rows = []
    missed_rows = [row for row in audit_rows if boolish(row.get("truth_lateral_retained_but_not_selected"))]
    for audit_row in missed_rows:
        summary_path = Path(str(audit_row["source_summary_json"]))
        candidate_csv = Path(str(audit_row["candidate_csv"]))
        case_label = str(audit_row.get("case_label", ""))
        target_index = safe_int(audit_row.get("target_index"), -1)
        summary = read_json(summary_path)
        truth_x = [safe_float(value) for value in summary["true_x_values_mm"]]
        truth_z = [safe_float(value) for value in summary["true_z_values_mm"]]
        rows_for_step = candidate_rows(candidate_csv, case_label)
        if not rows_for_step:
            continue
        best = rows_for_step[0]
        truth_row = choose_truth_lateral_row(rows_for_step, safe_float(audit_row.get("truth_x_mm")))
        if not truth_row:
            continue
        best_linf = linf_error_mm(
            truth_x,
            truth_z,
            parse_float_list(best["x_values_mm"]),
            parse_float_list(best["z_values_mm"]),
        )
        truth_linf = linf_error_mm(
            truth_x,
            truth_z,
            parse_float_list(truth_row["x_values_mm"]),
            parse_float_list(truth_row["z_values_mm"]),
        )
        step_index = find_step_index(summary, str(candidate_csv), target_index)
        has_downstream = step_index >= 0 and step_index < len(summary.get("steps", [])) - 1
        revisit = "revisit" in candidate_csv.name
        candidate_linf_improvement = best_linf - truth_linf
        output_row = {
            "run_dir": audit_row.get("run_dir", ""),
            "run_name": audit_row.get("run_name", ""),
            "target_index": target_index,
            "case_label": case_label,
            "candidate_csv": str(candidate_csv),
            "candidate_step_name": candidate_csv.name,
            "step_index": step_index,
            "has_downstream_steps": has_downstream,
            "is_revisit_step": revisit,
            "best_x_mm": safe_float(best.get("x_mm")),
            "best_z_mm": safe_float(best.get("z_mm")),
            "truth_lateral_x_mm": safe_float(truth_row.get("x_mm")),
            "truth_lateral_z_mm": safe_float(truth_row.get("z_mm")),
            "best_misfit": safe_float(best.get("misfit")),
            "truth_lateral_misfit": safe_float(truth_row.get("misfit")),
            "truth_lateral_gap_abs": safe_float(truth_row.get("misfit")) - safe_float(best.get("misfit")),
            "truth_lateral_gap_rel": (
                (safe_float(truth_row.get("misfit")) - safe_float(best.get("misfit"))) / safe_float(best.get("misfit"))
                if safe_float(best.get("misfit")) != 0.0
                else math.nan
            ),
            "best_candidate_linf_error_mm": best_linf,
            "truth_lateral_candidate_linf_error_mm": truth_linf,
            "candidate_linf_improvement_mm": candidate_linf_improvement,
            "already_coupled_followup": str(audit_row.get("run_dir", "")).startswith("1341_"),
            "source_summary_json": str(summary_path),
        }
        output_row["actionability_label"] = actionability_label(output_row)
        rows.append(output_row)
    return sorted(
        rows,
        key=lambda row: (
            row["actionability_label"] != "candidate_for_narrow_coupled_probe",
            -safe_float(row.get("candidate_linf_improvement_mm"), 0.0),
            safe_int(row.get("target_index"), 99),
            str(row.get("run_dir", "")),
        ),
    )


def summarize_actionability(rows: list[dict]) -> tuple[list[dict], dict]:
    labels = sorted({str(row["actionability_label"]) for row in rows})
    label_rows = []
    for label in labels:
        group = [row for row in rows if row["actionability_label"] == label]
        label_rows.append({
            "actionability_label": label,
            "row_count": len(group),
            "max_linf_improvement_mm": max((safe_float(row.get("candidate_linf_improvement_mm")) for row in group), default=math.nan),
            "mean_linf_improvement_mm": float(
                np.mean([safe_float(row.get("candidate_linf_improvement_mm")) for row in group])
            )
            if group
            else math.nan,
        })
    improved = [row for row in rows if safe_float(row.get("candidate_linf_improvement_mm")) > 0.0]
    same = [row for row in rows if math.isclose(safe_float(row.get("candidate_linf_improvement_mm")), 0.0, abs_tol=1.0e-12)]
    worse = [row for row in rows if safe_float(row.get("candidate_linf_improvement_mm")) < 0.0]
    coupled_candidates = [row for row in rows if row["actionability_label"] == "candidate_for_narrow_coupled_probe"]
    summary = {
        "policy_label": "local_2d_branch_preservation_actionability_cpu_no_gpu",
        "missed_retained_row_count": len(rows),
        "truth_lateral_improves_linf_count": len(improved),
        "truth_lateral_same_linf_count": len(same),
        "truth_lateral_worse_linf_count": len(worse),
        "narrow_coupled_probe_candidate_count": len(coupled_candidates),
        "already_coupled_followup_count": sum(1 for row in rows if boolish(row.get("already_coupled_followup"))),
        "max_linf_improvement_mm": max((safe_float(row.get("candidate_linf_improvement_mm")) for row in rows), default=math.nan),
        "mean_linf_improvement_mm": float(np.mean([safe_float(row.get("candidate_linf_improvement_mm")) for row in rows]))
        if rows
        else math.nan,
        "ready_for_branch_preservation_actionability_claim": bool(rows),
        "ready_for_narrow_gpu_probe": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use this CPU triage to separate archive near-ties that directly improve "
            "coordinate error from those that only mark objective ambiguity. Do not "
            "launch GPU work without a separate case-specific coupled-search design."
        ),
    }
    return label_rows, summary


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "branch_preservation_actionability_claim",
            "ready": summary["ready_for_branch_preservation_actionability_claim"],
            "allowed_use": "CPU triage of preserved truth-lateral branch impact",
            "blocked_use": "deployable branch selector guarantee",
            "evidence": f"missed-retained rows={summary['missed_retained_row_count']}",
        },
        {
            "gate_key": "narrow_gpu_probe",
            "ready": summary["ready_for_narrow_gpu_probe"],
            "allowed_use": "none",
            "blocked_use": "launch narrow GPU probe from this summary alone",
            "evidence": "requires a separate case-specific coupled-search design",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch broad branch-preserving queue",
            "evidence": "CPU triage only",
        },
    ]


def plot_actionability(rows: list[dict], label_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    labels = [row["actionability_label"].replace("_", "\n") for row in label_rows]
    counts = [row["row_count"] for row in label_rows]
    axes[0].bar(labels, counts, color="#607d8b")
    axes[0].set_ylabel("row count")
    axes[0].set_title("Missed-Retained Row Classes")
    axes[0].grid(axis="y", alpha=0.25)

    sorted_rows = sorted(rows, key=lambda row: safe_float(row.get("candidate_linf_improvement_mm")), reverse=True)
    gains = [safe_float(row.get("candidate_linf_improvement_mm")) for row in sorted_rows]
    colors = ["#2f9d55" if value > 0.0 else "#d8a03d" if math.isclose(value, 0.0, abs_tol=1e-12) else "#d6453d" for value in gains]
    axes[1].bar(np.arange(len(gains)), gains, color=colors)
    axes[1].axhline(0.0, color="#333333", linewidth=1.0)
    axes[1].set_xlabel("missed-retained row rank")
    axes[1].set_ylabel("L-inf improvement [mm]")
    axes[1].set_title("Truth-Lateral Candidate Coordinate Impact")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].text(
        0.02,
        0.94,
        f"improves={summary['truth_lateral_improves_linf_count']}\n"
        f"same={summary['truth_lateral_same_linf_count']}\n"
        f"worse={summary['truth_lateral_worse_linf_count']}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D Branch-Preservation Actionability Triage", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_branch_preservation_actionability.png`",
                "",
                "This figure triages the missed-but-retained truth-lateral rows from",
                "run `094` by their effect on full x/z coordinate error.",
                "",
                f"Rows triaged: `{summary['missed_retained_row_count']}`.",
                f"Truth-lateral improves L-inf count: `{summary['truth_lateral_improves_linf_count']}`.",
                f"Narrow GPU probe ready: `{summary['ready_for_narrow_gpu_probe']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This is CPU-only triage of saved candidate CSVs. It does not run",
                "new FDTD/FWI, launch GPU work, or define a deployable selector.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-rows", default=DEFAULT_AUDIT_ROWS)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="local_2d_branch_preservation_actionability")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    audit_rows = read_csv_rows(Path(args.audit_rows))
    rows = build_actionability_rows(audit_rows)
    label_rows, summary = summarize_actionability(rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_branch_preservation_actionability_rows.csv"
    label_csv = data_dir / "local_2d_branch_preservation_actionability_label_rows.csv"
    gates_csv = data_dir / "local_2d_branch_preservation_actionability_gates.csv"
    summary_json = data_dir / "local_2d_branch_preservation_actionability_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_branch_preservation_actionability.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_actionability(rows, label_rows, summary, figure_path)
    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(label_csv, [json_safe(row) for row in label_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "label_rows_csv": str(label_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_audit_rows_csv": args.audit_rows,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_branch_preservation_actionability",
        {
            "audit_rows": args.audit_rows,
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
