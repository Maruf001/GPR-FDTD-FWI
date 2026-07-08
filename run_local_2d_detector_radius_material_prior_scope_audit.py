#!/usr/bin/env python3
"""Audit whether detector radius/material blockers can be scoped as synthetic priors."""

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

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PLAN_RUN = "017_local_2d_detector_baseline_command_plan_post_interface_patch"
DEFAULT_LAUNCH_CONTRACT_RUN = "077_local_2d_detector_refinement_launch_contract_audit"
DEFAULT_XZ_CONTRACT_RUN = "088_local_2d_detector_xz_seed_neighborhood_contract"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def case_key(row: dict) -> tuple[str, int, str]:
    return (
        str(row.get("branch_key", "")),
        safe_int(row.get("seed"), 0),
        str(row.get("case_variant", "")),
    )


def parse_float_list(value: object) -> list[float]:
    values: list[float] = []
    for item in str(value or "").split(","):
        item = item.strip()
        if not item:
            continue
        number = safe_float(item, math.nan)
        if math.isfinite(number):
            values.append(number)
    return values


def format_radius_pattern(values: list[float]) -> str:
    return ",".join(f"{value:g}" for value in values)


def material_prior_rows() -> list[dict]:
    return [
        {
            "parameter": "concrete_epsr",
            "value": float(cfg.CONCRETE_EPSR),
            "source": "config.py",
            "role": "controlled synthetic material prior",
        },
        {
            "parameter": "concrete_sigma_s_per_m",
            "value": float(cfg.CONCRETE_SIGMA),
            "source": "config.py",
            "role": "controlled synthetic material prior",
        },
        {
            "parameter": "rebar_epsr",
            "value": float(cfg.REBAR_EPSR),
            "source": "config.py",
            "role": "controlled synthetic material prior",
        },
        {
            "parameter": "rebar_sigma_s_per_m",
            "value": float(cfg.REBAR_SIGMA),
            "source": "config.py",
            "role": "controlled synthetic material prior",
        },
    ]


def build_case_rows(
    plan_rows: list[dict],
    launch_rows: list[dict],
    xz_contract_rows: list[dict],
) -> list[dict]:
    launch_by_key = {case_key(row): row for row in launch_rows}
    xz_by_key = {case_key(row): row for row in xz_contract_rows}
    outputs: list[dict] = []
    for plan in plan_rows:
        key = case_key(plan)
        launch = launch_by_key.get(key, {})
        xz = xz_by_key.get(key, {})
        radius_values = parse_float_list(plan.get("truth_radius_values_mm"))
        radius_prior_available = len(radius_values) > 0
        material_prior_available = True
        stable_xz_contract = str(xz.get("case_contract_status", "")) == "stable_in_contract"
        review_assignment = boolish(launch.get("review_assignment", xz.get("review_assignment", False)))
        detector_radius_seed = boolish(launch.get("radius_seed_available", False))
        detector_material_seed = boolish(launch.get("material_seed_available", False))
        outputs.append(
            {
                "case_label": (
                    f"{plan.get('branch_key', '')}|seed{safe_int(plan.get('seed'), 0)}|"
                    f"{plan.get('case_variant', '')}"
                ),
                "source_plan_case_label": plan.get("case_label", ""),
                "branch_key": plan.get("branch_key", ""),
                "seed": safe_int(plan.get("seed"), 0),
                "case_variant": plan.get("case_variant", ""),
                "xz_contract_status": xz.get("case_contract_status", "missing_xz_contract_row"),
                "review_assignment": review_assignment,
                "truth_radius_values_mm": format_radius_pattern(radius_values),
                "truth_radius_pattern_key": format_radius_pattern(radius_values),
                "radius_prior_available_from_synthetic_plan": radius_prior_available,
                "material_prior_available_from_config": material_prior_available,
                "detector_radius_seed_available": detector_radius_seed,
                "detector_material_seed_available": detector_material_seed,
                "controlled_synthetic_prior_contract_ready": (
                    stable_xz_contract
                    and radius_prior_available
                    and material_prior_available
                    and not review_assignment
                ),
                "detector_inferred_radius_material_contract_ready": False,
                "ready_for_narrow_refinement_launch": False,
                "ready_for_detector_seeded_fwi": False,
                "allowed_use": "controlled synthetic prior scope for stable saved detector cases",
                "blocked_use": "detector-inferred radius/material claims, field transfer, GPU/FWI launch",
            }
        )
    return sorted(outputs, key=lambda row: (row["branch_key"], row["seed"], row["case_variant"]))


def summarize_scope(
    case_rows: list[dict],
    material_rows: list[dict],
    launch_summary: dict,
    xz_summary: dict,
) -> dict:
    stable_prior_rows = [row for row in case_rows if boolish(row["controlled_synthetic_prior_contract_ready"])]
    review_rows = [row for row in case_rows if boolish(row["review_assignment"])]
    radius_patterns = sorted({row["truth_radius_pattern_key"] for row in case_rows if row["truth_radius_pattern_key"]})
    detector_radius_count = sum(boolish(row["detector_radius_seed_available"]) for row in case_rows)
    detector_material_count = sum(boolish(row["detector_material_seed_available"]) for row in case_rows)
    radius_pattern_consistent = len(radius_patterns) == 1
    material_prior_fixed = len(material_rows) == 4
    controlled_ready = (
        boolish(xz_summary.get("ready_for_branch_specific_xz_seed_neighborhood_contract", False))
        and len(stable_prior_rows) > 0
        and radius_pattern_consistent
        and material_prior_fixed
    )
    return {
        "policy_label": "local_2d_detector_radius_material_prior_scope_audit_cpu_no_fwi",
        "source_launch_contract_policy_label": launch_summary.get("policy_label", ""),
        "source_xz_contract_policy_label": xz_summary.get("policy_label", ""),
        "source_case_count": len(case_rows),
        "stable_controlled_prior_case_count": len(stable_prior_rows),
        "review_case_excluded_count": len(review_rows),
        "radius_prior_case_count": sum(
            boolish(row["radius_prior_available_from_synthetic_plan"]) for row in case_rows
        ),
        "unique_radius_pattern_count": len(radius_patterns),
        "radius_patterns_mm": ";".join(radius_patterns),
        "radius_pattern_consistent_across_cases": radius_pattern_consistent,
        "material_prior_parameter_count": len(material_rows),
        "material_prior_fixed_by_config": material_prior_fixed,
        "detector_radius_seed_available_count": detector_radius_count,
        "detector_material_seed_available_count": detector_material_count,
        "ready_for_controlled_synthetic_prior_contract": controlled_ready,
        "ready_for_detector_inferred_radius_material_contract": False,
        "ready_for_field_transfer": False,
        "ready_for_review_case_inclusion": False,
        "ready_for_narrow_refinement_launch": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_gpu_work": False,
        "gpu_priority": "none",
        "active_blocker_keys": launch_summary.get("active_blocker_keys", ""),
        "decision": (
            "The saved detector benchmark has a controlled synthetic radius/material prior: every case "
            "uses truth radii 5,6,8 mm and fixed config.py material constants. This can support a "
            "controlled synthetic prior-scope contract for the stable saved cases, but it is not a "
            "detector-inferred radius/material seed. Review cases, field transfer, narrow refinement, "
            "detector-seeded FWI, and GPU work remain blocked."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "controlled_synthetic_prior_contract",
            "ready": summary["ready_for_controlled_synthetic_prior_contract"],
            "allowed_use": "controlled synthetic stable-case radius/material prior scoping",
            "blocked_use": "detector-inferred radius/material claim",
            "evidence": (
                f"stable prior cases={summary['stable_controlled_prior_case_count']}; "
                f"radius patterns={summary['radius_patterns_mm']}; "
                f"material params={summary['material_prior_parameter_count']}"
            ),
        },
        {
            "gate_key": "detector_inferred_radius_material_contract",
            "ready": summary["ready_for_detector_inferred_radius_material_contract"],
            "allowed_use": "none",
            "blocked_use": "detector-inferred radius/material refinement contract",
            "evidence": (
                f"detector radius seeds={summary['detector_radius_seed_available_count']}; "
                f"detector material seeds={summary['detector_material_seed_available_count']}"
            ),
        },
        {
            "gate_key": "field_transfer",
            "ready": summary["ready_for_field_transfer"],
            "allowed_use": "none",
            "blocked_use": "field radius/material transfer",
            "evidence": "field dataset lacks calibrated radius/material/depth controls",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "GPU/FWI launch",
            "evidence": "prior-scope audit is not a refinement launch contract",
        },
    ]


def plot_scope(summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), constrained_layout=True)
    count_labels = [
        "source\ncases",
        "stable\nprior",
        "review\nexcluded",
        "detector\nradius",
        "detector\nmaterial",
    ]
    count_values = [
        summary["source_case_count"],
        summary["stable_controlled_prior_case_count"],
        summary["review_case_excluded_count"],
        summary["detector_radius_seed_available_count"],
        summary["detector_material_seed_available_count"],
    ]
    axes[0].bar(count_labels, count_values, color=["#6b6b6b", "#59a14f", "#e15759", "#bab0ac", "#bab0ac"])
    axes[0].set_ylabel("case count")
    axes[0].set_title("Radius/material prior availability")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["controlled\nprior", "detector\ninferred", "field\ntransfer", "GPU/FWI"]
    gate_values = [
        summary["ready_for_controlled_synthetic_prior_contract"],
        summary["ready_for_detector_inferred_radius_material_contract"],
        summary["ready_for_field_transfer"],
        summary["ready_for_detector_seeded_fwi"],
    ]
    axes[1].bar(
        gate_labels,
        [1 if value else 0 for value in gate_values],
        color=["#59a14f" if value else "#bab0ac" for value in gate_values],
    )
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_ylim(0, 1.15)
    axes[1].set_title("Scope gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.04,
        0.08,
        f"radii={summary['radius_patterns_mm']} mm\n"
        f"material params={summary['material_prior_parameter_count']}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector radius/material prior-scope audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_radius_material_prior_scope_audit.png`",
                "",
                "This CPU-only figure separates controlled synthetic radius/material priors",
                "from detector-inferred radius/material seeds.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Stable controlled-prior cases: `{summary['stable_controlled_prior_case_count']}`.",
                f"Review cases excluded: `{summary['review_case_excluded_count']}`.",
                f"Radius patterns: `{summary['radius_patterns_mm']}`.",
                f"Detector radius seeds: `{summary['detector_radius_seed_available_count']}`.",
                f"Detector material seeds: `{summary['detector_material_seed_available_count']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "The radius/material values are controlled synthetic design priors from the command",
                "plan and config, not detector-inferred seeds. This audit does not run refinement,",
                "FWI, GPU kernels, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-run", default=DEFAULT_PLAN_RUN)
    parser.add_argument("--launch-contract-run", default=DEFAULT_LAUNCH_CONTRACT_RUN)
    parser.add_argument("--xz-contract-run", default=DEFAULT_XZ_CONTRACT_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_radius_material_prior_scope_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path("outputs/summary_tables")
    plan_dir = root / args.plan_run
    launch_dir = root / args.launch_contract_run
    xz_dir = root / args.xz_contract_run

    plan_rows = read_csv_rows(plan_dir / "data/local_2d_detector_baseline_command_plan_rows.csv")
    launch_rows = read_csv_rows(launch_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv")
    xz_case_rows = read_csv_rows(xz_dir / "data/local_2d_detector_xz_seed_neighborhood_contract_cases.csv")
    launch_summary = read_json(launch_dir / "data/local_2d_detector_refinement_launch_contract_summary.json")
    xz_summary = read_json(xz_dir / "data/local_2d_detector_xz_seed_neighborhood_contract_summary.json")

    materials = material_prior_rows()
    cases = build_case_rows(plan_rows, launch_rows, xz_case_rows)
    summary = summarize_scope(cases, materials, launch_summary, xz_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    cases_csv = data_dir / "local_2d_detector_radius_material_prior_scope_cases.csv"
    materials_csv = data_dir / "local_2d_detector_radius_material_prior_scope_materials.csv"
    gates_csv = data_dir / "local_2d_detector_radius_material_prior_scope_gates.csv"
    summary_json = data_dir / "local_2d_detector_radius_material_prior_scope_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_radius_material_prior_scope_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(cases_csv, [json_safe(row) for row in cases])
    write_csv(materials_csv, [json_safe(row) for row in materials])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_scope(summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "paths": {
            "case_rows_csv": str(cases_csv),
            "material_rows_csv": str(materials_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "source_plan_rows_csv": str(plan_dir / "data/local_2d_detector_baseline_command_plan_rows.csv"),
            "source_launch_contract_summary_json": str(
                launch_dir / "data/local_2d_detector_refinement_launch_contract_summary.json"
            ),
            "source_xz_contract_summary_json": str(
                xz_dir / "data/local_2d_detector_xz_seed_neighborhood_contract_summary.json"
            ),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_radius_material_prior_scope_audit",
        {
            "summary_json": str(summary_json),
            "case_rows_csv": str(cases_csv),
            "material_rows_csv": str(materials_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
