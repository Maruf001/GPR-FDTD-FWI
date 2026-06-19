#!/usr/bin/env python3
"""Preflight exact-radius detector seeds for geometric non-overlap."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from run_local_2d_detector_radius_material_prior_scope_audit import parse_float_list  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPONENT_SEED_RUN = "081_local_2d_detector_component_seed_export"
DEFAULT_PRIOR_SCOPE_RUN = "089_local_2d_detector_radius_material_prior_scope_audit"
DEFAULT_REPAIR_STEP_MM = 2.0


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def format_values(values: list[float]) -> str:
    return ",".join(f"{value:g}" for value in values)


def group_seed_rows(seed_rows: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in seed_rows:
        grouped[str(row.get("case_label", ""))].append(row)
    return {
        case_label: sorted(rows, key=lambda item: safe_int(item.get("component_index"), 0))
        for case_label, rows in grouped.items()
    }


def prior_by_case(prior_rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("case_label", "")): row for row in prior_rows}


def pair_clearance_rows(
    case_label: str,
    x_values: list[float],
    z_values: list[float],
    radii: list[float],
) -> list[dict]:
    rows: list[dict] = []
    for first in range(len(radii)):
        for second in range(first + 1, len(radii)):
            distance = math.hypot(
                float(x_values[first]) - float(x_values[second]),
                float(z_values[first]) - float(z_values[second]),
            )
            radius_sum = float(radii[first]) + float(radii[second])
            clearance = distance - radius_sum
            rows.append(
                {
                    "case_label": case_label,
                    "pair_key": f"{first}-{second}",
                    "first_component_index": first,
                    "second_component_index": second,
                    "first_x_seed_mm": float(x_values[first]),
                    "first_z_seed_mm": float(z_values[first]),
                    "first_radius_mm": float(radii[first]),
                    "second_x_seed_mm": float(x_values[second]),
                    "second_z_seed_mm": float(z_values[second]),
                    "second_radius_mm": float(radii[second]),
                    "center_distance_mm": distance,
                    "radius_sum_mm": radius_sum,
                    "clearance_mm": clearance,
                    "overlaps_under_exact_radii": clearance < -1.0e-9,
                }
            )
    return rows


def build_preflight_rows(
    seed_rows: list[dict],
    prior_rows: list[dict],
    *,
    repair_step_mm: float = DEFAULT_REPAIR_STEP_MM,
) -> tuple[list[dict], list[dict]]:
    prior_lookup = prior_by_case(prior_rows)
    cases: list[dict] = []
    pairs: list[dict] = []
    for case_label, rows in sorted(group_seed_rows(seed_rows).items()):
        prior = prior_lookup.get(case_label, {})
        radii = parse_float_list(str(prior.get("truth_radius_pattern_key") or prior.get("truth_radius_values_mm")))
        if len(radii) != len(rows):
            raise ValueError(f"case {case_label} has {len(rows)} seed rows but {len(radii)} radii")
        x_values = [safe_float(row.get("x_seed_mm")) for row in rows]
        z_values = [safe_float(row.get("z_seed_mm")) for row in rows]
        case_pairs = pair_clearance_rows(case_label, x_values, z_values, radii)
        pairs.extend(case_pairs)
        min_clearance = min(row["clearance_mm"] for row in case_pairs)
        overlap_pairs = [row for row in case_pairs if row["overlaps_under_exact_radii"]]
        repair_needed = max(0.0, -float(min_clearance))
        first = rows[0]
        ready = not overlap_pairs and boolish(first.get("coordinate_seed_ready", False))
        cases.append(
            {
                "case_label": case_label,
                "branch_key": first.get("branch_key", ""),
                "seed": safe_int(first.get("seed"), 0),
                "case_variant": first.get("case_variant", ""),
                "component_count": len(rows),
                "exact_radius_values_mm": format_values(radii),
                "x_seed_values_mm": format_values(x_values),
                "z_seed_values_mm": format_values(z_values),
                "min_pair_clearance_mm": min_clearance,
                "overlapping_pair_count": len(overlap_pairs),
                "overlapping_pair_keys": ";".join(row["pair_key"] for row in overlap_pairs),
                "repair_required_mm": repair_needed,
                "repair_within_default_step": repair_needed > 0.0 and repair_needed <= float(repair_step_mm) + 1.0e-9,
                "exact_radius_seed_nonoverlap_ready": not overlap_pairs,
                "direct_fixed_radius_pilot_ready": ready,
                "ready_for_repair_preflight": bool(overlap_pairs),
                "ready_for_detector_seeded_fwi": False,
                "allowed_use": (
                    "direct fixed-radius local pilot seed"
                    if ready
                    else "repair/preflight blocker before fixed-radius local pilot"
                ),
                "blocked_use": "broad GPU queue, detector-inferred radius/material, field transfer, FWI launch",
            }
        )
    return cases, pairs


def summarize_preflight(
    case_rows: list[dict],
    pair_rows: list[dict],
    seed_summary: dict,
    prior_summary: dict,
    *,
    repair_step_mm: float = DEFAULT_REPAIR_STEP_MM,
) -> dict:
    ready_cases = [row for row in case_rows if boolish(row.get("direct_fixed_radius_pilot_ready"))]
    overlap_cases = [row for row in case_rows if safe_int(row.get("overlapping_pair_count"), 0) > 0]
    repairable = [row for row in overlap_cases if boolish(row.get("repair_within_default_step"))]
    close14_rows = [row for row in case_rows if row.get("branch_key") == "target2_close14"]
    close50_rows = [row for row in case_rows if row.get("branch_key") == "target2_close50_linear29p5"]
    close14_ready = [row for row in close14_rows if boolish(row.get("direct_fixed_radius_pilot_ready"))]
    close50_ready = [row for row in close50_rows if boolish(row.get("direct_fixed_radius_pilot_ready"))]
    min_clearance = min(safe_float(row.get("min_pair_clearance_mm"), math.inf) for row in case_rows)
    max_repair = max((safe_float(row.get("repair_required_mm"), 0.0) for row in overlap_cases), default=0.0)
    return {
        "policy_label": "local_2d_detector_exact_radius_seed_nonoverlap_preflight_cpu_no_fwi",
        "source_seed_export_policy_label": seed_summary.get("policy_label", ""),
        "source_prior_scope_policy_label": prior_summary.get("policy_label", ""),
        "stable_seed_case_count": len(case_rows),
        "component_pair_count": len(pair_rows),
        "direct_fixed_radius_pilot_ready_count": len(ready_cases),
        "overlap_blocked_case_count": len(overlap_cases),
        "repair_within_default_step_count": len(repairable),
        "repair_step_mm": float(repair_step_mm),
        "min_pair_clearance_mm": min_clearance,
        "max_repair_required_mm": max_repair,
        "close14_case_count": len(close14_rows),
        "close14_direct_ready_count": len(close14_ready),
        "close50_linear29p5_case_count": len(close50_rows),
        "close50_linear29p5_direct_ready_count": len(close50_ready),
        "all_stable_seeds_nonoverlap_ready": len(overlap_cases) == 0,
        "ready_for_direct_fixed_radius_pilot_subset": bool(ready_cases),
        "ready_for_seed_repair_audit": bool(overlap_cases),
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use only the direct-ready subset for any further narrow fixed-radius pilots. "
            "Exact radii make some stable detector seeds geometrically overlapping, so the "
            "remaining stable cases need a seed repair/preflight step before launch. This "
            "does not authorize broad GPU work, field transfer, detector-inferred radius/material, or FWI."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "direct_fixed_radius_pilot_subset",
            "ready": summary["ready_for_direct_fixed_radius_pilot_subset"],
            "allowed_use": "narrow one-case-at-a-time controlled fixed-radius pilots",
            "blocked_use": "all stable seeds without preflight",
            "evidence": (
                f"{summary['direct_fixed_radius_pilot_ready_count']}/"
                f"{summary['stable_seed_case_count']} stable seeds non-overlap-ready"
            ),
        },
        {
            "gate_key": "seed_repair_audit",
            "ready": summary["ready_for_seed_repair_audit"],
            "allowed_use": "CPU-side repair design before more GPU pilots",
            "blocked_use": "launch overlap-blocked seeds directly",
            "evidence": (
                f"overlap-blocked={summary['overlap_blocked_case_count']}; "
                f"max repair={summary['max_repair_required_mm']:.3f} mm"
            ),
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad fixed-radius refinement campaign",
            "evidence": "preflight finds overlap blockers and only one completed pilot so far",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "non-overlap preflight is not an FWI launch contract",
        },
    ]


def plot_preflight(case_rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(case_rows, key=lambda row: (row["branch_key"], safe_int(row["seed"], 0), row["case_variant"]))
    labels = [
        f"{row['branch_key'].replace('target2_', '')}\nseed{row['seed']} {row['case_variant'].replace('_', ' ')}"
        for row in ordered
    ]
    values = np.asarray([safe_float(row.get("min_pair_clearance_mm"), 0.0) for row in ordered], dtype=float)
    colors = ["#2f9d55" if value >= 0.0 else "#d6453d" for value in values]
    fig, ax = plt.subplots(figsize=(13.5, 5.8), constrained_layout=True)
    x = np.arange(len(ordered))
    ax.bar(x, values, color=colors, edgecolor="#333333", linewidth=0.5)
    ax.axhline(0.0, color="#111111", linewidth=1.1)
    ax.set_xticks(x, labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("minimum exact-radius pair clearance [mm]")
    ax.set_title("Exact-Radius Detector Seed Non-Overlap Preflight")
    ax.grid(axis="y", alpha=0.25)
    ax.text(
        0.01,
        0.97,
        (
            f"direct-ready={summary['direct_fixed_radius_pilot_ready_count']}/"
            f"{summary['stable_seed_case_count']} | "
            f"overlap-blocked={summary['overlap_blocked_case_count']} | "
            f"gpu={summary['gpu_priority']}"
        ),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
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
                "## `local_2d_detector_exact_radius_seed_nonoverlap_preflight.png`",
                "",
                "This figure checks whether stable detector-exported coordinate seeds",
                "remain physically non-overlapping when the controlled synthetic",
                "`5,6,8` mm radius prior is imposed.",
                "",
                f"Direct-ready stable seeds: `{summary['direct_fixed_radius_pilot_ready_count']}`.",
                f"Overlap-blocked stable seeds: `{summary['overlap_blocked_case_count']}`.",
                f"Maximum repair required: `{summary['max_repair_required_mm']:.3f}` mm.",
                "",
                "Scope boundary:",
                "",
                "This is a CPU preflight for future narrow synthetic fixed-radius",
                "pilots. It does not run FDTD/FWI, infer detector radii/materials,",
                "transfer to field data, or authorize broad GPU work.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--component-seed-run", default=DEFAULT_COMPONENT_SEED_RUN)
    parser.add_argument("--prior-scope-run", default=DEFAULT_PRIOR_SCOPE_RUN)
    parser.add_argument("--repair-step-mm", type=float, default=DEFAULT_REPAIR_STEP_MM)
    parser.add_argument("--run-name", default="local_2d_detector_exact_radius_seed_nonoverlap_preflight")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    summary_root = Path(args.summary_root)
    seed_dir = summary_root / args.component_seed_run
    prior_dir = summary_root / args.prior_scope_run
    seed_rows = read_csv_rows(seed_dir / "data/local_2d_detector_component_seed_rows.csv")
    seed_summary = read_json(seed_dir / "data/local_2d_detector_component_seed_export_summary.json")
    prior_rows = read_csv_rows(prior_dir / "data/local_2d_detector_radius_material_prior_scope_cases.csv")
    prior_summary = read_json(prior_dir / "data/local_2d_detector_radius_material_prior_scope_summary.json")

    case_rows, pair_rows = build_preflight_rows(seed_rows, prior_rows, repair_step_mm=args.repair_step_mm)
    summary = summarize_preflight(
        case_rows,
        pair_rows,
        seed_summary,
        prior_summary,
        repair_step_mm=args.repair_step_mm,
    )
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(summary_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    cases_csv = data_dir / "local_2d_detector_exact_radius_seed_nonoverlap_preflight_cases.csv"
    pairs_csv = data_dir / "local_2d_detector_exact_radius_seed_nonoverlap_preflight_pairs.csv"
    gates_csv = data_dir / "local_2d_detector_exact_radius_seed_nonoverlap_preflight_gates.csv"
    summary_json = data_dir / "local_2d_detector_exact_radius_seed_nonoverlap_preflight_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_exact_radius_seed_nonoverlap_preflight.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_preflight(case_rows, summary, figure_path)
    write_csv(cases_csv, [json_safe(row) for row in case_rows])
    write_csv(pairs_csv, [json_safe(row) for row in pair_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "cases_csv": str(cases_csv),
        "pairs_csv": str(pairs_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_component_seed_summary_json": str(seed_dir / "data/local_2d_detector_component_seed_export_summary.json"),
        "source_prior_scope_summary_json": str(prior_dir / "data/local_2d_detector_radius_material_prior_scope_summary.json"),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_exact_radius_seed_nonoverlap_preflight",
        {
            "component_seed_run": args.component_seed_run,
            "prior_scope_run": args.prior_scope_run,
            "repair_step_mm": args.repair_step_mm,
            "summary_json": str(summary_json),
            "cases_csv": str(cases_csv),
            "pairs_csv": str(pairs_csv),
            "gates_csv": str(gates_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
