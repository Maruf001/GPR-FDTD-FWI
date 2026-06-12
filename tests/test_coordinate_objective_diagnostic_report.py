"""Tests for coordinate objective diagnostic reporting."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_coordinate_objective_diagnostic_report import (  # noqa: E402
    build_ratio_rows,
    enrich_objective_rows,
    float_or_nan,
    format_optional_float,
    main,
    objective_confidence_rows,
    summarize_objective_confidence,
    summarize_ratio_rows,
    write_figure_notes,
)


def _summary():
    return {
        "run_name": "run",
        "backend": "cpu",
        "grid_step_mm": 1.0,
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
        "steps": [
            {
                "pass_index": 0,
                "target_index": 0,
                "update_case_label": "noise",
                "objective_results": {
                    "noise": {
                        "base": {
                            "margin": {
                                "best_radius_mm": 6.0,
                                "next_radius_mm": 6.2,
                                "radius_margin_abs": 0.0007,
                                "radius_margin_rel": 0.006,
                                "best_radius_misfit": 0.1,
                                "next_radius_misfit": 0.1007,
                            },
                            "top_candidates": [
                                {
                                    "misfit": 0.1,
                                    "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
                                    "source_profile": {"frequency_scale": 1.0},
                                },
                                {
                                    "misfit": 0.1007,
                                    "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.2},
                                    "source_profile": {"frequency_scale": 1.0},
                                },
                            ],
                        },
                        "highband": {
                            "margin": {
                                "best_radius_mm": 6.0,
                                "next_radius_mm": 6.2,
                                "radius_margin_abs": 0.002,
                                "radius_margin_rel": 0.02,
                                "best_radius_misfit": 0.1,
                                "next_radius_misfit": 0.102,
                            },
                            "top_candidates": [
                                {
                                    "misfit": 0.1,
                                    "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
                                    "source_profile": {"frequency_scale": 1.0},
                                },
                                {
                                    "misfit": 0.102,
                                    "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.2},
                                    "source_profile": {"frequency_scale": 1.0},
                                },
                            ],
                        },
                    }
                },
            }
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


def test_diagnostic_ratio_rows_tolerate_missing_best_geometry():
    summary = _summary()
    summary["objective_diagnostic_rows"][1]["best_z_mm"] = None

    rows = enrich_objective_rows(summary)
    ratio_rows = build_ratio_rows(rows)
    aggregate = summarize_ratio_rows(ratio_rows)

    sparse = [row for row in rows if row["case_label"] == "noise" and row["objective_label"] == "highband"][0]
    assert sparse["z_abs_error_mm"] is None
    assert sparse["is_truth_geometry"] is False

    sparse_ratio = [row for row in ratio_rows if row["case_label"] == "noise"][0]
    assert sparse_ratio["variant_best_z_mm"] is None
    assert sparse_ratio["geometry_comparison_available"] is False
    assert sparse_ratio["variant_changes_geometry"] is None
    assert aggregate["by_objective"]["highband"]["geometry_comparison_unavailable_count"] == 1


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


def test_build_ratio_rows_keeps_unavailable_margin_ratio_as_null():
    summary = _summary()
    summary["objective_diagnostic_rows"][0]["radius_margin_abs"] = None

    ratio_rows = build_ratio_rows(enrich_objective_rows(summary))

    assert ratio_rows[0]["base_margin_abs"] is None
    assert ratio_rows[0]["margin_ratio_to_base"] is None


def test_summarize_ratio_rows_counts_truth_and_changes():
    rows = build_ratio_rows(enrich_objective_rows(_summary()))

    summary = summarize_ratio_rows(rows)

    assert summary["row_count"] == 2
    assert summary["by_objective"]["highband"]["variant_truth_count"] == 1
    assert summary["by_objective"]["highband"]["margin_ratio_mean"] == pytest.approx(2.0)


def test_objective_confidence_rows_include_labels_and_ambiguity():
    rows = objective_confidence_rows(_summary(), "summary.json")

    assert [row["objective_label"] for row in rows] == ["base", "highband"]
    assert rows[0]["confidence_label"] == "moderate"
    assert rows[1]["confidence_label"] == "strong"
    assert rows[0]["summary_path"] == "summary.json"
    assert rows[0]["is_truth_geometry"] is True
    assert rows[1]["ambiguity_radius_min_mm"] == pytest.approx(6.0)
    assert rows[1]["ambiguity_radius_max_mm"] == pytest.approx(6.0)


def test_objective_confidence_rows_tolerate_missing_top_candidate_geometry():
    summary = _summary()
    summary["steps"][0]["objective_results"]["noise"]["sparse"] = {
        "margin": {
            "best_radius_mm": None,
            "next_radius_mm": None,
            "radius_margin_abs": None,
            "radius_margin_rel": None,
        },
        "top_candidates": [],
    }

    rows = objective_confidence_rows(summary)

    sparse = [row for row in rows if row["objective_label"] == "sparse"][0]
    assert sparse["confidence_label"] == "missing"
    assert sparse["best_x_mm"] is None
    assert sparse["x_abs_error_mm"] is None
    assert sparse["z_abs_error_mm"] is None
    assert sparse["radius_abs_error_mm"] is None
    assert sparse["is_truth_geometry"] is False


def test_summarize_objective_confidence_counts_by_objective():
    rows = objective_confidence_rows(_summary())

    summary = summarize_objective_confidence(rows)

    assert summary["row_count"] == 2
    assert summary["by_objective"]["base"]["confidence_label_counts"] == {"moderate": 1}
    assert summary["by_objective"]["highband"]["confidence_label_counts"] == {"strong": 1}
    assert summary["by_objective"]["highband"]["truth_geometry_count"] == 1
    assert summary["by_objective"]["highband"]["ambiguity_radius_width_max_mm"] == pytest.approx(0.0)


def test_format_optional_float_marks_missing_values():
    assert format_optional_float(None) == "not_recorded"
    assert format_optional_float(float("nan")) == "not_recorded"
    assert format_optional_float("bad") == "not_recorded"
    assert format_optional_float(1.23456) == "1.23"


def test_write_figure_notes_handles_missing_objective_confidence_widths(tmp_path):
    path = tmp_path / "FIGURE_NOTES.md"
    write_figure_notes(
        path,
        {
            "by_objective": {
                "highband": {
                    "row_count": 1,
                    "variant_truth_count": 1,
                    "geometry_change_count": 0,
                    "margin_ratio_mean": None,
                }
            },
            "objective_confidence": {
                "by_objective": {
                    "highband": {
                        "row_count": 1,
                        "truth_geometry_count": 1,
                        "confidence_label_counts": {"weak": 1},
                        "ambiguity_x_width_max_mm": None,
                        "ambiguity_z_width_max_mm": None,
                        "ambiguity_radius_width_max_mm": None,
                    }
                }
            },
        },
    )

    text = path.read_text(encoding="utf-8")
    assert "mean margin ratio=not_recorded" in text
    assert "not_recorded/not_recorded/not_recorded mm" in text


def test_main_omits_missing_confidence_csv_artifact(tmp_path, monkeypatch):
    summary = _summary()
    summary["steps"] = []
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    outdir = tmp_path / "report"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_coordinate_objective_diagnostic_report.py",
            str(summary_path),
            "--outdir",
            str(outdir),
        ],
    )

    main()

    manifest = json.loads((outdir / "run_manifest.json").read_text(encoding="utf-8"))
    assert "confidence_csv" not in manifest
    assert not (outdir / "data" / "coordinate_objective_confidence_rows.csv").exists()
