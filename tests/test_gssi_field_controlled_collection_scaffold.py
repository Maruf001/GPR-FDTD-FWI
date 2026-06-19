from run_gssi_field_controlled_collection_scaffold import (
    build_scaffold_tables,
    collection_task_rows,
    scaffold_status_rows,
    summarize_scaffold,
)


FIELDS_BY_TABLE = {
    "session_log": [
        "dataset_id",
        "session_id",
        "date_utc",
        "operator",
        "antenna_model",
        "antenna_serial",
        "system",
        "software_version",
        "gain_setting",
        "dielectric_setting",
        "scan_spacing_m",
        "time_range_ns",
        "weather",
        "notes",
    ],
    "target_truth": [
        "target_id",
        "material",
        "center_x_mm",
        "center_y_mm",
        "cover_depth_mm",
        "diameter_mm",
        "radius_mm",
        "dielectric_epsr",
        "velocity_m_per_ns",
        "measurement_uncertainty_mm",
        "truth_source",
    ],
    "profile_geometry": [
        "profile_id",
        "session_id",
        "profile_role",
        "start_x_mm",
        "start_y_mm",
        "end_x_mm",
        "end_y_mm",
        "scan_direction",
        "trace_spacing_mm",
        "target_ids_crossed",
        "survey_method",
    ],
    "acquisition_run": [
        "file_name",
        "session_id",
        "profile_id",
        "repeat_id",
        "target_id",
        "tx_rx_offset_mm",
        "coupling_condition",
        "reference_id_before",
        "reference_id_after",
        "notes",
    ],
    "reference_measurement": [
        "reference_id",
        "session_id",
        "reference_type",
        "before_after",
        "file_name",
        "repeat_id",
        "measured_time_zero_ns",
        "time_zero_uncertainty_ns",
        "amplitude_metric",
        "amplitude_repeatability_pct",
        "expected_response",
    ],
}


def _action_rows():
    return [
        {
            "priority": "1",
            "blocker_group": "target_truth_geometry",
            "action_type": "new_controlled_measurement",
            "minimum_rows_or_repeats": "1",
            "reference_uncertainty_gate_ns": "",
            "reference_depth_equivalent_mm": "",
            "field_names": "target_id,radius_mm",
            "requires_new_controlled_data": "True",
            "action": "measure target",
        },
        {
            "priority": "2",
            "blocker_group": "time_zero_reference",
            "action_type": "new_reference_measurement",
            "minimum_rows_or_repeats": "3",
            "reference_uncertainty_gate_ns": "0.02",
            "reference_depth_equivalent_mm": "1.99",
            "field_names": "measured_time_zero_ns,time_zero_uncertainty_ns",
            "requires_new_controlled_data": "True",
            "action": "measure t0",
        },
        {
            "priority": "6",
            "blocker_group": "session_metadata",
            "action_type": "recover_or_recollect_metadata",
            "minimum_rows_or_repeats": "1",
            "reference_uncertainty_gate_ns": "",
            "reference_depth_equivalent_mm": "",
            "field_names": "operator",
            "requires_new_controlled_data": "False",
            "action": "recover notes",
        },
    ]


def test_scaffold_tables_create_planned_ids_but_leave_measurements_blank():
    tables = build_scaffold_tables(FIELDS_BY_TABLE, dataset_id="dataset", reference_repeat_gate=3)

    assert len(tables["acquisition_run"]) == 3
    assert len(tables["reference_measurement"]) == 6
    assert tables["target_truth"][0]["target_id"] == "T_CONTROL_001"
    assert tables["target_truth"][0]["radius_mm"] == ""
    assert tables["reference_measurement"][0]["measured_time_zero_ns"] == ""
    assert tables["acquisition_run"][0]["reference_id_before"] == "T0_REF_001"
    assert tables["acquisition_run"][0]["reference_id_after"] == "AMP_REF_001"


def test_task_rows_map_action_groups_to_planned_ids():
    tables = build_scaffold_tables(FIELDS_BY_TABLE, dataset_id="dataset", reference_repeat_gate=3)
    tasks = collection_task_rows(_action_rows(), tables)
    by_group = {row["blocker_group"]: row for row in tasks}

    assert by_group["target_truth_geometry"]["planned_ids_or_repeats"] == "T_CONTROL_001"
    assert "T0_REF_001" in by_group["time_zero_reference"]["planned_ids_or_repeats"]
    assert by_group["session_metadata"]["requires_new_controlled_data"] is False


def test_summary_marks_scaffold_collection_ready_but_validation_not_ready():
    tables = build_scaffold_tables(FIELDS_BY_TABLE, dataset_id="dataset", reference_repeat_gate=3)
    status = scaffold_status_rows(tables)
    tasks = collection_task_rows(_action_rows(), tables)
    summary = summarize_scaffold(
        tables,
        status,
        tasks,
        {
            "reference_repeat_gate": 3,
            "reference_uncertainty_gate_ns": 0.02,
            "reference_uncertainty_gate_depth_error_mm": 1.99,
        },
    )

    assert summary["planned_acquisition_repeat_count"] == 3
    assert summary["planned_time_zero_reference_count"] == 3
    assert summary["planned_amplitude_reference_count"] == 3
    assert summary["measured_or_session_blank_count"] > 0
    assert summary["ready_for_collection"] is True
    assert summary["validator_expected_to_pass"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
