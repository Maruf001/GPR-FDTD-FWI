#!/usr/bin/env python3
"""Audit residual ambiguity after the fixed-radius detector second-pass pilot."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

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
from run_local_2d_detector_fixed_radius_pilot_outcome_synthesis import parse_values, vector_errors  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PILOT_RUN = "1357_local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu"
DEFAULT_SYNTHESIS_RUN = "127_local_2d_detector_fixed_radius_pilot_outcome_synthesis_post_second_pass"
EXPECTED_FULL_GRID_CANDIDATES = 25


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def format_values(values: list[float]) -> str:
    return ",".join(f"{float(value):g}" for value in values)


def _candidate_key(row: dict) -> tuple[float, float, float]:
    return (
        safe_float(row.get("x_mm"), math.nan),
        safe_float(row.get("z_mm"), math.nan),
        safe_float(row.get("radius_mm"), math.nan),
    )


def _same_float(first: float, second: float, tolerance: float = 1.0e-9) -> bool:
    return abs(float(first) - float(second)) <= tolerance


def _same_candidate(row: dict, x_mm: float, z_mm: float, radius_mm: float) -> bool:
    x_value, z_value, radius_value = _candidate_key(row)
    return (
        _same_float(x_value, x_mm)
        and _same_float(z_value, z_mm)
        and _same_float(radius_value, radius_mm)
    )


def rank_candidates(rows: list[dict]) -> list[dict]:
    ranked = sorted(rows, key=lambda row: safe_float(row.get("misfit"), math.inf))
    outputs: list[dict] = []
    for index, row in enumerate(ranked, start=1):
        enriched = dict(row)
        enriched["rank"] = index
        outputs.append(enriched)
    return outputs


def _confidence_by_target(summary: dict) -> dict[int, dict]:
    return {
        safe_int(row.get("target_rebar_index"), safe_int(row.get("step_target_index"), -1)): row
        for row in summary.get("confidence_rows", [])
    }


def audit_step(
    *,
    step: dict,
    candidates: list[dict],
    confidence: dict,
    true_x: list[float],
    true_z: list[float],
    true_radii: list[float],
    final_x: list[float],
    final_z: list[float],
) -> dict:
    ranked = rank_candidates(candidates)
    if not ranked:
        raise ValueError("candidate table is empty")
    best = ranked[0]
    target_index = safe_int(step.get("target_index"), safe_int(best.get("target_index"), -1))
    truth_x = true_x[target_index]
    truth_z = true_z[target_index]
    truth_radius = true_radii[target_index]
    truth_rows = [
        row for row in ranked
        if _same_candidate(row, truth_x, truth_z, truth_radius)
    ]
    truth_row = truth_rows[0] if truth_rows else None
    best_misfit = safe_float(best.get("misfit"), math.nan)
    truth_misfit = safe_float(truth_row.get("misfit"), math.nan) if truth_row else math.nan
    truth_delta = truth_misfit - best_misfit if math.isfinite(truth_misfit) else math.nan
    selected_truth = _same_candidate(best, truth_x, truth_z, truth_radius)
    ambiguity_count = safe_int(confidence.get("ambiguity_candidate_count"), 0)
    candidate_count = len(ranked)
    candidate_shortfall = max(0, EXPECTED_FULL_GRID_CANDIDATES - candidate_count)
    final_x_error = float(final_x[target_index]) - float(truth_x)
    final_z_error = float(final_z[target_index]) - float(truth_z)
    if selected_truth and ambiguity_count > 1:
        residual_mode = "truth_selected_but_ambiguous"
    elif truth_row is None and candidate_shortfall > 0:
        residual_mode = "truth_candidate_absent_after_nonoverlap_filter"
    elif truth_row is None:
        residual_mode = "truth_candidate_absent"
    elif not selected_truth:
        residual_mode = "truth_present_but_objective_prefers_neighbor"
    else:
        residual_mode = "truth_selected_clean"
    return {
        "target_index": target_index,
        "candidate_csv": step.get("candidate_csv", ""),
        "candidate_count": candidate_count,
        "candidate_shortfall_from_25": candidate_shortfall,
        "selected_x_mm": safe_float(best.get("x_mm"), math.nan),
        "selected_z_mm": safe_float(best.get("z_mm"), math.nan),
        "selected_radius_mm": safe_float(best.get("radius_mm"), math.nan),
        "truth_x_mm": truth_x,
        "truth_z_mm": truth_z,
        "truth_radius_mm": truth_radius,
        "selected_is_truth_coordinate": selected_truth,
        "truth_candidate_present": truth_row is not None,
        "truth_candidate_rank": None if truth_row is None else safe_int(truth_row.get("rank"), 0),
        "best_misfit": best_misfit,
        "truth_candidate_misfit": None if not math.isfinite(truth_misfit) else truth_misfit,
        "truth_minus_best_misfit_abs": None if not math.isfinite(truth_delta) else truth_delta,
        "truth_minus_best_misfit_rel": (
            None if not math.isfinite(truth_delta) or best_misfit == 0.0
            else truth_delta / best_misfit
        ),
        "ambiguity_candidate_count": ambiguity_count,
        "ambiguity_misfit_threshold": safe_float(confidence.get("ambiguity_misfit_threshold"), math.nan),
        "final_x_error_mm": final_x_error,
        "final_z_error_mm": final_z_error,
        "final_linf_error_mm": max(abs(final_x_error), abs(final_z_error)),
        "residual_mode": residual_mode,
        "ready_for_more_gpu": False,
        "allowed_use": "CPU residual-cause audit for fixed-radius detector refinement",
        "blocked_use": "immediate GPU loop, broad detector queue, field transfer, FWI launch",
    }


def build_audit_rows(summary: dict) -> list[dict]:
    true_x = parse_values(summary.get("true_x_values_mm", []))
    true_z = parse_values(summary.get("true_z_values_mm", []))
    true_radii = parse_values(summary.get("truth_radius_values_mm") or summary.get("truth_radius_mm"))
    final_x = parse_values(summary.get("final_state", {}).get("x_values_mm", []))
    final_z = parse_values(summary.get("final_state", {}).get("z_values_mm", []))
    confidence_lookup = _confidence_by_target(summary)
    rows: list[dict] = []
    for step in summary.get("steps", []):
        if step.get("step_kind", "main") not in {"main", ""}:
            continue
        target_index = safe_int(step.get("target_index"), -1)
        candidate_csv = step.get("candidate_csv")
        if not candidate_csv:
            continue
        candidates = read_csv_rows(Path(candidate_csv))
        rows.append(
            audit_step(
                step=step,
                candidates=candidates,
                confidence=confidence_lookup.get(target_index, {}),
                true_x=true_x,
                true_z=true_z,
                true_radii=true_radii,
                final_x=final_x,
                final_z=final_z,
            )
        )
    return rows


def summarize(summary: dict, synthesis_summary: dict, audit_rows: list[dict], guard_summary: dict | None) -> dict:
    final_x = parse_values(summary.get("final_state", {}).get("x_values_mm", []))
    final_z = parse_values(summary.get("final_state", {}).get("z_values_mm", []))
    true_x = parse_values(summary.get("true_x_values_mm", []))
    true_z = parse_values(summary.get("true_z_values_mm", []))
    final_x_errors = vector_errors(final_x, true_x)
    final_z_errors = vector_errors(final_z, true_z)
    selected_truth = [row for row in audit_rows if boolish(row.get("selected_is_truth_coordinate"))]
    truth_present = [row for row in audit_rows if boolish(row.get("truth_candidate_present"))]
    absent_nonoverlap = [
        row for row in audit_rows
        if row.get("residual_mode") == "truth_candidate_absent_after_nonoverlap_filter"
    ]
    objective_neighbor = [
        row for row in audit_rows
        if row.get("residual_mode") == "truth_present_but_objective_prefers_neighbor"
    ]
    truth_ambiguous = [
        row for row in audit_rows
        if row.get("residual_mode") == "truth_selected_but_ambiguous"
    ]
    return {
        "policy_label": "local_2d_detector_fixed_radius_residual_ambiguity_audit_cpu_no_gpu",
        "source_pilot_run": summary.get("run_name", ""),
        "source_synthesis_policy_label": synthesis_summary.get("policy_label", ""),
        "target_count": len(audit_rows),
        "selected_truth_coordinate_count": len(selected_truth),
        "truth_candidate_present_count": len(truth_present),
        "truth_candidate_absent_count": len(audit_rows) - len(truth_present),
        "truth_selected_but_ambiguous_count": len(truth_ambiguous),
        "truth_present_but_objective_prefers_neighbor_count": len(objective_neighbor),
        "truth_absent_after_nonoverlap_filter_count": len(absent_nonoverlap),
        "final_x_errors_mm": format_values(final_x_errors),
        "final_z_errors_mm": format_values(final_z_errors),
        "final_linf_error_mm": max([abs(value) for value in final_x_errors + final_z_errors], default=0.0),
        "best_truth_minus_best_misfit_abs": min(
            (
                safe_float(row.get("truth_minus_best_misfit_abs"), math.inf)
                for row in audit_rows
                if row.get("truth_minus_best_misfit_abs") is not None
            ),
            default=None,
        ),
        "max_truth_minus_best_misfit_abs": max(
            (
                safe_float(row.get("truth_minus_best_misfit_abs"), -math.inf)
                for row in audit_rows
                if row.get("truth_minus_best_misfit_abs") is not None
            ),
            default=None,
        ),
        "guard_aborted": None if guard_summary is None else boolish(guard_summary.get("aborted")),
        "guard_max_gpu_util_percent": None if guard_summary is None else guard_summary.get("max_gpu_util_percent"),
        "guard_max_ram_used_percent": None if guard_summary is None else guard_summary.get("max_ram_used_percent"),
        "ready_for_immediate_gpu_iteration": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_transfer": False,
        "gpu_priority": "none",
        "decision": (
            "The 1 mm residual is not a simple need-more-iterations signal. Target 0 "
            "selects truth but has a near tie, target 1 has the exact coordinate present "
            "but slightly worse than a neighbor, and target 2's exact coordinate is absent "
            "after the non-overlap filter because earlier residuals constrain the sequential "
            "state. Do CPU-side update-order/locking design before any further GPU work."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "residual_cause_identified",
            "ready": True,
            "allowed_use": "interpret second-pass residual",
            "blocked_use": "exact-recovery claim",
            "evidence": (
                f"objective-neighbor={summary['truth_present_but_objective_prefers_neighbor_count']}; "
                f"nonoverlap-absent={summary['truth_absent_after_nonoverlap_filter_count']}"
            ),
        },
        {
            "gate_key": "immediate_gpu_iteration",
            "ready": summary["ready_for_immediate_gpu_iteration"],
            "allowed_use": "none",
            "blocked_use": "another second-pass GPU loop",
            "evidence": "residual cause is policy/coordinate-coupling, not missing local samples",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "fresh detector-seed queue",
            "evidence": "post-pilot residual needs interpretation first",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "FWI launch",
            "evidence": "coordinate residual remains and radius/material are controlled priors",
        },
    ]


def plot_audit(summary: dict, audit_rows: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.6), constrained_layout=True)
    labels = [f"T{safe_int(row['target_index'], 0)}" for row in audit_rows]
    errors = [safe_float(row.get("final_linf_error_mm"), 0.0) for row in audit_rows]
    truth_delta = [
        safe_float(row.get("truth_minus_best_misfit_abs"), 0.0)
        if row.get("truth_minus_best_misfit_abs") is not None else 0.0
        for row in audit_rows
    ]
    present = [1 if boolish(row.get("truth_candidate_present")) else 0 for row in audit_rows]

    axes[0].bar(labels, errors, color=["#59a14f" if value == 0 else "#f28e2b" for value in errors])
    axes[0].set_ylabel("final coordinate error (mm)")
    axes[0].set_title("Residual by target")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(labels, truth_delta, color="#4e79a7")
    axes[1].set_ylabel("truth minus best misfit")
    axes[1].set_title("Truth objective penalty")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(labels, present, color=["#59a14f" if value else "#e15759" for value in present])
    axes[2].set_yticks([0, 1], ["absent", "present"])
    axes[2].set_ylim(0, 1.15)
    axes[2].set_title("Truth candidate availability")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[2].text(
        0.04,
        0.08,
        f"final Linf={summary['final_linf_error_mm']} mm\n"
        f"objective-neighbor={summary['truth_present_but_objective_prefers_neighbor_count']}\n"
        f"nonoverlap-absent={summary['truth_absent_after_nonoverlap_filter_count']}\n"
        f"GPU next={summary['gpu_priority']}",
        transform=axes[2].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.3,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("Fixed-radius second-pass residual ambiguity audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_fixed_radius_residual_ambiguity_audit.png`",
                "",
                "This CPU-only figure audits why the guarded fixed-radius second-pass",
                "pilot stopped at a 1 mm residual instead of exact recovery.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Final L-infinity residual: `{summary['final_linf_error_mm']}` mm.",
                f"Truth selected but ambiguous: `{summary['truth_selected_but_ambiguous_count']}`.",
                f"Truth present but objective prefers neighbor: `{summary['truth_present_but_objective_prefers_neighbor_count']}`.",
                f"Truth absent after non-overlap filtering: `{summary['truth_absent_after_nonoverlap_filter_count']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "This audit does not authorize another GPU iteration, broad detector",
                "queue, detector-seeded FWI, field transfer, 3D/HPC work, or neural",
                "network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-run", default=DEFAULT_PILOT_RUN)
    parser.add_argument("--synthesis-run", default=DEFAULT_SYNTHESIS_RUN)
    parser.add_argument("--guard-summary", default="outputs/resource_guards/local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu_guard_summary.json")
    parser.add_argument("--run-name", default="local_2d_detector_fixed_radius_residual_ambiguity_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_dir = Path("outputs/experiments") / args.pilot_run
    synthesis_dir = Path("outputs/summary_tables") / args.synthesis_run
    optimizer_summary = read_json(experiment_dir / "data/multi_rebar_coordinate_optimizer_summary.json")
    synthesis_summary = read_json(
        synthesis_dir / "data/local_2d_detector_fixed_radius_pilot_outcome_synthesis_summary.json"
    )
    guard_summary = read_json(args.guard_summary) if args.guard_summary and Path(args.guard_summary).exists() else None
    audit_rows = build_audit_rows(optimizer_summary)
    summary = summarize(optimizer_summary, synthesis_summary, audit_rows, guard_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_fixed_radius_residual_ambiguity_rows.csv"
    gates_csv = data_dir / "local_2d_detector_fixed_radius_residual_ambiguity_gates.csv"
    summary_json = data_dir / "local_2d_detector_fixed_radius_residual_ambiguity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_fixed_radius_residual_ambiguity_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in audit_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_audit(summary, audit_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "source_optimizer_summary_json": str(experiment_dir / "data/multi_rebar_coordinate_optimizer_summary.json"),
            "source_synthesis_summary_json": str(
                synthesis_dir / "data/local_2d_detector_fixed_radius_pilot_outcome_synthesis_summary.json"
            ),
            "source_guard_summary_json": str(args.guard_summary),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_fixed_radius_residual_ambiguity_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
