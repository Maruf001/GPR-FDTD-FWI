#!/usr/bin/env python3
"""Synthesize current GSSI field evidence into inversion/HPC readiness gates."""

from __future__ import annotations

import argparse
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_APPARENT_DEPTH_RUN = "084_gssi51600s_field_apparent_depth_qc"
DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN = "085_gssi51600s_field_apparent_depth_sensitivity"
DEFAULT_HYPERBOLA_DEGENERACY_RUN = "086_gssi51600s_field_hyperbola_timezero_degeneracy_audit"
DEFAULT_CUE_TIMING_RUN = "115_gssi51600s_field_cue_timing_envelope_post_cue_support_catalog"
DEFAULT_SPATIAL_TRANSFER_RUN = "116_gssi51600s_field_spatial_transfer_audit_post_timing_envelope"
DEFAULT_ANCHOR_INTERVAL_RUN = "117_gssi51600s_field_anchor_interval_reconciliation_post_spatial_transfer"
DEFAULT_DIMENSIONALITY_RUN = "118_gssi51600s_field_hpc_dimensionality_decision_card_post_anchor_interval"
DEFAULT_TIME_ZERO_LADDER_RUN = "121_gssi51600s_field_time_zero_ladder_post_leave_one"
DEFAULT_SPATIAL_CONSISTENCY_RUN = "122_gssi51600s_field_short_anchor_spatial_consistency_audit"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_float(value: object, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def gate_row(
    gate_key: str,
    status: str,
    ready: bool,
    allowed_use: str,
    blocked_use: str,
    evidence: str,
    limiting_metric: str,
    source_run: str,
) -> dict:
    return {
        "gate_key": gate_key,
        "status": status,
        "ready": ready,
        "allowed_use": allowed_use,
        "blocked_use": blocked_use,
        "evidence": evidence,
        "limiting_metric": limiting_metric,
        "source_run": source_run,
    }


def build_readiness_rows(
    apparent_depth: dict,
    apparent_sensitivity: dict,
    hyperbola_degeneracy: dict,
    cue_timing: dict,
    spatial_transfer: dict,
    anchor_interval: dict,
    dimensionality: dict,
    time_zero_ladder: dict,
    spatial_consistency: dict,
) -> list[dict]:
    rows = [
        gate_row(
            "short_relative_timing_qc",
            "supported",
            bool(time_zero_ladder.get("ready_for_short_relative_timing_qc", False))
            and bool(anchor_interval.get("ready_for_short_relative_timing_qc", False))
            and bool(spatial_consistency.get("ready_for_short_relative_timing_qc", False)),
            "short-profile relative timing and visual QC",
            "absolute time-zero or calibrated inversion",
            (
                f"short anchors inside intervals={anchor_interval.get('short_anchor_inside_supported_interval_count', 0)}; "
                f"content half-range={safe_float(time_zero_ladder.get('content_only_offset_half_range_ns'), 0.0):.6f} ns"
            ),
            "short anchors supported; no absolute time-zero",
            "117,121,122",
        ),
        gate_row(
            "apparent_depth_scale_qc",
            "supported_qc_only",
            bool(apparent_depth.get("ready_for_apparent_depth_scale_qc", False))
            and bool(apparent_sensitivity.get("all_residuals_within_budget_all_scenarios", False)),
            "apparent-depth scale sanity check for short-profile QC",
            "cover-depth or radius recovery",
            (
                f"corrected residual max={safe_float(apparent_depth.get('max_corrected_depth_residual_mm'), 0.0):.3f} mm; "
                f"budget={safe_float(apparent_depth.get('time_zero_depth_equivalent_mm'), 0.0):.3f} mm"
            ),
            "depth scale is dielectric/time-zero dependent",
            "084,085",
        ),
        gate_row(
            "long_profile_transfer",
            "blocked",
            bool(cue_timing.get("ready_for_long_short_transfer", False))
            and bool(spatial_transfer.get("ready_for_short_to_long_timing_transfer", False)),
            "none beyond long-profile pattern context",
            "short-to-long timing transfer",
            (
                f"long timing rejections={cue_timing.get('long_pattern_reject_short_transfer_count', 0)}; "
                f"long anchors near short content={spatial_transfer.get('long_pattern_with_nearest_short_content_within_threshold_count', 0)}"
            ),
            "timing and spatial coverage reject transfer",
            "115,116",
        ),
        gate_row(
            "profile_spatial_calibration",
            "blocked",
            bool(spatial_consistency.get("ready_for_profile_spatial_calibration", False)),
            "none beyond short-profile visual/timing QC",
            "single calibrated profile-to-profile spatial translation",
            (
                f"content residual range={safe_float(spatial_consistency.get('content_residual_range_mm'), 0.0):.3f} mm; "
                f"min margin={safe_float(spatial_consistency.get('content_min_supported_interval_margin_mm'), 0.0):.3f} mm"
            ),
            "signed residuals do not support one translation",
            "122",
        ),
        gate_row(
            "cover_depth_recovery",
            "blocked",
            bool(apparent_depth.get("ready_for_cover_depth_recovery", False))
            and bool(apparent_sensitivity.get("cover_depth_claim_ready", False))
            and bool(hyperbola_degeneracy.get("cover_depth_claim_ready", False)),
            "none beyond apparent-depth scale QC",
            "calibrated cover-depth recovery",
            (
                f"max apparent-depth span={safe_float(apparent_sensitivity.get('max_apparent_depth_span_mm'), 0.0):.3f} mm; "
                f"factor={safe_float(apparent_sensitivity.get('max_apparent_depth_sensitivity_factor'), 0.0):.2f}x"
            ),
            "absolute depth is unstable across dielectric/time-zero assumptions",
            "084,085,086",
        ),
        gate_row(
            "radius_recovery",
            "blocked",
            bool(dimensionality.get("ready_for_radius_recovery", False))
            and bool(hyperbola_degeneracy.get("radius_claim_ready", False)),
            "none",
            "field radius recovery",
            (
                f"near-top epsr span={safe_float(hyperbola_degeneracy.get('max_near_top_epsr_span'), 0.0):.3f}; "
                f"time-zero span={safe_float(hyperbola_degeneracy.get('max_near_top_time_zero_span_ns'), 0.0):.3f} ns"
            ),
            "hyperbola/time-zero degeneracy remains too broad",
            "086,118",
        ),
        gate_row(
            "field_fwi",
            "blocked",
            bool(dimensionality.get("ready_for_field_fwi", False))
            and bool(time_zero_ladder.get("ready_for_field_fwi", False))
            and bool(spatial_consistency.get("ready_for_field_fwi", False)),
            "none",
            "field full-waveform inversion",
            (
                f"absolute t0={time_zero_ladder.get('ready_for_absolute_time_zero', False)}; "
                f"spatial calibration={spatial_consistency.get('ready_for_profile_spatial_calibration', False)}"
            ),
            "no absolute time-zero, spatial calibration, target labels, or radius/depth controls",
            "118,121,122",
        ),
        gate_row(
            "field_3d_hpc",
            "blocked",
            bool(dimensionality.get("ready_for_3d_hpc", False))
            and bool(spatial_consistency.get("ready_for_3d_hpc", False)),
            "none",
            "3D/HPC field inversion workload",
            (
                f"geometry={dimensionality.get('field_geometry_type', '')}; "
                f"is_3d={dimensionality.get('is_3d_survey', False)}"
            ),
            "dataset is independent 2D line profiles, not a 3D survey",
            "118,122",
        ),
    ]
    return rows


def summarize_readiness(
    rows: list[dict],
    apparent_depth: dict,
    apparent_sensitivity: dict,
    hyperbola_degeneracy: dict,
    dimensionality: dict,
    time_zero_ladder: dict,
    spatial_consistency: dict,
) -> dict:
    supported = [row for row in rows if row["ready"]]
    blocked = [row for row in rows if not row["ready"]]
    return {
        "policy_label": "gssi51600s_field_inversion_readiness_synthesis_short_qc_only",
        "gate_count": len(rows),
        "supported_gate_count": len(supported),
        "blocked_gate_count": len(blocked),
        "supported_gate_keys": ";".join(row["gate_key"] for row in supported),
        "blocked_gate_keys": ";".join(row["gate_key"] for row in blocked),
        "ready_for_short_relative_timing_qc": any(row["gate_key"] == "short_relative_timing_qc" and row["ready"] for row in rows),
        "ready_for_apparent_depth_scale_qc": any(row["gate_key"] == "apparent_depth_scale_qc" and row["ready"] for row in rows),
        "ready_for_long_profile_transfer": any(row["gate_key"] == "long_profile_transfer" and row["ready"] for row in rows),
        "ready_for_profile_spatial_calibration": any(row["gate_key"] == "profile_spatial_calibration" and row["ready"] for row in rows),
        "ready_for_cover_depth_recovery": any(row["gate_key"] == "cover_depth_recovery" and row["ready"] for row in rows),
        "ready_for_radius_recovery": any(row["gate_key"] == "radius_recovery" and row["ready"] for row in rows),
        "ready_for_field_fwi": any(row["gate_key"] == "field_fwi" and row["ready"] for row in rows),
        "ready_for_3d_hpc": any(row["gate_key"] == "field_3d_hpc" and row["ready"] for row in rows),
        "field_geometry_type": dimensionality.get("field_geometry_type", ""),
        "is_3d_survey": bool(dimensionality.get("is_3d_survey", False)),
        "profile_count": safe_float(dimensionality.get("profile_count"), 0.0),
        "short_time_zero_content_half_range_ns": safe_float(
            time_zero_ladder.get("content_only_offset_half_range_ns"), 0.0
        ),
        "spatial_content_residual_range_mm": safe_float(spatial_consistency.get("content_residual_range_mm"), 0.0),
        "spatial_content_residual_half_range_mm": safe_float(
            spatial_consistency.get("content_residual_half_range_mm"), 0.0
        ),
        "apparent_depth_max_span_mm": safe_float(apparent_sensitivity.get("max_apparent_depth_span_mm"), 0.0),
        "apparent_depth_sensitivity_factor": safe_float(
            apparent_sensitivity.get("max_apparent_depth_sensitivity_factor"), 0.0
        ),
        "hyperbola_max_near_top_epsr_span": safe_float(hyperbola_degeneracy.get("max_near_top_epsr_span"), 0.0),
        "hyperbola_max_near_top_time_zero_span_ns": safe_float(
            hyperbola_degeneracy.get("max_near_top_time_zero_span_ns"), 0.0
        ),
        "max_corrected_depth_residual_mm": safe_float(apparent_depth.get("max_corrected_depth_residual_mm"), 0.0),
        "time_zero_depth_equivalent_mm": safe_float(apparent_depth.get("time_zero_depth_equivalent_mm"), 0.0),
        "required_external_controls": (
            "survey_layout;absolute_time_zero;calibrated_dielectric;known_target_geometry;"
            "cover_depth_validation;radius_validation"
        ),
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "Use the local GSSI field data for short-profile timing/visual QC and apparent-depth scale checks only. "
            "Do not launch field FWI, calibrated cover-depth/radius recovery, 3D/HPC, or neural inversion from this "
            "archive without external survey layout, absolute timing/depth controls, and known target geometry."
        ),
    }


def plot_readiness(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["gate_key"].replace("_", "\n") for row in rows]
    values = [1 if row["ready"] else 0 for row in rows]
    colors = ["#59a14f" if row["ready"] else "#e15759" for row in rows]
    fig, ax = plt.subplots(figsize=(13.2, 5.1), constrained_layout=True)
    ax.bar(np.arange(len(rows)), values, color=colors)
    ax.set_xticks(np.arange(len(rows)), labels, fontsize=8)
    ax.set_yticks([0, 1], ["blocked", "supported"])
    ax.set_ylim(-0.15, 1.25)
    ax.set_title("GSSI field inversion/HPC readiness synthesis")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax.text(
        0.02,
        0.96,
        f"policy={summary['policy_label']}\n"
        f"supported={summary['supported_gate_count']}/{summary['gate_count']}\n"
        f"geometry={summary['field_geometry_type']}\n"
        f"depth span={summary['apparent_depth_max_span_mm']:.1f} mm ({summary['apparent_depth_sensitivity_factor']:.2f}x)\n"
        f"spatial residual range={summary['spatial_content_residual_range_mm']:.1f} mm\n"
        f"field FWI={summary['ready_for_field_fwi']} | 3D/HPC={summary['ready_for_3d_hpc']}",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_inversion_readiness_synthesis.png`",
                "",
                "This CPU-only figure consolidates current GSSI field QC evidence into",
                "inversion and HPC readiness gates.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Supported gates: `{summary['supported_gate_count']}` / `{summary['gate_count']}`.",
                f"Supported gate keys: `{summary['supported_gate_keys']}`.",
                f"Blocked gate keys: `{summary['blocked_gate_keys']}`.",
                f"Ready for short relative timing QC: `{summary['ready_for_short_relative_timing_qc']}`.",
                f"Ready for apparent-depth scale QC: `{summary['ready_for_apparent_depth_scale_qc']}`.",
                f"Ready for cover-depth recovery: `{summary['ready_for_cover_depth_recovery']}`.",
                f"Ready for radius recovery: `{summary['ready_for_radius_recovery']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"Ready for 3D/HPC: `{summary['ready_for_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Readiness rows: `{rows_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This synthesis reads saved field summaries only. It does not run FDTD,",
                "FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--apparent-depth-run", default=DEFAULT_APPARENT_DEPTH_RUN)
    parser.add_argument("--apparent-depth-sensitivity-run", default=DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN)
    parser.add_argument("--hyperbola-degeneracy-run", default=DEFAULT_HYPERBOLA_DEGENERACY_RUN)
    parser.add_argument("--cue-timing-run", default=DEFAULT_CUE_TIMING_RUN)
    parser.add_argument("--spatial-transfer-run", default=DEFAULT_SPATIAL_TRANSFER_RUN)
    parser.add_argument("--anchor-interval-run", default=DEFAULT_ANCHOR_INTERVAL_RUN)
    parser.add_argument("--dimensionality-run", default=DEFAULT_DIMENSIONALITY_RUN)
    parser.add_argument("--time-zero-ladder-run", default=DEFAULT_TIME_ZERO_LADDER_RUN)
    parser.add_argument("--spatial-consistency-run", default=DEFAULT_SPATIAL_CONSISTENCY_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_inversion_readiness_synthesis_post_spatial_consistency")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    apparent_depth_dir = field_root / args.apparent_depth_run
    apparent_sensitivity_dir = field_root / args.apparent_depth_sensitivity_run
    hyperbola_dir = field_root / args.hyperbola_degeneracy_run
    cue_timing_dir = field_root / args.cue_timing_run
    spatial_transfer_dir = field_root / args.spatial_transfer_run
    anchor_interval_dir = field_root / args.anchor_interval_run
    dimensionality_dir = field_root / args.dimensionality_run
    time_zero_ladder_dir = field_root / args.time_zero_ladder_run
    spatial_consistency_dir = field_root / args.spatial_consistency_run

    apparent_depth = read_json(apparent_depth_dir / "data/field_apparent_depth_qc_summary.json")
    apparent_sensitivity = read_json(
        apparent_sensitivity_dir / "data/field_apparent_depth_sensitivity_summary.json"
    )
    hyperbola_degeneracy = read_json(
        hyperbola_dir / "data/field_hyperbola_timezero_degeneracy_summary.json"
    )
    cue_timing = read_json(cue_timing_dir / "data/field_cue_timing_envelope_summary.json")
    spatial_transfer = read_json(spatial_transfer_dir / "data/field_spatial_transfer_audit_summary.json")
    anchor_interval = read_json(anchor_interval_dir / "data/field_anchor_interval_reconciliation_summary.json")
    dimensionality = read_json(dimensionality_dir / "data/field_hpc_dimensionality_decision_summary.json")
    time_zero_ladder = read_json(time_zero_ladder_dir / "data/field_time_zero_evidence_ladder_summary.json")
    spatial_consistency = read_json(
        spatial_consistency_dir / "data/field_short_anchor_spatial_consistency_summary.json"
    )

    rows = build_readiness_rows(
        apparent_depth,
        apparent_sensitivity,
        hyperbola_degeneracy,
        cue_timing,
        spatial_transfer,
        anchor_interval,
        dimensionality,
        time_zero_ladder,
        spatial_consistency,
    )
    summary = summarize_readiness(
        rows,
        apparent_depth,
        apparent_sensitivity,
        hyperbola_degeneracy,
        dimensionality,
        time_zero_ladder,
        spatial_consistency,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(field_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_inversion_readiness_synthesis_rows.csv"
    summary_json = data_dir / "field_inversion_readiness_synthesis_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_inversion_readiness_synthesis.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_readiness(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv)
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "source_apparent_depth_summary_json": str(apparent_depth_dir / "data/field_apparent_depth_qc_summary.json"),
        "source_apparent_depth_sensitivity_summary_json": str(
            apparent_sensitivity_dir / "data/field_apparent_depth_sensitivity_summary.json"
        ),
        "source_hyperbola_degeneracy_summary_json": str(
            hyperbola_dir / "data/field_hyperbola_timezero_degeneracy_summary.json"
        ),
        "source_cue_timing_summary_json": str(cue_timing_dir / "data/field_cue_timing_envelope_summary.json"),
        "source_spatial_transfer_summary_json": str(
            spatial_transfer_dir / "data/field_spatial_transfer_audit_summary.json"
        ),
        "source_anchor_interval_summary_json": str(
            anchor_interval_dir / "data/field_anchor_interval_reconciliation_summary.json"
        ),
        "source_dimensionality_summary_json": str(
            dimensionality_dir / "data/field_hpc_dimensionality_decision_summary.json"
        ),
        "source_time_zero_ladder_summary_json": str(
            time_zero_ladder_dir / "data/field_time_zero_evidence_ladder_summary.json"
        ),
        "source_spatial_consistency_summary_json": str(
            spatial_consistency_dir / "data/field_short_anchor_spatial_consistency_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_inversion_readiness_synthesis",
        {
            "dataset_id": args.dataset_id,
            "apparent_depth_run": args.apparent_depth_run,
            "apparent_depth_sensitivity_run": args.apparent_depth_sensitivity_run,
            "hyperbola_degeneracy_run": args.hyperbola_degeneracy_run,
            "cue_timing_run": args.cue_timing_run,
            "spatial_transfer_run": args.spatial_transfer_run,
            "anchor_interval_run": args.anchor_interval_run,
            "dimensionality_run": args.dimensionality_run,
            "time_zero_ladder_run": args.time_zero_ladder_run,
            "spatial_consistency_run": args.spatial_consistency_run,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
