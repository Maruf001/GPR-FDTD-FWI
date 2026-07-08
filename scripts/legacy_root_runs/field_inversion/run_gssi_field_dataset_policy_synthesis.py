#!/usr/bin/env python3
"""Synthesize the current local GSSI field-data policy from field trackers."""

from __future__ import annotations

import argparse
import json
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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_optional_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return read_json(path)


def read_publication_claim_bundle(dataset_root: Path) -> dict:
    for run_name in (
        "111_gssi51600s_field_publication_claim_bundle_post_event_support_timing_discriminant_hpc",
        "107_gssi51600s_field_publication_claim_bundle_post_timing_discriminant_hpc",
        "102_gssi51600s_field_publication_claim_bundle_post_timing_window_family",
        "098_gssi51600s_field_publication_claim_bundle_post_timing_anchor_conflict",
        "095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context",
        "091_gssi51600s_field_publication_claim_bundle_post_early_time_anchor_qc",
        "088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc",
        "082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness",
        "079_gssi51600s_field_publication_claim_bundle_post_time_zero_perturbation",
        "076_gssi51600s_field_publication_claim_bundle_post_time_zero_budget",
        "073_gssi51600s_field_publication_claim_bundle_post_event_support_tiers",
        "070_gssi51600s_field_publication_claim_bundle_post_bandlimited_audit",
        "066_gssi51600s_field_publication_claim_bundle_post_relaxed_anchor",
        "062_gssi51600s_field_publication_claim_bundle",
    ):
        summary = read_optional_json(
            Path(dataset_root)
            / run_name
            / "data"
            / "field_publication_claim_bundle_summary.json"
        )
        if summary:
            return summary
    return {}


def field_policy_decision(
    survey: dict,
    network: dict,
    short: dict,
    long: dict,
    time_zero: dict | None = None,
    applied_time_zero: dict | None = None,
    phase_convention: dict | None = None,
    timing_bootstrap: dict | None = None,
    content_windows: dict | None = None,
    content_synthetic: dict | None = None,
    content_time_zero_anchor: dict | None = None,
    content_trace_alignment: dict | None = None,
    content_trace_sensitivity: dict | None = None,
    content_panels: dict | None = None,
    corrected_profile_stack: dict | None = None,
    corrected_profile_stack_sensitivity: dict | None = None,
    corrected_stack_spatial_support: dict | None = None,
    supported_interval_visual_qc: dict | None = None,
    long_profile_transfer_audit: dict | None = None,
    long_profile_shift_scan: dict | None = None,
    long_profile_shift_sensitivity: dict | None = None,
    long_profile_pattern_visual_qc: dict | None = None,
    long_profile_pattern_holdout_qc: dict | None = None,
    long_profile_holdout_sensitivity: dict | None = None,
    long_profile_holdout_width_sensitivity: dict | None = None,
    publication_claim_bundle: dict | None = None,
    long_profile_relaxed_phase_anchor: dict | None = None,
    bandlimited_repeatability: dict | None = None,
    apparent_depth_qc: dict | None = None,
    apparent_depth_sensitivity: dict | None = None,
    hyperbola_timezero_degeneracy: dict | None = None,
) -> dict:
    short_summary = short["summary"]
    long_summary = long["summary"]
    time_zero_summary = (time_zero or {}).get("summary", {})
    applied_summary = (applied_time_zero or {}).get("summary", {})
    phase_summary = (phase_convention or {}).get("summary", {})
    bootstrap_summary = (timing_bootstrap or {}).get("summary", {})
    content_summary = (content_windows or {}).get("summary", {})
    synthetic_summary = (content_synthetic or {}).get("summary", {})
    anchor_summary = content_time_zero_anchor or {}
    trace_summary = content_trace_alignment or {}
    sensitivity_summary = content_trace_sensitivity or {}
    panel_summary = content_panels or {}
    corrected_stack_summary = (corrected_profile_stack or {}).get("summary", {})
    corrected_stack_sensitivity_summary = corrected_profile_stack_sensitivity or {}
    spatial_support_summary = corrected_stack_spatial_support or {}
    interval_visual_summary = supported_interval_visual_qc or {}
    long_transfer_summary = (long_profile_transfer_audit or {}).get("summary", {})
    long_shift_summary = (long_profile_shift_scan or {}).get("summary", {})
    long_shift_sensitivity_summary = long_profile_shift_sensitivity or {}
    long_visual_summary = long_profile_pattern_visual_qc or {}
    long_holdout_summary = long_profile_pattern_holdout_qc or {}
    long_window_sensitivity_summary = long_profile_holdout_sensitivity or {}
    long_width_sensitivity_summary = long_profile_holdout_width_sensitivity or {}
    publication_summary = publication_claim_bundle or {}
    long_relaxed_summary = long_profile_relaxed_phase_anchor or {}
    bandlimited_summary = bandlimited_repeatability or {}
    apparent_depth_summary = apparent_depth_qc or {}
    depth_sensitivity_summary = apparent_depth_sensitivity or {}
    hyperbola_degeneracy_summary = hyperbola_timezero_degeneracy or {}
    long_relaxed_best = long_relaxed_summary.get("best_phase_hypothesis", {})
    long_relaxed_pick_count = safe_float(long_relaxed_summary.get("phase_anchor_pick_count"))
    long_relaxed_low_snr_count = safe_float(long_relaxed_summary.get("low_snr_phase_anchor_pick_count"))
    long_relaxed_boundary_count = safe_float(long_relaxed_best.get("boundary_solution_count"))
    if long_relaxed_pick_count > 0 and long_relaxed_low_snr_count >= long_relaxed_pick_count:
        long_relaxed_policy_label = "long_profile_relaxed_phase_anchor_low_snr_not_time_zero"
    elif long_relaxed_boundary_count > 0:
        long_relaxed_policy_label = "long_profile_relaxed_phase_anchor_boundary_limited"
    elif long_relaxed_pick_count > 0:
        long_relaxed_policy_label = "long_profile_relaxed_phase_anchor_review_needed"
    else:
        long_relaxed_policy_label = "not_run"
    repeat_candidates = network.get("pair_label_counts", {}).get("repeat_candidate", 0)
    embedded_candidates = network.get("pair_label_counts", {}).get("embedded_segment_candidate", 0)
    is_3d_ready = (
        survey.get("classification") != "independent_2d_line_profiles"
        and embedded_candidates > 0
        and not long_summary.get("comparison_profile_missing_phase_anchor_picks", True)
    )
    if is_3d_ready:
        label = "field_geometry_candidate_needs_review"
    else:
        label = "field_2d_qc_not_3d_or_fwi"
    decision = (
        "The local GSSI 51600S dataset should be used as 2D line-profile QC "
        "and timing/repeatability evidence only. The short pair 014/016 is the "
        "strongest repeat/timing anchor; the applied relative transfer improves "
        "short-pair phase consistency, and the multi-phase convention check "
        "shows the delay is not tied to one pick definition. Bootstrap "
        "resampling bounds the relative delay away from zero. Repeat-content "
        "window classification identifies the content-backed short-pair events "
        "and separates one timing-only cue. Content-backed field-to-synthetic "
        "waveform QC supports those two content-backed events as later visual "
        "comparison candidates, while the timing-only event remains limited. "
        "The content time-zero anchor policy quantifies the two content-backed "
        "events as measured-data time-zero and visual-QC anchors only. "
        "The content-anchor trace-alignment packet directly shows the relative "
        "time-zero correction improving measured 014/016 trace agreement at "
        "those anchors. "
        "A window-sensitivity check shows that this trace-alignment improvement "
        "survives the tested short, nominal, and wider windows. "
        "The corrected short-profile stack extends the same timing correction "
        "to the spatially aligned B-scan window and improves the measured "
        "profile-level agreement, while still remaining a timing/repeatability "
        "QC result. "
        "A corrected-stack window-sensitivity check shows that the B-scan-level "
        "improvement survives the tested shallow windows. "
        "The corrected-stack spatial support mask is more conservative: usable "
        "visual-QC regions are limited to supported intervals, so unsupported "
        "columns should not be used for interpretation. "
        "The supported-interval visual-QC package is therefore the preferred "
        "corrected-stack figure endpoint because it only shows all-window "
        "supported regions. "
        "The content-backed waveform panels are the preferred measured-data "
        "visual-QC figure endpoint. These remain QC results, not an absolute "
        "time-zero calibration. The long pair 015/013 is pattern-only because "
        "013 lacks phase-anchor picks. The long-profile transfer audit shows "
        "that applying the short-pair correction to 015/013 is not supported, "
        "so the short-pair time-zero policy should not be generalized to the "
        "long pair. A separate long-profile shift scan finds a stronger "
        "pattern-only offset for 015/013, but this remains non-calibrated "
        "pattern alignment because profile 013 still lacks phase-anchor picks. "
        "A relaxed late-window phase-anchor audit admits profile 013 candidates, "
        "but all relaxed picks are low-SNR and the best relaxed hypothesis still "
        "has a boundary solution, so it does not upgrade the long pair to "
        "absolute time-zero or measured-data FWI evidence. "
        "Window sensitivity shows that this long-pair pattern offset is stable "
        "across the tested shallow windows while the short-pair offset remains "
        "negative in all of them. Long-profile pattern-only visual QC, holdout "
        "stress testing, and the all-anchor time-window and spatial-width "
        "sensitivity checks now support the +0.06 ns pattern interpretation "
        "for all candidate anchors. A band-limited repeatability audit shows "
        "that the short-pair relative time-zero correction is supported in "
        "low, mid-low, mid-high, and broad bands, while the long pair remains "
        "pattern-only band support rather than time-zero calibration. "
        "The refreshed field publication bundle packages those figures, "
        "the event-support tier table, the relative time-zero uncertainty "
        "budget, the time-zero perturbation sensitivity audit, and the "
        "acquisition/HPC-readiness audit with explicit no-FWI/no-3D claim "
        "boundaries. "
        "The apparent-depth scale QC, apparent-depth sensitivity sweep, and "
        "hyperbola/time-zero degeneracy audit add the current measured-data "
        "depth-scale guardrails: the short-pair corrected residuals support "
        "relative apparent-depth QC, but dielectric/time-zero sensitivity and "
        "score-surface degeneracy block calibrated cover-depth, radius, field "
        "FWI, or 3D inversion claims. The early-time common-mode anchor audit "
        "adds a negative-control boundary: the direct/ringdown component aligns "
        "near zero lag and does not reproduce the content-backed short-pair "
        "relative offset, so it should not be used as absolute time-zero. "
        "The cue-spacing threshold sensitivity audit adds measured-field "
        "spacing context only: visible same-time cue spacings stay wider than "
        "the synthetic close-spacing stress scale, but this is not known-truth "
        "resolution validation or field FWI evidence. "
        "The timing-anchor conflict synthesis keeps the short relative "
        "content-backed timing, early common-mode negative control, and long "
        "pattern-only shift separate; it is a manuscript boundary for timing "
        "claim scope, not an absolute time-zero calibration or field FWI input. "
        "The timing-window family classification strengthens that boundary: "
        "strict early windows remain near zero, all non-raw short content "
        "windows support the relative correction, and long windows reject "
        "transferring the short-pair timing correction. "
        "The survey audit still lacks "
        "recoverable crossline/grid metadata, so the dataset is not a 3D "
        "survey or measured-data FWI benchmark."
    )
    return {
        "policy_label": label,
        "decision": decision,
        "repeat_candidate_pair_count": repeat_candidates,
        "embedded_segment_candidate_count": embedded_candidates,
        "short_pair_correlation": short_summary["best_normalized_correlation"],
        "short_pair_event_pair_count": short_summary["event_pair_count"],
        "short_pair_radius_match_fraction": short_summary["radius_match_fraction"],
        "long_pair_correlation": long_summary["best_normalized_correlation"],
        "long_pair_missing_phase_anchor_picks": long_summary["comparison_profile_missing_phase_anchor_picks"],
        "survey_classification": survey.get("classification"),
        "short_pair_time_zero_policy_label": time_zero_summary.get("policy_label", "not_run"),
        "short_pair_relative_time_zero_offset_ns": safe_float(
            time_zero_summary.get("median_comparison_minus_reference_phase_time_ns")
        ),
        "short_pair_applied_time_zero_policy_label": applied_summary.get("policy_label", "not_run"),
        "short_pair_applied_residual_reduction_factor": safe_float(
            applied_summary.get("mean_abs_residual_reduction_factor")
        ),
        "short_pair_applied_corrected_max_abs_residual_ns": safe_float(
            applied_summary.get("corrected_max_abs_phase_residual_ns")
        ),
        "short_pair_applied_leave_one_out_max_abs_residual_ns": safe_float(
            applied_summary.get("leave_one_out_max_abs_residual_ns")
        ),
        "short_pair_phase_convention_policy_label": phase_summary.get("policy_label", "not_run"),
        "short_pair_stable_phase_convention_count": safe_float(
            phase_summary.get("stable_phase_convention_count")
        ),
        "short_pair_stable_phase_conventions": phase_summary.get("stable_phase_conventions", ""),
        "short_pair_stable_phase_median_spread_ns": safe_float(
            phase_summary.get("stable_median_delta_spread_ns")
        ),
        "short_pair_timing_bootstrap_policy_label": bootstrap_summary.get("policy_label", "not_run"),
        "short_pair_bootstrap_observed_median_offset_ns": safe_float(
            bootstrap_summary.get("observed_median_offset_ns")
        ),
        "short_pair_bootstrap_min_ci_lower_ns": safe_float(
            bootstrap_summary.get("min_bootstrap_ci_lower_ns")
        ),
        "short_pair_bootstrap_max_ci_upper_ns": safe_float(
            bootstrap_summary.get("max_bootstrap_ci_upper_ns")
        ),
        "short_pair_bootstrap_max_ci_width_ns": safe_float(
            bootstrap_summary.get("max_bootstrap_ci_width_ns")
        ),
        "short_pair_content_window_policy_label": content_summary.get("policy_label", "not_run"),
        "short_pair_stable_content_window_count": safe_float(
            content_summary.get("stable_content_window_count")
        ),
        "short_pair_content_backed_event_pair_count": safe_float(
            content_summary.get("content_backed_event_pair_count")
        ),
        "short_pair_timing_only_event_pair_count": safe_float(
            content_summary.get("timing_only_event_pair_count")
        ),
        "short_pair_content_backed_event_fraction": safe_float(
            content_summary.get("content_backed_event_fraction")
        ),
        "short_pair_max_content_anchor_distance_mm": safe_float(
            content_summary.get("max_content_anchor_distance_mm")
        ),
        "short_pair_max_abs_content_timing_residual_ns": safe_float(
            content_summary.get("max_abs_content_timing_residual_to_bootstrap_median_ns")
        ),
        "short_pair_content_synthetic_policy_label": synthetic_summary.get("policy_label", "not_run"),
        "short_pair_content_backed_waveform_supported_count": safe_float(
            synthetic_summary.get("content_backed_waveform_supported_count")
        ),
        "short_pair_timing_only_waveform_supported_count": safe_float(
            synthetic_summary.get("timing_only_waveform_supported_count")
        ),
        "short_pair_min_content_pair_absolute_correlation": safe_float(
            synthetic_summary.get("min_content_pair_absolute_correlation")
        ),
        "short_pair_min_timing_only_pair_absolute_correlation": safe_float(
            synthetic_summary.get("min_timing_only_pair_absolute_correlation")
        ),
        "short_pair_min_abs_correlation_threshold": safe_float(
            synthetic_summary.get("min_abs_correlation_threshold")
        ),
        "short_pair_content_time_zero_anchor_policy_label": anchor_summary.get("policy_label", "not_run"),
        "short_pair_supported_content_anchor_pair_count": safe_float(
            anchor_summary.get("supported_content_anchor_pair_count")
        ),
        "short_pair_anchor_max_abs_content_residual_ns": safe_float(
            anchor_summary.get("max_abs_content_timing_residual_ns")
        ),
        "short_pair_anchor_max_abs_all_residual_ns": safe_float(
            anchor_summary.get("max_abs_all_timing_residual_ns")
        ),
        "short_pair_anchor_min_content_abs_correlation": safe_float(
            anchor_summary.get("min_content_pair_absolute_correlation")
        ),
        "short_pair_anchor_max_content_panel_rms": safe_float(
            anchor_summary.get("max_content_panel_normalized_residual_rms")
        ),
        "short_pair_trace_alignment_policy_label": trace_summary.get("policy_label", "not_run"),
        "short_pair_trace_alignment_supported_pair_count": safe_float(
            trace_summary.get("supported_anchor_pair_count")
        ),
        "short_pair_trace_alignment_improved_count": safe_float(
            trace_summary.get("field_trace_alignment_improved_count")
        ),
        "short_pair_trace_alignment_mean_raw_abs_correlation": safe_float(
            trace_summary.get("mean_raw_abs_correlation")
        ),
        "short_pair_trace_alignment_mean_corrected_abs_correlation": safe_float(
            trace_summary.get("mean_corrected_abs_correlation")
        ),
        "short_pair_trace_alignment_mean_abs_correlation_improvement": safe_float(
            trace_summary.get("mean_abs_correlation_improvement")
        ),
        "short_pair_trace_sensitivity_policy_label": sensitivity_summary.get("policy_label", "not_run"),
        "short_pair_trace_sensitivity_window_count": safe_float(
            sensitivity_summary.get("window_count")
        ),
        "short_pair_trace_sensitivity_pair_window_row_count": safe_float(
            sensitivity_summary.get("pair_window_row_count")
        ),
        "short_pair_trace_sensitivity_improved_pair_window_count": safe_float(
            sensitivity_summary.get("improved_pair_window_count")
        ),
        "short_pair_trace_sensitivity_min_improvement": safe_float(
            sensitivity_summary.get("min_abs_correlation_improvement")
        ),
        "short_pair_trace_sensitivity_min_corrected_abs_correlation": safe_float(
            sensitivity_summary.get("min_corrected_abs_correlation")
        ),
        "short_pair_corrected_profile_stack_policy_label": corrected_stack_summary.get("policy_label", "not_run"),
        "short_pair_corrected_profile_stack_raw_matrix_abs_correlation": safe_float(
            corrected_stack_summary.get("raw_matrix_abs_correlation")
        ),
        "short_pair_corrected_profile_stack_corrected_matrix_abs_correlation": safe_float(
            corrected_stack_summary.get("corrected_matrix_abs_correlation")
        ),
        "short_pair_corrected_profile_stack_matrix_improvement": safe_float(
            corrected_stack_summary.get("matrix_abs_correlation_improvement")
        ),
        "short_pair_corrected_profile_stack_improved_column_count": safe_float(
            corrected_stack_summary.get("improved_column_count")
        ),
        "short_pair_corrected_profile_stack_finite_column_count": safe_float(
            corrected_stack_summary.get("finite_column_count")
        ),
        "short_pair_corrected_profile_stack_improved_column_fraction": safe_float(
            corrected_stack_summary.get("improved_column_fraction")
        ),
        "short_pair_corrected_profile_stack_mean_column_improvement": safe_float(
            corrected_stack_summary.get("mean_column_abs_correlation_improvement")
        ),
        "short_pair_corrected_profile_stack_sensitivity_policy_label": (
            corrected_stack_sensitivity_summary.get("policy_label", "not_run")
        ),
        "short_pair_corrected_profile_stack_sensitivity_window_count": safe_float(
            corrected_stack_sensitivity_summary.get("window_count")
        ),
        "short_pair_corrected_profile_stack_sensitivity_robust_window_count": safe_float(
            corrected_stack_sensitivity_summary.get("robust_window_count")
        ),
        "short_pair_corrected_profile_stack_sensitivity_min_matrix_improvement": safe_float(
            corrected_stack_sensitivity_summary.get("min_matrix_abs_correlation_improvement")
        ),
        "short_pair_corrected_profile_stack_sensitivity_min_corrected_abs_correlation": safe_float(
            corrected_stack_sensitivity_summary.get("min_corrected_matrix_abs_correlation")
        ),
        "short_pair_corrected_profile_stack_sensitivity_min_improved_column_fraction": safe_float(
            corrected_stack_sensitivity_summary.get("min_improved_column_fraction")
        ),
        "short_pair_corrected_stack_spatial_support_policy_label": spatial_support_summary.get(
            "policy_label", "not_run"
        ),
        "short_pair_corrected_stack_spatial_support_majority_column_count": safe_float(
            spatial_support_summary.get("majority_supported_column_count")
        ),
        "short_pair_corrected_stack_spatial_support_majority_column_fraction": safe_float(
            spatial_support_summary.get("majority_supported_column_fraction")
        ),
        "short_pair_corrected_stack_spatial_support_all_window_column_count": safe_float(
            spatial_support_summary.get("all_window_supported_column_count")
        ),
        "short_pair_corrected_stack_spatial_support_all_window_column_fraction": safe_float(
            spatial_support_summary.get("all_window_supported_column_fraction")
        ),
        "short_pair_corrected_stack_spatial_support_interval_count": safe_float(
            spatial_support_summary.get("support_interval_count")
        ),
        "short_pair_corrected_stack_spatial_support_largest_interval_length_m": safe_float(
            spatial_support_summary.get("largest_majority_interval_length_m")
        ),
        "short_pair_supported_interval_visual_qc_policy_label": interval_visual_summary.get(
            "policy_label", "not_run"
        ),
        "short_pair_supported_interval_visual_qc_selected_count": safe_float(
            interval_visual_summary.get("selected_interval_count")
        ),
        "short_pair_supported_interval_visual_qc_supported_count": safe_float(
            interval_visual_summary.get("supported_interval_count")
        ),
        "short_pair_supported_interval_visual_qc_total_length_m": safe_float(
            interval_visual_summary.get("total_selected_interval_length_m")
        ),
        "short_pair_supported_interval_visual_qc_min_improvement": safe_float(
            interval_visual_summary.get("min_interval_abs_correlation_improvement")
        ),
        "short_pair_supported_interval_visual_qc_min_corrected_abs_correlation": safe_float(
            interval_visual_summary.get("min_corrected_interval_abs_correlation")
        ),
        "long_pair_short_correction_transfer_policy_label": long_transfer_summary.get(
            "policy_label", "not_run"
        ),
        "long_pair_short_correction_transfer_raw_matrix_abs_correlation": safe_float(
            long_transfer_summary.get("raw_matrix_abs_correlation")
        ),
        "long_pair_short_correction_transfer_corrected_matrix_abs_correlation": safe_float(
            long_transfer_summary.get("corrected_matrix_abs_correlation")
        ),
        "long_pair_short_correction_transfer_matrix_improvement": safe_float(
            long_transfer_summary.get("matrix_abs_correlation_improvement")
        ),
        "long_pair_short_correction_transfer_anchor_window_count": safe_float(
            long_transfer_summary.get("stable_anchor_window_count")
        ),
        "long_pair_short_correction_transfer_improved_anchor_count": safe_float(
            long_transfer_summary.get("improved_anchor_window_count")
        ),
        "long_pair_short_correction_transfer_min_corrected_anchor_abs_correlation": safe_float(
            long_transfer_summary.get("min_corrected_anchor_abs_correlation")
        ),
        "long_pair_shift_scan_policy_label": long_shift_summary.get("policy_label", "not_run"),
        "long_pair_shift_scan_zero_offset_matrix_abs_correlation": safe_float(
            long_shift_summary.get("zero_offset_matrix_abs_correlation")
        ),
        "long_pair_shift_scan_short_pair_offset_matrix_abs_correlation": safe_float(
            long_shift_summary.get("short_pair_offset_matrix_abs_correlation")
        ),
        "long_pair_shift_scan_short_pair_offset_gain_vs_zero": safe_float(
            long_shift_summary.get("short_pair_offset_gain_vs_zero")
        ),
        "long_pair_shift_scan_best_matrix_offset_ns": safe_float(
            long_shift_summary.get("best_matrix_offset_ns")
        ),
        "long_pair_shift_scan_best_matrix_abs_correlation": safe_float(
            long_shift_summary.get("best_matrix_abs_correlation")
        ),
        "long_pair_shift_scan_best_matrix_gain_vs_zero": safe_float(
            long_shift_summary.get("best_matrix_gain_vs_zero")
        ),
        "long_pair_shift_scan_best_anchor_improved_window_count": safe_float(
            long_shift_summary.get("best_anchor_improved_window_count")
        ),
        "long_pair_shift_scan_best_anchor_min_corrected_abs_correlation": safe_float(
            long_shift_summary.get("best_anchor_min_corrected_abs_correlation")
        ),
        "long_pair_shift_sensitivity_policy_label": long_shift_sensitivity_summary.get(
            "policy_label", "not_run"
        ),
        "long_pair_shift_sensitivity_window_count": safe_float(
            long_shift_sensitivity_summary.get("window_count")
        ),
        "long_pair_shift_sensitivity_reject_short_window_count": safe_float(
            long_shift_sensitivity_summary.get("reject_short_transfer_window_count")
        ),
        "long_pair_shift_sensitivity_best_offset_median_ns": safe_float(
            long_shift_sensitivity_summary.get("best_offset_median_ns")
        ),
        "long_pair_shift_sensitivity_best_offset_spread_ns": safe_float(
            long_shift_sensitivity_summary.get("best_offset_spread_ns")
        ),
        "long_pair_shift_sensitivity_min_best_gain": safe_float(
            long_shift_sensitivity_summary.get("min_best_matrix_gain_vs_zero")
        ),
        "long_pair_shift_sensitivity_max_short_gain": safe_float(
            long_shift_sensitivity_summary.get("max_short_pair_offset_gain_vs_zero")
        ),
        "long_pair_shift_sensitivity_min_anchor_count": safe_float(
            long_shift_sensitivity_summary.get("min_best_anchor_improved_window_count")
        ),
        "long_pair_pattern_visual_qc_policy_label": long_visual_summary.get("policy_label", "not_run"),
        "long_pair_pattern_visual_qc_supported_anchor_count": safe_float(
            long_visual_summary.get("supported_anchor_window_count")
        ),
        "long_pair_pattern_visual_qc_min_gain": safe_float(
            long_visual_summary.get("min_pattern_shift_gain")
        ),
        "long_pair_pattern_visual_qc_min_abs_correlation": safe_float(
            long_visual_summary.get("min_pattern_shift_abs_correlation")
        ),
        "long_pair_pattern_holdout_qc_policy_label": long_holdout_summary.get(
            "policy_label", "not_run"
        ),
        "long_pair_pattern_holdout_candidate_anchor_count": safe_float(
            long_holdout_summary.get("candidate_anchor_count")
        ),
        "long_pair_pattern_holdout_stable_supported_count": safe_float(
            long_holdout_summary.get("stable_supported_anchor_count")
        ),
        "long_pair_pattern_holdout_repeat_limited_supported_count": safe_float(
            long_holdout_summary.get("repeat_limited_supported_anchor_count")
        ),
        "long_pair_pattern_holdout_min_repeat_limited_gain": safe_float(
            long_holdout_summary.get("min_repeat_limited_pattern_shift_gain")
        ),
        "long_pair_pattern_holdout_min_repeat_limited_abs_correlation": safe_float(
            long_holdout_summary.get("min_repeat_limited_pattern_shift_abs_correlation")
        ),
        "long_pair_holdout_window_sensitivity_policy_label": long_window_sensitivity_summary.get(
            "policy_label", "not_run"
        ),
        "long_pair_holdout_window_sensitivity_window_count": safe_float(
            long_window_sensitivity_summary.get("window_count")
        ),
        "long_pair_holdout_window_sensitivity_supported_rows": safe_float(
            long_window_sensitivity_summary.get("supported_row_count")
        ),
        "long_pair_holdout_window_sensitivity_row_count": safe_float(
            long_window_sensitivity_summary.get("row_count")
        ),
        "long_pair_holdout_window_sensitivity_all_supported_count": safe_float(
            long_window_sensitivity_summary.get("all_window_supported_anchor_count")
        ),
        "long_pair_holdout_window_sensitivity_min_gain": safe_float(
            long_window_sensitivity_summary.get("min_pattern_shift_gain")
        ),
        "long_pair_holdout_window_sensitivity_min_abs_correlation": safe_float(
            long_window_sensitivity_summary.get("min_pattern_shift_abs_correlation")
        ),
        "long_pair_holdout_width_sensitivity_policy_label": long_width_sensitivity_summary.get(
            "policy_label", "not_run"
        ),
        "long_pair_holdout_width_sensitivity_width_count": safe_float(
            long_width_sensitivity_summary.get("width_count")
        ),
        "long_pair_holdout_width_sensitivity_supported_rows": safe_float(
            long_width_sensitivity_summary.get("supported_row_count")
        ),
        "long_pair_holdout_width_sensitivity_row_count": safe_float(
            long_width_sensitivity_summary.get("row_count")
        ),
        "long_pair_holdout_width_sensitivity_all_supported_count": safe_float(
            long_width_sensitivity_summary.get("all_width_supported_anchor_count")
        ),
        "long_pair_holdout_width_sensitivity_min_gain": safe_float(
            long_width_sensitivity_summary.get("min_pattern_shift_gain")
        ),
        "long_pair_holdout_width_sensitivity_min_abs_correlation": safe_float(
            long_width_sensitivity_summary.get("min_pattern_shift_abs_correlation")
        ),
        "field_bandlimited_repeatability_policy_label": bandlimited_summary.get(
            "policy_label", "not_run"
        ),
        "field_bandlimited_short_supported_band_count": safe_float(
            bandlimited_summary.get("short_supported_band_count")
        ),
        "field_bandlimited_short_supported_bands": bandlimited_summary.get(
            "short_supported_bands", ""
        ),
        "field_bandlimited_short_unfiltered_corrected_abs_correlation": safe_float(
            bandlimited_summary.get("short_unfiltered_corrected_abs_correlation")
        ),
        "field_bandlimited_short_unfiltered_gain": safe_float(
            bandlimited_summary.get("short_unfiltered_abs_correlation_gain")
        ),
        "field_bandlimited_long_pattern_supported_band_count": safe_float(
            bandlimited_summary.get("long_pattern_supported_band_count")
        ),
        "field_bandlimited_long_pattern_supported_bands": bandlimited_summary.get(
            "long_pattern_supported_bands", ""
        ),
        "field_bandlimited_long_unfiltered_pattern_abs_correlation": safe_float(
            bandlimited_summary.get("long_unfiltered_pattern_abs_correlation")
        ),
        "field_bandlimited_long_pattern_gain": safe_float(
            bandlimited_summary.get("long_unfiltered_pattern_gain")
        ),
        "field_bandlimited_gpu_fwi_priority": bandlimited_summary.get(
            "field_gpu_fwi_priority", "unknown"
        ),
        "field_apparent_depth_qc_policy_label": apparent_depth_summary.get(
            "policy_label", "not_run"
        ),
        "field_apparent_depth_qc_cue_count": safe_float(
            apparent_depth_summary.get("cue_count")
        ),
        "field_apparent_depth_qc_short_pair_corrected_support_count": safe_float(
            apparent_depth_summary.get("short_pair_corrected_depth_support_count")
        ),
        "field_apparent_depth_qc_short_pair_corrected_support_fraction": safe_float(
            apparent_depth_summary.get("short_pair_corrected_depth_support_fraction")
        ),
        "field_apparent_depth_qc_mean_corrected_depth_residual_mm": safe_float(
            apparent_depth_summary.get("mean_corrected_depth_residual_mm")
        ),
        "field_apparent_depth_qc_max_corrected_depth_residual_mm": safe_float(
            apparent_depth_summary.get("max_corrected_depth_residual_mm")
        ),
        "field_apparent_depth_qc_time_zero_depth_equivalent_mm": safe_float(
            apparent_depth_summary.get("time_zero_depth_equivalent_mm")
        ),
        "field_apparent_depth_qc_ready_for_apparent_depth_scale_qc": bool(
            apparent_depth_summary.get("ready_for_apparent_depth_scale_qc", False)
        ),
        "field_apparent_depth_qc_ready_for_cover_depth_recovery": bool(
            apparent_depth_summary.get("ready_for_cover_depth_recovery", False)
        ),
        "field_apparent_depth_qc_ready_for_field_fwi": bool(
            apparent_depth_summary.get("ready_for_field_fwi", False)
        ),
        "field_apparent_depth_sensitivity_policy_label": depth_sensitivity_summary.get(
            "policy_label", "not_run"
        ),
        "field_apparent_depth_sensitivity_scenario_count": safe_float(
            depth_sensitivity_summary.get("scenario_count")
        ),
        "field_apparent_depth_sensitivity_max_depth_span_mm": safe_float(
            depth_sensitivity_summary.get("max_apparent_depth_span_mm")
        ),
        "field_apparent_depth_sensitivity_factor": safe_float(
            depth_sensitivity_summary.get("max_apparent_depth_sensitivity_factor")
        ),
        "field_apparent_depth_sensitivity_all_residuals_supported": bool(
            depth_sensitivity_summary.get("all_residuals_within_budget_all_scenarios", False)
        ),
        "field_apparent_depth_sensitivity_cover_depth_claim_ready": bool(
            depth_sensitivity_summary.get("cover_depth_claim_ready", False)
        ),
        "field_apparent_depth_sensitivity_field_fwi_ready": bool(
            depth_sensitivity_summary.get("field_fwi_ready", False)
        ),
        "field_hyperbola_timezero_degeneracy_policy_label": hyperbola_degeneracy_summary.get(
            "policy_label", "not_run"
        ),
        "field_hyperbola_timezero_surface_count": safe_float(
            hyperbola_degeneracy_summary.get("surface_summary_row_count")
        ),
        "field_hyperbola_timezero_boundary_best_surface_count": safe_float(
            hyperbola_degeneracy_summary.get("boundary_best_surface_count")
        ),
        "field_hyperbola_timezero_max_near_top_epsr_span": safe_float(
            hyperbola_degeneracy_summary.get("max_near_top_epsr_span")
        ),
        "field_hyperbola_timezero_max_near_top_time_zero_span_ns": safe_float(
            hyperbola_degeneracy_summary.get("max_near_top_time_zero_span_ns")
        ),
        "field_hyperbola_timezero_max_near_top_offset_count_5pct": safe_float(
            hyperbola_degeneracy_summary.get("max_near_top_offset_count_5pct")
        ),
        "field_hyperbola_timezero_cover_depth_claim_ready": bool(
            hyperbola_degeneracy_summary.get("cover_depth_claim_ready", False)
        ),
        "field_hyperbola_timezero_radius_claim_ready": bool(
            hyperbola_degeneracy_summary.get("radius_claim_ready", False)
        ),
        "field_hyperbola_timezero_field_fwi_ready": bool(
            hyperbola_degeneracy_summary.get("field_fwi_ready", False)
        ),
        "publication_claim_bundle_policy_label": publication_summary.get("policy_label", "not_run"),
        "publication_claim_bundle_figure_row_count": safe_float(
            publication_summary.get("figure_row_count")
        ),
        "publication_claim_bundle_claim_boundary_count": safe_float(
            publication_summary.get("claim_boundary_count")
        ),
        "publication_claim_bundle_ready": bool(
            publication_summary.get("ready_for_manuscript_field_supplement", False)
        ),
        "publication_claim_bundle_gpu_priority": publication_summary.get("gpu_priority", "unknown"),
        "publication_time_zero_uncertainty_included": bool(
            publication_summary.get("time_zero_uncertainty_included", False)
        ),
        "publication_time_zero_uncertainty_policy_label": publication_summary.get(
            "time_zero_uncertainty_policy", "not_run"
        ),
        "publication_time_zero_conservative_half_width_ns": safe_float(
            publication_summary.get("time_zero_conservative_half_width_ns")
        ),
        "publication_time_zero_absolute_ready": bool(
            publication_summary.get("time_zero_absolute_ready", False)
        ),
        "publication_time_zero_perturbation_included": bool(
            publication_summary.get("time_zero_perturbation_included", False)
        ),
        "publication_time_zero_perturbation_policy_label": publication_summary.get(
            "time_zero_perturbation_policy", "not_run"
        ),
        "publication_time_zero_perturbation_bootstrap_supported_count": safe_float(
            publication_summary.get("time_zero_perturbation_bootstrap_supported_count")
        ),
        "publication_time_zero_perturbation_bootstrap_row_count": safe_float(
            publication_summary.get("time_zero_perturbation_bootstrap_row_count")
        ),
        "publication_time_zero_perturbation_conservative_supported_count": safe_float(
            publication_summary.get("time_zero_perturbation_conservative_supported_count")
        ),
        "publication_time_zero_perturbation_conservative_row_count": safe_float(
            publication_summary.get("time_zero_perturbation_conservative_row_count")
        ),
        "publication_time_zero_perturbation_min_matrix_improvement": safe_float(
            publication_summary.get("time_zero_perturbation_min_matrix_improvement")
        ),
        "publication_early_time_anchor_included": bool(
            publication_summary.get("early_time_anchor_included", False)
        ),
        "publication_early_time_anchor_policy": publication_summary.get(
            "early_time_anchor_policy",
            "not_run",
        ),
        "publication_early_time_short_pair_shift_ns": safe_float(
            publication_summary.get("early_time_short_pair_shift_ns")
        ),
        "publication_early_time_short_vs_content_delta_ns": safe_float(
            publication_summary.get("early_time_short_vs_content_delta_ns")
        ),
        "publication_early_time_short_agrees_with_content_budget": bool(
            publication_summary.get("early_time_short_agrees_with_content_budget", False)
        ),
        "publication_early_time_absolute_ready": bool(
            publication_summary.get("early_time_absolute_ready", False)
        ),
        "publication_cue_spacing_included": bool(
            publication_summary.get("cue_spacing_sensitivity_included", False)
        ),
        "publication_cue_spacing_policy": publication_summary.get(
            "cue_spacing_sensitivity_policy",
            "not_run",
        ),
        "publication_cue_spacing_threshold_count": safe_float(
            publication_summary.get("cue_spacing_threshold_count")
        ),
        "publication_cue_spacing_min_same_time_spacing_mm": safe_float(
            publication_summary.get("cue_spacing_min_same_time_spacing_mm")
        ),
        "publication_cue_spacing_ready_for_field_context": bool(
            publication_summary.get("cue_spacing_ready_for_field_context", False)
        ),
        "publication_cue_spacing_resolution_benchmark_ready": bool(
            publication_summary.get("cue_spacing_resolution_benchmark_ready", False)
        ),
        "publication_cue_spacing_field_fwi_ready": bool(
            publication_summary.get("cue_spacing_field_fwi_ready", False)
        ),
        "publication_timing_anchor_conflict_included": bool(
            publication_summary.get("timing_anchor_conflict_included", False)
        ),
        "publication_timing_anchor_conflict_policy": publication_summary.get(
            "timing_anchor_conflict_policy",
            "not_run",
        ),
        "publication_timing_anchor_early_vs_short_delta_half_widths": safe_float(
            publication_summary.get("timing_anchor_early_vs_short_delta_half_widths")
        ),
        "publication_timing_anchor_long_vs_short_delta_half_widths": safe_float(
            publication_summary.get("timing_anchor_long_vs_short_delta_half_widths")
        ),
        "publication_timing_anchor_absolute_time_zero_ready": bool(
            publication_summary.get("timing_anchor_absolute_time_zero_ready", False)
        ),
        "publication_timing_anchor_field_fwi_ready": bool(
            publication_summary.get("timing_anchor_field_fwi_ready", False)
        ),
        "publication_timing_anchor_ready_for_manuscript_boundary": bool(
            publication_summary.get("timing_anchor_ready_for_manuscript_boundary", False)
        ),
        "publication_timing_window_family_included": bool(
            publication_summary.get("timing_window_family_included", False)
        ),
        "publication_timing_window_family_policy": publication_summary.get(
            "timing_window_family_policy",
            "not_run",
        ),
        "publication_timing_window_early_strict_near_zero_lag_count": safe_float(
            publication_summary.get("timing_window_early_strict_near_zero_lag_count")
        ),
        "publication_timing_window_early_strict_row_count": safe_float(
            publication_summary.get("timing_window_early_strict_row_count")
        ),
        "publication_timing_window_short_nonraw_supported_count": safe_float(
            publication_summary.get("timing_window_short_nonraw_supported_count")
        ),
        "publication_timing_window_short_nonraw_row_count": safe_float(
            publication_summary.get("timing_window_short_nonraw_row_count")
        ),
        "publication_timing_window_long_reject_short_transfer_count": safe_float(
            publication_summary.get("timing_window_long_reject_short_transfer_count")
        ),
        "publication_timing_window_long_row_count": safe_float(
            publication_summary.get("timing_window_long_row_count")
        ),
        "publication_timing_window_absolute_time_zero_ready": bool(
            publication_summary.get("timing_window_absolute_time_zero_ready", False)
        ),
        "publication_timing_window_field_fwi_ready": bool(
            publication_summary.get("timing_window_field_fwi_ready", False)
        ),
        "publication_timing_window_ready_for_manuscript_boundary": bool(
            publication_summary.get("timing_window_ready_for_manuscript_boundary", False)
        ),
        "publication_timing_discriminant_included": bool(
            publication_summary.get("timing_discriminant_included", False)
        ),
        "publication_timing_discriminant_policy": publication_summary.get(
            "timing_discriminant_policy",
            "not_run",
        ),
        "publication_timing_discriminant_score_row_count": safe_float(
            publication_summary.get("timing_discriminant_score_row_count")
        ),
        "publication_timing_discriminant_short_nonraw_supported_count": safe_float(
            publication_summary.get("timing_discriminant_short_nonraw_supported_count")
        ),
        "publication_timing_discriminant_long_reject_short_transfer_count": safe_float(
            publication_summary.get("timing_discriminant_long_reject_short_transfer_count")
        ),
        "publication_timing_discriminant_absolute_time_zero_ready": bool(
            publication_summary.get("timing_discriminant_absolute_time_zero_ready", False)
        ),
        "publication_timing_discriminant_field_fwi_ready": bool(
            publication_summary.get("timing_discriminant_field_fwi_ready", False)
        ),
        "publication_timing_discriminant_ready_for_scorecard": bool(
            publication_summary.get("timing_discriminant_ready_for_scorecard", False)
        ),
        "publication_hpc_dimensionality_included": bool(
            publication_summary.get("hpc_dimensionality_included", False)
        ),
        "publication_hpc_dimensionality_policy": publication_summary.get(
            "hpc_dimensionality_policy",
            "not_run",
        ),
        "publication_hpc_dimensionality_field_geometry_type": publication_summary.get(
            "hpc_dimensionality_field_geometry_type",
            "",
        ),
        "publication_hpc_dimensionality_is_3d_survey": bool(
            publication_summary.get("hpc_dimensionality_is_3d_survey", False)
        ),
        "publication_hpc_dimensionality_ready_for_2d_qc": bool(
            publication_summary.get("hpc_dimensionality_ready_for_2d_qc", False)
        ),
        "publication_hpc_dimensionality_ready_for_3d_hpc": bool(
            publication_summary.get("hpc_dimensionality_ready_for_3d_hpc", False)
        ),
        "publication_hpc_dimensionality_ready_for_field_fwi": bool(
            publication_summary.get("hpc_dimensionality_ready_for_field_fwi", False)
        ),
        "publication_hpc_dimensionality_field_hpc_priority": publication_summary.get(
            "hpc_dimensionality_field_hpc_priority",
            "",
        ),
        "publication_acquisition_readiness_included": bool(
            publication_summary.get("acquisition_readiness_included", False)
        ),
        "publication_acquisition_readiness_policy": publication_summary.get(
            "acquisition_readiness_policy",
            "",
        ),
        "publication_acquisition_ready_for_3d_hpc": bool(
            publication_summary.get("acquisition_readiness_ready_for_3d_hpc", False)
        ),
        "publication_acquisition_ready_for_field_fwi": bool(
            publication_summary.get("acquisition_readiness_ready_for_field_fwi", False)
        ),
        "publication_acquisition_field_hpc_priority": publication_summary.get(
            "acquisition_readiness_field_hpc_priority",
            "",
        ),
        "long_pair_relaxed_phase_anchor_policy_label": long_relaxed_policy_label,
        "long_pair_relaxed_phase_anchor_profile_count": safe_float(
            long_relaxed_summary.get("profile_count")
        ),
        "long_pair_relaxed_phase_anchor_pick_count": long_relaxed_pick_count,
        "long_pair_relaxed_phase_anchor_low_snr_count": long_relaxed_low_snr_count,
        "long_pair_relaxed_phase_anchor_boundary_solution_count": long_relaxed_boundary_count,
        "long_pair_relaxed_phase_anchor_best_phase_convention": long_relaxed_best.get(
            "phase_convention", ""
        ),
        "long_pair_relaxed_phase_anchor_median_depth_m": safe_float(
            long_relaxed_best.get("median_depth_m")
        ),
        "long_pair_relaxed_phase_anchor_plausible_depth": bool(
            long_relaxed_best.get("plausible_depth_15_to_120mm", False)
        ),
        "short_pair_content_panel_policy_label": panel_summary.get("policy_label", "not_run"),
        "short_pair_content_panel_count": safe_float(panel_summary.get("panel_count")),
        "short_pair_content_panel_valid_count": safe_float(panel_summary.get("valid_panel_count")),
        "short_pair_content_panel_pair_count": safe_float(panel_summary.get("content_backed_pair_count")),
        "short_pair_content_panel_min_abs_correlation": safe_float(
            panel_summary.get("min_absolute_correlation")
        ),
        "short_pair_content_panel_mean_abs_correlation": safe_float(
            panel_summary.get("mean_absolute_correlation")
        ),
    }


def evidence_rows(
    survey: dict,
    network: dict,
    short: dict,
    long: dict,
    time_zero: dict | None = None,
    applied_time_zero: dict | None = None,
    phase_convention: dict | None = None,
    timing_bootstrap: dict | None = None,
    content_windows: dict | None = None,
    content_synthetic: dict | None = None,
    content_time_zero_anchor: dict | None = None,
    content_trace_alignment: dict | None = None,
    content_trace_sensitivity: dict | None = None,
    content_panels: dict | None = None,
    corrected_profile_stack: dict | None = None,
    corrected_profile_stack_sensitivity: dict | None = None,
    corrected_stack_spatial_support: dict | None = None,
    supported_interval_visual_qc: dict | None = None,
    long_profile_transfer_audit: dict | None = None,
    long_profile_shift_scan: dict | None = None,
    long_profile_shift_sensitivity: dict | None = None,
    long_profile_pattern_visual_qc: dict | None = None,
    long_profile_pattern_holdout_qc: dict | None = None,
    long_profile_holdout_sensitivity: dict | None = None,
    long_profile_holdout_width_sensitivity: dict | None = None,
    publication_claim_bundle: dict | None = None,
    long_profile_relaxed_phase_anchor: dict | None = None,
    bandlimited_repeatability: dict | None = None,
    apparent_depth_qc: dict | None = None,
    apparent_depth_sensitivity: dict | None = None,
    hyperbola_timezero_degeneracy: dict | None = None,
) -> list[dict]:
    short_summary = short["summary"]
    long_summary = long["summary"]
    time_zero_summary = (time_zero or {}).get("summary", {})
    applied_summary = (applied_time_zero or {}).get("summary", {})
    phase_summary = (phase_convention or {}).get("summary", {})
    bootstrap_summary = (timing_bootstrap or {}).get("summary", {})
    content_summary = (content_windows or {}).get("summary", {})
    synthetic_summary = (content_synthetic or {}).get("summary", {})
    anchor_summary = content_time_zero_anchor or {}
    trace_summary = content_trace_alignment or {}
    sensitivity_summary = content_trace_sensitivity or {}
    panel_summary = content_panels or {}
    corrected_stack_summary = (corrected_profile_stack or {}).get("summary", {})
    corrected_stack_sensitivity_summary = corrected_profile_stack_sensitivity or {}
    spatial_support_summary = corrected_stack_spatial_support or {}
    interval_visual_summary = supported_interval_visual_qc or {}
    long_transfer_summary = (long_profile_transfer_audit or {}).get("summary", {})
    long_shift_summary = (long_profile_shift_scan or {}).get("summary", {})
    long_shift_sensitivity_summary = long_profile_shift_sensitivity or {}
    long_visual_summary = long_profile_pattern_visual_qc or {}
    long_holdout_summary = long_profile_pattern_holdout_qc or {}
    long_window_sensitivity_summary = long_profile_holdout_sensitivity or {}
    long_width_sensitivity_summary = long_profile_holdout_width_sensitivity or {}
    publication_summary = publication_claim_bundle or {}
    long_relaxed_summary = long_profile_relaxed_phase_anchor or {}
    bandlimited_summary = bandlimited_repeatability or {}
    apparent_depth_summary = apparent_depth_qc or {}
    depth_sensitivity_summary = apparent_depth_sensitivity or {}
    hyperbola_degeneracy_summary = hyperbola_timezero_degeneracy or {}
    long_relaxed_best = long_relaxed_summary.get("best_phase_hypothesis", {})
    long_relaxed_pick_count = safe_float(long_relaxed_summary.get("phase_anchor_pick_count"))
    long_relaxed_low_snr_count = safe_float(long_relaxed_summary.get("low_snr_phase_anchor_pick_count"))
    long_relaxed_boundary_count = safe_float(long_relaxed_best.get("boundary_solution_count"))
    if long_relaxed_pick_count > 0 and long_relaxed_low_snr_count >= long_relaxed_pick_count:
        long_relaxed_policy_label = "long_profile_relaxed_phase_anchor_low_snr_not_time_zero"
    elif long_relaxed_boundary_count > 0:
        long_relaxed_policy_label = "long_profile_relaxed_phase_anchor_boundary_limited"
    elif long_relaxed_pick_count > 0:
        long_relaxed_policy_label = "long_profile_relaxed_phase_anchor_review_needed"
    else:
        long_relaxed_policy_label = "not_run"
    rows = [
        {
            "evidence": "survey_geometry",
            "status": survey.get("classification"),
            "correlation": "",
            "stable_stack_anchor_count": "",
            "event_pair_count": "",
            "limitation": "; ".join(survey.get("reasons", [])),
        },
        {
            "evidence": "profile_network",
            "status": network.get("decision"),
            "correlation": safe_float(network.get("strongest_pair", {}).get("best_normalized_correlation")),
            "stable_stack_anchor_count": "",
            "event_pair_count": "",
            "limitation": f"embedded_segment_candidate_count={network.get('pair_label_counts', {}).get('embedded_segment_candidate', 0)}",
        },
        {
            "evidence": "short_pair_014_016",
            "status": short_summary["policy_label"],
            "correlation": short_summary["best_normalized_correlation"],
            "stable_stack_anchor_count": short_summary["stable_stack_anchor_count"],
            "event_pair_count": short_summary["event_pair_count"],
            "limitation": f"radius_match_fraction={short_summary['radius_match_fraction']}",
        },
        {
            "evidence": "long_pair_015_013",
            "status": long_summary["policy_label"],
            "correlation": long_summary["best_normalized_correlation"],
            "stable_stack_anchor_count": long_summary["stable_stack_anchor_count"],
            "event_pair_count": 0,
            "limitation": "profile_013_no_phase_anchor_picks",
        },
    ]
    if long_relaxed_summary:
        rows.append({
            "evidence": "long_pair_relaxed_phase_anchor_audit",
            "status": long_relaxed_policy_label,
            "correlation": safe_float(long_relaxed_best.get("mean_profile_score")),
            "stable_stack_anchor_count": max(0.0, long_relaxed_pick_count - long_relaxed_low_snr_count),
            "event_pair_count": long_relaxed_pick_count,
            "limitation": (
                "low_snr_picks="
                f"{long_relaxed_low_snr_count:.0f}/{long_relaxed_pick_count:.0f}; "
                "boundary_solutions="
                f"{long_relaxed_boundary_count:.0f}; "
                "relaxed_late_window_no_time_zero_upgrade"
            ),
        })
    if time_zero_summary:
        rows.append({
            "evidence": "short_pair_time_zero_transfer",
            "status": time_zero_summary["policy_label"],
            "correlation": "",
            "stable_stack_anchor_count": time_zero_summary["stable_stack_anchor_count"],
            "event_pair_count": time_zero_summary["event_pair_count"],
            "limitation": (
                "relative_offset_ns="
                f"{safe_float(time_zero_summary['median_comparison_minus_reference_phase_time_ns']):.6f}; "
                "not_absolute_time_zero"
            ),
        })
    if applied_summary:
        rows.append({
            "evidence": "short_pair_applied_time_zero",
            "status": applied_summary["policy_label"],
            "correlation": "",
            "stable_stack_anchor_count": "",
            "event_pair_count": applied_summary["event_pair_count"],
            "limitation": (
                "mean_abs_residual_reduction="
                f"{safe_float(applied_summary['mean_abs_residual_reduction_factor']):.3f}x; "
                "still_no_geometry_radius_depth_claim"
            ),
        })
    if phase_summary:
        rows.append({
            "evidence": "short_pair_phase_convention_transfer",
            "status": phase_summary["policy_label"],
            "correlation": "",
            "stable_stack_anchor_count": phase_summary["stable_phase_convention_count"],
            "event_pair_count": "",
            "limitation": (
                "stable_conventions="
                f"{phase_summary['stable_phase_convention_count']}/"
                f"{phase_summary['phase_convention_count']}; "
                "relative_timing_qc_only"
            ),
        })
    if bootstrap_summary:
        rows.append({
            "evidence": "short_pair_timing_bootstrap",
            "status": bootstrap_summary["policy_label"],
            "correlation": "",
            "stable_stack_anchor_count": bootstrap_summary["stable_phase_convention_count"],
            "event_pair_count": "",
            "limitation": (
                "bootstrap_ci_ns="
                f"{safe_float(bootstrap_summary['min_bootstrap_ci_lower_ns']):.6f}-"
                f"{safe_float(bootstrap_summary['max_bootstrap_ci_upper_ns']):.6f}; "
                "relative_timing_qc_only"
            ),
        })
    if content_summary:
        rows.append({
            "evidence": "short_pair_content_windows",
            "status": content_summary["policy_label"],
            "correlation": "",
            "stable_stack_anchor_count": content_summary["stable_content_window_count"],
            "event_pair_count": content_summary["event_pair_count"],
            "limitation": (
                "content_backed_events="
                f"{content_summary['content_backed_event_pair_count']}/"
                f"{content_summary['event_pair_count']}; "
                f"timing_only_events={content_summary['timing_only_event_pair_count']}; "
                "content_qc_only"
            ),
        })
    if synthetic_summary:
        rows.append({
            "evidence": "short_pair_content_synthetic_waveform_qc",
            "status": synthetic_summary["policy_label"],
            "correlation": safe_float(synthetic_summary["min_content_pair_absolute_correlation"]),
            "stable_stack_anchor_count": synthetic_summary["content_backed_waveform_supported_count"],
            "event_pair_count": synthetic_summary["event_pair_count"],
            "limitation": (
                "content_waveform_supported="
                f"{synthetic_summary['content_backed_waveform_supported_count']}/"
                f"{synthetic_summary['content_backed_event_pair_count']}; "
                "timing_only_waveform_supported="
                f"{synthetic_summary['timing_only_waveform_supported_count']}; "
                "visual_qc_only"
            ),
        })
    if anchor_summary:
        rows.append({
            "evidence": "short_pair_content_time_zero_anchors",
            "status": anchor_summary["policy_label"],
            "correlation": safe_float(anchor_summary["min_content_pair_absolute_correlation"]),
            "stable_stack_anchor_count": anchor_summary["supported_content_anchor_pair_count"],
            "event_pair_count": anchor_summary["event_pair_count"],
            "limitation": (
                "supported_content_anchors="
                f"{anchor_summary['supported_content_anchor_pair_count']}/"
                f"{anchor_summary['content_backed_event_pair_count']}; "
                "time_zero_visual_qc_only"
            ),
        })
    if trace_summary:
        rows.append({
            "evidence": "short_pair_content_anchor_trace_alignment",
            "status": trace_summary["policy_label"],
            "correlation": safe_float(trace_summary["mean_corrected_abs_correlation"]),
            "stable_stack_anchor_count": trace_summary["field_trace_alignment_improved_count"],
            "event_pair_count": trace_summary["supported_anchor_pair_count"],
            "limitation": (
                "mean_abs_corr="
                f"{safe_float(trace_summary['mean_raw_abs_correlation']):.3f}->"
                f"{safe_float(trace_summary['mean_corrected_abs_correlation']):.3f}; "
                "measured_trace_time_zero_qc_only"
            ),
        })
    if sensitivity_summary:
        rows.append({
            "evidence": "short_pair_content_anchor_trace_alignment_sensitivity",
            "status": sensitivity_summary["policy_label"],
            "correlation": safe_float(sensitivity_summary["min_corrected_abs_correlation"]),
            "stable_stack_anchor_count": sensitivity_summary["improved_pair_window_count"],
            "event_pair_count": sensitivity_summary["pair_window_row_count"],
            "limitation": (
                "all_pair_windows_improved="
                f"{sensitivity_summary['improved_pair_window_count']}/"
                f"{sensitivity_summary['pair_window_row_count']}; "
                "window_robust_time_zero_qc_only"
            ),
        })
    if panel_summary:
        rows.append({
            "evidence": "short_pair_content_backed_waveform_panels",
            "status": panel_summary["policy_label"],
            "correlation": safe_float(panel_summary["min_absolute_correlation"]),
            "stable_stack_anchor_count": panel_summary["content_backed_pair_count"],
            "event_pair_count": panel_summary["panel_count"],
            "limitation": (
                "valid_panels="
                f"{panel_summary['valid_panel_count']}/"
                f"{panel_summary['panel_count']}; "
                "visual_qc_only_no_field_inversion"
            ),
        })
    if corrected_stack_summary:
        rows.append({
            "evidence": "short_pair_corrected_profile_stack",
            "status": corrected_stack_summary["policy_label"],
            "correlation": safe_float(corrected_stack_summary["corrected_matrix_abs_correlation"]),
            "stable_stack_anchor_count": corrected_stack_summary["improved_column_count"],
            "event_pair_count": corrected_stack_summary["finite_column_count"],
            "limitation": (
                "matrix_abs_corr="
                f"{safe_float(corrected_stack_summary['raw_matrix_abs_correlation']):.3f}->"
                f"{safe_float(corrected_stack_summary['corrected_matrix_abs_correlation']):.3f}; "
                "improved_columns="
                f"{corrected_stack_summary['improved_column_count']}/"
                f"{corrected_stack_summary['finite_column_count']}; "
                "bscan_time_zero_qc_only"
            ),
        })
    if corrected_stack_sensitivity_summary:
        rows.append({
            "evidence": "short_pair_corrected_profile_stack_sensitivity",
            "status": corrected_stack_sensitivity_summary["policy_label"],
            "correlation": safe_float(
                corrected_stack_sensitivity_summary["min_corrected_matrix_abs_correlation"]
            ),
            "stable_stack_anchor_count": corrected_stack_sensitivity_summary["robust_window_count"],
            "event_pair_count": corrected_stack_sensitivity_summary["window_count"],
            "limitation": (
                "robust_windows="
                f"{corrected_stack_sensitivity_summary['robust_window_count']}/"
                f"{corrected_stack_sensitivity_summary['window_count']}; "
                "min_matrix_improvement="
                f"{safe_float(corrected_stack_sensitivity_summary['min_matrix_abs_correlation_improvement']):.3f}; "
                "window_robust_bscan_time_zero_qc_only"
            ),
        })
    if spatial_support_summary:
        rows.append({
            "evidence": "short_pair_corrected_stack_spatial_support",
            "status": spatial_support_summary["policy_label"],
            "correlation": safe_float(spatial_support_summary["majority_supported_column_fraction"]),
            "stable_stack_anchor_count": spatial_support_summary["majority_supported_column_count"],
            "event_pair_count": spatial_support_summary["finite_column_count"],
            "limitation": (
                "majority_supported_columns="
                f"{spatial_support_summary['majority_supported_column_count']}/"
                f"{spatial_support_summary['finite_column_count']}; "
                "largest_interval_m="
                f"{safe_float(spatial_support_summary['largest_majority_interval_length_m']):.3f}; "
                "spatial_mask_limits_visual_qc"
            ),
        })
    if interval_visual_summary:
        rows.append({
            "evidence": "short_pair_supported_interval_visual_qc",
            "status": interval_visual_summary["policy_label"],
            "correlation": safe_float(interval_visual_summary["min_corrected_interval_abs_correlation"]),
            "stable_stack_anchor_count": interval_visual_summary["supported_interval_count"],
            "event_pair_count": interval_visual_summary["selected_interval_count"],
            "limitation": (
                "supported_intervals="
                f"{interval_visual_summary['supported_interval_count']}/"
                f"{interval_visual_summary['selected_interval_count']}; "
                "selected_length_m="
                f"{safe_float(interval_visual_summary['total_selected_interval_length_m']):.3f}; "
                "supported_regions_visual_qc_only"
            ),
        })
    if long_transfer_summary:
        rows.append({
            "evidence": "long_pair_short_correction_transfer_audit",
            "status": long_transfer_summary["policy_label"],
            "correlation": safe_float(long_transfer_summary["corrected_matrix_abs_correlation"]),
            "stable_stack_anchor_count": long_transfer_summary["improved_anchor_window_count"],
            "event_pair_count": long_transfer_summary["stable_anchor_window_count"],
            "limitation": (
                "matrix_abs_corr="
                f"{safe_float(long_transfer_summary['raw_matrix_abs_correlation']):.3f}->"
                f"{safe_float(long_transfer_summary['corrected_matrix_abs_correlation']):.3f}; "
                "improved_anchor_windows="
                f"{long_transfer_summary['improved_anchor_window_count']}/"
                f"{long_transfer_summary['stable_anchor_window_count']}; "
                "short_pair_correction_not_transferable_to_long_pair"
            ),
        })
    if long_shift_summary:
        rows.append({
            "evidence": "long_pair_pattern_shift_scan",
            "status": long_shift_summary["policy_label"],
            "correlation": safe_float(long_shift_summary["best_matrix_abs_correlation"]),
            "stable_stack_anchor_count": long_shift_summary["best_anchor_improved_window_count"],
            "event_pair_count": long_shift_summary["scanned_offset_count"],
            "limitation": (
                "short_offset_gain_vs_zero="
                f"{safe_float(long_shift_summary['short_pair_offset_gain_vs_zero']):.3f}; "
                "best_pattern_offset_ns="
                f"{safe_float(long_shift_summary['best_matrix_offset_ns']):.3f}; "
                "pattern_only_no_phase_anchor_picks"
            ),
        })
    if long_shift_sensitivity_summary:
        rows.append({
            "evidence": "long_pair_pattern_shift_sensitivity",
            "status": long_shift_sensitivity_summary["policy_label"],
            "correlation": safe_float(long_shift_sensitivity_summary["min_best_matrix_gain_vs_zero"]),
            "stable_stack_anchor_count": long_shift_sensitivity_summary[
                "min_best_anchor_improved_window_count"
            ],
            "event_pair_count": long_shift_sensitivity_summary["window_count"],
            "limitation": (
                "best_offset_median_ns="
                f"{safe_float(long_shift_sensitivity_summary['best_offset_median_ns']):.3f}; "
                "offset_spread_ns="
                f"{safe_float(long_shift_sensitivity_summary['best_offset_spread_ns']):.3f}; "
                "pattern_shift_stability_only"
            ),
        })
    if long_visual_summary:
        rows.append({
            "evidence": "long_pair_pattern_visual_qc",
            "status": long_visual_summary["policy_label"],
            "correlation": safe_float(long_visual_summary["min_pattern_shift_abs_correlation"]),
            "stable_stack_anchor_count": long_visual_summary["supported_anchor_window_count"],
            "event_pair_count": long_visual_summary["selected_anchor_window_count"],
            "limitation": (
                "supported_stable_anchors="
                f"{long_visual_summary['supported_anchor_window_count']}/"
                f"{long_visual_summary['selected_anchor_window_count']}; "
                "pattern_visual_qc_only"
            ),
        })
    if long_holdout_summary:
        rows.append({
            "evidence": "long_pair_pattern_holdout_qc",
            "status": long_holdout_summary["policy_label"],
            "correlation": safe_float(
                long_holdout_summary["min_repeat_limited_pattern_shift_abs_correlation"]
            ),
            "stable_stack_anchor_count": (
                safe_float(long_holdout_summary["stable_supported_anchor_count"], 0.0)
                + safe_float(long_holdout_summary["repeat_limited_supported_anchor_count"], 0.0)
            ),
            "event_pair_count": long_holdout_summary["candidate_anchor_count"],
            "limitation": (
                "stable_supported="
                f"{long_holdout_summary['stable_supported_anchor_count']}/"
                f"{long_holdout_summary['stable_anchor_count']}; "
                "repeat_limited_supported="
                f"{long_holdout_summary['repeat_limited_supported_anchor_count']}/"
                f"{long_holdout_summary['repeat_limited_anchor_count']}; "
                "holdout_pattern_qc_only"
            ),
        })
    if long_window_sensitivity_summary:
        rows.append({
            "evidence": "long_pair_pattern_holdout_window_sensitivity",
            "status": long_window_sensitivity_summary["policy_label"],
            "correlation": safe_float(
                long_window_sensitivity_summary["min_pattern_shift_abs_correlation"]
            ),
            "stable_stack_anchor_count": long_window_sensitivity_summary[
                "all_window_supported_anchor_count"
            ],
            "event_pair_count": long_window_sensitivity_summary["row_count"],
            "limitation": (
                "supported_rows="
                f"{long_window_sensitivity_summary['supported_row_count']}/"
                f"{long_window_sensitivity_summary['row_count']}; "
                "windows="
                f"{long_window_sensitivity_summary['window_count']}; "
                "time_window_sensitivity_qc_only"
            ),
        })
    if long_width_sensitivity_summary:
        rows.append({
            "evidence": "long_pair_pattern_holdout_width_sensitivity",
            "status": long_width_sensitivity_summary["policy_label"],
            "correlation": safe_float(
                long_width_sensitivity_summary["min_pattern_shift_abs_correlation"]
            ),
            "stable_stack_anchor_count": long_width_sensitivity_summary[
                "all_width_supported_anchor_count"
            ],
            "event_pair_count": long_width_sensitivity_summary["row_count"],
            "limitation": (
                "supported_rows="
                f"{long_width_sensitivity_summary['supported_row_count']}/"
                f"{long_width_sensitivity_summary['row_count']}; "
                "widths="
                f"{long_width_sensitivity_summary['width_count']}; "
                "spatial_width_sensitivity_qc_only"
            ),
        })
    if bandlimited_summary:
        rows.append({
            "evidence": "field_bandlimited_repeatability_audit",
            "status": bandlimited_summary["policy_label"],
            "correlation": safe_float(
                bandlimited_summary["short_unfiltered_corrected_abs_correlation"]
            ),
            "stable_stack_anchor_count": bandlimited_summary["short_supported_band_count"],
            "event_pair_count": bandlimited_summary["long_pattern_supported_band_count"],
            "limitation": (
                "short_supported_bands="
                f"{bandlimited_summary['short_supported_bands']}; "
                "long_pattern_supported_bands="
                f"{bandlimited_summary['long_pattern_supported_bands']}; "
                "gpu_fwi_priority="
                f"{bandlimited_summary['field_gpu_fwi_priority']}; "
                "band_qc_only_no_time_zero_upgrade"
            ),
        })
    if apparent_depth_summary:
        rows.append({
            "evidence": "field_apparent_depth_scale_qc",
            "status": apparent_depth_summary["policy_label"],
            "correlation": safe_float(
                apparent_depth_summary["short_pair_corrected_depth_support_fraction"]
            ),
            "stable_stack_anchor_count": apparent_depth_summary[
                "short_pair_corrected_depth_support_count"
            ],
            "event_pair_count": apparent_depth_summary["cue_count"],
            "limitation": (
                "mean_corrected_depth_residual_mm="
                f"{safe_float(apparent_depth_summary['mean_corrected_depth_residual_mm']):.3f}; "
                "max_corrected_depth_residual_mm="
                f"{safe_float(apparent_depth_summary['max_corrected_depth_residual_mm']):.3f}; "
                "depth_budget_mm="
                f"{safe_float(apparent_depth_summary['time_zero_depth_equivalent_mm']):.3f}; "
                "relative_apparent_depth_qc_only"
            ),
        })
    if depth_sensitivity_summary:
        rows.append({
            "evidence": "field_apparent_depth_sensitivity_qc",
            "status": depth_sensitivity_summary["policy_label"],
            "correlation": safe_float(
                depth_sensitivity_summary["max_apparent_depth_sensitivity_factor"]
            ),
            "stable_stack_anchor_count": (
                depth_sensitivity_summary["all_residuals_within_budget_scenario_count"]
            ),
            "event_pair_count": depth_sensitivity_summary["scenario_count"],
            "limitation": (
                "max_depth_span_mm="
                f"{safe_float(depth_sensitivity_summary['max_apparent_depth_span_mm']):.3f}; "
                "sensitivity_factor="
                f"{safe_float(depth_sensitivity_summary['max_apparent_depth_sensitivity_factor']):.2f}x; "
                "cover_depth_ready="
                f"{depth_sensitivity_summary['cover_depth_claim_ready']}; "
                "dielectric_sensitivity_blocks_calibrated_depth"
            ),
        })
    if hyperbola_degeneracy_summary:
        rows.append({
            "evidence": "field_hyperbola_timezero_degeneracy_audit",
            "status": hyperbola_degeneracy_summary["policy_label"],
            "correlation": safe_float(
                hyperbola_degeneracy_summary["max_near_top_epsr_span"]
            ),
            "stable_stack_anchor_count": hyperbola_degeneracy_summary[
                "boundary_best_surface_count"
            ],
            "event_pair_count": hyperbola_degeneracy_summary["surface_summary_row_count"],
            "limitation": (
                "boundary_best_surfaces="
                f"{hyperbola_degeneracy_summary['boundary_best_surface_count']}/"
                f"{hyperbola_degeneracy_summary['surface_summary_row_count']}; "
                "max_time_zero_span_ns="
                f"{safe_float(hyperbola_degeneracy_summary['max_near_top_time_zero_span_ns']):.3f}; "
                "max_offsets_at_5pct="
                f"{safe_float(hyperbola_degeneracy_summary['max_near_top_offset_count_5pct']):.0f}; "
                "no_cover_depth_radius_or_field_fwi"
            ),
        })
    if publication_summary:
        rows.append({
            "evidence": "field_publication_claim_bundle",
            "status": publication_summary["policy_label"],
            "correlation": "",
            "stable_stack_anchor_count": publication_summary["figure_row_count"],
            "event_pair_count": publication_summary["claim_boundary_count"],
            "limitation": (
                "ready="
                f"{publication_summary['ready_for_manuscript_field_supplement']}; "
                "gpu_priority="
                f"{publication_summary['gpu_priority']}; "
                "time_zero_budget="
                f"{publication_summary.get('time_zero_uncertainty_included', False)}; "
                "time_zero_perturbation="
                f"{publication_summary.get('time_zero_perturbation_included', False)}; "
                "early_time_anchor="
                f"{publication_summary.get('early_time_anchor_included', False)}; "
                "cue_spacing="
                f"{publication_summary.get('cue_spacing_sensitivity_included', False)}; "
                "timing_anchor_conflict="
                f"{publication_summary.get('timing_anchor_conflict_included', False)}; "
                "timing_window_family="
                f"{publication_summary.get('timing_window_family_included', False)}; "
                "acquisition_readiness="
                f"{publication_summary.get('acquisition_readiness_included', False)}; "
                "claim_bundle_no_field_fwi_or_3d"
            ),
        })
        if publication_summary.get("cue_spacing_sensitivity_included", False):
            rows.append({
                "evidence": "field_cue_spacing_context_bundle",
                "status": publication_summary.get("cue_spacing_sensitivity_policy", "not_run"),
                "correlation": safe_float(
                    publication_summary.get("cue_spacing_min_same_time_spacing_mm")
                ),
                "stable_stack_anchor_count": safe_float(
                    publication_summary.get("cue_spacing_threshold_count")
                ),
                "event_pair_count": safe_float(
                    publication_summary.get("cue_spacing_max_same_time_pair_count")
                ),
                "limitation": (
                    "min_same_time_spacing_mm="
                    f"{safe_float(publication_summary.get('cue_spacing_min_same_time_spacing_mm')):.3f}; "
                    "resolution_ready="
                    f"{publication_summary.get('cue_spacing_resolution_benchmark_ready', False)}; "
                    "field_fwi_ready="
                    f"{publication_summary.get('cue_spacing_field_fwi_ready', False)}; "
                    "measured_field_context_only_not_known_truth_resolution"
                ),
            })
        if publication_summary.get("timing_anchor_conflict_included", False):
            rows.append({
                "evidence": "field_timing_anchor_conflict_bundle",
                "status": publication_summary.get("timing_anchor_conflict_policy", "not_run"),
                "correlation": safe_float(
                    publication_summary.get("timing_anchor_early_vs_short_delta_half_widths")
                ),
                "stable_stack_anchor_count": safe_float(
                    publication_summary.get("timing_anchor_long_vs_short_delta_half_widths")
                ),
                "event_pair_count": 1,
                "limitation": (
                    "early_vs_short_delta_half_widths="
                    f"{safe_float(publication_summary.get('timing_anchor_early_vs_short_delta_half_widths')):.3f}; "
                    "long_vs_short_delta_half_widths="
                    f"{safe_float(publication_summary.get('timing_anchor_long_vs_short_delta_half_widths')):.3f}; "
                    "absolute_ready="
                    f"{publication_summary.get('timing_anchor_absolute_time_zero_ready', False)}; "
                    "field_fwi_ready="
                    f"{publication_summary.get('timing_anchor_field_fwi_ready', False)}; "
                    "timing_scope_boundary_only"
                ),
            })
        if publication_summary.get("timing_window_family_included", False):
            rows.append({
                "evidence": "field_timing_window_family_bundle",
                "status": publication_summary.get("timing_window_family_policy", "not_run"),
                "correlation": safe_float(
                    publication_summary.get("timing_window_short_nonraw_supported_count")
                ),
                "stable_stack_anchor_count": safe_float(
                    publication_summary.get("timing_window_early_strict_near_zero_lag_count")
                ),
                "event_pair_count": safe_float(
                    publication_summary.get("timing_window_long_reject_short_transfer_count")
                ),
                "limitation": (
                    "early_strict_near_zero="
                    f"{safe_float(publication_summary.get('timing_window_early_strict_near_zero_lag_count')):.0f}/"
                    f"{safe_float(publication_summary.get('timing_window_early_strict_row_count')):.0f}; "
                    "short_nonraw_supported="
                    f"{safe_float(publication_summary.get('timing_window_short_nonraw_supported_count')):.0f}/"
                    f"{safe_float(publication_summary.get('timing_window_short_nonraw_row_count')):.0f}; "
                    "long_reject_short_transfer="
                    f"{safe_float(publication_summary.get('timing_window_long_reject_short_transfer_count')):.0f}/"
                    f"{safe_float(publication_summary.get('timing_window_long_row_count')):.0f}; "
                    "absolute_ready="
                    f"{publication_summary.get('timing_window_absolute_time_zero_ready', False)}; "
                    "field_fwi_ready="
                    f"{publication_summary.get('timing_window_field_fwi_ready', False)}; "
                    "window_family_boundary_only"
                ),
            })
    return rows


def plot_field_policy(rows: list[dict], decision: dict, save_path: Path) -> str:
    pair_rows = [row for row in rows if row["evidence"] in {"short_pair_014_016", "long_pair_015_013"}]
    labels = ["014/016 short", "015/013 long"]
    corr = [safe_float(row["correlation"], 0.0) for row in pair_rows]
    anchors = [safe_float(row["stable_stack_anchor_count"], 0.0) for row in pair_rows]
    events = [safe_float(row["event_pair_count"], 0.0) for row in pair_rows]

    fig, axes = plt.subplots(1, 20, figsize=(76.0, 4.8), constrained_layout=True)
    x = np.arange(len(labels))
    axes[0].bar(x - 0.18, corr, width=0.36, color="#4c78a8", label="alignment correlation")
    axes[0].bar(x + 0.18, [value / max(1.0, max(anchors)) for value in anchors], width=0.36, color="#2ca02c", label="stable anchors scaled")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0, 1.05)
    axes[0].set_title("Repeat evidence by profile pair")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x, events, color=["#4c78a8", "#c7302b"])
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("paired phase events")
    axes[1].set_title("Timing support remains short-pair only")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    raw_mean = safe_float(decision.get("short_pair_time_zero_offset_abs_proxy_ns"), 0.0)
    corrected_max = safe_float(decision.get("short_pair_applied_corrected_max_abs_residual_ns"), 0.0)
    loo_max = safe_float(decision.get("short_pair_applied_leave_one_out_max_abs_residual_ns"), 0.0)
    reduction = safe_float(decision.get("short_pair_applied_residual_reduction_factor"), 0.0)
    axes[2].bar(
        np.arange(3),
        [raw_mean, corrected_max, loo_max],
        color=["#4c78a8", "#2f9d55", "#f58518"],
        width=0.58,
    )
    axes[2].set_xticks(np.arange(3), ["offset", "corrected\nmax", "LOO\nmax"])
    axes[2].set_ylabel("phase time [ns]")
    axes[2].set_title(f"Applied timing QC ({reduction:.1f}x residual drop)")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    stable_count = safe_float(decision.get("short_pair_stable_phase_convention_count"), 0.0)
    spread = safe_float(decision.get("short_pair_stable_phase_median_spread_ns"), 0.0)
    axes[3].bar([0, 1], [stable_count, spread * 100.0], color=["#2f9d55", "#f58518"], width=0.55)
    axes[3].set_xticks([0, 1], ["stable\nconventions", "median\nspread x100"])
    axes[3].set_title("Multi-phase timing QC")
    axes[3].grid(axis="y", color="#dddddd", linewidth=0.6)

    boot_median = safe_float(decision.get("short_pair_bootstrap_observed_median_offset_ns"), 0.0)
    boot_lower = safe_float(decision.get("short_pair_bootstrap_min_ci_lower_ns"), 0.0)
    boot_upper = safe_float(decision.get("short_pair_bootstrap_max_ci_upper_ns"), 0.0)
    axes[4].errorbar(
        [0],
        [boot_median],
        yerr=[[max(0.0, boot_median - boot_lower)], [max(0.0, boot_upper - boot_median)]],
        fmt="o",
        color="#2f6f9f",
        ecolor="#2f6f9f",
        capsize=5,
    )
    axes[4].set_xticks([0], ["bootstrap\ninterval"])
    axes[4].set_ylabel("phase time [ns]")
    axes[4].set_title("Timing uncertainty")
    axes[4].grid(axis="y", color="#dddddd", linewidth=0.6)

    content_count = safe_float(decision.get("short_pair_content_backed_event_pair_count"), 0.0)
    timing_only_count = safe_float(decision.get("short_pair_timing_only_event_pair_count"), 0.0)
    content_residual = safe_float(decision.get("short_pair_max_abs_content_timing_residual_ns"), 0.0)
    content_distance = safe_float(decision.get("short_pair_max_content_anchor_distance_mm"), 0.0)
    axes[5].bar(
        np.arange(4),
        [content_count, timing_only_count, content_residual * 100.0, content_distance / 10.0],
        color=["#2f9d55", "#c7302b", "#4c78a8", "#f58518"],
        width=0.58,
    )
    axes[5].set_xticks(
        np.arange(4),
        ["content\nevents", "timing\nonly", "content\nresid x100", "max dist\n/10"],
    )
    axes[5].set_title("Repeat content windows")
    axes[5].grid(axis="y", color="#dddddd", linewidth=0.6)

    synthetic_content = safe_float(
        decision.get("short_pair_content_backed_waveform_supported_count"), 0.0
    )
    synthetic_timing = safe_float(decision.get("short_pair_timing_only_waveform_supported_count"), 0.0)
    synthetic_content_corr = safe_float(
        decision.get("short_pair_min_content_pair_absolute_correlation"), 0.0
    )
    synthetic_timing_corr = safe_float(
        decision.get("short_pair_min_timing_only_pair_absolute_correlation"), 0.0
    )
    axes[6].bar(
        np.arange(4),
        [synthetic_content, synthetic_timing, synthetic_content_corr, synthetic_timing_corr],
        color=["#2f9d55", "#c7302b", "#4c78a8", "#f58518"],
        width=0.58,
    )
    axes[6].set_xticks(
        np.arange(4),
        ["content\nsupported", "timing\nsupported", "content\nmin corr", "timing\nmin corr"],
    )
    axes[6].set_ylim(0, max(2.2, synthetic_content + 0.2, synthetic_timing + 0.2))
    axes[6].set_title("Content-synthetic QC")
    axes[6].grid(axis="y", color="#dddddd", linewidth=0.6)

    anchor_supported = safe_float(decision.get("short_pair_supported_content_anchor_pair_count"), 0.0)
    anchor_resid = safe_float(decision.get("short_pair_anchor_max_abs_content_residual_ns"), 0.0)
    anchor_corr = safe_float(decision.get("short_pair_anchor_min_content_abs_correlation"), 0.0)
    anchor_rms = safe_float(decision.get("short_pair_anchor_max_content_panel_rms"), 0.0)
    axes[7].bar(
        np.arange(4),
        [anchor_supported, anchor_resid * 100.0, anchor_corr, anchor_rms],
        color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[7].set_xticks(
        np.arange(4),
        ["supported\nanchors", "max resid\nx100", "min\ncorr", "max\nRMS"],
    )
    axes[7].set_ylim(0, max(2.2, anchor_supported + 0.2))
    axes[7].set_title("Content time-zero anchors")
    axes[7].grid(axis="y", color="#dddddd", linewidth=0.6)

    trace_supported = safe_float(decision.get("short_pair_trace_alignment_supported_pair_count"), 0.0)
    trace_improved = safe_float(decision.get("short_pair_trace_alignment_improved_count"), 0.0)
    trace_raw = safe_float(decision.get("short_pair_trace_alignment_mean_raw_abs_correlation"), 0.0)
    trace_corrected = safe_float(decision.get("short_pair_trace_alignment_mean_corrected_abs_correlation"), 0.0)
    axes[8].bar(
        np.arange(4),
        [trace_supported, trace_improved, trace_raw, trace_corrected],
        color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[8].set_xticks(
        np.arange(4),
        ["supported\npairs", "improved\npairs", "raw\ncorr", "corrected\ncorr"],
    )
    axes[8].set_ylim(0, max(2.2, trace_supported + 0.2))
    axes[8].set_title("Measured trace alignment")
    axes[8].grid(axis="y", color="#dddddd", linewidth=0.6)

    sens_windows = safe_float(decision.get("short_pair_trace_sensitivity_window_count"), 0.0)
    sens_rows = safe_float(decision.get("short_pair_trace_sensitivity_pair_window_row_count"), 0.0)
    sens_improved = safe_float(decision.get("short_pair_trace_sensitivity_improved_pair_window_count"), 0.0)
    sens_min_corr = safe_float(decision.get("short_pair_trace_sensitivity_min_corrected_abs_correlation"), 0.0)
    axes[9].bar(
        np.arange(4),
        [sens_windows, sens_rows, sens_improved, sens_min_corr],
        color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[9].set_xticks(
        np.arange(4),
        ["windows", "pair\nwindows", "improved", "min corr"],
    )
    axes[9].set_ylim(0, max(6.2, sens_rows + 0.2))
    axes[9].set_title("Trace window sensitivity")
    axes[9].grid(axis="y", color="#dddddd", linewidth=0.6)

    stack_raw = safe_float(decision.get("short_pair_corrected_profile_stack_raw_matrix_abs_correlation"), 0.0)
    stack_corrected = safe_float(
        decision.get("short_pair_corrected_profile_stack_corrected_matrix_abs_correlation"), 0.0
    )
    stack_improvement = safe_float(decision.get("short_pair_corrected_profile_stack_matrix_improvement"), 0.0)
    stack_fraction = safe_float(decision.get("short_pair_corrected_profile_stack_improved_column_fraction"), 0.0)
    axes[10].bar(
        np.arange(4),
        [stack_raw, stack_corrected, stack_improvement, stack_fraction],
        color=["#c7302b", "#2f9d55", "#4c78a8", "#f58518"],
        width=0.58,
    )
    axes[10].set_xticks(
        np.arange(4),
        ["raw\ncorr", "corrected\ncorr", "matrix\nimprove", "column\nfraction"],
    )
    axes[10].set_ylim(0, max(1.05, stack_corrected + 0.1))
    axes[10].set_title("Corrected profile stack")
    axes[10].grid(axis="y", color="#dddddd", linewidth=0.6)

    stack_sens_windows = safe_float(decision.get("short_pair_corrected_profile_stack_sensitivity_window_count"), 0.0)
    stack_sens_robust = safe_float(
        decision.get("short_pair_corrected_profile_stack_sensitivity_robust_window_count"), 0.0
    )
    stack_sens_min_gain = safe_float(
        decision.get("short_pair_corrected_profile_stack_sensitivity_min_matrix_improvement"), 0.0
    )
    stack_sens_min_corr = safe_float(
        decision.get("short_pair_corrected_profile_stack_sensitivity_min_corrected_abs_correlation"), 0.0
    )
    axes[11].bar(
        np.arange(4),
        [stack_sens_windows, stack_sens_robust, stack_sens_min_gain, stack_sens_min_corr],
        color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[11].set_xticks(
        np.arange(4),
        ["windows", "robust", "min\nimprove", "min\ncorr"],
    )
    axes[11].set_ylim(0, max(3.2, stack_sens_windows + 0.2))
    axes[11].set_title("Stack window sensitivity")
    axes[11].grid(axis="y", color="#dddddd", linewidth=0.6)

    spatial_majority = safe_float(
        decision.get("short_pair_corrected_stack_spatial_support_majority_column_fraction"), 0.0
    )
    spatial_all = safe_float(
        decision.get("short_pair_corrected_stack_spatial_support_all_window_column_fraction"), 0.0
    )
    spatial_intervals = safe_float(decision.get("short_pair_corrected_stack_spatial_support_interval_count"), 0.0)
    spatial_largest = safe_float(
        decision.get("short_pair_corrected_stack_spatial_support_largest_interval_length_m"), 0.0
    )
    axes[12].bar(
        np.arange(4),
        [spatial_majority, spatial_all, spatial_intervals / 10.0, spatial_largest],
        color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[12].set_xticks(
        np.arange(4),
        ["majority\nfraction", "all-window\nfraction", "intervals\n/10", "largest\nm"],
    )
    axes[12].set_ylim(0, max(1.05, spatial_majority + 0.1, spatial_all + 0.1))
    axes[12].set_title("Stack spatial support")
    axes[12].grid(axis="y", color="#dddddd", linewidth=0.6)

    interval_count = safe_float(decision.get("short_pair_supported_interval_visual_qc_selected_count"), 0.0)
    interval_supported = safe_float(decision.get("short_pair_supported_interval_visual_qc_supported_count"), 0.0)
    interval_length = safe_float(decision.get("short_pair_supported_interval_visual_qc_total_length_m"), 0.0)
    interval_min_corr = safe_float(
        decision.get("short_pair_supported_interval_visual_qc_min_corrected_abs_correlation"), 0.0
    )
    axes[13].bar(
        np.arange(4),
        [interval_count, interval_supported, interval_length, interval_min_corr],
        color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[13].set_xticks(
        np.arange(4),
        ["selected", "supported", "length\nm", "min\ncorr"],
    )
    axes[13].set_ylim(0, max(3.2, interval_count + 0.2))
    axes[13].set_title("Supported interval QC")
    axes[13].grid(axis="y", color="#dddddd", linewidth=0.6)

    long_raw = safe_float(
        decision.get("long_pair_short_correction_transfer_raw_matrix_abs_correlation"), 0.0
    )
    long_corrected = safe_float(
        decision.get("long_pair_short_correction_transfer_corrected_matrix_abs_correlation"), 0.0
    )
    long_gain = safe_float(decision.get("long_pair_short_correction_transfer_matrix_improvement"), 0.0)
    long_anchor_count = safe_float(
        decision.get("long_pair_short_correction_transfer_anchor_window_count"), 0.0
    )
    long_improved_anchors = safe_float(
        decision.get("long_pair_short_correction_transfer_improved_anchor_count"), 0.0
    )
    axes[14].bar(
        np.arange(4),
        [long_raw, long_corrected, long_gain, long_improved_anchors / max(1.0, long_anchor_count)],
        color=["#4c78a8", "#c7302b", "#f58518", "#2f9d55"],
        width=0.58,
    )
    axes[14].set_xticks(
        np.arange(4),
        ["raw\ncorr", "corrected\ncorr", "gain", "improved\nanchors"],
    )
    axes[14].set_ylim(min(-0.1, long_gain - 0.05), max(1.05, long_raw + 0.1, long_corrected + 0.1))
    axes[14].set_title("Long transfer audit")
    axes[14].grid(axis="y", color="#dddddd", linewidth=0.6)

    shift_zero = safe_float(decision.get("long_pair_shift_scan_zero_offset_matrix_abs_correlation"), 0.0)
    shift_short = safe_float(
        decision.get("long_pair_shift_scan_short_pair_offset_matrix_abs_correlation"), 0.0
    )
    shift_best = safe_float(decision.get("long_pair_shift_scan_best_matrix_abs_correlation"), 0.0)
    shift_best_offset = safe_float(decision.get("long_pair_shift_scan_best_matrix_offset_ns"), 0.0)
    axes[15].bar(
        np.arange(4),
        [shift_zero, shift_short, shift_best, shift_best_offset],
        color=["#4c78a8", "#c7302b", "#2f9d55", "#f58518"],
        width=0.58,
    )
    axes[15].set_xticks(
        np.arange(4),
        ["zero\ncorr", "short\ncorr", "best\ncorr", "best\nns"],
    )
    axes[15].set_ylim(min(-0.1, shift_best_offset - 0.05), max(1.05, shift_best + 0.1))
    axes[15].set_title("Long shift scan")
    axes[15].grid(axis="y", color="#dddddd", linewidth=0.6)

    shift_sens_windows = safe_float(decision.get("long_pair_shift_sensitivity_window_count"), 0.0)
    shift_sens_reject = safe_float(
        decision.get("long_pair_shift_sensitivity_reject_short_window_count"), 0.0
    )
    shift_sens_spread = safe_float(decision.get("long_pair_shift_sensitivity_best_offset_spread_ns"), 0.0)
    shift_sens_gain = safe_float(decision.get("long_pair_shift_sensitivity_min_best_gain"), 0.0)
    axes[16].bar(
        np.arange(4),
        [shift_sens_windows, shift_sens_reject, shift_sens_spread, shift_sens_gain],
        color=["#4c78a8", "#2f9d55", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[16].set_xticks(
        np.arange(4),
        ["windows", "reject\nshort", "offset\nspread", "min\ngain"],
    )
    axes[16].set_ylim(0, max(3.2, shift_sens_windows + 0.2))
    axes[16].set_title("Long shift sensitivity")
    axes[16].grid(axis="y", color="#dddddd", linewidth=0.6)

    panel_count = safe_float(decision.get("short_pair_content_panel_valid_count"), 0.0)
    panel_pairs = safe_float(decision.get("short_pair_content_panel_pair_count"), 0.0)
    panel_min_corr = safe_float(decision.get("short_pair_content_panel_min_abs_correlation"), 0.0)
    panel_mean_corr = safe_float(decision.get("short_pair_content_panel_mean_abs_correlation"), 0.0)
    axes[17].bar(
        np.arange(4),
        [panel_count, panel_pairs, panel_min_corr, panel_mean_corr],
        color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"],
        width=0.58,
    )
    axes[17].set_xticks(
        np.arange(4),
        ["valid\npanels", "content\npairs", "min\ncorr", "mean\ncorr"],
    )
    axes[17].set_ylim(0, max(4.2, panel_count + 0.2))
    axes[17].set_title("Content visual QC")
    axes[17].grid(axis="y", color="#dddddd", linewidth=0.6)

    long_visual_supported = safe_float(
        decision.get("long_pair_pattern_visual_qc_supported_anchor_count"), 0.0
    )
    long_holdout_supported = (
        safe_float(decision.get("long_pair_pattern_holdout_stable_supported_count"), 0.0)
        + safe_float(decision.get("long_pair_pattern_holdout_repeat_limited_supported_count"), 0.0)
    )
    long_window_rows = safe_float(decision.get("long_pair_holdout_window_sensitivity_row_count"), 0.0)
    long_window_supported = safe_float(
        decision.get("long_pair_holdout_window_sensitivity_supported_rows"), 0.0
    )
    long_width_rows = safe_float(decision.get("long_pair_holdout_width_sensitivity_row_count"), 0.0)
    long_width_supported = safe_float(
        decision.get("long_pair_holdout_width_sensitivity_supported_rows"), 0.0
    )
    publication_ready = 1.0 if decision.get("publication_claim_bundle_ready") else 0.0
    timing_window_ready = (
        1.0 if decision.get("publication_timing_window_ready_for_manuscript_boundary") else 0.0
    )
    axes[18].bar(
        np.arange(6),
        [
            long_visual_supported,
            long_holdout_supported,
            long_window_supported / max(1.0, long_window_rows),
            long_width_supported / max(1.0, long_width_rows),
            publication_ready,
            timing_window_ready,
        ],
        color=["#4c78a8", "#2f9d55", "#f58518", "#b279a2", "#6b6b6b", "#8c564b"],
        width=0.58,
    )
    axes[18].set_xticks(
        np.arange(6),
        [
            "visual\nanchors",
            "holdout\nanchors",
            "window\nfraction",
            "width\nfraction",
            "bundle\nready",
            "timing\nfamily",
        ],
    )
    axes[18].set_ylim(0, max(8.2, long_visual_supported + 0.2, long_holdout_supported + 0.2))
    axes[18].set_title("Long publication endpoint")
    axes[18].grid(axis="y", color="#dddddd", linewidth=0.6)

    depth_max_resid = safe_float(
        decision.get("field_apparent_depth_qc_max_corrected_depth_residual_mm"), 0.0
    )
    depth_budget = safe_float(
        decision.get("field_apparent_depth_qc_time_zero_depth_equivalent_mm"), 0.0
    )
    depth_factor = safe_float(decision.get("field_apparent_depth_sensitivity_factor"), 0.0)
    degen_surfaces = safe_float(decision.get("field_hyperbola_timezero_surface_count"), 0.0)
    degen_boundary = safe_float(
        decision.get("field_hyperbola_timezero_boundary_best_surface_count"), 0.0
    )
    degen_fraction = degen_boundary / max(1.0, degen_surfaces)
    degen_epsr_span = safe_float(
        decision.get("field_hyperbola_timezero_max_near_top_epsr_span"), 0.0
    )
    axes[19].bar(
        np.arange(5),
        [depth_max_resid, depth_budget, depth_factor, degen_fraction, degen_epsr_span],
        color=["#2f9d55", "#4c78a8", "#f58518", "#c7302b", "#6b6b6b"],
        width=0.58,
    )
    axes[19].set_xticks(
        np.arange(5),
        ["max resid\nmm", "budget\nmm", "depth\nfactor", "boundary\nfraction", "epsr\nspan"],
    )
    axes[19].set_ylim(0, max(6.2, depth_budget + 0.5, degen_epsr_span + 0.5))
    axes[19].set_title("Depth/degen guardrails")
    axes[19].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(f"Field policy: {decision['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_dataset_policy_synthesis")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    survey = read_json(dataset_root / "015_gssi51600s_survey_geometry_audit" / "data" / "survey_geometry_audit_summary.json")
    network = read_json(dataset_root / "020_gssi51600s_profile_network_alignment" / "data" / "profile_network_alignment_summary.json")
    short = read_json(dataset_root / "021_gssi51600s_short_profile_stack_policy" / "data" / "short_profile_stack_policy_summary.json")
    long = read_json(dataset_root / "022_gssi51600s_long_profile_stack_policy" / "data" / "long_profile_stack_policy_summary.json")
    time_zero = read_optional_json(dataset_root / "024_gssi51600s_short_profile_time_zero_transfer_policy" / "data" / "short_profile_time_zero_transfer_summary.json")
    applied_time_zero = read_optional_json(dataset_root / "025_gssi51600s_short_profile_time_zero_application_policy" / "data" / "short_profile_time_zero_application_summary.json")
    phase_convention = read_optional_json(dataset_root / "027_gssi51600s_short_profile_phase_convention_transfer_policy" / "data" / "short_profile_phase_convention_transfer_summary.json")
    timing_bootstrap = read_optional_json(dataset_root / "029_gssi51600s_short_profile_timing_bootstrap_policy" / "data" / "short_profile_timing_bootstrap_policy_summary.json")
    content_windows = read_optional_json(dataset_root / "031_gssi51600s_short_profile_content_window_policy" / "data" / "short_profile_content_window_policy_summary.json")
    content_synthetic = read_optional_json(dataset_root / "033_gssi51600s_short_profile_content_synthetic_policy" / "data" / "short_profile_content_synthetic_policy_summary.json")
    content_time_zero_anchor = read_optional_json(dataset_root / "037_gssi51600s_content_time_zero_anchor_policy" / "data" / "short_profile_content_time_zero_anchor_summary.json")
    content_trace_alignment = read_optional_json(dataset_root / "039_gssi51600s_content_anchor_trace_alignment" / "data" / "content_anchor_trace_alignment_summary.json")
    content_trace_sensitivity = read_optional_json(dataset_root / "041_gssi51600s_content_anchor_trace_alignment_sensitivity" / "data" / "content_anchor_trace_alignment_sensitivity_summary.json")
    content_panels = read_optional_json(dataset_root / "035_gssi51600s_content_backed_waveform_panels" / "data" / "content_backed_waveform_panel_summary.json")
    corrected_profile_stack = read_optional_json(dataset_root / "043_gssi51600s_corrected_profile_stack" / "data" / "corrected_profile_stack_summary.json")
    corrected_profile_stack_sensitivity = read_optional_json(dataset_root / "045_gssi51600s_corrected_profile_stack_sensitivity" / "data" / "corrected_profile_stack_sensitivity_summary.json")
    corrected_stack_spatial_support = read_optional_json(dataset_root / "047_gssi51600s_corrected_stack_spatial_support" / "data" / "corrected_stack_spatial_support_summary.json")
    supported_interval_visual_qc = read_optional_json(dataset_root / "049_gssi51600s_supported_interval_visual_qc" / "data" / "supported_interval_visual_qc_summary.json")
    long_profile_transfer_audit = read_optional_json(dataset_root / "051_gssi51600s_long_profile_transfer_audit" / "data" / "long_profile_transfer_audit_summary.json")
    long_profile_shift_scan = read_optional_json(dataset_root / "053_gssi51600s_long_profile_shift_scan" / "data" / "long_profile_shift_scan_summary.json")
    long_profile_shift_sensitivity = read_optional_json(dataset_root / "055_gssi51600s_long_profile_shift_scan_sensitivity" / "data" / "long_profile_shift_scan_sensitivity_summary.json")
    long_profile_pattern_visual_qc = read_optional_json(dataset_root / "057_gssi51600s_long_profile_pattern_visual_qc" / "data" / "long_profile_pattern_visual_qc_summary.json")
    long_profile_pattern_holdout_qc = read_optional_json(dataset_root / "058_gssi51600s_long_profile_pattern_holdout_qc" / "data" / "long_profile_pattern_holdout_qc_summary.json")
    long_profile_holdout_sensitivity = read_optional_json(dataset_root / "060_gssi51600s_long_profile_pattern_holdout_sensitivity" / "data" / "long_profile_pattern_holdout_sensitivity_summary.json")
    long_profile_holdout_width_sensitivity = read_optional_json(dataset_root / "061_gssi51600s_long_profile_pattern_holdout_width_sensitivity" / "data" / "long_profile_pattern_holdout_width_sensitivity_summary.json")
    publication_claim_bundle = read_publication_claim_bundle(dataset_root)
    long_profile_relaxed_phase_anchor = read_optional_json(dataset_root / "064_gssi51600s_long_profiles_relaxed_phase_anchor_audit" / "data" / "field_phase_anchor_summary.json")
    bandlimited_repeatability = read_optional_json(dataset_root / "068_gssi51600s_field_bandlimited_repeatability_audit" / "data" / "field_bandlimited_repeatability_summary.json")
    apparent_depth_qc = read_optional_json(dataset_root / "084_gssi51600s_field_apparent_depth_qc" / "data" / "field_apparent_depth_qc_summary.json")
    apparent_depth_sensitivity = read_optional_json(dataset_root / "085_gssi51600s_field_apparent_depth_sensitivity" / "data" / "field_apparent_depth_sensitivity_summary.json")
    hyperbola_timezero_degeneracy = read_optional_json(dataset_root / "086_gssi51600s_field_hyperbola_timezero_degeneracy_audit" / "data" / "field_hyperbola_timezero_degeneracy_summary.json")

    decision = field_policy_decision(
        survey,
        network,
        short,
        long,
        time_zero,
        applied_time_zero,
        phase_convention,
        timing_bootstrap,
        content_windows,
        content_synthetic,
        content_time_zero_anchor,
        content_trace_alignment,
        content_trace_sensitivity,
        content_panels,
        corrected_profile_stack,
        corrected_profile_stack_sensitivity,
        corrected_stack_spatial_support,
        supported_interval_visual_qc,
        long_profile_transfer_audit,
        long_profile_shift_scan,
        long_profile_shift_sensitivity,
        long_profile_pattern_visual_qc,
        long_profile_pattern_holdout_qc,
        long_profile_holdout_sensitivity,
        long_profile_holdout_width_sensitivity,
        publication_claim_bundle,
        long_profile_relaxed_phase_anchor,
        bandlimited_repeatability,
        apparent_depth_qc,
        apparent_depth_sensitivity,
        hyperbola_timezero_degeneracy,
    )
    if applied_time_zero:
        applied_summary = applied_time_zero.get("summary", {})
        decision["short_pair_time_zero_offset_abs_proxy_ns"] = abs(
            safe_float(applied_summary.get("raw_mean_abs_phase_residual_ns"))
        )
    rows = evidence_rows(
        survey,
        network,
        short,
        long,
        time_zero,
        applied_time_zero,
        phase_convention,
        timing_bootstrap,
        content_windows,
        content_synthetic,
        content_time_zero_anchor,
        content_trace_alignment,
        content_trace_sensitivity,
        content_panels,
        corrected_profile_stack,
        corrected_profile_stack_sensitivity,
        corrected_stack_spatial_support,
        supported_interval_visual_qc,
        long_profile_transfer_audit,
        long_profile_shift_scan,
        long_profile_shift_sensitivity,
        long_profile_pattern_visual_qc,
        long_profile_pattern_holdout_qc,
        long_profile_holdout_sensitivity,
        long_profile_holdout_width_sensitivity,
        publication_claim_bundle,
        long_profile_relaxed_phase_anchor,
        bandlimited_repeatability,
        apparent_depth_qc,
        apparent_depth_sensitivity,
        hyperbola_timezero_degeneracy,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    evidence_csv = data_dir / "field_dataset_policy_evidence.csv"
    summary_json = data_dir / "field_dataset_policy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_field_policy(rows, decision, figures_dir / "field_dataset_policy.png"))

    write_csv(evidence_csv, [json_safe(row) for row in rows])
    validation_rows = [figure_stats(figure_path)]
    write_csv(validation_csv, [json_safe(row) for row in validation_rows])
    output_summary = {
        **decision,
        "paths": {
            "evidence_csv": str(evidence_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_dataset_policy_synthesis",
        {
            "summary_json": str(summary_json),
            "evidence_csv": str(evidence_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
