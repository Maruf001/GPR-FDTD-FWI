from run_gssi_field_controlled_acquisition_design import (
    build_design_rows,
    gate_rows,
    phase_rows,
    summarize_design,
)


def _blocker_rows():
    return [
        {
            "axis_key": "profile_spatial_calibration",
            "axis_family": "blocker",
            "ready": "False",
            "severity": "critical_blocker",
            "metric_label": "content residual range",
            "metric_value": "30.0",
            "metric_units": "mm",
            "evidence": "residual range=30 mm",
        },
        {
            "axis_key": "absolute_time_zero",
            "axis_family": "blocker",
            "ready": "False",
            "severity": "critical_blocker",
            "metric_label": "conservative half-width",
            "metric_value": "0.059",
            "metric_units": "ns",
            "evidence": "half-width=0.059 ns",
        },
        {
            "axis_key": "radius_seed_or_recovery",
            "axis_family": "blocker",
            "ready": "False",
            "severity": "critical_blocker",
            "metric_label": "weak radius sides",
            "metric_value": "4",
            "metric_units": "count",
            "evidence": "weak sides=4",
        },
        {
            "axis_key": "absolute_amplitude_calibration",
            "axis_family": "blocker",
            "ready": "False",
            "severity": "critical_blocker",
            "metric_label": "window-invariant combo fraction",
            "metric_value": "0.48",
            "metric_units": "fraction",
            "evidence": "all-supported combos=13/27",
        },
        {
            "axis_key": "cover_depth_recovery",
            "axis_family": "blocker",
            "ready": "False",
            "severity": "critical_blocker",
            "metric_label": "apparent depth max span",
            "metric_value": "149.9",
            "metric_units": "mm",
            "evidence": "span=149.9 mm",
        },
        {
            "axis_key": "field_fwi",
            "axis_family": "blocker",
            "ready": "False",
            "severity": "critical_blocker",
            "metric_label": "supported readiness gates",
            "metric_value": "2",
            "metric_units": "count",
            "evidence": "supported gates=2/8",
        },
        {
            "axis_key": "field_3d_hpc",
            "axis_family": "blocker",
            "ready": "False",
            "severity": "scope_blocker",
            "metric_label": "is 3D survey",
            "metric_value": "0",
            "metric_units": "boolean",
            "evidence": "independent 2D line profiles",
        },
    ]


def test_design_rows_convert_critical_blockers_to_acquisition_controls():
    rows = build_design_rows(_blocker_rows())
    by_axis = {row["axis_key"]: row for row in rows}
    phases = phase_rows(rows)
    summary = summarize_design(
        rows,
        {
            "critical_unresolved_blocker_count": 6,
            "is_3d_survey": False,
            "field_geometry_type": "independent_2d_line_profiles",
        },
    )

    assert by_axis["absolute_time_zero"]["priority"] == "must_have"
    assert "timing reference" in by_axis["absolute_time_zero"]["required_new_measurement"]
    assert by_axis["field_3d_hpc"]["priority"] == "blocked_out_of_scope"
    assert summary["must_have_requirement_count"] == 5
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["ready_for_new_controlled_2d_acquisition_design"] is True
    assert {row["phase"] for row in phases} >= {"geometry", "timing", "target_truth"}


def test_design_gates_keep_current_archive_heavy_work_blocked():
    rows = build_design_rows(_blocker_rows())
    summary = summarize_design(
        rows,
        {
            "critical_unresolved_blocker_count": 6,
            "is_3d_survey": False,
            "field_geometry_type": "independent_2d_line_profiles",
        },
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert gates["current_archive_field_fwi"]["ready"] is False
    assert gates["current_archive_heavy_field_work"]["ready"] is False
    assert gates["new_controlled_2d_acquisition_design"]["ready"] is True
    assert gates["field_3d_hpc"]["ready"] is False
