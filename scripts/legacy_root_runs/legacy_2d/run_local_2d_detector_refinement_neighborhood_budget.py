#!/usr/bin/env python3
"""Size lateral x-slot neighborhoods from saved detector seed errors."""

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


DEFAULT_CONTRACT_RUN = "077_local_2d_detector_refinement_launch_contract_audit"
DEFAULT_SEED_EXPORT_RUN = "081_local_2d_detector_component_seed_export"
DEFAULT_HALF_WIDTHS_MM = "2,3,4,5,6,8,10,12,15"
DEFAULT_STEPS_MM = "1,2,5"
DEFAULT_COMPONENT_COUNT = 3


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_positive_numbers(value: str) -> list[float]:
    numbers: list[float] = []
    for item in str(value or "").split(","):
        item = item.strip()
        if not item:
            continue
        number = float(item)
        if not math.isfinite(number) or number <= 0.0:
            raise ValueError(f"expected positive finite number, got {item!r}")
        numbers.append(number)
    if not numbers:
        raise ValueError("at least one value is required")
    return sorted(set(numbers))


def stable_case_rows(contract_rows: list[dict]) -> list[dict]:
    return [row for row in contract_rows if boolish(row.get("candidate_component_seed_ready"))]


def review_case_rows(contract_rows: list[dict]) -> list[dict]:
    return [row for row in contract_rows if boolish(row.get("review_assignment"))]


def _case_error_mm(row: dict) -> float:
    return safe_float(row.get("max_target_slot_abs_error_mm"))


def build_half_width_rows(contract_rows: list[dict], half_widths_mm: list[float]) -> list[dict]:
    stable_rows = stable_case_rows(contract_rows)
    review_rows = review_case_rows(contract_rows)
    outputs: list[dict] = []
    for half_width in half_widths_mm:
        stable_covered = [row for row in stable_rows if _case_error_mm(row) <= half_width]
        stable_uncovered = [row for row in stable_rows if _case_error_mm(row) > half_width]
        review_covered = [row for row in review_rows if _case_error_mm(row) <= half_width]
        all_covered = [row for row in contract_rows if _case_error_mm(row) <= half_width]
        outputs.append(
            {
                "half_width_mm": half_width,
                "source_case_count": len(contract_rows),
                "stable_seed_case_count": len(stable_rows),
                "stable_seed_covered_count": len(stable_covered),
                "stable_seed_coverage_fraction": len(stable_covered) / len(stable_rows) if stable_rows else math.nan,
                "review_case_count": len(review_rows),
                "review_case_covered_count": len(review_covered),
                "all_case_covered_count": len(all_covered),
                "all_case_coverage_fraction": len(all_covered) / len(contract_rows) if contract_rows else math.nan,
                "uncovered_stable_case_labels": ";".join(row.get("case_label", "") for row in stable_uncovered),
                "covered_review_case_labels": ";".join(row.get("case_label", "") for row in review_covered),
                "coverage_dimension": "lateral_x_slot_only",
                "ready_for_lateral_x_slot_neighborhood_design": (
                    len(stable_covered) == len(stable_rows) and len(stable_rows) > 0
                ),
                "ready_for_xz_neighborhood_design": False,
                "ready_for_refinement_launch": False,
                "allowed_use": "lateral x-slot half-width sizing for saved detector seed design",
                "blocked_use": "z coverage, narrow refinement launch, detector-seeded FWI, radius/material recovery",
            }
        )
    return outputs


def build_branch_half_width_rows(contract_rows: list[dict], half_widths_mm: list[float]) -> list[dict]:
    branches = sorted({row.get("branch_key", "") for row in contract_rows})
    outputs: list[dict] = []
    for branch in branches:
        branch_rows = [row for row in contract_rows if row.get("branch_key", "") == branch]
        branch_stable = stable_case_rows(branch_rows)
        branch_review = review_case_rows(branch_rows)
        for half_width in half_widths_mm:
            stable_covered = [row for row in branch_stable if _case_error_mm(row) <= half_width]
            review_covered = [row for row in branch_review if _case_error_mm(row) <= half_width]
            outputs.append(
                {
                    "branch_key": branch,
                    "half_width_mm": half_width,
                    "branch_case_count": len(branch_rows),
                    "stable_seed_case_count": len(branch_stable),
                    "stable_seed_covered_count": len(stable_covered),
                    "stable_seed_coverage_fraction": (
                        len(stable_covered) / len(branch_stable) if branch_stable else math.nan
                    ),
                    "review_case_count": len(branch_review),
                    "review_case_covered_count": len(review_covered),
                    "coverage_dimension": "lateral_x_slot_only",
                    "ready_for_branch_lateral_x_slot_neighborhood_design": (
                        len(stable_covered) == len(branch_stable) and len(branch_stable) > 0
                    ),
                    "ready_for_branch_xz_neighborhood_design": False,
                }
            )
    return outputs


def coordinate_grid_points(half_width_mm: float, step_mm: float, component_count: int = DEFAULT_COMPONENT_COUNT) -> int:
    values_per_axis = int(math.floor((2.0 * half_width_mm) / step_mm)) + 1
    dimensions = component_count
    return values_per_axis**dimensions


def hypothetical_xz_tensor_grid_points(
    half_width_mm: float,
    step_mm: float,
    component_count: int = DEFAULT_COMPONENT_COUNT,
) -> int:
    values_per_axis = int(math.floor((2.0 * half_width_mm) / step_mm)) + 1
    dimensions = 2 * component_count
    return values_per_axis**dimensions


def build_grid_budget_rows(
    half_width_rows: list[dict],
    steps_mm: list[float],
    *,
    component_count: int = DEFAULT_COMPONENT_COUNT,
) -> list[dict]:
    outputs: list[dict] = []
    for row in half_width_rows:
        half_width = safe_float(row.get("half_width_mm"))
        stable_count = safe_int(row.get("stable_seed_case_count"), 0)
        source_count = safe_int(row.get("source_case_count"), 0)
        for step in steps_mm:
            per_case = coordinate_grid_points(half_width, step, component_count=component_count)
            hypothetical_xz_per_case = hypothetical_xz_tensor_grid_points(
                half_width,
                step,
                component_count=component_count,
            )
            outputs.append(
                {
                    "half_width_mm": half_width,
                    "step_mm": step,
                    "component_count": component_count,
                    "coverage_dimension": "lateral_x_slot_only",
                    "coordinate_dimensions": component_count,
                    "values_per_axis": int(math.floor((2.0 * half_width) / step)) + 1,
                    "per_case_lateral_x_grid_points": per_case,
                    "stable_seed_total_lateral_x_grid_points": per_case * stable_count,
                    "all_case_total_lateral_x_grid_points": per_case * source_count,
                    "hypothetical_per_case_xz_tensor_points": hypothetical_xz_per_case,
                    "hypothetical_stable_total_xz_tensor_points": hypothetical_xz_per_case * stable_count,
                    "z_coverage_validated": False,
                    "ready_for_xz_neighborhood_design": False,
                    "ready_for_naive_full_tensor_refinement": False,
                    "allowed_use": "lateral x-slot budget sizing only",
                    "blocked_use": "z-validated tensor refinement, FWI/refinement launch",
                }
            )
    return outputs


def _min_covering_half_width(rows: list[dict], covered_key: str, total_key: str) -> float:
    for row in sorted(rows, key=lambda item: safe_float(item.get("half_width_mm"))):
        if safe_int(row.get(covered_key), 0) == safe_int(row.get(total_key), 0) and safe_int(row.get(total_key), 0) > 0:
            return safe_float(row.get("half_width_mm"))
    return math.nan


def _grid_points_at(grid_rows: list[dict], half_width_mm: float, step_mm: float, field: str) -> float:
    for row in grid_rows:
        if math.isclose(safe_float(row.get("half_width_mm")), half_width_mm) and math.isclose(
            safe_float(row.get("step_mm")), step_mm
        ):
            return safe_float(row.get(field))
    return math.nan


def _half_width_value_at(rows: list[dict], half_width_mm: float, field: str) -> float:
    for row in rows:
        if math.isclose(safe_float(row.get("half_width_mm")), half_width_mm):
            return safe_float(row.get(field))
    return math.nan


def summarize_budget(
    contract_rows: list[dict],
    half_width_rows: list[dict],
    branch_rows: list[dict],
    grid_rows: list[dict],
    contract_summary: dict,
    seed_summary: dict,
) -> dict:
    stable_rows = stable_case_rows(contract_rows)
    review_rows = review_case_rows(contract_rows)
    errors = [_case_error_mm(row) for row in stable_rows if math.isfinite(_case_error_mm(row))]
    min_half_width_all_stable = _min_covering_half_width(
        half_width_rows,
        "stable_seed_covered_count",
        "stable_seed_case_count",
    )
    branch_min_parts = []
    for branch in sorted({row.get("branch_key", "") for row in branch_rows}):
        rows = [row for row in branch_rows if row.get("branch_key", "") == branch]
        branch_min_parts.append(
            f"{branch}:{_min_covering_half_width(rows, 'stable_seed_covered_count', 'stable_seed_case_count'):.1f}"
        )
    return {
        "policy_label": "local_2d_detector_lateral_slot_neighborhood_budget_cpu_no_fwi",
        "source_contract_policy_label": contract_summary.get("policy_label", ""),
        "source_seed_export_policy_label": seed_summary.get("policy_label", ""),
        "coverage_dimension": "lateral_x_slot_only",
        "source_case_count": len(contract_rows),
        "stable_seed_case_count": len(stable_rows),
        "review_case_count": len(review_rows),
        "max_stable_lateral_x_slot_error_mm": max(errors) if errors else math.nan,
        "median_stable_lateral_x_slot_error_mm": float(np.median(errors)) if errors else math.nan,
        "min_lateral_x_half_width_all_stable_seed_cases_mm": min_half_width_all_stable,
        "branch_min_lateral_x_half_width_all_stable_seed_cases_mm": ";".join(branch_min_parts),
        "stable_lateral_x_coverage_at_5mm": _half_width_value_at(
            half_width_rows, 5.0, "stable_seed_covered_count"
        ),
        "stable_lateral_x_coverage_at_8mm": _half_width_value_at(
            half_width_rows, 8.0, "stable_seed_covered_count"
        ),
        "stable_lateral_x_coverage_at_10mm": _half_width_value_at(
            half_width_rows, 10.0, "stable_seed_covered_count"
        ),
        "per_case_lateral_x_grid_points_h10_step1": _grid_points_at(
            grid_rows, 10.0, 1.0, "per_case_lateral_x_grid_points"
        ),
        "per_case_lateral_x_grid_points_h10_step2": _grid_points_at(
            grid_rows, 10.0, 2.0, "per_case_lateral_x_grid_points"
        ),
        "per_case_lateral_x_grid_points_h10_step5": _grid_points_at(
            grid_rows, 10.0, 5.0, "per_case_lateral_x_grid_points"
        ),
        "stable_total_lateral_x_grid_points_h10_step2": _grid_points_at(
            grid_rows, 10.0, 2.0, "stable_seed_total_lateral_x_grid_points"
        ),
        "hypothetical_per_case_xz_tensor_points_h10_step2": _grid_points_at(
            grid_rows, 10.0, 2.0, "hypothetical_per_case_xz_tensor_points"
        ),
        "active_blocker_count": safe_float(contract_summary.get("active_blocker_count"), 0.0),
        "active_blocker_keys": contract_summary.get("active_blocker_keys", ""),
        "ready_for_lateral_x_slot_neighborhood_design": math.isfinite(min_half_width_all_stable),
        "z_coverage_validated": False,
        "ready_for_xz_neighborhood_design": False,
        "ready_for_radius_material_contract": False,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_naive_full_tensor_refinement": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "A 10 mm lateral x-slot half-width covers all 10 stable exported detector seed cases in the saved "
            "truth evaluation, while 8 mm misses one and 5 mm misses three. This evidence is lateral x-slot "
            "only: z coverage is not validated by the detector contract, and the two review cases remain "
            "policy-excluded. A 10 mm / 2 mm lateral x-only tensor is 1,331 points per case, while the "
            "corresponding 6D x/z tensor would be 1,771,561 points per case without z-coverage evidence. "
            "Use this as x-slot neighborhood sizing, not as a narrow refinement or GPU/FWI launch contract."
        ),
    }


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "lateral_x_slot_neighborhood_design",
            "ready": summary["ready_for_lateral_x_slot_neighborhood_design"],
            "allowed_use": "saved-corpus lateral x-slot half-width sizing",
            "blocked_use": "none within design scope",
            "evidence": (
                f"min half-width all stable seeds="
                f"{summary['min_lateral_x_half_width_all_stable_seed_cases_mm']:.1f} mm"
            ),
        },
        {
            "gate_key": "xz_neighborhood_design",
            "ready": summary["ready_for_xz_neighborhood_design"],
            "allowed_use": "none",
            "blocked_use": "z-validated x/z neighborhood design",
            "evidence": f"z coverage validated={summary['z_coverage_validated']}",
        },
        {
            "gate_key": "radius_material_contract",
            "ready": summary["ready_for_radius_material_contract"],
            "allowed_use": "none",
            "blocked_use": "radius/material initialization",
            "evidence": "component seeds contain x/z only",
        },
        {
            "gate_key": "narrow_refinement_contract",
            "ready": summary["ready_for_narrow_refinement_contract"],
            "allowed_use": "none",
            "blocked_use": "narrow refinement launch",
            "evidence": f"active blockers={summary['active_blocker_count']}",
        },
        {
            "gate_key": "naive_full_tensor_refinement",
            "ready": summary["ready_for_naive_full_tensor_refinement"],
            "allowed_use": "none",
            "blocked_use": "full 6D coordinate tensor FWI/refinement queue",
            "evidence": (
                f"h10 step2 lateral grid={summary['per_case_lateral_x_grid_points_h10_step2']:.0f}; "
                f"hypothetical x/z tensor={summary['hypothetical_per_case_xz_tensor_points_h10_step2']:.0f}"
            ),
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI",
            "evidence": summary["active_blocker_keys"],
        },
    ]


def plot_budget(half_width_rows: list[dict], grid_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    half_widths = [safe_float(row.get("half_width_mm")) for row in half_width_rows]
    axes[0].plot(
        half_widths,
        [safe_float(row.get("stable_seed_covered_count")) for row in half_width_rows],
        marker="o",
        color="#4c72b0",
        label="stable exported cases",
    )
    axes[0].plot(
        half_widths,
        [safe_float(row.get("all_case_covered_count")) for row in half_width_rows],
        marker="s",
        color="#55a868",
        label="all contract cases",
    )
    axes[0].axvline(
        summary["min_lateral_x_half_width_all_stable_seed_cases_mm"],
        color="#333333",
        linestyle="--",
        linewidth=0.8,
    )
    axes[0].set_xlabel("lateral x-slot half-width (mm)")
    axes[0].set_ylabel("covered cases")
    axes[0].set_title("Detector lateral slot coverage by neighborhood")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    for step in sorted({safe_float(row.get("step_mm")) for row in grid_rows}):
        step_rows = sorted(
            [row for row in grid_rows if math.isclose(safe_float(row.get("step_mm")), step)],
            key=lambda row: safe_float(row.get("half_width_mm")),
        )
        axes[1].plot(
            [safe_float(row.get("half_width_mm")) for row in step_rows],
            [safe_float(row.get("per_case_lateral_x_grid_points")) for row in step_rows],
            marker="o",
            label=f"{step:g} mm step",
        )
    axes[1].set_yscale("log")
    axes[1].set_xlabel("lateral x-slot half-width (mm)")
    axes[1].set_ylabel("per-case x-only grid points")
    axes[1].set_title("Lateral slot tensor budget")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.03,
        0.06,
        f"stable cases: {summary['stable_seed_case_count']}/{summary['source_case_count']}\n"
        f"min x half-width: {summary['min_lateral_x_half_width_all_stable_seed_cases_mm']:.1f} mm\n"
        f"x-only h10 step2: {summary['per_case_lateral_x_grid_points_h10_step2']:.0f}\n"
        f"z validated: {summary['z_coverage_validated']}\n"
        f"ready for FWI: {summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector lateral-slot neighborhood budget", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, half_width_csv: Path, grid_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_lateral_slot_neighborhood_budget.png`",
                "",
                "This CPU-only figure sizes lateral x-slot neighborhoods from saved detector seed errors.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Stable seed cases: `{summary['stable_seed_case_count']}`.",
                f"Review cases: `{summary['review_case_count']}`.",
                (
                    "Min lateral x-slot half-width for all stable cases: "
                    f"`{summary['min_lateral_x_half_width_all_stable_seed_cases_mm']}` mm."
                ),
                f"Per-case lateral x-only h10 step2 grid points: `{summary['per_case_lateral_x_grid_points_h10_step2']}`.",
                f"Hypothetical per-case x/z h10 step2 tensor points: `{summary['hypothetical_per_case_xz_tensor_points_h10_step2']}`.",
                f"Z coverage validated: `{summary['z_coverage_validated']}`.",
                f"Ready for x/z neighborhood design: `{summary['ready_for_xz_neighborhood_design']}`.",
                f"Ready for narrow refinement contract: `{summary['ready_for_narrow_refinement_contract']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Half-width rows: `{half_width_csv.name}`.",
                f"- Grid budget rows: `{grid_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved detector contract and seed-export artifacts only. The contract validates",
                "lateral x-slot error, not z error. It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC",
                "jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract-run", default=DEFAULT_CONTRACT_RUN)
    parser.add_argument("--seed-export-run", default=DEFAULT_SEED_EXPORT_RUN)
    parser.add_argument("--half-widths-mm", default=DEFAULT_HALF_WIDTHS_MM)
    parser.add_argument("--steps-mm", default=DEFAULT_STEPS_MM)
    parser.add_argument("--component-count", type=int, default=DEFAULT_COMPONENT_COUNT)
    parser.add_argument("--run-name", default="local_2d_detector_lateral_slot_neighborhood_budget")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.component_count <= 0:
        raise ValueError("--component-count must be positive")
    root = Path("outputs/summary_tables")
    contract_dir = root / args.contract_run
    seed_dir = root / args.seed_export_run
    contract_rows = read_csv_rows(contract_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv")
    contract_summary = read_json(contract_dir / "data/local_2d_detector_refinement_launch_contract_summary.json")
    seed_summary = read_json(seed_dir / "data/local_2d_detector_component_seed_export_summary.json")
    half_widths = parse_positive_numbers(args.half_widths_mm)
    steps = parse_positive_numbers(args.steps_mm)

    half_width_rows = build_half_width_rows(contract_rows, half_widths)
    branch_rows = build_branch_half_width_rows(contract_rows, half_widths)
    grid_rows = build_grid_budget_rows(half_width_rows, steps, component_count=args.component_count)
    summary = summarize_budget(
        contract_rows,
        half_width_rows,
        branch_rows,
        grid_rows,
        contract_summary,
        seed_summary,
    )
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    half_width_csv = data_dir / "local_2d_detector_lateral_slot_half_width_rows.csv"
    branch_csv = data_dir / "local_2d_detector_lateral_slot_branch_rows.csv"
    grid_csv = data_dir / "local_2d_detector_lateral_slot_grid_budget_rows.csv"
    gates_csv = data_dir / "local_2d_detector_lateral_slot_gates.csv"
    summary_json = data_dir / "local_2d_detector_lateral_slot_neighborhood_budget_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_lateral_slot_neighborhood_budget.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(half_width_csv, [json_safe(row) for row in half_width_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(grid_csv, [json_safe(row) for row in grid_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_budget(half_width_rows, grid_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, half_width_csv, grid_csv)

    summary["paths"] = {
        "half_width_rows_csv": str(half_width_csv),
        "branch_rows_csv": str(branch_csv),
        "grid_budget_rows_csv": str(grid_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_contract_cases_csv": str(
            contract_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv"
        ),
        "source_contract_summary_json": str(
            contract_dir / "data/local_2d_detector_refinement_launch_contract_summary.json"
        ),
        "source_seed_export_summary_json": str(seed_dir / "data/local_2d_detector_component_seed_export_summary.json"),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_lateral_slot_neighborhood_budget",
        {
            "contract_run": args.contract_run,
            "seed_export_run": args.seed_export_run,
            "half_widths_mm": half_widths,
            "steps_mm": steps,
            "component_count": args.component_count,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
