from run_gssi_field_controlled_collection_handoff import (
    build_gate_handoff_rows,
    build_handoff_rows,
    build_packet_fill_map,
    summarize_handoff,
)


def _packet():
    return {
        "session_log": [
            {
                "session_id": "planned_controlled_2d_session_001",
                "date_utc": "",
                "operator": "",
            }
        ],
        "target_truth": [
            {
                "target_id": "T_CONTROL_001",
                "material": "",
                "center_x_mm": "",
                "radius_mm": "",
            }
        ],
        "profile_geometry": [
            {
                "profile_id": "P_CONTROL_001",
                "session_id": "planned_controlled_2d_session_001",
                "target_ids_crossed": "T_CONTROL_001",
                "start_x_mm": "",
                "end_x_mm": "",
            }
        ],
        "acquisition_run": [
            {
                "profile_id": "P_CONTROL_001",
                "repeat_id": str(idx),
                "target_id": "T_CONTROL_001",
                "tx_rx_offset_mm": "",
                "coupling_condition": "",
            }
            for idx in range(1, 4)
        ],
        "reference_measurement": [
            {
                "reference_id": f"T0_REF_{idx:03d}",
                "reference_type": "metal_plate_t0",
                "repeat_id": str(idx),
                "measured_time_zero_ns": "",
                "time_zero_uncertainty_ns": "",
                "file_name": "",
            }
            for idx in range(1, 4)
        ]
        + [
            {
                "reference_id": f"AMP_REF_{idx:03d}",
                "reference_type": "amplitude_reflector",
                "repeat_id": str(idx),
                "amplitude_metric": "",
                "amplitude_repeatability_pct": "",
                "file_name": "",
            }
            for idx in range(1, 4)
        ],
    }


def _action_rows():
    return [
        {
            "blocker_group": "target_truth_geometry",
            "priority": "1",
            "table_names": "target_truth",
            "field_names": "material,center_x_mm,radius_mm",
            "minimum_rows_or_repeats": "1",
            "missing_required_count": "3",
            "requires_new_controlled_data": "True",
            "current_archive_can_resolve": "False",
            "acceptance_gates_unblocked": "target_truth_controls,field_fwi_or_heavy_work",
            "action": "Measure target truth.",
        },
        {
            "blocker_group": "time_zero_reference",
            "priority": "2",
            "table_names": "reference_measurement",
            "field_names": "measured_time_zero_ns,time_zero_uncertainty_ns",
            "minimum_rows_or_repeats": "3",
            "missing_required_count": "6",
            "requires_new_controlled_data": "True",
            "current_archive_can_resolve": "False",
            "acceptance_gates_unblocked": "absolute_time_zero_references,field_fwi_or_heavy_work",
            "action": "Measure time-zero references.",
        },
        {
            "blocker_group": "amplitude_reference",
            "priority": "3",
            "table_names": "reference_measurement",
            "field_names": "amplitude_metric,amplitude_repeatability_pct",
            "minimum_rows_or_repeats": "3",
            "missing_required_count": "6",
            "requires_new_controlled_data": "True",
            "current_archive_can_resolve": "False",
            "acceptance_gates_unblocked": "amplitude_references,field_fwi_or_heavy_work",
            "action": "Measure amplitude references.",
        },
        {
            "blocker_group": "profile_target_geometry",
            "priority": "4",
            "table_names": "profile_geometry",
            "field_names": "start_x_mm,end_x_mm",
            "minimum_rows_or_repeats": "1",
            "missing_required_count": "2",
            "requires_new_controlled_data": "True",
            "current_archive_can_resolve": "False",
            "acceptance_gates_unblocked": "required_metadata_fields,cross_table_links,short_repeat_redundancy",
            "action": "Survey profile.",
        },
        {
            "blocker_group": "acquisition_control_links",
            "priority": "5",
            "table_names": "acquisition_run",
            "field_names": "tx_rx_offset_mm,coupling_condition",
            "minimum_rows_or_repeats": "3",
            "missing_required_count": "6",
            "requires_new_controlled_data": "True",
            "current_archive_can_resolve": "False",
            "acceptance_gates_unblocked": "required_metadata_fields,cross_table_links,short_repeat_redundancy",
            "action": "Record repeats.",
        },
        {
            "blocker_group": "session_metadata",
            "priority": "6",
            "table_names": "session_log",
            "field_names": "date_utc,operator",
            "minimum_rows_or_repeats": "1",
            "missing_required_count": "2",
            "requires_new_controlled_data": "False",
            "current_archive_can_resolve": "True",
            "acceptance_gates_unblocked": "required_metadata_fields",
            "action": "Verify session metadata.",
        },
    ]


def _gate_rows():
    return [
        {
            "gate_key": "target_truth_controls",
            "ready_now": "False",
            "highest_priority": "1",
            "required_blocker_groups": "target_truth_geometry",
            "current_evidence": "filled_target_truth_rows=1",
            "extra_requirement": "",
            "blocking_if_fail": "radius/depth validation",
        },
        {
            "gate_key": "absolute_time_zero_references",
            "ready_now": "False",
            "highest_priority": "2",
            "required_blocker_groups": "time_zero_reference",
            "current_evidence": "time_zero_reference_count=0",
            "extra_requirement": "reference_repeat_gate=3; uncertainty_gate_ns=0.02",
            "blocking_if_fail": "absolute time-zero",
        },
        {
            "gate_key": "amplitude_references",
            "ready_now": "False",
            "highest_priority": "3",
            "required_blocker_groups": "amplitude_reference",
            "current_evidence": "amplitude_reference_count=0",
            "extra_requirement": "",
            "blocking_if_fail": "amplitude calibration",
        },
        {
            "gate_key": "required_metadata_fields",
            "ready_now": "False",
            "highest_priority": "4",
            "required_blocker_groups": "profile_target_geometry,acquisition_control_links,session_metadata",
            "current_evidence": "missing_required=44",
            "extra_requirement": "",
            "blocking_if_fail": "packet acceptance",
        },
        {
            "gate_key": "cross_table_links",
            "ready_now": "False",
            "highest_priority": "4",
            "required_blocker_groups": "profile_target_geometry,acquisition_control_links",
            "current_evidence": "cross_table_failures=0",
            "extra_requirement": "",
            "blocking_if_fail": "profile/reference joins",
        },
        {
            "gate_key": "short_repeat_redundancy",
            "ready_now": "False",
            "highest_priority": "4",
            "required_blocker_groups": "profile_target_geometry,acquisition_control_links",
            "current_evidence": "targets_with_at_least_3_repeats=1",
            "extra_requirement": "",
            "blocking_if_fail": "repeatability",
        },
        {
            "gate_key": "field_fwi_or_heavy_work",
            "ready_now": "False",
            "highest_priority": "1",
            "required_blocker_groups": "target_truth_geometry,time_zero_reference,amplitude_reference",
            "current_evidence": "all_packet_gates_ready=False",
            "extra_requirement": "",
            "blocking_if_fail": "field FWI and heavy GPU work",
        },
    ]


def _findings():
    return [
        {
            "table_name": "session_log",
            "row_index": "1",
            "field_name": "operator",
            "check_key": "required_nonempty",
            "severity": "blocking",
            "passed": "False",
        },
        {
            "table_name": "target_truth",
            "row_index": "1",
            "field_name": "radius_mm",
            "check_key": "required_nonempty",
            "severity": "blocking",
            "passed": "False",
        },
        {
            "table_name": "reference_measurement",
            "row_index": "1",
            "field_name": "measured_time_zero_ns",
            "check_key": "required_nonempty",
            "severity": "blocking",
            "passed": "False",
        },
        {
            "table_name": "reference_measurement",
            "row_index": "4",
            "field_name": "amplitude_metric",
            "check_key": "required_nonempty",
            "severity": "blocking",
            "passed": "False",
        },
    ]


def test_handoff_rows_map_blockers_to_planned_packet_ids_and_gates():
    rows = build_handoff_rows(_action_rows(), _gate_rows(), _packet())
    by_group = {row["blocker_group"]: row for row in rows}

    assert by_group["target_truth_geometry"]["planned_ids_or_repeats"] == "T_CONTROL_001"
    assert "T0_REF_001" in by_group["time_zero_reference"]["planned_ids_or_repeats"]
    assert "AMP_REF_003" in by_group["amplitude_reference"]["planned_ids_or_repeats"]
    assert "repeat1" in by_group["acquisition_control_links"]["planned_ids_or_repeats"]
    assert "uncertainty_gate_ns=0.02" in by_group["time_zero_reference"]["gate_requirements"]
    assert by_group["session_metadata"]["current_archive_can_resolve"] is True


def test_packet_fill_map_classifies_missing_required_fields_into_blockers():
    rows = build_packet_fill_map(_packet(), _findings())
    by_table = {(row["table_name"], row["row_index"]): row for row in rows}

    assert by_table[("session_log", 1)]["blocker_groups"] == "session_metadata"
    assert by_table[("target_truth", 1)]["blocker_groups"] == "target_truth_geometry"
    assert by_table[("reference_measurement", 1)]["blocker_groups"] == "time_zero_reference"
    assert by_table[("reference_measurement", 4)]["blocker_groups"] == "amplitude_reference"


def test_handoff_summary_stays_collection_ready_but_blocks_field_fwi_and_gpu():
    handoff_rows = build_handoff_rows(_action_rows(), _gate_rows(), _packet())
    packet_rows = build_packet_fill_map(_packet(), _findings())
    gate_rows = build_gate_handoff_rows(_gate_rows())
    summary = summarize_handoff(
        handoff_rows,
        packet_rows,
        gate_rows,
        {
            "reference_repeat_gate": 3,
            "reference_uncertainty_gate_ns": 0.02,
            "reference_uncertainty_gate_depth_error_mm": 1.9986,
            "field_geometry_type": "independent_2d_line_profiles",
            "is_3d_survey": False,
            "ready_for_current_archive_field_qc_supplement": True,
        },
        {
            "missing_required_value_count": 44,
            "blocking_finding_count": 44,
            "ready_for_packet_acceptance": False,
        },
    )

    assert summary["critical_new_data_action_count"] == 5
    assert summary["packet_rows_needing_entry"] == 4
    assert summary["ready_for_collection_day"] is True
    assert summary["ready_for_packet_acceptance"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["ready_for_current_archive_heavy_field_work"] is False
    assert summary["ready_for_field_3d_hpc"] is False
    assert summary["gpu_priority"] == "none"
