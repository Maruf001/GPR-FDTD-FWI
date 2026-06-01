"""Tests for staged variable-radius pipeline summaries."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_variable_radius_staged_pipeline_summary import (  # noqa: E402
    coordinate_confidence_metrics,
    focus_policy,
    max_abs_error,
    parse_case_spec,
    stage_rows,
    summarize_case,
    truth_tuple_rank,
)


def _write(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


def test_parse_case_spec_requires_five_parts():
    spec = parse_case_spec("seed|det.json|loc.json|focus.json|joint.json")

    assert spec["label"] == "seed"
    assert spec["joint_json"] == "joint.json"
    assert spec["focused_refinement_json"] is None

    refined = parse_case_spec("seed|det.json|loc.json|focus.json|joint.json|refined.json")

    assert refined["focused_refinement_json"] == "refined.json"

    with pytest.raises(Exception, match="case spec"):
        parse_case_spec("seed|det.json")


def test_max_abs_error_returns_largest_component():
    assert max_abs_error([1.0, 3.0], [2.0, 0.0]) == 3.0


def test_truth_tuple_rank_finds_tuple_in_ranked_rows():
    rows = [
        {"radii_mm": [5.5, 6.0, 8.0]},
        {"radii_mm": [5.0, 6.0, 8.0]},
    ]

    assert truth_tuple_rank(rows, [5.0, 6.0, 8.0]) == 2


def test_coordinate_confidence_metrics_counts_x_ambiguity_and_truth():
    summary = {
        "sources": 7,
        "tx_rx_offset_mm": 40.0,
        "frequency_ghz": 1.5,
        "confidence_rows": [
            {
                "step_target_index": 2,
                "best_x_mm": 310.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 8.0,
                "ambiguity_x_min_mm": 310.0,
                "ambiguity_x_max_mm": 310.0,
            },
            {
                "step_target_index": 2,
                "best_x_mm": 309.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 8.0,
                "ambiguity_x_min_mm": 309.0,
                "ambiguity_x_max_mm": 310.0,
            },
        ],
    }

    metrics = coordinate_confidence_metrics(
        summary,
        [190.0, 250.0, 310.0],
        [90.0, 90.0, 90.0],
        [5.0, 6.0, 8.0],
    )

    assert metrics["sources"] == 7
    assert metrics["tx_rx_offset_mm"] == 40.0
    assert metrics["frequency_ghz"] == 1.5
    assert metrics["row_count"] == 2
    assert metrics["truth_geometry_count"] == 1
    assert metrics["x_ambiguity_row_count"] == 1
    assert metrics["x_ambiguity_width_max_mm"] == 1.0


def test_focus_policy_prefers_refined_point_when_standard_is_interval():
    standard = {"x_ambiguity_row_count": 1}
    refined = {"x_ambiguity_row_count": 0}

    assert focus_policy(standard, refined) == "use_refined_focus_for_point_x"
    assert focus_policy(standard) == "report_focused_x_interval"
    assert focus_policy({"x_ambiguity_row_count": 0}) == "standard_focus_point_ok"


def test_summarize_case_builds_stage_errors(tmp_path):
    detection = {
        "truth_x_values_mm": [190.0, 250.0, 310.0],
        "truth_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
    }
    location = {
        "sources": 5,
        "tx_rx_offset_mm": 20.0,
        "frequency_ghz": 1.5,
        "final_state": {
            "x_values_mm": [190.0, 250.0, 310.0],
            "z_values_mm": [90.0, 90.0, 85.0],
            "radii_mm": [6.0, 6.0, 6.0],
        }
    }
    focused = {
        "sources": 5,
        "tx_rx_offset_mm": 20.0,
        "frequency_ghz": 1.5,
        "final_state": {
            "x_values_mm": [190.0, 250.0, 310.0],
            "z_values_mm": [90.0, 90.0, 90.0],
            "radii_mm": [6.0, 6.0, 8.0],
        },
        "confidence_rows": [
            {
                "step_target_index": 2,
                "best_x_mm": 310.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 8.0,
                "ambiguity_x_min_mm": 309.0,
                "ambiguity_x_max_mm": 310.0,
            }
        ],
    }
    refined = {
        "sources": 7,
        "tx_rx_offset_mm": 40.0,
        "frequency_ghz": 1.5,
        "final_state": {
            "x_values_mm": [190.0, 250.0, 310.0],
            "z_values_mm": [90.0, 90.0, 90.0],
            "radii_mm": [6.0, 6.0, 8.0],
        },
        "confidence_rows": [
            {
                "step_target_index": 2,
                "best_x_mm": 310.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 8.0,
                "ambiguity_x_min_mm": 310.0,
                "ambiguity_x_max_mm": 310.0,
            }
        ],
    }
    joint = {
        "update_case_label": "case",
        "sources": 5,
        "tx_rx_offset_mm": 20.0,
        "frequency_ghz": 1.5,
        "candidate_x_values_mm": [190.0, 250.0, 310.0],
        "candidate_z_values_mm": [90.0, 90.0, 90.0],
        "ranked_by_case": {
            "case": [
                {"radii_mm": [5.0, 6.0, 8.0], "misfit": 0.1},
                {"radii_mm": [5.5, 6.0, 8.0], "misfit": 0.13},
            ],
        },
    }
    case = {
        "label": "seed",
        "detection_json": _write(tmp_path / "det.json", detection),
        "location_json": _write(tmp_path / "loc.json", location),
        "focused_json": _write(tmp_path / "focus.json", focused),
        "joint_json": _write(tmp_path / "joint.json", joint),
        "focused_refinement_json": _write(tmp_path / "refined.json", refined),
    }

    summary = summarize_case(case)

    assert summary["location_max_z_error_mm"] == 5.0
    assert summary["focused_max_radius_error_mm"] == 1.0
    assert summary["joint_max_radius_error_mm"] == 0.0
    assert summary["joint_truth_tuple_rank_in_top"] == 1
    assert summary["joint_next_radius_values_mm"] == [5.5, 6.0, 8.0]
    assert summary["joint_margin_abs"] == pytest.approx(0.03)
    assert summary["joint_margin_rel"] == pytest.approx(0.3)
    assert summary["location_tx_rx_offset_mm"] == 20.0
    assert summary["focused_sources"] == 5
    assert summary["focused_tx_rx_offset_mm"] == 20.0
    assert summary["focused_frequency_ghz"] == 1.5
    assert summary["focused_x_ambiguity_row_count"] == 1
    assert summary["refined_focused_sources"] == 7
    assert summary["refined_focused_tx_rx_offset_mm"] == 40.0
    assert summary["refined_focused_x_ambiguity_row_count"] == 0
    assert summary["joint_tx_rx_offset_mm"] == 20.0
    assert summary["focused_policy"] == "use_refined_focus_for_point_x"

    rows = stage_rows(summary)
    assert [row["stage"] for row in rows] == [
        "location_only",
        "focused_target2",
        "focused_target2_refined",
        "joint_radius",
    ]


def test_summarize_case_uses_full_joint_candidate_csv_when_available(tmp_path):
    detection = {
        "truth_x_values_mm": [190.0, 250.0, 310.0],
        "truth_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
    }
    state = {
        "final_state": {
            "x_values_mm": [190.0, 250.0, 310.0],
            "z_values_mm": [90.0, 90.0, 90.0],
            "radii_mm": [6.0, 6.0, 8.0],
        }
    }
    candidate_csv = tmp_path / "joint_radius_candidates.csv"
    candidate_csv.write_text(
        "\n".join([
            "case_label,misfit,radii_mm,source_frequency_scale,source_time_shift_ps,source_amplitude_scale",
            'case,0.10,"[5.5, 6.0, 8.0]",1.0,0.0,1.0',
            'case,0.11,"[5.0, 6.0, 8.0]",1.0,0.0,1.0',
        ])
        + "\n",
        encoding="utf-8",
    )
    joint = {
        "update_case_label": "case",
        "candidate_x_values_mm": [190.0, 250.0, 310.0],
        "candidate_z_values_mm": [90.0, 90.0, 90.0],
        "paths": {"candidate_csv": str(candidate_csv)},
        "ranked_by_case": {
            "case": [
                {"radii_mm": [5.5, 6.0, 8.0], "misfit": 0.1},
            ],
        },
    }
    case = {
        "label": "seed",
        "detection_json": _write(tmp_path / "det.json", detection),
        "location_json": _write(tmp_path / "loc.json", state),
        "focused_json": _write(tmp_path / "focus.json", state),
        "joint_json": _write(tmp_path / "joint.json", joint),
    }

    summary = summarize_case(case)

    assert summary["joint_truth_tuple_rank_in_top"] == 2
    assert summary["joint_best_radius_values_mm"] == [5.5, 6.0, 8.0]
    assert summary["joint_margin_abs"] == pytest.approx(0.01)
