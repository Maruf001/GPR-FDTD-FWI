#!/usr/bin/env python3
"""Audit local GSSI acquisition readiness for 2D QC, 3D survey, and field FWI."""

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
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


C_M_PER_NS = 0.299792458

DEFAULT_RUNS = {
    "dzt_qc": "001_gssi51600s_dzt_qc",
    "survey": "015_gssi51600s_survey_geometry_audit",
    "network": "020_gssi51600s_profile_network_alignment",
    "short_stack": "021_gssi51600s_short_profile_stack_policy",
    "long_stack": "022_gssi51600s_long_profile_stack_policy",
    "spatial_support": "047_gssi51600s_corrected_stack_spatial_support",
    "supported_interval": "049_gssi51600s_supported_interval_visual_qc",
    "event_support": "072_gssi51600s_field_event_support_tiers",
    "time_zero_budget": "075_gssi51600s_field_time_zero_uncertainty_budget",
    "time_zero_perturbation": "078_gssi51600s_field_time_zero_perturbation_sensitivity",
    "field_policy": "080_gssi51600s_field_dataset_policy_synthesis_post_time_zero_perturbation",
}


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def finite_median(values: list[float]) -> float:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    if not finite:
        return math.nan
    return float(np.median(np.asarray(finite, dtype=np.float64)))


def medium_velocity_m_per_ns(epsr: float) -> float:
    if not math.isfinite(float(epsr)) or float(epsr) <= 0.0:
        return math.nan
    return float(C_M_PER_NS / math.sqrt(float(epsr)))


def wavelength_m(antenna_frequency_mhz: float, epsr: float) -> float:
    velocity = medium_velocity_m_per_ns(epsr)
    frequency_cycles_per_ns = float(antenna_frequency_mhz) / 1000.0
    if not math.isfinite(velocity) or frequency_cycles_per_ns <= 0.0:
        return math.nan
    return float(velocity / frequency_cycles_per_ns)


def two_way_depth_equivalent_mm(time_uncertainty_ns: float, epsr: float) -> float:
    velocity = medium_velocity_m_per_ns(epsr)
    if not math.isfinite(velocity) or not math.isfinite(float(time_uncertainty_ns)):
        return math.nan
    return float(1000.0 * 0.5 * velocity * float(time_uncertainty_ns))


def acquisition_sampling_metrics(dzt_summary: dict) -> dict:
    records = list(dzt_summary.get("records", []))
    scan_spacing_m = finite_median([safe_float(row.get("scan_spacing_m")) for row in records])
    antenna_frequency_mhz = finite_median([safe_float(row.get("antenna_frequency_mhz")) for row in records])
    epsr = finite_median([safe_float(row.get("dielectric")) for row in records])
    time_range_ns = finite_median([safe_float(row.get("time_range_ns")) for row in records])
    profile_lengths = [safe_float(row.get("profile_length_m")) for row in records]
    trace_counts = [safe_float(row.get("traces")) for row in records]
    sample_counts = [safe_float(row.get("samples")) for row in records]
    lambda_m = wavelength_m(antenna_frequency_mhz, epsr)
    samples_per_wavelength = lambda_m / scan_spacing_m if scan_spacing_m > 0.0 else math.nan
    nominal_depth_m = 0.5 * medium_velocity_m_per_ns(epsr) * time_range_ns
    return {
        "profile_count": len(records),
        "dzt_file_count": int(safe_float(dzt_summary.get("dzt_file_count"), len(records))),
        "channel_count": int(safe_float(dzt_summary.get("profile_channel_count"), len(records))),
        "scan_spacing_m": scan_spacing_m,
        "scan_spacing_mm": 1000.0 * scan_spacing_m,
        "antenna_frequency_mhz": antenna_frequency_mhz,
        "dielectric": epsr,
        "medium_velocity_m_per_ns": medium_velocity_m_per_ns(epsr),
        "center_wavelength_m": lambda_m,
        "center_wavelength_mm": 1000.0 * lambda_m,
        "samples_per_wavelength": samples_per_wavelength,
        "time_range_ns": time_range_ns,
        "nominal_depth_window_m": nominal_depth_m,
        "nominal_depth_window_mm": 1000.0 * nominal_depth_m,
        "min_profile_length_m": float(np.nanmin(profile_lengths)) if profile_lengths else math.nan,
        "max_profile_length_m": float(np.nanmax(profile_lengths)) if profile_lengths else math.nan,
        "total_trace_derived_length_m": float(np.nansum(profile_lengths)) if profile_lengths else math.nan,
        "min_trace_count": int(np.nanmin(trace_counts)) if trace_counts else 0,
        "max_trace_count": int(np.nanmax(trace_counts)) if trace_counts else 0,
        "sample_count": int(finite_median(sample_counts)) if sample_counts else 0,
    }


def event_tier_lookup(event_rows: list[dict], tier_key: str) -> dict:
    for row in event_rows:
        if row.get("tier_key") == tier_key:
            return row
    return {}


def build_readiness_rows(
    sampling: dict,
    survey: dict,
    network: dict,
    short_stack: dict,
    long_stack: dict,
    spatial_support: dict,
    supported_interval: dict,
    time_zero_budget: dict,
    time_zero_perturbation: dict,
    field_policy: dict,
    event_rows: list[dict],
) -> list[dict]:
    short_summary = short_stack.get("summary", {})
    long_summary = long_stack.get("summary", {})
    short_tier = event_tier_lookup(event_rows, "short_content_time_zero_anchors")
    long_tier = event_tier_lookup(event_rows, "long_stable_pattern_anchors")
    fwi_tier = event_tier_lookup(event_rows, "field_fwi_readiness_blocked")
    samples_per_wavelength = safe_float(sampling.get("samples_per_wavelength"))
    all_support_fraction = safe_float(spatial_support.get("all_window_supported_column_fraction"))
    conservative_half_width_ns = safe_float(time_zero_budget.get("conservative_half_width_ns"))
    depth_uncertainty_mm = two_way_depth_equivalent_mm(conservative_half_width_ns, safe_float(sampling.get("dielectric")))
    return [
        {
            "audit_key": "survey_dimensionality",
            "evidence": str(survey.get("classification", "")),
            "measured_value": str(survey.get("classification", "")),
            "threshold_or_requirement": "recoverable crossline/grid metadata for 3D survey use",
            "status": "blocks_3d_hpc",
            "readiness_score": 0.0,
            "allowed_use": "independent 2D line-profile QC",
            "blocked_use": "3D survey, 3D inversion, field FWI benchmark",
        },
        {
            "audit_key": "alongline_sampling",
            "evidence": f"{sampling.get('scan_spacing_mm', math.nan):.3f} mm scan spacing",
            "measured_value": f"{samples_per_wavelength:.2f} samples per nominal wavelength",
            "threshold_or_requirement": "dense along-line samples for 2D visual/timing QC",
            "status": "supports_2d_qc",
            "readiness_score": min(1.0, samples_per_wavelength / 10.0) if math.isfinite(samples_per_wavelength) else 0.0,
            "allowed_use": "sampled 2D B-scan timing and repeatability QC",
            "blocked_use": "crossline or volumetric interpretation",
        },
        {
            "audit_key": "short_pair_repeatability",
            "evidence": str(short_summary.get("alignment_label", "")),
            "measured_value": f"{safe_float(short_summary.get('best_normalized_correlation')):.3f}",
            "threshold_or_requirement": "strong repeat pair with stable timing anchors",
            "status": "supports_short_pair_timing_qc",
            "readiness_score": safe_float(short_summary.get("best_normalized_correlation"), 0.0),
            "allowed_use": "short 014/016 relative time-zero and corrected-stack QC",
            "blocked_use": "absolute time-zero, radius, cover depth, or FWI",
        },
        {
            "audit_key": "relative_time_zero_uncertainty",
            "evidence": str(time_zero_budget.get("policy_label", "")),
            "measured_value": f"{conservative_half_width_ns:.6f} ns half-width; {depth_uncertainty_mm:.3f} mm two-way depth equivalent",
            "threshold_or_requirement": "relative uncertainty bounded away from zero, but not absolute calibration",
            "status": "relative_only",
            "readiness_score": 0.65 if not bool(time_zero_budget.get("absolute_time_zero_ready", True)) else 1.0,
            "allowed_use": "relative short-pair timing uncertainty budget",
            "blocked_use": "absolute depth/radius inversion claims",
        },
        {
            "audit_key": "time_zero_perturbation",
            "evidence": str(time_zero_perturbation.get("policy_label", "")),
            "measured_value": (
                f"{safe_float(time_zero_perturbation.get('bootstrap_ci_supported_count')):.0f}/"
                f"{safe_float(time_zero_perturbation.get('bootstrap_ci_row_count')):.0f} bootstrap rows supported"
            ),
            "threshold_or_requirement": "corrected-stack support across bootstrap-CI offsets",
            "status": "supports_uncertainty_qc",
            "readiness_score": 1.0 if safe_float(time_zero_perturbation.get("bootstrap_ci_supported_count")) == safe_float(time_zero_perturbation.get("bootstrap_ci_row_count")) else 0.5,
            "allowed_use": "uncertainty sensitivity for short-pair visual QC",
            "blocked_use": "new field inversion target",
        },
        {
            "audit_key": "spatial_support",
            "evidence": str(spatial_support.get("policy_label", "")),
            "measured_value": f"{all_support_fraction:.3f} all-window supported column fraction",
            "threshold_or_requirement": "broad spatial support for interpretation beyond visual QC",
            "status": "sparse_support",
            "readiness_score": all_support_fraction if math.isfinite(all_support_fraction) else 0.0,
            "allowed_use": "supported-interval visual QC",
            "blocked_use": "interpretation outside supported intervals",
        },
        {
            "audit_key": "supported_interval_endpoint",
            "evidence": str(supported_interval.get("policy_label", "")),
            "measured_value": f"{safe_float(supported_interval.get('total_selected_interval_length_m')):.5f} m selected",
            "threshold_or_requirement": "all selected intervals must be supported",
            "status": "supports_visual_endpoint",
            "readiness_score": 1.0 if safe_float(supported_interval.get("selected_interval_count")) == safe_float(supported_interval.get("supported_interval_count")) else 0.5,
            "allowed_use": "field visual-QC figure endpoint",
            "blocked_use": "full-profile field inversion",
        },
        {
            "audit_key": "long_pair_phase_support",
            "evidence": str(long_summary.get("alignment_label", "")),
            "measured_value": f"missing phase anchors={bool(long_summary.get('comparison_profile_missing_phase_anchor_picks', True))}",
            "threshold_or_requirement": "usable phase-anchor picks on both long profiles",
            "status": "pattern_only",
            "readiness_score": 0.0 if bool(long_summary.get("comparison_profile_missing_phase_anchor_picks", True)) else 0.5,
            "allowed_use": str(long_tier.get("claim_allowed", "long-pair pattern-only QC")),
            "blocked_use": str(long_tier.get("claim_blocked", "phase-anchor or absolute time-zero evidence")),
        },
        {
            "audit_key": "event_support_tiers",
            "evidence": f"{len(event_rows)} support-tier rows",
            "measured_value": f"short={short_tier.get('support_fraction', '')}; long={long_tier.get('support_fraction', '')}",
            "threshold_or_requirement": "claim-specific support tiers before publication use",
            "status": "claim_tiers_ready",
            "readiness_score": 1.0 if event_rows else 0.0,
            "allowed_use": "claim-boundary table",
            "blocked_use": "collapsing field QC into synthetic confidence labels",
        },
        {
            "audit_key": "field_fwi_readiness",
            "evidence": str(fwi_tier.get("support_tier", "blocked_not_ready")),
            "measured_value": str(field_policy.get("policy_label", "")),
            "threshold_or_requirement": "absolute time zero, geometry, target ground truth, and broad support",
            "status": "blocked",
            "readiness_score": 0.0,
            "allowed_use": "none; keep field GPU/FWI priority at none",
            "blocked_use": "field FWI, 3D inversion, radius, and cover-depth claims",
        },
        {
            "audit_key": "hpc_priority",
            "evidence": "field-side heavy compute gate",
            "measured_value": "none",
            "threshold_or_requirement": "new calibrated acquisition or external survey geometry metadata",
            "status": "do_not_submit_field_hpc_job",
            "readiness_score": 0.0,
            "allowed_use": "local CPU-side field QC synthesis",
            "blocked_use": "NERSC/A100 field-data FWI or 3D job from this dataset",
        },
    ]


def summarize_readiness(readiness_rows: list[dict], sampling: dict, survey: dict, time_zero_budget: dict, spatial_support: dict) -> dict:
    status_by_key = {row["audit_key"]: row["status"] for row in readiness_rows}
    ready_for_3d = status_by_key.get("survey_dimensionality") != "blocks_3d_hpc"
    ready_for_field_fwi = status_by_key.get("field_fwi_readiness") != "blocked"
    conservative_half_width_ns = safe_float(time_zero_budget.get("conservative_half_width_ns"))
    depth_uncertainty_mm = two_way_depth_equivalent_mm(conservative_half_width_ns, safe_float(sampling.get("dielectric")))
    policy_label = (
        "field_acquisition_readiness_2d_qc_not_hpc_fwi"
        if not ready_for_3d and not ready_for_field_fwi
        else "field_acquisition_readiness_review_needed"
    )
    decision = (
        "The local GSSI 51600S field data are dense along-line 2D profiles, "
        "not a 3D or field-FWI workload. The scan spacing is small relative "
        "to the nominal in-medium wavelength, so the data remain useful for "
        "2D visual/timing QC. However, missing crossline/grid metadata, "
        "relative-only time-zero calibration, sparse all-window spatial "
        "support, and long-profile pattern-only evidence block heavy field "
        "FWI or 3D HPC submission from this dataset."
    )
    return {
        "policy_label": policy_label,
        "decision": decision,
        "survey_classification": survey.get("classification", ""),
        "profile_count": sampling.get("profile_count", 0),
        "dzt_file_count": sampling.get("dzt_file_count", 0),
        "scan_spacing_mm": sampling.get("scan_spacing_mm", math.nan),
        "antenna_frequency_mhz": sampling.get("antenna_frequency_mhz", math.nan),
        "dielectric": sampling.get("dielectric", math.nan),
        "medium_velocity_m_per_ns": sampling.get("medium_velocity_m_per_ns", math.nan),
        "center_wavelength_mm": sampling.get("center_wavelength_mm", math.nan),
        "samples_per_wavelength": sampling.get("samples_per_wavelength", math.nan),
        "nominal_depth_window_mm": sampling.get("nominal_depth_window_mm", math.nan),
        "min_profile_length_m": sampling.get("min_profile_length_m", math.nan),
        "max_profile_length_m": sampling.get("max_profile_length_m", math.nan),
        "total_trace_derived_length_m": sampling.get("total_trace_derived_length_m", math.nan),
        "time_zero_conservative_half_width_ns": conservative_half_width_ns,
        "time_zero_two_way_depth_equivalent_mm": depth_uncertainty_mm,
        "spatial_all_window_supported_fraction": safe_float(
            spatial_support.get("all_window_supported_column_fraction")
        ),
        "spatial_all_window_supported_column_count": safe_float(
            spatial_support.get("all_window_supported_column_count")
        ),
        "spatial_finite_column_count": safe_float(spatial_support.get("finite_column_count")),
        "readiness_row_count": len(readiness_rows),
        "ready_for_2d_qc": True,
        "ready_for_3d_hpc": bool(ready_for_3d),
        "ready_for_field_fwi": bool(ready_for_field_fwi),
        "field_hpc_priority": "none",
        "recommended_next": (
            "Use this dataset as measured 2D timing/repeatability QC and "
            "publication boundary evidence. Field-side HPC should wait for "
            "external survey-layout metadata, calibrated target geometry, or "
            "a new controlled acquisition."
        ),
    }


def plot_readiness(readiness_rows: list[dict], summary: dict, save_path: Path) -> None:
    selected_keys = [
        "alongline_sampling",
        "short_pair_repeatability",
        "relative_time_zero_uncertainty",
        "time_zero_perturbation",
        "spatial_support",
        "long_pair_phase_support",
        "survey_dimensionality",
        "field_fwi_readiness",
        "hpc_priority",
    ]
    rows_by_key = {row["audit_key"]: row for row in readiness_rows}
    plot_rows = [rows_by_key[key] for key in selected_keys if key in rows_by_key]
    labels = [row["audit_key"].replace("_", "\n") for row in plot_rows]
    scores = [float(row["readiness_score"]) for row in plot_rows]
    colors = [
        "#2f9d55" if score >= 0.75 else "#d99a19" if score >= 0.35 else "#c7302b"
        for score in scores
    ]

    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    x = np.arange(len(plot_rows))
    axes[0].bar(x, scores, color=colors, edgecolor="#333333", linewidth=0.6)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_ylabel("readiness score")
    axes[0].set_title("Field acquisition readiness by evidence gate")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    decision_labels = ["2D QC", "3D HPC", "field FWI", "field HPC priority"]
    decision_scores = [
        1.0 if summary["ready_for_2d_qc"] else 0.0,
        1.0 if summary["ready_for_3d_hpc"] else 0.0,
        1.0 if summary["ready_for_field_fwi"] else 0.0,
        0.0,
    ]
    decision_colors = ["#2f9d55", "#c7302b", "#c7302b", "#c7302b"]
    axes[1].bar(np.arange(len(decision_labels)), decision_scores, color=decision_colors, edgecolor="#333333")
    axes[1].set_xticks(np.arange(len(decision_labels)), decision_labels)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_title("Allowed use decision")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.94,
        (
            f"spacing={summary['scan_spacing_mm']:.3f} mm, "
            f"lambda={summary['center_wavelength_mm']:.1f} mm\n"
            f"time-zero half-width={summary['time_zero_conservative_half_width_ns']:.3f} ns "
            f"({summary['time_zero_two_way_depth_equivalent_mm']:.1f} mm depth eq.)\n"
            f"all-window spatial support={summary['spatial_all_window_supported_fraction']:.3f}"
        ),
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#aaaaaa"},
    )
    fig.suptitle("Local GSSI field acquisition readiness audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def load_inputs(dataset_root: Path, runs: dict) -> tuple[dict, list[dict]]:
    data = {
        "dzt": read_json(dataset_root / runs["dzt_qc"] / "data" / "gssi_dzt_qc_summary.json"),
        "survey": read_json(dataset_root / runs["survey"] / "data" / "survey_geometry_audit_summary.json"),
        "network": read_json(dataset_root / runs["network"] / "data" / "profile_network_alignment_summary.json"),
        "short_stack": read_json(dataset_root / runs["short_stack"] / "data" / "short_profile_stack_policy_summary.json"),
        "long_stack": read_json(dataset_root / runs["long_stack"] / "data" / "long_profile_stack_policy_summary.json"),
        "spatial_support": read_json(dataset_root / runs["spatial_support"] / "data" / "corrected_stack_spatial_support_summary.json"),
        "supported_interval": read_json(dataset_root / runs["supported_interval"] / "data" / "supported_interval_visual_qc_summary.json"),
        "time_zero_budget": read_json(dataset_root / runs["time_zero_budget"] / "data" / "field_time_zero_uncertainty_budget_summary.json"),
        "time_zero_perturbation": read_json(dataset_root / runs["time_zero_perturbation"] / "data" / "field_time_zero_perturbation_sensitivity_summary.json"),
        "field_policy": read_json(dataset_root / runs["field_policy"] / "data" / "field_dataset_policy_summary.json"),
    }
    event_rows = read_csv_rows(dataset_root / runs["event_support"] / "data" / "field_event_support_tiers.csv")
    return data, event_rows


def build_audit(data: dict, event_rows: list[dict]) -> tuple[list[dict], dict]:
    sampling = acquisition_sampling_metrics(data["dzt"])
    readiness_rows = build_readiness_rows(
        sampling=sampling,
        survey=data["survey"],
        network=data["network"],
        short_stack=data["short_stack"],
        long_stack=data["long_stack"],
        spatial_support=data["spatial_support"],
        supported_interval=data["supported_interval"],
        time_zero_budget=data["time_zero_budget"],
        time_zero_perturbation=data["time_zero_perturbation"],
        field_policy=data["field_policy"],
        event_rows=event_rows,
    )
    summary = summarize_readiness(
        readiness_rows=readiness_rows,
        sampling=sampling,
        survey=data["survey"],
        time_zero_budget=data["time_zero_budget"],
        spatial_support=data["spatial_support"],
    )
    return readiness_rows, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_acquisition_readiness_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    data, event_rows = load_inputs(dataset_root, DEFAULT_RUNS)
    readiness_rows, summary = build_audit(data, event_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_acquisition_readiness_rows.csv"
    summary_json = data_dir / "field_acquisition_readiness_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_acquisition_readiness_audit.png"

    plot_readiness(readiness_rows, summary, figure_path)
    write_csv(rows_csv, [json_safe(row) for row in readiness_rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_acquisition_readiness_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
