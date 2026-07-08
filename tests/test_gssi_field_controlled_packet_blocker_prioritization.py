from run_gssi_field_controlled_packet_blocker_prioritization import (
    action_group_rows,
    classify_blocker,
    enrich_blocker_rows,
    gate_action_rows,
    summarize_prioritization,
)


def _finding(table, field, row=1):
    return {
        "table_name": table,
        "row_index": str(row),
        "field_name": field,
        "check_key": "required_nonempty",
        "severity": "blocking",
        "passed": "False",
        "expected": "non-empty value",
        "message": f"{table}.{field} is required",
    }


def test_classify_blockers_maps_reference_fields_to_specific_actions():
    assert classify_blocker("target_truth", "radius_mm") == "target_truth_geometry"
    assert classify_blocker("reference_measurement", "measured_time_zero_ns") == "time_zero_reference"
    assert classify_blocker("reference_measurement", "amplitude_metric") == "amplitude_reference"
    assert classify_blocker("reference_measurement", "reference_id") == "reference_registry"
    assert classify_blocker("session_log", "operator") == "session_metadata"


def test_action_groups_include_reference_requirement_gate():
    findings = [
        _finding("target_truth", "target_id"),
        _finding("reference_measurement", "measured_time_zero_ns"),
        _finding("reference_measurement", "amplitude_metric"),
        _finding("session_log", "operator"),
    ]
    blockers = enrich_blocker_rows(findings)
    actions = action_group_rows(
        blockers,
        {
            "reference_repeat_gate": 3,
            "reference_uncertainty_gate_ns": 0.02,
            "reference_uncertainty_gate_depth_error_mm": 1.99,
        },
    )
    by_group = {row["blocker_group"]: row for row in actions}

    assert by_group["target_truth_geometry"]["priority"] == 1
    assert by_group["time_zero_reference"]["minimum_rows_or_repeats"] == 3
    assert by_group["time_zero_reference"]["reference_uncertainty_gate_ns"] == 0.02
    assert by_group["session_metadata"]["current_archive_can_resolve"] is True
    assert by_group["target_truth_geometry"]["requires_new_controlled_data"] is True


def test_gate_rows_and_summary_keep_field_fwi_blocked():
    findings = [
        _finding("target_truth", "target_id"),
        _finding("reference_measurement", "measured_time_zero_ns"),
        _finding("reference_measurement", "amplitude_metric"),
    ]
    blockers = enrich_blocker_rows(findings)
    reference = {"reference_repeat_gate": 3, "reference_uncertainty_gate_ns": 0.02}
    actions = action_group_rows(blockers, reference)
    gates = gate_action_rows(
        [
            {"gate_key": "target_truth_controls", "ready": "False", "evidence": "filled_target_truth_rows=0", "blocks_if_fail": "truth"},
            {"gate_key": "absolute_time_zero_references", "ready": "False", "evidence": "time_zero_reference_count=0", "blocks_if_fail": "time zero"},
        ],
        actions,
        reference,
    )
    summary = summarize_prioritization(
        blockers,
        actions,
        gates,
        {"blocking_finding_count": 3, "missing_required_value_count": 3},
        reference,
    )

    assert gates[1]["extra_requirement"] == "reference_repeat_gate=3; uncertainty_gate_ns=0.02"
    assert summary["failed_acceptance_gate_count"] == 2
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["ready_for_new_controlled_2d_acquisition"] is True
    assert summary["gpu_priority"] == "none"
