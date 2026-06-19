from run_gssi_field_controlled_2d_acquisition_protocol import (
    acceptance_gates,
    protocol_steps,
    schema_rows,
    summarize,
)


def _design_row(axis, priority="must_have"):
    return {
        "axis_key": axis,
        "priority": priority,
        "required_new_measurement": f"measure {axis}",
        "acceptance_gate": f"accept {axis}",
        "analysis_after_acquisition": f"analyze {axis}",
    }


def _control_row(axis):
    return {
        "axis_key": axis,
        "missing_control": f"missing {axis}",
    }


def test_protocol_includes_must_have_controls_and_blocks_current_fwi():
    axes = [
        "absolute_amplitude_calibration",
        "profile_spatial_calibration",
        "cover_depth_recovery",
        "radius_seed_or_recovery",
        "absolute_time_zero",
        "leave_one_content_redundancy",
        "long_profile_transfer",
    ]
    design_rows = [_design_row(axis) for axis in axes]
    control_rows = [_control_row(axis) for axis in axes]
    time_zero_summary = {
        "recommended_next_measurement": "record timing reference",
    }

    protocol = protocol_steps(design_rows, control_rows, time_zero_summary)
    schema = schema_rows()
    gates = acceptance_gates(protocol, schema)
    summary = summarize(
        protocol,
        schema,
        gates,
        {
            "satisfied_must_have_requirement_count": 0,
            "must_have_requirement_count": 5,
        },
    )

    protocol_axes = {row["requirement_axis"] for row in protocol}
    gate_lookup = {row["gate_key"]: row for row in gates}

    assert {"absolute_time_zero", "profile_spatial_calibration"}.issubset(protocol_axes)
    assert {"radius_seed_or_recovery", "cover_depth_recovery"}.issubset(protocol_axes)
    assert "absolute_amplitude_calibration" in protocol_axes
    assert gate_lookup["current_archive_field_fwi"]["ready"] is False
    assert summary["must_have_protocol_step_count"] == 6
    assert summary["ready_for_new_controlled_2d_acquisition"] is True
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["gpu_priority"] == "none"


def test_schema_contains_required_join_and_reference_fields():
    schema = schema_rows()
    required = {
        (row["table_name"], row["field_name"])
        for row in schema
        if row["required"] is True
    }

    assert ("session_log", "session_id") in required
    assert ("target_truth", "radius_mm") in required
    assert ("target_truth", "cover_depth_mm") in required
    assert ("profile_geometry", "trace_spacing_mm") in required
    assert ("reference_measurement", "measured_time_zero_ns") in required
    assert ("reference_measurement", "amplitude_repeatability_pct") in required
    assert ("acquisition_run", "reference_id_before") in required
