import math

import pandas as pd

import run_local_2d_field_holistic_report as report


def test_parse_run_id_accepts_numbered_output_names():
    assert report.parse_run_id("1358_local2d_fixed_radius_locking") == 1358
    assert report.parse_run_id("001_gssi51600s_status") == 1
    assert report.parse_run_id("_by_category_symlinks") is None
    assert report.parse_run_id("field_index.md") is None


def test_synthetic_phase_classification_marks_locking_endpoint():
    assert (
        report.classify_recent_synthetic_phase(1358, "local2d_fixed_radius_locking")
        == "1357-1358 fixed-radius locking validation endpoint"
    )
    assert (
        report.classify_recent_synthetic_phase(1326, "local2d_detector_baseline")
        == "1326-1338 local detector baselines and sampling boundary"
    )


def test_field_phase_classification_marks_controlled_collection_checkpoint():
    assert (
        report.classify_field_phase(156, "gssi51600s_controlled_collection_critical_path")
        == "137-156 controlled 2D collection packet and critical path"
    )
    assert (
        report.classify_field_phase(119, "gssi51600s_field_time_zero_evidence_ladder")
        == "119-136 short-anchor inversion-readiness blockers"
    )


def test_state_linf_mm_covers_x_z_and_radius():
    state = {
        "x_values_mm": [190.0, 251.0, 265.0],
        "z_values_mm": [90.0, 89.0, 91.0],
        "radii_mm": [5.0, 6.0, 8.0],
    }
    value = report.state_linf_mm(
        state,
        truth_x=[190.0, 250.0, 264.0],
        truth_z=[90.0, 90.0, 90.0],
        truth_r=[5.0, 6.0, 8.0],
    )
    assert math.isclose(value, 1.0)


def test_phase_summary_preserves_first_last_and_manifest_count():
    df = pd.DataFrame(
        [
            {"run_id": 1200, "phase": "a", "has_manifest": True},
            {"run_id": 1201, "phase": "a", "has_manifest": False},
            {"run_id": 1358, "phase": "b", "has_manifest": True},
        ]
    )
    summary = report.phase_summary(df)
    row_a = summary[summary["phase"] == "a"].iloc[0]
    row_b = summary[summary["phase"] == "b"].iloc[0]

    assert row_a["first_run"] == 1200
    assert row_a["last_run"] == 1201
    assert row_a["run_count"] == 2
    assert row_a["manifest_count"] == 1
    assert row_b["first_run"] == 1358


def test_md_table_escapes_pipes_and_limits_rows():
    df = pd.DataFrame(
        [
            {"name": "a|b", "value": 1.23456},
            {"name": "c", "value": 0.0001234},
        ]
    )
    table = report.md_table(df, [("name", "Name"), ("value", "Value")], max_rows=1)

    assert "a\\|b" in table
    assert "1.235" in table
    assert "1 more rows omitted" in table
