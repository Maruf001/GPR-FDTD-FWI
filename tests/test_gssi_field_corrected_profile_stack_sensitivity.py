import pytest

from run_gssi_field_corrected_profile_stack_sensitivity import (
    parse_window_configs,
    summarize_sensitivity,
)


def test_parse_window_configs_accepts_multiple_windows():
    configs = parse_window_configs("0.35:1.1,0.45:1.25")

    assert configs == [
        {"window_label": "0.35_1.1ns", "time_window_min_ns": 0.35, "time_window_max_ns": 1.1},
        {"window_label": "0.45_1.25ns", "time_window_min_ns": 0.45, "time_window_max_ns": 1.25},
    ]


def test_parse_window_configs_rejects_inverted_window():
    with pytest.raises(Exception):
        parse_window_configs("1.25:0.45")


def test_summarize_sensitivity_marks_all_supported_windows_robust():
    rows = [
        {
            "matrix_abs_correlation_improvement": 0.12,
            "corrected_matrix_abs_correlation": 0.80,
            "improved_column_fraction": 0.62,
        },
        {
            "matrix_abs_correlation_improvement": 0.08,
            "corrected_matrix_abs_correlation": 0.72,
            "improved_column_fraction": 0.58,
        },
    ]

    summary = summarize_sensitivity(rows)

    assert summary["policy_label"] == "corrected_profile_stack_window_robust"
    assert summary["window_count"] == 2
    assert summary["robust_window_count"] == 2
    assert summary["min_matrix_abs_correlation_improvement"] == 0.08


def test_summarize_sensitivity_marks_mixed_support():
    rows = [
        {
            "matrix_abs_correlation_improvement": 0.12,
            "corrected_matrix_abs_correlation": 0.80,
            "improved_column_fraction": 0.62,
        },
        {
            "matrix_abs_correlation_improvement": 0.02,
            "corrected_matrix_abs_correlation": 0.70,
            "improved_column_fraction": 0.60,
        },
    ]

    summary = summarize_sensitivity(rows)

    assert summary["policy_label"] == "corrected_profile_stack_window_mixed"
    assert summary["robust_window_count"] == 1
