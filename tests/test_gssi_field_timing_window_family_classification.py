from run_gssi_field_timing_window_family_classification import (
    classify_early_rows,
    classify_long_pattern_rows,
    classify_short_content_rows,
    family_rows,
    summarize,
)


def test_classify_early_rows_counts_strict_near_zero_lags():
    rows = [
        {
            "window_max_ns": "0.55",
            "dt_ns": "0.01",
            "lag_samples": "0",
            "comparison_minus_reference_shift_ns": "0.0",
        },
        {
            "window_max_ns": "0.70",
            "dt_ns": "0.01",
            "lag_samples": "-1",
            "comparison_minus_reference_shift_ns": "-0.01",
        },
        {
            "window_max_ns": "1.60",
            "dt_ns": "0.01",
            "lag_samples": "4",
            "comparison_minus_reference_shift_ns": "0.04",
        },
    ]

    summary = classify_early_rows(rows)

    assert summary["row_count"] == 3
    assert summary["strict_early_row_count"] == 2
    assert summary["strict_early_near_zero_lag_row_count"] == 2
    assert summary["near_zero_lag_row_count"] == 2


def test_classify_short_content_rows_requires_nonraw_support_and_raw_rejection():
    rows = [
        {"offset_family": "raw_baseline", "offset_window_supported": "False"},
        {
            "offset_family": "nominal",
            "offset_window_supported": "True",
            "matrix_abs_correlation_improvement": "0.2",
            "corrected_matrix_abs_correlation": "0.8",
        },
        {
            "offset_family": "bootstrap_ci",
            "offset_window_supported": "True",
            "matrix_abs_correlation_improvement": "0.1",
            "corrected_matrix_abs_correlation": "0.7",
        },
    ]

    summary = classify_short_content_rows(rows)

    assert summary["raw_supported_count"] == 0
    assert summary["nonraw_supported_count"] == 2
    assert summary["nonraw_row_count"] == 2
    assert summary["min_nonraw_matrix_improvement"] == 0.1


def test_classify_long_pattern_rows_finds_rejecting_windows():
    rows = [
        {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "best_matrix_offset_ns": "0.06",
            "best_matrix_offset_distance_from_short_pair_ns": "0.067",
            "best_matrix_gain_vs_zero": "0.15",
            "short_pair_offset_gain_vs_zero": "-0.04",
        },
        {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "best_matrix_offset_ns": "0.05",
            "best_matrix_offset_distance_from_short_pair_ns": "0.077",
            "best_matrix_gain_vs_zero": "0.12",
            "short_pair_offset_gain_vs_zero": "-0.02",
        },
    ]

    summary = classify_long_pattern_rows(rows)

    assert summary["reject_short_transfer_row_count"] == 2
    assert summary["row_count"] == 2
    assert summary["best_offset_median_ns"] == 0.055
    assert summary["max_short_transfer_gain_vs_zero"] == -0.02


def test_summarize_marks_ready_when_window_families_separate():
    early = {
        "row_count": 8,
        "strict_early_row_count": 6,
        "zero_lag_row_count": 5,
        "near_zero_lag_row_count": 7,
        "strict_early_near_zero_lag_row_count": 6,
        "max_strict_early_abs_shift_ns": 0.01,
        "max_all_early_abs_shift_ns": 0.04,
    }
    short_content = {
        "row_count": 21,
        "raw_row_count": 3,
        "raw_supported_count": 0,
        "nonraw_row_count": 18,
        "nonraw_supported_count": 18,
        "nominal_supported_count": 3,
        "nominal_row_count": 3,
        "min_nonraw_matrix_improvement": 0.12,
        "min_nonraw_corrected_abs_correlation": 0.66,
    }
    long_pattern = {
        "row_count": 3,
        "reject_short_transfer_row_count": 3,
        "best_offset_median_ns": 0.06,
        "best_offset_distance_from_short_pair_median_ns": 0.067,
        "min_best_gain_vs_zero": 0.15,
        "max_short_transfer_gain_vs_zero": -0.03,
    }
    timing = {
        "short_content_offset_ns": 0.1277,
        "short_content_half_width_ns": 0.0589,
        "early_common_mode_shift_ns": 0.0,
        "long_pattern_offset_ns": 0.06,
        "early_vs_short_delta_half_widths": 2.16,
        "long_vs_short_delta_half_widths": 1.15,
    }

    rows = family_rows(early, short_content, long_pattern, timing)
    summary = summarize(early, short_content, long_pattern, timing)

    assert len(rows) == 3
    assert summary["policy_label"] == "field_timing_window_family_classification_ready_not_absolute"
    assert summary["ready_for_manuscript_field_timing_boundary"] is True
    assert summary["absolute_time_zero_ready"] is False
    assert summary["field_fwi_ready"] is False
