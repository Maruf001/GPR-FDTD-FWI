#!/usr/bin/env python3
"""Bridge local GSSI field QC evidence to the controlled-collection action plan."""

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
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_DIMENSIONALITY_RUN = "118_gssi51600s_field_hpc_dimensionality_decision_card_post_anchor_interval"
DEFAULT_TIME_ZERO_LADDER_RUN = "121_gssi51600s_field_time_zero_ladder_post_leave_one"
DEFAULT_SPATIAL_CONSISTENCY_RUN = "122_gssi51600s_field_short_anchor_spatial_consistency_audit"
DEFAULT_WAVEFORM_RUN = "124_gssi51600s_field_short_anchor_waveform_coherence_audit"
DEFAULT_TIMING_MARGIN_RUN = "129_gssi51600s_field_short_anchor_signed_morphology_timing_margin"
DEFAULT_CONTRAST_REGIME_RUN = "135_gssi51600s_field_short_anchor_signal_contrast_regime_synthesis"
DEFAULT_REFERENCE_RUN = "145_gssi51600s_field_time_zero_reference_requirement"
DEFAULT_VALIDATION_RUN = "152_gssi51600s_recovered_scaffold_type_aware_validation"
DEFAULT_ACTION_RUN = "153_gssi51600s_recovered_scaffold_type_aware_blocker_prioritization"


ACTION_AXIS_MAP = {
    "target_truth_geometry": "target_truth_controls;cover_depth_validation;radius_validation;field_fwi",
    "time_zero_reference": "absolute_time_zero;calibrated_depth;field_fwi",
    "amplitude_reference": "amplitude_calibration;field_fwi",
    "profile_target_geometry": "profile_spatial_calibration;cross_table_links;short_repeat_redundancy",
    "acquisition_control_links": "controlled_repeats;tx_rx_offset_confirmation;short_repeat_redundancy",
    "session_metadata": "required_metadata_fields;packet_acceptance",
    "reference_registry": "absolute_time_zero;amplitude_calibration;cross_table_links",
}


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def metric_text(value: object, suffix: str = "") -> str:
    number = safe_float(value, math.nan)
    if math.isfinite(number):
        return f"{number:.6g}{suffix}"
    return ""


def gate_ready(gate_rows: list[dict], gate_key: str) -> bool:
    for row in gate_rows:
        if row.get("gate_key") == gate_key:
            return boolish(row.get("ready_now"))
    return False


def missing_count(action_rows: list[dict], group: str) -> int:
    return sum(
        safe_int(row.get("missing_required_count"), 0)
        for row in action_rows
        if row.get("blocker_group") == group
    )


def build_evidence_rows(summaries: dict[str, dict], action_rows: list[dict], gate_rows: list[dict]) -> list[dict]:
    dimensionality = summaries["dimensionality"]
    time_zero = summaries["time_zero_ladder"]
    spatial = summaries["spatial_consistency"]
    waveform = summaries["waveform"]
    timing_margin = summaries["timing_margin"]
    contrast = summaries["contrast_regime"]
    reference = summaries["reference_requirement"]
    validation = summaries["packet_validation"]
    action_summary = summaries["action_summary"]

    is_2d_profile_bundle = (
        str(dimensionality.get("field_geometry_type")) == "independent_2d_line_profiles"
        and not boolish(dimensionality.get("is_3d_survey"))
    )
    packet_ready = boolish(validation.get("ready_for_packet_acceptance"))
    all_packet_gates_ready = all(gate_ready(gate_rows, key) for key in {row.get("gate_key") for row in gate_rows})

    rows = [
        {
            "axis_key": "field_archive_dimensionality",
            "axis_family": "scope_context",
            "status": "2d_qc_scope" if is_2d_profile_bundle else "review_required",
            "ready": is_2d_profile_bundle,
            "source_run": "118",
            "metric_label": "profile count",
            "metric_value": safe_float(dimensionality.get("profile_count"), math.nan),
            "metric_units": "profiles",
            "allowed_use": "local 2D line-profile QC and field supplement context",
            "blocked_use": "field 3D/HPC inversion workload",
            "evidence": (
                f"geometry={dimensionality.get('field_geometry_type', '')}; "
                f"is_3d={dimensionality.get('is_3d_survey', False)}"
            ),
        },
        {
            "axis_key": "short_relative_timing_qc",
            "axis_family": "current_archive_support",
            "status": "supported_qc_only",
            "ready": boolish(time_zero.get("ready_for_short_relative_timing_qc")),
            "source_run": "121",
            "metric_label": "content-only half range",
            "metric_value": safe_float(time_zero.get("content_only_offset_half_range_ns"), math.nan),
            "metric_units": "ns",
            "allowed_use": "short-profile relative timing QC",
            "blocked_use": "absolute time-zero or calibrated depth inversion",
            "evidence": (
                "content-only offset half-range="
                f"{metric_text(time_zero.get('content_only_offset_half_range_ns'), ' ns')}; "
                f"leave-one content ready={time_zero.get('ready_for_leave_one_content_anchor_claim', False)}"
            ),
        },
        {
            "axis_key": "waveform_morphology_qc",
            "axis_family": "current_archive_support",
            "status": "supported_qc_only",
            "ready": boolish(waveform.get("ready_for_waveform_morphology_qc")),
            "source_run": "124",
            "metric_label": "minimum corrected abs correlation",
            "metric_value": safe_float(waveform.get("min_corrected_field_trace_abs_correlation"), math.nan),
            "metric_units": "corr",
            "allowed_use": "short-anchor waveform morphology QC",
            "blocked_use": "geometry seed, radius seed, or amplitude calibration",
            "evidence": (
                "min corrected abs corr="
                f"{metric_text(waveform.get('min_corrected_field_trace_abs_correlation'))}; "
                f"radius matches={waveform.get('radius_match_pair_count', 0)}"
            ),
        },
        {
            "axis_key": "content_only_timing_margin",
            "axis_family": "current_archive_support",
            "status": "supported_qc_only",
            "ready": boolish(timing_margin.get("ready_for_content_only_morphology_timing_qc")),
            "source_run": "129",
            "metric_label": "minimum default timing slack",
            "metric_value": safe_float(timing_margin.get("min_default_timing_slack_ns"), math.nan),
            "metric_units": "ns",
            "allowed_use": "content-only morphology timing-margin QC",
            "blocked_use": "conservative timing promotion or absolute time-zero",
            "evidence": (
                "min default slack="
                f"{metric_text(timing_margin.get('min_default_timing_slack_ns'), ' ns')}; "
                f"conservative ready={timing_margin.get('ready_for_conservative_timing_morphology_claim', False)}"
            ),
        },
        {
            "axis_key": "broad_signal_contrast_qc",
            "axis_family": "current_archive_support",
            "status": "supported_qc_only",
            "ready": boolish(contrast.get("ready_for_broad_event_signal_contrast_regime")),
            "source_run": "135",
            "metric_label": "broad-window minimum RMS ratio",
            "metric_value": safe_float(contrast.get("broad_event_min_event_to_noise_rms"), math.nan),
            "metric_units": "ratio",
            "allowed_use": "broad-window signal-contrast morphology QC",
            "blocked_use": "strict window-invariant contrast or amplitude calibration",
            "evidence": (
                "broad min RMS ratio="
                f"{metric_text(contrast.get('broad_event_min_event_to_noise_rms'), 'x')}; "
                f"strict ready={contrast.get('ready_for_strict_window_invariant_signal_contrast_claim', False)}"
            ),
        },
        {
            "axis_key": "absolute_time_zero_reference",
            "axis_family": "inversion_blocker",
            "status": "blocked_new_reference_required",
            "ready": boolish(reference.get("current_packet_time_zero_reference_ready"))
            and gate_ready(gate_rows, "absolute_time_zero_references"),
            "source_run": "145,153",
            "metric_label": "reference uncertainty gate",
            "metric_value": safe_float(reference.get("reference_uncertainty_gate_ns"), math.nan),
            "metric_units": "ns",
            "allowed_use": "future absolute time-zero if references pass",
            "blocked_use": "current archive absolute time-zero, calibrated depth, field FWI",
            "evidence": (
                f"repeat gate={reference.get('reference_repeat_gate')}; "
                f"uncertainty gate={metric_text(reference.get('reference_uncertainty_gate_ns'), ' ns')}; "
                f"missing fields={missing_count(action_rows, 'time_zero_reference')}"
            ),
        },
        {
            "axis_key": "absolute_amplitude_calibration",
            "axis_family": "inversion_blocker",
            "status": "blocked_new_reference_required",
            "ready": gate_ready(gate_rows, "amplitude_references"),
            "source_run": "153",
            "metric_label": "missing amplitude-reference fields",
            "metric_value": missing_count(action_rows, "amplitude_reference"),
            "metric_units": "fields",
            "allowed_use": "future amplitude-calibrated comparison after reference repeats",
            "blocked_use": "absolute amplitude, amplitude-calibrated field FWI",
            "evidence": f"missing amplitude-reference fields={missing_count(action_rows, 'amplitude_reference')}",
        },
        {
            "axis_key": "target_truth_and_profile_geometry",
            "axis_family": "inversion_blocker",
            "status": "blocked_new_measurement_required",
            "ready": gate_ready(gate_rows, "target_truth_controls")
            and gate_ready(gate_rows, "required_metadata_fields")
            and gate_ready(gate_rows, "cross_table_links"),
            "source_run": "152,153",
            "metric_label": "truth/profile missing fields",
            "metric_value": missing_count(action_rows, "target_truth_geometry")
            + missing_count(action_rows, "profile_target_geometry"),
            "metric_units": "fields",
            "allowed_use": "future calibrated geometry validation after survey/truth entry",
            "blocked_use": "cover-depth recovery, radius recovery, geometry seeding",
            "evidence": (
                f"target truth missing={missing_count(action_rows, 'target_truth_geometry')}; "
                f"profile geometry missing={missing_count(action_rows, 'profile_target_geometry')}; "
                f"spatial calibration ready={spatial.get('ready_for_profile_spatial_calibration', False)}"
            ),
        },
        {
            "axis_key": "controlled_repeat_packet_acceptance",
            "axis_family": "inversion_blocker",
            "status": "blocked_packet_incomplete",
            "ready": packet_ready and all_packet_gates_ready,
            "source_run": "152,153",
            "metric_label": "packet blocking findings",
            "metric_value": safe_float(validation.get("blocking_finding_count"), math.nan),
            "metric_units": "findings",
            "allowed_use": "future packet-accepted field inversion preflight",
            "blocked_use": "field FWI, heavy field GPU work, field 3D/HPC",
            "evidence": (
                f"blocking findings={validation.get('blocking_finding_count')}; "
                f"failed gates={action_summary.get('failed_acceptance_gate_count')}"
            ),
        },
    ]
    return rows


def build_action_bridge_rows(action_rows: list[dict]) -> list[dict]:
    rows = []
    for row in action_rows:
        priority = safe_int(row.get("priority"), 99)
        group = str(row.get("blocker_group", ""))
        rows.append(
            {
                "priority": priority,
                "blocker_group": group,
                "research_priority": "critical" if priority <= 3 else "high" if priority <= 5 else "metadata",
                "action_type": row.get("action_type", ""),
                "minimum_rows_or_repeats": row.get("minimum_rows_or_repeats", ""),
                "missing_required_count": safe_int(row.get("missing_required_count"), 0),
                "requires_new_controlled_data": boolish(row.get("requires_new_controlled_data")),
                "current_archive_can_resolve": boolish(row.get("current_archive_can_resolve")),
                "unblocks_axes": ACTION_AXIS_MAP.get(group, ""),
                "acceptance_gates_unblocked": row.get("acceptance_gates_unblocked", ""),
                "reference_uncertainty_gate_ns": row.get("reference_uncertainty_gate_ns", ""),
                "reference_depth_equivalent_mm": row.get("reference_depth_equivalent_mm", ""),
                "action": row.get("action", ""),
            }
        )
    return sorted(rows, key=lambda item: (safe_int(item["priority"], 99), str(item["blocker_group"])))


def summarize_bridge(
    evidence_rows: list[dict],
    action_rows: list[dict],
    summaries: dict[str, dict],
) -> dict:
    supported_qc = [
        row
        for row in evidence_rows
        if row["axis_family"] in {"scope_context", "current_archive_support"} and boolish(row["ready"])
    ]
    blocker_rows = [row for row in evidence_rows if row["axis_family"] == "inversion_blocker"]
    unresolved_blockers = [row for row in blocker_rows if not boolish(row["ready"])]
    critical_actions = [
        row
        for row in action_rows
        if safe_int(row.get("priority"), 99) <= 5 and boolish(row.get("requires_new_controlled_data"))
    ]
    reference = summaries["reference_requirement"]
    validation = summaries["packet_validation"]
    action_summary = summaries["action_summary"]
    dimensionality = summaries["dimensionality"]

    return {
        "policy_label": "gssi51600s_field_qc_to_controlled_collection_bridge",
        "evidence_axis_count": len(evidence_rows),
        "current_archive_supported_axis_count": len(supported_qc),
        "inversion_blocker_axis_count": len(blocker_rows),
        "unresolved_inversion_blocker_axis_count": len(unresolved_blockers),
        "action_group_count": len(action_rows),
        "critical_new_data_action_group_count": len(critical_actions),
        "critical_new_data_action_groups": ";".join(row["blocker_group"] for row in critical_actions),
        "packet_blocking_finding_count": validation.get("blocking_finding_count"),
        "packet_missing_required_value_count": validation.get("missing_required_value_count"),
        "failed_acceptance_gate_count": action_summary.get("failed_acceptance_gate_count"),
        "reference_repeat_gate": reference.get("reference_repeat_gate"),
        "reference_uncertainty_gate_ns": reference.get("reference_uncertainty_gate_ns"),
        "reference_uncertainty_gate_depth_error_mm": reference.get("reference_uncertainty_gate_depth_error_mm"),
        "field_geometry_type": dimensionality.get("field_geometry_type", ""),
        "is_3d_survey": boolish(dimensionality.get("is_3d_survey")),
        "ready_for_current_archive_field_qc_supplement": all(
            row["axis_key"] in {item["axis_key"] for item in supported_qc}
            for row in evidence_rows
            if row["axis_family"] in {"scope_context", "current_archive_support"}
        ),
        "ready_for_current_archive_absolute_time_zero": False,
        "ready_for_current_archive_calibrated_depth_or_radius": False,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "ready_for_new_controlled_2d_acquisition": boolish(
            action_summary.get("ready_for_new_controlled_2d_acquisition")
        ),
        "gpu_priority": "none",
        "decision": (
            "The current GSSI archive is useful for a scoped 2D field-QC/manuscript supplement "
            "because short-profile timing, waveform morphology, timing-margin, and broad-window "
            "contrast evidence are supported. It is not inversion-ready: absolute time-zero, "
            "amplitude references, target truth, surveyed geometry, and controlled acquisition "
            "links remain unresolved. Continue local CPU field QC and prepare a controlled 2D "
            "collection packet before any field FWI, heavy GPU work, or field 3D/HPC."
        ),
    }


def plot_bridge(evidence_rows: list[dict], action_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(15.8, 5.6), constrained_layout=True)

    labels = [row["axis_key"].replace("_", "\n") for row in evidence_rows]
    values = [1 if boolish(row["ready"]) else 0 for row in evidence_rows]
    colors = []
    for row in evidence_rows:
        if row["axis_family"] == "scope_context":
            colors.append("#4c78a8")
        elif boolish(row["ready"]):
            colors.append("#59a14f")
        else:
            colors.append("#e15759")
    axes[0].bar(np.arange(len(evidence_rows)), values, color=colors, width=0.65)
    axes[0].set_xticks(np.arange(len(evidence_rows)), labels, fontsize=7.2)
    axes[0].set_yticks([0, 1], ["blocked", "supported"])
    axes[0].set_ylim(-0.15, 1.25)
    axes[0].set_title("Current archive evidence boundary")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    action_labels = [row["blocker_group"].replace("_", "\n") for row in action_rows]
    missing = [safe_int(row.get("missing_required_count"), 0) for row in action_rows]
    action_colors = [
        "#e15759" if safe_int(row.get("priority"), 99) <= 3 else "#f2cf5b" if safe_int(row.get("priority"), 99) <= 5 else "#4c78a8"
        for row in action_rows
    ]
    axes[1].bar(np.arange(len(action_rows)), missing, color=action_colors, width=0.65)
    axes[1].set_xticks(np.arange(len(action_rows)), action_labels, fontsize=7.5)
    axes[1].set_ylabel("missing required fields")
    axes[1].set_title("Controlled-collection action groups")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"QC axes supported={summary['current_archive_supported_axis_count']}/{summary['evidence_axis_count']}\n"
        f"unresolved inversion blockers={summary['unresolved_inversion_blocker_axis_count']}\n"
        f"packet blockers={summary['packet_blocking_finding_count']}\n"
        f"t0 gate={summary['reference_uncertainty_gate_ns']} ns\n"
        f"field FWI={summary['ready_for_current_archive_field_fwi']} | 3D/HPC={summary['ready_for_field_3d_hpc']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.2,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("GSSI field QC to controlled-collection bridge", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_qc_to_controlled_collection_bridge.png`",
                "",
                "This CPU-only figure connects the current local GSSI field-QC evidence",
                "to the corrected controlled-collection packet blockers.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Current archive supported axes: `{summary['current_archive_supported_axis_count']}` / `{summary['evidence_axis_count']}`.",
                f"Unresolved inversion blockers: `{summary['unresolved_inversion_blocker_axis_count']}`.",
                f"Action groups: `{summary['action_group_count']}`.",
                f"Critical new-data groups: `{summary['critical_new_data_action_groups']}`.",
                f"Packet blocking findings: `{summary['packet_blocking_finding_count']}`.",
                f"Reference uncertainty gate: `{summary['reference_uncertainty_gate_ns']}` ns.",
                f"Ready for field FWI: `{summary['ready_for_current_archive_field_fwi']}`.",
                f"Ready for 3D/HPC: `{summary['ready_for_field_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                summary["decision"],
                "",
                "Scope boundary: this run reads saved summaries and packet CSVs only. It does",
                "not run DZT preprocessing, FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs,",
                "or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def source_paths(field_root: Path, args: argparse.Namespace) -> dict[str, Path]:
    return {
        "dimensionality": field_root
        / args.dimensionality_run
        / "data/field_hpc_dimensionality_decision_summary.json",
        "time_zero_ladder": field_root
        / args.time_zero_ladder_run
        / "data/field_time_zero_evidence_ladder_summary.json",
        "spatial_consistency": field_root
        / args.spatial_consistency_run
        / "data/field_short_anchor_spatial_consistency_summary.json",
        "waveform": field_root / args.waveform_run / "data/field_short_anchor_waveform_coherence_summary.json",
        "timing_margin": field_root
        / args.timing_margin_run
        / "data/field_short_anchor_signed_morphology_timing_margin_summary.json",
        "contrast_regime": field_root
        / args.contrast_regime_run
        / "data/field_short_anchor_signal_contrast_regime_summary.json",
        "reference_requirement": field_root
        / args.reference_run
        / "data/field_time_zero_reference_requirement_summary.json",
        "packet_validation": field_root
        / args.validation_run
        / "data/controlled_2d_packet_validation_summary.json",
        "action_summary": field_root
        / args.action_run
        / "data/field_controlled_packet_blocker_prioritization_summary.json",
        "action_groups_csv": field_root
        / args.action_run
        / "data/field_controlled_packet_action_groups.csv",
        "gate_actions_csv": field_root
        / args.action_run
        / "data/field_controlled_packet_gate_actions.csv",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--dimensionality-run", default=DEFAULT_DIMENSIONALITY_RUN)
    parser.add_argument("--time-zero-ladder-run", default=DEFAULT_TIME_ZERO_LADDER_RUN)
    parser.add_argument("--spatial-consistency-run", default=DEFAULT_SPATIAL_CONSISTENCY_RUN)
    parser.add_argument("--waveform-run", default=DEFAULT_WAVEFORM_RUN)
    parser.add_argument("--timing-margin-run", default=DEFAULT_TIMING_MARGIN_RUN)
    parser.add_argument("--contrast-regime-run", default=DEFAULT_CONTRAST_REGIME_RUN)
    parser.add_argument("--reference-run", default=DEFAULT_REFERENCE_RUN)
    parser.add_argument("--validation-run", default=DEFAULT_VALIDATION_RUN)
    parser.add_argument("--action-run", default=DEFAULT_ACTION_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_qc_to_controlled_collection_bridge")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = source_paths(field_root, args)
    summaries = {
        key: read_json(path)
        for key, path in paths.items()
        if key not in {"action_groups_csv", "gate_actions_csv"}
    }
    source_action_rows = read_csv_rows(paths["action_groups_csv"])
    gate_rows = read_csv_rows(paths["gate_actions_csv"])
    evidence_rows = build_evidence_rows(summaries, source_action_rows, gate_rows)
    action_rows = build_action_bridge_rows(source_action_rows)
    summary = summarize_bridge(evidence_rows, action_rows, summaries)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(field_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    evidence_csv = data_dir / "field_qc_to_controlled_collection_evidence_rows.csv"
    action_csv = data_dir / "field_qc_to_controlled_collection_action_rows.csv"
    summary_json = data_dir / "field_qc_to_controlled_collection_bridge_summary.json"
    figure_path = figures_dir / "field_qc_to_controlled_collection_bridge.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(action_csv, [json_safe(row) for row in action_rows])
    plot_bridge(evidence_rows, action_rows, summary, figure_path)
    write_figure_notes(figure_notes, summary)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])

    summary["paths"] = {
        "evidence_csv": str(evidence_csv),
        "action_csv": str(action_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_paths": {key: str(value) for key, value in paths.items()},
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_qc_to_controlled_collection_bridge",
        {
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_json),
            "evidence_csv": str(evidence_csv),
            "action_csv": str(action_csv),
            "figure": str(figure_path),
            "source_runs": {
                "dimensionality_run": args.dimensionality_run,
                "time_zero_ladder_run": args.time_zero_ladder_run,
                "spatial_consistency_run": args.spatial_consistency_run,
                "waveform_run": args.waveform_run,
                "timing_margin_run": args.timing_margin_run,
                "contrast_regime_run": args.contrast_regime_run,
                "reference_run": args.reference_run,
                "validation_run": args.validation_run,
                "action_run": args.action_run,
            },
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
