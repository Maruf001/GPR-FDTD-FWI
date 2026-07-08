#!/usr/bin/env python3
"""Translate current GSSI field blockers into a controlled acquisition design."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BLOCKER_RUN = "136_gssi51600s_field_inversion_blocker_map_post_contrast"

DESIGN_REQUIREMENTS = {
    "leave_one_content_redundancy": {
        "priority": "should_have",
        "phase": "repeatability",
        "new_measurement": "collect at least three independent short-profile repeats per controlled target",
        "acceptance_gate": "content-backed timing interval survives leave-one-profile removal",
        "analysis_after_acquisition": "repeat run120/run121 leave-one ladder on controlled repeats",
        "paper_role": "robust field supplement, not inversion by itself",
    },
    "long_profile_transfer": {
        "priority": "optional_scope",
        "phase": "survey_scope",
        "new_measurement": "avoid mixing long and short profiles unless profile geometry is surveyed",
        "acceptance_gate": "long/short transfer residuals fall within the short-profile timing envelope",
        "analysis_after_acquisition": "rerun timing-envelope transfer only if geometry is controlled",
        "paper_role": "scope guardrail",
    },
    "profile_spatial_calibration": {
        "priority": "must_have",
        "phase": "geometry",
        "new_measurement": "survey profile starts, trace spacing, scan direction, and target x locations",
        "acceptance_gate": "one profile-to-target spatial translation has residual range below 5 mm",
        "analysis_after_acquisition": "rerun run122 spatial-consistency audit with surveyed positions",
        "paper_role": "minimum requirement for geometry seeding",
    },
    "absolute_time_zero": {
        "priority": "must_have",
        "phase": "timing",
        "new_measurement": "record a repeatable air/direct-wave or metal-plate timing reference per session",
        "acceptance_gate": "absolute time-zero uncertainty below 0.02 ns or explicitly propagated",
        "analysis_after_acquisition": "rerun time-zero ladder with absolute reference rows",
        "paper_role": "minimum requirement for calibrated depth/inversion",
    },
    "radius_seed_or_recovery": {
        "priority": "must_have",
        "phase": "target_truth",
        "new_measurement": "use targets with measured radius/diameter and fixed cover depth before scanning",
        "acceptance_gate": "known radius/diameter table exists before waveform fitting",
        "analysis_after_acquisition": "compare radius-sensitive objective margins against known target table",
        "paper_role": "minimum requirement for radius or geometry claims",
    },
    "absolute_amplitude_calibration": {
        "priority": "must_have",
        "phase": "amplitude",
        "new_measurement": "capture gain settings, antenna coupling state, reference reflector, and repeat amplitudes",
        "acceptance_gate": "reference-amplitude coefficient repeatability within 10 percent",
        "analysis_after_acquisition": "extend run131/run132 contrast checks with absolute reference amplitude",
        "paper_role": "minimum requirement for amplitude-driven inversion",
    },
    "cover_depth_recovery": {
        "priority": "must_have",
        "phase": "material_depth",
        "new_measurement": "measure cover depth and dielectric/velocity calibration for each target zone",
        "acceptance_gate": "depth/velocity calibration predicts two-way travel within 5 mm apparent-depth residual",
        "analysis_after_acquisition": "rerun apparent-depth and hyperbola/time-zero degeneracy audits with ground truth",
        "paper_role": "minimum requirement for cover-depth recovery",
    },
    "field_fwi": {
        "priority": "blocked_until_controls",
        "phase": "inversion",
        "new_measurement": "none for the current archive; first satisfy timing, geometry, radius, amplitude, and depth controls",
        "acceptance_gate": "all must-have acquisition controls pass before field FWI is queued",
        "analysis_after_acquisition": "only then design a small synthetic-to-field inversion pilot",
        "paper_role": "future controlled-validation step",
    },
    "field_3d_hpc": {
        "priority": "blocked_out_of_scope",
        "phase": "survey_scope",
        "new_measurement": "current archive is independent 2D line profiles; do not submit as 3D/HPC field workload",
        "acceptance_gate": "3D grid/C-scan geometry exists before any field 3D claim",
        "analysis_after_acquisition": "separate from this 2D field track if ever collected",
        "paper_role": "scope boundary",
    },
}


PRIORITY_SCORE = {
    "must_have": 4,
    "should_have": 3,
    "optional_scope": 2,
    "blocked_until_controls": 1,
    "blocked_out_of_scope": 0,
}


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def blocker_paths(dataset_root: Path, blocker_run: str) -> tuple[Path, Path]:
    data_dir = dataset_root / blocker_run / "data"
    return (
        data_dir / "field_inversion_blocker_map_rows.csv",
        data_dir / "field_inversion_blocker_map_summary.json",
    )


def build_design_rows(blocker_rows: list[dict]) -> list[dict]:
    rows = []
    for blocker in blocker_rows:
        if blocker.get("axis_family") != "blocker":
            continue
        axis_key = str(blocker.get("axis_key", ""))
        req = DESIGN_REQUIREMENTS.get(axis_key)
        if not req:
            continue
        rows.append({
            "axis_key": axis_key,
            "severity": blocker.get("severity", ""),
            "currently_ready": boolish(blocker.get("ready")),
            "current_metric_label": blocker.get("metric_label", ""),
            "current_metric_value": safe_float(blocker.get("metric_value"), math.nan),
            "current_metric_units": blocker.get("metric_units", ""),
            "current_evidence": blocker.get("evidence", ""),
            "priority": req["priority"],
            "priority_score": PRIORITY_SCORE[req["priority"]],
            "phase": req["phase"],
            "required_new_measurement": req["new_measurement"],
            "acceptance_gate": req["acceptance_gate"],
            "analysis_after_acquisition": req["analysis_after_acquisition"],
            "paper_role": req["paper_role"],
            "current_archive_action": "keep_qc_only" if not boolish(blocker.get("ready")) else "already_supported",
        })
    return sorted(rows, key=lambda row: (-safe_int(row.get("priority_score")), row["phase"], row["axis_key"]))


def phase_rows(design_rows: list[dict]) -> list[dict]:
    phases = sorted({str(row["phase"]) for row in design_rows})
    rows = []
    for phase in phases:
        group = [row for row in design_rows if row["phase"] == phase]
        rows.append({
            "phase": phase,
            "requirement_count": len(group),
            "must_have_count": sum(row["priority"] == "must_have" for row in group),
            "blocked_count": sum(str(row["priority"]).startswith("blocked") for row in group),
            "ready_count": sum(boolish(row.get("currently_ready")) for row in group),
            "actions": " | ".join(str(row["axis_key"]) for row in group),
        })
    return rows


def summarize_design(design_rows: list[dict], blocker_summary: dict) -> dict:
    must_have = [row for row in design_rows if row["priority"] == "must_have"]
    unresolved_must_have = [row for row in must_have if not boolish(row.get("currently_ready"))]
    return {
        "policy_label": "gssi51600s_controlled_field_acquisition_design_from_blockers",
        "design_requirement_count": len(design_rows),
        "must_have_requirement_count": len(must_have),
        "unresolved_must_have_requirement_count": len(unresolved_must_have),
        "critical_unresolved_blocker_count_from_source": safe_int(
            blocker_summary.get("critical_unresolved_blocker_count"), -1
        ),
        "current_archive_is_3d_survey": boolish(blocker_summary.get("is_3d_survey")),
        "current_archive_field_geometry_type": blocker_summary.get("field_geometry_type", ""),
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_new_controlled_2d_acquisition_design": len(unresolved_must_have) >= 5,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "recommended_next_field_mode": "controlled_2d_line_profile_validation_not_fwi",
        "decision": (
            "Use the current local GSSI archive as field morphology/timing QC only. "
            "A future controlled 2D field pass must first collect surveyed geometry, "
            "absolute timing, target radius/cover truth, dielectric/depth calibration, "
            "and amplitude-reference data before field inversion or heavy compute is justified."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "current_archive_field_fwi",
            "ready": summary["ready_for_current_archive_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI on current GSSI archive",
            "evidence": "must-have acquisition controls remain unresolved",
        },
        {
            "gate_key": "current_archive_heavy_field_work",
            "ready": summary["ready_for_current_archive_heavy_field_work"],
            "allowed_use": "none",
            "blocked_use": "broad local/GPU field inversion queue",
            "evidence": "current archive remains QC-only",
        },
        {
            "gate_key": "new_controlled_2d_acquisition_design",
            "ready": summary["ready_for_new_controlled_2d_acquisition_design"],
            "allowed_use": "plan measured controls for a future 2D validation pass",
            "blocked_use": "treat design as data or inversion result",
            "evidence": f"unresolved must-have requirements={summary['unresolved_must_have_requirement_count']}",
        },
        {
            "gate_key": "field_3d_hpc",
            "ready": summary["ready_for_field_3d_hpc"],
            "allowed_use": "none",
            "blocked_use": "3D/HPC field inversion from current archive",
            "evidence": f"geometry={summary['current_archive_field_geometry_type']}",
        },
    ]


def plot_design(design_rows: list[dict], phases: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 5.4), constrained_layout=True)

    labels = [str(row["axis_key"]).replace("_", "\n") for row in design_rows]
    scores = [safe_float(row.get("priority_score"), 0.0) for row in design_rows]
    colors = {
        "must_have": "#d95f02",
        "should_have": "#7570b3",
        "optional_scope": "#66a61e",
        "blocked_until_controls": "#b3b3b3",
        "blocked_out_of_scope": "#8c8c8c",
    }
    axes[0].bar(
        np.arange(len(design_rows)),
        scores,
        color=[colors.get(str(row["priority"]), "#999999") for row in design_rows],
        edgecolor="#333333",
        linewidth=0.4,
    )
    axes[0].set_xticks(np.arange(len(design_rows)), labels, rotation=35, ha="right")
    axes[0].set_yticks([0, 1, 2, 3, 4], ["out", "blocked", "optional", "should", "must"])
    axes[0].set_title("Acquisition controls by blocker")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    phase_labels = [str(row["phase"]).replace("_", "\n") for row in phases]
    req_counts = [safe_float(row.get("requirement_count"), 0.0) for row in phases]
    must_counts = [safe_float(row.get("must_have_count"), 0.0) for row in phases]
    x = np.arange(len(phases))
    axes[1].bar(x - 0.18, req_counts, width=0.36, label="requirements", color="#4e79a7")
    axes[1].bar(x + 0.18, must_counts, width=0.36, label="must-have", color="#d95f02")
    axes[1].set_xticks(x, phase_labels, rotation=25, ha="right")
    axes[1].set_title("Requirements by acquisition phase")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(loc="upper right", fontsize=8)
    axes[1].text(
        0.03,
        0.95,
        f"new 2D design ready: {summary['ready_for_new_controlled_2d_acquisition_design']}\n"
        f"current archive FWI: {summary['ready_for_current_archive_field_fwi']}\n"
        f"3D/HPC field: {summary['ready_for_field_3d_hpc']}\n"
        f"gpu: {summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Controlled Field Acquisition Design from Current GSSI Blockers", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_controlled_acquisition_design.png`",
                "",
                "This figure translates the current GSSI 51600S inversion blockers into",
                "a controlled future 2D acquisition design matrix.",
                "",
                f"Design requirements: `{summary['design_requirement_count']}`.",
                f"Must-have requirements: `{summary['must_have_requirement_count']}`.",
                f"Unresolved must-have requirements: `{summary['unresolved_must_have_requirement_count']}`.",
                f"Current archive field FWI ready: `{summary['ready_for_current_archive_field_fwi']}`.",
                f"Current archive heavy field work ready: `{summary['ready_for_current_archive_heavy_field_work']}`.",
                f"Field 3D/HPC ready: `{summary['ready_for_field_3d_hpc']}`.",
                "",
                "Scope boundary:",
                "",
                "This is an acquisition-design scorecard from saved blocker rows. It",
                "does not run field FWI, launch GPU/HPC work, or convert the current",
                "archive into calibrated inversion data.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--blocker-run", default=DEFAULT_BLOCKER_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_controlled_acquisition_design")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    blocker_rows_path, blocker_summary_path = blocker_paths(Path(dataset_root), args.blocker_run)
    blocker_rows = read_csv_rows(blocker_rows_path)
    blocker_summary = read_json(blocker_summary_path)

    design_rows = build_design_rows(blocker_rows)
    phases = phase_rows(design_rows)
    summary = summarize_design(design_rows, blocker_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=dataset_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    design_csv = data_dir / "field_controlled_acquisition_design_rows.csv"
    phase_csv = data_dir / "field_controlled_acquisition_design_phases.csv"
    gates_csv = data_dir / "field_controlled_acquisition_design_gates.csv"
    summary_json = data_dir / "field_controlled_acquisition_design_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_controlled_acquisition_design.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(design_csv, [json_safe(row) for row in design_rows])
    write_csv(phase_csv, [json_safe(row) for row in phases])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_design(design_rows, phases, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    summary["paths"] = {
        "design_rows_csv": str(design_csv),
        "phase_rows_csv": str(phase_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_blocker_rows_csv": str(blocker_rows_path),
        "source_blocker_summary_json": str(blocker_summary_path),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_controlled_acquisition_design",
        {
            "dataset_id": args.dataset_id,
            "blocker_run": args.blocker_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
