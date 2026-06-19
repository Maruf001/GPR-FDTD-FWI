from pathlib import Path

from run_gssi_field_controlled_2d_packet_builder import (
    build_templates,
    current_archive_prefill_limits,
    summarize_packet,
    validation_rules,
)


def _schema_rows():
    return [
        {
            "table_name": "session_log",
            "field_name": "session_id",
            "required": True,
            "dtype": "string",
            "units": "",
            "description": "session key",
        },
        {
            "table_name": "session_log",
            "field_name": "notes",
            "required": False,
            "dtype": "string",
            "units": "",
            "description": "notes",
        },
        {
            "table_name": "reference_measurement",
            "field_name": "measured_time_zero_ns",
            "required": True,
            "dtype": "float",
            "units": "ns",
            "description": "time zero",
        },
    ]


def _evidence_rows():
    return [
        {"evidence_key": "raw_file_inventory", "present": True},
        {"evidence_key": "parsed_profile_inventory", "present": True},
        {"evidence_key": "survey_geometry_metadata", "present": True},
        {"evidence_key": "short_anchor_spatial_consistency", "present": True},
        {"evidence_key": "radius_degeneracy_gates", "present": True},
        {"evidence_key": "inversion_blocker_map", "present": True},
        {"evidence_key": "time_zero_ladder", "present": True},
        {"evidence_key": "relative_signal_contrast_gates", "present": True},
    ]


def test_build_templates_splits_tables_and_keeps_optional_fields(tmp_path):
    template_index = build_templates(_schema_rows(), Path(tmp_path))
    by_table = {row["table_name"]: row for row in template_index}

    assert set(by_table) == {"session_log", "reference_measurement"}
    assert by_table["session_log"]["field_count"] == 2
    assert by_table["session_log"]["required_field_count"] == 1
    assert by_table["session_log"]["optional_field_count"] == 1
    assert Path(by_table["session_log"]["template_path"]).exists()
    assert "session_id,notes" in Path(by_table["session_log"]["template_path"]).read_text()


def test_validation_rules_only_block_on_required_fields():
    rules = validation_rules(_schema_rows())
    rule_keys = {(row["table_name"], row["field_name"]) for row in rules}
    by_key = {(row["table_name"], row["field_name"]): row for row in rules}

    assert len(rules) == 2
    assert ("session_log", "session_id") in rule_keys
    assert ("reference_measurement", "measured_time_zero_ns") in rule_keys
    assert by_key[("reference_measurement", "measured_time_zero_ns")]["required_reference_types"] == (
        "air_direct,metal_plate_t0"
    )
    assert by_key[("session_log", "session_id")]["required_reference_types"] == ""
    assert ("session_log", "notes") not in rule_keys
    assert all(row["severity"] == "blocking" for row in rules)


def test_packet_summary_keeps_current_archive_fwi_blocked():
    schema = _schema_rows()
    template_index = [
        {"table_name": "session_log"},
        {"table_name": "reference_measurement"},
    ]
    rules = validation_rules(schema)
    prefill_rows = current_archive_prefill_limits(_evidence_rows())
    summary = summarize_packet(
        template_index,
        rules,
        prefill_rows,
        {"required_metadata_field_count": 2, "acceptance_gate_count": 7},
        {"satisfied_must_have_requirement_count": 0, "must_have_requirement_count": 5},
    )
    prefill_by_table = {row["table_name"]: row for row in prefill_rows}

    assert prefill_by_table["session_log"]["current_archive_prefill_status"] == "partial"
    assert prefill_by_table["target_truth"]["current_archive_prefill_status"] == "blocked"
    assert prefill_by_table["reference_measurement"]["current_archive_prefill_status"] == "blocked"
    assert summary["ready_for_new_controlled_2d_acquisition"] is True
    assert summary["ready_for_packet_validation"] is True
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
