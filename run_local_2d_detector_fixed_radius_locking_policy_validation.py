#!/usr/bin/env python3
"""Synthesize the guarded validation of the fixed-radius locking policy."""

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
from run_local_2d_detector_fixed_radius_pilot_outcome_synthesis import format_values, parse_values, vector_errors  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_DESIGN_RUN = "130_local_2d_detector_fixed_radius_locking_policy_design"
DEFAULT_VALIDATION_RUN = "1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu"
DEFAULT_GUARD_SUMMARY = (
    "outputs/resource_guards/"
    "local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu_guard_summary.json"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def final_linf_error(summary: dict) -> tuple[list[float], list[float], float]:
    final_state = summary.get("final_state", {})
    final_x = parse_values(final_state.get("x_values_mm", []))
    final_z = parse_values(final_state.get("z_values_mm", []))
    true_x = parse_values(summary.get("true_x_values_mm", []))
    true_z = parse_values(summary.get("true_z_values_mm", []))
    x_errors = vector_errors(final_x, true_x)
    z_errors = vector_errors(final_z, true_z)
    linf = max([abs(value) for value in x_errors + z_errors], default=0.0)
    return x_errors, z_errors, linf


def build_validation_rows(validation_summary: dict) -> list[dict]:
    true_x = parse_values(validation_summary.get("true_x_values_mm", []))
    true_z = parse_values(validation_summary.get("true_z_values_mm", []))
    true_radii = parse_values(
        validation_summary.get("truth_radius_values_mm") or validation_summary.get("truth_radius_mm")
    )
    rows: list[dict] = []
    for confidence in validation_summary.get("confidence_rows", []):
        target = safe_int(confidence.get("target_rebar_index"), -1)
        best_x = safe_float(confidence.get("best_x_mm"), math.nan)
        best_z = safe_float(confidence.get("best_z_mm"), math.nan)
        best_r = safe_float(confidence.get("best_radius_mm"), math.nan)
        truth_selected = (
            abs(best_x - true_x[target]) <= 1.0e-9
            and abs(best_z - true_z[target]) <= 1.0e-9
            and abs(best_r - true_radii[target]) <= 1.0e-9
        )
        best_misfit = safe_float(confidence.get("best_misfit"), math.nan)
        competitor_misfit = safe_float(confidence.get("competing_geometry_misfit"), math.nan)
        rows.append(
            {
                "target_index": target,
                "candidate_count": safe_int(confidence.get("candidate_count"), 0),
                "best_x_mm": best_x,
                "best_z_mm": best_z,
                "best_radius_mm": best_r,
                "truth_x_mm": true_x[target],
                "truth_z_mm": true_z[target],
                "truth_radius_mm": true_radii[target],
                "truth_selected": truth_selected,
                "best_misfit": best_misfit,
                "competing_geometry_x_mm": safe_float(confidence.get("competing_geometry_x_mm"), math.nan),
                "competing_geometry_z_mm": safe_float(confidence.get("competing_geometry_z_mm"), math.nan),
                "competing_geometry_misfit": competitor_misfit,
                "competing_minus_best_abs": competitor_misfit - best_misfit,
                "competing_minus_best_rel": (
                    (competitor_misfit - best_misfit) / best_misfit if best_misfit else math.nan
                ),
                "ambiguity_candidate_count": safe_int(confidence.get("ambiguity_candidate_count"), 0),
                "truth_selected_but_ambiguous": (
                    truth_selected and safe_int(confidence.get("ambiguity_candidate_count"), 0) > 1
                ),
                "allowed_use": "single-branch fixed-radius locking validation evidence",
                "blocked_use": "broad detector policy claim, detector-seeded FWI, field transfer",
            }
        )
    return rows


def summarize_validation(
    design_summary: dict,
    validation_summary: dict,
    guard_summary: dict,
    validation_rows: list[dict],
) -> dict:
    x_errors, z_errors, linf = final_linf_error(validation_summary)
    truth_selected_count = sum(1 for row in validation_rows if boolish(row.get("truth_selected")))
    ambiguous_count = sum(1 for row in validation_rows if boolish(row.get("truth_selected_but_ambiguous")))
    exact = linf <= 1.0e-9
    guard_ok = (
        not boolish(guard_summary.get("aborted", False))
        and safe_float(guard_summary.get("max_gpu_util_percent"), 0.0) <= 90.0
        and safe_float(guard_summary.get("max_ram_used_percent"), 0.0) <= 80.0
    )
    return {
        "policy_label": "local_2d_detector_fixed_radius_locking_policy_validation_cpu_synthesis",
        "source_design_policy_label": design_summary.get("policy_label", ""),
        "source_validation_run": validation_summary.get("run_name", ""),
        "target_count": len(validation_rows),
        "truth_selected_count": truth_selected_count,
        "truth_selected_but_ambiguous_count": ambiguous_count,
        "final_x_errors_mm": format_values(x_errors),
        "final_z_errors_mm": format_values(z_errors),
        "final_linf_error_mm": linf,
        "exact_geometry_recovered": exact,
        "guard_aborted": boolish(guard_summary.get("aborted", False)),
        "guard_max_gpu_util_percent": safe_float(guard_summary.get("max_gpu_util_percent"), 0.0),
        "guard_max_ram_used_percent": safe_float(guard_summary.get("max_ram_used_percent"), 0.0),
        "guard_within_caps": guard_ok,
        "ready_for_locking_mechanism_claim": exact and guard_ok and truth_selected_count == len(validation_rows),
        "ready_for_general_detector_policy_claim": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_transfer": False,
        "gpu_priority": "none",
        "decision": (
            "The single guarded unlock probe validates the fixed-radius near-tie "
            "downstream-clearance mechanism on this repaired target2_close14 branch: "
            "target2 moves to exact truth after target1 is locked to [250,90]. Treat "
            "this as a mechanism result, not as a general detector-policy or FWI claim."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "locking_mechanism_claim",
            "ready": summary["ready_for_locking_mechanism_claim"],
            "allowed_use": "single-branch mechanism evidence",
            "blocked_use": "general detector policy claim",
            "evidence": (
                f"exact={summary['exact_geometry_recovered']}; "
                f"guard_ok={summary['guard_within_caps']}; "
                f"truth_selected={summary['truth_selected_count']}/{summary['target_count']}"
            ),
        },
        {
            "gate_key": "general_detector_policy_claim",
            "ready": summary["ready_for_general_detector_policy_claim"],
            "allowed_use": "none",
            "blocked_use": "claiming deployable policy without multi-case validation",
            "evidence": "validation covers one target2_close14 repaired branch",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad detector-refinement queue",
            "evidence": "mechanism validation does not open a queue",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "FWI launch",
            "evidence": "fixed radii are still controlled priors",
        },
    ]


def plot_validation(summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
    axes[0].bar(
        ["final\nLinf", "truth\nselected", "ambiguous"],
        [
            summary["final_linf_error_mm"],
            summary["truth_selected_count"],
            summary["truth_selected_but_ambiguous_count"],
        ],
        color=["#59a14f", "#4e79a7", "#f28e2b"],
    )
    axes[0].set_title("Validation result")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["mechanism", "general\npolicy", "broad\nGPU", "FWI"]
    gate_values = [
        summary["ready_for_locking_mechanism_claim"],
        summary["ready_for_general_detector_policy_claim"],
        summary["ready_for_broad_gpu_queue"],
        summary["ready_for_detector_seeded_fwi"],
    ]
    axes[1].bar(
        gate_labels,
        [1 if value else 0 for value in gate_values],
        color=["#59a14f" if value else "#bab0ac" for value in gate_values],
    )
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_ylim(0, 1.15)
    axes[1].set_title("Claim gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.04,
        0.08,
        f"GPU max={summary['guard_max_gpu_util_percent']:.0f}%\n"
        f"RAM max={summary['guard_max_ram_used_percent']:.2f}%\n"
        f"priority={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.3,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Fixed-radius locking policy validation", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_fixed_radius_locking_policy_validation.png`",
                "",
                "This CPU-only figure summarizes the guarded validation probe for the",
                "fixed-radius near-tie downstream-clearance locking design.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Exact geometry recovered: `{summary['exact_geometry_recovered']}`.",
                f"Truth selected but ambiguous count: `{summary['truth_selected_but_ambiguous_count']}`.",
                f"Guard max GPU utilization: `{summary['guard_max_gpu_util_percent']}` percent.",
                f"Guard max RAM used: `{summary['guard_max_ram_used_percent']}` percent.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "This validates one fixed-radius mechanism branch. It does not authorize",
                "a broad detector queue, detector-seeded FWI, field transfer, 3D/HPC work,",
                "or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design-run", default=DEFAULT_DESIGN_RUN)
    parser.add_argument("--validation-run", default=DEFAULT_VALIDATION_RUN)
    parser.add_argument("--guard-summary", default=DEFAULT_GUARD_SUMMARY)
    parser.add_argument("--run-name", default="local_2d_detector_fixed_radius_locking_policy_validation")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    design_dir = Path("outputs/summary_tables") / args.design_run
    validation_dir = Path("outputs/experiments") / args.validation_run
    design_summary = read_json(design_dir / "data/local_2d_detector_fixed_radius_locking_policy_summary.json")
    validation_summary = read_json(validation_dir / "data/multi_rebar_coordinate_optimizer_summary.json")
    guard_summary = read_json(args.guard_summary)
    validation_rows = build_validation_rows(validation_summary)
    summary = summarize_validation(design_summary, validation_summary, guard_summary, validation_rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_fixed_radius_locking_policy_validation_rows.csv"
    gates_csv = data_dir / "local_2d_detector_fixed_radius_locking_policy_validation_gates.csv"
    summary_json = data_dir / "local_2d_detector_fixed_radius_locking_policy_validation_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_fixed_radius_locking_policy_validation.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in validation_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_validation(summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "source_design_summary_json": str(
                design_dir / "data/local_2d_detector_fixed_radius_locking_policy_summary.json"
            ),
            "source_validation_summary_json": str(
                validation_dir / "data/multi_rebar_coordinate_optimizer_summary.json"
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
        "local_2d_detector_fixed_radius_locking_policy_validation",
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
