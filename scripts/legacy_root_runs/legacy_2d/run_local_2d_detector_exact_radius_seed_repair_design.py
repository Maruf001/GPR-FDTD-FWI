#!/usr/bin/env python3
"""Design truth-free exact-radius repairs for overlapping detector seeds."""

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
from run_local_2d_detector_exact_radius_seed_nonoverlap_preflight import (  # noqa: E402
    DEFAULT_REPAIR_STEP_MM,
    format_values,
    pair_clearance_rows,
)
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PREFLIGHT_RUN = "091_local_2d_detector_exact_radius_seed_nonoverlap_preflight"
DEFAULT_OFFSET_VALUES_MM = "-2:2:2"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float_list(text: str) -> list[float]:
    return [float(part.strip()) for part in str(text).split(",") if part.strip()]


def ordered_by_x(x_values: list[float], *, min_gap_mm: float = 0.0) -> bool:
    return all(float(left) + float(min_gap_mm) <= float(right) for left, right in zip(x_values, x_values[1:]))


def geometry_min_clearance(x_values: list[float], z_values: list[float], radii: list[float]) -> float:
    return min(
        safe_float(row.get("clearance_mm"))
        for row in pair_clearance_rows("candidate", x_values, z_values, radii)
    )


def shifted_values(values: list[float], offsets: tuple[float, ...]) -> list[float]:
    return [float(value) + float(offset) for value, offset in zip(values, offsets)]


def find_repair_candidate(
    x_seed: list[float],
    z_seed: list[float],
    radii: list[float],
    offsets_mm: list[float],
) -> dict:
    best: dict | None = None
    component_count = len(radii)
    for x_offsets in itertools.product(offsets_mm, repeat=component_count):
        repaired_x = shifted_values(x_seed, x_offsets)
        if not ordered_by_x(repaired_x):
            continue
        for z_offsets in itertools.product(offsets_mm, repeat=component_count):
            repaired_z = shifted_values(z_seed, z_offsets)
            min_clearance = geometry_min_clearance(repaired_x, repaired_z, radii)
            if min_clearance < -1.0e-9:
                continue
            shifts = [
                math.hypot(float(x_offsets[idx]), float(z_offsets[idx]))
                for idx in range(component_count)
            ]
            max_shift = max(shifts)
            l2_shift = math.sqrt(sum(value * value for value in shifts))
            shifted_component_count = sum(value > 1.0e-9 for value in shifts)
            candidate = {
                "repaired_x_values_mm": repaired_x,
                "repaired_z_values_mm": repaired_z,
                "x_offsets_mm": [float(value) for value in x_offsets],
                "z_offsets_mm": [float(value) for value in z_offsets],
                "min_pair_clearance_after_repair_mm": min_clearance,
                "max_component_shift_mm": max_shift,
                "l2_component_shift_mm": l2_shift,
                "shifted_component_count": shifted_component_count,
            }
            sort_key = (
                max_shift,
                l2_shift,
                shifted_component_count,
                -min_clearance,
                candidate["repaired_x_values_mm"],
                candidate["repaired_z_values_mm"],
            )
            if best is None or sort_key < best["_sort_key"]:
                best = {**candidate, "_sort_key": sort_key}
    if best is None:
        return {}
    best.pop("_sort_key", None)
    return best


def build_repair_rows(case_rows: list[dict], offsets_mm: list[float]) -> list[dict]:
    rows: list[dict] = []
    for row in case_rows:
        if safe_int(row.get("overlapping_pair_count"), 0) <= 0:
            continue
        x_seed = parse_float_list(str(row.get("x_seed_values_mm", "")))
        z_seed = parse_float_list(str(row.get("z_seed_values_mm", "")))
        radii = parse_float_list(str(row.get("exact_radius_values_mm", "")))
        repair = find_repair_candidate(x_seed, z_seed, radii, offsets_mm)
        ready = bool(repair)
        rows.append(
            {
                "case_label": row.get("case_label", ""),
                "branch_key": row.get("branch_key", ""),
                "seed": safe_int(row.get("seed"), 0),
                "case_variant": row.get("case_variant", ""),
                "overlapping_pair_keys": row.get("overlapping_pair_keys", ""),
                "min_pair_clearance_before_repair_mm": safe_float(row.get("min_pair_clearance_mm")),
                "repair_required_before_mm": safe_float(row.get("repair_required_mm")),
                "repair_search_offsets_mm": format_values(offsets_mm),
                "repair_found": ready,
                "repaired_x_values_mm": format_values(repair.get("repaired_x_values_mm", [])) if ready else "",
                "repaired_z_values_mm": format_values(repair.get("repaired_z_values_mm", [])) if ready else "",
                "x_offsets_mm": format_values(repair.get("x_offsets_mm", [])) if ready else "",
                "z_offsets_mm": format_values(repair.get("z_offsets_mm", [])) if ready else "",
                "min_pair_clearance_after_repair_mm": safe_float(
                    repair.get("min_pair_clearance_after_repair_mm"),
                    math.nan,
                ),
                "max_component_shift_mm": safe_float(repair.get("max_component_shift_mm"), math.nan),
                "l2_component_shift_mm": safe_float(repair.get("l2_component_shift_mm"), math.nan),
                "shifted_component_count": safe_int(repair.get("shifted_component_count"), 0),
                "ready_for_repaired_fixed_radius_pilot": ready,
                "ready_for_detector_seeded_fwi": False,
                "allowed_use": "truth-free geometric repair candidate before a narrow fixed-radius pilot",
                "blocked_use": "truth-selected repair, broad GPU queue, detector-inferred radius/material, FWI launch",
            }
        )
    return rows


def summarize_repairs(repair_rows: list[dict], preflight_summary: dict) -> dict:
    found = [row for row in repair_rows if boolish(row.get("repair_found"))]
    max_shift = max((safe_float(row.get("max_component_shift_mm"), 0.0) for row in found), default=0.0)
    min_after = min(
        (safe_float(row.get("min_pair_clearance_after_repair_mm"), math.inf) for row in found),
        default=math.inf,
    )
    return {
        "policy_label": "local_2d_detector_exact_radius_seed_repair_design_cpu_no_fwi",
        "source_preflight_policy_label": preflight_summary.get("policy_label", ""),
        "overlap_blocked_case_count": len(repair_rows),
        "repair_found_count": len(found),
        "all_overlap_blocked_cases_repairable": len(found) == len(repair_rows) and bool(repair_rows),
        "max_component_shift_mm": max_shift,
        "min_pair_clearance_after_repair_mm": min_after if math.isfinite(min_after) else math.nan,
        "ready_for_repaired_fixed_radius_pilot_subset": bool(found),
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use these truth-free geometric repairs only as preflight candidates for "
            "future one-case-at-a-time fixed-radius pilots. They do not validate the "
            "repaired seeds against waveform objectives and do not authorize broad GPU work or FWI."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "repaired_fixed_radius_pilot_subset",
            "ready": summary["ready_for_repaired_fixed_radius_pilot_subset"],
            "allowed_use": "one-case-at-a-time fixed-radius pilot after repair",
            "blocked_use": "claim repaired seeds are waveform validated",
            "evidence": f"repair found={summary['repair_found_count']}/{summary['overlap_blocked_case_count']}",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch all repaired seeds or a broad fixed-radius campaign",
            "evidence": "repair design is geometric only",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "repair design is not an FWI launch contract",
        },
    ]


def plot_repairs(repair_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"seed{row['seed']}\n{row['case_variant'].replace('_', ' ')}" for row in repair_rows]
    before = np.asarray([safe_float(row.get("min_pair_clearance_before_repair_mm"), 0.0) for row in repair_rows])
    after = np.asarray([safe_float(row.get("min_pair_clearance_after_repair_mm"), 0.0) for row in repair_rows])
    x = np.arange(len(repair_rows))
    fig, ax = plt.subplots(figsize=(9.8, 5.0), constrained_layout=True)
    width = 0.36
    ax.bar(x - width / 2, before, width=width, color="#d6453d", label="before repair")
    ax.bar(x + width / 2, after, width=width, color="#2f9d55", label="after repair")
    ax.axhline(0.0, color="#111111", linewidth=1.0)
    ax.set_xticks(x, labels)
    ax.set_ylabel("minimum exact-radius pair clearance [mm]")
    ax.set_title("Exact-Radius Seed Repair Design")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="best")
    ax.text(
        0.01,
        0.97,
        f"repairable={summary['repair_found_count']}/{summary['overlap_blocked_case_count']} | gpu=none",
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
                "## `local_2d_detector_exact_radius_seed_repair_design.png`",
                "",
                "This figure compares exact-radius pair clearance before and after",
                "truth-free geometric seed repairs for the overlap-blocked stable",
                "detector seeds.",
                "",
                f"Repairable cases: `{summary['repair_found_count']}` / `{summary['overlap_blocked_case_count']}`.",
                f"Max component shift: `{summary['max_component_shift_mm']:.3f}` mm.",
                "",
                "Scope boundary:",
                "",
                "This is a geometry-only repair design. It does not run FDTD/FWI,",
                "validate repaired seeds by waveform objective, infer radii/materials,",
                "or authorize broad GPU work.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--preflight-run", default=DEFAULT_PREFLIGHT_RUN)
    parser.add_argument("--repair-offsets-mm", type=parse_values_mm, default=parse_values_mm(DEFAULT_OFFSET_VALUES_MM))
    parser.add_argument("--run-name", default="local_2d_detector_exact_radius_seed_repair_design")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    summary_root = Path(args.summary_root)
    preflight_dir = summary_root / args.preflight_run
    case_rows = read_csv_rows(
        preflight_dir / "data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_cases.csv"
    )
    preflight_summary = read_json(
        preflight_dir / "data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_summary.json"
    )
    repair_rows = build_repair_rows(case_rows, list(args.repair_offsets_mm))
    summary = summarize_repairs(repair_rows, preflight_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(summary_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    repairs_csv = data_dir / "local_2d_detector_exact_radius_seed_repair_design_rows.csv"
    gates_csv = data_dir / "local_2d_detector_exact_radius_seed_repair_design_gates.csv"
    summary_json = data_dir / "local_2d_detector_exact_radius_seed_repair_design_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_exact_radius_seed_repair_design.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_repairs(repair_rows, summary, figure_path)
    write_csv(repairs_csv, [json_safe(row) for row in repair_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "repairs_csv": str(repairs_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_preflight_summary_json": str(
            preflight_dir / "data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_summary.json"
        ),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_exact_radius_seed_repair_design",
        {
            "preflight_run": args.preflight_run,
            "repair_offsets_mm": list(args.repair_offsets_mm),
            "summary_json": str(summary_json),
            "repairs_csv": str(repairs_csv),
            "gates_csv": str(gates_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
