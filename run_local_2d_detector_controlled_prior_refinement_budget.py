#!/usr/bin/env python3
"""Budget controlled-prior detector refinement scopes without launching FWI."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from run_local_2d_detector_radius_material_prior_scope_audit import parse_float_list  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_XZ_CONTRACT_RUN = "088_local_2d_detector_xz_seed_neighborhood_contract"
DEFAULT_PRIOR_SCOPE_RUN = "089_local_2d_detector_radius_material_prior_scope_audit"
DEFAULT_COMPONENT_COUNT = 3


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def format_radius_pattern(values: list[float]) -> str:
    return ",".join(f"{value:g}" for value in values)


def radius_scope_rows(radius_values_mm: list[float], component_count: int) -> list[dict]:
    unique_count = len(set(radius_values_mm))
    fixed_count = 1
    permutation_count = math.factorial(unique_count) if unique_count == component_count else 0
    independent_count = unique_count**component_count if unique_count > 0 else 0
    return [
        {
            "radius_scope_key": "fixed_slot_radii",
            "radius_combination_count": fixed_count,
            "uses_truth_slot_assignment": True,
            "claim_scope": "controlled synthetic exact-radius ablation only",
            "ready_for_launch": False,
        },
        {
            "radius_scope_key": "known_radius_permutations",
            "radius_combination_count": permutation_count,
            "uses_truth_slot_assignment": False,
            "claim_scope": "known radius set with unknown slot assignment; budget only",
            "ready_for_launch": False,
        },
        {
            "radius_scope_key": "independent_known_radius_choices",
            "radius_combination_count": independent_count,
            "uses_truth_slot_assignment": False,
            "claim_scope": "independent per-slot choices from known synthetic radius set; budget only",
            "ready_for_launch": False,
        },
    ]


def _source_radius_pattern(prior_case_rows: list[dict]) -> list[float]:
    patterns = {
        str(row.get("truth_radius_pattern_key") or row.get("truth_radius_values_mm") or "")
        for row in prior_case_rows
        if str(row.get("truth_radius_pattern_key") or row.get("truth_radius_values_mm") or "")
    }
    if len(patterns) != 1:
        raise ValueError(f"expected exactly one radius pattern, found {sorted(patterns)!r}")
    return parse_float_list(next(iter(patterns)))


def build_budget_rows(
    branch_rows: list[dict],
    radius_rows: list[dict],
) -> list[dict]:
    outputs: list[dict] = []
    for branch in branch_rows:
        branch_key = str(branch.get("branch_key", ""))
        stable_count = safe_int(branch.get("stable_seed_case_count"), 0)
        review_count = safe_int(branch.get("review_case_count"), 0)
        fine_per_case = safe_int(branch.get("per_case_xz_grid_points_fine"), 0)
        fine_total = safe_int(branch.get("stable_total_xz_grid_points_fine"), 0)
        coarse_per_case = safe_int(branch.get("per_case_xz_grid_points_coarse"), 0)
        coarse_total = safe_int(branch.get("stable_total_xz_grid_points_coarse"), 0)
        for radius in radius_rows:
            combinations = safe_int(radius.get("radius_combination_count"), 0)
            outputs.append(
                {
                    "branch_key": branch_key,
                    "radius_scope_key": radius["radius_scope_key"],
                    "recommended_half_width_mm": safe_float(branch.get("recommended_half_width_mm")),
                    "fine_step_mm": safe_float(branch.get("fine_step_mm")),
                    "coarse_step_mm": safe_float(branch.get("coarse_step_mm")),
                    "stable_seed_case_count": stable_count,
                    "review_case_count": review_count,
                    "per_case_xz_grid_points_fine": fine_per_case,
                    "stable_total_xz_grid_points_fine": fine_total,
                    "per_case_xz_grid_points_coarse": coarse_per_case,
                    "stable_total_xz_grid_points_coarse": coarse_total,
                    "radius_combination_count": combinations,
                    "per_case_coordinate_radius_points_fine": fine_per_case * combinations,
                    "stable_total_coordinate_radius_points_fine": fine_total * combinations,
                    "per_case_coordinate_radius_points_coarse": coarse_per_case * combinations,
                    "stable_total_coordinate_radius_points_coarse": coarse_total * combinations,
                    "uses_truth_slot_assignment": radius["uses_truth_slot_assignment"],
                    "claim_scope": radius["claim_scope"],
                    "ready_for_launch": False,
                    "ready_for_detector_seeded_fwi": False,
                    "allowed_use": "budget sizing for controlled synthetic detector-refinement design",
                    "blocked_use": "refinement/FWI/GPU launch, field transfer, detector-inferred radius claim",
                }
            )
    return sorted(outputs, key=lambda row: (row["radius_scope_key"], row["branch_key"]))


def _total_for_scope(rows: list[dict], scope_key: str, field: str) -> int:
    return sum(safe_int(row.get(field), 0) for row in rows if row.get("radius_scope_key") == scope_key)


def summarize_budget(
    branch_rows: list[dict],
    prior_case_rows: list[dict],
    radius_rows: list[dict],
    budget_rows: list[dict],
    xz_summary: dict,
    prior_summary: dict,
    radius_values_mm: list[float],
) -> dict:
    stable_prior = [
        row for row in prior_case_rows if boolish(row.get("controlled_synthetic_prior_contract_ready"))
    ]
    review_rows = [row for row in prior_case_rows if boolish(row.get("review_assignment"))]
    fixed_total = _total_for_scope(
        budget_rows,
        "fixed_slot_radii",
        "stable_total_coordinate_radius_points_fine",
    )
    permutation_total = _total_for_scope(
        budget_rows,
        "known_radius_permutations",
        "stable_total_coordinate_radius_points_fine",
    )
    independent_total = _total_for_scope(
        budget_rows,
        "independent_known_radius_choices",
        "stable_total_coordinate_radius_points_fine",
    )
    fixed_coarse_total = _total_for_scope(
        budget_rows,
        "fixed_slot_radii",
        "stable_total_coordinate_radius_points_coarse",
    )
    return {
        "policy_label": "local_2d_detector_controlled_prior_refinement_budget_cpu_no_fwi",
        "source_xz_contract_policy_label": xz_summary.get("policy_label", ""),
        "source_prior_scope_policy_label": prior_summary.get("policy_label", ""),
        "branch_count": len(branch_rows),
        "source_case_count": len(prior_case_rows),
        "stable_controlled_prior_case_count": len(stable_prior),
        "review_case_excluded_count": len(review_rows),
        "radius_pattern_mm": format_radius_pattern(radius_values_mm),
        "radius_value_count": len(radius_values_mm),
        "component_count": DEFAULT_COMPONENT_COUNT,
        "fixed_slot_radius_combination_count": 1,
        "known_radius_permutation_count": next(
            row["radius_combination_count"]
            for row in radius_rows
            if row["radius_scope_key"] == "known_radius_permutations"
        ),
        "independent_known_radius_choice_count": next(
            row["radius_combination_count"]
            for row in radius_rows
            if row["radius_scope_key"] == "independent_known_radius_choices"
        ),
        "fixed_slot_radii_stable_total_points_fine": fixed_total,
        "fixed_slot_radii_stable_total_points_coarse": fixed_coarse_total,
        "known_radius_permutations_stable_total_points_fine": permutation_total,
        "independent_known_radius_choices_stable_total_points_fine": independent_total,
        "permutation_vs_fixed_multiplier": (
            permutation_total / fixed_total if fixed_total > 0 else math.nan
        ),
        "independent_vs_fixed_multiplier": (
            independent_total / fixed_total if fixed_total > 0 else math.nan
        ),
        "ready_for_controlled_fixed_radius_budget": boolish(
            prior_summary.get("ready_for_controlled_synthetic_prior_contract", False)
        )
        and boolish(xz_summary.get("ready_for_branch_specific_xz_seed_neighborhood_contract", False)),
        "ready_for_known_radius_permutation_budget": True,
        "ready_for_independent_radius_search": False,
        "ready_for_review_case_inclusion": False,
        "ready_for_field_transfer": False,
        "ready_for_refinement_launch": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_gpu_work": False,
        "gpu_priority": "none",
        "decision": (
            "A controlled fixed-radius synthetic refinement budget is now scoped, "
            "but only as a design artifact: fixed slot radii keep the stable-case "
            "fine x/z grid at the run 088 total, while radius permutations multiply "
            "that cost by 6 and independent per-slot known-radius choices multiply it "
            "by 27. Do not launch refinement, FWI, GPU work, field transfer, or "
            "detector-inferred radius claims from this audit."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "controlled_fixed_radius_budget",
            "ready": summary["ready_for_controlled_fixed_radius_budget"],
            "allowed_use": "synthetic fixed-radius refinement budget design",
            "blocked_use": "blind detector-inferred radius/material claim",
            "evidence": (
                f"stable cases={summary['stable_controlled_prior_case_count']}; "
                f"fine points={summary['fixed_slot_radii_stable_total_points_fine']}"
            ),
        },
        {
            "gate_key": "known_radius_permutation_budget",
            "ready": summary["ready_for_known_radius_permutation_budget"],
            "allowed_use": "cost comparison only",
            "blocked_use": "launch without objective/runtime contract",
            "evidence": (
                f"combos={summary['known_radius_permutation_count']}; "
                f"multiplier={summary['permutation_vs_fixed_multiplier']:.1f}"
            ),
        },
        {
            "gate_key": "independent_radius_search",
            "ready": summary["ready_for_independent_radius_search"],
            "allowed_use": "none",
            "blocked_use": "naive independent radius tensor search",
            "evidence": (
                f"combos={summary['independent_known_radius_choice_count']}; "
                f"fine points={summary['independent_known_radius_choices_stable_total_points_fine']}"
            ),
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "FWI/GPU launch",
            "evidence": "budget audit is not a launch contract",
        },
    ]


def plot_budget(summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8), constrained_layout=True)

    scopes = ["fixed", "permuted", "independent"]
    fine_totals = [
        summary["fixed_slot_radii_stable_total_points_fine"],
        summary["known_radius_permutations_stable_total_points_fine"],
        summary["independent_known_radius_choices_stable_total_points_fine"],
    ]
    axes[0].bar(scopes, fine_totals, color=["#59a14f", "#f28e2b", "#e15759"])
    axes[0].set_yscale("log")
    axes[0].set_ylabel("stable fine-grid points, log scale")
    axes[0].set_title("Radius-scope cost")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["fixed\nbudget", "permutation\nbudget", "independent\nsearch", "FWI/GPU"]
    gate_values = [
        summary["ready_for_controlled_fixed_radius_budget"],
        summary["ready_for_known_radius_permutation_budget"],
        summary["ready_for_independent_radius_search"],
        summary["ready_for_detector_seeded_fwi"],
    ]
    axes[1].bar(
        gate_labels,
        [1 if value else 0 for value in gate_values],
        color=["#59a14f" if value else "#bab0ac" for value in gate_values],
    )
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_ylim(0, 1.15)
    axes[1].set_title("Decision gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.04,
        0.08,
        f"radii={summary['radius_pattern_mm']} mm\n"
        f"perm x{summary['permutation_vs_fixed_multiplier']:.1f}\n"
        f"independent x{summary['independent_vs_fixed_multiplier']:.1f}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("Local 2D controlled-prior refinement budget", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_controlled_prior_refinement_budget.png`",
                "",
                "This CPU-only figure budgets detector handoff scopes after the x/z",
                "neighborhood and controlled radius/material prior audits.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Radius pattern: `{summary['radius_pattern_mm']}` mm.",
                f"Fixed-radius fine stable points: `{summary['fixed_slot_radii_stable_total_points_fine']}`.",
                f"Known-radius permutation multiplier: `{summary['permutation_vs_fixed_multiplier']:.1f}`.",
                f"Independent known-radius multiplier: `{summary['independent_vs_fixed_multiplier']:.1f}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "Fixed slot radii are controlled synthetic priors, not detector-inferred",
                "radius/material estimates. This audit does not run refinement, FWI,",
                "GPU kernels, 3D/HPC jobs, field transfer, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xz-contract-run", default=DEFAULT_XZ_CONTRACT_RUN)
    parser.add_argument("--prior-scope-run", default=DEFAULT_PRIOR_SCOPE_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_controlled_prior_refinement_budget")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path("outputs/summary_tables")
    xz_dir = root / args.xz_contract_run
    prior_dir = root / args.prior_scope_run

    xz_branches = read_csv_rows(xz_dir / "data/local_2d_detector_xz_seed_neighborhood_contract_branches.csv")
    xz_summary = read_json(xz_dir / "data/local_2d_detector_xz_seed_neighborhood_contract_summary.json")
    prior_cases = read_csv_rows(prior_dir / "data/local_2d_detector_radius_material_prior_scope_cases.csv")
    prior_summary = read_json(prior_dir / "data/local_2d_detector_radius_material_prior_scope_summary.json")

    radius_values = _source_radius_pattern(prior_cases)
    radius_rows_out = radius_scope_rows(radius_values, DEFAULT_COMPONENT_COUNT)
    budget = build_budget_rows(xz_branches, radius_rows_out)
    summary = summarize_budget(
        xz_branches,
        prior_cases,
        radius_rows_out,
        budget,
        xz_summary,
        prior_summary,
        radius_values,
    )
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    radius_csv = data_dir / "local_2d_detector_controlled_prior_radius_scopes.csv"
    budget_csv = data_dir / "local_2d_detector_controlled_prior_refinement_budget_rows.csv"
    gates_csv = data_dir / "local_2d_detector_controlled_prior_refinement_budget_gates.csv"
    summary_json = data_dir / "local_2d_detector_controlled_prior_refinement_budget_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_controlled_prior_refinement_budget.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(radius_csv, [json_safe(row) for row in radius_rows_out])
    write_csv(budget_csv, [json_safe(row) for row in budget])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_budget(summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "paths": {
            "radius_scopes_csv": str(radius_csv),
            "budget_rows_csv": str(budget_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "source_xz_contract_summary_json": str(
                xz_dir / "data/local_2d_detector_xz_seed_neighborhood_contract_summary.json"
            ),
            "source_prior_scope_summary_json": str(
                prior_dir / "data/local_2d_detector_radius_material_prior_scope_summary.json"
            ),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_controlled_prior_refinement_budget",
        {
            "summary_json": str(summary_json),
            "radius_scopes_csv": str(radius_csv),
            "budget_rows_csv": str(budget_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
