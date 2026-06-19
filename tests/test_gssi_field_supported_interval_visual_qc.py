import math

import numpy as np

from run_gssi_field_supported_interval_visual_qc import (
    crop_interval,
    interval_metric_row,
    select_supported_intervals,
    summarize_visual_qc,
)


def test_select_supported_intervals_prefers_longest_all_window_rows():
    rows = [
        {"support_key": "majority_supported", "length_m": "0.20", "start_x_m": "0.5", "mean_corrected_abs_correlation": "0.9"},
        {"support_key": "all_window_supported", "length_m": "0.03", "start_x_m": "0.2", "mean_corrected_abs_correlation": "0.8"},
        {"support_key": "all_window_supported", "length_m": "0.07", "start_x_m": "0.4", "mean_corrected_abs_correlation": "0.95"},
        {"support_key": "all_window_supported", "length_m": "0.05", "start_x_m": "0.1", "mean_corrected_abs_correlation": "0.85"},
    ]

    selected = select_supported_intervals(rows, support_key="all_window_supported", max_intervals=2)

    assert [row["start_x_m"] for row in selected] == ["0.1", "0.4"]
    assert [row["selected_interval_index"] for row in selected] == [1, 2]


def test_select_supported_intervals_falls_back_to_majority_when_requested_key_missing():
    rows = [
        {"support_key": "majority_supported", "length_m": "0.04", "start_x_m": "0.2"},
    ]

    selected = select_supported_intervals(rows, support_key="all_window_supported", max_intervals=1)

    assert len(selected) == 1
    assert selected[0]["support_key"] == "majority_supported"


def test_crop_interval_expands_with_padding_columns():
    windows = {
        "x_m": np.array([0.0, 0.1, 0.2, 0.3, 0.4]),
        "time_ns": np.array([0.0, 1.0]),
        "reference_window": np.arange(10, dtype=float).reshape(2, 5),
        "raw_aligned_comparison": np.arange(10, 20, dtype=float).reshape(2, 5),
        "corrected_aligned_comparison": np.arange(20, 30, dtype=float).reshape(2, 5),
    }
    interval = {"start_x_m": "0.1", "end_x_m": "0.2"}

    crop = crop_interval(windows, interval, pad_columns=1)

    assert crop["column_start"] == 0
    assert crop["column_end"] == 3
    np.testing.assert_allclose(crop["x_m"], [0.0, 0.1, 0.2, 0.3])
    assert crop["reference_window"].shape == (2, 4)


def test_interval_metric_row_reports_correlation_improvement():
    interval = {"selected_interval_index": 1, "start_x_m": 0.0, "end_x_m": 0.1, "length_m": 0.1}
    reference = np.tile(np.linspace(-1.0, 1.0, 16), (4, 1)).T
    raw = np.tile(np.cos(np.linspace(0.0, 2.0 * np.pi, 16)), (4, 1)).T
    corrected = reference.copy()
    cropped = {
        "x_m": np.array([0.0, 0.1, 0.2, 0.3]),
        "time_ns": np.linspace(0.0, 1.0, 16),
        "reference_window": reference,
        "raw_aligned_comparison": raw,
        "corrected_aligned_comparison": corrected,
        "column_start": 0,
        "column_end": 3,
    }

    row = interval_metric_row(interval, cropped)

    assert row["corrected_interval_abs_correlation"] > row["raw_interval_abs_correlation"]
    assert row["interval_abs_correlation_improvement"] > 0.0


def test_summarize_visual_qc_marks_ready_when_all_selected_intervals_supported():
    rows = [
        {"corrected_interval_abs_correlation": 0.91, "interval_abs_correlation_improvement": 0.2, "length_m": 0.07},
        {"corrected_interval_abs_correlation": 0.83, "interval_abs_correlation_improvement": 0.1, "length_m": 0.05},
    ]

    summary = summarize_visual_qc(rows, requested_support_key="all_window_supported")

    assert summary["policy_label"] == "supported_interval_visual_qc_ready"
    assert summary["selected_interval_count"] == 2
    assert summary["supported_interval_count"] == 2
    assert math.isclose(summary["total_selected_interval_length_m"], 0.12)
