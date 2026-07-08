#!/usr/bin/env python3
"""Audit whether blind-envelope detector rows define a refinement launch contract."""

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
from run_local_2d_detector_blind_envelope_robustness_audit import parse_bool  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BLIND_ENVELOPE_RUN = "059_local_2d_detector_blind_component_envelope_assembly"
DEFAULT_ROBUSTNESS_RUN = "061_local_2d_detector_blind_envelope_robustness_audit"
DEFAULT_STABILITY_RUN = "063_local_2d_detector_blind_envelope_policy_stability"
DEFAULT_RELIABILITY_RUN = "069_local_2d_detector_blind_envelope_reliability_gate"
DEFAULT_PHYSICS_LINK_RUN = "074_local_2d_detector_physics_ambiguity_link"
DEFAULT_UPPER_BOUND_RUN = "039_local_2d_detector_upper_bound_policy_post_selector_audit"
DEFAULT_COARSE_ERROR_GATE_MM = 10.0


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _lookup(rows: list[dict], key: str) -> dict[str, dict]:
    return {str(row.get(key, "")): row for row in rows}


def selected_best_variant_rows(selected_rows: list[dict], best_variant_label: str) -> list[dict]:
    return sorted(
        [row for row in selected_rows if str(row.get("variant_label", "")) == best_variant_label],
        key=lambda row: (str(row.get("branch_key", "")), safe_int(row.get("seed"), 0), str(row.get("case_variant", ""))),
    )


def build_contract_rows(
    best_rows: list[dict],
    reliability_rows: list[dict],
    coarse_error_gate_mm: float = DEFAULT_COARSE_ERROR_GATE_MM,
) -> list[dict]:
    reliability_by_case = _lookup(reliability_rows, "case_label")
    outputs = []
    for row in best_rows:
        case_label = str(row.get("case_label", ""))
        reliability = reliability_by_case.get(case_label, {})
        stable = parse_bool(reliability.get("truth_free_stable_assignment"))
        review = not stable
        all_variant_success = safe_float(reliability.get("success_fraction_truth_eval"), 0.0) == 1.0
        best_hits = parse_bool(row.get("all_target_slots_hit"))
        max_error = safe_float(row.get("max_target_slot_abs_error_mm"), math.nan)
        coarse_error_ok = math.isfinite(max_error) and max_error <= coarse_error_gate_mm
        candidate_component_seed_ready = stable and all_variant_success and best_hits and coarse_error_ok
        outputs.append(
            {
                "case_label": case_label,
                "branch_key": row.get("branch_key", ""),
                "seed": safe_int(row.get("seed"), 0),
                "case_variant": row.get("case_variant", ""),
                "selection_mode": row.get("selection_mode", ""),
                "selected_x_values_mm": row.get("selected_x_values_mm", ""),
                "selected_z_values_mm": row.get("selected_z_values_mm", ""),
                "selected_component_count": safe_int(row.get("selected_component_count"), 0),
                "component_candidate_count": safe_int(row.get("component_candidate_count"), 0),
                "detector_reliability_label": reliability.get("truth_free_reliability_label", ""),
                "truth_free_stable_assignment": stable,
                "review_assignment": review,
                "success_fraction_truth_eval": safe_float(reliability.get("success_fraction_truth_eval"), 0.0),
                "all_variant_success": all_variant_success,
                "best_variant_all_slots_hit": best_hits,
                "max_target_slot_abs_error_mm": max_error,
                "coarse_error_gate_mm": coarse_error_gate_mm,
                "coarse_error_gate_pass": coarse_error_ok,
                "radius_seed_available": False,
                "material_seed_available": False,
                "candidate_component_seed_ready": candidate_component_seed_ready,
                "gpu_refinement_launch_ready": False,
                "launch_blocker": (
                    "review_assignment"
                    if review
                    else "missing_radius_material_and_independent_validation"
                ),
            }
        )
    return outputs


def build_branch_rows(contract_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in contract_rows:
        grouped[str(row.get("branch_key", ""))].append(row)
    outputs = []
    for branch_key, rows in grouped.items():
        stable_rows = [row for row in rows if row["truth_free_stable_assignment"]]
        seed_ready_rows = [row for row in rows if row["candidate_component_seed_ready"]]
        review_rows = [row for row in rows if row["review_assignment"]]
        outputs.append(
            {
                "branch_key": branch_key,
                "case_count": len(rows),
                "stable_case_count": len(stable_rows),
                "candidate_component_seed_ready_count": len(seed_ready_rows),
                "review_case_count": len(review_rows),
                "max_target_slot_abs_error_mm": max(
                    [safe_float(row.get("max_target_slot_abs_error_mm"), math.nan) for row in rows]
                    or [math.nan]
                ),
                "median_target_slot_abs_error_mm": float(
                    np.nanmedian([safe_float(row.get("max_target_slot_abs_error_mm"), math.nan) for row in rows])
                )
                if rows
                else math.nan,
                "review_case_labels": ";".join(str(row["case_label"]) for row in review_rows),
            }
        )
    return sorted(outputs, key=lambda row: row["branch_key"])


def build_blocker_rows(
    blind_summary: dict,
    robustness_summary: dict,
    reliability_summary: dict,
    physics_link_summary: dict,
    upper_bound_summary: dict,
) -> list[dict]:
    return [
        {
            "blocker_key": "radius_material_contract_missing",
            "blocks_gpu_refinement": True,
            "evidence": "blind-envelope detector rows provide x/z component locations but not radius/material seeds",
            "source_metric": "radius_seed_available=false; material_seed_available=false",
        },
        {
            "blocker_key": "policy_grid_selected_on_saved_corpus",
            "blocks_gpu_refinement": bool(blind_summary.get("uses_truth_for_grid_scoring", True)),
            "evidence": "best blind-envelope grid was selected using the saved synthetic corpus",
            "source_metric": f"uses_truth_for_grid_scoring={blind_summary.get('uses_truth_for_grid_scoring', '')}",
        },
        {
            "blocker_key": "deployable_top1_selector_not_validated",
            "blocks_gpu_refinement": safe_float(
                upper_bound_summary.get("best_deployable_selector_all_truth_case_count"), 0.0
            )
            < safe_float(upper_bound_summary.get("case_count"), 0.0),
            "evidence": "validated truth-free top-1 selector does not recover all saved cases",
            "source_metric": (
                f"deployable_top1={upper_bound_summary.get('best_deployable_selector_all_truth_case_count', 0)}/"
                f"{upper_bound_summary.get('case_count', 0)}"
            ),
        },
        {
            "blocker_key": "branch_independent_transfer_not_robust",
            "blocks_gpu_refinement": not bool(robustness_summary.get("heldout_branch_robust", False)),
            "evidence": "leave-one-branch transfer drops one case",
            "source_metric": (
                f"leave_one_branch={robustness_summary.get('leave_one_branch_all_target_slot_case_count', 0)}/"
                f"{robustness_summary.get('leave_one_branch_case_count', 0)}"
            ),
        },
        {
            "blocker_key": "review_cases_present",
            "blocks_gpu_refinement": safe_float(reliability_summary.get("review_assignment_case_count"), 0.0) > 0.0,
            "evidence": "truth-free reliability gate flags close50 nominal review cases",
            "source_metric": f"review_cases={reliability_summary.get('review_assignment_case_count', 0)}",
        },
        {
            "blocker_key": "per_seed_physics_equivalence_not_ready",
            "blocks_gpu_refinement": not bool(
                physics_link_summary.get("ready_for_per_seed_physics_equivalence_claim", False)
            ),
            "evidence": "coordinate x ambiguity explains only part of the detector review set",
            "source_metric": (
                f"x_ambiguous_reviews={physics_link_summary.get('review_cases_with_synthetic_x_ambiguity_count', 0)}/"
                f"{physics_link_summary.get('detector_review_case_count', 0)}"
            ),
        },
    ]


def summarize_contract(
    contract_rows: list[dict],
    branch_rows: list[dict],
    blocker_rows: list[dict],
    blind_summary: dict,
    reliability_summary: dict,
    upper_bound_summary: dict,
    coarse_error_gate_mm: float = DEFAULT_COARSE_ERROR_GATE_MM,
) -> dict:
    stable_rows = [row for row in contract_rows if row["truth_free_stable_assignment"]]
    ready_rows = [row for row in contract_rows if row["candidate_component_seed_ready"]]
    review_rows = [row for row in contract_rows if row["review_assignment"]]
    active_blockers = [row for row in blocker_rows if row["blocks_gpu_refinement"]]
    launch_ready = len(active_blockers) == 0 and len(ready_rows) == len(contract_rows)
    return {
        "policy_label": "local_2d_detector_refinement_launch_contract_audit_cpu_no_fwi",
        "source_blind_envelope_policy_label": blind_summary.get("policy_label", ""),
        "source_reliability_policy_label": reliability_summary.get("policy_label", ""),
        "source_upper_bound_policy_label": upper_bound_summary.get("policy_label", ""),
        "case_count": len(contract_rows),
        "branch_count": len(branch_rows),
        "best_variant_label": blind_summary.get("best_variant_label", ""),
        "coarse_error_gate_mm": coarse_error_gate_mm,
        "truth_free_stable_case_count": len(stable_rows),
        "review_case_count": len(review_rows),
        "candidate_component_seed_ready_count": len(ready_rows),
        "candidate_component_seed_ready_fraction": len(ready_rows) / len(contract_rows) if contract_rows else 0.0,
        "candidate_component_seed_ready_labels": ";".join(str(row["case_label"]) for row in ready_rows),
        "review_case_labels": ";".join(str(row["case_label"]) for row in review_rows),
        "max_component_seed_error_mm": max(
            [safe_float(row.get("max_target_slot_abs_error_mm"), math.nan) for row in contract_rows]
            or [math.nan]
        ),
        "stable_max_component_seed_error_mm": max(
            [safe_float(row.get("max_target_slot_abs_error_mm"), math.nan) for row in stable_rows]
            or [math.nan]
        ),
        "radius_seed_available": False,
        "material_seed_available": False,
        "active_blocker_count": len(active_blockers),
        "active_blocker_keys": ";".join(str(row["blocker_key"]) for row in active_blockers),
        "deployable_selector_all_truth_case_count": safe_float(
            upper_bound_summary.get("best_deployable_selector_all_truth_case_count"), 0.0
        ),
        "rank_gated_upper_bound_all_truth_case_count": safe_float(
            upper_bound_summary.get("best_rank_gated_upper_bound_all_truth_case_count"), 0.0
        ),
        "ready_for_component_seed_table": len(ready_rows) > 0,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_detector_seeded_fwi": launch_ready,
        "gpu_priority": "none",
        "decision": (
            "The stable detector cases can be exported as a saved-corpus x/z component seed table, "
            "but they do not define a GPU/FWI launch contract. Radius/material seeds, independent "
            "deployable top-1 validation, branch-independent transfer, and review-case closure are still missing."
        ),
    }


def plot_contract(branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["branch_key"].replace("target2_", "").replace("_linear29p5", "\n29.5") for row in branch_rows]
    stable = [safe_float(row.get("stable_case_count"), 0.0) for row in branch_rows]
    ready = [safe_float(row.get("candidate_component_seed_ready_count"), 0.0) for row in branch_rows]
    review = [safe_float(row.get("review_case_count"), 0.0) for row in branch_rows]
    x = np.arange(len(branch_rows))

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.0), constrained_layout=True)
    axes[0].bar(x - 0.22, stable, width=0.22, label="stable", color="#4e79a7")
    axes[0].bar(x, ready, width=0.22, label="x/z seed table", color="#59a14f")
    axes[0].bar(x + 0.22, review, width=0.22, label="review", color="#e15759")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("case count")
    axes[0].set_title("Detector component seed readiness")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(fontsize=8)

    axes[1].bar(
        ["x/z seed table", "narrow refinement", "detector FWI"],
        [
            1 if summary["ready_for_component_seed_table"] else 0,
            1 if summary["ready_for_narrow_refinement_contract"] else 0,
            1 if summary["ready_for_detector_seeded_fwi"] else 0,
        ],
        color=["#59a14f", "#e15759", "#e15759"],
    )
    axes[1].set_ylim(-0.15, 1.25)
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_title("Launch contract gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"seed table cases: {summary['candidate_component_seed_ready_count']}/{summary['case_count']}\n"
        f"review cases: {summary['review_case_count']}\n"
        f"active blockers: {summary['active_blocker_count']}\n"
        f"radius seed: {summary['radius_seed_available']}\n"
        f"FWI ready: {summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Detector refinement launch contract audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, contract_csv: Path, blockers_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_refinement_launch_contract_audit.png`",
                "",
                "This CPU-only figure audits whether the saved blind-envelope detector",
                "assignments define a refinement launch contract.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Candidate component seed table cases: `{summary['candidate_component_seed_ready_count']}` / `{summary['case_count']}`.",
                f"Review cases: `{summary['review_case_count']}`.",
                f"Active blocker count: `{summary['active_blocker_count']}`.",
                f"Active blockers: `{summary['active_blocker_keys']}`.",
                f"Ready for component seed table: `{summary['ready_for_component_seed_table']}`.",
                f"Ready for narrow refinement contract: `{summary['ready_for_narrow_refinement_contract']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Contract rows: `{contract_csv.name}`.",
                f"- Blocker rows: `{blockers_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved detector policy rows only. It does not run FDTD,",
                "FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--blind-envelope-run", default=DEFAULT_BLIND_ENVELOPE_RUN)
    parser.add_argument("--robustness-run", default=DEFAULT_ROBUSTNESS_RUN)
    parser.add_argument("--stability-run", default=DEFAULT_STABILITY_RUN)
    parser.add_argument("--reliability-run", default=DEFAULT_RELIABILITY_RUN)
    parser.add_argument("--physics-link-run", default=DEFAULT_PHYSICS_LINK_RUN)
    parser.add_argument("--upper-bound-run", default=DEFAULT_UPPER_BOUND_RUN)
    parser.add_argument("--coarse-error-gate-mm", type=float, default=DEFAULT_COARSE_ERROR_GATE_MM)
    parser.add_argument("--run-name", default="local_2d_detector_refinement_launch_contract_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.summary_root)
    blind_dir = root / args.blind_envelope_run
    robustness_dir = root / args.robustness_run
    stability_dir = root / args.stability_run
    reliability_dir = root / args.reliability_run
    physics_dir = root / args.physics_link_run
    upper_bound_dir = root / args.upper_bound_run

    blind_summary = read_json(blind_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json")
    robustness_summary = read_json(robustness_dir / "data/local_2d_detector_blind_envelope_robustness_summary.json")
    stability_summary = read_json(stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_summary.json")
    reliability_summary = read_json(
        reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
    )
    physics_summary = read_json(physics_dir / "data/local_2d_detector_physics_ambiguity_link_summary.json")
    upper_bound_summary = read_json(upper_bound_dir / "data/local_2d_detector_upper_bound_policy_summary.json")
    selected_rows = read_csv_rows(
        blind_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
    )
    reliability_rows = read_csv_rows(
        reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_cases.csv"
    )

    best_rows = selected_best_variant_rows(selected_rows, str(blind_summary.get("best_variant_label", "")))
    contract_rows = build_contract_rows(best_rows, reliability_rows, args.coarse_error_gate_mm)
    branch_rows = build_branch_rows(contract_rows)
    blocker_rows = build_blocker_rows(
        blind_summary,
        robustness_summary,
        reliability_summary,
        physics_summary,
        upper_bound_summary,
    )
    summary = summarize_contract(
        contract_rows,
        branch_rows,
        blocker_rows,
        blind_summary,
        reliability_summary,
        upper_bound_summary,
        args.coarse_error_gate_mm,
    )
    summary["source_stability_policy_label"] = stability_summary.get("policy_label", "")

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    contract_csv = data_dir / "local_2d_detector_refinement_launch_contract_cases.csv"
    branch_csv = data_dir / "local_2d_detector_refinement_launch_contract_branches.csv"
    blockers_csv = data_dir / "local_2d_detector_refinement_launch_contract_blockers.csv"
    summary_json = data_dir / "local_2d_detector_refinement_launch_contract_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_refinement_launch_contract_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(contract_csv, [json_safe(row) for row in contract_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(blockers_csv, [json_safe(row) for row in blocker_rows])
    plot_contract(branch_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, contract_csv, blockers_csv)

    summary["paths"] = {
        "contract_cases_csv": str(contract_csv),
        "branch_csv": str(branch_csv),
        "blocker_csv": str(blockers_csv),
        "summary_json": str(summary_json),
        "source_blind_envelope_summary_json": str(
            blind_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
        ),
        "source_blind_envelope_selected_cases_csv": str(
            blind_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
        ),
        "source_robustness_summary_json": str(
            robustness_dir / "data/local_2d_detector_blind_envelope_robustness_summary.json"
        ),
        "source_stability_summary_json": str(
            stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_summary.json"
        ),
        "source_reliability_summary_json": str(
            reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
        ),
        "source_physics_link_summary_json": str(
            physics_dir / "data/local_2d_detector_physics_ambiguity_link_summary.json"
        ),
        "source_upper_bound_summary_json": str(
            upper_bound_dir / "data/local_2d_detector_upper_bound_policy_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_refinement_launch_contract_audit",
        {
            "blind_envelope_run": args.blind_envelope_run,
            "robustness_run": args.robustness_run,
            "stability_run": args.stability_run,
            "reliability_run": args.reliability_run,
            "physics_link_run": args.physics_link_run,
            "upper_bound_run": args.upper_bound_run,
            "coarse_error_gate_mm": args.coarse_error_gate_mm,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
