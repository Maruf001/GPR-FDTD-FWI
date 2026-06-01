"""Tests for coordinate objective diagnostic reporting."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_coordinate_objective_diagnostic_report import (  # noqa: E402
    build_ratio_rows,
    enrich_objective_rows,
    float_or_nan,
    summarize_ratio_rows,
)


def _summary():
    return {
        "true_x_values_mm": [150.0],
        "true_z_values_mm": [90.0],
        "truth_radius_mm": 6.0,
        "objective_diagnostic_rows": [
            {
                "run_name": "run",
                "case_label": "noise",
                "objective_label": "base",
                "pass_index": 0,
                "step_kind": "main",
                "step_target_index": 0,
                "best_x_mm": 150.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 6.0,
                "radius_margin_abs": 0.001,
            },
            {
                "run_name": "run",
                "case_label": "noise",
                "objective_label": "highband",
                "pass_index": 0,
                "step_kind": "main",
                "step_target_index": 0,
                "best_x_mm": 150.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 6.0,
                "radius_margin_abs": 0.002,
            },
            {
                "run_name": "run",
                "case_label": "mismatch",
                "objective_label": "base",
                "pass_index": 0,
                "step_kind": "main",
                "step_target_index": 0,
                "best_x_mm": 150.0,
                "best_z_mm": 91.0,
                "best_radius_mm": 6.8,
                "radius_margin_abs": 0.0005,
            },
            {
                "run_name": "run",
                "case_label": "mismatch",
                "objective_label": "highband",
                "pass_index": 0,
                "step_kind": "main",
                "step_target_index": 0,
                "best_x_mm": 150.0,
                "best_z_mm": 91.0,
                "best_radius_mm": 6.8,
                "radius_margin_abs": 0.001,
            },
        ],
    }


def test_enrich_objective_rows_marks_truth_geometry():
    rows = enrich_objective_rows(_summary(), "summary.json")

    assert rows[0]["is_truth_geometry"] is True
    assert rows[2]["is_truth_geometry"] is False
    assert rows[2]["radius_abs_error_mm"] == pytest.approx(0.8)


def test_enrich_objective_rows_uses_per_target_truth_radii_when_present():
    summary = _summary()
    summary["truth_radius_mm"] = 6.0
    summary["truth_radius_values_mm"] = [8.0]
    summary["objective_diagnostic_rows"][0]["best_radius_mm"] = 8.0

    rows = enrich_objective_rows(summary, "summary.json")

    assert rows[0]["truth_radius_mm"] == 8.0
    assert rows[0]["is_truth_geometry"] is True


def test_float_or_nan_accepts_missing_margin_values():
    assert float_or_nan(None) != float_or_nan(None)
    assert float_or_nan("0.2") == pytest.approx(0.2)


def test_build_ratio_rows_compares_to_matching_base():
    rows = enrich_objective_rows(_summary())
    ratio_rows = build_ratio_rows(rows)

    assert len(ratio_rows) == 2
    assert ratio_rows[0]["objective_label"] == "highband"
    assert ratio_rows[0]["margin_ratio_to_base"] == pytest.approx(2.0)
    assert ratio_rows[1]["base_is_truth_geometry"] is False
    assert ratio_rows[1]["variant_is_truth_geometry"] is False


def test_build_ratio_rows_keeps_unavailable_margin_ratio_as_nan():
    summary = _summary()
    summary["objective_diagnostic_rows"][0]["radius_margin_abs"] = None

    ratio_rows = build_ratio_rows(enrich_objective_rows(summary))

    assert ratio_rows[0]["margin_ratio_to_base"] != ratio_rows[0]["margin_ratio_to_base"]


def test_summarize_ratio_rows_counts_truth_and_changes():
    rows = build_ratio_rows(enrich_objective_rows(_summary()))

    summary = summarize_ratio_rows(rows)

    assert summary["row_count"] == 2
    assert summary["by_objective"]["highband"]["variant_truth_count"] == 1
    assert summary["by_objective"]["highband"]["margin_ratio_mean"] == pytest.approx(2.0)
