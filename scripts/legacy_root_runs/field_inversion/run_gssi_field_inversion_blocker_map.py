#!/usr/bin/env python3
"""Map GSSI short-anchor field evidence against inversion blockers."""

from __future__ import annotations

import argparse
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

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


SOURCE_SUMMARIES = {
    "time_zero_ladder": (
        "121_gssi51600s_field_time_zero_ladder_post_leave_one/"
        "data/field_time_zero_evidence_ladder_summary.json"
    ),
    "spatial_consistency": (
        "122_gssi51600s_field_short_anchor_spatial_consistency_audit/"
        "data/field_short_anchor_spatial_consistency_summary.json"
    ),
    "inversion_readiness": (
        "123_gssi51600s_field_inversion_readiness_synthesis_post_spatial_consistency/"
        "data/field_inversion_readiness_synthesis_summary.json"
    ),
    "waveform_coherence": (
        "124_gssi51600s_field_short_anchor_waveform_coherence_audit/"
        "data/field_short_anchor_waveform_coherence_summary.json"
    ),
    "radius_degeneracy": (
        "125_gssi51600s_field_short_anchor_radius_degeneracy_audit/"
        "data/field_short_anchor_radius_degeneracy_summary.json"
    ),
    "signed_morphology": (
        "126_gssi51600s_field_short_anchor_signed_morphology_audit/"
        "data/field_short_anchor_signed_morphology_summary.json"
    ),
    "timing_margin": (
        "129_gssi51600s_field_short_anchor_signed_morphology_timing_margin/"
        "data/field_short_anchor_signed_morphology_timing_margin_summary.json"
    ),
    "signal_contrast": (
        "131_gssi51600s_field_short_anchor_signal_contrast_audit/"
        "data/field_short_anchor_signal_contrast_summary.json"
    ),
    "contrast_sensitivity": (
        "132_gssi51600s_field_short_anchor_signal_contrast_sensitivity/"
        "data/field_short_anchor_signal_contrast_sensitivity_summary.json"
    ),
    "contrast_regime": (
        "135_gssi51600s_field_short_anchor_signal_contrast_regime_synthesis/"
        "data/field_short_anchor_signal_contrast_regime_summary.json"
    ),
}


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def metric_text(value: object, suffix: str = "") -> str:
    number = safe_float(value, math.nan)
    if math.isfinite(number):
        return f"{number:.6g}{suffix}"
    return ""


def load_source_summaries(dataset_root: Path) -> dict[str, dict]:
    return {key: read_json(dataset_root / rel_path) for key, rel_path in SOURCE_SUMMARIES.items()}


def build_evidence_rows(summaries: dict[str, dict]) -> list[dict]:
    time_zero = summaries["time_zero_ladder"]
    spatial = summaries["spatial_consistency"]
    readiness = summaries["inversion_readiness"]
    waveform = summaries["waveform_coherence"]
    radius = summaries["radius_degeneracy"]
    signed = summaries["signed_morphology"]
    timing_margin = summaries["timing_margin"]
    contrast = summaries["signal_contrast"]
    contrast_sensitivity = summaries["contrast_sensitivity"]
    contrast_regime = summaries["contrast_regime"]

    rows = [
        {
            "axis_key": "short_relative_timing_qc",
            "axis_family": "positive_evidence",
            "ready": boolish(time_zero.get("ready_for_short_relative_timing_qc")),
            "severity": "support",
            "metric_label": "content-only half range",
            "metric_value": safe_float(time_zero.get("content_only_offset_half_range_ns"), math.nan),
            "metric_units": "ns",
            "source_run": "121",
            "allowed_use": "short-profile relative timing QC",
            "blocked_use": "absolute time-zero or calibrated depth inversion",
            "evidence": (
                "content-only offset half-range="
                f"{metric_text(time_zero.get('content_only_offset_half_range_ns'), ' ns')}"
            ),
        },
        {
            "axis_key": "waveform_morphology_qc",
            "axis_family": "positive_evidence",
            "ready": boolish(waveform.get("ready_for_waveform_morphology_qc")),
            "severity": "support",
            "metric_label": "minimum corrected abs correlation",
            "metric_value": safe_float(waveform.get("min_corrected_field_trace_abs_correlation"), math.nan),
            "metric_units": "corr",
            "source_run": "124",
            "allowed_use": "short-anchor waveform morphology QC",
            "blocked_use": "geometry, radius, or amplitude calibration",
            "evidence": (
                "min corrected abs corr="
                f"{metric_text(waveform.get('min_corrected_field_trace_abs_correlation'))}"
            ),
        },
        {
            "axis_key": "signed_morphology_qc",
            "axis_family": "positive_evidence",
            "ready": boolish(signed.get("ready_for_signed_waveform_morphology_qc")),
            "severity": "support",
            "metric_label": "minimum signed correlation",
            "metric_value": safe_float(signed.get("min_corrected_signed_correlation"), math.nan),
            "metric_units": "corr",
            "source_run": "126",
            "allowed_use": "signed short-anchor morphology QC",
            "blocked_use": "absolute amplitude or radius/geometry seeding",
            "evidence": (
                "min signed corr="
                f"{metric_text(signed.get('min_corrected_signed_correlation'))}"
            ),
        },
        {
            "axis_key": "content_only_timing_margin",
            "axis_family": "positive_evidence",
            "ready": boolish(timing_margin.get("ready_for_content_only_morphology_timing_qc")),
            "severity": "support",
            "metric_label": "default timing slack",
            "metric_value": safe_float(timing_margin.get("min_default_timing_slack_ns"), math.nan),
            "metric_units": "ns",
            "source_run": "129",
            "allowed_use": "content-only morphology timing-margin QC",
            "blocked_use": "conservative timing promotion or absolute time-zero",
            "evidence": (
                "minimum default timing slack="
                f"{metric_text(timing_margin.get('min_default_timing_slack_ns'), ' ns')}"
            ),
        },
        {
            "axis_key": "broad_signal_contrast_qc",
            "axis_family": "positive_evidence",
            "ready": boolish(contrast_regime.get("ready_for_broad_event_signal_contrast_regime")),
            "severity": "support",
            "metric_label": "broad-event minimum RMS ratio",
            "metric_value": safe_float(contrast_regime.get("broad_event_min_event_to_noise_rms"), math.nan),
            "metric_units": "ratio",
            "source_run": "135",
            "allowed_use": "broad-window signal-contrast morphology QC",
            "blocked_use": "window-invariant contrast or amplitude calibration",
            "evidence": (
                "broad min RMS ratio="
                f"{metric_text(contrast_regime.get('broad_event_min_event_to_noise_rms'), 'x')}"
            ),
        },
        {
            "axis_key": "apparent_depth_scale_qc",
            "axis_family": "positive_evidence",
            "ready": boolish(readiness.get("ready_for_apparent_depth_scale_qc")),
            "severity": "support",
            "metric_label": "max corrected depth residual",
            "metric_value": safe_float(readiness.get("max_corrected_depth_residual_mm"), math.nan),
            "metric_units": "mm",
            "source_run": "123",
            "allowed_use": "apparent-depth scale sanity check",
            "blocked_use": "cover-depth recovery or calibrated inversion",
            "evidence": (
                "max corrected depth residual="
                f"{metric_text(readiness.get('max_corrected_depth_residual_mm'), ' mm')}"
            ),
        },
        {
            "axis_key": "leave_one_content_redundancy",
            "axis_family": "blocker",
            "ready": boolish(time_zero.get("ready_for_leave_one_content_anchor_claim")),
            "severity": "major_blocker",
            "metric_label": "degraded single-content cases",
            "metric_value": safe_float(time_zero.get("leave_one_degraded_single_content_count"), math.nan),
            "metric_units": "count",
            "source_run": "121",
            "allowed_use": "none beyond scoped QC",
            "blocked_use": "leave-one-content robust time-zero claim",
            "evidence": (
                "degraded single-content cases="
                f"{metric_text(time_zero.get('leave_one_degraded_single_content_count'))}"
            ),
        },
        {
            "axis_key": "long_profile_transfer",
            "axis_family": "blocker",
            "ready": boolish(time_zero.get("ready_for_long_short_transfer")),
            "severity": "major_blocker",
            "metric_label": "long anchors rejecting short transfer",
            "metric_value": safe_float(time_zero.get("long_pattern_reject_short_transfer_count"), math.nan),
            "metric_units": "count",
            "source_run": "121",
            "allowed_use": "none",
            "blocked_use": "transfer short-profile timing to long profiles",
            "evidence": (
                "long transfer rejections="
                f"{metric_text(time_zero.get('long_pattern_reject_short_transfer_count'))}"
            ),
        },
        {
            "axis_key": "profile_spatial_calibration",
            "axis_family": "blocker",
            "ready": boolish(spatial.get("ready_for_profile_spatial_calibration")),
            "severity": "critical_blocker",
            "metric_label": "content residual range",
            "metric_value": safe_float(spatial.get("content_residual_range_mm"), math.nan),
            "metric_units": "mm",
            "source_run": "122",
            "allowed_use": "none",
            "blocked_use": "single profile-to-profile spatial translation",
            "evidence": (
                "residual range="
                f"{metric_text(spatial.get('content_residual_range_mm'), ' mm')}; "
                f"sign consistent={boolish(spatial.get('content_residual_sign_consistent'))}"
            ),
        },
        {
            "axis_key": "absolute_time_zero",
            "axis_family": "blocker",
            "ready": boolish(time_zero.get("ready_for_absolute_time_zero")),
            "severity": "critical_blocker",
            "metric_label": "conservative half-width",
            "metric_value": safe_float(time_zero.get("short_conservative_half_width_ns"), math.nan),
            "metric_units": "ns",
            "source_run": "121",
            "allowed_use": "none",
            "blocked_use": "absolute time-zero or calibrated depth inversion",
            "evidence": (
                "short conservative half-width="
                f"{metric_text(time_zero.get('short_conservative_half_width_ns'), ' ns')}"
            ),
        },
        {
            "axis_key": "radius_seed_or_recovery",
            "axis_family": "blocker",
            "ready": boolish(radius.get("ready_for_radius_recovery")) or boolish(radius.get("ready_for_radius_seed")),
            "severity": "critical_blocker",
            "metric_label": "weak radius sides",
            "metric_value": safe_float(radius.get("weak_radius_side_count"), math.nan),
            "metric_units": "count",
            "source_run": "125",
            "allowed_use": "none",
            "blocked_use": "radius seed, radius recovery, or geometry seed",
            "evidence": (
                f"weak sides={metric_text(radius.get('weak_radius_side_count'))}; "
                f"mismatch pairs={metric_text(radius.get('selected_radius_mismatch_pair_count'))}; "
                f"common-radius near ties={metric_text(radius.get('common_radius_near_tie_pair_count'))}"
            ),
        },
        {
            "axis_key": "absolute_amplitude_calibration",
            "axis_family": "blocker",
            "ready": boolish(contrast.get("ready_for_absolute_amplitude_calibration"))
            or boolish(contrast_regime.get("ready_for_absolute_amplitude_calibration")),
            "severity": "critical_blocker",
            "metric_label": "window-invariant combo fraction",
            "metric_value": safe_float(contrast_sensitivity.get("all_supported_combo_fraction"), math.nan),
            "metric_units": "fraction",
            "source_run": "132/135",
            "allowed_use": "none",
            "blocked_use": "absolute amplitude calibration or amplitude-driven inversion",
            "evidence": (
                "strict window invariant="
                f"{boolish(contrast_regime.get('ready_for_strict_window_invariant_signal_contrast_claim'))}; "
                "all-supported combos="
                f"{metric_text(contrast_sensitivity.get('all_supported_combo_count'))}/"
                f"{metric_text(contrast_sensitivity.get('sensitivity_combo_count'))}"
            ),
        },
        {
            "axis_key": "cover_depth_recovery",
            "axis_family": "blocker",
            "ready": boolish(readiness.get("ready_for_cover_depth_recovery")),
            "severity": "critical_blocker",
            "metric_label": "apparent depth max span",
            "metric_value": safe_float(readiness.get("apparent_depth_max_span_mm"), math.nan),
            "metric_units": "mm",
            "source_run": "123",
            "allowed_use": "none",
            "blocked_use": "cover-depth recovery claim",
            "evidence": (
                "apparent depth max span="
                f"{metric_text(readiness.get('apparent_depth_max_span_mm'), ' mm')}"
            ),
        },
        {
            "axis_key": "field_fwi",
            "axis_family": "blocker",
            "ready": boolish(readiness.get("ready_for_field_fwi")),
            "severity": "critical_blocker",
            "metric_label": "supported readiness gates",
            "metric_value": safe_float(readiness.get("supported_gate_count"), math.nan),
            "metric_units": "count",
            "source_run": "123-135",
            "allowed_use": "none",
            "blocked_use": "field FWI launch",
            "evidence": (
                f"supported gates={metric_text(readiness.get('supported_gate_count'))}/"
                f"{metric_text(readiness.get('gate_count'))}; latest morphology/contrast gates remain QC-only"
            ),
        },
        {
            "axis_key": "field_3d_hpc",
            "axis_family": "blocker",
            "ready": boolish(readiness.get("ready_for_3d_hpc")),
            "severity": "scope_blocker",
            "metric_label": "is 3D survey",
            "metric_value": 1.0 if boolish(readiness.get("is_3d_survey")) else 0.0,
            "metric_units": "boolean",
            "source_run": "123",
            "allowed_use": "none",
            "blocked_use": "3D/HPC field inversion workload",
            "evidence": f"field geometry type={readiness.get('field_geometry_type', 'unknown')}",
        },
    ]
    return rows


def summarize_blocker_map(rows: list[dict], summaries: dict[str, dict]) -> dict:
    evidence_rows = [row for row in rows if row["axis_family"] == "positive_evidence"]
    blocker_rows = [row for row in rows if row["axis_family"] == "blocker"]
    ready_evidence = [row for row in evidence_rows if boolish(row.get("ready"))]
    unresolved_blockers = [row for row in blocker_rows if not boolish(row.get("ready"))]
    critical_unresolved = [row for row in unresolved_blockers if row["severity"] == "critical_blocker"]
    ready_for_morphology_supplement = all(
        any(row["axis_key"] == key and boolish(row["ready"]) for row in rows)
        for key in [
            "short_relative_timing_qc",
            "signed_morphology_qc",
            "content_only_timing_margin",
            "broad_signal_contrast_qc",
        ]
    )
    ready_for_field_inversion = len(critical_unresolved) == 0 and not any(
        row["axis_key"] in {"field_fwi", "field_3d_hpc"} and not boolish(row["ready"]) for row in blocker_rows
    )
    readiness = summaries["inversion_readiness"]
    return {
        "policy_label": "gssi51600s_field_inversion_blocker_map_qc_only",
        "evidence_axis_count": len(evidence_rows),
        "ready_evidence_axis_count": len(ready_evidence),
        "blocker_axis_count": len(blocker_rows),
        "unresolved_blocker_axis_count": len(unresolved_blockers),
        "critical_unresolved_blocker_count": len(critical_unresolved),
        "ready_for_field_morphology_supplement": ready_for_morphology_supplement,
        "ready_for_short_relative_timing_qc": any(
            row["axis_key"] == "short_relative_timing_qc" and boolish(row["ready"]) for row in rows
        ),
        "ready_for_profile_spatial_calibration": any(
            row["axis_key"] == "profile_spatial_calibration" and boolish(row["ready"]) for row in rows
        ),
        "ready_for_absolute_time_zero": any(
            row["axis_key"] == "absolute_time_zero" and boolish(row["ready"]) for row in rows
        ),
        "ready_for_radius_or_geometry_seed": any(
            row["axis_key"] == "radius_seed_or_recovery" and boolish(row["ready"]) for row in rows
        ),
        "ready_for_absolute_amplitude_calibration": any(
            row["axis_key"] == "absolute_amplitude_calibration" and boolish(row["ready"]) for row in rows
        ),
        "ready_for_cover_depth_recovery": any(
            row["axis_key"] == "cover_depth_recovery" and boolish(row["ready"]) for row in rows
        ),
        "ready_for_field_fwi": ready_for_field_inversion and any(
            row["axis_key"] == "field_fwi" and boolish(row["ready"]) for row in rows
        ),
        "ready_for_3d_hpc": any(row["axis_key"] == "field_3d_hpc" and boolish(row["ready"]) for row in rows),
        "ready_for_heavy_field_work": False,
        "field_geometry_type": readiness.get("field_geometry_type", "unknown"),
        "is_3d_survey": boolish(readiness.get("is_3d_survey")),
        "gpu_priority": "none",
        "decision": (
            "Latest short-anchor timing, signed morphology, timing-margin, and broad-window "
            "contrast evidence support a field morphology supplement. Independent blockers "
            "still prevent field inversion: no absolute time-zero, no single spatial "
            "translation, weak radius evidence, no absolute amplitude calibration, no "
            "cover-depth validation, and no 3D survey geometry."
        ),
        "recommended_next_field_work": (
            "Do not run field FWI/HPC from this archive. Either keep the data as a 2D QC "
            "supplement or design a new controlled field acquisition with surveyed target "
            "geometry, absolute timing/depth controls, dielectric calibration, and amplitude "
            "calibration."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "field_morphology_supplement",
            "ready": summary["ready_for_field_morphology_supplement"],
            "allowed_use": "short-profile field morphology/timing supplement",
            "blocked_use": "calibrated inversion claim",
            "evidence": f"ready evidence axes={summary['ready_evidence_axis_count']}/{summary['evidence_axis_count']}",
        },
        {
            "gate_key": "field_inversion_or_fwi",
            "ready": summary["ready_for_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI or calibrated inversion",
            "evidence": f"critical unresolved blockers={summary['critical_unresolved_blocker_count']}",
        },
        {
            "gate_key": "field_3d_hpc",
            "ready": summary["ready_for_3d_hpc"],
            "allowed_use": "none",
            "blocked_use": "3D/HPC field inversion workload",
            "evidence": f"geometry={summary['field_geometry_type']}",
        },
        {
            "gate_key": "heavy_field_work",
            "ready": summary["ready_for_heavy_field_work"],
            "allowed_use": "none",
            "blocked_use": "local broad field computation or GPU queue",
            "evidence": summary["recommended_next_field_work"],
        },
    ]


def plot_blocker_map(rows: list[dict], summary: dict, save_path: Path) -> str:
    evidence = [row for row in rows if row["axis_family"] == "positive_evidence"]
    blockers = [row for row in rows if row["axis_family"] == "blocker"]
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.0), constrained_layout=True)
    for ax, panel_rows, title in [
        (axes[0], evidence, "Supported Field Evidence"),
        (axes[1], blockers, "Unresolved Inversion Blockers"),
    ]:
        labels = [row["axis_key"].replace("_", "\n") for row in panel_rows]
        values = [1.0 if boolish(row["ready"]) else 0.0 for row in panel_rows]
        colors = [
            "#2f9d55" if row["axis_family"] == "positive_evidence" and boolish(row["ready"]) else "#d6453d"
            for row in panel_rows
        ]
        ax.bar(range(len(panel_rows)), values, color=colors)
        ax.set_xticks(range(len(panel_rows)))
        ax.set_xticklabels(labels, rotation=0, ha="center", fontsize=8)
        ax.set_ylim(0, 1.15)
        ax.set_ylabel("ready flag")
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
        for idx, row in enumerate(panel_rows):
            ax.text(
                idx,
                min(1.05, values[idx] + 0.04),
                "ready" if boolish(row["ready"]) else "blocked",
                ha="center",
                va="bottom",
                fontsize=8,
            )
    axes[1].text(
        0.02,
        0.08,
        f"critical blockers={summary['critical_unresolved_blocker_count']}\n"
        f"field FWI={summary['ready_for_field_fwi']}\n"
        f"3D/HPC={summary['ready_for_3d_hpc']}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S Field Evidence And Inversion Blocker Map", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_inversion_blocker_map.png`",
                "",
                "This figure maps the current GSSI 51600S short-anchor field evidence",
                "against the controls still required for calibrated field inversion.",
                "",
                f"Ready evidence axes: `{summary['ready_evidence_axis_count']}/{summary['evidence_axis_count']}`.",
                f"Unresolved blockers: `{summary['unresolved_blocker_axis_count']}`.",
                f"Critical unresolved blockers: `{summary['critical_unresolved_blocker_count']}`.",
                f"Field morphology supplement ready: `{summary['ready_for_field_morphology_supplement']}`.",
                f"Field FWI ready: `{summary['ready_for_field_fwi']}`.",
                f"3D/HPC ready: `{summary['ready_for_3d_hpc']}`.",
                "",
                "Scope boundary:",
                "",
                "This is a CPU-only synthesis of saved field summaries. It does not",
                "provide absolute time-zero, profile spatial calibration, radius",
                "recovery, cover-depth recovery, amplitude calibration, field FWI,",
                "or 3D/HPC readiness.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_inversion_blocker_map_post_contrast")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = Path(field_dataset_output_root(args.field_root, args.dataset_id))
    source_summaries = load_source_summaries(dataset_root)
    evidence_rows = build_evidence_rows(source_summaries)
    summary = summarize_blocker_map(evidence_rows, source_summaries)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    evidence_csv = data_dir / "field_inversion_blocker_map_rows.csv"
    gates_csv = data_dir / "field_inversion_blocker_map_gates.csv"
    summary_json = data_dir / "field_inversion_blocker_map_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_inversion_blocker_map.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_blocker_map(evidence_rows, summary, figure_path)
    write_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(evidence_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_summaries": {key: str(dataset_root / rel_path) for key, rel_path in SOURCE_SUMMARIES.items()},
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "gssi_field_inversion_blocker_map",
        {
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
