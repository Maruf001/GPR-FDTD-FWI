"""Tests for packaged two-stage refinement aggregation."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_two_stage_refinement_aggregate import (  # noqa: E402
    confidence_label,
    finite_value_notice,
    interval_width,
    material_uncertainty_row_from_summary,
    positive_axis_limit,
    run_id_from_path,
    summarize_two_stage_summary,
    symmetric_error_limits,
)


def _summary(margin_abs=0.002, margin_rel=0.02):
    return {
        "truth": {"x_mm": 250.0, "z_mm": 70.0, "radius_mm": 4.0},
        "observed_source": {
            "frequency_scale": 1.1,
            "time_shift_ps": -50.0,
            "amplitude_scale": 1.1,
            "noise_rms_fraction": 0.1,
            "noise_seed": 13,
        },
        "selected_detection": {"rank": 1, "x_mm": 250.0, "z_mm": 75.0},
        "coarse_grid": {"candidate_count": 49},
        "fine_grid": {"candidate_count": 15},
        "fine_best": {
            "params": {"x_mm": 250.0, "z_mm": 70.0, "radius_mm": 4.0},
            "source_profile": {
                "frequency_scale": 1.1,
                "time_shift_ps": -50.0,
                "amplitude_scale": 1.09,
            },
        },
        "fine_margin": {
            "radius_margin_abs": margin_abs,
            "radius_margin_rel": margin_rel,
        },
        "fine_radius_ambiguity": {
            "exact_tie": {
                "radius_min_mm": 4.0,
                "radius_max_mm": 4.1,
                "radius_count": 2,
            },
            "weak_interval": {
                "radius_min_mm": 3.9,
                "radius_max_mm": 4.2,
                "radius_count": 4,
            },
        },
        "truth_errors": {
            "x_error_mm": 0.0,
            "z_error_mm": 0.0,
            "radius_error_mm": 0.0,
        },
        "elapsed_time_s": {"overall_wall": 422.0},
    }


def _guarded_summary():
    summary = _summary(margin_abs=0.002, margin_rel=0.02)
    summary["final_stage"] = "guarded_polish"
    summary["final_best"] = {
        "params": {"x_mm": 250.0, "z_mm": 70.0, "radius_mm": 3.9},
        "source_profile": {
            "frequency_scale": 1.1,
            "time_shift_ps": -50.0,
            "amplitude_scale": 1.08,
        },
    }
    summary["final_margin"] = {
        "radius_margin_abs": 0.0001,
        "radius_margin_rel": 0.001,
    }
    summary["final_radius_ambiguity"] = {
        "exact_tie": {
            "radius_min_mm": 3.9,
            "radius_max_mm": 3.9,
            "radius_count": 1,
        },
        "weak_interval": {
            "radius_min_mm": 3.8,
            "radius_max_mm": 4.0,
            "radius_count": 3,
        },
    }
    summary["truth_errors"]["radius_error_mm"] = 0.1
    return summary


def _highband_summary():
    summary = _summary(margin_abs=0.0006, margin_rel=0.002)
    summary["final_stage"] = "highband_polish"
    summary["final_best"] = {
        "params": {"x_mm": 250.0, "z_mm": 70.0, "radius_mm": 4.0},
        "source_profile": {
            "frequency_scale": 1.1,
            "time_shift_ps": -50.0,
            "amplitude_scale": 1.1,
        },
    }
    summary["final_margin"] = {
        "radius_margin_abs": 0.0018,
        "radius_margin_rel": 0.003,
    }
    summary["final_radius_ambiguity"] = {
        "exact_tie": {
            "radius_min_mm": 4.0,
            "radius_max_mm": 4.0,
            "radius_count": 1,
        },
        "weak_interval": {
            "radius_min_mm": 3.9,
            "radius_max_mm": 4.0,
            "radius_count": 2,
        },
    }
    return summary


def test_confidence_label_marks_weak_small_relative_margin():
    assert confidence_label(0.0006, 0.002) == "weak"
    assert confidence_label(0.002, 0.002) == "strong"
    assert confidence_label(0.0008, 0.008) == "moderate"


def test_run_id_from_path_reads_numbered_prefix():
    assert run_id_from_path("outputs/experiments/121_example") == "121"


def test_symmetric_error_limits_keeps_all_zero_data_visible():
    assert symmetric_error_limits([0.0, 0.0], floor=0.05) == (-0.05, 0.05)


def test_positive_axis_limit_keeps_all_zero_bar_data_visible():
    assert positive_axis_limit([0.0, 0.0], floor=0.25) == 0.25


def test_finite_value_notice_marks_all_zero_and_missing_values():
    notice = finite_value_notice(
        [0.0, float("nan")],
        "all zero",
        "radius error",
    )

    assert notice == "all zero; 1 run(s) missing finite values"


def test_finite_value_notice_marks_no_finite_values():
    notice = finite_value_notice(
        [float("nan")],
        "all zero",
        "radius error",
    )

    assert notice == "radius error: no finite values available"


def test_interval_width_returns_non_negative_span():
    row = {
        "exact_radius_min_mm": 4.1,
        "exact_radius_max_mm": 4.0,
        "weak_radius_min_mm": 3.7,
        "weak_radius_max_mm": 4.3,
    }

    assert interval_width(row, "exact") == 0.0
    assert interval_width(row, "weak") == pytest.approx(0.6)


def test_summarize_two_stage_summary_flattens_key_fields():
    row = summarize_two_stage_summary(_summary(margin_abs=0.0006, margin_rel=0.002), "outputs/experiments/121_example")

    assert row["run_id"] == "121"
    assert row["final_stage"] == "fine_polish"
    assert row["truth_z_mm"] == 70.0
    assert row["fine_radius_mm"] == 4.0
    assert row["fine_stage_radius_mm"] == 4.0
    assert row["fine_stage_margin_abs"] == pytest.approx(0.0006)
    assert row["final_radius_mm"] == 4.0
    assert row["final_margin_abs"] == pytest.approx(0.0006)
    assert row["confidence"] == "weak"
    assert row["fine_stage_confidence"] == "weak"
    assert row["final_confidence"] == "weak"
    assert row["exact_radius_min_mm"] == 4.0
    assert row["exact_radius_max_mm"] == 4.1
    assert row["weak_radius_count"] == 4
    assert row["fine_source_time_shift_ps"] == -50.0


def test_summarize_two_stage_summary_prefers_guarded_final_fields():
    row = summarize_two_stage_summary(_guarded_summary(), "outputs/experiments/148_example")

    assert row["run_id"] == "148"
    assert row["final_stage"] == "guarded_polish"
    assert row["fine_radius_mm"] == 3.9
    assert row["fine_stage_radius_mm"] == 4.0
    assert row["fine_stage_margin_abs"] == pytest.approx(0.002)
    assert row["final_radius_mm"] == 3.9
    assert row["final_margin_abs"] == pytest.approx(0.0001)
    assert row["fine_stage_confidence"] == "strong"
    assert row["final_confidence"] == "weak"
    assert row["radius_error_mm"] == 0.1
    assert row["weak_radius_min_mm"] == 3.8


def test_summarize_two_stage_summary_accepts_highband_final_stage():
    row = summarize_two_stage_summary(_highband_summary(), "outputs/experiments/178_example")

    assert row["run_id"] == "178"
    assert row["final_stage"] == "highband_polish"
    assert row["final_margin_abs"] == 0.0018
    assert row["final_confidence"] == "strong"
    assert row["weak_radius_min_mm"] == 3.9


def test_material_uncertainty_row_from_summary_reads_report(tmp_path):
    report_path = tmp_path / "radius_uncertainty_report.json"
    report_path.write_text(
        '{"rows": [{"case": "r4", "material_best_radius_mm": 4.05}]}',
        encoding="utf-8",
    )

    row = material_uncertainty_row_from_summary({
        "paths": {"radius_uncertainty_report_summary": str(report_path)}
    })

    assert row["material_best_radius_mm"] == 4.05


def test_summarize_two_stage_summary_includes_material_uncertainty_fields(tmp_path):
    report_path = tmp_path / "radius_uncertainty_report.json"
    report_path.write_text(
        """
        {
          "rows": [
            {
              "material_best_radius_mm": 4.05,
              "material_radius_error_mm": 0.05,
              "material_margin_abs": 0.00002,
              "material_weak_min_mm": 3.95,
              "material_weak_max_mm": 4.05,
              "material_weak_width_mm": 0.1,
              "material_minus_nominal_best_mm": 0.05,
              "material_best_concrete_epsr": 6.0,
              "material_best_rebar_log10_sigma": 6.0
            }
          ]
        }
        """,
        encoding="utf-8",
    )
    summary = _highband_summary()
    summary["paths"] = {"radius_uncertainty_report_summary": str(report_path)}
    summary["material_uncertainty_enabled"] = True

    row = summarize_two_stage_summary(summary, "outputs/experiments/198_example")

    assert row["material_uncertainty_enabled"] is True
    assert row["material_best_radius_mm"] == 4.05
    assert row["material_weak_interval_width_mm"] == pytest.approx(0.1)
    assert row["material_best_rebar_log10_sigma"] == 6.0
