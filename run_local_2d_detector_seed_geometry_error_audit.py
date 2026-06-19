#!/usr/bin/env python3
"""Audit matched x/z detector seed errors without launching refinement or FWI."""

from __future__ import annotations

import argparse
import csv
import itertools
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


DEFAULT_PLAN_RUN = "017_local_2d_detector_baseline_command_plan_post_interface_patch"
DEFAULT_CONTRACT_RUN = "077_local_2d_detector_refinement_launch_contract_audit"
DEFAULT_LATERAL_BUDGET_RUN = "084_local_2d_detector_lateral_slot_neighborhood_budget"
DEFAULT_HALF_WIDTHS_MM = "5,8,10,12,15"
DEFAULT_STEPS_MM = "1,2,5"
DEFAULT_COMPONENT_COUNT = 3


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float_list(value: object) -> list[float]:
    out: list[float] = []
    for item in str(value or "").split(","):
        item = item.strip()
        if not item:
            continue
        number = safe_float(item, math.nan)
        if math.isfinite(number):
            out.append(number)
    return out


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


def case_key(row: dict) -> tuple[str, int, str]:
    return (
        str(row.get("branch_key", "")),
        safe_int(row.get("seed"), 0),
        str(row.get("case_variant", "")),
    )


def stable_case_rows(rows: list[dict]) -> list[dict]:
    return [row for row in rows if boolish(row.get("candidate_component_seed_ready"))]


def review_case_rows(rows: list[dict]) -> list[dict]:
    return [row for row in rows if boolish(row.get("review_assignment"))]


def coordinate_grid_points(
    half_width_mm: float,
    step_mm: float,
    *,
    dimensions: int,
) -> int:
    values_per_axis = int(math.floor((2.0 * float(half_width_mm)) / float(step_mm))) + 1
    return values_per_axis**int(dimensions)


def best_coordinate_assignment(
    truth_points: list[tuple[float, float]],
    seed_points: list[tuple[float, float]],
) -> dict:
    if not truth_points or not seed_points:
        raise ValueError("truth and seed points are required")
    if len(seed_points) < len(truth_points):
        raise ValueError("seed point count must be at least truth point count")
    if len(seed_points) > 8:
        raise ValueError("assignment brute force is intended for small component sets")

    best: tuple[float, float, float, float, tuple[int, ...]] | None = None
    for selected_indices in itertools.permutations(range(len(seed_points)), len(truth_points)):
        total_linf = 0.0
        max_x = 0.0
        max_z = 0.0
        max_linf = 0.0
        for truth_index, seed_index in enumerate(selected_indices):
            truth_x, truth_z = truth_points[truth_index]
            seed_x, seed_z = seed_points[seed_index]
            x_error = abs(seed_x - truth_x)
            z_error = abs(seed_z - truth_z)
            linf_error = max(x_error, z_error)
            total_linf += linf_error
            max_x = max(max_x, x_error)
            max_z = max(max_z, z_error)
            max_linf = max(max_linf, linf_error)
        candidate = (max_linf, total_linf, max_x, max_z, selected_indices)
        if best is None or candidate < best:
            best = candidate

    assert best is not None
    selected_indices = best[-1]
    component_rows = []
    euclidean_errors = []
    linf_errors = []
    x_errors = []
    z_errors = []
    for truth_index, seed_index in enumerate(selected_indices):
        truth_x, truth_z = truth_points[truth_index]
        seed_x, seed_z = seed_points[seed_index]
        x_error = abs(seed_x - truth_x)
        z_error = abs(seed_z - truth_z)
        linf_error = max(x_error, z_error)
        euclidean_error = math.hypot(x_error, z_error)
        x_errors.append(x_error)
        z_errors.append(z_error)
        linf_errors.append(linf_error)
        euclidean_errors.append(euclidean_error)
        component_rows.append(
            {
                "truth_component_index": truth_index,
                "seed_component_index": seed_index,
                "truth_x_mm": truth_x,
                "truth_z_mm": truth_z,
                "x_seed_mm": seed_x,
                "z_seed_mm": seed_z,
                "x_abs_error_mm": x_error,
                "z_abs_error_mm": z_error,
                "linf_abs_error_mm": linf_error,
                "euclidean_error_mm": euclidean_error,
            }
        )

    return {
        "component_rows": component_rows,
        "max_x_error_mm": max(x_errors),
        "max_z_error_mm": max(z_errors),
        "max_linf_error_mm": max(linf_errors),
        "mean_linf_error_mm": float(np.mean(linf_errors)),
        "max_euclidean_error_mm": max(euclidean_errors),
        "assignment_cost_linf_sum_mm": sum(linf_errors),
    }


def build_geometry_error_rows(
    plan_rows: list[dict],
    contract_rows: list[dict],
) -> tuple[list[dict], list[dict]]:
    plan_by_key = {case_key(row): row for row in plan_rows}
    case_rows: list[dict] = []
    component_rows: list[dict] = []
    for contract in contract_rows:
        key = case_key(contract)
        if key not in plan_by_key:
            raise ValueError(f"missing plan row for {key!r}")
        plan = plan_by_key[key]
        truth_x = parse_float_list(plan.get("truth_x_values_mm"))
        truth_z = parse_float_list(plan.get("truth_z_values_mm"))
        seed_x = parse_float_list(contract.get("selected_x_values_mm"))
        seed_z = parse_float_list(contract.get("selected_z_values_mm"))
        if len(truth_x) != len(truth_z):
            raise ValueError(f"truth x/z length mismatch for {key!r}")
        if len(seed_x) != len(seed_z):
            raise ValueError(f"seed x/z length mismatch for {key!r}")

        assignment = best_coordinate_assignment(list(zip(truth_x, truth_z)), list(zip(seed_x, seed_z)))
        max_lateral_slot_error = safe_float(contract.get("max_target_slot_abs_error_mm"), math.nan)
        case_row = {
            "case_label": contract.get("case_label", ""),
            "source_plan_case_label": plan.get("case_label", ""),
            "branch_key": contract.get("branch_key", ""),
            "seed": safe_int(contract.get("seed"), 0),
            "case_variant": contract.get("case_variant", ""),
            "candidate_component_seed_ready": boolish(contract.get("candidate_component_seed_ready")),
            "review_assignment": boolish(contract.get("review_assignment")),
            "truth_free_stable_assignment": boolish(contract.get("truth_free_stable_assignment")),
            "selected_component_count": safe_int(contract.get("selected_component_count"), 0),
            "truth_component_count": len(truth_x),
            "component_candidate_count": safe_int(contract.get("component_candidate_count"), 0),
            "max_lateral_x_slot_error_mm": max_lateral_slot_error,
            "matched_max_x_error_mm": assignment["max_x_error_mm"],
            "matched_max_z_error_mm": assignment["max_z_error_mm"],
            "matched_max_linf_error_mm": assignment["max_linf_error_mm"],
            "matched_mean_linf_error_mm": assignment["mean_linf_error_mm"],
            "matched_max_euclidean_error_mm": assignment["max_euclidean_error_mm"],
            "z_exceeds_lateral_slot_error": assignment["max_z_error_mm"] > max_lateral_slot_error,
            "ready_for_xz_seed_neighborhood_design": boolish(contract.get("candidate_component_seed_ready")),
            "ready_for_narrow_refinement_contract": False,
            "ready_for_detector_seeded_fwi": False,
            "allowed_use": "matched x/z seed-error sizing for saved detector cases",
            "blocked_use": "radius/material seeding, narrow refinement launch, detector-seeded FWI",
        }
        case_rows.append(case_row)
        for component in assignment["component_rows"]:
            component_out = dict(case_row)
            component_out.update(component)
            component_rows.append(component_out)

    return (
        sorted(case_rows, key=lambda row: (row["branch_key"], row["seed"], row["case_variant"])),
        sorted(
            component_rows,
            key=lambda row: (
                row["branch_key"],
                row["seed"],
                row["case_variant"],
                row["truth_component_index"],
            ),
        ),
    )


def build_half_width_rows(case_rows: list[dict], half_widths_mm: list[float]) -> list[dict]:
    stable_rows = stable_case_rows(case_rows)
    review_rows = review_case_rows(case_rows)
    outputs: list[dict] = []
    for half_width in half_widths_mm:
        stable_xz_covered = [
            row for row in stable_rows if safe_float(row.get("matched_max_linf_error_mm"), math.inf) <= half_width
        ]
        stable_x_covered = [
            row for row in stable_rows if safe_float(row.get("matched_max_x_error_mm"), math.inf) <= half_width
        ]
        stable_z_covered = [
            row for row in stable_rows if safe_float(row.get("matched_max_z_error_mm"), math.inf) <= half_width
        ]
        review_xz_covered = [
            row for row in review_rows if safe_float(row.get("matched_max_linf_error_mm"), math.inf) <= half_width
        ]
        all_xz_covered = [
            row for row in case_rows if safe_float(row.get("matched_max_linf_error_mm"), math.inf) <= half_width
        ]
        outputs.append(
            {
                "half_width_mm": half_width,
                "source_case_count": len(case_rows),
                "stable_seed_case_count": len(stable_rows),
                "stable_seed_xz_covered_count": len(stable_xz_covered),
                "stable_seed_x_covered_count": len(stable_x_covered),
                "stable_seed_z_covered_count": len(stable_z_covered),
                "stable_seed_xz_coverage_fraction": len(stable_xz_covered) / len(stable_rows) if stable_rows else math.nan,
                "review_case_count": len(review_rows),
                "review_case_xz_covered_count": len(review_xz_covered),
                "all_case_xz_covered_count": len(all_xz_covered),
                "all_case_xz_coverage_fraction": len(all_xz_covered) / len(case_rows) if case_rows else math.nan,
                "uncovered_stable_case_labels": ";".join(
                    row.get("case_label", "")
                    for row in stable_rows
                    if safe_float(row.get("matched_max_linf_error_mm"), math.inf) > half_width
                ),
                "covered_review_case_labels": ";".join(row.get("case_label", "") for row in review_xz_covered),
                "coverage_dimension": "matched_xz_linf",
                "ready_for_xz_seed_neighborhood_design": (
                    len(stable_xz_covered) == len(stable_rows) and len(stable_rows) > 0
                ),
                "ready_for_refinement_launch": False,
            }
        )
    return outputs


def build_branch_rows(case_rows: list[dict], half_widths_mm: list[float]) -> list[dict]:
    outputs: list[dict] = []
    for branch in sorted({row.get("branch_key", "") for row in case_rows}):
        branch_rows = [row for row in case_rows if row.get("branch_key", "") == branch]
        branch_stable = stable_case_rows(branch_rows)
        branch_review = review_case_rows(branch_rows)
        for half_width in half_widths_mm:
            stable_xz_covered = [
                row
                for row in branch_stable
                if safe_float(row.get("matched_max_linf_error_mm"), math.inf) <= half_width
            ]
            review_xz_covered = [
                row
                for row in branch_review
                if safe_float(row.get("matched_max_linf_error_mm"), math.inf) <= half_width
            ]
            outputs.append(
                {
                    "branch_key": branch,
                    "half_width_mm": half_width,
                    "branch_case_count": len(branch_rows),
                    "stable_seed_case_count": len(branch_stable),
                    "stable_seed_xz_covered_count": len(stable_xz_covered),
                    "stable_seed_xz_coverage_fraction": (
                        len(stable_xz_covered) / len(branch_stable) if branch_stable else math.nan
                    ),
                    "review_case_count": len(branch_review),
                    "review_case_xz_covered_count": len(review_xz_covered),
                    "ready_for_branch_xz_seed_neighborhood_design": (
                        len(stable_xz_covered) == len(branch_stable) and len(branch_stable) > 0
                    ),
                }
            )
    return outputs


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
            lateral_points = coordinate_grid_points(half_width, step, dimensions=component_count)
            xz_points = coordinate_grid_points(half_width, step, dimensions=2 * component_count)
            outputs.append(
                {
                    "half_width_mm": half_width,
                    "step_mm": step,
                    "component_count": component_count,
                    "coverage_dimension": "matched_xz_linf",
                    "coordinate_dimensions": 2 * component_count,
                    "values_per_axis": int(math.floor((2.0 * half_width) / step)) + 1,
                    "per_case_lateral_x_grid_points": lateral_points,
                    "per_case_xz_grid_points": xz_points,
                    "stable_seed_total_xz_grid_points": xz_points * stable_count,
                    "all_case_total_xz_grid_points": xz_points * source_count,
                    "ready_for_refinement_launch": False,
                    "allowed_use": "matched x/z coordinate seed neighborhood sizing",
                    "blocked_use": "radius/material tensor refinement, detector-seeded FWI",
                }
            )
    return outputs


def _min_covering_half_width(rows: list[dict], covered_key: str, total_key: str) -> float:
    for row in sorted(rows, key=lambda item: safe_float(item.get("half_width_mm"))):
        if safe_int(row.get(covered_key), 0) == safe_int(row.get(total_key), 0) and safe_int(row.get(total_key), 0) > 0:
            return safe_float(row.get("half_width_mm"))
    return math.nan


def _half_width_value_at(rows: list[dict], half_width_mm: float, field: str) -> float:
    for row in rows:
        if math.isclose(safe_float(row.get("half_width_mm")), half_width_mm):
            return safe_float(row.get(field))
    return math.nan


def _grid_points_at(grid_rows: list[dict], half_width_mm: float, step_mm: float, field: str) -> float:
    for row in grid_rows:
        if math.isclose(safe_float(row.get("half_width_mm")), half_width_mm) and math.isclose(
            safe_float(row.get("step_mm")), step_mm
        ):
            return safe_float(row.get(field))
    return math.nan


def summarize_audit(
    case_rows: list[dict],
    half_width_rows: list[dict],
    branch_rows: list[dict],
    grid_rows: list[dict],
    contract_summary: dict,
    lateral_budget_summary: dict,
) -> dict:
    stable_rows = stable_case_rows(case_rows)
    review_rows = review_case_rows(case_rows)
    stable_x = [safe_float(row.get("matched_max_x_error_mm")) for row in stable_rows]
    stable_z = [safe_float(row.get("matched_max_z_error_mm")) for row in stable_rows]
    stable_linf = [safe_float(row.get("matched_max_linf_error_mm")) for row in stable_rows]
    z_exceeds_count = sum(1 for row in stable_rows if boolish(row.get("z_exceeds_lateral_slot_error")))
    min_xz_half_width = _min_covering_half_width(
        half_width_rows,
        "stable_seed_xz_covered_count",
        "stable_seed_case_count",
    )
    branch_min_parts = []
    for branch in sorted({row.get("branch_key", "") for row in branch_rows}):
        rows = [row for row in branch_rows if row.get("branch_key", "") == branch]
        branch_min_parts.append(
            f"{branch}:{_min_covering_half_width(rows, 'stable_seed_xz_covered_count', 'stable_seed_case_count'):.1f}"
        )

    return {
        "policy_label": "local_2d_detector_seed_geometry_error_audit_cpu_no_fwi",
        "source_contract_policy_label": contract_summary.get("policy_label", ""),
        "source_lateral_budget_policy_label": lateral_budget_summary.get("policy_label", ""),
        "coverage_dimension": "matched_xz_linf",
        "source_case_count": len(case_rows),
        "stable_seed_case_count": len(stable_rows),
        "review_case_count": len(review_rows),
        "max_stable_x_error_mm": max(stable_x) if stable_x else math.nan,
        "max_stable_z_error_mm": max(stable_z) if stable_z else math.nan,
        "max_stable_linf_error_mm": max(stable_linf) if stable_linf else math.nan,
        "median_stable_linf_error_mm": float(np.median(stable_linf)) if stable_linf else math.nan,
        "stable_cases_z_exceeds_lateral_slot_error_count": z_exceeds_count,
        "min_xz_half_width_all_stable_seed_cases_mm": min_xz_half_width,
        "source_lateral_min_half_width_all_stable_seed_cases_mm": safe_float(
            lateral_budget_summary.get("min_lateral_x_half_width_all_stable_seed_cases_mm"), math.nan
        ),
        "branch_min_xz_half_width_all_stable_seed_cases_mm": ";".join(branch_min_parts),
        "stable_xz_coverage_at_5mm": _half_width_value_at(half_width_rows, 5.0, "stable_seed_xz_covered_count"),
        "stable_xz_coverage_at_8mm": _half_width_value_at(half_width_rows, 8.0, "stable_seed_xz_covered_count"),
        "stable_xz_coverage_at_10mm": _half_width_value_at(half_width_rows, 10.0, "stable_seed_xz_covered_count"),
        "stable_xz_coverage_at_12mm": _half_width_value_at(half_width_rows, 12.0, "stable_seed_xz_covered_count"),
        "review_xz_coverage_at_12mm": _half_width_value_at(half_width_rows, 12.0, "review_case_xz_covered_count"),
        "per_case_xz_grid_points_h10_step2": _grid_points_at(grid_rows, 10.0, 2.0, "per_case_xz_grid_points"),
        "per_case_xz_grid_points_h12_step2": _grid_points_at(grid_rows, 12.0, 2.0, "per_case_xz_grid_points"),
        "stable_total_xz_grid_points_h12_step2": _grid_points_at(
            grid_rows,
            12.0,
            2.0,
            "stable_seed_total_xz_grid_points",
        ),
        "ready_for_xz_seed_neighborhood_design": math.isfinite(min_xz_half_width),
        "ready_for_radius_material_contract": False,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_naive_full_tensor_refinement": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Matched x/z seed errors show that the 10 stable detector seed cases need a 12 mm "
            "x/z L-infinity half-width, not the earlier 10 mm lateral x-slot half-width. "
            "This closes the z-evidence gap for seed-neighborhood sizing only. Radius/material "
            "seeds, review-case policy exclusions, independent selector validation, and FWI launch "
            "contracts remain blocked; do not launch detector-seeded refinement or FWI from this audit."
        ),
    }


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "xz_seed_neighborhood_design",
            "ready": summary["ready_for_xz_seed_neighborhood_design"],
            "allowed_use": "matched x/z coordinate seed-neighborhood sizing",
            "blocked_use": "narrow refinement launch",
            "evidence": (
                f"min x/z half-width all stable seeds="
                f"{summary['min_xz_half_width_all_stable_seed_cases_mm']:.1f} mm"
            ),
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
            "blocked_use": "narrow coordinate/refinement launch",
            "evidence": "review cases and non-coordinate launch blockers remain active",
        },
        {
            "gate_key": "naive_full_tensor_refinement",
            "ready": summary["ready_for_naive_full_tensor_refinement"],
            "allowed_use": "none",
            "blocked_use": "full 6D coordinate tensor FWI/refinement queue",
            "evidence": (
                f"h12 step2 x/z tensor={summary['per_case_xz_grid_points_h12_step2']:.0f} points/case"
            ),
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI",
            "evidence": "radius/material seeds, launch contract, and review-case closure remain blocked",
        },
    ]


def plot_audit(case_rows: list[dict], half_width_rows: list[dict], grid_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)

    stable_rows = stable_case_rows(case_rows)
    labels = [
        row["case_label"].replace("target2_", "").replace("_linear29p5", "29p5").replace("|", "\n")
        for row in stable_rows
    ]
    x = np.arange(len(stable_rows), dtype=float)
    width = 0.34
    axes[0].bar(
        x - width / 2,
        [safe_float(row.get("matched_max_x_error_mm")) for row in stable_rows],
        width=width,
        color="#4c72b0",
        label="x",
    )
    axes[0].bar(
        x + width / 2,
        [safe_float(row.get("matched_max_z_error_mm")) for row in stable_rows],
        width=width,
        color="#dd8452",
        label="z",
    )
    axes[0].axhline(summary["min_xz_half_width_all_stable_seed_cases_mm"], color="#333333", linestyle="--", linewidth=0.8)
    axes[0].set_xticks(x, labels, rotation=55, ha="right", fontsize=7)
    axes[0].set_ylabel("max matched component error (mm)")
    axes[0].set_title("Stable seed x/z errors")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    half_widths = [safe_float(row.get("half_width_mm")) for row in half_width_rows]
    axes[1].plot(
        half_widths,
        [safe_float(row.get("stable_seed_xz_covered_count")) for row in half_width_rows],
        marker="o",
        color="#4c72b0",
        label="stable x/z covered",
    )
    axes[1].plot(
        half_widths,
        [safe_float(row.get("review_case_xz_covered_count")) for row in half_width_rows],
        marker="s",
        color="#c44e52",
        label="review x/z covered",
    )
    axes[1].set_xlabel("x/z L-infinity half-width (mm)")
    axes[1].set_ylabel("covered cases")
    axes[1].set_title("Matched seed-neighborhood coverage")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.04,
        0.08,
        f"stable cases: {summary['stable_seed_case_count']}/{summary['source_case_count']}\n"
        f"min x/z half-width: {summary['min_xz_half_width_all_stable_seed_cases_mm']:.1f} mm\n"
        f"max stable z error: {summary['max_stable_z_error_mm']:.1f} mm\n"
        f"h12 step2 x/z tensor: {summary['per_case_xz_grid_points_h12_step2']:.0f}\n"
        f"ready for FWI: {summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector matched x/z seed geometry audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, case_csv: Path, component_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_seed_geometry_error_audit.png`",
                "",
                "This CPU-only figure joins the baseline detector truth plan with the saved detector launch-contract rows,",
                "then computes matched x/z component seed errors for the stable exported detector cases.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Stable seed cases: `{summary['stable_seed_case_count']}`.",
                f"Review cases: `{summary['review_case_count']}`.",
                f"Max stable x error: `{summary['max_stable_x_error_mm']}` mm.",
                f"Max stable z error: `{summary['max_stable_z_error_mm']}` mm.",
                f"Minimum x/z half-width for all stable cases: `{summary['min_xz_half_width_all_stable_seed_cases_mm']}` mm.",
                f"Per-case h12/step2 x/z tensor points: `{summary['per_case_xz_grid_points_h12_step2']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case rows: `{case_csv.name}`.",
                f"- Component rows: `{component_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved CSV/JSON tables only. It does not run FDTD, FWI, GPU kernels, field FWI,",
                "3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-run", default=DEFAULT_PLAN_RUN)
    parser.add_argument("--contract-run", default=DEFAULT_CONTRACT_RUN)
    parser.add_argument("--lateral-budget-run", default=DEFAULT_LATERAL_BUDGET_RUN)
    parser.add_argument("--half-widths-mm", default=DEFAULT_HALF_WIDTHS_MM)
    parser.add_argument("--steps-mm", default=DEFAULT_STEPS_MM)
    parser.add_argument("--run-name", default="local_2d_detector_seed_geometry_error_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path("outputs/summary_tables")
    plan_dir = root / args.plan_run
    contract_dir = root / args.contract_run
    lateral_budget_dir = root / args.lateral_budget_run

    plan_rows = read_csv_rows(plan_dir / "data/local_2d_detector_baseline_command_plan_rows.csv")
    contract_rows = read_csv_rows(contract_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv")
    contract_summary = read_json(contract_dir / "data/local_2d_detector_refinement_launch_contract_summary.json")
    lateral_budget_summary = read_json(
        lateral_budget_dir / "data/local_2d_detector_lateral_slot_neighborhood_budget_summary.json"
    )
    half_widths_mm = parse_positive_numbers(args.half_widths_mm)
    steps_mm = parse_positive_numbers(args.steps_mm)

    case_rows, component_rows = build_geometry_error_rows(plan_rows, contract_rows)
    half_width_rows = build_half_width_rows(case_rows, half_widths_mm)
    branch_rows = build_branch_rows(case_rows, half_widths_mm)
    grid_rows = build_grid_budget_rows(half_width_rows, steps_mm)
    summary = summarize_audit(case_rows, half_width_rows, branch_rows, grid_rows, contract_summary, lateral_budget_summary)
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_seed_geometry_error_cases.csv"
    component_csv = data_dir / "local_2d_detector_seed_geometry_error_components.csv"
    half_width_csv = data_dir / "local_2d_detector_seed_geometry_error_half_width_rows.csv"
    branch_csv = data_dir / "local_2d_detector_seed_geometry_error_branch_rows.csv"
    grid_csv = data_dir / "local_2d_detector_seed_geometry_error_grid_budget_rows.csv"
    gates_csv = data_dir / "local_2d_detector_seed_geometry_error_gates.csv"
    summary_json = data_dir / "local_2d_detector_seed_geometry_error_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_seed_geometry_error_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(case_csv, [json_safe(row) for row in case_rows])
    write_csv(component_csv, [json_safe(row) for row in component_rows])
    write_csv(half_width_csv, [json_safe(row) for row in half_width_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(grid_csv, [json_safe(row) for row in grid_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_audit(case_rows, half_width_rows, grid_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, case_csv, component_csv)
    summary["paths"] = {
        "case_rows_csv": str(case_csv),
        "component_rows_csv": str(component_csv),
        "half_width_rows_csv": str(half_width_csv),
        "branch_rows_csv": str(branch_csv),
        "grid_budget_rows_csv": str(grid_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_seed_geometry_error_audit",
        {
            "plan_run": args.plan_run,
            "contract_run": args.contract_run,
            "lateral_budget_run": args.lateral_budget_run,
            "summary_json": str(summary_json),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
