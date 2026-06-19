from pathlib import Path

import pytest

from run_gssi_field_timing_discriminant_scorecard import (
    build_score_rows,
    classify_early_rows,
    classify_long_rows,
    classify_short_rows,
    summarize_scorecard,
    write_figure_notes,
)


def test_classify_early_rows_finds_near_zero_and_low_margin():
    rows = [
        {
            "window_label": "early_0p00_0p55",
            "dt_ns": "0.01",
            "comparison_minus_reference_shift_ns": "0.0",
            "best_minus_second_correlation": "0.002",
        },
        {
            "window_label": "early_0p00_0p70",
            "dt_ns": "0.01",
            "comparison_minus_reference_shift_ns": "-0.01",
            "best_minus_second_correlation": "0.00003",
        },
        {
            "window_label": "shallow_0p55_1p60",
            "dt_ns": "0.01",
            "comparison_minus_reference_shift_ns": "0.04",
            "best_minus_second_correlation": "0.001",
        },
    ]

    summary = classify_early_rows(rows)

    assert summary["strict_row_count"] == 2
    assert summary["strict_near_zero_count"] == 2
    assert summary["all_near_zero_count"] == 2
    assert summary["has_low_uniqueness_margin"] is True


def test_classify_short_rows_separates_raw_and_nonraw_support():
    rows = [
        {
            "offset_family": "raw_baseline",
            "offset_window_supported": "False",
            "offset_ns": "0.0",
            "matrix_abs_correlation_improvement": "0.0",
            "corrected_matrix_abs_correlation": "0.50",
        },
        {
            "offset_family": "nominal",
            "offset_window_supported": "True",
            "offset_ns": "0.127701",
            "matrix_abs_correlation_improvement": "0.25",
            "corrected_matrix_abs_correlation": "0.80",
        },
        {
            "offset_family": "bootstrap_ci",
            "offset_window_supported": "True",
            "offset_ns": "0.108055",
            "matrix_abs_correlation_improvement": "0.20",
            "corrected_matrix_abs_correlation": "0.75",
        },
    ]

    summary = classify_short_rows(rows)

    assert summary["raw_supported_count"] == 0
    assert summary["raw_row_count"] == 1
    assert summary["nonraw_supported_count"] == 2
    assert summary["nonraw_row_count"] == 2
    assert summary["nominal_offset_ns"] == 0.127701
    assert summary["min_nonraw_matrix_improvement"] == 0.20


def test_classify_long_rows_requires_rejecting_short_transfer():
    rows = [
        {
            "short_pair_offset_gain_vs_zero": "-0.05",
            "best_matrix_offset_ns": "0.06",
            "best_matrix_gain_vs_zero": "0.15",
        },
        {
            "short_pair_offset_gain_vs_zero": "-0.03",
            "best_matrix_offset_ns": "0.06",
            "best_matrix_gain_vs_zero": "0.16",
        },
    ]

    summary = classify_long_rows(rows, short_offset_ns=0.127701)

    assert summary["reject_short_transfer_count"] == 2
    assert summary["row_count"] == 2
    assert summary["best_offset_median_ns"] == 0.06
    assert summary["best_offset_distance_from_short_ns"] == pytest.approx(0.067701)
    assert summary["min_best_gain_vs_zero"] == 0.15


def test_scorecard_summary_ready_not_absolute():
    early = {
        "strict_near_zero_count": 2,
        "strict_row_count": 2,
        "strict_near_zero_fraction": 1.0,
        "min_strict_best_minus_second_correlation": 0.00003,
        "has_low_uniqueness_margin": True,
    }
    short = {
        "nonraw_supported_count": 2,
        "nonraw_row_count": 2,
        "raw_supported_count": 0,
        "raw_row_count": 1,
        "nominal_offset_ns": 0.127701,
        "min_nonraw_matrix_improvement": 0.20,
        "min_nonraw_corrected_abs_correlation": 0.75,
        "raw_supported_fraction": 0.0,
        "nonraw_supported_fraction": 1.0,
        "max_raw_matrix_improvement": 0.0,
    }
    long = {
        "reject_short_transfer_count": 2,
        "row_count": 2,
        "reject_short_transfer_fraction": 1.0,
        "best_offset_median_ns": 0.06,
        "best_offset_distance_from_short_ns": 0.067701,
        "min_best_gain_vs_zero": 0.15,
    }
    score_rows = build_score_rows(early=early, short=short, long=long)
    summary = summarize_scorecard(
        score_rows,
        early,
        short,
        long,
        {"absolute_time_zero_ready": False, "field_fwi_ready": False},
    )

    assert len(score_rows) == 4
    assert summary["policy_label"] == "field_timing_discriminant_scorecard_ready_not_absolute"
    assert summary["early_has_low_uniqueness_margin"] is True
    assert summary["short_raw_supported_count"] == 0
    assert summary["long_reject_short_transfer_count"] == 2
    assert summary["ready_for_manuscript_timing_scorecard"] is True


def test_write_figure_notes_documents_no_fwi_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "scorecard_ready",
        "early_strict_near_zero_count": 6,
        "early_strict_row_count": 6,
        "short_nonraw_supported_count": 18,
        "short_nonraw_row_count": 18,
        "short_raw_supported_count": 0,
        "short_raw_row_count": 3,
        "long_reject_short_transfer_count": 3,
        "long_row_count": 3,
        "gpu_priority": "none",
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("score.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "field_timing_discriminant_scorecard.png" in text
    assert "does not create absolute time-zero" in text
    assert "field FWI" in text
