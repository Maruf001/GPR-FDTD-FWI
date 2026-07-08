import math

import numpy as np

from run_gssi_field_long_profile_transfer_audit import (
    anchor_window_metric_rows,
    crop_x_window,
    summarize_long_transfer_audit,
)


def test_crop_x_window_selects_expected_columns():
    windows = {
        "x_m": np.array([0.0, 0.1, 0.2, 0.3, 0.4]),
        "time_ns": np.array([0.0, 1.0]),
        "reference_window": np.arange(10, dtype=float).reshape(2, 5),
        "raw_aligned_comparison": np.arange(10, 20, dtype=float).reshape(2, 5),
        "corrected_aligned_comparison": np.arange(20, 30, dtype=float).reshape(2, 5),
    }

    crop = crop_x_window(windows, center_x_m=0.2, half_width_m=0.11)

    assert crop["column_start"] == 1
    assert crop["column_end"] == 3
    np.testing.assert_allclose(crop["x_m"], [0.1, 0.2, 0.3])
    assert crop["reference_window"].shape == (2, 3)


def test_anchor_window_metric_rows_uses_stable_anchors_only():
    reference = np.tile(np.linspace(-1.0, 1.0, 24), (5, 1)).T
    raw = np.tile(np.cos(np.linspace(0.0, 2.0 * np.pi, 24)), (5, 1)).T
    windows = {
        "x_m": np.array([0.0, 0.1, 0.2, 0.3, 0.4]),
        "time_ns": np.linspace(0.0, 1.0, 24),
        "reference_window": reference,
        "raw_aligned_comparison": raw,
        "corrected_aligned_comparison": reference.copy(),
    }
    anchors = [
        {"candidate_index": "1", "x_m": "0.2", "stability_label": "stable_stack_anchor"},
        {"candidate_index": "2", "x_m": "0.4", "stability_label": "repeat_limited_anchor"},
    ]

    rows = anchor_window_metric_rows(anchors, windows, half_width_m=0.2, stable_only=True)

    assert len(rows) == 1
    assert rows[0]["anchor_index"] == 1
    assert rows[0]["corrected_anchor_abs_correlation"] > rows[0]["raw_anchor_abs_correlation"]
    assert rows[0]["anchor_abs_correlation_improvement"] > 0.0


def test_summarize_long_transfer_marks_pattern_only_when_strong_but_missing_phase():
    column_rows = [
        {"abs_correlation_improvement": 0.2, "corrected_abs_correlation": 0.9},
        {"abs_correlation_improvement": 0.1, "corrected_abs_correlation": 0.8},
        {"abs_correlation_improvement": -0.01, "corrected_abs_correlation": 0.7},
    ]
    anchor_rows = [
        {"anchor_abs_correlation_improvement": 0.15, "corrected_anchor_abs_correlation": 0.88},
        {"anchor_abs_correlation_improvement": 0.05, "corrected_anchor_abs_correlation": 0.75},
    ]

    summary = summarize_long_transfer_audit(
        column_rows,
        anchor_rows,
        {"absolute_correlation": 0.60},
        {"absolute_correlation": 0.74, "valid_sample_count": 100},
        long_stack_summary={
            "comparison_profile_missing_phase_anchor_picks": True,
            "policy_label": "long_repeat_stack_pattern_only_qc",
        },
        transfer_offset_ns=0.12,
        orientation="direct",
        lag_samples=124,
        lag_mm=413.0,
    )

    assert summary["policy_label"] == "long_profile_short_correction_pattern_only_transfer"
    assert summary["long_pair_missing_phase_anchor_picks"] is True
    assert "cannot support field event pairing" in summary["policy"]


def test_summarize_long_transfer_rejects_negative_matrix_gain():
    summary = summarize_long_transfer_audit(
        [{"abs_correlation_improvement": -0.1, "corrected_abs_correlation": 0.4}],
        [{"anchor_abs_correlation_improvement": -0.05, "corrected_anchor_abs_correlation": 0.5}],
        {"absolute_correlation": 0.70},
        {"absolute_correlation": 0.62},
        long_stack_summary={"comparison_profile_missing_phase_anchor_picks": True},
        transfer_offset_ns=0.12,
        orientation="direct",
        lag_samples=124,
        lag_mm=413.0,
    )

    assert summary["policy_label"] == "long_profile_short_correction_transfer_not_supported"
    assert math.isclose(summary["matrix_abs_correlation_improvement"], -0.08)
