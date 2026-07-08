#!/usr/bin/env python3
"""Build a branch-specific x/z detector seed-neighborhood contract without FWI."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SEED_GEOMETRY_AUDIT_RUN = "086_local_2d_detector_seed_geometry_error_audit"
DEFAULT_COMPONENT_SEED_EXPORT_RUN = "081_local_2d_detector_component_seed_export"
DEFAULT_STEP_MM = 2.0
DEFAULT_COARSE_STEP_MM = 5.0
DEFAULT_COMPONENT_COUNT = 3


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def coordinate_grid_points(half_width_mm: float, step_mm: float, component_count: int) -> int:
    values_per_axis = int(math.floor((2.0 * float(half_width_mm)) / float(step_mm))) + 1
    return values_per_axis ** (2 * int(component_count))


def branch_contract_rows(
    branch_rows: list[dict],
    *,
    step_mm: float = DEFAULT_STEP_MM,
    coarse_step_mm: float = DEFAULT_COARSE_STEP_MM,
    component_count: int = DEFAULT_COMPONENT_COUNT,
) -> list[dict]:
    branch_names = sorted({str(row.get("branch_key", "")) for row in branch_rows if row.get("branch_key")})
    outputs: list[dict] = []
    for branch in branch_names:
        candidates = [
            row
            for row in branch_rows
            if row.get("branch_key") == branch
            and safe_float(row.get("stable_seed_case_count"), 0.0) > 0
            and safe_float(row.get("stable_seed_xz_coverage_fraction"), 0.0) >= 1.0
        ]
        if not candidates:
            continue
        best = min(candidates, key=lambda row: safe_float(row.get("half_width_mm"), math.inf))
        half_width = safe_float(best.get("half_width_mm"))
        stable_count = safe_int(best.get("stable_seed_case_count"), 0)
        review_count = safe_int(best.get("review_case_count"), 0)
        fine_points = coordinate_grid_points(half_width, step_mm, component_count)
        coarse_points = coordinate_grid_points(half_width, coarse_step_mm, component_count)
        outputs.append(
            {
                "branch_key": branch,
                "recommended_half_width_mm": half_width,
                "fine_step_mm": step_mm,
                "coarse_step_mm": coarse_step_mm,
                "stable_seed_case_count": stable_count,
                "review_case_count": review_count,
                "stable_seed_xz_coverage_fraction": safe_float(best.get("stable_seed_xz_coverage_fraction")),
                "review_case_xz_covered_count_at_half_width": safe_int(
                    best.get("review_case_xz_covered_count"),
                    0,
                ),
                "per_case_xz_grid_points_fine": fine_points,
                "stable_total_xz_grid_points_fine": stable_count * fine_points,
                "per_case_xz_grid_points_coarse": coarse_points,
                "stable_total_xz_grid_points_coarse": stable_count * coarse_points,
                "ready_for_branch_xz_seed_neighborhood_contract": True,
                "ready_for_review_case_inclusion": False,
                "ready_for_radius_material_contract": False,
                "ready_for_narrow_refinement_launch": False,
                "ready_for_detector_seeded_fwi": False,
                "allowed_use": "branch-specific x/z coordinate seed-neighborhood sizing for stable saved cases",
                "blocked_use": "review-case inclusion, radius/material tensor refinement, detector-seeded FWI",
            }
        )
    return outputs


def contract_case_rows(case_rows: list[dict], branch_rows_out: list[dict]) -> list[dict]:
    branch_half_width = {
        row["branch_key"]: safe_float(row.get("recommended_half_width_mm"))
        for row in branch_rows_out
    }
    rows: list[dict] = []
    for row in case_rows:
        stable = boolish(row.get("candidate_component_seed_ready"))
        review = boolish(row.get("review_assignment"))
        branch = str(row.get("branch_key", ""))
        half_width = branch_half_width.get(branch, math.nan)
        linf_error = safe_float(row.get("matched_max_linf_error_mm"), math.nan)
        covered = stable and math.isfinite(half_width) and linf_error <= half_width
        rows.append(
            {
                "case_label": row.get("case_label", ""),
                "branch_key": branch,
                "seed": safe_int(row.get("seed"), 0),
                "case_variant": row.get("case_variant", ""),
                "case_contract_status": "stable_in_contract" if stable else "excluded_review_case",
                "review_assignment": review,
                "recommended_branch_half_width_mm": half_width if stable else math.nan,
                "matched_max_x_error_mm": safe_float(row.get("matched_max_x_error_mm")),
                "matched_max_z_error_mm": safe_float(row.get("matched_max_z_error_mm")),
                "matched_max_linf_error_mm": linf_error,
                "covered_by_branch_contract": covered,
                "ready_for_coordinate_neighborhood_contract": covered,
                "ready_for_review_case_inclusion": False,
                "ready_for_detector_seeded_fwi": False,
                "allowed_use": "stable-case x/z seed-neighborhood handoff design" if stable else "review blocker context",
                "blocked_use": "radius/material seeding, review-case promotion, detector-seeded FWI",
            }
        )
    return sorted(rows, key=lambda item: (item["branch_key"], item["seed"], item["case_variant"]))


def summarize_contract(
    branch_rows_out: list[dict],
    case_rows_out: list[dict],
    source_summary: dict,
    seed_export_summary: dict,
    *,
    step_mm: float = DEFAULT_STEP_MM,
    component_count: int = DEFAULT_COMPONENT_COUNT,
) -> dict:
    stable_cases = [row for row in case_rows_out if row["case_contract_status"] == "stable_in_contract"]
    review_cases = [row for row in case_rows_out if row["case_contract_status"] == "excluded_review_case"]
    global_half_width = max(safe_float(row.get("recommended_half_width_mm"), 0.0) for row in branch_rows_out)
    global_per_case_points = coordinate_grid_points(global_half_width, step_mm, component_count)
    global_stable_points = global_per_case_points * len(stable_cases)
    branch_half_width = {
        row["branch_key"]: safe_float(row.get("recommended_half_width_mm"))
        for row in branch_rows_out
    }
    branch_coarse_step = {
        row["branch_key"]: safe_float(row.get("coarse_step_mm"), DEFAULT_COARSE_STEP_MM)
        for row in branch_rows_out
    }
    branch_stable_points = sum(
        coordinate_grid_points(branch_half_width[row["branch_key"]], step_mm, component_count)
        for row in stable_cases
    )
    branch_coarse_points = sum(
        coordinate_grid_points(
            branch_half_width[row["branch_key"]],
            branch_coarse_step[row["branch_key"]],
            component_count,
        )
        for row in stable_cases
    )
    saved_points = global_stable_points - branch_stable_points
    reduction_fraction = saved_points / global_stable_points if global_stable_points else 0.0
    all_stable_covered = all(boolish(row.get("covered_by_branch_contract")) for row in stable_cases)
    return {
        "policy_label": "local_2d_detector_xz_seed_neighborhood_contract_cpu_no_fwi",
        "source_seed_geometry_policy_label": source_summary.get("policy_label", ""),
        "source_seed_export_policy_label": seed_export_summary.get("policy_label", ""),
        "branch_contract_count": len(branch_rows_out),
        "stable_contract_case_count": len(stable_cases),
        "review_case_excluded_count": len(review_cases),
        "global_half_width_mm": global_half_width,
        "branch_half_widths_mm": ";".join(
            f"{row['branch_key']}:{safe_float(row.get('recommended_half_width_mm')):g}"
            for row in branch_rows_out
        ),
        "fine_step_mm": step_mm,
        "component_count": component_count,
        "global_per_case_xz_grid_points_fine": global_per_case_points,
        "global_stable_total_xz_grid_points_fine": global_stable_points,
        "branch_specific_stable_total_xz_grid_points_fine": branch_stable_points,
        "branch_specific_stable_total_xz_grid_points_coarse": branch_coarse_points,
        "branch_specific_saved_xz_grid_points_fine": saved_points,
        "branch_specific_grid_reduction_fraction_fine": reduction_fraction,
        "all_stable_cases_covered_by_branch_contract": all_stable_covered,
        "ready_for_branch_specific_xz_seed_neighborhood_contract": all_stable_covered and bool(branch_rows_out),
        "ready_for_review_case_inclusion": False,
        "ready_for_radius_material_contract": False,
        "ready_for_narrow_refinement_launch": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_gpu_work": False,
        "gpu_priority": "none",
        "active_blocker_keys": seed_export_summary.get("active_blocker_keys", ""),
        "decision": (
            "Use branch-specific x/z coordinate neighborhoods for stable saved detector cases only: "
            "target2_close14 needs 10 mm and target2_close50_linear29p5 needs 12 mm at the current "
            "matched x/z L-infinity sizing. This reduces the hypothetical fine coordinate grid versus "
            "a global 12 mm half-width, but radius/material seeds, review-case closure, branch-transfer "
            "validation, and detector-seeded FWI launch contracts remain blocked."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "branch_specific_xz_seed_neighborhood_contract",
            "ready": summary["ready_for_branch_specific_xz_seed_neighborhood_contract"],
            "allowed_use": "stable saved-case coordinate-neighborhood sizing",
            "blocked_use": "none within sizing-only scope",
            "evidence": (
                f"{summary['stable_contract_case_count']} stable cases covered; "
                f"branch half-widths={summary['branch_half_widths_mm']}"
            ),
        },
        {
            "gate_key": "review_case_inclusion",
            "ready": summary["ready_for_review_case_inclusion"],
            "allowed_use": "none",
            "blocked_use": "include close50 nominal review cases in a launch contract",
            "evidence": f"excluded review cases={summary['review_case_excluded_count']}",
        },
        {
            "gate_key": "radius_material_contract",
            "ready": summary["ready_for_radius_material_contract"],
            "allowed_use": "none",
            "blocked_use": "radius/material tensor refinement",
            "evidence": "source seed export reports radius/material blockers",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "GPU/FWI launch",
            "evidence": "coordinate-only contract is not a full refinement/FWI launch contract",
        },
    ]


def plot_contract(branch_rows_out: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["branch_key"].replace("_", "\n") for row in branch_rows_out]
    half_widths = [safe_float(row.get("recommended_half_width_mm")) for row in branch_rows_out]
    totals = [safe_float(row.get("stable_total_xz_grid_points_fine")) / 1e6 for row in branch_rows_out]

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8), constrained_layout=True)
    axes[0].bar(labels, half_widths, color=["#4c78a8", "#f58518"][: len(labels)])
    axes[0].set_ylabel("x/z L-inf half-width (mm)")
    axes[0].set_title("Branch-specific stable-case coverage")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(labels, totals, color=["#54a24b", "#b279a2"][: len(labels)])
    axes[1].axhline(
        safe_float(summary.get("global_stable_total_xz_grid_points_fine")) / 1e6,
        color="#6b6b6b",
        linestyle="--",
        linewidth=1.2,
        label="global h12 total",
    )
    axes[1].set_ylabel("stable fine-grid points (millions)")
    axes[1].set_title("Fine-grid budget at 2 mm")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(loc="upper left", fontsize=8)
    axes[1].text(
        0.98,
        0.95,
        f"saved={summary['branch_specific_saved_xz_grid_points_fine'] / 1e6:.2f}M\n"
        f"review excluded={summary['review_case_excluded_count']}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector x/z seed-neighborhood contract", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_xz_seed_neighborhood_contract.png`",
                "",
                "This CPU-only figure summarizes the branch-specific x/z seed-neighborhood",
                "contract derived from saved detector seed artifacts.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Stable contract cases: `{summary['stable_contract_case_count']}`.",
                f"Review cases excluded: `{summary['review_case_excluded_count']}`.",
                f"Branch half-widths: `{summary['branch_half_widths_mm']}`.",
                f"Fine-grid reduction fraction: `{summary['branch_specific_grid_reduction_fraction_fine']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "This contract sizes coordinate-only x/z neighborhoods for saved stable detector",
                "cases. It does not run refinement, FWI, GPU kernels, 3D/HPC jobs, or neural",
                "network training, and it does not provide radius/material seeds.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-geometry-audit-run", default=DEFAULT_SEED_GEOMETRY_AUDIT_RUN)
    parser.add_argument("--component-seed-export-run", default=DEFAULT_COMPONENT_SEED_EXPORT_RUN)
    parser.add_argument("--step-mm", type=float, default=DEFAULT_STEP_MM)
    parser.add_argument("--coarse-step-mm", type=float, default=DEFAULT_COARSE_STEP_MM)
    parser.add_argument("--run-name", default="local_2d_detector_xz_seed_neighborhood_contract")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    seed_dir = Path("outputs/summary_tables") / args.seed_geometry_audit_run
    export_dir = Path("outputs/summary_tables") / args.component_seed_export_run
    source_summary = read_json(seed_dir / "data/local_2d_detector_seed_geometry_error_audit_summary.json")
    seed_export_summary = read_json(export_dir / "data/local_2d_detector_component_seed_export_summary.json")
    source_case_rows = read_csv_rows(seed_dir / "data/local_2d_detector_seed_geometry_error_cases.csv")
    source_branch_rows = read_csv_rows(seed_dir / "data/local_2d_detector_seed_geometry_error_branch_rows.csv")

    branch_rows_out = branch_contract_rows(
        source_branch_rows,
        step_mm=args.step_mm,
        coarse_step_mm=args.coarse_step_mm,
    )
    case_rows_out = contract_case_rows(source_case_rows, branch_rows_out)
    summary = summarize_contract(
        branch_rows_out,
        case_rows_out,
        source_summary,
        seed_export_summary,
        step_mm=args.step_mm,
    )
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    branch_csv = data_dir / "local_2d_detector_xz_seed_neighborhood_contract_branches.csv"
    cases_csv = data_dir / "local_2d_detector_xz_seed_neighborhood_contract_cases.csv"
    gates_csv = data_dir / "local_2d_detector_xz_seed_neighborhood_contract_gates.csv"
    summary_json = data_dir / "local_2d_detector_xz_seed_neighborhood_contract_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_xz_seed_neighborhood_contract.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(branch_csv, [json_safe(row) for row in branch_rows_out])
    write_csv(cases_csv, [json_safe(row) for row in case_rows_out])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_contract(branch_rows_out, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "paths": {
            "branch_rows_csv": str(branch_csv),
            "case_rows_csv": str(cases_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "source_seed_geometry_summary_json": str(
                seed_dir / "data/local_2d_detector_seed_geometry_error_audit_summary.json"
            ),
            "source_component_seed_export_summary_json": str(
                export_dir / "data/local_2d_detector_component_seed_export_summary.json"
            ),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_xz_seed_neighborhood_contract",
        {
            "summary_json": str(summary_json),
            "branch_rows_csv": str(branch_csv),
            "case_rows_csv": str(cases_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
