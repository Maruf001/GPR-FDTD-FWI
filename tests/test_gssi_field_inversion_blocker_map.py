from run_gssi_field_inversion_blocker_map import build_evidence_rows, gate_rows, summarize_blocker_map


def _sample_summaries():
    return {
        "time_zero_ladder": {
            "ready_for_short_relative_timing_qc": True,
            "ready_for_leave_one_content_anchor_claim": False,
            "ready_for_long_short_transfer": False,
            "ready_for_absolute_time_zero": False,
            "content_only_offset_half_range_ns": 0.0098,
            "leave_one_degraded_single_content_count": 2,
            "long_pattern_reject_short_transfer_count": 8,
            "short_conservative_half_width_ns": 0.0589,
        },
        "spatial_consistency": {
            "ready_for_profile_spatial_calibration": False,
            "content_residual_range_mm": 30.0,
            "content_residual_sign_consistent": False,
        },
        "inversion_readiness": {
            "ready_for_apparent_depth_scale_qc": True,
            "ready_for_cover_depth_recovery": False,
            "ready_for_field_fwi": False,
            "ready_for_3d_hpc": False,
            "field_geometry_type": "independent_2d_line_profiles",
            "is_3d_survey": False,
            "max_corrected_depth_residual_mm": 4.9,
            "apparent_depth_max_span_mm": 149.9,
            "supported_gate_count": 2,
            "gate_count": 8,
        },
        "waveform_coherence": {
            "ready_for_waveform_morphology_qc": True,
            "min_corrected_field_trace_abs_correlation": 0.94,
        },
        "radius_degeneracy": {
            "ready_for_radius_recovery": False,
            "ready_for_radius_seed": False,
            "weak_radius_side_count": 4,
            "selected_radius_mismatch_pair_count": 2,
            "common_radius_near_tie_pair_count": 2,
        },
        "signed_morphology": {
            "ready_for_signed_waveform_morphology_qc": True,
            "min_corrected_signed_correlation": 0.94,
        },
        "timing_margin": {
            "ready_for_content_only_morphology_timing_qc": True,
            "min_default_timing_slack_ns": 0.03,
        },
        "signal_contrast": {
            "ready_for_absolute_amplitude_calibration": False,
        },
        "contrast_sensitivity": {
            "all_supported_combo_fraction": 13 / 27,
            "all_supported_combo_count": 13,
            "sensitivity_combo_count": 27,
        },
        "contrast_regime": {
            "ready_for_broad_event_signal_contrast_regime": True,
            "ready_for_absolute_amplitude_calibration": False,
            "ready_for_strict_window_invariant_signal_contrast_claim": False,
            "broad_event_min_event_to_noise_rms": 5.05,
        },
    }


def test_blocker_map_promotes_morphology_but_blocks_inversion():
    summaries = _sample_summaries()
    rows = build_evidence_rows(summaries)
    summary = summarize_blocker_map(rows, summaries)

    assert summary["evidence_axis_count"] == 6
    assert summary["ready_evidence_axis_count"] == 6
    assert summary["blocker_axis_count"] == 9
    assert summary["critical_unresolved_blocker_count"] == 6
    assert summary["ready_for_field_morphology_supplement"] is True
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["gpu_priority"] == "none"


def test_gate_rows_keep_heavy_field_work_blocked():
    summaries = _sample_summaries()
    rows = build_evidence_rows(summaries)
    summary = summarize_blocker_map(rows, summaries)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert gates["field_morphology_supplement"]["ready"] is True
    assert gates["field_inversion_or_fwi"]["ready"] is False
    assert gates["field_3d_hpc"]["ready"] is False
    assert gates["heavy_field_work"]["ready"] is False
