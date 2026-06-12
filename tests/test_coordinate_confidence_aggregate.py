"""Tests for coordinate confidence aggregate reporting."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_coordinate_confidence_aggregate import (  # noqa: E402
    _format_optional_float,
    aggregate_rows,
    enrich_coordinate_rows,
    write_figure_notes,
)


def _summary():
    return {
        "run_name": "unit",
        "true_x_values_mm": [150.0, 250.0],
        "true_z_values_mm": [90.0, 90.0],
        "truth_radius_mm": 6.0,
        "sources": 5,
        "frequency_ghz": 1.5,
        "tx_rx_offset_mm": 40.0,
        "confidence_rows": [
            {
                "run_name": "unit",
                "case_label": "noise",
                "step_target_index": 0,
                "best_x_mm": 150.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 6.0,
                "radius_margin_abs": 4.0e-4,
                "confidence_label": "weak",
                "fallback_warning": "radius_weak_confidence",
                "ambiguity_x_min_mm": 149.0,
                "ambiguity_x_max_mm": 150.0,
                "ambiguity_z_min_mm": 90.0,
                "ambiguity_z_max_mm": 90.0,
                "ambiguity_radius_min_mm": 6.0,
                "ambiguity_radius_max_mm": 6.2,
            },
            {
                "run_name": "unit",
                "case_label": "noise",
                "step_target_index": 1,
                "best_x_mm": 251.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 6.2,
                "radius_margin_abs": 1.2e-3,
                "confidence_label": "strong",
                "fallback_warning": "",
                "ambiguity_x_min_mm": 251.0,
                "ambiguity_x_max_mm": 251.0,
                "ambiguity_z_min_mm": 90.0,
                "ambiguity_z_max_mm": 91.0,
                "ambiguity_radius_min_mm": 6.2,
                "ambiguity_radius_max_mm": 6.2,
            },
        ],
    }


def test_enrich_coordinate_rows_adds_truth_errors_and_flags():
    rows = enrich_coordinate_rows(_summary(), "summary.json")

    assert rows[0]["summary_path"] == "summary.json"
    assert rows[0]["sources"] == 5
    assert rows[0]["frequency_ghz"] == 1.5
    assert rows[0]["tx_rx_offset_mm"] == 40.0
    assert rows[0]["tx_rx_offset_inferred"] is False
    assert rows[0]["tx_rx_offset_source"] == "summary"
    assert rows[0]["is_truth_geometry"] is True
    assert rows[0]["x_abs_error_mm"] == 0.0
    assert rows[0]["ambiguity_x_width_mm"] == 1.0
    assert rows[0]["ambiguity_radius_width_mm"] == 0.20000000000000018
    assert rows[1]["is_truth_geometry"] is False
    assert rows[1]["x_abs_error_mm"] == 1.0
    assert rows[1]["radius_abs_error_mm"] == 0.20000000000000018


def test_enrich_coordinate_rows_uses_per_target_truth_radii():
    summary = _summary()
    summary["truth_radius_mm"] = 6.0
    summary["truth_radius_values_mm"] = [5.0, 6.2]
    summary["confidence_rows"][0]["best_radius_mm"] = 5.0
    summary["confidence_rows"][1]["best_radius_mm"] = 6.2

    rows = enrich_coordinate_rows(summary)

    assert rows[0]["truth_radius_mm"] == 5.0
    assert rows[0]["is_truth_geometry"] is True
    assert rows[1]["truth_radius_mm"] == 6.2
    assert rows[1]["is_truth_radius"] is True


def test_enrich_coordinate_rows_can_fill_missing_tx_rx_offset_explicitly():
    summary = _summary()
    summary.pop("tx_rx_offset_mm")

    rows = enrich_coordinate_rows(
        summary,
        default_missing_tx_rx_offset_mm=20.0,
    )
    aggregate = aggregate_rows(rows)

    assert rows[0]["tx_rx_offset_mm"] == 20.0
    assert rows[0]["tx_rx_offset_inferred"] is True
    assert rows[0]["tx_rx_offset_source"] == "default_missing"
    key = "sources=5|tx_rx_offset_mm=20|tx_rx_offset_source=default_missing"
    assert aggregate["acquisition_summary"][key]["label"] == (
        "5 sources, Tx/Rx offset 20 mm (filled default)"
    )


def test_missing_tx_rx_offset_remains_visible_without_default():
    summary = _summary()
    summary.pop("tx_rx_offset_mm")

    rows = enrich_coordinate_rows(summary)
    aggregate = aggregate_rows(rows)

    assert rows[0]["tx_rx_offset_mm"] is None
    assert rows[0]["tx_rx_offset_inferred"] is False
    assert rows[0]["tx_rx_offset_source"] == "missing"
    key = "sources=5|tx_rx_offset_mm=not_recorded"
    assert aggregate["acquisition_summary"][key]["label"] == (
        "5 sources, Tx/Rx offset not recorded"
    )


def test_missing_tx_rx_default_must_be_finite_and_nonnegative():
    summary = _summary()
    summary.pop("tx_rx_offset_mm")

    with pytest.raises(ValueError, match="finite non-negative"):
        enrich_coordinate_rows(summary, default_missing_tx_rx_offset_mm=float("nan"))

    with pytest.raises(ValueError, match="finite non-negative"):
        enrich_coordinate_rows(summary, default_missing_tx_rx_offset_mm=float("inf"))

    with pytest.raises(ValueError, match="finite non-negative"):
        enrich_coordinate_rows(summary, default_missing_tx_rx_offset_mm=-1.0)


def test_enrich_coordinate_rows_tolerates_nonfinite_optional_metrics():
    summary = _summary()
    summary["sources"] = "bad"
    summary["frequency_ghz"] = float("inf")
    summary["tx_rx_offset_mm"] = float("nan")
    summary["confidence_rows"][0]["best_x_mm"] = "nan"
    summary["confidence_rows"][0]["best_z_mm"] = "bad"
    summary["confidence_rows"][0]["best_radius_mm"] = float("inf")
    summary["confidence_rows"][0]["next_radius_mm"] = "bad"
    summary["confidence_rows"][0]["radius_margin_abs"] = "nan"
    summary["confidence_rows"][0]["radius_margin_rel"] = float("inf")
    summary["confidence_rows"][0]["best_misfit"] = float("inf")
    summary["confidence_rows"][0]["next_radius_misfit"] = float("nan")
    summary["confidence_rows"][0]["ambiguity_x_min_mm"] = "bad"
    summary["confidence_rows"][0]["source_frequency_scale"] = float("nan")

    rows = enrich_coordinate_rows(summary)
    aggregate = aggregate_rows(rows)

    assert rows[0]["sources"] is None
    assert rows[0]["frequency_ghz"] is None
    assert rows[0]["tx_rx_offset_mm"] is None
    assert rows[0]["best_x_mm"] is None
    assert rows[0]["best_z_mm"] is None
    assert rows[0]["best_radius_mm"] is None
    assert rows[0]["next_radius_mm"] is None
    assert rows[0]["radius_margin_abs"] is None
    assert rows[0]["radius_margin_rel"] is None
    assert rows[0]["best_misfit"] is None
    assert rows[0]["next_radius_misfit"] is None
    assert rows[0]["source_frequency_scale"] is None
    json.dumps(rows, allow_nan=False)
    assert rows[0]["x_abs_error_mm"] is None
    assert rows[0]["z_abs_error_mm"] is None
    assert rows[0]["radius_abs_error_mm"] is None
    assert rows[0]["ambiguity_x_width_mm"] is None
    assert rows[0]["is_truth_geometry"] is False
    assert aggregate["radius_margin_abs_min"] == 1.2e-3
    assert aggregate["target_summary"]["0"]["radius_margin_abs_min"] is None


def test_aggregate_rows_counts_accuracy_labels_warnings_and_targets():
    rows = enrich_coordinate_rows(_summary())
    aggregate = aggregate_rows(rows)

    assert aggregate["row_count"] == 2
    assert aggregate["truth_geometry_count"] == 1
    assert aggregate["confidence_label_counts"] == {"weak": 1, "strong": 1}
    assert aggregate["fallback_warning_count"] == 1
    assert aggregate["radius_margin_abs_min"] == 4.0e-4
    assert aggregate["radius_margin_abs_max"] == 1.2e-3
    assert aggregate["ambiguity_x_width_max_mm"] == 1.0
    assert aggregate["ambiguity_z_width_max_mm"] == 1.0
    assert aggregate["ambiguity_radius_width_max_mm"] == 0.20000000000000018
    assert aggregate["x_ambiguity_row_count"] == 1
    assert aggregate["target_summary"]["0"]["truth_geometry_count"] == 1
    assert aggregate["target_summary"]["1"]["truth_geometry_count"] == 0
    assert aggregate["source_summary"]["5"]["row_count"] == 2
    assert aggregate["source_summary"]["5"]["x_ambiguity_row_count"] == 1
    key = "sources=5|tx_rx_offset_mm=40"
    assert aggregate["acquisition_summary"][key]["label"] == "5 sources, Tx/Rx offset 40 mm"
    assert aggregate["acquisition_summary"][key]["row_count"] == 2
    assert aggregate["acquisition_summary"][key]["x_ambiguity_row_count"] == 1


def test_write_figure_notes_describes_aggregate(tmp_path):
    aggregate = aggregate_rows(enrich_coordinate_rows(_summary()))
    path = tmp_path / "FIGURE_NOTES.md"

    write_figure_notes(path, aggregate)

    text = path.read_text(encoding="utf-8")
    assert "coordinate_confidence_aggregate.png" in text
    assert "coordinate_ambiguity_widths.png" in text
    assert "Rows: 2" in text
    assert "target 0" in text
    assert "5 sources" in text
    assert "Tx/Rx offset 40 mm" in text


def test_write_figure_notes_marks_missing_widths(tmp_path):
    path = tmp_path / "FIGURE_NOTES.md"
    write_figure_notes(
        path,
        {
            "row_count": 1,
            "truth_geometry_count": 0,
            "confidence_label_counts": {"missing": 1},
            "target_summary": {},
            "source_summary": {},
            "acquisition_summary": {},
            "x_ambiguity_row_count": 0,
            "ambiguity_x_width_max_mm": None,
            "ambiguity_z_width_max_mm": None,
            "ambiguity_radius_width_max_mm": None,
        },
    )

    text = path.read_text(encoding="utf-8")
    assert "not_recorded / not_recorded / not_recorded mm" in text


def test_format_optional_float_marks_nonfinite_values():
    assert _format_optional_float(float("nan")) == "not_recorded"
    assert _format_optional_float("bad") == "not_recorded"
