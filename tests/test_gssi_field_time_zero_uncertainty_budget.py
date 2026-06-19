from run_gssi_field_time_zero_uncertainty_budget import budget_rows, summarize_budget


def _summaries():
    return {
        "transfer": {
            "summary": {
                "policy_label": "relative_time_zero_transfer_limited_qc",
                "event_pair_count": 3,
                "median_comparison_minus_reference_phase_time_ns": 0.127701,
                "min_comparison_minus_reference_phase_time_ns": 0.108055,
                "max_comparison_minus_reference_phase_time_ns": 0.176817,
                "best_normalized_correlation": 0.931186,
            }
        },
        "application": {
            "summary": {
                "policy_label": "applied_relative_time_zero_transfer_qc",
                "event_pair_count": 3,
                "applied_transfer_offset_ns": 0.127701,
                "leave_one_out_max_abs_residual_ns": 0.058939,
                "mean_abs_residual_reduction_factor": 6.0,
            }
        },
        "phase_convention": {
            "summary": {
                "policy_label": "multi_phase_relative_time_zero_supported_qc",
                "phase_convention_count": 6,
                "stable_phase_convention_count": 4,
                "stable_median_delta_min_ns": 0.108055,
                "stable_median_delta_max_ns": 0.127701,
                "stable_median_delta_spread_ns": 0.019646,
            }
        },
        "bootstrap": {
            "summary": {
                "policy_label": "bootstrap_relative_time_zero_supported_qc",
                "stable_offset_count": 12,
                "observed_median_offset_ns": 0.117878,
                "min_bootstrap_ci_lower_ns": 0.108055,
                "max_bootstrap_ci_upper_ns": 0.147348,
                "max_bootstrap_ci_width_ns": 0.039293,
            }
        },
        "content_anchor": {
            "policy_label": "short_profile_content_time_zero_anchor_supported_for_visual_qc",
            "event_pair_count": 3,
            "supported_content_anchor_pair_count": 2,
            "max_abs_content_timing_residual_ns": 0.009823,
            "min_content_pair_absolute_correlation": 0.819494,
        },
        "trace_alignment": {
            "policy_label": "content_anchor_field_trace_alignment_improves_after_time_zero",
            "supported_anchor_pair_count": 2,
            "field_trace_alignment_improved_count": 2,
            "max_corrected_abs_timing_residual_ns": 0.019646,
            "mean_corrected_abs_correlation": 0.963803,
        },
        "trace_sensitivity": {
            "policy_label": "content_anchor_trace_alignment_window_robust",
            "improved_pair_window_count": 6,
            "pair_window_row_count": 6,
            "min_corrected_abs_correlation": 0.920890,
        },
        "stack": {
            "summary": {
                "policy_label": "corrected_profile_stack_time_zero_supported",
                "improved_column_count": 161,
                "finite_column_count": 249,
                "corrected_matrix_abs_correlation": 0.812268,
            }
        },
        "stack_sensitivity": {
            "policy_label": "corrected_profile_stack_window_robust",
            "robust_window_count": 3,
            "window_count": 3,
            "min_matrix_abs_correlation_improvement": 0.263036,
        },
        "spatial_support": {
            "policy_label": "corrected_stack_spatial_support_sparse",
            "all_window_supported_column_count": 70,
            "finite_column_count": 249,
            "largest_majority_interval_length_m": 0.069993,
        },
        "supported_interval": {
            "policy_label": "supported_interval_visual_qc_ready",
            "supported_interval_count": 3,
            "selected_interval_count": 3,
            "min_corrected_interval_abs_correlation": 0.909285,
        },
        "bandlimited": {
            "policy_label": "field_bandlimited_repeatability_short_pair_supported_long_pattern_only",
            "short_supported_band_count": 4,
            "short_supported_bands": "low,mid_low,mid_high,broad",
            "short_unfiltered_abs_correlation_gain": 0.225736,
            "bands": [{}, {}, {}, {}, {}],
        },
        "event_support": {
            "policy_label": "field_event_support_tiers_2d_qc_ready_not_fwi",
            "short_content_anchor_supported_count": 2,
            "short_event_pair_count": 3,
            "short_content_anchor_support_fraction": 2 / 3,
        },
    }


def test_budget_rows_capture_offset_bounds_and_support_rows():
    rows = budget_rows(_summaries())
    by_key = {row["budget_key"]: row for row in rows}

    assert len(rows) == 13
    assert by_key["short_pair_transfer_offset_range"]["central_offset_ns"] == 0.127701
    assert by_key["short_pair_transfer_offset_range"]["lower_bound_ns"] == 0.108055
    assert by_key["bootstrap_stable_offset_ci"]["upper_bound_ns"] == 0.147348
    assert by_key["content_anchor_residual_guardrail"]["support_count"] == 2
    assert by_key["content_anchor_residual_guardrail"]["total_count"] == 3
    assert by_key["trace_alignment_window_robustness"]["support_fraction"] == 1.0
    assert by_key["spatial_support_mask"]["support_fraction"] == 70 / 249
    assert by_key["bandlimited_short_repeatability"]["support_fraction"] == 4 / 5
    assert "absolute calibrated time-zero" in by_key["bootstrap_stable_offset_ci"]["claim_blocked"]


def test_summarize_budget_preserves_relative_qc_boundary():
    summaries = _summaries()
    rows = budget_rows(summaries)
    summary = summarize_budget(rows, summaries)

    assert summary["policy_label"] == "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute"
    assert summary["budget_row_count"] == 13
    assert summary["relative_anchor_offset_ns"] == 0.127701
    assert summary["bootstrap_ci_lower_ns"] == 0.108055
    assert summary["bootstrap_ci_upper_ns"] == 0.147348
    assert summary["leave_one_out_max_abs_residual_ns"] == 0.058939
    assert summary["content_anchor_supported_pair_count"] == 2
    assert summary["absolute_time_zero_ready"] is False
    assert summary["field_fwi_ready"] is False
    assert summary["field_gpu_fwi_priority"] == "none"
