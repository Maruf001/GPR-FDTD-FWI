from run_gssi_field_qc_to_controlled_collection_bridge import (
    build_action_bridge_rows,
    build_evidence_rows,
    summarize_bridge,
)


def _summaries():
    return {
        "dimensionality": {
            "field_geometry_type": "independent_2d_line_profiles",
            "is_3d_survey": False,
            "profile_count": 4,
        },
        "time_zero_ladder": {
            "ready_for_short_relative_timing_qc": True,
            "ready_for_leave_one_content_anchor_claim": False,
            "content_only_offset_half_range_ns": 0.009823,
        },
        "spatial_consistency": {
            "ready_for_profile_spatial_calibration": False,
        },
        "waveform": {
            "ready_for_waveform_morphology_qc": True,
            "min_corrected_field_trace_abs_correlation": 0.939,
            "radius_match_pair_count": 0,
        },
        "timing_margin": {
            "ready_for_content_only_morphology_timing_qc": True,
            "ready_for_conservative_timing_morphology_claim": False,
            "min_default_timing_slack_ns": 0.030354,
        },
        "contrast_regime": {
            "ready_for_broad_event_signal_contrast_regime": True,
            "ready_for_strict_window_invariant_signal_contrast_claim": False,
            "broad_event_min_event_to_noise_rms": 5.051,
        },
        "reference_requirement": {
            "current_packet_time_zero_reference_ready": False,
            "reference_repeat_gate": 3,
            "reference_uncertainty_gate_ns": 0.02,
            "reference_uncertainty_gate_depth_error_mm": 1.9986,
        },
        "packet_validation": {
            "ready_for_packet_acceptance": False,
            "blocking_finding_count": 44,
            "missing_required_value_count": 44,
        },
        "action_summary": {
            "failed_acceptance_gate_count": 7,
            "ready_for_new_controlled_2d_acquisition": True,
        },
    }


def _action_rows():
    rows = [
        ("target_truth_geometry", 1, 9, True, False),
        ("time_zero_reference", 2, 6, True, False),
        ("amplitude_reference", 3, 6, True, False),
        ("profile_target_geometry", 4, 6, True, False),
        ("acquisition_control_links", 5, 9, True, False),
        ("session_metadata", 6, 2, False, True),
        ("reference_registry", 7, 6, True, False),
    ]
    return [
        {
            "blocker_group": group,
            "priority": priority,
            "action_type": "new_controlled_measurement",
            "missing_required_count": missing,
            "minimum_rows_or_repeats": 3 if "reference" in group else 1,
            "requires_new_controlled_data": requires_new,
            "current_archive_can_resolve": archive_can_resolve,
            "acceptance_gates_unblocked": "field_fwi_or_heavy_work",
            "reference_uncertainty_gate_ns": 0.02 if group == "time_zero_reference" else "",
            "reference_depth_equivalent_mm": 1.9986 if group == "time_zero_reference" else "",
            "action": f"Resolve {group}",
        }
        for group, priority, missing, requires_new, archive_can_resolve in rows
    ]


def _gate_rows():
    return [
        {"gate_key": "target_truth_controls", "ready_now": False},
        {"gate_key": "required_metadata_fields", "ready_now": False},
        {"gate_key": "cross_table_links", "ready_now": False},
        {"gate_key": "absolute_time_zero_references", "ready_now": False},
        {"gate_key": "amplitude_references", "ready_now": False},
        {"gate_key": "field_fwi_or_heavy_work", "ready_now": False},
    ]


def test_evidence_rows_separate_current_qc_support_from_inversion_blockers():
    rows = build_evidence_rows(_summaries(), _action_rows(), _gate_rows())
    by_key = {row["axis_key"]: row for row in rows}

    assert by_key["field_archive_dimensionality"]["ready"] is True
    assert by_key["short_relative_timing_qc"]["ready"] is True
    assert by_key["waveform_morphology_qc"]["ready"] is True
    assert by_key["content_only_timing_margin"]["ready"] is True
    assert by_key["broad_signal_contrast_qc"]["ready"] is True
    assert by_key["absolute_time_zero_reference"]["ready"] is False
    assert by_key["absolute_amplitude_calibration"]["ready"] is False
    assert by_key["target_truth_and_profile_geometry"]["ready"] is False
    assert by_key["controlled_repeat_packet_acceptance"]["ready"] is False


def test_action_bridge_marks_first_five_groups_as_critical_or_high_new_data():
    rows = build_action_bridge_rows(_action_rows())
    by_group = {row["blocker_group"]: row for row in rows}

    assert by_group["target_truth_geometry"]["research_priority"] == "critical"
    assert by_group["time_zero_reference"]["research_priority"] == "critical"
    assert by_group["amplitude_reference"]["research_priority"] == "critical"
    assert by_group["profile_target_geometry"]["research_priority"] == "high"
    assert by_group["acquisition_control_links"]["research_priority"] == "high"
    assert by_group["session_metadata"]["current_archive_can_resolve"] is True
    assert "absolute_time_zero" in by_group["time_zero_reference"]["unblocks_axes"]


def test_summary_keeps_current_archive_out_of_field_fwi_and_hpc():
    evidence_rows = build_evidence_rows(_summaries(), _action_rows(), _gate_rows())
    action_rows = build_action_bridge_rows(_action_rows())
    summary = summarize_bridge(evidence_rows, action_rows, _summaries())

    assert summary["current_archive_supported_axis_count"] == 5
    assert summary["unresolved_inversion_blocker_axis_count"] == 4
    assert summary["critical_new_data_action_group_count"] == 5
    assert summary["ready_for_current_archive_field_qc_supplement"] is True
    assert summary["ready_for_current_archive_absolute_time_zero"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["ready_for_current_archive_heavy_field_work"] is False
    assert summary["ready_for_field_3d_hpc"] is False
    assert summary["ready_for_new_controlled_2d_acquisition"] is True
    assert summary["gpu_priority"] == "none"
