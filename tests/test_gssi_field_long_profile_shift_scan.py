import math

from run_gssi_field_long_profile_shift_scan import closest_row, summarize_shift_scan


def test_closest_row_returns_nearest_offset():
    rows = [{"offset_ns": -0.1}, {"offset_ns": 0.03}, {"offset_ns": 0.14}]

    row = closest_row(rows, 0.12)

    assert row["offset_ns"] == 0.14


def test_summarize_shift_scan_rejects_short_transfer_when_it_hurts_matrix():
    rows = [
        {
            "offset_ns": 0.0,
            "matrix_abs_correlation": 0.76,
            "improved_anchor_window_count": 0,
            "mean_anchor_abs_correlation_improvement": -0.02,
            "min_corrected_anchor_abs_correlation": 0.6,
        },
        {
            "offset_ns": 0.13,
            "matrix_abs_correlation": 0.73,
            "improved_anchor_window_count": 0,
            "mean_anchor_abs_correlation_improvement": -0.12,
            "min_corrected_anchor_abs_correlation": 0.5,
        },
        {
            "offset_ns": -0.08,
            "matrix_abs_correlation": 0.79,
            "improved_anchor_window_count": 2,
            "mean_anchor_abs_correlation_improvement": 0.04,
            "min_corrected_anchor_abs_correlation": 0.7,
        },
    ]

    summary = summarize_shift_scan(
        rows,
        short_pair_transfer_offset_ns=0.1277,
        long_pair_missing_phase_anchor_picks=True,
        offset_step_ns=0.01,
    )

    assert summary["policy_label"] == "long_profile_shift_scan_rejects_short_transfer"
    assert summary["nearest_short_pair_scan_offset_ns"] == 0.13
    assert summary["best_matrix_offset_ns"] == -0.08
    assert math.isclose(summary["short_pair_offset_gain_vs_zero"], -0.03)
    assert math.isclose(summary["best_matrix_gain_vs_zero"], 0.03)
    assert summary["long_pair_missing_phase_anchor_picks"] is True


def test_summarize_shift_scan_marks_pattern_only_candidate_with_strong_anchor_support():
    rows = [
        {
            "offset_ns": 0.0,
            "matrix_abs_correlation": 0.60,
            "improved_anchor_window_count": 0,
            "mean_anchor_abs_correlation_improvement": 0.0,
            "min_corrected_anchor_abs_correlation": 0.6,
        },
        {
            "offset_ns": 0.10,
            "matrix_abs_correlation": 0.67,
            "improved_anchor_window_count": 4,
            "mean_anchor_abs_correlation_improvement": 0.08,
            "min_corrected_anchor_abs_correlation": 0.74,
        },
    ]

    summary = summarize_shift_scan(
        rows,
        short_pair_transfer_offset_ns=0.10,
        long_pair_missing_phase_anchor_picks=True,
        offset_step_ns=0.01,
    )

    assert summary["policy_label"] == "long_profile_shift_scan_pattern_only_candidate"
    assert "not time-zero calibration" in summary["policy"]


def test_summarize_shift_scan_marks_no_stable_transfer_when_gain_is_small():
    rows = [
        {
            "offset_ns": 0.0,
            "matrix_abs_correlation": 0.60,
            "improved_anchor_window_count": 0,
            "mean_anchor_abs_correlation_improvement": 0.0,
            "min_corrected_anchor_abs_correlation": 0.6,
        },
        {
            "offset_ns": 0.10,
            "matrix_abs_correlation": 0.61,
            "improved_anchor_window_count": 1,
            "mean_anchor_abs_correlation_improvement": 0.01,
            "min_corrected_anchor_abs_correlation": 0.62,
        },
    ]

    summary = summarize_shift_scan(
        rows,
        short_pair_transfer_offset_ns=0.10,
        long_pair_missing_phase_anchor_picks=True,
        offset_step_ns=0.01,
    )

    assert summary["policy_label"] == "long_profile_shift_scan_no_stable_transfer"
