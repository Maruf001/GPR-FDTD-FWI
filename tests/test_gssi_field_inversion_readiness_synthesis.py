from run_gssi_field_inversion_readiness_synthesis import (
    build_readiness_rows,
    summarize_readiness,
)


def _inputs():
    apparent_depth = {
        "ready_for_apparent_depth_scale_qc": True,
        "ready_for_cover_depth_recovery": False,
        "max_corrected_depth_residual_mm": 4.9,
        "time_zero_depth_equivalent_mm": 5.89,
    }
    apparent_sensitivity = {
        "all_residuals_within_budget_all_scenarios": True,
        "cover_depth_claim_ready": False,
        "max_apparent_depth_span_mm": 149.9,
        "max_apparent_depth_sensitivity_factor": 2.18,
    }
    hyperbola = {
        "cover_depth_claim_ready": False,
        "radius_claim_ready": False,
        "field_fwi_ready": False,
        "max_near_top_epsr_span": 4.08,
        "max_near_top_time_zero_span_ns": 0.3,
    }
    cue_timing = {
        "long_pattern_reject_short_transfer_count": 8,
        "ready_for_long_short_transfer": False,
    }
    spatial_transfer = {
        "long_pattern_with_nearest_short_content_within_threshold_count": 1,
        "ready_for_short_to_long_timing_transfer": False,
    }
    anchor_interval = {
        "short_anchor_inside_supported_interval_count": 3,
        "ready_for_short_relative_timing_qc": True,
    }
    dimensionality = {
        "field_geometry_type": "independent_2d_line_profiles",
        "is_3d_survey": False,
        "profile_count": 4,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "ready_for_radius_recovery": False,
    }
    time_zero = {
        "ready_for_short_relative_timing_qc": True,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "content_only_offset_half_range_ns": 0.009823,
    }
    spatial_consistency = {
        "ready_for_short_relative_timing_qc": True,
        "ready_for_profile_spatial_calibration": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "content_residual_range_mm": 29.997,
        "content_residual_half_range_mm": 14.9985,
        "content_min_supported_interval_margin_mm": 13.332,
    }
    return (
        apparent_depth,
        apparent_sensitivity,
        hyperbola,
        cue_timing,
        spatial_transfer,
        anchor_interval,
        dimensionality,
        time_zero,
        spatial_consistency,
    )


def test_readiness_rows_support_only_short_qc_and_depth_scale_qc():
    rows = build_readiness_rows(*_inputs())
    by_key = {row["gate_key"]: row for row in rows}

    assert by_key["short_relative_timing_qc"]["ready"] is True
    assert by_key["apparent_depth_scale_qc"]["ready"] is True
    assert by_key["long_profile_transfer"]["ready"] is False
    assert by_key["profile_spatial_calibration"]["ready"] is False
    assert by_key["cover_depth_recovery"]["ready"] is False
    assert by_key["radius_recovery"]["ready"] is False
    assert by_key["field_fwi"]["ready"] is False
    assert by_key["field_3d_hpc"]["ready"] is False


def test_summary_blocks_heavy_field_work():
    inputs = _inputs()
    rows = build_readiness_rows(*inputs)
    summary = summarize_readiness(
        rows,
        inputs[0],
        inputs[1],
        inputs[2],
        inputs[6],
        inputs[7],
        inputs[8],
    )

    assert summary["gate_count"] == 8
    assert summary["supported_gate_count"] == 2
    assert summary["blocked_gate_count"] == 6
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_apparent_depth_scale_qc"] is True
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["ready_for_heavy_field_work"] is False
    assert summary["gpu_priority"] == "none"
