import math

from run_gssi_field_short_profile_time_zero_transfer_policy import (
    robust_sigma,
    summarize_time_zero_transfer,
)


def test_robust_sigma_uses_median_absolute_deviation():
    values = [0.10, 0.12, 0.20]

    assert math.isclose(robust_sigma(values), 1.4826 * 0.02)


def test_summarize_time_zero_transfer_labels_limited_qc():
    event_pairs = [
        {
            "comparison_minus_reference_phase_time_ns": "0.1768",
            "aligned_x_residual_mm": "-10.0",
            "radius_match": "False",
        },
        {
            "comparison_minus_reference_phase_time_ns": "0.1081",
            "aligned_x_residual_mm": "-10.0",
            "radius_match": "False",
        },
        {
            "comparison_minus_reference_phase_time_ns": "0.1277",
            "aligned_x_residual_mm": "20.0",
            "radius_match": "False",
        },
    ]
    stack_summary = {
        "stable_stack_anchor_count": 2,
        "best_normalized_correlation": 0.931,
    }

    summary = summarize_time_zero_transfer(
        event_pairs,
        stack_summary,
        max_time_range_ns=0.10,
        max_x_residual_mm=25.0,
        min_correlation=0.90,
    )

    assert summary["policy_label"] == "relative_time_zero_transfer_limited_qc"
    assert summary["timing_consistent"] is True
    assert summary["event_pair_count"] == 3
    assert summary["radius_match_fraction"] == 0.0
    assert math.isclose(summary["median_comparison_minus_reference_phase_time_ns"], 0.1277)


def test_summarize_time_zero_transfer_rejects_large_time_spread():
    event_pairs = [
        {"comparison_minus_reference_phase_time_ns": "0.10", "aligned_x_residual_mm": "0.0"},
        {"comparison_minus_reference_phase_time_ns": "0.30", "aligned_x_residual_mm": "0.0"},
        {"comparison_minus_reference_phase_time_ns": "0.40", "aligned_x_residual_mm": "0.0"},
    ]

    summary = summarize_time_zero_transfer(
        event_pairs,
        {"stable_stack_anchor_count": 2, "best_normalized_correlation": 0.95},
        max_time_range_ns=0.10,
        max_x_residual_mm=25.0,
        min_correlation=0.90,
    )

    assert summary["timing_consistent"] is False
    assert summary["policy_label"] == "relative_time_zero_transfer_pattern_only"

