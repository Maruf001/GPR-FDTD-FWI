from run_gssi_field_controlled_2d_packet_validator import (
    acceptance_status_rows,
    summarize_validation,
    validate_cross_table_links,
    validate_required_rules,
)


def _rules():
    return [
        {"table_name": "session_log", "field_name": "session_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "session_log", "field_name": "dielectric_setting", "rule_key": "required_nonempty", "expected_dtype": "float", "severity": "blocking"},
        {"table_name": "target_truth", "field_name": "target_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "profile_geometry", "field_name": "profile_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "profile_geometry", "field_name": "session_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "acquisition_run", "field_name": "session_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "acquisition_run", "field_name": "profile_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "acquisition_run", "field_name": "target_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "acquisition_run", "field_name": "repeat_id", "rule_key": "required_nonempty", "expected_dtype": "integer", "severity": "blocking"},
        {"table_name": "acquisition_run", "field_name": "reference_id_before", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "acquisition_run", "field_name": "reference_id_after", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "reference_measurement", "field_name": "reference_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "reference_measurement", "field_name": "session_id", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "reference_measurement", "field_name": "reference_type", "rule_key": "required_nonempty", "expected_dtype": "string", "severity": "blocking"},
        {"table_name": "reference_measurement", "field_name": "measured_time_zero_ns", "rule_key": "required_nonempty", "expected_dtype": "float", "severity": "blocking"},
        {"table_name": "reference_measurement", "field_name": "time_zero_uncertainty_ns", "rule_key": "required_nonempty", "expected_dtype": "float", "severity": "blocking"},
        {"table_name": "reference_measurement", "field_name": "amplitude_metric", "rule_key": "required_nonempty", "expected_dtype": "float", "severity": "blocking"},
        {"table_name": "reference_measurement", "field_name": "amplitude_repeatability_pct", "rule_key": "required_nonempty", "expected_dtype": "float", "severity": "blocking"},
    ]


def _empty_tables():
    return {
        "session_log": [{"session_id": "", "dielectric_setting": ""}],
        "target_truth": [{"target_id": ""}],
        "profile_geometry": [{"profile_id": "", "session_id": ""}],
        "acquisition_run": [
            {
                "session_id": "",
                "profile_id": "",
                "target_id": "",
                "repeat_id": "",
                "reference_id_before": "",
                "reference_id_after": "",
            }
        ],
        "reference_measurement": [
            {
                "reference_id": "",
                "session_id": "",
                "reference_type": "",
                "measured_time_zero_ns": "",
                "time_zero_uncertainty_ns": "",
                "amplitude_metric": "",
                "amplitude_repeatability_pct": "",
            }
        ],
    }


def _valid_tables():
    refs = []
    for idx in range(1, 4):
        refs.append(
            {
                "reference_id": f"T0R{idx}",
                "session_id": "S1",
                "reference_type": "air_direct",
                "measured_time_zero_ns": "0.012",
                "time_zero_uncertainty_ns": "0.005",
                "amplitude_metric": "1.0",
                "amplitude_repeatability_pct": "5.0",
            }
        )
    for idx in range(1, 4):
        refs.append(
            {
                "reference_id": f"AR{idx}",
                "session_id": "S1",
                "reference_type": "amplitude_reflector",
                "measured_time_zero_ns": "0.012",
                "time_zero_uncertainty_ns": "0.005",
                "amplitude_metric": "1.0",
                "amplitude_repeatability_pct": "5.0",
            }
        )
    return {
        "session_log": [{"session_id": "S1", "dielectric_setting": "6.25"}],
        "target_truth": [{"target_id": "T1"}],
        "profile_geometry": [{"profile_id": "P1", "session_id": "S1"}],
        "acquisition_run": [
            {
                "session_id": "S1",
                "profile_id": "P1",
                "target_id": "T1",
                "repeat_id": str(idx),
                "reference_id_before": "T0R1",
                "reference_id_after": "AR1",
            }
            for idx in range(1, 4)
        ],
        "reference_measurement": refs,
    }


def test_blank_packet_fails_required_fields_and_acceptance():
    tables = _empty_tables()
    rules = _rules()
    findings = validate_required_rules(tables, rules) + validate_cross_table_links(tables)
    acceptance = acceptance_status_rows(tables, findings)
    summary = summarize_validation(tables, rules, findings, acceptance, "packet")

    assert summary["missing_required_value_count"] == len(rules)
    assert summary["ready_for_packet_acceptance"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert all(row["ready"] is False for row in acceptance)


def test_dtype_failure_is_reported_for_present_bad_float():
    tables = _empty_tables()
    tables["session_log"][0]["session_id"] = "S1"
    tables["session_log"][0]["dielectric_setting"] = "not-a-number"

    findings = validate_required_rules(tables, _rules())
    dtype_findings = [row for row in findings if row["check_key"] == "dtype_valid"]

    assert len(dtype_findings) == 1
    assert dtype_findings[0]["field_name"] == "dielectric_setting"


def test_cross_table_link_failure_is_blocking():
    tables = _valid_tables()
    tables["acquisition_run"][0]["target_id"] = "missing-target"

    findings = validate_cross_table_links(tables)

    assert len(findings) == 1
    assert findings[0]["check_key"] == "cross_table_link"
    assert findings[0]["field_name"] == "target_id"
    assert findings[0]["severity"] == "blocking"


def test_minimal_complete_packet_clears_acceptance_gates():
    tables = _valid_tables()
    rules = _rules()
    findings = validate_required_rules(tables, rules) + validate_cross_table_links(tables)
    acceptance = acceptance_status_rows(tables, findings)
    summary = summarize_validation(tables, rules, findings, acceptance, "packet")

    assert findings == []
    assert all(row["ready"] is True for row in acceptance)
    assert summary["ready_for_packet_acceptance"] is True
    assert summary["gpu_priority"] == "none"


def test_typed_reference_rows_only_require_relevant_measurement_fields():
    tables = _valid_tables()
    for row in tables["reference_measurement"]:
        if row["reference_type"] == "air_direct":
            row["amplitude_metric"] = ""
            row["amplitude_repeatability_pct"] = ""
        if row["reference_type"] == "amplitude_reflector":
            row["measured_time_zero_ns"] = ""
            row["time_zero_uncertainty_ns"] = ""

    rules = []
    for rule in _rules():
        updated = dict(rule)
        if updated["field_name"] in {"measured_time_zero_ns", "time_zero_uncertainty_ns"}:
            updated["required_reference_types"] = "air_direct,metal_plate_t0"
        if updated["field_name"] in {"amplitude_metric", "amplitude_repeatability_pct"}:
            updated["required_reference_types"] = "amplitude_reflector"
        rules.append(updated)

    findings = validate_required_rules(tables, rules) + validate_cross_table_links(tables)
    acceptance = acceptance_status_rows(tables, findings)
    summary = summarize_validation(tables, rules, findings, acceptance, "packet")

    assert findings == []
    assert all(row["ready"] is True for row in acceptance)
    assert summary["ready_for_packet_acceptance"] is True
