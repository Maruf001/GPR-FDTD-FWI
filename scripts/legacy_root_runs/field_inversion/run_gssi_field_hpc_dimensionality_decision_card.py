#!/usr/bin/env python3
"""Consolidate local GSSI field dimensionality and HPC readiness decisions."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SURVEY_RUN = "015_gssi51600s_survey_geometry_audit"
DEFAULT_READINESS_RUN = "081_gssi51600s_field_acquisition_readiness_audit"
DEFAULT_TIMING_RUN = "105_gssi51600s_field_timing_discriminant_scorecard"
DEFAULT_CLAIM_SUMMARY_RUN = "013_local_gssi_field_claim_viability_scorecard_post_timing_discriminant"
DEFAULT_TIMING_ENVELOPE_RUN = "115_gssi51600s_field_cue_timing_envelope_post_cue_support_catalog"
DEFAULT_SPATIAL_TRANSFER_RUN = "116_gssi51600s_field_spatial_transfer_audit_post_timing_envelope"
DEFAULT_ANCHOR_INTERVAL_RUN = "117_gssi51600s_field_anchor_interval_reconciliation_post_spatial_transfer"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def decision_row(
    *,
    gate_key: str,
    decision: str,
    status: str,
    evidence: str,
    allowed_use: str,
    blocked_use: str,
    readiness_score: float,
) -> dict:
    return {
        "gate_key": gate_key,
        "decision": decision,
        "status": status,
        "evidence": evidence,
        "allowed_use": allowed_use,
        "blocked_use": blocked_use,
        "readiness_score": float(readiness_score),
    }


def build_decision_rows(
    *,
    survey: dict,
    readiness: dict,
    timing: dict,
    claims: dict,
    timing_envelope: dict | None = None,
    spatial_transfer: dict | None = None,
    anchor_interval: dict | None = None,
) -> list[dict]:
    timing_envelope = timing_envelope or {}
    spatial_transfer = spatial_transfer or {}
    anchor_interval = anchor_interval or {}
    is_3d = str(survey.get("classification", "")) != "independent_2d_line_profiles"
    ready_3d = bool(readiness.get("ready_for_3d_hpc")) and is_3d
    ready_fwi = bool(readiness.get("ready_for_field_fwi")) and bool(claims.get("ready_for_field_fwi"))
    ready_abs_t0 = bool(claims.get("ready_for_absolute_time_zero")) and not bool(
        timing.get("early_has_low_uniqueness_margin")
    )
    short_qc_ready = bool(timing_envelope.get("ready_for_short_relative_timing_qc")) and bool(
        anchor_interval.get("ready_for_short_relative_timing_qc")
    )
    transfer_ready = bool(timing_envelope.get("ready_for_long_short_transfer")) and bool(
        spatial_transfer.get("ready_for_short_to_long_timing_transfer")
    )
    return [
        decision_row(
            gate_key="survey_dimensionality",
            decision="2d_line_profiles_only" if not is_3d else "review_3d_geometry",
            status="blocks_3d_hpc" if not is_3d else "review",
            evidence=(
                f"classification={survey.get('classification', '')}; "
                f"profiles={survey.get('profile_count', '')}; "
                f"crossline_file={bool(survey.get('has_crossline_file'))}; "
                f"reliable_waypoints={bool(survey.get('has_reliable_waypoint_lengths'))}"
            ),
            allowed_use="independent 2D line-profile timing and visual QC",
            blocked_use="3D survey, 3D inversion, volumetric field benchmark",
            readiness_score=0.0 if not is_3d else 0.5,
        ),
        decision_row(
            gate_key="alongline_sampling",
            decision="supports_2d_qc",
            status="ready_for_2d_qc",
            evidence=(
                f"scan_spacing={safe_float(readiness.get('scan_spacing_mm')):.3f} mm; "
                f"lambda={safe_float(readiness.get('center_wavelength_mm')):.3f} mm; "
                f"samples_per_lambda={safe_float(readiness.get('samples_per_wavelength')):.3f}"
            ),
            allowed_use="dense along-line B-scan timing/repeatability QC",
            blocked_use="crossline interpolation or 3D reconstruction",
            readiness_score=1.0,
        ),
        decision_row(
            gate_key="timing_anchor_scope",
            decision="relative_not_absolute",
            status="blocks_absolute_time_zero" if not ready_abs_t0 else "review",
            evidence=(
                f"short_offset={safe_float(timing.get('short_nominal_offset_ns')):.6f} ns; "
                f"early_min_margin={safe_float(timing.get('early_min_uniqueness_margin')):.6e}; "
                f"long_short_separation={safe_float(timing.get('long_best_offset_distance_from_short_ns')):.6f} ns"
            ),
            allowed_use="relative short-pair timing and timing-boundary wording",
            blocked_use="absolute time-zero, calibrated cover-depth, field FWI",
            readiness_score=0.45 if not ready_abs_t0 else 0.8,
        ),
        decision_row(
            gate_key="short_profile_timing_support",
            decision="short_relative_qc_supported" if short_qc_ready else "short_timing_review",
            status="ready_for_short_qc" if short_qc_ready else "review",
            evidence=(
                f"timing_inside={safe_float(timing_envelope.get('short_anchor_inside_envelope_count'), 0):.0f}/"
                f"{safe_float(timing_envelope.get('short_anchor_count'), 0):.0f}; "
                f"interval_inside={safe_float(anchor_interval.get('short_anchor_inside_supported_interval_count'), 0):.0f}/"
                f"{safe_float(anchor_interval.get('short_anchor_count'), 0):.0f}; "
                f"min_interval_margin={safe_float(anchor_interval.get('min_margin_to_supported_interval_edge_mm'), 0):.3f} mm"
            ),
            allowed_use="short-profile relative timing and supported-interval visual QC",
            blocked_use="absolute time-zero, cover-depth, radius, field FWI",
            readiness_score=0.85 if short_qc_ready else 0.35,
        ),
        decision_row(
            gate_key="long_profile_transfer_scope",
            decision="reject_short_to_long_transfer" if not transfer_ready else "review_transfer",
            status="blocks_long_transfer" if not transfer_ready else "review",
            evidence=(
                f"long_reject_count={safe_float(timing_envelope.get('long_pattern_reject_short_transfer_count'), 0):.0f}; "
                f"long_covered={safe_float(spatial_transfer.get('long_pattern_with_nearest_short_content_within_threshold_count'), 0):.0f}/"
                f"{safe_float(spatial_transfer.get('long_pattern_anchor_count'), 0):.0f}; "
                f"median_long_to_short={safe_float(spatial_transfer.get('median_long_to_short_distance_mm'), 0):.3f} mm"
            ),
            allowed_use="long-profile pattern context and transfer guardrail",
            blocked_use="applying short-profile timing to long profiles or field inversion",
            readiness_score=0.0 if not transfer_ready else 0.5,
        ),
        decision_row(
            gate_key="spatial_support_scope",
            decision="supported_intervals_only",
            status="scope_limited",
            evidence=(
                f"all_window_support={safe_float(readiness.get('spatial_all_window_supported_fraction')):.3f}; "
                f"columns={safe_float(readiness.get('spatial_all_window_supported_column_count')):.0f}/"
                f"{safe_float(readiness.get('spatial_finite_column_count')):.0f}"
            ),
            allowed_use="supported-interval visual QC",
            blocked_use="full-profile field inversion or interpretation outside support intervals",
            readiness_score=safe_float(readiness.get("spatial_all_window_supported_fraction"), 0.0),
        ),
        decision_row(
            gate_key="claim_viability",
            decision="2d_field_qc_only",
            status="ready_scoped_not_inversion",
            evidence=(
                f"supported={claims.get('supported_count', 0)}; "
                f"scope_limited={claims.get('scope_limited_count', 0)}; "
                f"blocked={claims.get('blocked_count', 0)}"
            ),
            allowed_use="field methods/QC context and timing-boundary evidence",
            blocked_use="field radius, cover-depth, 3D, HPC, or FWI validation claims",
            readiness_score=1.0 if bool(claims.get("ready_for_2d_field_qc")) else 0.0,
        ),
        decision_row(
            gate_key="field_hpc_fwi_gate",
            decision="do_not_submit_field_hpc_job" if not ready_3d and not ready_fwi else "review",
            status="blocked",
            evidence=(
                f"ready_3d_hpc={bool(readiness.get('ready_for_3d_hpc'))}; "
                f"ready_field_fwi={bool(readiness.get('ready_for_field_fwi'))}; "
                f"field_hpc_priority={readiness.get('field_hpc_priority', 'none')}"
            ),
            allowed_use="local CPU-side field QC synthesis only",
            blocked_use="NERSC/A100 field-data FWI or 3D job from this dataset",
            readiness_score=0.0,
        ),
    ]


def summarize_decision(
    rows: list[dict],
    survey: dict,
    readiness: dict,
    timing: dict,
    claims: dict,
    timing_envelope: dict | None = None,
    spatial_transfer: dict | None = None,
    anchor_interval: dict | None = None,
) -> dict:
    timing_envelope = timing_envelope or {}
    spatial_transfer = spatial_transfer or {}
    anchor_interval = anchor_interval or {}
    status_by_key = {row["gate_key"]: row["status"] for row in rows}
    is_3d = status_by_key.get("survey_dimensionality") != "blocks_3d_hpc"
    ready_3d = bool(readiness.get("ready_for_3d_hpc")) and is_3d
    ready_fwi = bool(readiness.get("ready_for_field_fwi")) and bool(claims.get("ready_for_field_fwi"))
    short_qc_ready = status_by_key.get("short_profile_timing_support") == "ready_for_short_qc"
    transfer_ready = status_by_key.get("long_profile_transfer_scope") != "blocks_long_transfer"
    return {
        "policy_label": "gssi51600s_field_hpc_dimensionality_decision_2d_short_qc_no_hpc",
        "field_geometry_type": survey.get("classification", ""),
        "is_3d_survey": bool(is_3d),
        "ready_for_2d_qc": bool(readiness.get("ready_for_2d_qc")) and bool(claims.get("ready_for_2d_field_qc")),
        "ready_for_short_relative_timing_qc": bool(short_qc_ready),
        "ready_for_long_short_transfer": bool(transfer_ready),
        "ready_for_3d_hpc": bool(ready_3d),
        "ready_for_field_fwi": bool(ready_fwi),
        "ready_for_absolute_time_zero": bool(claims.get("ready_for_absolute_time_zero")),
        "ready_for_cover_depth_recovery": bool(claims.get("ready_for_cover_depth_recovery")),
        "ready_for_radius_recovery": bool(claims.get("ready_for_radius_recovery")),
        "profile_count": int(safe_float(readiness.get("profile_count"), 0)),
        "total_trace_derived_length_m": safe_float(readiness.get("total_trace_derived_length_m")),
        "scan_spacing_mm": safe_float(readiness.get("scan_spacing_mm")),
        "samples_per_wavelength": safe_float(readiness.get("samples_per_wavelength")),
        "time_zero_two_way_depth_equivalent_mm": safe_float(
            readiness.get("time_zero_two_way_depth_equivalent_mm")
        ),
        "short_nominal_offset_ns": safe_float(timing.get("short_nominal_offset_ns")),
        "long_short_offset_separation_ns": safe_float(timing.get("long_best_offset_distance_from_short_ns")),
        "spatial_all_window_supported_fraction": safe_float(
            readiness.get("spatial_all_window_supported_fraction")
        ),
        "short_anchor_inside_envelope_count": safe_float(
            timing_envelope.get("short_anchor_inside_envelope_count"), 0.0
        ),
        "short_anchor_inside_supported_interval_count": safe_float(
            anchor_interval.get("short_anchor_inside_supported_interval_count"), 0.0
        ),
        "short_content_anchor_inside_supported_interval_count": safe_float(
            anchor_interval.get("short_content_anchor_inside_supported_interval_count"), 0.0
        ),
        "anchor_interval_min_margin_mm": safe_float(
            anchor_interval.get("min_margin_to_supported_interval_edge_mm"), 0.0
        ),
        "long_pattern_reject_short_transfer_count": safe_float(
            timing_envelope.get("long_pattern_reject_short_transfer_count"), 0.0
        ),
        "long_pattern_with_nearest_short_content_count": safe_float(
            spatial_transfer.get("long_pattern_with_nearest_short_content_within_threshold_count"), 0.0
        ),
        "median_long_to_short_distance_mm": safe_float(
            spatial_transfer.get("median_long_to_short_distance_mm"), 0.0
        ),
        "decision_gate_count": len(rows),
        "field_hpc_priority": "none",
        "recommended_next": (
            "Keep this dataset on the local CPU field-QC path. Use the short profiles "
            "for scoped relative-timing QC, keep the long profiles as pattern context, "
            "and do not send field data to HPC for 3D or FWI unless external survey-layout "
            "metadata, calibrated target geometry, and absolute timing/depth controls are added."
        ),
        "decision": (
            "The local GSSI 51600S field data should be treated as four independent "
            "2D line profiles. The short profiles support relative timing and interval "
            "QC, while short-to-long transfer is rejected. The dataset is not a 3D survey "
            "or a field-FWI/HPC workload in the current archive state."
        ),
    }


def plot_decision(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["gate_key"].replace("_", "\n") for row in rows]
    scores = [float(row["readiness_score"]) for row in rows]
    colors = ["#2f9d55" if score >= 0.75 else "#d99a19" if score >= 0.35 else "#c7302b" for score in scores]

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.0), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, scores, color=colors, edgecolor="#333333", linewidth=0.6)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_ylabel("readiness score")
    axes[0].set_title("Field decision gates")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    decision_labels = ["2D\nQC", "short\nQC", "3D\nHPC", "field\nFWI", "long\ntransfer", "abs\nt0", "radius", "cover"]
    decision_values = [
        summary["ready_for_2d_qc"],
        summary["ready_for_short_relative_timing_qc"],
        summary["ready_for_3d_hpc"],
        summary["ready_for_field_fwi"],
        summary["ready_for_long_short_transfer"],
        summary["ready_for_absolute_time_zero"],
        summary["ready_for_radius_recovery"],
        summary["ready_for_cover_depth_recovery"],
    ]
    decision_colors = ["#2f9d55" if value else "#c7302b" for value in decision_values]
    axes[1].bar(np.arange(len(decision_labels)), [1 if value else 0 for value in decision_values], color=decision_colors)
    axes[1].set_xticks(np.arange(len(decision_labels)), decision_labels)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_title("Allowed-use gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.94,
        (
            f"{summary['field_geometry_type']}\n"
            f"profiles={summary['profile_count']}, length={summary['total_trace_derived_length_m']:.3f} m\n"
            f"spacing={summary['scan_spacing_mm']:.3f} mm, "
            f"samples/lambda={summary['samples_per_wavelength']:.1f}\n"
            f"relative t0 depth eq.={summary['time_zero_two_way_depth_equivalent_mm']:.2f} mm"
        ),
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#aaaaaa"},
    )
    fig.suptitle("Local GSSI field dimensionality and HPC decision card", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_hpc_dimensionality_decision_card.png`",
                "",
                "This figure consolidates the local GSSI field dimensionality and HPC decision.",
                "It does not run FDTD, FWI, 3D inversion, GPU kernels, or neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Geometry type: `{summary['field_geometry_type']}`.",
                f"Ready for 2D QC: `{summary['ready_for_2d_qc']}`.",
                f"Ready for short relative timing QC: `{summary['ready_for_short_relative_timing_qc']}`.",
                f"Ready for long-short transfer: `{summary['ready_for_long_short_transfer']}`.",
                f"Ready for 3D HPC: `{summary['ready_for_3d_hpc']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"Field HPC priority: `{summary['field_hpc_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Decision rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
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
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--survey-run", default=DEFAULT_SURVEY_RUN)
    parser.add_argument("--readiness-run", default=DEFAULT_READINESS_RUN)
    parser.add_argument("--timing-run", default=DEFAULT_TIMING_RUN)
    parser.add_argument("--claim-summary-run", default=DEFAULT_CLAIM_SUMMARY_RUN)
    parser.add_argument("--timing-envelope-run", default=DEFAULT_TIMING_ENVELOPE_RUN)
    parser.add_argument("--spatial-transfer-run", default=DEFAULT_SPATIAL_TRANSFER_RUN)
    parser.add_argument("--anchor-interval-run", default=DEFAULT_ANCHOR_INTERVAL_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_hpc_dimensionality_decision_card_post_anchor_interval")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    summary_root = Path(args.summary_root)
    survey = read_json(dataset_root / args.survey_run / "data/survey_geometry_audit_summary.json")
    readiness = read_json(dataset_root / args.readiness_run / "data/field_acquisition_readiness_summary.json")
    timing = read_json(dataset_root / args.timing_run / "data/field_timing_discriminant_scorecard_summary.json")
    claims = read_json(summary_root / args.claim_summary_run / "data/local_gssi_field_claim_viability_summary.json")
    timing_envelope = read_json(dataset_root / args.timing_envelope_run / "data/field_cue_timing_envelope_summary.json")
    spatial_transfer = read_json(dataset_root / args.spatial_transfer_run / "data/field_spatial_transfer_audit_summary.json")
    anchor_interval = read_json(
        dataset_root / args.anchor_interval_run / "data/field_anchor_interval_reconciliation_summary.json"
    )

    rows = build_decision_rows(
        survey=survey,
        readiness=readiness,
        timing=timing,
        claims=claims,
        timing_envelope=timing_envelope,
        spatial_transfer=spatial_transfer,
        anchor_interval=anchor_interval,
    )
    summary = summarize_decision(
        rows,
        survey,
        readiness,
        timing,
        claims,
        timing_envelope,
        spatial_transfer,
        anchor_interval,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_hpc_dimensionality_decision_rows.csv"
    summary_json = data_dir / "field_hpc_dimensionality_decision_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_hpc_dimensionality_decision_card.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_decision(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "timing_envelope_summary_json": str(
            dataset_root / args.timing_envelope_run / "data/field_cue_timing_envelope_summary.json"
        ),
        "spatial_transfer_summary_json": str(
            dataset_root / args.spatial_transfer_run / "data/field_spatial_transfer_audit_summary.json"
        ),
        "anchor_interval_summary_json": str(
            dataset_root / args.anchor_interval_run / "data/field_anchor_interval_reconciliation_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "gssi_field_hpc_dimensionality_decision_card",
        {
            "survey_run": args.survey_run,
            "readiness_run": args.readiness_run,
            "timing_run": args.timing_run,
            "claim_summary_run": args.claim_summary_run,
            "timing_envelope_run": args.timing_envelope_run,
            "spatial_transfer_run": args.spatial_transfer_run,
            "anchor_interval_run": args.anchor_interval_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
