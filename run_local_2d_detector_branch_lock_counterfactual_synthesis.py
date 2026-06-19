#!/usr/bin/env python3
"""Synthesize the repaired-seed greedy branch-lock counterfactual."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_GREEDY_RUN = (
    "outputs/experiments/"
    "1341_local2d_repaired_exact_radius_seed_refine_target2_close14_seed21_nominal_gpu"
)
DEFAULT_COUNTERFACTUAL_RUN = (
    "outputs/experiments/"
    "1342_local2d_counterfactual_middle_neartie_target2_unlock_close14_seed21_nominal_gpu"
)
DEFAULT_ABS_GAP_CUTOFF = 0.01
DEFAULT_REL_GAP_CUTOFF = 0.10


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def candidate_rows(path: Path) -> list[dict]:
    rows = read_csv_rows(path)
    for row in rows:
        row["misfit"] = safe_float(row.get("misfit"))
        row["x_mm"] = safe_float(row.get("x_mm"))
        row["z_mm"] = safe_float(row.get("z_mm"))
        row["radius_mm"] = safe_float(row.get("radius_mm"))
    return sorted(rows, key=lambda item: item["misfit"])


def summary_path(run_dir: Path) -> Path:
    return run_dir / "data/multi_rebar_coordinate_optimizer_summary.json"


def confidence_path(run_dir: Path) -> Path:
    return run_dir / "data/coordinate_confidence_report.csv"


def step_for_target(summary: dict, target_index: int) -> dict:
    for step in summary.get("steps", []):
        if int(step.get("target_index", -1)) == int(target_index):
            return step
    raise ValueError(f"missing target {target_index} step")


def linf_error_mm(summary: dict, state_key: str) -> float:
    truth_x = np.asarray(summary["true_x_values_mm"], dtype=float)
    truth_z = np.asarray(summary["true_z_values_mm"], dtype=float)
    state = summary[state_key]
    x_values = np.asarray(state["x_values_mm"], dtype=float)
    z_values = np.asarray(state["z_values_mm"], dtype=float)
    return float(max(np.max(np.abs(x_values - truth_x)), np.max(np.abs(z_values - truth_z))))


def candidate_at_x_nearest_z(rows: list[dict], x_mm: float, z_mm: float) -> dict:
    matches = [row for row in rows if math.isclose(safe_float(row.get("x_mm")), float(x_mm), abs_tol=1.0e-9)]
    if not matches:
        raise ValueError(f"no candidate at x={x_mm:g} mm")
    return min(
        matches,
        key=lambda row: (
            abs(safe_float(row.get("z_mm")) - float(z_mm)),
            safe_float(row.get("misfit")),
        ),
    )


def has_candidate_at_x(rows: list[dict], x_mm: float) -> bool:
    return any(math.isclose(safe_float(row.get("x_mm")), float(x_mm), abs_tol=1.0e-9) for row in rows)


def build_synthesis(
    greedy_summary: dict,
    greedy_target1_rows: list[dict],
    greedy_target2_rows: list[dict],
    counterfactual_summary: dict,
    *,
    abs_gap_cutoff: float = DEFAULT_ABS_GAP_CUTOFF,
    rel_gap_cutoff: float = DEFAULT_REL_GAP_CUTOFF,
) -> tuple[list[dict], list[dict], dict]:
    target1_step = step_for_target(greedy_summary, 1)
    target2_step = step_for_target(greedy_summary, 2)
    counter_target2_step = step_for_target(counterfactual_summary, 2)

    truth_x = [safe_float(value) for value in greedy_summary["true_x_values_mm"]]
    truth_z = [safe_float(value) for value in greedy_summary["true_z_values_mm"]]
    selected_target1 = target1_step["best_candidate"]["params"]
    selected_target2 = target2_step["best_candidate"]["params"]
    counter_target2 = counter_target2_step["best_candidate"]["params"]
    near_tie_target1 = candidate_at_x_nearest_z(greedy_target1_rows, truth_x[1], truth_z[1])

    selected_target1_misfit = safe_float(target1_step["best_candidate"].get("misfit"))
    near_tie_misfit = safe_float(near_tie_target1.get("misfit"))
    near_tie_gap_abs = near_tie_misfit - selected_target1_misfit
    near_tie_gap_rel = near_tie_gap_abs / selected_target1_misfit if selected_target1_misfit else math.nan
    near_tie_retained = near_tie_gap_abs <= abs_gap_cutoff and near_tie_gap_rel <= rel_gap_cutoff

    greedy_has_target2_true_x = has_candidate_at_x(greedy_target2_rows, truth_x[2])
    counter_unlocked_target2_true_x = math.isclose(
        safe_float(counter_target2.get("x_mm")),
        truth_x[2],
        abs_tol=1.0e-9,
    )

    greedy_final_linf = linf_error_mm(greedy_summary, "final_state")
    counter_final_linf = linf_error_mm(counterfactual_summary, "final_state")
    counter_improvement = greedy_final_linf - counter_final_linf

    candidate_comparison_rows = [
        {
            "comparison_key": "target1_selected_branch",
            "target_index": 1,
            "x_mm": safe_float(selected_target1.get("x_mm")),
            "z_mm": safe_float(selected_target1.get("z_mm")),
            "misfit": selected_target1_misfit,
            "misfit_gap_abs_vs_selected": 0.0,
            "misfit_gap_rel_vs_selected": 0.0,
            "target2_true_lateral_candidate_available": "",
            "role": "greedy selected middle branch",
        },
        {
            "comparison_key": "target1_near_tie_truth_lateral_branch",
            "target_index": 1,
            "x_mm": safe_float(near_tie_target1.get("x_mm")),
            "z_mm": safe_float(near_tie_target1.get("z_mm")),
            "misfit": near_tie_misfit,
            "misfit_gap_abs_vs_selected": near_tie_gap_abs,
            "misfit_gap_rel_vs_selected": near_tie_gap_rel,
            "target2_true_lateral_candidate_available": "",
            "role": "near-tie middle branch retained by branch-preserving rule",
        },
        {
            "comparison_key": "target2_greedy_selected_middle",
            "target_index": 2,
            "x_mm": safe_float(selected_target2.get("x_mm")),
            "z_mm": safe_float(selected_target2.get("z_mm")),
            "misfit": safe_float(target2_step["best_candidate"].get("misfit")),
            "misfit_gap_abs_vs_selected": "",
            "misfit_gap_rel_vs_selected": "",
            "target2_true_lateral_candidate_available": greedy_has_target2_true_x,
            "role": "target2 after greedy middle branch",
        },
        {
            "comparison_key": "target2_counterfactual_near_tie_middle",
            "target_index": 2,
            "x_mm": safe_float(counter_target2.get("x_mm")),
            "z_mm": safe_float(counter_target2.get("z_mm")),
            "misfit": safe_float(counter_target2_step["best_candidate"].get("misfit")),
            "misfit_gap_abs_vs_selected": "",
            "misfit_gap_rel_vs_selected": "",
            "target2_true_lateral_candidate_available": True,
            "role": "target2 after near-tie middle branch",
        },
    ]

    summary = {
        "policy_label": "local_2d_detector_branch_lock_counterfactual_synthesis_cpu_no_fwi",
        "greedy_run_name": greedy_summary.get("run_name", ""),
        "counterfactual_run_name": counterfactual_summary.get("run_name", ""),
        "target1_selected_x_mm": safe_float(selected_target1.get("x_mm")),
        "target1_selected_z_mm": safe_float(selected_target1.get("z_mm")),
        "target1_selected_misfit": selected_target1_misfit,
        "target1_near_tie_x_mm": safe_float(near_tie_target1.get("x_mm")),
        "target1_near_tie_z_mm": safe_float(near_tie_target1.get("z_mm")),
        "target1_near_tie_misfit": near_tie_misfit,
        "target1_near_tie_gap_abs": near_tie_gap_abs,
        "target1_near_tie_gap_rel": near_tie_gap_rel,
        "branch_preservation_abs_gap_cutoff": abs_gap_cutoff,
        "branch_preservation_rel_gap_cutoff": rel_gap_cutoff,
        "target1_near_tie_retained_by_rule": near_tie_retained,
        "target2_true_lateral_candidate_available_after_greedy_middle": greedy_has_target2_true_x,
        "target2_counterfactual_unlocked_true_lateral": counter_unlocked_target2_true_x,
        "greedy_final_linf_error_mm": greedy_final_linf,
        "counterfactual_final_linf_error_mm": counter_final_linf,
        "counterfactual_linf_improvement_mm": counter_improvement,
        "ready_for_branch_preserving_selector_design": near_tie_retained and counter_unlocked_target2_true_x,
        "ready_for_coupled_middle_right_probe": near_tie_retained and counter_unlocked_target2_true_x,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "The repaired-seed residual is a greedy branch-lock/coupled-assignment "
            "problem. Preserve near-tie middle/right branches or test a small "
            "coupled middle-right selector before any broader GPU or FWI work."
        ),
    }
    gates = [
        {
            "gate_key": "branch_preserving_selector_design",
            "ready": summary["ready_for_branch_preserving_selector_design"],
            "allowed_use": "CPU design of branch-preserving selector or beam rule",
            "blocked_use": "claim deployable detector refinement policy",
            "evidence": (
                f"target1 near-tie rel gap={near_tie_gap_rel:.4f}; "
                f"target2 true lateral unlocked={counter_unlocked_target2_true_x}"
            ),
        },
        {
            "gate_key": "coupled_middle_right_probe",
            "ready": summary["ready_for_coupled_middle_right_probe"],
            "allowed_use": "one-case coupled middle-right diagnostic after CPU sizing",
            "blocked_use": "broad GPU campaign",
            "evidence": f"L-inf error improves {greedy_final_linf:.1f}->{counter_final_linf:.1f} mm",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch many repaired or coupled searches",
            "evidence": "single-case counterfactual only",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "branch-lock mechanism is not a validated FWI launch contract",
        },
    ]
    return candidate_comparison_rows, gates, summary


def plot_synthesis(rows: list[dict], summary: dict, save_path: Path) -> str:
    target1_rows = [row for row in rows if str(row["comparison_key"]).startswith("target1_")]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6), constrained_layout=True)
    labels = ["selected\nmiddle", "near-tie\nmiddle"]
    misfits = [safe_float(row.get("misfit")) for row in target1_rows]
    colors = ["#607d8b", "#f9a825"]
    axes[0].bar(labels, misfits, color=colors)
    axes[0].set_ylabel("target1 local misfit")
    axes[0].set_title("Middle Branch Near-Tie")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].text(
        0.5,
        0.92,
        f"gap={summary['target1_near_tie_gap_abs']:.4f} "
        f"({summary['target1_near_tie_gap_rel']:.1%})",
        transform=axes[0].transAxes,
        ha="center",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.3"},
    )

    axes[1].bar(
        ["greedy\nfinal", "counterfactual\nfinal"],
        [summary["greedy_final_linf_error_mm"], summary["counterfactual_final_linf_error_mm"]],
        color=["#d6453d", "#2f9d55"],
    )
    axes[1].set_ylabel("final L-infinity x/z error [mm]")
    axes[1].set_title("Target2 Unlock Effect")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].text(
        0.5,
        0.92,
        "target2 true-x candidate absent after greedy middle\n"
        "but selected after near-tie middle",
        transform=axes[1].transAxes,
        ha="center",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.3"},
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_branch_lock_counterfactual_synthesis.png`",
                "",
                "This figure summarizes the branch-lock mechanism found after the",
                "repaired exact-radius seed pilot. The left panel compares the greedy",
                "middle branch against the near-tie truth-lateral middle branch. The",
                "right panel compares final coordinate error before and after the",
                "target2 counterfactual unlock.",
                "",
                f"Near-tie relative gap: `{summary['target1_near_tie_gap_rel']:.4f}`.",
                f"Greedy/counterfactual L-infinity error: `{summary['greedy_final_linf_error_mm']:.1f}` / `{summary['counterfactual_final_linf_error_mm']:.1f}` mm.",
                "",
                "Scope boundary:",
                "",
                "This is a CPU synthesis of two narrow GPU diagnostics. It does not",
                "authorize broad GPU work, detector-seeded FWI, or a deployable",
                "field-transfer policy.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--greedy-run", default=DEFAULT_GREEDY_RUN)
    parser.add_argument("--counterfactual-run", default=DEFAULT_COUNTERFACTUAL_RUN)
    parser.add_argument("--abs-gap-cutoff", type=float, default=DEFAULT_ABS_GAP_CUTOFF)
    parser.add_argument("--rel-gap-cutoff", type=float, default=DEFAULT_REL_GAP_CUTOFF)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="local_2d_detector_branch_lock_counterfactual_synthesis")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    greedy_run = Path(args.greedy_run)
    counterfactual_run = Path(args.counterfactual_run)
    greedy_summary = read_json(summary_path(greedy_run))
    counterfactual_summary = read_json(summary_path(counterfactual_run))
    target1_step = step_for_target(greedy_summary, 1)
    target2_step = step_for_target(greedy_summary, 2)
    target1_rows = candidate_rows(Path(target1_step["candidate_csv"]))
    target2_rows = candidate_rows(Path(target2_step["candidate_csv"]))

    comparison_rows, gates, summary = build_synthesis(
        greedy_summary,
        target1_rows,
        target2_rows,
        counterfactual_summary,
        abs_gap_cutoff=args.abs_gap_cutoff,
        rel_gap_cutoff=args.rel_gap_cutoff,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    comparison_csv = data_dir / "local_2d_detector_branch_lock_counterfactual_synthesis_rows.csv"
    gates_csv = data_dir / "local_2d_detector_branch_lock_counterfactual_synthesis_gates.csv"
    summary_json = data_dir / "local_2d_detector_branch_lock_counterfactual_synthesis_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_branch_lock_counterfactual_synthesis.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_synthesis(comparison_rows, summary, figure_path)
    write_csv(comparison_csv, [json_safe(row) for row in comparison_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "comparison_csv": str(comparison_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "greedy_summary_json": str(summary_path(greedy_run)),
        "counterfactual_summary_json": str(summary_path(counterfactual_run)),
        "greedy_confidence_csv": str(confidence_path(greedy_run)),
        "counterfactual_confidence_csv": str(confidence_path(counterfactual_run)),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_branch_lock_counterfactual_synthesis",
        {
            "greedy_run": args.greedy_run,
            "counterfactual_run": args.counterfactual_run,
            "abs_gap_cutoff": args.abs_gap_cutoff,
            "rel_gap_cutoff": args.rel_gap_cutoff,
            "summary_json": str(summary_json),
            "comparison_csv": str(comparison_csv),
            "gates_csv": str(gates_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
