from run_gssi_field_current_archive_packet_prefill import (
    build_acquisition_run,
    build_packet,
    build_profile_geometry,
    build_session_log,
    dataset_date,
    prefill_status_rows,
)


def _fields():
    return {
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
        "target_truth": ["target_id", "material", "radius_mm"],
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
        "reference_measurement": ["reference_id", "session_id", "reference_type"],
    }


def _inventory_rows():
    return [
        {
            "file": "PROJECT001C__013.DZT",
            "antenna_name": "51600S",
            "dzx_system": "SIR4K",
            "dzx_software_version": "1.4.35",
            "dielectric": "2.25",
            "scan_spacing_m": "0.003333",
            "time_range_ns": "5.0",
        },
        {
            "file": "PROJECT001C__014.DZT",
            "antenna_name": "51600S",
            "dzx_system": "SIR4K",
            "dzx_software_version": "1.4.35",
            "dielectric": "2.25",
            "scan_spacing_m": "0.003333",
            "time_range_ns": "5.0",
        },
    ]


def _survey_rows():
    return [
        {"file": "PROJECT001C__013.DZT", "scan_spacing_m": "0.003333"},
        {"file": "PROJECT001C__014.DZT", "scan_spacing_m": "0.003333"},
    ]


def test_dataset_date_parses_dataset_id_suffix():
    assert dataset_date("local_gssi_51600s_2026_06_09") == "2026-06-09"
    assert dataset_date("no_date") == ""


def test_session_prefill_uses_consistent_archive_metadata_only():
    rows = build_session_log(_fields()["session_log"], _inventory_rows(), "local_gssi_51600s_2026_06_09")
    row = rows[0]

    assert row["dataset_id"] == "local_gssi_51600s_2026_06_09"
    assert row["date_utc"] == "2026-06-09"
    assert row["antenna_model"] == "51600S"
    assert row["system"] == "SIR4K"
    assert row["software_version"] == "1.4.35"
    assert row["dielectric_setting"] == "2.25"
    assert row["operator"] == ""
    assert row["gain_setting"] == ""


def test_profile_and_acquisition_prefill_leave_unsafe_controls_blank():
    profiles = build_profile_geometry(_fields()["profile_geometry"], _survey_rows())
    acquisitions = build_acquisition_run(_fields()["acquisition_run"], _inventory_rows())

    assert profiles[0]["profile_id"] == "PROJECT001C__013"
    assert profiles[0]["trace_spacing_mm"] == "3.333"
    assert profiles[0]["start_x_mm"] == ""
    assert profiles[0]["target_ids_crossed"] == ""
    assert acquisitions[0]["file_name"] == "PROJECT001C__013.DZT"
    assert acquisitions[0]["repeat_id"] == 1
    assert acquisitions[0]["target_id"] == ""
    assert acquisitions[0]["tx_rx_offset_mm"] == ""
    assert acquisitions[0]["reference_id_before"] == ""


def test_packet_prefill_status_keeps_target_and_reference_empty():
    packet = build_packet(
        _fields(),
        _inventory_rows(),
        _survey_rows(),
        "local_gssi_51600s_2026_06_09",
    )
    status = {row["table_name"]: row for row in prefill_status_rows(packet)}

    assert status["session_log"]["filled_row_count"] == 1
    assert status["profile_geometry"]["filled_row_count"] == 2
    assert status["acquisition_run"]["filled_row_count"] == 2
    assert status["target_truth"]["filled_row_count"] == 0
    assert status["reference_measurement"]["filled_row_count"] == 0
