#!/usr/bin/env python3
"""Quantify external time-zero reference requirements for local GSSI field work."""

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
from run_gssi_dzt_qc import C_M_PER_NS, DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_controlled_2d_acquisition_protocol import read_csv_rows  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_INVENTORY_RUN = "001_gssi51600s_dzt_qc"
DEFAULT_UNCERTAINTY_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_CONTROL_GAP_RUN = "139_gssi51600s_field_time_zero_control_gap_manifest"
DEFAULT_PACKET_VALIDATION_RUN = "144_gssi51600s_current_archive_packet_prefill_validation"
REFERENCE_UNCERTAINTY_GATE_NS = 0.02
REFERENCE_REPEAT_GATE = 3


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def field_paths(dataset_root: Path) -> dict[str, Path]:
    return {
        "inventory": dataset_root / DEFAULT_INVENTORY_RUN / "data/gssi_dzt_inventory.csv",
        "uncertainty_summary": dataset_root
        / DEFAULT_UNCERTAINTY_RUN
        / "data/field_time_zero_uncertainty_budget_summary.json",
        "control_gap_summary": dataset_root
        / DEFAULT_CONTROL_GAP_RUN
        / "data/field_time_zero_control_gap_summary.json",
        "packet_acceptance": dataset_root
        / DEFAULT_PACKET_VALIDATION_RUN
        / "data/controlled_2d_packet_acceptance_status.csv",
        "packet_summary": dataset_root
        / DEFAULT_PACKET_VALIDATION_RUN
        / "data/controlled_2d_packet_validation_summary.json",
    }


def consistent_dielectric(inventory_rows: list[dict]) -> float:
    values = {
        safe_float(row.get("dielectric"))
        for row in inventory_rows
        if math.isfinite(safe_float(row.get("dielectric")))
    }
    return values.pop() if len(values) == 1 else math.nan


def velocity_m_per_ns(epsr: float) -> float:
    if not math.isfinite(epsr) or epsr <= 0.0:
        return math.nan
    return C_M_PER_NS / math.sqrt(epsr)


def two_way_depth_error_mm(dt_ns: float, epsr: float) -> float:
    velocity = velocity_m_per_ns(epsr)
    if not math.isfinite(dt_ns) or not math.isfinite(velocity):
        return math.nan
    return 0.5 * velocity * abs(dt_ns) * 1000.0


def timing_error_for_depth_mm(depth_mm: float, epsr: float) -> float:
    velocity = velocity_m_per_ns(epsr)
    if not math.isfinite(depth_mm) or not math.isfinite(velocity) or velocity <= 0.0:
        return math.nan
    return 2.0 * (depth_mm / 1000.0) / velocity


def packet_gate_ready(acceptance_rows: list[dict], gate_key: str) -> bool:
    for row in acceptance_rows:
        if row.get("gate_key") == gate_key:
            return boolish(row.get("ready"))
    return False


def reference_count_from_evidence(acceptance_rows: list[dict]) -> int:
    for row in acceptance_rows:
        if row.get("gate_key") == "absolute_time_zero_references":
            evidence = str(row.get("evidence", ""))
            if "time_zero_reference_count=" in evidence:
                return safe_int(evidence.split("time_zero_reference_count=", 1)[1].split(";", 1)[0], 0)
    return 0


def requirement_rows(uncertainty_summary: dict, control_gap_summary: dict, epsr: float) -> list[dict]:
    rows = [
        {
            "requirement_key": "content_anchor_residual",
            "kind": "current_relative_evidence",
            "dt_ns": safe_float(uncertainty_summary.get("max_abs_content_anchor_residual_ns")),
            "depth_error_mm": two_way_depth_error_mm(
                safe_float(uncertainty_summary.get("max_abs_content_anchor_residual_ns")), epsr
            ),
            "ready": True,
            "allowed_use": "relative short-profile timing QC",
            "blocked_use": "absolute time-zero or calibrated depth",
        },
        {
            "requirement_key": "bootstrap_ci_half_width",
            "kind": "current_relative_evidence",
            "dt_ns": 0.5 * safe_float(uncertainty_summary.get("bootstrap_ci_width_ns")),
            "depth_error_mm": two_way_depth_error_mm(
                0.5 * safe_float(uncertainty_summary.get("bootstrap_ci_width_ns")), epsr
            ),
            "ready": True,
            "allowed_use": "relative timing uncertainty bound",
            "blocked_use": "absolute time-zero calibration",
        },
        {
            "requirement_key": "conservative_half_width",
            "kind": "current_relative_evidence",
            "dt_ns": safe_float(uncertainty_summary.get("conservative_half_width_ns")),
            "depth_error_mm": two_way_depth_error_mm(
                safe_float(uncertainty_summary.get("conservative_half_width_ns")), epsr
            ),
            "ready": True,
            "allowed_use": "conservative short-profile timing envelope",
            "blocked_use": "unpropagated field inversion",
        },
        {
            "requirement_key": "short_vs_early_conflict",
            "kind": "current_negative_control",
            "dt_ns": safe_float(control_gap_summary.get("short_vs_early_delta_ns")),
            "depth_error_mm": two_way_depth_error_mm(
                safe_float(control_gap_summary.get("short_vs_early_delta_ns")), epsr
            ),
            "ready": False,
            "allowed_use": "negative control separating relative content timing from early common-mode timing",
            "blocked_use": "using early/direct component as absolute time-zero",
        },
        {
            "requirement_key": "packet_reference_uncertainty_gate",
            "kind": "future_external_reference_requirement",
            "dt_ns": REFERENCE_UNCERTAINTY_GATE_NS,
            "depth_error_mm": two_way_depth_error_mm(REFERENCE_UNCERTAINTY_GATE_NS, epsr),
            "ready": False,
            "allowed_use": "future absolute time-zero gate if reference repeats are collected",
            "blocked_use": "current archive field FWI",
        },
    ]
    for depth_mm in (1.0, 2.0, 5.0, 10.0):
        rows.append(
            {
                "requirement_key": f"depth_error_{depth_mm:g}mm_equivalent",
                "kind": "derived_tolerance_reference",
                "dt_ns": timing_error_for_depth_mm(depth_mm, epsr),
                "depth_error_mm": depth_mm,
                "ready": False,
                "allowed_use": "planning threshold for external reference measurements",
                "blocked_use": "claiming this tolerance from the current archive",
            }
        )
    return rows


def gate_rows(rows: list[dict], packet_acceptance_rows: list[dict]) -> list[dict]:
    current_reference_count = reference_count_from_evidence(packet_acceptance_rows)
    current_ref_gate_ready = packet_gate_ready(packet_acceptance_rows, "absolute_time_zero_references")
    reference_gate = next(row for row in rows if row["requirement_key"] == "packet_reference_uncertainty_gate")
    return [
        {
            "gate_key": "external_reference_requirement_defined",
            "ready": True,
            "evidence": (
                f"required_repeats={REFERENCE_REPEAT_GATE}; uncertainty_gate_ns="
                f"{REFERENCE_UNCERTAINTY_GATE_NS}; depth_error_mm={reference_gate['depth_error_mm']:.6g}"
            ),
            "blocked_use": "none",
        },
        {
            "gate_key": "current_archive_absolute_time_zero",
            "ready": current_ref_gate_ready,
            "evidence": f"current_time_zero_reference_count={current_reference_count}",
            "blocked_use": "absolute time-zero, calibrated depth, field FWI",
        },
        {
            "gate_key": "current_archive_field_fwi_or_heavy_work",
            "ready": False,
            "evidence": "reference requirement is quantified but not satisfied by current archive",
            "blocked_use": "field FWI, heavy field GPU work, field 3D/HPC",
        },
    ]


def summarize(rows: list[dict], gates: list[dict], epsr: float, packet_summary: dict) -> dict:
    reference_gate = next(row for row in rows if row["requirement_key"] == "packet_reference_uncertainty_gate")
    conservative = next(row for row in rows if row["requirement_key"] == "conservative_half_width")
    conflict = next(row for row in rows if row["requirement_key"] == "short_vs_early_conflict")
    return {
        "policy_label": "gssi51600s_field_time_zero_reference_requirement",
        "requirement_row_count": len(rows),
        "gate_count": len(gates),
        "dielectric_epsr": epsr,
        "velocity_m_per_ns": velocity_m_per_ns(epsr),
        "reference_repeat_gate": REFERENCE_REPEAT_GATE,
        "reference_uncertainty_gate_ns": REFERENCE_UNCERTAINTY_GATE_NS,
        "reference_uncertainty_gate_depth_error_mm": reference_gate["depth_error_mm"],
        "conservative_half_width_depth_error_mm": conservative["depth_error_mm"],
        "short_vs_early_conflict_depth_shift_mm": conflict["depth_error_mm"],
        "current_packet_time_zero_reference_ready": any(
            row["gate_key"] == "current_archive_absolute_time_zero" and boolish(row["ready"]) for row in gates
        ),
        "current_packet_blocking_findings": packet_summary.get("blocking_finding_count"),
        "ready_for_reference_collection": True,
        "ready_for_current_archive_absolute_time_zero": False,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "The external reference requirement is now quantified: collect at least three air/direct-wave "
            "or metal-plate timing references with uncertainty at or below 0.02 ns, equivalent to about "
            f"{reference_gate['depth_error_mm']:.2f} mm two-way depth error at epsr={epsr:g}. The current "
            "archive has zero such references, so absolute time-zero, calibrated depth, field FWI, heavy "
            "field GPU work, and field 3D/HPC remain blocked."
        ),
    }


def plot_requirements(rows: list[dict], save_path: Path) -> str:
    selected = [
        row
        for row in rows
        if row["requirement_key"]
        in {
            "content_anchor_residual",
            "bootstrap_ci_half_width",
            "conservative_half_width",
            "short_vs_early_conflict",
            "packet_reference_uncertainty_gate",
        }
    ]
    labels = [row["requirement_key"].replace("_", "\n") for row in selected]
    dt_values = [safe_float(row["dt_ns"], 0.0) for row in selected]
    depth_values = [safe_float(row["depth_error_mm"], 0.0) for row in selected]
    x = np.arange(len(selected))
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 5.0), constrained_layout=True)
    axes[0].bar(x, dt_values, color="#4e79a7")
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylabel("timing uncertainty / delta (ns)")
    axes[0].set_title("Timing scale")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, depth_values, color="#f28e2b")
    axes[1].set_xticks(x, labels, fontsize=8)
    axes[1].set_ylabel("two-way depth equivalent (mm)")
    axes[1].set_title("Depth-equivalent scale")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle("GSSI Field Time-Zero Reference Requirement", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_time_zero_reference_requirement")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = field_paths(dataset_root)
    inventory_rows = read_csv_rows(paths["inventory"])
    uncertainty_summary = read_json(paths["uncertainty_summary"])
    control_gap_summary = read_json(paths["control_gap_summary"])
    packet_acceptance_rows = read_csv_rows(paths["packet_acceptance"])
    packet_summary = read_json(paths["packet_summary"])
    epsr = consistent_dielectric(inventory_rows)
    rows = requirement_rows(uncertainty_summary, control_gap_summary, epsr)
    gates = gate_rows(rows, packet_acceptance_rows)
    summary = summarize(rows, gates, epsr, packet_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_time_zero_reference_requirement_rows.csv"
    gates_csv = data_dir / "field_time_zero_reference_requirement_gates.csv"
    summary_json = data_dir / "field_time_zero_reference_requirement_summary.json"
    figure_path = figures_dir / "field_time_zero_reference_requirement.png"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_requirements(rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
        "source_paths": {key: str(value) for key, value in paths.items()},
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_time_zero_reference_requirement",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "gates_csv": str(gates_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
