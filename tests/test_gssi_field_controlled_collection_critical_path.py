from run_gssi_field_controlled_collection_critical_path import (
    build_action_rows,
    build_gate_rows,
    build_phase_rows,
    parse_gate_status,
    summarize,
)


def test_parse_gate_status_extracts_gate_keys():
    assert parse_gate_status("a=blocked; b=ready") == ["a", "b"]


def test_critical_path_keeps_current_archive_from_unblocking_field_gates():
    handoff_rows = [
        {
            "priority": 1,
            "collection_phase": "target_truth",
            "blocker_group": "target_truth_geometry",
            "planned_ids_or_repeats": "T_CONTROL_001",
            "minimum_rows_or_repeats": 1,
            "missing_required_count": 9,
            "acceptance_gate_status": "target_truth_controls=blocked; field_fwi_or_heavy_work=blocked",
            "requires_new_controlled_data": True,
            "current_archive_can_resolve": False,
            "done_when": "target truth is filled",
        },
        {
            "priority": 6,
            "collection_phase": "session_metadata",
            "blocker_group": "session_metadata",
            "planned_ids_or_repeats": "session",
            "minimum_rows_or_repeats": 1,
            "missing_required_count": 2,
            "acceptance_gate_status": "required_metadata_fields=blocked",
            "requires_new_controlled_data": False,
            "current_archive_can_resolve": True,
            "done_when": "metadata is verified",
        },
    ]
    source_gate_rows = [
        {
            "gate_key": "field_fwi_or_heavy_work",
            "ready_now": False,
            "highest_priority": 1,
            "required_blocker_groups": "target_truth_geometry",
            "blocks_if_fail": "field FWI",
        },
        {
            "gate_key": "required_metadata_fields",
            "ready_now": False,
            "highest_priority": 6,
            "required_blocker_groups": "session_metadata",
            "blocks_if_fail": "packet acceptance",
        },
    ]
    packet_rows = [{"fill_status": "needs_collection_entry"}, {"fill_status": "complete_for_required_fields"}]

    actions = build_action_rows(handoff_rows)
    gates = build_gate_rows(source_gate_rows, actions)
    phases = build_phase_rows(actions)
    summary = summarize(
        {
            "policy_label": "handoff",
            "critical_new_data_action_count": 1,
            "missing_required_value_count": 11,
            "ready_for_collection_day": True,
            "ready_for_packet_acceptance": False,
            "ready_for_current_archive_field_qc_supplement": True,
            "ready_for_current_archive_field_fwi": False,
            "ready_for_current_archive_heavy_field_work": False,
            "ready_for_field_3d_hpc": False,
        },
        actions,
        gates,
        phases,
        packet_rows,
    )

    gate_by_key = {row["gate_key"]: row for row in gates}
    assert gate_by_key["field_fwi_or_heavy_work"]["current_archive_can_unblock"] is False
    assert gate_by_key["field_fwi_or_heavy_work"]["requires_new_controlled_data"] is True
    assert gate_by_key["required_metadata_fields"]["current_archive_can_unblock"] is True
    assert summary["ready_for_collection_execution"] is True
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["ready_for_gpu_work"] is False
    assert summary["packet_rows_needing_entry"] == 1
