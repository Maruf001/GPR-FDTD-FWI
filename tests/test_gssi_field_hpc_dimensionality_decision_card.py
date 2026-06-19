from run_gssi_field_hpc_dimensionality_decision_card import (
    build_decision_rows,
    summarize_decision,
)


def _inputs():
    survey = {
        "classification": "independent_2d_line_profiles",
        "profile_count": 4,
        "has_crossline_file": False,
        "has_reliable_waypoint_lengths": False,
    }
    readiness = {
        "ready_for_2d_qc": True,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "profile_count": 4,
        "total_trace_derived_length_m": 7.215945,
        "scan_spacing_mm": 3.333,
        "center_wavelength_mm": 124.9135,
        "samples_per_wavelength": 37.4778,
        "time_zero_two_way_depth_equivalent_mm": 5.8898,
        "spatial_all_window_supported_fraction": 0.281124,
        "spatial_all_window_supported_column_count": 70,
        "spatial_finite_column_count": 249,
        "field_hpc_priority": "none",
    }
    timing = {
        "short_nominal_offset_ns": 0.127701,
        "early_min_uniqueness_margin": 3.017058e-05,
        "early_has_low_uniqueness_margin": True,
        "long_best_offset_distance_from_short_ns": 0.067701,
    }
    claims = {
        "supported_count": 3,
        "scope_limited_count": 5,
        "blocked_count": 3,
        "ready_for_2d_field_qc": True,
        "ready_for_absolute_time_zero": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
    }
    timing_envelope = {
        "short_anchor_count": 3,
        "short_anchor_inside_envelope_count": 3,
        "long_pattern_reject_short_transfer_count": 8,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_long_short_transfer": False,
    }
    spatial_transfer = {
        "long_pattern_anchor_count": 8,
        "long_pattern_with_nearest_short_content_within_threshold_count": 1,
        "median_long_to_short_distance_mm": 701.5965,
        "ready_for_short_to_long_timing_transfer": False,
    }
    anchor_interval = {
        "short_anchor_count": 3,
        "short_anchor_inside_supported_interval_count": 3,
        "short_content_anchor_inside_supported_interval_count": 2,
        "min_margin_to_supported_interval_edge_mm": 13.332,
        "ready_for_short_relative_timing_qc": True,
    }
    return survey, readiness, timing, claims, timing_envelope, spatial_transfer, anchor_interval


def test_decision_rows_keep_field_dataset_on_2d_cpu_path():
    survey, readiness, timing, claims, timing_envelope, spatial_transfer, anchor_interval = _inputs()
    rows = build_decision_rows(
        survey=survey,
        readiness=readiness,
        timing=timing,
        claims=claims,
        timing_envelope=timing_envelope,
        spatial_transfer=spatial_transfer,
        anchor_interval=anchor_interval,
    )
    by_key = {row["gate_key"]: row for row in rows}

    assert by_key["survey_dimensionality"]["decision"] == "2d_line_profiles_only"
    assert by_key["survey_dimensionality"]["status"] == "blocks_3d_hpc"
    assert by_key["alongline_sampling"]["status"] == "ready_for_2d_qc"
    assert by_key["timing_anchor_scope"]["status"] == "blocks_absolute_time_zero"
    assert by_key["short_profile_timing_support"]["status"] == "ready_for_short_qc"
    assert by_key["long_profile_transfer_scope"]["status"] == "blocks_long_transfer"
    assert by_key["field_hpc_fwi_gate"]["decision"] == "do_not_submit_field_hpc_job"
    assert by_key["field_hpc_fwi_gate"]["readiness_score"] == 0.0


def test_summary_blocks_3d_hpc_fwi_and_parametric_recovery():
    survey, readiness, timing, claims, timing_envelope, spatial_transfer, anchor_interval = _inputs()
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

    assert summary["policy_label"] == "gssi51600s_field_hpc_dimensionality_decision_2d_short_qc_no_hpc"
    assert summary["field_geometry_type"] == "independent_2d_line_profiles"
    assert summary["is_3d_survey"] is False
    assert summary["ready_for_2d_qc"] is True
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_long_short_transfer"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_radius_recovery"] is False
    assert summary["ready_for_cover_depth_recovery"] is False
    assert summary["short_anchor_inside_supported_interval_count"] == 3
    assert summary["long_pattern_reject_short_transfer_count"] == 8
    assert summary["field_hpc_priority"] == "none"
    assert "four independent 2D line profiles" in summary["decision"]
