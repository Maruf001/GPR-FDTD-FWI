#!/usr/bin/env python3
"""Build a field publication claim bundle from existing GSSI QC outputs."""

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
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_GEOMETRY_RUN = "015_gssi51600s_survey_geometry_audit"
DEFAULT_SHORT_WAVEFORM_RUN = "035_gssi51600s_content_backed_waveform_panels"
DEFAULT_SHORT_STACK_RUN = "049_gssi51600s_supported_interval_visual_qc"
DEFAULT_LONG_VISUAL_RUN = "057_gssi51600s_long_profile_pattern_visual_qc"
DEFAULT_LONG_HOLDOUT_RUN = "058_gssi51600s_long_profile_pattern_holdout_qc"
DEFAULT_LONG_WINDOW_SENSITIVITY_RUN = "060_gssi51600s_long_profile_pattern_holdout_sensitivity"
DEFAULT_LONG_WIDTH_SENSITIVITY_RUN = "061_gssi51600s_long_profile_pattern_holdout_width_sensitivity"
DEFAULT_LONG_RELAXED_PHASE_ANCHOR_RUN = "064_gssi51600s_long_profiles_relaxed_phase_anchor_audit"
DEFAULT_BANDLIMITED_RUN = "068_gssi51600s_field_bandlimited_repeatability_audit"
DEFAULT_EVENT_SUPPORT_RUN = "110_gssi51600s_field_event_support_tiers_post_timing_discriminant_hpc"
DEFAULT_TIME_ZERO_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_TIME_ZERO_PERTURBATION_RUN = "078_gssi51600s_field_time_zero_perturbation_sensitivity"
DEFAULT_ACQUISITION_READINESS_RUN = "081_gssi51600s_field_acquisition_readiness_audit"
DEFAULT_APPARENT_DEPTH_QC_RUN = "084_gssi51600s_field_apparent_depth_qc"
DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN = "085_gssi51600s_field_apparent_depth_sensitivity"
DEFAULT_HYPERBOLA_TIMEZERO_DEGENERACY_RUN = "086_gssi51600s_field_hyperbola_timezero_degeneracy_audit"
DEFAULT_EARLY_TIME_ANCHOR_RUN = "090_gssi51600s_field_early_time_anchor_audit"
DEFAULT_CUE_SPACING_SENSITIVITY_RUN = "094_gssi51600s_field_cue_spacing_sensitivity_audit"
DEFAULT_TIMING_ANCHOR_CONFLICT_RUN = "097_gssi51600s_field_timing_anchor_conflict_synthesis"
DEFAULT_TIMING_WINDOW_FAMILY_RUN = "101_gssi51600s_field_timing_window_family_classification"
DEFAULT_TIMING_DISCRIMINANT_RUN = "105_gssi51600s_field_timing_discriminant_scorecard"
DEFAULT_HPC_DIMENSIONALITY_RUN = "106_gssi51600s_field_hpc_dimensionality_decision_card"
DEFAULT_SHORT_WAVEFORM_COHERENCE_RUN = "124_gssi51600s_field_short_anchor_waveform_coherence_audit"
DEFAULT_SHORT_RADIUS_DEGENERACY_RUN = "125_gssi51600s_field_short_anchor_radius_degeneracy_audit"
DEFAULT_SHORT_SIGNED_MORPHOLOGY_RUN = "126_gssi51600s_field_short_anchor_signed_morphology_audit"
DEFAULT_SHORT_SIGNED_MORPHOLOGY_SENSITIVITY_RUN = "127_gssi51600s_field_short_anchor_signed_morphology_sensitivity"
DEFAULT_SHORT_SIGNED_MORPHOLOGY_TIMING_MARGIN_RUN = "129_gssi51600s_field_short_anchor_signed_morphology_timing_margin"
DEFAULT_SHORT_SIGNAL_CONTRAST_RUN = "131_gssi51600s_field_short_anchor_signal_contrast_audit"
DEFAULT_SHORT_SIGNAL_CONTRAST_SENSITIVITY_RUN = "132_gssi51600s_field_short_anchor_signal_contrast_sensitivity"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_optional_json(path: Path) -> dict:
    if not Path(path).exists():
        return {}
    return read_json(path)


def source_run_from_summary(summary: dict, fallback: str) -> str:
    summary_path = summary.get("paths", {}).get("summary_json", "")
    if summary_path:
        try:
            return Path(summary_path).parents[1].name
        except IndexError:
            return fallback
    return fallback


def load_field_summaries(dataset_root: Path, runs: dict[str, str]) -> dict[str, dict]:
    summaries = {
        "geometry": read_json(dataset_root / runs["geometry"] / "data" / "survey_geometry_audit_summary.json"),
        "short_waveform": read_json(
            dataset_root
            / runs["short_waveform"]
            / "data"
            / "content_backed_waveform_panel_summary.json"
        ),
        "short_stack": read_json(
            dataset_root
            / runs["short_stack"]
            / "data"
            / "supported_interval_visual_qc_summary.json"
        ),
        "long_visual": read_json(
            dataset_root
            / runs["long_visual"]
            / "data"
            / "long_profile_pattern_visual_qc_summary.json"
        ),
        "long_holdout": read_json(
            dataset_root
            / runs["long_holdout"]
            / "data"
            / "long_profile_pattern_holdout_qc_summary.json"
        ),
        "long_window_sensitivity": read_json(
            dataset_root
            / runs["long_window_sensitivity"]
            / "data"
            / "long_profile_pattern_holdout_sensitivity_summary.json"
        ),
        "long_width_sensitivity": read_json(
            dataset_root
            / runs["long_width_sensitivity"]
            / "data"
            / "long_profile_pattern_holdout_width_sensitivity_summary.json"
        ),
    }
    relaxed_run = runs.get("long_relaxed_phase_anchor", "")
    if relaxed_run:
        relaxed = read_optional_json(
            dataset_root
            / relaxed_run
            / "data"
            / "field_phase_anchor_summary.json"
        )
        if relaxed:
            summaries["long_relaxed_phase_anchor"] = relaxed
    bandlimited_run = runs.get("bandlimited_repeatability", "")
    if bandlimited_run:
        bandlimited = read_optional_json(
            dataset_root
            / bandlimited_run
            / "data"
            / "field_bandlimited_repeatability_summary.json"
        )
        if bandlimited:
            summaries["bandlimited_repeatability"] = bandlimited
    event_support_run = runs.get("event_support_tiers", "")
    if event_support_run:
        event_support = read_optional_json(
            dataset_root
            / event_support_run
            / "data"
            / "field_event_support_tiers_summary.json"
        )
        if event_support:
            summaries["event_support_tiers"] = event_support
    time_zero_budget_run = runs.get("time_zero_uncertainty", "")
    if time_zero_budget_run:
        time_zero_budget = read_optional_json(
            dataset_root
            / time_zero_budget_run
            / "data"
            / "field_time_zero_uncertainty_budget_summary.json"
        )
        if time_zero_budget:
            summaries["time_zero_uncertainty"] = time_zero_budget
    time_zero_perturbation_run = runs.get("time_zero_perturbation", "")
    if time_zero_perturbation_run:
        time_zero_perturbation = read_optional_json(
            dataset_root
            / time_zero_perturbation_run
            / "data"
            / "field_time_zero_perturbation_sensitivity_summary.json"
        )
        if time_zero_perturbation:
            summaries["time_zero_perturbation"] = time_zero_perturbation
    acquisition_run = runs.get("acquisition_readiness", "")
    if acquisition_run:
        acquisition = read_optional_json(
            dataset_root
            / acquisition_run
            / "data"
            / "field_acquisition_readiness_summary.json"
        )
        if acquisition:
            summaries["acquisition_readiness"] = acquisition
    apparent_depth_run = runs.get("apparent_depth_qc", "")
    if apparent_depth_run:
        apparent_depth = read_optional_json(
            dataset_root
            / apparent_depth_run
            / "data"
            / "field_apparent_depth_qc_summary.json"
        )
        if apparent_depth:
            summaries["apparent_depth_qc"] = apparent_depth
    apparent_depth_sensitivity_run = runs.get("apparent_depth_sensitivity", "")
    if apparent_depth_sensitivity_run:
        apparent_depth_sensitivity = read_optional_json(
            dataset_root
            / apparent_depth_sensitivity_run
            / "data"
            / "field_apparent_depth_sensitivity_summary.json"
        )
        if apparent_depth_sensitivity:
            summaries["apparent_depth_sensitivity"] = apparent_depth_sensitivity
    hyperbola_timezero_run = runs.get("hyperbola_timezero_degeneracy", "")
    if hyperbola_timezero_run:
        hyperbola_timezero = read_optional_json(
            dataset_root
            / hyperbola_timezero_run
            / "data"
            / "field_hyperbola_timezero_degeneracy_summary.json"
        )
        if hyperbola_timezero:
            summaries["hyperbola_timezero_degeneracy"] = hyperbola_timezero
    early_time_run = runs.get("early_time_anchor", "")
    if early_time_run:
        early_time = read_optional_json(
            dataset_root
            / early_time_run
            / "data"
            / "field_early_time_anchor_audit_summary.json"
        )
        if early_time:
            summaries["early_time_anchor"] = early_time
    cue_spacing_run = runs.get("cue_spacing_sensitivity", "")
    if cue_spacing_run:
        cue_spacing = read_optional_json(
            dataset_root
            / cue_spacing_run
            / "data"
            / "field_cue_spacing_threshold_sensitivity_summary.json"
        )
        if cue_spacing:
            summaries["cue_spacing_sensitivity"] = cue_spacing
    timing_anchor_run = runs.get("timing_anchor_conflict", "")
    if timing_anchor_run:
        timing_anchor = read_optional_json(
            dataset_root
            / timing_anchor_run
            / "data"
            / "field_timing_anchor_conflict_summary.json"
        )
        if timing_anchor:
            summaries["timing_anchor_conflict"] = timing_anchor
    timing_window_run = runs.get("timing_window_family", "")
    if timing_window_run:
        timing_window = read_optional_json(
            dataset_root
            / timing_window_run
            / "data"
            / "field_timing_window_family_classification_summary.json"
        )
        if timing_window:
            summaries["timing_window_family"] = timing_window
    timing_discriminant_run = runs.get("timing_discriminant", "")
    if timing_discriminant_run:
        timing_discriminant = read_optional_json(
            dataset_root
            / timing_discriminant_run
            / "data"
            / "field_timing_discriminant_scorecard_summary.json"
        )
        if timing_discriminant:
            summaries["timing_discriminant"] = timing_discriminant
    hpc_dimensionality_run = runs.get("hpc_dimensionality", "")
    if hpc_dimensionality_run:
        hpc_dimensionality = read_optional_json(
            dataset_root
            / hpc_dimensionality_run
            / "data"
            / "field_hpc_dimensionality_decision_summary.json"
        )
        if hpc_dimensionality:
            summaries["hpc_dimensionality"] = hpc_dimensionality
    short_waveform_coherence_run = runs.get("short_waveform_coherence", "")
    if short_waveform_coherence_run:
        short_waveform_coherence = read_optional_json(
            dataset_root
            / short_waveform_coherence_run
            / "data"
            / "field_short_anchor_waveform_coherence_summary.json"
        )
        if short_waveform_coherence:
            summaries["short_waveform_coherence"] = short_waveform_coherence
    short_radius_degeneracy_run = runs.get("short_radius_degeneracy", "")
    if short_radius_degeneracy_run:
        short_radius_degeneracy = read_optional_json(
            dataset_root
            / short_radius_degeneracy_run
            / "data"
            / "field_short_anchor_radius_degeneracy_summary.json"
        )
        if short_radius_degeneracy:
            summaries["short_radius_degeneracy"] = short_radius_degeneracy
    short_signed_morphology_run = runs.get("short_signed_morphology", "")
    if short_signed_morphology_run:
        short_signed_morphology = read_optional_json(
            dataset_root
            / short_signed_morphology_run
            / "data"
            / "field_short_anchor_signed_morphology_summary.json"
        )
        if short_signed_morphology:
            summaries["short_signed_morphology"] = short_signed_morphology
    short_signed_morphology_sensitivity_run = runs.get("short_signed_morphology_sensitivity", "")
    if short_signed_morphology_sensitivity_run:
        short_signed_morphology_sensitivity = read_optional_json(
            dataset_root
            / short_signed_morphology_sensitivity_run
            / "data"
            / "field_short_anchor_signed_morphology_sensitivity_summary.json"
        )
        if short_signed_morphology_sensitivity:
            summaries["short_signed_morphology_sensitivity"] = short_signed_morphology_sensitivity
    short_signed_morphology_timing_margin_run = runs.get("short_signed_morphology_timing_margin", "")
    if short_signed_morphology_timing_margin_run:
        short_signed_morphology_timing_margin = read_optional_json(
            dataset_root
            / short_signed_morphology_timing_margin_run
            / "data"
            / "field_short_anchor_signed_morphology_timing_margin_summary.json"
        )
        if short_signed_morphology_timing_margin:
            summaries["short_signed_morphology_timing_margin"] = short_signed_morphology_timing_margin
    short_signal_contrast_run = runs.get("short_signal_contrast", "")
    if short_signal_contrast_run:
        short_signal_contrast = read_optional_json(
            dataset_root
            / short_signal_contrast_run
            / "data"
            / "field_short_anchor_signal_contrast_summary.json"
        )
        if short_signal_contrast:
            summaries["short_signal_contrast"] = short_signal_contrast
    short_signal_contrast_sensitivity_run = runs.get("short_signal_contrast_sensitivity", "")
    if short_signal_contrast_sensitivity_run:
        short_signal_contrast_sensitivity = read_optional_json(
            dataset_root
            / short_signal_contrast_sensitivity_run
            / "data"
            / "field_short_anchor_signal_contrast_sensitivity_summary.json"
        )
        if short_signal_contrast_sensitivity:
            summaries["short_signal_contrast_sensitivity"] = short_signal_contrast_sensitivity
    return summaries


def relaxed_phase_anchor_policy(summary: dict) -> str:
    pick_count = safe_float(summary.get("phase_anchor_pick_count"), 0.0)
    low_snr_count = safe_float(summary.get("low_snr_phase_anchor_pick_count"), 0.0)
    boundary_count = safe_float(
        summary.get("best_phase_hypothesis", {}).get("boundary_solution_count"),
        0.0,
    )
    if pick_count > 0 and low_snr_count >= pick_count:
        return "long_profile_relaxed_phase_anchor_low_snr_not_time_zero"
    if boundary_count > 0:
        return "long_profile_relaxed_phase_anchor_boundary_limited"
    return "long_profile_relaxed_phase_anchor_review"


def figure_rows(summaries: dict[str, dict]) -> list[dict]:
    rows = [
        {
            "figure_key": "survey_geometry_boundary",
            "source_run": DEFAULT_GEOMETRY_RUN,
            "policy_label": summaries["geometry"].get("classification", ""),
            "metric_label": "profile_count",
            "metric_value": safe_float(summaries["geometry"].get("profile_count")),
            "figure_path": summaries["geometry"].get("paths", {}).get("plot", ""),
            "allowed_use": "2D line-profile geometry boundary",
        },
        {
            "figure_key": "short_content_waveform_qc",
            "source_run": DEFAULT_SHORT_WAVEFORM_RUN,
            "policy_label": summaries["short_waveform"].get("policy_label", ""),
            "metric_label": "min_abs_corr",
            "metric_value": safe_float(summaries["short_waveform"].get("min_absolute_correlation")),
            "figure_path": summaries["short_waveform"].get("paths", {}).get("figure", ""),
            "allowed_use": "short-profile content-backed field-to-synthetic QC",
        },
        {
            "figure_key": "short_supported_stack_intervals",
            "source_run": DEFAULT_SHORT_STACK_RUN,
            "policy_label": summaries["short_stack"].get("policy_label", ""),
            "metric_label": "min_corrected_interval_abs_corr",
            "metric_value": safe_float(summaries["short_stack"].get("min_corrected_interval_abs_correlation")),
            "figure_path": summaries["short_stack"].get("paths", {}).get("figure", ""),
            "allowed_use": "short-profile supported corrected-stack interval QC",
        },
        {
            "figure_key": "long_pattern_visual_qc",
            "source_run": DEFAULT_LONG_VISUAL_RUN,
            "policy_label": summaries["long_visual"].get("policy_label", ""),
            "metric_label": "min_shifted_abs_corr",
            "metric_value": safe_float(summaries["long_visual"].get("min_pattern_shift_abs_correlation")),
            "figure_path": summaries["long_visual"].get("paths", {}).get("figure", ""),
            "allowed_use": "long-profile pattern-only visual QC",
        },
        {
            "figure_key": "long_pattern_holdout_qc",
            "source_run": DEFAULT_LONG_HOLDOUT_RUN,
            "policy_label": summaries["long_holdout"].get("policy_label", ""),
            "metric_label": "repeat_limited_supported",
            "metric_value": safe_float(summaries["long_holdout"].get("repeat_limited_supported_anchor_count")),
            "figure_path": summaries["long_holdout"].get("paths", {}).get("figure", ""),
            "allowed_use": "long-profile repeat-limited anchor holdout QC",
        },
        {
            "figure_key": "long_pattern_window_sensitivity",
            "source_run": DEFAULT_LONG_WINDOW_SENSITIVITY_RUN,
            "policy_label": summaries["long_window_sensitivity"].get("policy_label", ""),
            "metric_label": "all_window_supported_anchor_count",
            "metric_value": safe_float(
                summaries["long_window_sensitivity"].get("all_window_supported_anchor_count")
            ),
            "figure_path": summaries["long_window_sensitivity"].get("paths", {}).get("figure", ""),
            "allowed_use": "long-profile pattern-only QC time-window sensitivity",
        },
        {
            "figure_key": "long_pattern_width_sensitivity",
            "source_run": DEFAULT_LONG_WIDTH_SENSITIVITY_RUN,
            "policy_label": summaries["long_width_sensitivity"].get("policy_label", ""),
            "metric_label": "all_width_supported_anchor_count",
            "metric_value": safe_float(
                summaries["long_width_sensitivity"].get("all_width_supported_anchor_count")
            ),
            "figure_path": summaries["long_width_sensitivity"].get("paths", {}).get("figure", ""),
            "allowed_use": "long-profile pattern-only QC spatial-width sensitivity",
        },
    ]
    short_waveform_coherence = summaries.get("short_waveform_coherence", {})
    if short_waveform_coherence:
        rows.append(
            {
                "figure_key": "field_short_anchor_waveform_coherence_qc",
                "source_run": source_run_from_summary(
                    short_waveform_coherence,
                    DEFAULT_SHORT_WAVEFORM_COHERENCE_RUN,
                ),
                "policy_label": short_waveform_coherence.get("policy_label", ""),
                "metric_label": "min_corrected_abs_corr",
                "metric_value": safe_float(
                    short_waveform_coherence.get("min_corrected_field_trace_abs_correlation")
                ),
                "figure_path": short_waveform_coherence.get("paths", {}).get("figure", ""),
                "allowed_use": "short-anchor waveform morphology QC guardrail",
            }
        )
    short_radius_degeneracy = summaries.get("short_radius_degeneracy", {})
    if short_radius_degeneracy:
        rows.append(
            {
                "figure_key": "field_short_anchor_radius_degeneracy_guardrail",
                "source_run": source_run_from_summary(
                    short_radius_degeneracy,
                    DEFAULT_SHORT_RADIUS_DEGENERACY_RUN,
                ),
                "policy_label": short_radius_degeneracy.get("policy_label", ""),
                "metric_label": "weak_radius_side_count",
                "metric_value": safe_float(short_radius_degeneracy.get("weak_radius_side_count")),
                "figure_path": short_radius_degeneracy.get("paths", {}).get("figure", ""),
                "allowed_use": "short-anchor radius-degeneracy blocker for morphology QC",
            }
        )
    short_signed_morphology = summaries.get("short_signed_morphology", {})
    if short_signed_morphology:
        rows.append(
            {
                "figure_key": "field_short_anchor_signed_morphology_qc",
                "source_run": source_run_from_summary(
                    short_signed_morphology,
                    DEFAULT_SHORT_SIGNED_MORPHOLOGY_RUN,
                ),
                "policy_label": short_signed_morphology.get("policy_label", ""),
                "metric_label": "min_corrected_signed_corr",
                "metric_value": safe_float(
                    short_signed_morphology.get("min_corrected_signed_correlation")
                ),
                "figure_path": short_signed_morphology.get("paths", {}).get("figure", ""),
                "allowed_use": "signed short-anchor waveform morphology QC",
            }
        )
    short_signed_sensitivity = summaries.get("short_signed_morphology_sensitivity", {})
    if short_signed_sensitivity:
        rows.append(
            {
                "figure_key": "field_short_anchor_signed_morphology_threshold_sensitivity",
                "source_run": source_run_from_summary(
                    short_signed_sensitivity,
                    DEFAULT_SHORT_SIGNED_MORPHOLOGY_SENSITIVITY_RUN,
                ),
                "policy_label": short_signed_sensitivity.get("policy_label", ""),
                "metric_label": "supported_threshold_combos",
                "metric_value": safe_float(
                    short_signed_sensitivity.get("all_pairs_supported_threshold_combo_count")
                ),
                "figure_path": short_signed_sensitivity.get("paths", {}).get("figure", ""),
                "allowed_use": "threshold-margin sensitivity for signed morphology QC",
            }
        )
    short_signed_timing_margin = summaries.get("short_signed_morphology_timing_margin", {})
    if short_signed_timing_margin:
        rows.append(
            {
                "figure_key": "field_short_anchor_signed_morphology_timing_margin",
                "source_run": source_run_from_summary(
                    short_signed_timing_margin,
                    DEFAULT_SHORT_SIGNED_MORPHOLOGY_TIMING_MARGIN_RUN,
                ),
                "policy_label": short_signed_timing_margin.get("policy_label", ""),
                "metric_label": "min_default_timing_slack_ns",
                "metric_value": safe_float(short_signed_timing_margin.get("min_default_timing_slack_ns")),
                "figure_path": short_signed_timing_margin.get("paths", {}).get("figure", ""),
                "allowed_use": "content-only signed morphology timing-margin QC",
            }
        )
    short_signal_contrast = summaries.get("short_signal_contrast", {})
    if short_signal_contrast:
        rows.append(
            {
                "figure_key": "field_short_anchor_signal_contrast_qc",
                "source_run": source_run_from_summary(
                    short_signal_contrast,
                    DEFAULT_SHORT_SIGNAL_CONTRAST_RUN,
                ),
                "policy_label": short_signal_contrast.get("policy_label", ""),
                "metric_label": "min_event_to_noise_rms",
                "metric_value": safe_float(short_signal_contrast.get("min_event_to_noise_rms")),
                "figure_path": short_signal_contrast.get("paths", {}).get("figure", ""),
                "allowed_use": "default-window short-anchor signal-contrast QC",
            }
        )
    short_signal_contrast_sensitivity = summaries.get("short_signal_contrast_sensitivity", {})
    if short_signal_contrast_sensitivity:
        rows.append(
            {
                "figure_key": "field_short_anchor_signal_contrast_sensitivity",
                "source_run": source_run_from_summary(
                    short_signal_contrast_sensitivity,
                    DEFAULT_SHORT_SIGNAL_CONTRAST_SENSITIVITY_RUN,
                ),
                "policy_label": short_signal_contrast_sensitivity.get("policy_label", ""),
                "metric_label": "all_supported_combo_count",
                "metric_value": safe_float(
                    short_signal_contrast_sensitivity.get("all_supported_combo_count")
                ),
                "figure_path": short_signal_contrast_sensitivity.get("paths", {}).get("figure", ""),
                "allowed_use": "signal-contrast window-sensitivity guardrail",
            }
        )
    relaxed = summaries.get("long_relaxed_phase_anchor", {})
    if relaxed:
        rows.append(
            {
                "figure_key": "long_relaxed_phase_anchor_negative_qc",
                "source_run": DEFAULT_LONG_RELAXED_PHASE_ANCHOR_RUN,
                "policy_label": relaxed_phase_anchor_policy(relaxed),
                "metric_label": "low_snr_pick_count",
                "metric_value": safe_float(relaxed.get("low_snr_phase_anchor_pick_count")),
                "figure_path": relaxed.get("figures", {}).get("convention_summary", ""),
                "allowed_use": "long-profile relaxed phase-anchor negative QC",
            }
        )
    bandlimited = summaries.get("bandlimited_repeatability", {})
    if bandlimited:
        rows.append(
            {
                "figure_key": "field_bandlimited_repeatability_qc",
                "source_run": DEFAULT_BANDLIMITED_RUN,
                "policy_label": bandlimited.get("policy_label", ""),
                "metric_label": "short_supported_band_count",
                "metric_value": safe_float(bandlimited.get("short_supported_band_count")),
                "figure_path": bandlimited.get("paths", {}).get("figure", ""),
                "allowed_use": "field band-limited repeatability QC",
            }
        )
    event_support = summaries.get("event_support_tiers", {})
    if event_support:
        rows.append(
            {
                "figure_key": "field_event_support_tiers",
                "source_run": source_run_from_summary(event_support, DEFAULT_EVENT_SUPPORT_RUN),
                "policy_label": event_support.get("policy_label", ""),
                "metric_label": "tier_row_count",
                "metric_value": safe_float(event_support.get("tier_row_count")),
                "figure_path": event_support.get("paths", {}).get("figure", ""),
                "allowed_use": "measured-field event support tier table",
            }
        )
    time_zero = summaries.get("time_zero_uncertainty", {})
    if time_zero:
        rows.append(
            {
                "figure_key": "field_time_zero_uncertainty_budget",
                "source_run": DEFAULT_TIME_ZERO_BUDGET_RUN,
                "policy_label": time_zero.get("policy_label", ""),
                "metric_label": "conservative_half_width_ns",
                "metric_value": safe_float(time_zero.get("conservative_half_width_ns")),
                "figure_path": time_zero.get("paths", {}).get("figure", ""),
                "allowed_use": "short-profile relative time-zero uncertainty budget",
            }
        )
    time_zero_perturbation = summaries.get("time_zero_perturbation", {})
    if time_zero_perturbation:
        rows.append(
            {
                "figure_key": "field_time_zero_perturbation_sensitivity",
                "source_run": DEFAULT_TIME_ZERO_PERTURBATION_RUN,
                "policy_label": time_zero_perturbation.get("policy_label", ""),
                "metric_label": "bootstrap_ci_supported_count",
                "metric_value": safe_float(time_zero_perturbation.get("bootstrap_ci_supported_count")),
                "figure_path": time_zero_perturbation.get("paths", {}).get("figure", ""),
                "allowed_use": "short-profile time-zero perturbation sensitivity QC",
            }
        )
    early_time = summaries.get("early_time_anchor", {})
    if early_time:
        rows.append(
            {
                "figure_key": "field_early_time_anchor_negative_qc",
                "source_run": DEFAULT_EARLY_TIME_ANCHOR_RUN,
                "policy_label": early_time.get("policy_label", ""),
                "metric_label": "short_early_vs_content_delta_ns",
                "metric_value": safe_float(early_time.get("short_pair_early_vs_content_delta_ns")),
                "figure_path": early_time.get("paths", {}).get("figure", ""),
                "allowed_use": "early-time common-mode negative QC for absolute time-zero",
            }
        )
    timing_anchor = summaries.get("timing_anchor_conflict", {})
    if timing_anchor:
        rows.append(
            {
                "figure_key": "field_timing_anchor_conflict",
                "source_run": DEFAULT_TIMING_ANCHOR_CONFLICT_RUN,
                "policy_label": timing_anchor.get("policy_label", ""),
                "metric_label": "early_vs_short_delta_half_widths",
                "metric_value": safe_float(timing_anchor.get("early_vs_short_delta_half_widths")),
                "figure_path": timing_anchor.get("paths", {}).get("figure", ""),
                "allowed_use": "timing-anchor conflict boundary, not absolute time-zero or field FWI",
            }
        )
    timing_window = summaries.get("timing_window_family", {})
    if timing_window:
        rows.append(
            {
                "figure_key": "field_timing_window_family_classification",
                "source_run": DEFAULT_TIMING_WINDOW_FAMILY_RUN,
                "policy_label": timing_window.get("policy_label", ""),
                "metric_label": "short_nonraw_supported_count",
                "metric_value": safe_float(timing_window.get("short_nonraw_supported_count")),
                "figure_path": timing_window.get("paths", {}).get("figure", ""),
                "allowed_use": "window-family timing classification, not absolute time-zero or field FWI",
            }
        )
    timing_discriminant = summaries.get("timing_discriminant", {})
    if timing_discriminant:
        rows.append(
            {
                "figure_key": "field_timing_discriminant_scorecard",
                "source_run": DEFAULT_TIMING_DISCRIMINANT_RUN,
                "policy_label": timing_discriminant.get("policy_label", ""),
                "metric_label": "score_row_count",
                "metric_value": safe_float(timing_discriminant.get("score_row_count")),
                "figure_path": timing_discriminant.get("paths", {}).get("figure", ""),
                "allowed_use": "row-level timing discriminants, not absolute time-zero or field FWI",
            }
        )
    cue_spacing = summaries.get("cue_spacing_sensitivity", {})
    if cue_spacing:
        rows.append(
            {
                "figure_key": "field_cue_spacing_threshold_sensitivity",
                "source_run": DEFAULT_CUE_SPACING_SENSITIVITY_RUN,
                "policy_label": cue_spacing.get("policy_label", ""),
                "metric_label": "min_same_time_lateral_spacing_mm",
                "metric_value": safe_float(
                    cue_spacing.get("min_same_time_lateral_spacing_mm_across_thresholds")
                ),
                "figure_path": cue_spacing.get("paths", {}).get("figure", ""),
                "allowed_use": "measured cue-spacing context, not known-truth resolution benchmark",
            }
        )
    acquisition = summaries.get("acquisition_readiness", {})
    if acquisition:
        rows.append(
            {
                "figure_key": "field_acquisition_readiness_audit",
                "source_run": DEFAULT_ACQUISITION_READINESS_RUN,
                "policy_label": acquisition.get("policy_label", ""),
                "metric_label": "readiness_row_count",
                "metric_value": safe_float(acquisition.get("readiness_row_count")),
                "figure_path": acquisition.get("paths", {}).get("figure", ""),
                "allowed_use": "field acquisition and HPC-readiness boundary",
            }
        )
    hpc_dimensionality = summaries.get("hpc_dimensionality", {})
    if hpc_dimensionality:
        rows.append(
            {
                "figure_key": "field_hpc_dimensionality_decision_card",
                "source_run": DEFAULT_HPC_DIMENSIONALITY_RUN,
                "policy_label": hpc_dimensionality.get("policy_label", ""),
                "metric_label": "profile_count",
                "metric_value": safe_float(hpc_dimensionality.get("profile_count")),
                "figure_path": hpc_dimensionality.get("paths", {}).get("figure", ""),
                "allowed_use": "2D-only/no-HPC dimensionality decision",
            }
        )
    apparent_depth = summaries.get("apparent_depth_qc", {})
    if apparent_depth:
        rows.append(
            {
                "figure_key": "field_apparent_depth_scale_qc",
                "source_run": DEFAULT_APPARENT_DEPTH_QC_RUN,
                "policy_label": apparent_depth.get("policy_label", ""),
                "metric_label": "max_corrected_depth_residual_mm",
                "metric_value": safe_float(apparent_depth.get("max_corrected_depth_residual_mm")),
                "figure_path": apparent_depth.get("paths", {}).get("figure", ""),
                "allowed_use": "relative apparent-depth scale QC guardrail",
            }
        )
    apparent_depth_sensitivity = summaries.get("apparent_depth_sensitivity", {})
    if apparent_depth_sensitivity:
        rows.append(
            {
                "figure_key": "field_apparent_depth_sensitivity_qc",
                "source_run": DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN,
                "policy_label": apparent_depth_sensitivity.get("policy_label", ""),
                "metric_label": "max_apparent_depth_sensitivity_factor",
                "metric_value": safe_float(
                    apparent_depth_sensitivity.get("max_apparent_depth_sensitivity_factor")
                ),
                "figure_path": apparent_depth_sensitivity.get("paths", {}).get("figure", ""),
                "allowed_use": "dielectric/time-zero sensitivity guardrail, not calibrated cover depth",
            }
        )
    hyperbola_timezero = summaries.get("hyperbola_timezero_degeneracy", {})
    if hyperbola_timezero:
        rows.append(
            {
                "figure_key": "field_hyperbola_timezero_degeneracy",
                "source_run": DEFAULT_HYPERBOLA_TIMEZERO_DEGENERACY_RUN,
                "policy_label": hyperbola_timezero.get("policy_label", ""),
                "metric_label": "boundary_best_surface_count",
                "metric_value": safe_float(hyperbola_timezero.get("boundary_best_surface_count")),
                "figure_path": hyperbola_timezero.get("paths", {}).get("figure", ""),
                "allowed_use": "hyperbola/time-zero score degeneracy guardrail",
            }
        )
    return rows


def claim_boundary_rows(
    relaxed_phase_anchor_summary: dict | None = None,
    bandlimited_repeatability_summary: dict | None = None,
    event_support_tiers_summary: dict | None = None,
    time_zero_uncertainty_summary: dict | None = None,
    time_zero_perturbation_summary: dict | None = None,
    early_time_anchor_summary: dict | None = None,
    acquisition_readiness_summary: dict | None = None,
    apparent_depth_qc_summary: dict | None = None,
    apparent_depth_sensitivity_summary: dict | None = None,
    hyperbola_timezero_degeneracy_summary: dict | None = None,
    cue_spacing_sensitivity_summary: dict | None = None,
    timing_anchor_conflict_summary: dict | None = None,
    timing_window_family_summary: dict | None = None,
    timing_discriminant_summary: dict | None = None,
    hpc_dimensionality_summary: dict | None = None,
    short_waveform_coherence_summary: dict | None = None,
    short_radius_degeneracy_summary: dict | None = None,
    short_signed_morphology_summary: dict | None = None,
    short_signed_morphology_sensitivity_summary: dict | None = None,
    short_signed_morphology_timing_margin_summary: dict | None = None,
    short_signal_contrast_summary: dict | None = None,
    short_signal_contrast_sensitivity_summary: dict | None = None,
) -> list[dict]:
    rows = [
        {
            "claim_area": "field_geometry",
            "allowed_claim": "The local GSSI data are independent 2D line-profile QC evidence.",
            "not_allowed": "Do not treat the dataset as a recovered 3D survey grid without external layout metadata.",
        },
        {
            "claim_area": "short_profile_timing",
            "allowed_claim": "Use short 014/016 content-backed and supported-stack figures for relative timing/repeatability QC.",
            "not_allowed": "Do not claim absolute time-zero, cover depth, radius, or measured-data FWI from these panels.",
        },
        {
            "claim_area": "long_profile_pattern",
            "allowed_claim": "Use long 015/013 figures as pattern-only QC at the robust +0.06 ns shift.",
            "not_allowed": "Do not call the long-profile shift a phase anchor or transferable time-zero correction.",
        },
        {
            "claim_area": "synthetic_separation",
            "allowed_claim": "Keep field QC and known-truth synthetic confidence policies separate.",
            "not_allowed": "Do not use field QC to relabel synthetic optimizer success or ambiguity tiers.",
        },
        {
            "claim_area": "gpu_next_step",
            "allowed_claim": "No field GPU/FWI run is justified without external survey geometry or a new measured-data objective.",
            "not_allowed": "Do not launch field FWI/3D runs from this dataset alone.",
        },
        {
            "claim_area": "long_profile_sensitivity",
            "allowed_claim": "The +0.06 ns long-profile pattern-only support survives the tested shallow time windows and anchor widths.",
            "not_allowed": "Do not convert sensitivity robustness into absolute phase-anchor, cover-depth, radius, 3D, or FWI claims.",
        },
    ]
    relaxed_phase_anchor_summary = relaxed_phase_anchor_summary or {}
    if relaxed_phase_anchor_summary:
        rows.append(
            {
                "claim_area": "long_relaxed_phase_anchor",
                "allowed_claim": (
                    "Use the relaxed long-profile phase-anchor audit as negative evidence: "
                    "profile 013 candidates remain low-SNR and the long pair remains pattern-only QC."
                ),
                "not_allowed": (
                    "Do not promote relaxed late-window picks to absolute time-zero, cover-depth, radius, "
                    "3D, or measured-data FWI evidence."
                ),
            }
        )
    if bandlimited_repeatability_summary:
        rows.append(
            {
                "claim_area": "field_bandlimited_repeatability",
                "allowed_claim": (
                    "Use the band-limited repeatability audit to justify measured-field QC band choices "
                    "for the short pair and pattern-only band support for the long pair."
                ),
                "not_allowed": (
                    "Do not convert band-limited repeatability into absolute time-zero, cover-depth, "
                    "radius, 3D, or measured-data FWI evidence."
                ),
            }
        )
    if event_support_tiers_summary:
        rows.append(
            {
                "claim_area": "field_event_support_tiers",
                "allowed_claim": (
                    "Use the event-support tier table to separate short-pair "
                    "content-backed timing QC, long-pair pattern-only support, "
                    "band-limited repeatability, and explicit FWI/3D blockers."
                ),
                "not_allowed": (
                    "Do not convert event-support tiers into field radius, "
                    "cover-depth, 3D, or measured-data FWI claims."
                ),
            }
        )
    if time_zero_uncertainty_summary:
        rows.append(
            {
                "claim_area": "field_time_zero_uncertainty_budget",
                "allowed_claim": (
                    "Use the relative time-zero uncertainty budget for short 014/016 "
                    "QC, robustness accounting, and manuscript uncertainty bounds."
                ),
                "not_allowed": (
                    "Do not convert the relative uncertainty budget into absolute "
                    "time-zero, field FWI, 3D, radius, or cover-depth claims."
                ),
            }
        )
    if time_zero_perturbation_summary:
        rows.append(
            {
                "claim_area": "field_time_zero_perturbation_sensitivity",
                "allowed_claim": (
                    "Use the perturbation sensitivity audit to show that the "
                    "short 014/016 B-scan QC remains supported under bootstrap-CI "
                    "and conservative relative-offset perturbations."
                ),
                "not_allowed": (
                    "Do not convert perturbation robustness into absolute "
                    "time-zero, field FWI, 3D, radius, or cover-depth claims."
                ),
            }
        )
    if early_time_anchor_summary:
        rows.append(
            {
                "claim_area": "field_early_time_anchor_negative_qc",
                "allowed_claim": (
                    "Use the early-time median-trace audit as a negative "
                    "control showing that common-mode/direct-wave alignment "
                    "does not reproduce the content-backed short-pair offset."
                ),
                "not_allowed": (
                    "Do not use the early direct/ringdown component as an "
                    "absolute time-zero calibration, field FWI anchor, 3D "
                    "inversion input, or replacement for content-backed timing."
                ),
            }
        )
    if timing_anchor_conflict_summary:
        rows.append(
            {
                "claim_area": "field_timing_anchor_conflict",
                "allowed_claim": (
                    "Use the timing-anchor conflict synthesis to keep short "
                    "content-backed relative timing, early common-mode timing, "
                    "and long pattern-only timing as separate scoped QC anchors."
                ),
                "not_allowed": (
                    "Do not average or reconcile these anchors into absolute "
                    "time-zero, cover-depth/radius recovery, field FWI, 3D "
                    "inversion, or synthetic-policy relabeling."
                ),
            }
        )
    if timing_window_family_summary:
        rows.append(
            {
                "claim_area": "field_timing_window_family_classification",
                "allowed_claim": (
                    "Use the timing window-family classification to show that "
                    "strict early windows are common-mode near-zero, short "
                    "content windows support the relative correction envelope, "
                    "and long shallow windows remain pattern-only."
                ),
                "not_allowed": (
                    "Do not convert window-family separation into absolute "
                    "time-zero, cover-depth/radius recovery, field FWI, 3D "
                    "inversion, or synthetic-policy relabeling."
                ),
            }
        )
    if timing_discriminant_summary:
        rows.append(
            {
                "claim_area": "field_timing_discriminant_scorecard",
                "allowed_claim": (
                    "Use the timing-discriminant scorecard to report that early, short-content, "
                    "raw/no-correction, and long-pattern timing windows are separable scoped QC evidence."
                ),
                "not_allowed": (
                    "Do not convert the timing discriminants into absolute time-zero, cover-depth/radius "
                    "recovery, field FWI, 3D inversion, or synthetic-policy relabeling."
                ),
            }
        )
    if cue_spacing_sensitivity_summary:
        rows.append(
            {
                "claim_area": "field_cue_spacing_context",
                "allowed_claim": (
                    "Use cue-spacing threshold sensitivity as measured-field context showing visible "
                    "cues remain wider than the synthetic close-spacing stress scale."
                ),
                "not_allowed": (
                    "Do not use measured cue spacing as known-truth rebar separation, synthetic "
                    "resolution validation, calibrated cover-depth/radius evidence, field FWI, "
                    "3D inversion, or synthetic-policy relabeling."
                ),
            }
        )
    if acquisition_readiness_summary:
        rows.append(
            {
                "claim_area": "field_acquisition_readiness",
                "allowed_claim": (
                    "Use the acquisition readiness audit to justify the field "
                    "dataset as dense 2D line-profile QC with no current field "
                    "FWI or 3D HPC priority."
                ),
                "not_allowed": (
                    "Do not submit field FWI/3D HPC jobs or infer volumetric "
                    "survey geometry from this dataset without external layout "
                    "metadata or a new calibrated acquisition."
                ),
            }
        )
    if hpc_dimensionality_summary:
        rows.append(
            {
                "claim_area": "field_hpc_dimensionality",
                "allowed_claim": (
                    "Use the dimensionality decision card to report that the current archive contains "
                    "four independent dense 2D line profiles suitable for scoped field QC."
                ),
                "not_allowed": (
                    "Do not treat the current field dataset as a 3D/HPC/FWI workload without external "
                    "survey layout metadata, calibrated target geometry, and absolute timing/depth controls."
                ),
            }
        )
    short_waveform_coherence_summary = short_waveform_coherence_summary or {}
    short_signed_morphology_summary = short_signed_morphology_summary or {}
    short_signed_morphology_sensitivity_summary = short_signed_morphology_sensitivity_summary or {}
    if (
        short_waveform_coherence_summary
        or short_signed_morphology_summary
        or short_signed_morphology_sensitivity_summary
    ):
        rows.append(
            {
                "claim_area": "field_short_anchor_signed_morphology_qc",
                "allowed_claim": (
                    "Use short-anchor waveform coherence, signed morphology, and threshold "
                    "sensitivity as content-backed measured-field morphology QC."
                ),
                "not_allowed": (
                    "Do not convert morphology QC into absolute amplitude calibration, calibrated "
                    "time-zero, radius/geometry/cover-depth recovery, field FWI, 3D inversion, "
                    "or synthetic-policy relabeling."
                ),
            }
        )
    short_radius_degeneracy_summary = short_radius_degeneracy_summary or {}
    if short_radius_degeneracy_summary:
        rows.append(
            {
                "claim_area": "field_short_anchor_radius_degeneracy",
                "allowed_claim": (
                    "Use the short-anchor radius-degeneracy audit as a blocker explaining why "
                    "morphology support should not be promoted to radius seeding or recovery."
                ),
                "not_allowed": (
                    "Do not use weak or near-tied radius families as field radius seeds, "
                    "calibrated radius recovery, cover-depth recovery, field FWI, or 3D/HPC evidence."
                ),
            }
        )
    short_signed_morphology_timing_margin_summary = short_signed_morphology_timing_margin_summary or {}
    if short_signed_morphology_timing_margin_summary:
        rows.append(
            {
                "claim_area": "field_short_anchor_signed_morphology_timing_margin",
                "allowed_claim": (
                    "Use the signed morphology timing-margin audit for content-only timing-margin "
                    "support in the short-anchor QC chain."
                ),
                "not_allowed": (
                    "Do not promote the content-only timing-margin support to conservative timing, "
                    "absolute time-zero, field FWI, 3D/HPC, radius, geometry, or cover-depth claims."
                ),
            }
        )
    short_signal_contrast_summary = short_signal_contrast_summary or {}
    short_signal_contrast_sensitivity_summary = short_signal_contrast_sensitivity_summary or {}
    if short_signal_contrast_summary or short_signal_contrast_sensitivity_summary:
        rows.append(
            {
                "claim_area": "field_short_anchor_signal_contrast_qc",
                "allowed_claim": (
                    "Use the short-anchor signal-contrast audit and sensitivity sweep as a "
                    "default-window morphology-QC guardrail."
                ),
                "not_allowed": (
                    "Do not promote signal-contrast QC to absolute amplitude calibration, "
                    "strict window-invariant contrast, radius/geometry/cover-depth recovery, "
                    "field FWI, 3D/HPC, or synthetic-policy relabeling."
                ),
            }
        )
    if apparent_depth_qc_summary:
        rows.append(
            {
                "claim_area": "field_apparent_depth_scale_qc",
                "allowed_claim": (
                    "Use the apparent-depth QC figure as a relative scale "
                    "guardrail for field cue timing and short-pair residuals."
                ),
                "not_allowed": (
                    "Do not convert apparent-depth scale QC into calibrated "
                    "cover-depth recovery, radius recovery, 3D, or measured-data FWI."
                ),
            }
        )
    if apparent_depth_sensitivity_summary:
        rows.append(
            {
                "claim_area": "field_apparent_depth_sensitivity",
                "allowed_claim": (
                    "Use the apparent-depth sensitivity figure to show that "
                    "the field depth scale depends strongly on dielectric and "
                    "time-zero assumptions."
                ),
                "not_allowed": (
                    "Do not report calibrated cover depth from the field cues "
                    "while the apparent-depth span remains dielectric/time-zero sensitive."
                ),
            }
        )
    if hyperbola_timezero_degeneracy_summary:
        rows.append(
            {
                "claim_area": "field_hyperbola_timezero_degeneracy",
                "allowed_claim": (
                    "Use the hyperbola/time-zero degeneracy figure as negative "
                    "identifiability evidence for measured field inversion."
                ),
                "not_allowed": (
                    "Do not promote hyperbola/common-offset overlays to cover-depth, "
                    "radius, 3D, or measured-data FWI recovery while score surfaces "
                    "retain boundary and near-top degeneracy."
                ),
            }
        )
    return rows


def summarize_bundle(figures: list[dict], claims: list[dict], summaries: dict[str, dict]) -> dict:
    geometry_class = str(summaries["geometry"].get("classification", ""))
    long_window_ready = safe_float(
        summaries["long_window_sensitivity"].get("all_window_supported_anchor_count")
    ) == safe_float(summaries["long_window_sensitivity"].get("candidate_anchor_count"))
    long_width_ready = safe_float(
        summaries["long_width_sensitivity"].get("all_width_supported_anchor_count")
    ) == safe_float(summaries["long_width_sensitivity"].get("candidate_anchor_count"))
    relaxed = summaries.get("long_relaxed_phase_anchor", {})
    bandlimited = summaries.get("bandlimited_repeatability", {})
    event_support = summaries.get("event_support_tiers", {})
    time_zero = summaries.get("time_zero_uncertainty", {})
    time_zero_perturbation = summaries.get("time_zero_perturbation", {})
    early_time = summaries.get("early_time_anchor", {})
    acquisition = summaries.get("acquisition_readiness", {})
    apparent_depth = summaries.get("apparent_depth_qc", {})
    apparent_depth_sensitivity = summaries.get("apparent_depth_sensitivity", {})
    hyperbola_timezero = summaries.get("hyperbola_timezero_degeneracy", {})
    cue_spacing = summaries.get("cue_spacing_sensitivity", {})
    timing_anchor = summaries.get("timing_anchor_conflict", {})
    timing_window = summaries.get("timing_window_family", {})
    timing_discriminant = summaries.get("timing_discriminant", {})
    hpc_dimensionality = summaries.get("hpc_dimensionality", {})
    short_waveform_coherence = summaries.get("short_waveform_coherence", {})
    short_radius_degeneracy = summaries.get("short_radius_degeneracy", {})
    short_signed_morphology = summaries.get("short_signed_morphology", {})
    short_signed_morphology_sensitivity = summaries.get("short_signed_morphology_sensitivity", {})
    short_signed_morphology_timing_margin = summaries.get("short_signed_morphology_timing_margin", {})
    short_signal_contrast = summaries.get("short_signal_contrast", {})
    short_signal_contrast_sensitivity = summaries.get("short_signal_contrast_sensitivity", {})
    cue_spacing_context_ready = bool(
        cue_spacing.get(
            "ready_for_field_context",
            cue_spacing.get(
                "all_thresholds_wider_than_synthetic_close_context",
                cue_spacing.get("all_thresholds_wider_than_close_scale", False),
            ),
        )
    )
    ready = (
        geometry_class == "independent_2d_line_profiles"
        and len(figures) >= 7
        and len(claims) >= 6
        and long_window_ready
        and long_width_ready
    )
    policy_label = "field_publication_claim_bundle_2d_qc_sensitivity_ready_not_fwi"
    if (
        early_time
        and relaxed
        and bandlimited
        and event_support
        and time_zero
        and time_zero_perturbation
        and acquisition
        and apparent_depth
        and apparent_depth_sensitivity
        and hyperbola_timezero
    ):
        policy_label = "field_publication_claim_bundle_2d_qc_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
    elif (
        relaxed
        and bandlimited
        and event_support
        and time_zero
        and time_zero_perturbation
        and acquisition
        and apparent_depth
        and apparent_depth_sensitivity
        and hyperbola_timezero
    ):
        policy_label = "field_publication_claim_bundle_2d_qc_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
    elif relaxed and bandlimited and event_support and time_zero and time_zero_perturbation and acquisition:
        policy_label = "field_publication_claim_bundle_2d_qc_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
    elif relaxed and bandlimited and event_support and time_zero and time_zero_perturbation:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
    elif bandlimited and event_support and time_zero and time_zero_perturbation:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_perturbation_event_tiers_bandlimited_ready_not_fwi"
    elif bandlimited and time_zero and time_zero_perturbation:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_perturbation_bandlimited_ready_not_fwi"
    elif relaxed and bandlimited and event_support and time_zero:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_event_tiers_bandlimited_relaxed_ready_not_fwi"
    elif bandlimited and event_support and time_zero:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_event_tiers_bandlimited_ready_not_fwi"
    elif relaxed and bandlimited and time_zero:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_bandlimited_relaxed_anchor_ready_not_fwi"
    elif relaxed and bandlimited and event_support:
        policy_label = "field_publication_claim_bundle_2d_qc_event_tiers_bandlimited_relaxed_ready_not_fwi"
    elif relaxed and bandlimited:
        policy_label = "field_publication_claim_bundle_2d_qc_bandlimited_relaxed_anchor_ready_not_fwi"
    elif bandlimited and event_support:
        policy_label = "field_publication_claim_bundle_2d_qc_event_tiers_bandlimited_ready_not_fwi"
    elif bandlimited and time_zero:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_bandlimited_ready_not_fwi"
    elif event_support and time_zero:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_event_tiers_ready_not_fwi"
    elif event_support:
        policy_label = "field_publication_claim_bundle_2d_qc_event_tiers_ready_not_fwi"
    elif relaxed:
        policy_label = "field_publication_claim_bundle_2d_qc_relaxed_anchor_negative_ready_not_fwi"
    elif bandlimited:
        policy_label = "field_publication_claim_bundle_2d_qc_bandlimited_ready_not_fwi"
    elif time_zero:
        policy_label = "field_publication_claim_bundle_2d_qc_time_zero_budget_ready_not_fwi"
    if cue_spacing and "cue_spacing" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_cue_spacing_",
            1,
        )
    if timing_anchor and "timing_anchor" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_timing_anchor_",
            1,
        )
    if timing_window and "timing_window" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_timing_window_",
            1,
        )
    if timing_discriminant and "timing_discriminant" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_timing_discriminant_",
            1,
        )
    if hpc_dimensionality and "hpc_dimensionality" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_hpc_dimensionality_",
            1,
        )
    if (
        short_waveform_coherence
        or short_radius_degeneracy
        or short_signed_morphology
        or short_signed_morphology_sensitivity
    ) and "short_morphology" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_short_morphology_",
            1,
        )
    if short_signed_morphology_timing_margin and "short_timing_margin" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_short_timing_margin_",
            1,
        )
    if (short_signal_contrast or short_signal_contrast_sensitivity) and "short_signal_contrast" not in policy_label:
        policy_label = policy_label.replace(
            "field_publication_claim_bundle_2d_qc_",
            "field_publication_claim_bundle_2d_qc_short_signal_contrast_",
            1,
        )
    return {
        "policy_label": policy_label,
        "figure_row_count": len(figures),
        "claim_boundary_count": len(claims),
        "geometry_classification": geometry_class,
        "long_holdout_policy": summaries["long_holdout"].get("policy_label", ""),
        "long_window_sensitivity_policy": summaries["long_window_sensitivity"].get("policy_label", ""),
        "long_width_sensitivity_policy": summaries["long_width_sensitivity"].get("policy_label", ""),
        "long_window_sensitivity_ready": long_window_ready,
        "long_width_sensitivity_ready": long_width_ready,
        "long_relaxed_phase_anchor_included": bool(relaxed),
        "long_relaxed_phase_anchor_policy": relaxed_phase_anchor_policy(relaxed) if relaxed else "",
        "long_relaxed_phase_anchor_pick_count": safe_float(relaxed.get("phase_anchor_pick_count"), 0.0),
        "long_relaxed_phase_anchor_low_snr_pick_count": safe_float(
            relaxed.get("low_snr_phase_anchor_pick_count"),
            0.0,
        ),
        "bandlimited_repeatability_included": bool(bandlimited),
        "bandlimited_repeatability_policy": bandlimited.get("policy_label", ""),
        "bandlimited_short_supported_band_count": safe_float(
            bandlimited.get("short_supported_band_count"), 0.0
        ),
        "bandlimited_long_pattern_supported_band_count": safe_float(
            bandlimited.get("long_pattern_supported_band_count"), 0.0
        ),
        "event_support_tiers_included": bool(event_support),
        "event_support_tiers_policy": event_support.get("policy_label", ""),
        "event_support_tier_row_count": safe_float(event_support.get("tier_row_count"), 0.0),
        "event_support_short_content_anchor_supported_count": safe_float(
            event_support.get("short_content_anchor_supported_count"), 0.0
        ),
        "event_support_long_pattern_total_supported_anchor_count": safe_float(
            event_support.get("long_pattern_total_supported_anchor_count"), 0.0
        ),
        "time_zero_uncertainty_included": bool(time_zero),
        "time_zero_uncertainty_policy": time_zero.get("policy_label", ""),
        "time_zero_relative_anchor_offset_ns": safe_float(
            time_zero.get("relative_anchor_offset_ns"), 0.0
        ),
        "time_zero_bootstrap_ci_lower_ns": safe_float(
            time_zero.get("bootstrap_ci_lower_ns"), 0.0
        ),
        "time_zero_bootstrap_ci_upper_ns": safe_float(
            time_zero.get("bootstrap_ci_upper_ns"), 0.0
        ),
        "time_zero_conservative_half_width_ns": safe_float(
            time_zero.get("conservative_half_width_ns"), 0.0
        ),
        "time_zero_absolute_ready": bool(time_zero.get("absolute_time_zero_ready", False)),
        "time_zero_perturbation_included": bool(time_zero_perturbation),
        "time_zero_perturbation_policy": time_zero_perturbation.get("policy_label", ""),
        "time_zero_perturbation_bootstrap_supported_count": safe_float(
            time_zero_perturbation.get("bootstrap_ci_supported_count"), 0.0
        ),
        "time_zero_perturbation_bootstrap_row_count": safe_float(
            time_zero_perturbation.get("bootstrap_ci_row_count"), 0.0
        ),
        "time_zero_perturbation_conservative_supported_count": safe_float(
            time_zero_perturbation.get("conservative_supported_count"), 0.0
        ),
        "time_zero_perturbation_conservative_row_count": safe_float(
            time_zero_perturbation.get("conservative_row_count"), 0.0
        ),
        "time_zero_perturbation_min_matrix_improvement": safe_float(
            time_zero_perturbation.get("min_nonraw_matrix_improvement"), 0.0
        ),
        "time_zero_perturbation_min_corrected_abs_correlation": safe_float(
            time_zero_perturbation.get("min_nonraw_corrected_abs_correlation"), 0.0
        ),
        "time_zero_perturbation_min_improved_column_fraction": safe_float(
            time_zero_perturbation.get("min_nonraw_improved_column_fraction"), 0.0
        ),
        "early_time_anchor_included": bool(early_time),
        "early_time_anchor_policy": early_time.get("policy_label", ""),
        "early_time_short_pair_shift_ns": safe_float(
            early_time.get("short_pair_early_shift_ns"), 0.0
        ),
        "early_time_short_vs_content_delta_ns": safe_float(
            early_time.get("short_pair_early_vs_content_delta_ns"), 0.0
        ),
        "early_time_short_agrees_with_content_budget": bool(
            early_time.get("short_pair_early_agrees_with_content_budget", False)
        ),
        "early_time_absolute_ready": bool(early_time.get("absolute_time_zero_ready", False)),
        "acquisition_readiness_included": bool(acquisition),
        "acquisition_readiness_policy": acquisition.get("policy_label", ""),
        "acquisition_readiness_ready_for_3d_hpc": bool(acquisition.get("ready_for_3d_hpc", False)),
        "acquisition_readiness_ready_for_field_fwi": bool(acquisition.get("ready_for_field_fwi", False)),
        "acquisition_readiness_field_hpc_priority": acquisition.get("field_hpc_priority", ""),
        "acquisition_readiness_samples_per_wavelength": safe_float(
            acquisition.get("samples_per_wavelength"), 0.0
        ),
        "acquisition_readiness_time_zero_depth_equivalent_mm": safe_float(
            acquisition.get("time_zero_two_way_depth_equivalent_mm"), 0.0
        ),
        "apparent_depth_qc_included": bool(apparent_depth),
        "apparent_depth_qc_policy": apparent_depth.get("policy_label", ""),
        "apparent_depth_qc_cue_count": safe_float(apparent_depth.get("cue_count"), 0.0),
        "apparent_depth_qc_max_corrected_depth_residual_mm": safe_float(
            apparent_depth.get("max_corrected_depth_residual_mm"), 0.0
        ),
        "apparent_depth_qc_time_zero_depth_equivalent_mm": safe_float(
            apparent_depth.get("time_zero_depth_equivalent_mm"), 0.0
        ),
        "apparent_depth_qc_ready_for_apparent_depth_scale_qc": bool(
            apparent_depth.get("ready_for_apparent_depth_scale_qc", False)
        ),
        "apparent_depth_qc_ready_for_cover_depth_recovery": bool(
            apparent_depth.get("ready_for_cover_depth_recovery", False)
        ),
        "apparent_depth_sensitivity_included": bool(apparent_depth_sensitivity),
        "apparent_depth_sensitivity_policy": apparent_depth_sensitivity.get("policy_label", ""),
        "apparent_depth_sensitivity_scenario_count": safe_float(
            apparent_depth_sensitivity.get("scenario_count"), 0.0
        ),
        "apparent_depth_sensitivity_factor": safe_float(
            apparent_depth_sensitivity.get("max_apparent_depth_sensitivity_factor"), 0.0
        ),
        "apparent_depth_sensitivity_max_span_mm": safe_float(
            apparent_depth_sensitivity.get("max_apparent_depth_span_mm"), 0.0
        ),
        "apparent_depth_sensitivity_cover_depth_ready": bool(
            apparent_depth_sensitivity.get("cover_depth_claim_ready", False)
        ),
        "hyperbola_timezero_degeneracy_included": bool(hyperbola_timezero),
        "hyperbola_timezero_degeneracy_policy": hyperbola_timezero.get("policy_label", ""),
        "hyperbola_timezero_boundary_best_surface_count": safe_float(
            hyperbola_timezero.get("boundary_best_surface_count"), 0.0
        ),
        "hyperbola_timezero_surface_count": safe_float(
            hyperbola_timezero.get("surface_summary_row_count"), 0.0
        ),
        "hyperbola_timezero_max_near_top_epsr_span": safe_float(
            hyperbola_timezero.get("max_near_top_epsr_span"), 0.0
        ),
        "hyperbola_timezero_max_near_top_time_zero_span_ns": safe_float(
            hyperbola_timezero.get("max_near_top_time_zero_span_ns"), 0.0
        ),
        "hyperbola_timezero_cover_depth_ready": bool(
            hyperbola_timezero.get("cover_depth_claim_ready", False)
        ),
        "hyperbola_timezero_radius_ready": bool(
            hyperbola_timezero.get("radius_claim_ready", False)
        ),
        "hyperbola_timezero_field_fwi_ready": bool(
            hyperbola_timezero.get("field_fwi_ready", False)
        ),
        "cue_spacing_sensitivity_included": bool(cue_spacing),
        "cue_spacing_sensitivity_policy": cue_spacing.get("policy_label", ""),
        "cue_spacing_threshold_count": safe_float(cue_spacing.get("threshold_count"), 0.0),
        "cue_spacing_min_same_time_spacing_mm": safe_float(
            cue_spacing.get("min_same_time_lateral_spacing_mm_across_thresholds"), 0.0
        ),
        "cue_spacing_max_same_time_pair_count": safe_float(
            cue_spacing.get("max_same_time_lateral_pair_count"), 0.0
        ),
        "cue_spacing_ready_for_field_context": cue_spacing_context_ready,
        "cue_spacing_resolution_benchmark_ready": bool(
            cue_spacing.get("ready_for_resolution_benchmark", False)
        ),
        "cue_spacing_field_fwi_ready": bool(cue_spacing.get("ready_for_field_fwi", False)),
        "timing_anchor_conflict_included": bool(timing_anchor),
        "timing_anchor_conflict_policy": timing_anchor.get("policy_label", ""),
        "timing_anchor_early_vs_short_delta_half_widths": safe_float(
            timing_anchor.get("early_vs_short_delta_half_widths"), 0.0
        ),
        "timing_anchor_long_vs_short_delta_half_widths": safe_float(
            timing_anchor.get("long_vs_short_delta_half_widths"), 0.0
        ),
        "timing_anchor_absolute_time_zero_ready": bool(
            timing_anchor.get("absolute_time_zero_ready", False)
        ),
        "timing_anchor_field_fwi_ready": bool(timing_anchor.get("field_fwi_ready", False)),
        "timing_anchor_ready_for_manuscript_boundary": bool(
            timing_anchor.get("ready_for_manuscript_field_timing_boundary", False)
        ),
        "timing_window_family_included": bool(timing_window),
        "timing_window_family_policy": timing_window.get("policy_label", ""),
        "timing_window_early_strict_near_zero_lag_count": safe_float(
            timing_window.get("early_strict_near_zero_lag_row_count"), 0.0
        ),
        "timing_window_early_strict_row_count": safe_float(
            timing_window.get("early_strict_row_count"), 0.0
        ),
        "timing_window_short_nonraw_supported_count": safe_float(
            timing_window.get("short_nonraw_supported_count"), 0.0
        ),
        "timing_window_short_nonraw_row_count": safe_float(
            timing_window.get("short_nonraw_row_count"), 0.0
        ),
        "timing_window_long_reject_short_transfer_count": safe_float(
            timing_window.get("long_reject_short_transfer_row_count"), 0.0
        ),
        "timing_window_long_row_count": safe_float(timing_window.get("long_row_count"), 0.0),
        "timing_window_absolute_time_zero_ready": bool(
            timing_window.get("absolute_time_zero_ready", False)
        ),
        "timing_window_field_fwi_ready": bool(timing_window.get("field_fwi_ready", False)),
        "timing_window_ready_for_manuscript_boundary": bool(
            timing_window.get("ready_for_manuscript_field_timing_boundary", False)
        ),
        "timing_discriminant_included": bool(timing_discriminant),
        "timing_discriminant_policy": timing_discriminant.get("policy_label", ""),
        "timing_discriminant_score_row_count": safe_float(
            timing_discriminant.get("score_row_count"), 0.0
        ),
        "timing_discriminant_early_low_uniqueness_margin": bool(
            timing_discriminant.get("early_has_low_uniqueness_margin", False)
        ),
        "timing_discriminant_short_nonraw_supported_count": safe_float(
            timing_discriminant.get("short_nonraw_supported_count"), 0.0
        ),
        "timing_discriminant_long_reject_short_transfer_count": safe_float(
            timing_discriminant.get("long_reject_short_transfer_count"), 0.0
        ),
        "timing_discriminant_absolute_time_zero_ready": bool(
            timing_discriminant.get("absolute_time_zero_ready", False)
        ),
        "timing_discriminant_field_fwi_ready": bool(
            timing_discriminant.get("field_fwi_ready", False)
        ),
        "timing_discriminant_ready_for_scorecard": bool(
            timing_discriminant.get("ready_for_manuscript_timing_scorecard", False)
        ),
        "hpc_dimensionality_included": bool(hpc_dimensionality),
        "hpc_dimensionality_policy": hpc_dimensionality.get("policy_label", ""),
        "hpc_dimensionality_field_geometry_type": hpc_dimensionality.get("field_geometry_type", ""),
        "hpc_dimensionality_is_3d_survey": bool(hpc_dimensionality.get("is_3d_survey", False)),
        "hpc_dimensionality_ready_for_2d_qc": bool(hpc_dimensionality.get("ready_for_2d_qc", False)),
        "hpc_dimensionality_ready_for_3d_hpc": bool(
            hpc_dimensionality.get("ready_for_3d_hpc", False)
        ),
        "hpc_dimensionality_ready_for_field_fwi": bool(
            hpc_dimensionality.get("ready_for_field_fwi", False)
        ),
        "hpc_dimensionality_field_hpc_priority": hpc_dimensionality.get("field_hpc_priority", ""),
        "short_waveform_coherence_included": bool(short_waveform_coherence),
        "short_waveform_coherence_policy": short_waveform_coherence.get("policy_label", ""),
        "short_waveform_coherence_min_corrected_abs_correlation": safe_float(
            short_waveform_coherence.get("min_corrected_field_trace_abs_correlation"), 0.0
        ),
        "short_waveform_coherence_ready_for_morphology_qc": bool(
            short_waveform_coherence.get("ready_for_waveform_morphology_qc", False)
        ),
        "short_waveform_coherence_field_fwi_ready": bool(
            short_waveform_coherence.get("ready_for_field_fwi", False)
        ),
        "short_radius_degeneracy_included": bool(short_radius_degeneracy),
        "short_radius_degeneracy_policy": short_radius_degeneracy.get("policy_label", ""),
        "short_radius_degeneracy_weak_side_count": safe_float(
            short_radius_degeneracy.get("weak_radius_side_count"), 0.0
        ),
        "short_radius_degeneracy_ready_for_radius_seed": bool(
            short_radius_degeneracy.get("ready_for_radius_seed", False)
        ),
        "short_radius_degeneracy_ready_for_radius_recovery": bool(
            short_radius_degeneracy.get("ready_for_radius_recovery", False)
        ),
        "short_radius_degeneracy_field_fwi_ready": bool(
            short_radius_degeneracy.get("ready_for_field_fwi", False)
        ),
        "short_signed_morphology_included": bool(short_signed_morphology),
        "short_signed_morphology_policy": short_signed_morphology.get("policy_label", ""),
        "short_signed_morphology_supported_pair_count": safe_float(
            short_signed_morphology.get("signed_morphology_supported_pair_count"), 0.0
        ),
        "short_signed_morphology_min_corrected_signed_correlation": safe_float(
            short_signed_morphology.get("min_corrected_signed_correlation"), 0.0
        ),
        "short_signed_morphology_ready_for_qc": bool(
            short_signed_morphology.get("ready_for_signed_waveform_morphology_qc", False)
        ),
        "short_signed_morphology_field_fwi_ready": bool(
            short_signed_morphology.get("ready_for_field_fwi", False)
        ),
        "short_signed_morphology_sensitivity_included": bool(short_signed_morphology_sensitivity),
        "short_signed_morphology_sensitivity_policy": short_signed_morphology_sensitivity.get(
            "policy_label",
            "",
        ),
        "short_signed_morphology_sensitivity_supported_threshold_combo_count": safe_float(
            short_signed_morphology_sensitivity.get("all_pairs_supported_threshold_combo_count"), 0.0
        ),
        "short_signed_morphology_sensitivity_ready_for_moderate_qc": bool(
            short_signed_morphology_sensitivity.get("ready_for_moderate_threshold_morphology_qc", False)
        ),
        "short_signed_morphology_sensitivity_field_fwi_ready": bool(
            short_signed_morphology_sensitivity.get("ready_for_field_fwi", False)
        ),
        "short_signed_morphology_timing_margin_included": bool(short_signed_morphology_timing_margin),
        "short_signed_morphology_timing_margin_policy": short_signed_morphology_timing_margin.get(
            "policy_label",
            "",
        ),
        "short_signed_morphology_timing_margin_max_residual_ns": safe_float(
            short_signed_morphology_timing_margin.get("max_corrected_abs_timing_residual_ns"), 0.0
        ),
        "short_signed_morphology_timing_margin_min_default_slack_ns": safe_float(
            short_signed_morphology_timing_margin.get("min_default_timing_slack_ns"), 0.0
        ),
        "short_signed_morphology_timing_margin_content_half_range_ns": safe_float(
            short_signed_morphology_timing_margin.get("content_only_offset_half_range_ns"), 0.0
        ),
        "short_signed_morphology_timing_margin_conservative_half_width_ns": safe_float(
            short_signed_morphology_timing_margin.get("short_conservative_half_width_ns"), 0.0
        ),
        "short_signed_morphology_timing_margin_default_content_covered_pair_count": safe_float(
            short_signed_morphology_timing_margin.get("default_slack_content_covered_pair_count"), 0.0
        ),
        "short_signed_morphology_timing_margin_ready_for_content_qc": bool(
            short_signed_morphology_timing_margin.get(
                "ready_for_content_only_morphology_timing_qc",
                False,
            )
        ),
        "short_signed_morphology_timing_margin_ready_for_conservative_claim": bool(
            short_signed_morphology_timing_margin.get(
                "ready_for_conservative_timing_morphology_claim",
                False,
            )
        ),
        "short_signed_morphology_timing_margin_absolute_time_zero_ready": bool(
            short_signed_morphology_timing_margin.get("ready_for_absolute_time_zero", False)
        ),
        "short_signed_morphology_timing_margin_field_fwi_ready": bool(
            short_signed_morphology_timing_margin.get("ready_for_field_fwi", False)
        ),
        "short_signed_morphology_timing_margin_3d_hpc_ready": bool(
            short_signed_morphology_timing_margin.get("ready_for_3d_hpc", False)
        ),
        "short_signal_contrast_included": bool(short_signal_contrast),
        "short_signal_contrast_policy": short_signal_contrast.get("policy_label", ""),
        "short_signal_contrast_supported_window_count": safe_float(
            short_signal_contrast.get("signal_contrast_supported_count"), 0.0
        ),
        "short_signal_contrast_side_window_count": safe_float(
            short_signal_contrast.get("side_window_count"), 0.0
        ),
        "short_signal_contrast_min_event_to_noise_rms": safe_float(
            short_signal_contrast.get("min_event_to_noise_rms"), 0.0
        ),
        "short_signal_contrast_min_peak_to_noise_p95": safe_float(
            short_signal_contrast.get("min_peak_to_noise_p95"), 0.0
        ),
        "short_signal_contrast_ready_for_qc": bool(
            short_signal_contrast.get("ready_for_signal_contrast_qc", False)
        ),
        "short_signal_contrast_amplitude_calibration_ready": bool(
            short_signal_contrast.get("ready_for_absolute_amplitude_calibration", False)
        ),
        "short_signal_contrast_field_fwi_ready": bool(
            short_signal_contrast.get("ready_for_field_fwi", False)
        ),
        "short_signal_contrast_sensitivity_included": bool(short_signal_contrast_sensitivity),
        "short_signal_contrast_sensitivity_policy": short_signal_contrast_sensitivity.get(
            "policy_label",
            "",
        ),
        "short_signal_contrast_sensitivity_combo_count": safe_float(
            short_signal_contrast_sensitivity.get("sensitivity_combo_count"), 0.0
        ),
        "short_signal_contrast_sensitivity_all_supported_combo_count": safe_float(
            short_signal_contrast_sensitivity.get("all_supported_combo_count"), 0.0
        ),
        "short_signal_contrast_sensitivity_default_supported": bool(
            short_signal_contrast_sensitivity.get("default_combo_all_supported", False)
        ),
        "short_signal_contrast_sensitivity_window_invariant_ready": bool(
            short_signal_contrast_sensitivity.get("ready_for_window_invariant_signal_contrast_claim", False)
        ),
        "short_signal_contrast_sensitivity_field_fwi_ready": bool(
            short_signal_contrast_sensitivity.get("ready_for_field_fwi", False)
        ),
        "gpu_priority": "none",
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_manuscript_field_supplement": ready,
        "decision": (
            "Use this bundle for measured field-data QC figures only. It does "
            "not create 3D, field inversion, radius, cover-depth, or measured "
            "FWI claims."
        ),
    }


def plot_bundle(figures: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["figure_key"].replace("_", " ") for row in figures]
    values = np.asarray([safe_float(row.get("metric_value"), 0.0) for row in figures], dtype=np.float64)
    values = np.nan_to_num(values, nan=0.0)
    x = np.arange(len(figures))
    palette = ["#6b6b6b", "#4c78a8", "#2f9d55", "#f58518", "#7f3c8d", "#54a24b", "#b279a2", "#d95f02"]
    large_bundle = len(figures) > 18
    if large_bundle:
        fig_height = max(7.2, 0.34 * len(figures) + 1.6)
        fig, ax = plt.subplots(figsize=(14.5, fig_height), constrained_layout=True)
        ax.barh(
            x,
            values,
            color=[palette[idx % len(palette)] for idx in range(len(figures))],
        )
        ax.set_yticks(x, labels, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlabel("primary support metric")
        ax.set_title("Field publication QC figure bundle")
        ax.grid(axis="x", color="#dddddd", linewidth=0.6)
    else:
        fig, ax = plt.subplots(figsize=(18.0, 5.2), constrained_layout=True)
        ax.bar(
            x,
            values,
            color=[palette[idx % len(palette)] for idx in range(len(figures))],
        )
        ax.set_xticks(x, [label.replace(" ", "\n") for label in labels])
        ax.set_ylabel("primary support metric")
        ax.set_title("Field publication QC figure bundle")
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax.text(
        0.99 if large_bundle else 0.01,
        0.02 if large_bundle else 0.96,
        f"geometry={summary['geometry_classification']} | window_sens={summary['long_window_sensitivity_ready']} | width_sens={summary['long_width_sensitivity_ready']} | gpu={summary['gpu_priority']}",
        transform=ax.transAxes,
        ha="right" if large_bundle else "left",
        va="bottom" if large_bundle else "top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.3"},
    )
    fig.suptitle("GSSI 51600S field claim bundle", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(
    path: Path,
    summary: dict,
    figure_rows_csv: Path,
    claims_csv: Path,
    validation_csv: Path,
) -> None:
    """Write notes for the field publication claim bundle figure."""
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_publication_claim_bundle.png`",
                "",
                "This figure summarizes measured GSSI 51600S field-data QC figures and",
                "claim boundaries for the current 2D line-profile evidence package.",
                "It aggregates support metrics from already-generated field runs.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Figure rows: `{summary['figure_row_count']}`.",
                f"Claim boundaries: `{summary['claim_boundary_count']}`.",
                f"Geometry classification: `{summary['geometry_classification']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "The figure does not establish a 3D survey, absolute time-zero, cover",
                "depth, radius, or measured-field FWI claim. Source figure rows and",
                f"claim boundaries are stored in `{figure_rows_csv.name}` and",
                f"`{claims_csv.name}`. Image-validation metrics for this bundle figure",
                f"are stored in `{validation_csv.name}`.",
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
    parser.add_argument("--geometry-run", default=DEFAULT_GEOMETRY_RUN)
    parser.add_argument("--short-waveform-run", default=DEFAULT_SHORT_WAVEFORM_RUN)
    parser.add_argument("--short-stack-run", default=DEFAULT_SHORT_STACK_RUN)
    parser.add_argument("--long-visual-run", default=DEFAULT_LONG_VISUAL_RUN)
    parser.add_argument("--long-holdout-run", default=DEFAULT_LONG_HOLDOUT_RUN)
    parser.add_argument("--long-window-sensitivity-run", default=DEFAULT_LONG_WINDOW_SENSITIVITY_RUN)
    parser.add_argument("--long-width-sensitivity-run", default=DEFAULT_LONG_WIDTH_SENSITIVITY_RUN)
    parser.add_argument("--long-relaxed-phase-anchor-run", default=DEFAULT_LONG_RELAXED_PHASE_ANCHOR_RUN)
    parser.add_argument("--bandlimited-run", default=DEFAULT_BANDLIMITED_RUN)
    parser.add_argument("--event-support-run", default=DEFAULT_EVENT_SUPPORT_RUN)
    parser.add_argument("--time-zero-budget-run", default=DEFAULT_TIME_ZERO_BUDGET_RUN)
    parser.add_argument("--time-zero-perturbation-run", default=DEFAULT_TIME_ZERO_PERTURBATION_RUN)
    parser.add_argument("--acquisition-readiness-run", default=DEFAULT_ACQUISITION_READINESS_RUN)
    parser.add_argument("--apparent-depth-qc-run", default=DEFAULT_APPARENT_DEPTH_QC_RUN)
    parser.add_argument("--apparent-depth-sensitivity-run", default=DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN)
    parser.add_argument("--hyperbola-timezero-degeneracy-run", default=DEFAULT_HYPERBOLA_TIMEZERO_DEGENERACY_RUN)
    parser.add_argument("--early-time-anchor-run", default=DEFAULT_EARLY_TIME_ANCHOR_RUN)
    parser.add_argument("--cue-spacing-sensitivity-run", default=DEFAULT_CUE_SPACING_SENSITIVITY_RUN)
    parser.add_argument("--timing-anchor-conflict-run", default=DEFAULT_TIMING_ANCHOR_CONFLICT_RUN)
    parser.add_argument("--timing-window-family-run", default=DEFAULT_TIMING_WINDOW_FAMILY_RUN)
    parser.add_argument("--timing-discriminant-run", default=DEFAULT_TIMING_DISCRIMINANT_RUN)
    parser.add_argument("--hpc-dimensionality-run", default=DEFAULT_HPC_DIMENSIONALITY_RUN)
    parser.add_argument("--short-waveform-coherence-run", default=DEFAULT_SHORT_WAVEFORM_COHERENCE_RUN)
    parser.add_argument("--short-radius-degeneracy-run", default=DEFAULT_SHORT_RADIUS_DEGENERACY_RUN)
    parser.add_argument("--short-signed-morphology-run", default=DEFAULT_SHORT_SIGNED_MORPHOLOGY_RUN)
    parser.add_argument(
        "--short-signed-morphology-sensitivity-run",
        default=DEFAULT_SHORT_SIGNED_MORPHOLOGY_SENSITIVITY_RUN,
    )
    parser.add_argument(
        "--short-signed-morphology-timing-margin-run",
        default=DEFAULT_SHORT_SIGNED_MORPHOLOGY_TIMING_MARGIN_RUN,
    )
    parser.add_argument("--short-signal-contrast-run", default=DEFAULT_SHORT_SIGNAL_CONTRAST_RUN)
    parser.add_argument(
        "--short-signal-contrast-sensitivity-run",
        default=DEFAULT_SHORT_SIGNAL_CONTRAST_SENSITIVITY_RUN,
    )
    parser.add_argument("--run-name", default="gssi51600s_field_publication_claim_bundle")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    runs = {
        "geometry": args.geometry_run,
        "short_waveform": args.short_waveform_run,
        "short_stack": args.short_stack_run,
        "long_visual": args.long_visual_run,
        "long_holdout": args.long_holdout_run,
        "long_window_sensitivity": args.long_window_sensitivity_run,
        "long_width_sensitivity": args.long_width_sensitivity_run,
        "long_relaxed_phase_anchor": args.long_relaxed_phase_anchor_run,
        "bandlimited_repeatability": args.bandlimited_run,
        "event_support_tiers": args.event_support_run,
        "time_zero_uncertainty": args.time_zero_budget_run,
        "time_zero_perturbation": args.time_zero_perturbation_run,
        "acquisition_readiness": args.acquisition_readiness_run,
        "apparent_depth_qc": args.apparent_depth_qc_run,
        "apparent_depth_sensitivity": args.apparent_depth_sensitivity_run,
        "hyperbola_timezero_degeneracy": args.hyperbola_timezero_degeneracy_run,
        "early_time_anchor": args.early_time_anchor_run,
        "cue_spacing_sensitivity": args.cue_spacing_sensitivity_run,
        "timing_anchor_conflict": args.timing_anchor_conflict_run,
        "timing_window_family": args.timing_window_family_run,
        "timing_discriminant": args.timing_discriminant_run,
        "hpc_dimensionality": args.hpc_dimensionality_run,
        "short_waveform_coherence": args.short_waveform_coherence_run,
        "short_radius_degeneracy": args.short_radius_degeneracy_run,
        "short_signed_morphology": args.short_signed_morphology_run,
        "short_signed_morphology_sensitivity": args.short_signed_morphology_sensitivity_run,
        "short_signed_morphology_timing_margin": args.short_signed_morphology_timing_margin_run,
        "short_signal_contrast": args.short_signal_contrast_run,
        "short_signal_contrast_sensitivity": args.short_signal_contrast_sensitivity_run,
    }
    summaries = load_field_summaries(dataset_root, runs)
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        summaries.get("long_relaxed_phase_anchor"),
        summaries.get("bandlimited_repeatability"),
        summaries.get("event_support_tiers"),
        summaries.get("time_zero_uncertainty"),
        summaries.get("time_zero_perturbation"),
        summaries.get("early_time_anchor"),
        summaries.get("acquisition_readiness"),
        summaries.get("apparent_depth_qc"),
        summaries.get("apparent_depth_sensitivity"),
        summaries.get("hyperbola_timezero_degeneracy"),
        cue_spacing_sensitivity_summary=summaries.get("cue_spacing_sensitivity"),
        timing_anchor_conflict_summary=summaries.get("timing_anchor_conflict"),
        timing_window_family_summary=summaries.get("timing_window_family"),
        timing_discriminant_summary=summaries.get("timing_discriminant"),
        hpc_dimensionality_summary=summaries.get("hpc_dimensionality"),
        short_waveform_coherence_summary=summaries.get("short_waveform_coherence"),
        short_radius_degeneracy_summary=summaries.get("short_radius_degeneracy"),
        short_signed_morphology_summary=summaries.get("short_signed_morphology"),
        short_signed_morphology_sensitivity_summary=summaries.get("short_signed_morphology_sensitivity"),
        short_signed_morphology_timing_margin_summary=summaries.get("short_signed_morphology_timing_margin"),
        short_signal_contrast_summary=summaries.get("short_signal_contrast"),
        short_signal_contrast_sensitivity_summary=summaries.get("short_signal_contrast_sensitivity"),
    )
    summary = summarize_bundle(figures, claims, summaries)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    figure_rows_csv = data_dir / "field_publication_figure_rows.csv"
    claims_csv = data_dir / "field_publication_claim_boundaries.csv"
    summary_json = data_dir / "field_publication_claim_bundle_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_bundle(figures, summary, figures_dir / "field_publication_claim_bundle.png"))
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(figure_rows_csv, [json_safe(row) for row in figures])
    write_csv(claims_csv, [json_safe(row) for row in claims])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, figure_rows_csv, claims_csv, validation_csv)
    output_summary = {
        "runs": runs,
        **summary,
        "paths": {
            "figure_rows_csv": str(figure_rows_csv),
            "claim_boundaries_csv": str(claims_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_publication_claim_bundle",
        {
            "summary_json": str(summary_json),
            "figure_rows_csv": str(figure_rows_csv),
            "claim_boundaries_csv": str(claims_csv),
            "figure_validation_csv": str(validation_csv),
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
