from run_gssi_field_event_support_tiers import summarize_tiers, tier_rows


def _summaries():
    return {
        "geometry": {
            "classification": "independent_2d_line_profiles",
            "profile_count": 4,
        },
        "short_anchor": {
            "event_pair_count": 3,
            "supported_content_anchor_pair_count": 2,
            "timing_only_event_pair_count": 1,
            "max_abs_all_timing_residual_ns": 0.058939,
            "min_content_pair_absolute_correlation": 0.819494,
        },
        "short_interval": {
            "selected_interval_count": 3,
            "supported_interval_count": 3,
            "min_corrected_interval_abs_correlation": 0.909285,
        },
        "long_visual": {
            "min_pattern_shift_abs_correlation": 0.889509,
        },
        "long_holdout": {
            "stable_anchor_count": 6,
            "stable_supported_anchor_count": 6,
            "repeat_limited_anchor_count": 2,
            "repeat_limited_supported_anchor_count": 2,
            "min_repeat_limited_pattern_shift_abs_correlation": 0.961006,
        },
        "bandlimited": {
            "short_supported_band_count": 4,
            "long_pattern_supported_band_count": 4,
            "short_unfiltered_abs_correlation_gain": 0.225736,
            "long_unfiltered_pattern_gain": 0.116082,
            "bands": [
                {"band_label": "low"},
                {"band_label": "mid_low"},
                {"band_label": "mid_high"},
                {"band_label": "high"},
                {"band_label": "broad"},
            ],
        },
        "timing_discriminant": {
            "score_row_count": 4,
            "short_nonraw_supported_count": 18,
            "long_reject_short_transfer_count": 3,
            "short_min_nonraw_matrix_improvement": 0.125152,
            "absolute_time_zero_ready": False,
        },
        "hpc_dimensionality": {
            "field_geometry_type": "independent_2d_line_profiles",
            "ready_for_2d_qc": True,
            "ready_for_3d_hpc": False,
            "ready_for_field_fwi": False,
            "field_hpc_priority": "none",
            "is_3d_survey": False,
        },
    }


def test_tier_rows_encode_field_support_and_blockers():
    rows = tier_rows(_summaries())
    by_key = {row["tier_key"]: row for row in rows}

    assert len(rows) == 11
    assert by_key["short_content_time_zero_anchors"]["supported_count"] == 2
    assert by_key["short_content_time_zero_anchors"]["total_count"] == 3
    assert by_key["short_content_time_zero_anchors"]["support_fraction"] == 2 / 3
    assert by_key["short_timing_only_cue"]["support_tier"] == "timing_only_limited_qc"
    assert by_key["long_stable_pattern_anchors"]["support_fraction"] == 1.0
    assert by_key["short_bandlimited_repeatability"]["support_fraction"] == 4 / 5
    assert by_key["timing_discriminant_scorecard"]["support_tier"] == "timing_scope_boundary_qc"
    assert by_key["timing_discriminant_scorecard"]["supported_count"] == 4
    assert by_key["hpc_dimensionality_boundary"]["support_tier"] == "hpc_2d_boundary_no_hpc"
    assert by_key["hpc_dimensionality_boundary"]["quality_metric_value"] == 0.0
    assert by_key["field_fwi_readiness_blocked"]["support_fraction"] == 0.0
    assert "field FWI" in by_key["field_fwi_readiness_blocked"]["claim_blocked"]


def test_summarize_tiers_preserves_no_fwi_policy():
    summaries = _summaries()
    rows = tier_rows(summaries)
    summary = summarize_tiers(rows, summaries)

    assert summary["policy_label"] == "field_event_support_tiers_timing_discriminant_hpc_2d_qc_ready_not_fwi"
    assert summary["tier_row_count"] == 11
    assert summary["blocked_row_count"] == 1
    assert summary["short_content_anchor_supported_count"] == 2
    assert summary["short_content_anchor_support_fraction"] == 2 / 3
    assert summary["long_pattern_total_supported_anchor_count"] == 8
    assert summary["timing_discriminant_included"] is True
    assert summary["timing_discriminant_absolute_time_zero_ready"] is False
    assert summary["hpc_dimensionality_included"] is True
    assert summary["hpc_dimensionality_ready_for_3d_hpc"] is False
    assert summary["field_fwi_ready"] is False
    assert summary["field_gpu_fwi_priority"] == "none"
    assert "Missing survey grid metadata" in summary["decision"]
