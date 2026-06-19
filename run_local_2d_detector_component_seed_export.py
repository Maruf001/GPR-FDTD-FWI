#!/usr/bin/env python3
"""Export stable detector component seeds without creating an FWI launch contract."""

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
COMPONENT_ROLES = ("left", "middle", "right")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float_list(value: object) -> list[float]:
    out: list[float] = []
    for item in str(value or "").split(","):
        item = item.strip()
        if not item:
            continue
        number = safe_float(item)
        if math.isfinite(number):
            out.append(number)
    return out


def build_component_seed_rows(contract_rows: list[dict]) -> list[dict]:
    outputs: list[dict] = []
    for row in contract_rows:
        if not boolish(row.get("candidate_component_seed_ready")):
            continue
        x_values = parse_float_list(row.get("selected_x_values_mm"))
        z_values = parse_float_list(row.get("selected_z_values_mm"))
        if len(x_values) != len(z_values):
            continue
        for index, (x_mm, z_mm) in enumerate(zip(x_values, z_values)):
            role = COMPONENT_ROLES[index] if index < len(COMPONENT_ROLES) else f"component_{index}"
            outputs.append(
                {
                    "case_label": row.get("case_label", ""),
                    "branch_key": row.get("branch_key", ""),
                    "seed": safe_int(row.get("seed"), 0),
                    "case_variant": row.get("case_variant", ""),
                    "component_index": index,
                    "component_role": role,
                    "x_seed_mm": x_mm,
                    "z_seed_mm": z_mm,
                    "selected_component_count": safe_int(row.get("selected_component_count"), 0),
                    "component_candidate_count": safe_int(row.get("component_candidate_count"), 0),
                    "detector_reliability_label": row.get("detector_reliability_label", ""),
                    "truth_free_stable_assignment": boolish(row.get("truth_free_stable_assignment")),
                    "max_case_component_seed_error_mm": safe_float(row.get("max_target_slot_abs_error_mm")),
                    "coarse_error_gate_mm": safe_float(row.get("coarse_error_gate_mm")),
                    "coarse_error_gate_pass": boolish(row.get("coarse_error_gate_pass")),
                    "radius_seed_available": False,
                    "material_seed_available": False,
                    "coordinate_seed_ready": True,
                    "narrow_refinement_ready": False,
                    "detector_seeded_fwi_ready": False,
                    "allowed_use": "coordinate-only saved component seed table for later design",
                    "blocked_use": "radius/material seeding, narrow refinement launch, detector-seeded FWI",
                }
            )
    return sorted(
        outputs,
        key=lambda item: (
            item["branch_key"],
            item["seed"],
            item["case_variant"],
            item["component_index"],
        ),
    )


def build_excluded_case_rows(contract_rows: list[dict]) -> list[dict]:
    outputs = []
    for row in contract_rows:
        if boolish(row.get("candidate_component_seed_ready")):
            continue
        outputs.append(
            {
                "case_label": row.get("case_label", ""),
                "branch_key": row.get("branch_key", ""),
                "seed": safe_int(row.get("seed"), 0),
                "case_variant": row.get("case_variant", ""),
                "detector_reliability_label": row.get("detector_reliability_label", ""),
                "review_assignment": boolish(row.get("review_assignment")),
                "truth_free_stable_assignment": boolish(row.get("truth_free_stable_assignment")),
                "best_variant_all_slots_hit": boolish(row.get("best_variant_all_slots_hit")),
                "success_fraction_truth_eval": safe_float(row.get("success_fraction_truth_eval"), 0.0),
                "max_target_slot_abs_error_mm": safe_float(row.get("max_target_slot_abs_error_mm")),
                "launch_blocker": row.get("launch_blocker", ""),
                "exclusion_reason": (
                    "review_assignment"
                    if boolish(row.get("review_assignment"))
                    else "not_candidate_component_seed_ready"
                ),
            }
        )
    return sorted(outputs, key=lambda item: (item["branch_key"], item["seed"], item["case_variant"]))


def build_branch_rows(seed_rows: list[dict], excluded_rows: list[dict], contract_rows: list[dict]) -> list[dict]:
    branches = sorted({row.get("branch_key", "") for row in contract_rows})
    outputs = []
    for branch in branches:
        branch_contract = [row for row in contract_rows if row.get("branch_key", "") == branch]
        branch_seeds = [row for row in seed_rows if row.get("branch_key", "") == branch]
        branch_excluded = [row for row in excluded_rows if row.get("branch_key", "") == branch]
        seed_case_labels = sorted({row["case_label"] for row in branch_seeds})
        errors = [
            safe_float(row.get("max_case_component_seed_error_mm"))
            for row in branch_seeds
            if math.isfinite(safe_float(row.get("max_case_component_seed_error_mm")))
        ]
        outputs.append(
            {
                "branch_key": branch,
                "case_count": len(branch_contract),
                "exported_seed_case_count": len(seed_case_labels),
                "exported_component_row_count": len(branch_seeds),
                "excluded_case_count": len(branch_excluded),
                "max_exported_case_seed_error_mm": max(errors) if errors else math.nan,
                "median_exported_case_seed_error_mm": float(np.median(errors)) if errors else math.nan,
                "excluded_case_labels": ";".join(row["case_label"] for row in branch_excluded),
            }
        )
    return outputs


def summarize_seed_export(
    seed_rows: list[dict],
    excluded_rows: list[dict],
    branch_rows: list[dict],
    contract_summary: dict,
) -> dict:
    seed_case_labels = sorted({row["case_label"] for row in seed_rows})
    errors = [
        safe_float(row.get("max_case_component_seed_error_mm"))
        for row in seed_rows
        if math.isfinite(safe_float(row.get("max_case_component_seed_error_mm")))
    ]
    return {
        "policy_label": "local_2d_detector_component_seed_export_coordinate_only_no_fwi",
        "source_contract_policy_label": contract_summary.get("policy_label", ""),
        "source_case_count": safe_float(contract_summary.get("case_count"), 0.0),
        "exported_seed_case_count": len(seed_case_labels),
        "exported_component_row_count": len(seed_rows),
        "excluded_review_case_count": len(excluded_rows),
        "branch_count": len(branch_rows),
        "exported_seed_case_labels": ";".join(seed_case_labels),
        "excluded_case_labels": ";".join(row["case_label"] for row in excluded_rows),
        "max_exported_case_seed_error_mm": max(errors) if errors else math.nan,
        "median_exported_case_seed_error_mm": float(np.median(errors)) if errors else math.nan,
        "active_blocker_count": safe_float(contract_summary.get("active_blocker_count"), 0.0),
        "active_blocker_keys": contract_summary.get("active_blocker_keys", ""),
        "radius_seed_available": False,
        "material_seed_available": False,
        "ready_for_coordinate_seed_table": len(seed_rows) > 0,
        "ready_for_radius_material_contract": False,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Export the 10 stable detector cases as coordinate-only x/z component seeds for future design work. "
            "Do not launch detector-seeded refinement or FWI from this table because radius/material seeds, "
            "independent selector validation, branch transfer, and review-case closure remain blocked."
        ),
    }


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "coordinate_seed_table",
            "ready": summary["ready_for_coordinate_seed_table"],
            "allowed_use": "coordinate-only seed table for later design",
            "blocked_use": "none within coordinate-seed export scope",
            "evidence": (
                f"seed cases={summary['exported_seed_case_count']}/"
                f"{int(summary['source_case_count'])}; components={summary['exported_component_row_count']}"
            ),
        },
        {
            "gate_key": "radius_material_contract",
            "ready": summary["ready_for_radius_material_contract"],
            "allowed_use": "none",
            "blocked_use": "radius/material initialization contract",
            "evidence": "detector rows export x/z only",
        },
        {
            "gate_key": "narrow_refinement_contract",
            "ready": summary["ready_for_narrow_refinement_contract"],
            "allowed_use": "none",
            "blocked_use": "narrow coordinate/refinement launch",
            "evidence": f"active blockers={summary['active_blocker_count']}",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI",
            "evidence": summary["active_blocker_keys"],
        },
    ]


def plot_seed_export(branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    labels = [row["branch_key"].replace("target2_", "") for row in branch_rows]
    x = np.arange(len(branch_rows), dtype=float)
    width = 0.34
    axes[0].bar(
        x - width / 2,
        [row["exported_seed_case_count"] for row in branch_rows],
        width=width,
        color="#4c72b0",
        label="exported",
    )
    axes[0].bar(
        x + width / 2,
        [row["excluded_case_count"] for row in branch_rows],
        width=width,
        color="#c44e52",
        label="excluded",
    )
    axes[0].set_xticks(x, labels, rotation=10)
    axes[0].set_ylabel("case count")
    axes[0].set_title("Coordinate seed export by branch")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    gate_labels = ["coordinate\nseeds", "radius/material\ncontract", "narrow\nrefinement", "detector\nFWI"]
    gate_values = [
        summary["ready_for_coordinate_seed_table"],
        summary["ready_for_radius_material_contract"],
        summary["ready_for_narrow_refinement_contract"],
        summary["ready_for_detector_seeded_fwi"],
    ]
    colors = ["#59a14f" if value else "#bab0ac" for value in gate_values]
    axes[1].bar(np.arange(len(gate_labels)), [1 if value else 0 for value in gate_values], color=colors)
    axes[1].set_xticks(np.arange(len(gate_labels)), gate_labels)
    axes[1].set_ylim(0, 1.15)
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_title("Export gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.04,
        0.06,
        f"exported cases: {summary['exported_seed_case_count']}/{int(summary['source_case_count'])}\n"
        f"component rows: {summary['exported_component_row_count']}\n"
        f"excluded review cases: {summary['excluded_review_case_count']}\n"
        f"active blockers: {summary['active_blocker_count']:.0f}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector coordinate seed export", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, seed_csv: Path, excluded_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_component_seed_export.png`",
                "",
                "This CPU-only figure exports stable detector rows as coordinate-only",
                "component seeds for later design work.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Exported seed cases: `{summary['exported_seed_case_count']}`.",
                f"Exported component rows: `{summary['exported_component_row_count']}`.",
                f"Excluded review cases: `{summary['excluded_review_case_count']}`.",
                f"Ready for coordinate seed table: `{summary['ready_for_coordinate_seed_table']}`.",
                f"Ready for radius/material contract: `{summary['ready_for_radius_material_contract']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Component seed rows: `{seed_csv.name}`.",
                f"- Excluded case rows: `{excluded_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This export reads saved detector launch-contract rows only. It does not run FDTD, FWI, GPU kernels,",
                "field FWI, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract-run", default=DEFAULT_CONTRACT_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_component_seed_export")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path("outputs/summary_tables")
    contract_dir = root / args.contract_run
    contract_rows = read_csv_rows(contract_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv")
    contract_summary = read_json(contract_dir / "data/local_2d_detector_refinement_launch_contract_summary.json")

    seed_rows = build_component_seed_rows(contract_rows)
    excluded_rows = build_excluded_case_rows(contract_rows)
    branch_rows = build_branch_rows(seed_rows, excluded_rows, contract_rows)
    summary = summarize_seed_export(seed_rows, excluded_rows, branch_rows, contract_summary)
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    seed_csv = data_dir / "local_2d_detector_component_seed_rows.csv"
    excluded_csv = data_dir / "local_2d_detector_component_seed_excluded_cases.csv"
    branch_csv = data_dir / "local_2d_detector_component_seed_branch_rows.csv"
    gates_csv = data_dir / "local_2d_detector_component_seed_gates.csv"
    summary_json = data_dir / "local_2d_detector_component_seed_export_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_component_seed_export.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(seed_csv, [json_safe(row) for row in seed_rows])
    write_csv(excluded_csv, [json_safe(row) for row in excluded_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_seed_export(branch_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, seed_csv, excluded_csv)

    summary["paths"] = {
        "component_seed_rows_csv": str(seed_csv),
        "excluded_cases_csv": str(excluded_csv),
        "branch_rows_csv": str(branch_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_contract_cases_csv": str(
            contract_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv"
        ),
        "source_contract_summary_json": str(
            contract_dir / "data/local_2d_detector_refinement_launch_contract_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_component_seed_export",
        {
            "contract_run": args.contract_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
