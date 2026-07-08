from pathlib import Path

from run_gssi_field_current_archive_metadata_recovery import (
    consistent_value,
    parse_dzx_recovery_metadata,
    recover_session_metadata,
    summarize_recovery,
)


def write_dzx(path: Path, serial="3385", gain="0"):
    path.write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<DZX xmlns="www.geophysical.com/DZX/1.020000">
  <DataCollection>
    <system>SIR4K</system>
    <softwareVersion>1.4.35</softwareVersion>
    <displayGain>{gain}</displayGain>
    <antSerialNumber>{serial}</antSerialNumber>
    <antModelNumber>70</antModelNumber>
  </DataCollection>
</DZX>
""",
        encoding="utf-8",
    )


def test_parse_dzx_recovery_metadata_reads_serial_and_display_gain(tmp_path):
    dzx = tmp_path / "PROJECT001C__013.DZX"
    write_dzx(dzx)

    row = parse_dzx_recovery_metadata(dzx)

    assert row["file_name"] == "PROJECT001C__013.DZT"
    assert row["antSerialNumber"] == "3385"
    assert row["displayGain"] == "0"
    assert row["system"] == "SIR4K"


def test_consistent_value_rejects_conflicting_values():
    value, consistent, count = consistent_value(
        [{"displayGain": "0"}, {"displayGain": "1"}],
        "displayGain",
    )

    assert value == ""
    assert consistent is False
    assert count == 2


def test_recover_session_metadata_applies_only_blank_consistent_fields():
    packet = {
        "session_log": [
            {
                "session_id": "s1",
                "antenna_serial": "",
                "gain_setting": "",
                "operator": "",
                "notes": "prefill",
            }
        ],
        "target_truth": [],
        "profile_geometry": [],
        "acquisition_run": [],
        "reference_measurement": [],
    }
    dzx_rows = [
        {"antSerialNumber": "3385", "displayGain": "0"},
        {"antSerialNumber": "3385", "displayGain": "0"},
    ]

    recovered, evidence = recover_session_metadata(packet, dzx_rows)

    session = recovered["session_log"][0]
    assert session["antenna_serial"] == "3385"
    assert session["gain_setting"] == "0"
    assert session["operator"] == ""
    assert sum(row["applied"] for row in evidence) == 2


def test_summarize_recovery_keeps_field_fwi_blocked():
    evidence = [
        {"source_tag": "antSerialNumber", "applied": True},
        {"source_tag": "displayGain", "applied": True},
        {"source_tag": "", "applied": False},
    ]
    before_summary = {"missing_required_value_count": 67}
    after_summary = {
        "missing_required_value_count": 65,
        "dtype_failure_count": 0,
        "cross_table_failure_count": 0,
        "acceptance_gate_count": 7,
        "ready_for_packet_acceptance": False,
    }
    before_status = [{"table_name": "session_log", "missing_required_count": 3}]
    after_status = [{"table_name": "session_log", "missing_required_count": 1}]
    for table in ("target_truth", "profile_geometry", "acquisition_run", "reference_measurement"):
        before_status.append({"table_name": table, "missing_required_count": 0})
        after_status.append({"table_name": table, "missing_required_count": 0})

    summary = summarize_recovery(evidence, before_summary, after_summary, before_status, after_status, [{}, {}])

    assert summary["applied_recovered_field_count"] == 2
    assert summary["missing_required_delta"] == -2
    assert summary["session_missing_required_delta"] == -2
    assert summary["ready_for_packet_acceptance"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
