from run_gssi_field_scaffold_validation_delta import (
    gate_delta_rows,
    parse_evidence,
    summarize_delta,
    table_delta_rows,
)


def test_parse_evidence_extracts_integer_pairs():
    assert parse_evidence("missing_required=67; dtype_failures=0") == {
        "missing_required": 67,
        "dtype_failures": 0,
    }
    assert parse_evidence("filled_target_truth_rows=1") == {"filled_target_truth_rows": 1}


def test_table_delta_counts_rows_and_missing_required_values():
    current = [
        {"table_name": "session_log", "row_count": "1", "filled_row_count": "1", "missing_required_count": "3", "cross_table_failure_count": "0"},
        {"table_name": "target_truth", "row_count": "1", "filled_row_count": "0", "missing_required_count": "10", "cross_table_failure_count": "0"},
    ]
    scaffold = [
        {"table_name": "session_log", "row_count": "1", "filled_row_count": "1", "missing_required_count": "6", "cross_table_failure_count": "0"},
        {"table_name": "target_truth", "row_count": "1", "filled_row_count": "1", "missing_required_count": "9", "cross_table_failure_count": "0"},
    ]

    rows = table_delta_rows(current, scaffold)
    by_table = {row["table_name"]: row for row in rows}

    assert by_table["target_truth"]["filled_row_delta"] == 1
    assert by_table["target_truth"]["missing_required_delta"] == -1
    assert by_table["session_log"]["missing_required_delta"] == 3


def test_gate_delta_and_summary_keep_inversion_blocked():
    current_gates = [
        {"gate_key": "target_truth_controls", "ready": "False", "evidence": "filled_target_truth_rows=0", "blocks_if_fail": "truth"},
        {"gate_key": "short_repeat_redundancy", "ready": "False", "evidence": "targets_with_at_least_3_repeats=0", "blocks_if_fail": "repeat"},
        {"gate_key": "absolute_time_zero_references", "ready": "False", "evidence": "time_zero_reference_count=0", "blocks_if_fail": "t0"},
        {"gate_key": "amplitude_references", "ready": "False", "evidence": "amplitude_reference_count=0", "blocks_if_fail": "amp"},
    ]
    scaffold_gates = [
        {"gate_key": "target_truth_controls", "ready": "False", "evidence": "filled_target_truth_rows=1", "blocks_if_fail": "truth"},
        {"gate_key": "short_repeat_redundancy", "ready": "False", "evidence": "targets_with_at_least_3_repeats=1", "blocks_if_fail": "repeat"},
        {"gate_key": "absolute_time_zero_references", "ready": "False", "evidence": "time_zero_reference_count=0", "blocks_if_fail": "t0"},
        {"gate_key": "amplitude_references", "ready": "False", "evidence": "amplitude_reference_count=0", "blocks_if_fail": "amp"},
    ]
    gates = gate_delta_rows(current_gates, scaffold_gates)
    summary = summarize_delta(
        {"total_row_count": 11, "filled_row_count": 9, "missing_required_value_count": 67, "cross_table_failure_count": 0},
        {"total_row_count": 12, "filled_row_count": 12, "missing_required_value_count": 60, "cross_table_failure_count": 0},
        {"planned_time_zero_reference_count": 3, "planned_amplitude_reference_count": 3, "ready_for_collection": True},
        [],
        gates,
    )

    by_gate = {row["gate_key"]: row for row in gates}
    assert by_gate["target_truth_controls"]["evidence_delta"] == "filled_target_truth_rows:0->1"
    assert summary["missing_required_delta"] == -7
    assert summary["filled_row_delta"] == 3
    assert summary["current_ready_gate_count"] == 0
    assert summary["scaffold_ready_gate_count"] == 0
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
