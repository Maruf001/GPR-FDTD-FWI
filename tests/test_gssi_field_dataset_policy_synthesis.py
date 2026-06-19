import json

from run_gssi_field_dataset_policy_synthesis import (
    evidence_rows,
    field_policy_decision,
    read_publication_claim_bundle,
)


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_read_publication_claim_bundle_prefers_timing_discriminant_hpc_refresh(tmp_path):
    _write_json(
        tmp_path
        / "062_gssi51600s_field_publication_claim_bundle/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "old_bundle", "figure_row_count": 7},
    )
    _write_json(
        tmp_path
        / "066_gssi51600s_field_publication_claim_bundle_post_relaxed_anchor/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "new_bundle", "figure_row_count": 8},
    )
    _write_json(
        tmp_path
        / "070_gssi51600s_field_publication_claim_bundle_post_bandlimited_audit/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "band_bundle", "figure_row_count": 9},
    )
    _write_json(
        tmp_path
        / "073_gssi51600s_field_publication_claim_bundle_post_event_support_tiers/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "event_tier_bundle", "figure_row_count": 10},
    )
    _write_json(
        tmp_path
        / "076_gssi51600s_field_publication_claim_bundle_post_time_zero_budget/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "time_zero_bundle", "figure_row_count": 11},
    )
    _write_json(
        tmp_path
        / "079_gssi51600s_field_publication_claim_bundle_post_time_zero_perturbation/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "perturbation_bundle", "figure_row_count": 12},
    )
    _write_json(
        tmp_path
        / "082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "acquisition_bundle", "figure_row_count": 13},
    )
    _write_json(
        tmp_path
        / "088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "depth_degen_bundle", "figure_row_count": 16},
    )
    _write_json(
        tmp_path
        / "091_gssi51600s_field_publication_claim_bundle_post_early_time_anchor_qc/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "early_time_bundle", "figure_row_count": 17},
    )
    _write_json(
        tmp_path
        / "095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "cue_spacing_bundle", "figure_row_count": 18},
    )
    _write_json(
        tmp_path
        / "098_gssi51600s_field_publication_claim_bundle_post_timing_anchor_conflict/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "timing_anchor_bundle", "figure_row_count": 19},
    )
    _write_json(
        tmp_path
        / "102_gssi51600s_field_publication_claim_bundle_post_timing_window_family/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "timing_window_bundle", "figure_row_count": 20},
    )
    _write_json(
        tmp_path
        / "107_gssi51600s_field_publication_claim_bundle_post_timing_discriminant_hpc/data/"
        "field_publication_claim_bundle_summary.json",
        {"policy_label": "timing_discriminant_hpc_bundle", "figure_row_count": 22},
    )

    summary = read_publication_claim_bundle(tmp_path)

    assert summary["policy_label"] == "timing_discriminant_hpc_bundle"
    assert summary["figure_row_count"] == 22


def _summaries():
    survey = {
        "classification": "independent_2d_line_profiles",
        "reasons": ["no DZG/GPS/grid position file is present"],
    }
    network = {
        "decision": "network decision",
        "pair_label_counts": {"repeat_candidate": 2, "embedded_segment_candidate": 0},
        "strongest_pair": {"best_normalized_correlation": 0.93},
    }
    short = {
        "summary": {
            "policy_label": "repeat_stack_limited_qc",
            "best_normalized_correlation": 0.93,
            "stable_stack_anchor_count": 2,
            "event_pair_count": 3,
            "radius_match_fraction": 0.0,
        }
    }
    long = {
        "summary": {
            "policy_label": "long_repeat_stack_pattern_only_qc",
            "best_normalized_correlation": 0.72,
            "stable_stack_anchor_count": 6,
            "comparison_profile_missing_phase_anchor_picks": True,
        }
    }
    time_zero = {
        "summary": {
            "policy_label": "relative_time_zero_transfer_limited_qc",
            "event_pair_count": 3,
            "stable_stack_anchor_count": 2,
            "median_comparison_minus_reference_phase_time_ns": 0.1277,
        }
    }
    applied_time_zero = {
        "summary": {
            "policy_label": "applied_relative_time_zero_transfer_qc",
            "event_pair_count": 3,
            "mean_abs_residual_reduction_factor": 6.0,
            "corrected_max_abs_phase_residual_ns": 0.049,
            "leave_one_out_max_abs_residual_ns": 0.059,
        }
    }
    phase_convention = {
        "summary": {
            "policy_label": "multi_phase_relative_time_zero_supported_qc",
            "phase_convention_count": 6,
            "stable_phase_convention_count": 4,
            "stable_phase_conventions": (
                "top_envelope_35pct, signed_positive_peak, "
                "signed_negative_peak, nearest_zero_crossing"
            ),
            "stable_median_delta_spread_ns": 0.019646,
        }
    }
    timing_bootstrap = {
        "summary": {
            "policy_label": "bootstrap_relative_time_zero_supported_qc",
            "stable_phase_convention_count": 4,
            "observed_median_offset_ns": 0.117878,
            "min_bootstrap_ci_lower_ns": 0.108055,
            "max_bootstrap_ci_upper_ns": 0.147348,
            "max_bootstrap_ci_width_ns": 0.039293,
        }
    }
    content_windows = {
        "summary": {
            "policy_label": "repeat_content_windows_limited_qc",
            "stable_content_window_count": 2,
            "event_pair_count": 3,
            "content_backed_event_pair_count": 2,
            "timing_only_event_pair_count": 1,
            "content_backed_event_fraction": 2 / 3,
            "max_content_anchor_distance_mm": 9.999,
            "max_abs_content_timing_residual_to_bootstrap_median_ns": 0.009823,
        }
    }
    content_synthetic = {
        "summary": {
            "policy_label": "content_backed_field_to_synthetic_qc_supported",
            "event_pair_count": 3,
            "content_backed_event_pair_count": 2,
            "content_backed_waveform_supported_count": 2,
            "timing_only_event_pair_count": 1,
            "timing_only_waveform_supported_count": 1,
            "min_abs_correlation_threshold": 0.8,
            "min_content_pair_absolute_correlation": 0.819494,
            "min_timing_only_pair_absolute_correlation": 0.810335,
        }
    }
    content_time_zero_anchor = {
        "policy_label": "short_profile_content_time_zero_anchor_supported_for_visual_qc",
        "event_pair_count": 3,
        "content_backed_event_pair_count": 2,
        "supported_content_anchor_pair_count": 2,
        "timing_only_event_pair_count": 1,
        "max_abs_content_timing_residual_ns": 0.009823,
        "max_abs_all_timing_residual_ns": 0.058939,
        "min_content_pair_absolute_correlation": 0.819494,
        "max_content_panel_normalized_residual_rms": 0.629150,
    }
    content_trace_alignment = {
        "policy_label": "content_anchor_field_trace_alignment_improves_after_time_zero",
        "supported_anchor_pair_count": 2,
        "field_trace_alignment_improved_count": 2,
        "mean_raw_abs_correlation": 0.301334,
        "mean_corrected_abs_correlation": 0.963803,
        "mean_abs_correlation_improvement": 0.662470,
    }
    content_trace_sensitivity = {
        "policy_label": "content_anchor_trace_alignment_window_robust",
        "window_count": 3,
        "pair_window_row_count": 6,
        "improved_pair_window_count": 6,
        "min_abs_correlation_improvement": 0.362904,
        "min_corrected_abs_correlation": 0.920890,
    }
    content_panels = {
        "policy_label": "content_backed_waveform_visual_qc",
        "panel_count": 4,
        "valid_panel_count": 4,
        "content_backed_pair_count": 2,
        "min_absolute_correlation": 0.819494,
        "mean_absolute_correlation": 0.856643,
    }
    corrected_profile_stack = {
        "summary": {
            "policy_label": "corrected_profile_stack_time_zero_supported",
            "raw_matrix_abs_correlation": 0.535682,
            "corrected_matrix_abs_correlation": 0.812268,
            "matrix_abs_correlation_improvement": 0.276586,
            "improved_column_count": 161,
            "finite_column_count": 249,
            "improved_column_fraction": 0.646586,
            "mean_column_abs_correlation_improvement": 0.144253,
        }
    }
    corrected_profile_stack_sensitivity = {
        "policy_label": "corrected_profile_stack_window_robust",
        "window_count": 3,
        "robust_window_count": 3,
        "min_matrix_abs_correlation_improvement": 0.263036,
        "min_corrected_matrix_abs_correlation": 0.7992,
        "min_improved_column_fraction": 0.606426,
    }
    corrected_stack_spatial_support = {
        "policy_label": "corrected_stack_spatial_support_sparse",
        "finite_column_count": 249,
        "majority_supported_column_count": 105,
        "majority_supported_column_fraction": 0.421687,
        "all_window_supported_column_count": 70,
        "all_window_supported_column_fraction": 0.281124,
        "support_interval_count": 15,
        "largest_majority_interval_length_m": 0.069993,
    }
    supported_interval_visual_qc = {
        "policy_label": "supported_interval_visual_qc_ready",
        "selected_interval_count": 3,
        "supported_interval_count": 3,
        "total_selected_interval_length_m": 0.16665,
        "min_interval_abs_correlation_improvement": 0.363612,
        "min_corrected_interval_abs_correlation": 0.909285,
    }
    long_profile_transfer_audit = {
        "summary": {
            "policy_label": "long_profile_short_correction_transfer_not_supported",
            "raw_matrix_abs_correlation": 0.763452,
            "corrected_matrix_abs_correlation": 0.732421,
            "matrix_abs_correlation_improvement": -0.031031,
            "stable_anchor_window_count": 6,
            "improved_anchor_window_count": 0,
            "min_corrected_anchor_abs_correlation": 0.539009,
        }
    }
    long_profile_shift_scan = {
        "summary": {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "scanned_offset_count": 51,
            "zero_offset_matrix_abs_correlation": 0.763452,
            "short_pair_offset_matrix_abs_correlation": 0.719581,
            "short_pair_offset_gain_vs_zero": -0.043871,
            "best_matrix_offset_ns": 0.06,
            "best_matrix_abs_correlation": 0.938531,
            "best_matrix_gain_vs_zero": 0.175079,
            "best_anchor_improved_window_count": 6,
            "best_anchor_min_corrected_abs_correlation": 0.909065,
        }
    }
    long_profile_shift_sensitivity = {
        "policy_label": "long_profile_pattern_shift_window_robust_rejects_short_transfer",
        "window_count": 3,
        "reject_short_transfer_window_count": 3,
        "best_offset_median_ns": 0.06,
        "best_offset_spread_ns": 0.0,
        "min_best_matrix_gain_vs_zero": 0.150305,
        "max_short_pair_offset_gain_vs_zero": -0.034047,
        "min_best_anchor_improved_window_count": 6,
    }
    long_profile_pattern_visual_qc = {
        "policy_label": "long_profile_pattern_visual_qc_ready",
        "selected_anchor_window_count": 6,
        "supported_anchor_window_count": 6,
        "min_pattern_shift_gain": 0.019532,
        "min_pattern_shift_abs_correlation": 0.889509,
    }
    long_profile_pattern_holdout_qc = {
        "policy_label": "long_profile_pattern_holdout_qc_all_candidate_anchors_supported",
        "candidate_anchor_count": 8,
        "stable_anchor_count": 6,
        "stable_supported_anchor_count": 6,
        "repeat_limited_anchor_count": 2,
        "repeat_limited_supported_anchor_count": 2,
        "min_repeat_limited_pattern_shift_gain": 0.172819,
        "min_repeat_limited_pattern_shift_abs_correlation": 0.961006,
    }
    long_profile_holdout_sensitivity = {
        "policy_label": "long_profile_pattern_holdout_sensitivity_all_candidate_anchors_all_windows_supported",
        "window_count": 3,
        "row_count": 24,
        "supported_row_count": 24,
        "all_window_supported_anchor_count": 8,
        "min_pattern_shift_gain": 0.001818,
        "min_pattern_shift_abs_correlation": 0.873226,
    }
    long_profile_holdout_width_sensitivity = {
        "policy_label": "long_profile_pattern_holdout_width_sensitivity_all_candidate_anchors_all_widths_supported",
        "width_count": 3,
        "row_count": 24,
        "supported_row_count": 24,
        "all_width_supported_anchor_count": 8,
        "min_pattern_shift_gain": 0.019532,
        "min_pattern_shift_abs_correlation": 0.888491,
    }
    publication_claim_bundle = {
        "policy_label": (
            "field_publication_claim_bundle_2d_qc_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_"
            "time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
        ),
        "figure_row_count": 20,
        "claim_boundary_count": 19,
        "ready_for_manuscript_field_supplement": True,
        "gpu_priority": "none",
        "time_zero_uncertainty_included": True,
        "time_zero_uncertainty_policy": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "time_zero_conservative_half_width_ns": 0.058939,
        "time_zero_absolute_ready": False,
        "time_zero_perturbation_included": True,
        "time_zero_perturbation_policy": "field_time_zero_ci_perturbation_stack_robust",
        "time_zero_perturbation_bootstrap_supported_count": 9,
        "time_zero_perturbation_bootstrap_row_count": 9,
        "time_zero_perturbation_conservative_supported_count": 6,
        "time_zero_perturbation_conservative_row_count": 6,
        "time_zero_perturbation_min_matrix_improvement": 0.125152,
        "early_time_anchor_included": True,
        "early_time_anchor_policy": "field_early_time_common_mode_not_content_time_zero",
        "early_time_short_pair_shift_ns": 0.0,
        "early_time_short_vs_content_delta_ns": 0.127701,
        "early_time_short_agrees_with_content_budget": False,
        "early_time_absolute_ready": False,
        "cue_spacing_sensitivity_included": True,
        "cue_spacing_sensitivity_policy": (
            "field_cue_spacing_context_threshold_robust_not_resolution_benchmark"
        ),
        "cue_spacing_threshold_count": 7,
        "cue_spacing_min_same_time_spacing_mm": 96.657,
        "cue_spacing_max_same_time_pair_count": 32,
        "cue_spacing_ready_for_field_context": True,
        "cue_spacing_resolution_benchmark_ready": False,
        "cue_spacing_field_fwi_ready": False,
        "timing_anchor_conflict_included": True,
        "timing_anchor_conflict_policy": "field_timing_anchor_conflict_short_relative_not_absolute",
        "timing_anchor_early_vs_short_delta_half_widths": 2.166667,
        "timing_anchor_long_vs_short_delta_half_widths": 1.148667,
        "timing_anchor_absolute_time_zero_ready": False,
        "timing_anchor_field_fwi_ready": False,
        "timing_anchor_ready_for_manuscript_boundary": True,
        "timing_window_family_included": True,
        "timing_window_family_policy": "field_timing_window_family_classification_ready_not_absolute",
        "timing_window_early_strict_near_zero_lag_count": 6,
        "timing_window_early_strict_row_count": 6,
        "timing_window_short_nonraw_supported_count": 18,
        "timing_window_short_nonraw_row_count": 18,
        "timing_window_long_reject_short_transfer_count": 3,
        "timing_window_long_row_count": 3,
        "timing_window_absolute_time_zero_ready": False,
        "timing_window_field_fwi_ready": False,
        "timing_window_ready_for_manuscript_boundary": True,
    }
    long_profile_relaxed_phase_anchor = {
        "profile_count": 2,
        "phase_anchor_pick_count": 10,
        "phase_quality_flag_counts": {"low_snr": 10},
        "low_snr_phase_anchor_pick_count": 10,
        "best_phase_hypothesis": {
            "phase_convention": "cue_time",
            "mean_profile_score": 1.847077,
            "median_depth_m": 0.102499,
            "boundary_solution_count": 1,
            "plausible_depth_15_to_120mm": True,
        },
    }
    bandlimited_repeatability = {
        "policy_label": "field_bandlimited_repeatability_short_pair_supported_long_pattern_only",
        "short_supported_band_count": 4,
        "short_supported_bands": "low,mid_low,mid_high,broad",
        "long_pattern_supported_band_count": 4,
        "long_pattern_supported_bands": "mid_low,mid_high,high,broad",
        "short_unfiltered_corrected_abs_correlation": 0.771287,
        "short_unfiltered_abs_correlation_gain": 0.225736,
        "long_unfiltered_pattern_abs_correlation": 0.905584,
        "long_unfiltered_pattern_gain": 0.116082,
        "field_gpu_fwi_priority": "none",
    }
    apparent_depth_qc = {
        "policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth",
        "cue_count": 19,
        "short_pair_corrected_depth_support_count": 3,
        "short_pair_corrected_depth_support_fraction": 1.0,
        "mean_corrected_depth_residual_mm": 2.29049,
        "max_corrected_depth_residual_mm": 4.908193,
        "time_zero_depth_equivalent_mm": 5.889832,
        "ready_for_apparent_depth_scale_qc": True,
        "ready_for_cover_depth_recovery": False,
        "ready_for_field_fwi": False,
        "gpu_priority": "none",
    }
    apparent_depth_sensitivity = {
        "policy_label": "field_apparent_depth_sensitivity_not_calibrated_cover_depth",
        "scenario_count": 5,
        "all_residuals_within_budget_scenario_count": 5,
        "all_residuals_within_budget_all_scenarios": True,
        "max_apparent_depth_span_mm": 149.915924,
        "max_apparent_depth_sensitivity_factor": 2.181313,
        "cover_depth_claim_ready": False,
        "field_fwi_ready": False,
        "gpu_priority": "none",
    }
    hyperbola_timezero_degeneracy = {
        "policy_label": "field_hyperbola_timezero_degeneracy_not_calibrated_inversion",
        "surface_summary_row_count": 4,
        "boundary_best_surface_count": 3,
        "max_near_top_epsr_span": 4.084544,
        "max_near_top_time_zero_span_ns": 0.3,
        "max_near_top_offset_count_5pct": 5,
        "cover_depth_claim_ready": False,
        "radius_claim_ready": False,
        "field_fwi_ready": False,
        "gpu_priority": "none",
    }
    return (
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


def test_field_policy_decision_keeps_dataset_out_of_3d_fwi_bucket():
    decision = field_policy_decision(*_summaries())

    assert decision["policy_label"] == "field_2d_qc_not_3d_or_fwi"
    assert decision["embedded_segment_candidate_count"] == 0
    assert decision["long_pair_missing_phase_anchor_picks"] is True
    assert "not a 3D survey" in decision["decision"]
    assert decision["short_pair_applied_time_zero_policy_label"] == "applied_relative_time_zero_transfer_qc"
    assert decision["short_pair_applied_residual_reduction_factor"] == 6.0
    assert decision["short_pair_phase_convention_policy_label"] == "multi_phase_relative_time_zero_supported_qc"
    assert decision["short_pair_stable_phase_convention_count"] == 4.0
    assert decision["short_pair_timing_bootstrap_policy_label"] == "bootstrap_relative_time_zero_supported_qc"
    assert decision["short_pair_bootstrap_max_ci_width_ns"] == 0.039293
    assert decision["short_pair_content_window_policy_label"] == "repeat_content_windows_limited_qc"
    assert decision["short_pair_content_backed_event_pair_count"] == 2.0
    assert decision["short_pair_timing_only_event_pair_count"] == 1.0
    assert (
        decision["short_pair_content_synthetic_policy_label"]
        == "content_backed_field_to_synthetic_qc_supported"
    )
    assert decision["short_pair_content_backed_waveform_supported_count"] == 2.0
    assert decision["short_pair_min_content_pair_absolute_correlation"] == 0.819494
    assert "Content-backed field-to-synthetic waveform QC supports" in decision["decision"]
    assert decision["short_pair_content_panel_policy_label"] == "content_backed_waveform_visual_qc"
    assert decision["short_pair_content_panel_valid_count"] == 4.0
    assert decision["short_pair_content_panel_pair_count"] == 2.0
    assert decision["short_pair_content_panel_min_abs_correlation"] == 0.819494
    assert (
        decision["short_pair_content_time_zero_anchor_policy_label"]
        == "short_profile_content_time_zero_anchor_supported_for_visual_qc"
    )
    assert decision["short_pair_supported_content_anchor_pair_count"] == 2.0
    assert decision["short_pair_anchor_max_abs_content_residual_ns"] == 0.009823
    assert decision["short_pair_anchor_max_abs_all_residual_ns"] == 0.058939
    assert decision["short_pair_anchor_min_content_abs_correlation"] == 0.819494
    assert "time-zero and visual-QC anchors only" in decision["decision"]
    assert (
        decision["short_pair_trace_alignment_policy_label"]
        == "content_anchor_field_trace_alignment_improves_after_time_zero"
    )
    assert decision["short_pair_trace_alignment_improved_count"] == 2.0
    assert decision["short_pair_trace_alignment_mean_raw_abs_correlation"] == 0.301334
    assert decision["short_pair_trace_alignment_mean_corrected_abs_correlation"] == 0.963803
    assert "improving measured 014/016 trace agreement" in decision["decision"]
    assert (
        decision["short_pair_trace_sensitivity_policy_label"]
        == "content_anchor_trace_alignment_window_robust"
    )
    assert decision["short_pair_trace_sensitivity_window_count"] == 3.0
    assert decision["short_pair_trace_sensitivity_improved_pair_window_count"] == 6.0
    assert decision["short_pair_trace_sensitivity_min_corrected_abs_correlation"] == 0.92089
    assert "survives the tested short, nominal, and wider windows" in decision["decision"]
    assert (
        decision["short_pair_corrected_profile_stack_policy_label"]
        == "corrected_profile_stack_time_zero_supported"
    )
    assert decision["short_pair_corrected_profile_stack_raw_matrix_abs_correlation"] == 0.535682
    assert decision["short_pair_corrected_profile_stack_corrected_matrix_abs_correlation"] == 0.812268
    assert decision["short_pair_corrected_profile_stack_improved_column_count"] == 161.0
    assert decision["short_pair_corrected_profile_stack_finite_column_count"] == 249.0
    assert "profile-level agreement" in decision["decision"]
    assert (
        decision["short_pair_corrected_profile_stack_sensitivity_policy_label"]
        == "corrected_profile_stack_window_robust"
    )
    assert decision["short_pair_corrected_profile_stack_sensitivity_window_count"] == 3.0
    assert decision["short_pair_corrected_profile_stack_sensitivity_robust_window_count"] == 3.0
    assert decision["short_pair_corrected_profile_stack_sensitivity_min_matrix_improvement"] == 0.263036
    assert "B-scan-level improvement survives" in decision["decision"]
    assert (
        decision["short_pair_corrected_stack_spatial_support_policy_label"]
        == "corrected_stack_spatial_support_sparse"
    )
    assert decision["short_pair_corrected_stack_spatial_support_majority_column_count"] == 105.0
    assert decision["short_pair_corrected_stack_spatial_support_majority_column_fraction"] == 0.421687
    assert decision["short_pair_corrected_stack_spatial_support_largest_interval_length_m"] == 0.069993
    assert "usable visual-QC regions are limited" in decision["decision"]
    assert (
        decision["short_pair_supported_interval_visual_qc_policy_label"]
        == "supported_interval_visual_qc_ready"
    )
    assert decision["short_pair_supported_interval_visual_qc_selected_count"] == 3.0
    assert decision["short_pair_supported_interval_visual_qc_supported_count"] == 3.0
    assert decision["short_pair_supported_interval_visual_qc_min_corrected_abs_correlation"] == 0.909285
    assert "preferred corrected-stack figure endpoint" in decision["decision"]
    assert (
        decision["long_pair_short_correction_transfer_policy_label"]
        == "long_profile_short_correction_transfer_not_supported"
    )
    assert decision["long_pair_short_correction_transfer_raw_matrix_abs_correlation"] == 0.763452
    assert decision["long_pair_short_correction_transfer_corrected_matrix_abs_correlation"] == 0.732421
    assert decision["long_pair_short_correction_transfer_matrix_improvement"] == -0.031031
    assert decision["long_pair_short_correction_transfer_anchor_window_count"] == 6.0
    assert decision["long_pair_short_correction_transfer_improved_anchor_count"] == 0.0
    assert "not be generalized to the long pair" in decision["decision"]
    assert decision["long_pair_shift_scan_policy_label"] == "long_profile_shift_scan_rejects_short_transfer"
    assert decision["long_pair_shift_scan_zero_offset_matrix_abs_correlation"] == 0.763452
    assert decision["long_pair_shift_scan_short_pair_offset_matrix_abs_correlation"] == 0.719581
    assert decision["long_pair_shift_scan_short_pair_offset_gain_vs_zero"] == -0.043871
    assert decision["long_pair_shift_scan_best_matrix_offset_ns"] == 0.06
    assert decision["long_pair_shift_scan_best_matrix_abs_correlation"] == 0.938531
    assert decision["long_pair_shift_scan_best_anchor_improved_window_count"] == 6.0
    assert "stronger pattern-only offset" in decision["decision"]
    assert (
        decision["long_pair_shift_sensitivity_policy_label"]
        == "long_profile_pattern_shift_window_robust_rejects_short_transfer"
    )
    assert decision["long_pair_shift_sensitivity_window_count"] == 3.0
    assert decision["long_pair_shift_sensitivity_reject_short_window_count"] == 3.0
    assert decision["long_pair_shift_sensitivity_best_offset_median_ns"] == 0.06
    assert decision["long_pair_shift_sensitivity_best_offset_spread_ns"] == 0.0
    assert decision["long_pair_shift_sensitivity_min_best_gain"] == 0.150305
    assert decision["long_pair_shift_sensitivity_max_short_gain"] == -0.034047
    assert "stable across the tested shallow windows" in decision["decision"]
    assert "preferred measured-data visual-QC figure endpoint" in decision["decision"]
    assert decision["long_pair_pattern_visual_qc_policy_label"] == "long_profile_pattern_visual_qc_ready"
    assert decision["long_pair_pattern_visual_qc_supported_anchor_count"] == 6.0
    assert decision["long_pair_pattern_visual_qc_min_abs_correlation"] == 0.889509
    assert (
        decision["long_pair_pattern_holdout_qc_policy_label"]
        == "long_profile_pattern_holdout_qc_all_candidate_anchors_supported"
    )
    assert decision["long_pair_pattern_holdout_candidate_anchor_count"] == 8.0
    assert decision["long_pair_pattern_holdout_repeat_limited_supported_count"] == 2.0
    assert (
        decision["long_pair_holdout_window_sensitivity_policy_label"]
        == "long_profile_pattern_holdout_sensitivity_all_candidate_anchors_all_windows_supported"
    )
    assert decision["long_pair_holdout_window_sensitivity_supported_rows"] == 24.0
    assert decision["long_pair_holdout_window_sensitivity_min_abs_correlation"] == 0.873226
    assert (
        decision["long_pair_holdout_width_sensitivity_policy_label"]
        == "long_profile_pattern_holdout_width_sensitivity_all_candidate_anchors_all_widths_supported"
    )
    assert decision["long_pair_holdout_width_sensitivity_supported_rows"] == 24.0
    assert decision["long_pair_holdout_width_sensitivity_min_abs_correlation"] == 0.888491
    assert (
        decision["publication_claim_bundle_policy_label"]
        == (
            "field_publication_claim_bundle_2d_qc_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_"
            "time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
        )
    )
    assert decision["publication_claim_bundle_figure_row_count"] == 20.0
    assert decision["publication_claim_bundle_claim_boundary_count"] == 19.0
    assert decision["publication_claim_bundle_ready"] is True
    assert decision["publication_time_zero_uncertainty_included"] is True
    assert (
        decision["publication_time_zero_uncertainty_policy_label"]
        == "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute"
    )
    assert decision["publication_time_zero_conservative_half_width_ns"] == 0.058939
    assert decision["publication_time_zero_absolute_ready"] is False
    assert decision["publication_time_zero_perturbation_included"] is True
    assert (
        decision["publication_time_zero_perturbation_policy_label"]
        == "field_time_zero_ci_perturbation_stack_robust"
    )
    assert decision["publication_time_zero_perturbation_bootstrap_supported_count"] == 9.0
    assert decision["publication_time_zero_perturbation_bootstrap_row_count"] == 9.0
    assert decision["publication_time_zero_perturbation_conservative_supported_count"] == 6.0
    assert decision["publication_time_zero_perturbation_conservative_row_count"] == 6.0
    assert decision["publication_time_zero_perturbation_min_matrix_improvement"] == 0.125152
    assert decision["publication_early_time_anchor_included"] is True
    assert (
        decision["publication_early_time_anchor_policy"]
        == "field_early_time_common_mode_not_content_time_zero"
    )
    assert decision["publication_early_time_short_pair_shift_ns"] == 0.0
    assert decision["publication_early_time_short_vs_content_delta_ns"] == 0.127701
    assert decision["publication_early_time_short_agrees_with_content_budget"] is False
    assert decision["publication_early_time_absolute_ready"] is False
    assert decision["publication_cue_spacing_included"] is True
    assert (
        decision["publication_cue_spacing_policy"]
        == "field_cue_spacing_context_threshold_robust_not_resolution_benchmark"
    )
    assert decision["publication_cue_spacing_threshold_count"] == 7.0
    assert decision["publication_cue_spacing_min_same_time_spacing_mm"] == 96.657
    assert decision["publication_cue_spacing_ready_for_field_context"] is True
    assert decision["publication_cue_spacing_resolution_benchmark_ready"] is False
    assert decision["publication_cue_spacing_field_fwi_ready"] is False
    assert decision["publication_timing_anchor_conflict_included"] is True
    assert (
        decision["publication_timing_anchor_conflict_policy"]
        == "field_timing_anchor_conflict_short_relative_not_absolute"
    )
    assert decision["publication_timing_anchor_early_vs_short_delta_half_widths"] == 2.166667
    assert decision["publication_timing_anchor_long_vs_short_delta_half_widths"] == 1.148667
    assert decision["publication_timing_anchor_absolute_time_zero_ready"] is False
    assert decision["publication_timing_anchor_field_fwi_ready"] is False
    assert decision["publication_timing_anchor_ready_for_manuscript_boundary"] is True
    assert decision["publication_timing_window_family_included"] is True
    assert (
        decision["publication_timing_window_family_policy"]
        == "field_timing_window_family_classification_ready_not_absolute"
    )
    assert decision["publication_timing_window_early_strict_near_zero_lag_count"] == 6.0
    assert decision["publication_timing_window_early_strict_row_count"] == 6.0
    assert decision["publication_timing_window_short_nonraw_supported_count"] == 18.0
    assert decision["publication_timing_window_short_nonraw_row_count"] == 18.0
    assert decision["publication_timing_window_long_reject_short_transfer_count"] == 3.0
    assert decision["publication_timing_window_long_row_count"] == 3.0
    assert decision["publication_timing_window_absolute_time_zero_ready"] is False
    assert decision["publication_timing_window_field_fwi_ready"] is False
    assert decision["publication_timing_window_ready_for_manuscript_boundary"] is True
    assert "all candidate anchors" in decision["decision"]
    assert "relative time-zero uncertainty budget" in decision["decision"]
    assert "time-zero perturbation sensitivity audit" in decision["decision"]
    assert "early-time common-mode anchor audit" in decision["decision"]
    assert "cue-spacing threshold sensitivity audit" in decision["decision"]
    assert "timing-anchor conflict synthesis" in decision["decision"]
    assert "timing-window family classification" in decision["decision"]
    assert "no-FWI/no-3D claim boundaries" in decision["decision"]
    assert (
        decision["long_pair_relaxed_phase_anchor_policy_label"]
        == "long_profile_relaxed_phase_anchor_low_snr_not_time_zero"
    )
    assert decision["long_pair_relaxed_phase_anchor_pick_count"] == 10.0
    assert decision["long_pair_relaxed_phase_anchor_low_snr_count"] == 10.0
    assert decision["long_pair_relaxed_phase_anchor_boundary_solution_count"] == 1.0
    assert decision["long_pair_relaxed_phase_anchor_best_phase_convention"] == "cue_time"
    assert decision["long_pair_relaxed_phase_anchor_plausible_depth"] is True
    assert "relaxed late-window phase-anchor audit" in decision["decision"]
    assert "does not upgrade the long pair" in decision["decision"]
    assert (
        decision["field_bandlimited_repeatability_policy_label"]
        == "field_bandlimited_repeatability_short_pair_supported_long_pattern_only"
    )
    assert decision["field_bandlimited_short_supported_band_count"] == 4.0
    assert decision["field_bandlimited_short_supported_bands"] == "low,mid_low,mid_high,broad"
    assert decision["field_bandlimited_short_unfiltered_corrected_abs_correlation"] == 0.771287
    assert decision["field_bandlimited_short_unfiltered_gain"] == 0.225736
    assert decision["field_bandlimited_long_pattern_supported_band_count"] == 4.0
    assert decision["field_bandlimited_long_pattern_supported_bands"] == "mid_low,mid_high,high,broad"
    assert decision["field_bandlimited_long_unfiltered_pattern_abs_correlation"] == 0.905584
    assert decision["field_bandlimited_long_pattern_gain"] == 0.116082
    assert decision["field_bandlimited_gpu_fwi_priority"] == "none"
    assert "band-limited repeatability audit" in decision["decision"]
    assert "pattern-only band support" in decision["decision"]
    assert (
        decision["field_apparent_depth_qc_policy_label"]
        == "field_apparent_depth_qc_relative_scale_not_cover_depth"
    )
    assert decision["field_apparent_depth_qc_cue_count"] == 19.0
    assert decision["field_apparent_depth_qc_short_pair_corrected_support_count"] == 3.0
    assert decision["field_apparent_depth_qc_mean_corrected_depth_residual_mm"] == 2.29049
    assert decision["field_apparent_depth_qc_max_corrected_depth_residual_mm"] == 4.908193
    assert decision["field_apparent_depth_qc_time_zero_depth_equivalent_mm"] == 5.889832
    assert decision["field_apparent_depth_qc_ready_for_apparent_depth_scale_qc"] is True
    assert decision["field_apparent_depth_qc_ready_for_cover_depth_recovery"] is False
    assert decision["field_apparent_depth_qc_ready_for_field_fwi"] is False
    assert (
        decision["field_apparent_depth_sensitivity_policy_label"]
        == "field_apparent_depth_sensitivity_not_calibrated_cover_depth"
    )
    assert decision["field_apparent_depth_sensitivity_scenario_count"] == 5.0
    assert decision["field_apparent_depth_sensitivity_max_depth_span_mm"] == 149.915924
    assert decision["field_apparent_depth_sensitivity_factor"] == 2.181313
    assert decision["field_apparent_depth_sensitivity_all_residuals_supported"] is True
    assert decision["field_apparent_depth_sensitivity_cover_depth_claim_ready"] is False
    assert decision["field_apparent_depth_sensitivity_field_fwi_ready"] is False
    assert (
        decision["field_hyperbola_timezero_degeneracy_policy_label"]
        == "field_hyperbola_timezero_degeneracy_not_calibrated_inversion"
    )
    assert decision["field_hyperbola_timezero_surface_count"] == 4.0
    assert decision["field_hyperbola_timezero_boundary_best_surface_count"] == 3.0
    assert decision["field_hyperbola_timezero_max_near_top_epsr_span"] == 4.084544
    assert decision["field_hyperbola_timezero_max_near_top_time_zero_span_ns"] == 0.3
    assert decision["field_hyperbola_timezero_max_near_top_offset_count_5pct"] == 5.0
    assert decision["field_hyperbola_timezero_cover_depth_claim_ready"] is False
    assert decision["field_hyperbola_timezero_radius_claim_ready"] is False
    assert decision["field_hyperbola_timezero_field_fwi_ready"] is False
    assert "apparent-depth scale QC" in decision["decision"]
    assert "score-surface degeneracy block calibrated cover-depth" in decision["decision"]


def test_evidence_rows_preserve_short_and_long_limits():
    rows = evidence_rows(*_summaries())
    by_name = {row["evidence"]: row for row in rows}

    assert by_name["short_pair_014_016"]["event_pair_count"] == 3
    assert by_name["long_pair_015_013"]["event_pair_count"] == 0
    assert "profile_013_no_phase_anchor_picks" in by_name["long_pair_015_013"]["limitation"]
    assert by_name["short_pair_time_zero_transfer"]["status"] == "relative_time_zero_transfer_limited_qc"
    assert by_name["short_pair_applied_time_zero"]["status"] == "applied_relative_time_zero_transfer_qc"
    assert "6.000x" in by_name["short_pair_applied_time_zero"]["limitation"]
    assert by_name["short_pair_phase_convention_transfer"]["status"] == "multi_phase_relative_time_zero_supported_qc"
    assert "stable_conventions=4/6" in by_name["short_pair_phase_convention_transfer"]["limitation"]
    assert by_name["short_pair_timing_bootstrap"]["status"] == "bootstrap_relative_time_zero_supported_qc"
    assert "bootstrap_ci_ns=0.108055-0.147348" in by_name["short_pair_timing_bootstrap"]["limitation"]
    assert by_name["short_pair_content_windows"]["status"] == "repeat_content_windows_limited_qc"
    assert "content_backed_events=2/3" in by_name["short_pair_content_windows"]["limitation"]
    assert (
        by_name["short_pair_content_synthetic_waveform_qc"]["status"]
        == "content_backed_field_to_synthetic_qc_supported"
    )
    assert by_name["short_pair_content_synthetic_waveform_qc"]["correlation"] == 0.819494
    assert (
        "content_waveform_supported=2/2"
        in by_name["short_pair_content_synthetic_waveform_qc"]["limitation"]
    )
    assert (
        by_name["short_pair_content_time_zero_anchors"]["status"]
        == "short_profile_content_time_zero_anchor_supported_for_visual_qc"
    )
    assert by_name["short_pair_content_time_zero_anchors"]["correlation"] == 0.819494
    assert (
        "supported_content_anchors=2/2"
        in by_name["short_pair_content_time_zero_anchors"]["limitation"]
    )
    assert (
        by_name["short_pair_content_anchor_trace_alignment"]["status"]
        == "content_anchor_field_trace_alignment_improves_after_time_zero"
    )
    assert by_name["short_pair_content_anchor_trace_alignment"]["correlation"] == 0.963803
    assert (
        "mean_abs_corr=0.301->0.964"
        in by_name["short_pair_content_anchor_trace_alignment"]["limitation"]
    )
    assert (
        by_name["short_pair_content_anchor_trace_alignment_sensitivity"]["status"]
        == "content_anchor_trace_alignment_window_robust"
    )
    assert by_name["short_pair_content_anchor_trace_alignment_sensitivity"]["correlation"] == 0.92089
    assert (
        "all_pair_windows_improved=6/6"
        in by_name["short_pair_content_anchor_trace_alignment_sensitivity"]["limitation"]
    )
    assert (
        by_name["short_pair_corrected_profile_stack"]["status"]
        == "corrected_profile_stack_time_zero_supported"
    )
    assert by_name["short_pair_corrected_profile_stack"]["correlation"] == 0.812268
    assert by_name["short_pair_corrected_profile_stack"]["event_pair_count"] == 249
    assert (
        "matrix_abs_corr=0.536->0.812"
        in by_name["short_pair_corrected_profile_stack"]["limitation"]
    )
    assert (
        "improved_columns=161/249"
        in by_name["short_pair_corrected_profile_stack"]["limitation"]
    )
    assert (
        by_name["short_pair_corrected_profile_stack_sensitivity"]["status"]
        == "corrected_profile_stack_window_robust"
    )
    assert by_name["short_pair_corrected_profile_stack_sensitivity"]["correlation"] == 0.7992
    assert by_name["short_pair_corrected_profile_stack_sensitivity"]["event_pair_count"] == 3
    assert (
        "robust_windows=3/3"
        in by_name["short_pair_corrected_profile_stack_sensitivity"]["limitation"]
    )
    assert (
        "min_matrix_improvement=0.263"
        in by_name["short_pair_corrected_profile_stack_sensitivity"]["limitation"]
    )
    assert (
        by_name["short_pair_corrected_stack_spatial_support"]["status"]
        == "corrected_stack_spatial_support_sparse"
    )
    assert by_name["short_pair_corrected_stack_spatial_support"]["correlation"] == 0.421687
    assert by_name["short_pair_corrected_stack_spatial_support"]["event_pair_count"] == 249
    assert (
        "majority_supported_columns=105/249"
        in by_name["short_pair_corrected_stack_spatial_support"]["limitation"]
    )
    assert (
        "largest_interval_m=0.070"
        in by_name["short_pair_corrected_stack_spatial_support"]["limitation"]
    )
    assert (
        by_name["short_pair_supported_interval_visual_qc"]["status"]
        == "supported_interval_visual_qc_ready"
    )
    assert by_name["short_pair_supported_interval_visual_qc"]["correlation"] == 0.909285
    assert by_name["short_pair_supported_interval_visual_qc"]["event_pair_count"] == 3
    assert (
        "supported_intervals=3/3"
        in by_name["short_pair_supported_interval_visual_qc"]["limitation"]
    )
    assert (
        "selected_length_m=0.167"
        in by_name["short_pair_supported_interval_visual_qc"]["limitation"]
    )
    assert (
        by_name["long_pair_short_correction_transfer_audit"]["status"]
        == "long_profile_short_correction_transfer_not_supported"
    )
    assert by_name["long_pair_short_correction_transfer_audit"]["correlation"] == 0.732421
    assert by_name["long_pair_short_correction_transfer_audit"]["event_pair_count"] == 6
    assert (
        "matrix_abs_corr=0.763->0.732"
        in by_name["long_pair_short_correction_transfer_audit"]["limitation"]
    )
    assert (
        "improved_anchor_windows=0/6"
        in by_name["long_pair_short_correction_transfer_audit"]["limitation"]
    )
    assert (
        by_name["long_pair_pattern_shift_scan"]["status"]
        == "long_profile_shift_scan_rejects_short_transfer"
    )
    assert by_name["long_pair_pattern_shift_scan"]["correlation"] == 0.938531
    assert by_name["long_pair_pattern_shift_scan"]["stable_stack_anchor_count"] == 6
    assert "short_offset_gain_vs_zero=-0.044" in by_name["long_pair_pattern_shift_scan"]["limitation"]
    assert "best_pattern_offset_ns=0.060" in by_name["long_pair_pattern_shift_scan"]["limitation"]
    assert (
        by_name["long_pair_pattern_shift_sensitivity"]["status"]
        == "long_profile_pattern_shift_window_robust_rejects_short_transfer"
    )
    assert by_name["long_pair_pattern_shift_sensitivity"]["correlation"] == 0.150305
    assert by_name["long_pair_pattern_shift_sensitivity"]["event_pair_count"] == 3
    assert (
        "best_offset_median_ns=0.060"
        in by_name["long_pair_pattern_shift_sensitivity"]["limitation"]
    )
    assert (
        "offset_spread_ns=0.000"
        in by_name["long_pair_pattern_shift_sensitivity"]["limitation"]
    )
    assert by_name["long_pair_pattern_visual_qc"]["status"] == "long_profile_pattern_visual_qc_ready"
    assert by_name["long_pair_pattern_visual_qc"]["correlation"] == 0.889509
    assert "supported_stable_anchors=6/6" in by_name["long_pair_pattern_visual_qc"]["limitation"]
    assert (
        by_name["long_pair_pattern_holdout_qc"]["status"]
        == "long_profile_pattern_holdout_qc_all_candidate_anchors_supported"
    )
    assert by_name["long_pair_pattern_holdout_qc"]["correlation"] == 0.961006
    assert by_name["long_pair_pattern_holdout_qc"]["event_pair_count"] == 8
    assert "repeat_limited_supported=2/2" in by_name["long_pair_pattern_holdout_qc"]["limitation"]
    assert (
        by_name["long_pair_pattern_holdout_window_sensitivity"]["status"]
        == "long_profile_pattern_holdout_sensitivity_all_candidate_anchors_all_windows_supported"
    )
    assert by_name["long_pair_pattern_holdout_window_sensitivity"]["correlation"] == 0.873226
    assert by_name["long_pair_pattern_holdout_window_sensitivity"]["event_pair_count"] == 24
    assert (
        "supported_rows=24/24"
        in by_name["long_pair_pattern_holdout_window_sensitivity"]["limitation"]
    )
    assert (
        by_name["long_pair_pattern_holdout_width_sensitivity"]["status"]
        == "long_profile_pattern_holdout_width_sensitivity_all_candidate_anchors_all_widths_supported"
    )
    assert by_name["long_pair_pattern_holdout_width_sensitivity"]["correlation"] == 0.888491
    assert by_name["long_pair_pattern_holdout_width_sensitivity"]["event_pair_count"] == 24
    assert (
        "widths=3"
        in by_name["long_pair_pattern_holdout_width_sensitivity"]["limitation"]
    )
    assert (
        by_name["field_publication_claim_bundle"]["status"]
        == (
            "field_publication_claim_bundle_2d_qc_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_"
            "time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
        )
    )
    assert by_name["field_publication_claim_bundle"]["stable_stack_anchor_count"] == 20
    assert by_name["field_publication_claim_bundle"]["event_pair_count"] == 19
    assert "gpu_priority=none" in by_name["field_publication_claim_bundle"]["limitation"]
    assert "time_zero_budget=True" in by_name["field_publication_claim_bundle"]["limitation"]
    assert "time_zero_perturbation=True" in by_name["field_publication_claim_bundle"]["limitation"]
    assert "early_time_anchor=True" in by_name["field_publication_claim_bundle"]["limitation"]
    assert "cue_spacing=True" in by_name["field_publication_claim_bundle"]["limitation"]
    assert "timing_anchor_conflict=True" in by_name["field_publication_claim_bundle"]["limitation"]
    assert "timing_window_family=True" in by_name["field_publication_claim_bundle"]["limitation"]
    assert (
        by_name["field_cue_spacing_context_bundle"]["status"]
        == "field_cue_spacing_context_threshold_robust_not_resolution_benchmark"
    )
    assert by_name["field_cue_spacing_context_bundle"]["correlation"] == 96.657
    assert by_name["field_cue_spacing_context_bundle"]["stable_stack_anchor_count"] == 7
    assert by_name["field_cue_spacing_context_bundle"]["event_pair_count"] == 32
    assert "resolution_ready=False" in by_name["field_cue_spacing_context_bundle"]["limitation"]
    assert "measured_field_context_only" in by_name["field_cue_spacing_context_bundle"]["limitation"]
    assert (
        by_name["field_timing_anchor_conflict_bundle"]["status"]
        == "field_timing_anchor_conflict_short_relative_not_absolute"
    )
    assert by_name["field_timing_anchor_conflict_bundle"]["correlation"] == 2.166667
    assert by_name["field_timing_anchor_conflict_bundle"]["stable_stack_anchor_count"] == 1.148667
    assert by_name["field_timing_anchor_conflict_bundle"]["event_pair_count"] == 1
    assert "absolute_ready=False" in by_name["field_timing_anchor_conflict_bundle"]["limitation"]
    assert "timing_scope_boundary_only" in by_name["field_timing_anchor_conflict_bundle"]["limitation"]
    assert (
        by_name["field_timing_window_family_bundle"]["status"]
        == "field_timing_window_family_classification_ready_not_absolute"
    )
    assert by_name["field_timing_window_family_bundle"]["correlation"] == 18
    assert by_name["field_timing_window_family_bundle"]["stable_stack_anchor_count"] == 6
    assert by_name["field_timing_window_family_bundle"]["event_pair_count"] == 3
    assert "early_strict_near_zero=6/6" in (
        by_name["field_timing_window_family_bundle"]["limitation"]
    )
    assert "short_nonraw_supported=18/18" in (
        by_name["field_timing_window_family_bundle"]["limitation"]
    )
    assert "long_reject_short_transfer=3/3" in (
        by_name["field_timing_window_family_bundle"]["limitation"]
    )
    assert "window_family_boundary_only" in (
        by_name["field_timing_window_family_bundle"]["limitation"]
    )
    assert (
        by_name["long_pair_relaxed_phase_anchor_audit"]["status"]
        == "long_profile_relaxed_phase_anchor_low_snr_not_time_zero"
    )
    assert by_name["long_pair_relaxed_phase_anchor_audit"]["correlation"] == 1.847077
    assert by_name["long_pair_relaxed_phase_anchor_audit"]["stable_stack_anchor_count"] == 0.0
    assert by_name["long_pair_relaxed_phase_anchor_audit"]["event_pair_count"] == 10.0
    assert "low_snr_picks=10/10" in by_name["long_pair_relaxed_phase_anchor_audit"]["limitation"]
    assert "boundary_solutions=1" in by_name["long_pair_relaxed_phase_anchor_audit"]["limitation"]
    assert (
        by_name["short_pair_content_backed_waveform_panels"]["status"]
        == "content_backed_waveform_visual_qc"
    )
    assert by_name["short_pair_content_backed_waveform_panels"]["event_pair_count"] == 4
    assert "valid_panels=4/4" in by_name["short_pair_content_backed_waveform_panels"]["limitation"]
    assert (
        by_name["field_bandlimited_repeatability_audit"]["status"]
        == "field_bandlimited_repeatability_short_pair_supported_long_pattern_only"
    )
    assert by_name["field_bandlimited_repeatability_audit"]["correlation"] == 0.771287
    assert by_name["field_bandlimited_repeatability_audit"]["stable_stack_anchor_count"] == 4
    assert by_name["field_bandlimited_repeatability_audit"]["event_pair_count"] == 4
    assert "short_supported_bands=low,mid_low,mid_high,broad" in (
        by_name["field_bandlimited_repeatability_audit"]["limitation"]
    )
    assert "gpu_fwi_priority=none" in by_name["field_bandlimited_repeatability_audit"]["limitation"]
    assert (
        by_name["field_apparent_depth_scale_qc"]["status"]
        == "field_apparent_depth_qc_relative_scale_not_cover_depth"
    )
    assert by_name["field_apparent_depth_scale_qc"]["correlation"] == 1.0
    assert by_name["field_apparent_depth_scale_qc"]["stable_stack_anchor_count"] == 3
    assert by_name["field_apparent_depth_scale_qc"]["event_pair_count"] == 19
    assert "max_corrected_depth_residual_mm=4.908" in (
        by_name["field_apparent_depth_scale_qc"]["limitation"]
    )
    assert "relative_apparent_depth_qc_only" in (
        by_name["field_apparent_depth_scale_qc"]["limitation"]
    )
    assert (
        by_name["field_apparent_depth_sensitivity_qc"]["status"]
        == "field_apparent_depth_sensitivity_not_calibrated_cover_depth"
    )
    assert by_name["field_apparent_depth_sensitivity_qc"]["correlation"] == 2.181313
    assert by_name["field_apparent_depth_sensitivity_qc"]["event_pair_count"] == 5
    assert "cover_depth_ready=False" in (
        by_name["field_apparent_depth_sensitivity_qc"]["limitation"]
    )
    assert (
        by_name["field_hyperbola_timezero_degeneracy_audit"]["status"]
        == "field_hyperbola_timezero_degeneracy_not_calibrated_inversion"
    )
    assert by_name["field_hyperbola_timezero_degeneracy_audit"]["correlation"] == 4.084544
    assert by_name["field_hyperbola_timezero_degeneracy_audit"]["stable_stack_anchor_count"] == 3
    assert by_name["field_hyperbola_timezero_degeneracy_audit"]["event_pair_count"] == 4
    assert "boundary_best_surfaces=3/4" in (
        by_name["field_hyperbola_timezero_degeneracy_audit"]["limitation"]
    )
    assert "no_cover_depth_radius_or_field_fwi" in (
        by_name["field_hyperbola_timezero_degeneracy_audit"]["limitation"]
    )
