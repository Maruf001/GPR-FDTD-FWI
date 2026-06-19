from run_gssi_field_existing_data_control_manifest import gate_rows, summarize_manifest


def _requirement(axis_key, priority, has_evidence, satisfies):
    return {
        "axis_key": axis_key,
        "priority": priority,
        "phase": "test",
        "current_archive_ready_from_design": satisfies,
        "archive_evidence_status": "partial" if has_evidence else "missing",
        "archive_has_relevant_evidence": has_evidence,
        "archive_satisfies_control": satisfies,
        "existing_evidence": "test evidence",
        "missing_control": "test missing control",
        "required_new_measurement": "test measurement",
        "acceptance_gate": "test gate",
        "allowed_current_use": "QC/context only",
        "blocked_current_use": "test blocked",
        "primary_source_path": "test.csv",
    }


def test_manifest_keeps_partial_must_have_qc_out_of_field_fwi():
    requirement_rows = [
        _requirement("absolute_time_zero", "must_have", True, False),
        _requirement("profile_spatial_calibration", "must_have", True, False),
        _requirement("radius_seed_or_recovery", "must_have", True, False),
        _requirement("cover_depth_recovery", "must_have", True, False),
        _requirement("absolute_amplitude_calibration", "must_have", True, False),
        _requirement("leave_one_content_redundancy", "should_have", True, False),
    ]
    evidence_rows = [
        {"evidence_key": "raw_file_inventory", "row_count": 4},
    ]
    inventory_rows = [
        {"profile_length_m": "2.0"},
        {"profile_length_m": "1.0"},
    ]

    summary = summarize_manifest(
        requirement_rows,
        evidence_rows,
        inventory_rows,
        {"ready_for_new_controlled_2d_acquisition_design": True},
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["must_have_requirement_count"] == 5
    assert summary["satisfied_must_have_requirement_count"] == 0
    assert summary["partial_qc_must_have_requirement_count"] == 5
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["ready_for_current_archive_heavy_field_work"] is False
    assert summary["ready_for_new_controlled_2d_acquisition_design"] is True
    assert gates["current_archive_field_fwi"]["ready"] is False
    assert gates["field_3d_hpc"]["ready"] is False


def test_manifest_counts_satisfied_must_have_without_enabling_heavy_work():
    requirement_rows = [
        _requirement("absolute_time_zero", "must_have", True, True),
        _requirement("profile_spatial_calibration", "must_have", True, False),
    ]
    summary = summarize_manifest(
        requirement_rows,
        [{"evidence_key": "raw_file_inventory", "row_count": 1}],
        [{"profile_length_m": "0.5"}],
        {"ready_for_new_controlled_2d_acquisition_design": True},
    )

    assert summary["satisfied_must_have_requirement_count"] == 1
    assert summary["missing_or_unsatisfied_must_have_requirement_count"] == 1
    assert summary["ready_for_current_archive_field_fwi"] is False
