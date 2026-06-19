from run_gssi_field_recovered_session_collection_scaffold import (
    apply_recovered_session_metadata,
    recoverable_session_values,
    summarize_recovered_scaffold,
)


def scaffold_packet():
    return {
        "session_log": [
            {
                "session_id": "planned",
                "antenna_serial": "",
                "software_version": "",
                "gain_setting": "",
                "time_range_ns": "",
                "notes": "planned",
            }
        ],
        "target_truth": [],
        "profile_geometry": [],
        "acquisition_run": [],
        "reference_measurement": [],
    }


def recovered_packet():
    return {
        "session_log": [
            {
                "session_id": "archive",
                "antenna_serial": "3385",
                "software_version": "1.4.35",
                "gain_setting": "0",
                "time_range_ns": "5.0",
            }
        ],
        "target_truth": [],
        "profile_geometry": [],
        "acquisition_run": [],
        "reference_measurement": [],
    }


def status_rows(session_missing):
    rows = [{"table_name": "session_log", "missing_required_count": session_missing}]
    for table in ("target_truth", "profile_geometry", "acquisition_run", "reference_measurement"):
        rows.append({"table_name": table, "missing_required_count": 0})
    return rows


def test_recoverable_session_values_uses_nonempty_allowed_fields():
    values = recoverable_session_values(recovered_packet())

    assert values == {
        "antenna_serial": "3385",
        "software_version": "1.4.35",
        "gain_setting": "0",
        "time_range_ns": "5.0",
    }


def test_apply_recovered_session_metadata_fills_blank_scaffold_fields():
    updated, evidence = apply_recovered_session_metadata(scaffold_packet(), recovered_packet())

    session = updated["session_log"][0]
    assert session["antenna_serial"] == "3385"
    assert session["software_version"] == "1.4.35"
    assert session["gain_setting"] == "0"
    assert session["time_range_ns"] == "5.0"
    assert sum(row["applied"] for row in evidence) == 4
    assert "verify/update" in session["notes"]


def test_apply_recovered_session_metadata_does_not_overwrite_existing_values():
    packet = scaffold_packet()
    packet["session_log"][0]["gain_setting"] = "manual"

    updated, evidence = apply_recovered_session_metadata(packet, recovered_packet())

    assert updated["session_log"][0]["gain_setting"] == "manual"
    gain_evidence = next(row for row in evidence if row["field_name"] == "gain_setting")
    assert gain_evidence["applied"] is False


def test_summarize_recovered_scaffold_keeps_field_fwi_blocked():
    evidence = [
        {"applied": True},
        {"applied": True},
        {"applied": True},
        {"applied": True},
    ]
    summary = summarize_recovered_scaffold(
        evidence,
        {"missing_required_value_count": 60},
        {
            "missing_required_value_count": 56,
            "dtype_failure_count": 0,
            "cross_table_failure_count": 0,
            "ready_for_packet_acceptance": False,
        },
        status_rows(6),
        status_rows(2),
    )

    assert summary["applied_session_prefill_field_count"] == 4
    assert summary["missing_required_delta"] == -4
    assert summary["session_missing_required_delta"] == -4
    assert summary["ready_for_collection"] is True
    assert summary["ready_for_packet_acceptance"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
