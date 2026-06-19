from run_modern_ringdown050_exception_status import (
    build_exception_rows,
    classify_exception_status,
    parse_run_ids,
    summarize_status,
)


def test_parse_run_ids_handles_empty_and_csv_values():
    assert parse_run_ids("") == []
    assert parse_run_ids("1136, 785") == [1136, 785]


def test_classify_exception_status_marks_closed_modern_followup():
    triage_by_id = {
        1136: {
            "run_id": "1136",
            "ringdown_value": "0.5",
            "classification": "near_threshold_modern_exception_monitor",
        }
    }
    closure = {
        "policy_label": "target0_exception_closed_by_source_density",
        "run_ids": "1136,1137,1138,1139,1140",
    }

    status = classify_exception_status(1136, triage_by_id, closure)

    assert status["exception_status"] == "closed_by_existing_source_density_followup"
    assert status["gpu_priority"] == "none"


def test_classify_exception_status_marks_legacy_archive_low_priority():
    triage_by_id = {
        785: {
            "run_id": "785",
            "ringdown_value": "0.25",
            "classification": "legacy_archive_exception_no_gpu_priority",
        }
    }

    status = classify_exception_status(785, triage_by_id, {"policy_label": "", "run_ids": ""})

    assert status["exception_status"] == "legacy_archive_no_gpu_priority"
    assert status["gpu_priority"] == "none"


def test_build_exception_rows_includes_no_exception_target():
    secondary = {
        "target_policy_rows": [
            {
                "target": 0,
                "target_label": "target0",
                "strongest_secondary_nonaccepted_run_ids": "1136",
                "strongest_secondary_objective": "highband",
                "strongest_secondary_accepted_fraction": 0.97,
            },
            {
                "target": 2,
                "target_label": "target2",
                "strongest_secondary_nonaccepted_run_ids": "",
                "strongest_secondary_objective": "late_high",
                "strongest_secondary_accepted_fraction": 1.0,
            },
        ]
    }
    triage = [
        {
            "run_id": "1136",
            "ringdown_value": "0.5",
            "classification": "near_threshold_modern_exception_monitor",
        }
    ]
    closure = {
        "policy_label": "target0_exception_closed_by_source_density",
        "run_ids": "1136,1137",
    }

    rows = build_exception_rows(secondary, triage, closure)

    assert rows[0]["exception_status"] == "closed_by_existing_source_density_followup"
    assert rows[1]["exception_status"] == "no_secondary_exception"


def test_summarize_status_reports_no_open_modern_exception():
    rows = [
        {"run_id": 1136, "ringdown_value": 0.5, "exception_status": "closed_by_existing_source_density_followup"},
        {"run_id": 785, "ringdown_value": 0.25, "exception_status": "legacy_archive_no_gpu_priority"},
        {"run_id": "", "ringdown_value": "", "exception_status": "no_secondary_exception"},
    ]

    summary = summarize_status(rows)

    assert summary["policy_label"] == "modern_ringdown050_no_open_exception_gpu_priority_none"
    assert summary["modern_ringdown050_exception_count"] == 1
    assert summary["modern_ringdown050_closed_count"] == 1
    assert summary["modern_ringdown050_open_count"] == 0
    assert summary["gpu_priority"] == "none"
