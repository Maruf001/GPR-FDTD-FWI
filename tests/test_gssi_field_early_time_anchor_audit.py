import math

import numpy as np

from run_gssi_field_early_time_anchor_audit import (
    best_lag_row,
    first_threshold_time,
    lag_scan,
    summarize_early_time_audit,
)


def test_lag_scan_positive_shift_means_comparison_later():
    dt = 0.01
    time = np.arange(120, dtype=float) * dt
    reference = np.exp(-0.5 * ((time - 0.42) / 0.035) ** 2)
    comparison = np.exp(-0.5 * ((time - 0.45) / 0.035) ** 2)

    best = best_lag_row(lag_scan(reference, comparison, dt, max_lag_samples=8))

    assert best["lag_samples"] == 3
    assert math.isclose(best["comparison_minus_reference_shift_ns"], 0.03)
    assert best["normalized_correlation"] > 0.99


def test_first_threshold_time_returns_first_abs_crossing():
    time = np.array([0.0, 0.1, 0.2, 0.3])
    values = np.array([0.1, -0.3, 0.6, -1.0])

    assert first_threshold_time(time, values, 0.5) == 0.2


def test_summarize_early_time_rejects_common_mode_as_content_time_zero():
    feature_rows = [
        {
            "profile_id": profile_id,
            "window_label": "early_0p00_0p55",
            "max_abs_time_ns": 0.235756,
        }
        for profile_id in ("013", "014", "015", "016")
    ]
    lag_rows = [
        {
            "pair_label": "short_014_016",
            "window_label": "early_0p00_0p55",
            "comparison_minus_reference_shift_ns": 0.0,
            "normalized_correlation": 0.9998,
            "lag_samples": 0,
        },
        {
            "pair_label": "long_015_013",
            "window_label": "early_0p00_0p55",
            "comparison_minus_reference_shift_ns": 0.0,
            "normalized_correlation": 0.9997,
            "lag_samples": 0,
        },
    ]
    budget = {
        "relative_anchor_offset_ns": 0.127701,
        "conservative_half_width_ns": 0.058939,
    }
    long_shift = {"best_offset_median_ns": 0.06}

    summary = summarize_early_time_audit(feature_rows, lag_rows, budget, long_shift)

    assert summary["policy_label"] == "field_early_time_common_mode_not_content_time_zero"
    assert summary["short_pair_early_shift_ns"] == 0.0
    assert summary["short_pair_early_vs_content_delta_ns"] == 0.127701
    assert summary["short_pair_early_agrees_with_content_budget"] is False
    assert summary["early_peak_time_span_ns"] == 0.0
    assert summary["absolute_time_zero_ready"] is False
    assert summary["field_fwi_ready"] is False
    assert summary["gpu_priority"] == "none"
