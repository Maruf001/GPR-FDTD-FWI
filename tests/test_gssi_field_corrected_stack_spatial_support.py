from run_gssi_field_corrected_stack_spatial_support import (
    grouped_column_rows,
    summarize_spatial_support,
    support_intervals,
)


def _row(column, window, improvement, corrected):
    return {
        "column_index": str(column),
        "window_label": window,
        "x_m": str(column * 0.01),
        "abs_correlation_improvement": str(improvement),
        "corrected_abs_correlation": str(corrected),
    }


def test_grouped_column_rows_marks_majority_and_all_window_support():
    rows = [
        _row(0, "a", 0.10, 0.80),
        _row(0, "b", 0.08, 0.77),
        _row(0, "c", 0.09, 0.78),
        _row(1, "a", 0.10, 0.80),
        _row(1, "b", -0.02, 0.77),
        _row(1, "c", 0.09, 0.78),
    ]

    grouped = grouped_column_rows(
        rows,
        min_improvement=0.05,
        min_corrected_abs_correlation=0.65,
        majority_fraction=2 / 3,
    )

    assert grouped[0]["supported_window_count"] == 3
    assert grouped[0]["majority_supported"] is True
    assert grouped[0]["all_window_supported"] is True
    assert grouped[1]["supported_window_count"] == 2
    assert grouped[1]["majority_supported"] is True
    assert grouped[1]["all_window_supported"] is False


def test_support_intervals_groups_contiguous_supported_columns():
    column_rows = [
        {"column_index": 0, "x_m": 0.00, "majority_supported": True, "mean_abs_correlation_improvement": 0.1, "mean_corrected_abs_correlation": 0.8},
        {"column_index": 1, "x_m": 0.01, "majority_supported": True, "mean_abs_correlation_improvement": 0.1, "mean_corrected_abs_correlation": 0.8},
        {"column_index": 2, "x_m": 0.02, "majority_supported": True, "mean_abs_correlation_improvement": 0.1, "mean_corrected_abs_correlation": 0.8},
        {"column_index": 3, "x_m": 0.03, "majority_supported": False, "mean_abs_correlation_improvement": 0.0, "mean_corrected_abs_correlation": 0.4},
        {"column_index": 4, "x_m": 0.04, "majority_supported": True, "mean_abs_correlation_improvement": 0.2, "mean_corrected_abs_correlation": 0.9},
        {"column_index": 5, "x_m": 0.05, "majority_supported": True, "mean_abs_correlation_improvement": 0.2, "mean_corrected_abs_correlation": 0.9},
    ]

    intervals = support_intervals(column_rows, "majority_supported", min_columns=2)

    assert len(intervals) == 2
    assert intervals[0]["start_column_index"] == 0
    assert intervals[0]["end_column_index"] == 2
    assert intervals[1]["start_column_index"] == 4
    assert intervals[1]["end_column_index"] == 5


def test_summarize_spatial_support_marks_limited_but_usable_mask():
    column_rows = [
        {"majority_supported": True, "all_window_supported": False, "mean_abs_correlation_improvement": 0.1},
        {"majority_supported": True, "all_window_supported": True, "mean_abs_correlation_improvement": 0.2},
        {"majority_supported": False, "all_window_supported": False, "mean_abs_correlation_improvement": -0.1},
    ]
    interval_rows = [
        {
            "support_key": "majority_supported",
            "length_m": 0.12,
            "start_x_m": 0.1,
            "end_x_m": 0.22,
        }
    ]

    summary = summarize_spatial_support(column_rows, interval_rows)

    assert summary["policy_label"] == "corrected_stack_spatial_support_limited_but_usable"
    assert summary["majority_supported_column_count"] == 2
    assert summary["all_window_supported_column_count"] == 1
    assert summary["largest_majority_interval_length_m"] == 0.12
