import math

import pytest

from run_gssi_field_long_profile_shift_scan_sensitivity import parse_windows, summarize_sensitivity


def test_parse_windows_reads_semicolon_separated_ranges():
    windows = parse_windows("0.40,1.15;0.45,1.25")

    assert windows == [(0.40, 1.15), (0.45, 1.25)]


def test_parse_windows_rejects_empty_or_reversed_ranges():
    with pytest.raises(ValueError):
        parse_windows("")

    with pytest.raises(ValueError):
        parse_windows("1.0,0.5")


def test_summarize_sensitivity_marks_robust_rejection():
    rows = [
        {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "best_matrix_offset_ns": 0.05,
            "best_matrix_gain_vs_zero": 0.12,
            "short_pair_offset_gain_vs_zero": -0.03,
            "best_anchor_improved_window_count": 6,
        },
        {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "best_matrix_offset_ns": 0.06,
            "best_matrix_gain_vs_zero": 0.11,
            "short_pair_offset_gain_vs_zero": -0.04,
            "best_anchor_improved_window_count": 5,
        },
        {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "best_matrix_offset_ns": 0.07,
            "best_matrix_gain_vs_zero": 0.10,
            "short_pair_offset_gain_vs_zero": -0.02,
            "best_anchor_improved_window_count": 4,
        },
    ]

    summary = summarize_sensitivity(rows)

    assert summary["policy_label"] == "long_profile_pattern_shift_window_robust_rejects_short_transfer"
    assert math.isclose(summary["best_offset_spread_ns"], 0.02)
    assert summary["reject_short_transfer_window_count"] == 3


def test_summarize_sensitivity_marks_variable_when_offsets_spread():
    rows = [
        {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "best_matrix_offset_ns": 0.02,
            "best_matrix_gain_vs_zero": 0.12,
            "short_pair_offset_gain_vs_zero": -0.03,
            "best_anchor_improved_window_count": 6,
        },
        {
            "policy_label": "long_profile_shift_scan_rejects_short_transfer",
            "best_matrix_offset_ns": 0.09,
            "best_matrix_gain_vs_zero": 0.11,
            "short_pair_offset_gain_vs_zero": -0.04,
            "best_anchor_improved_window_count": 5,
        },
    ]

    summary = summarize_sensitivity(rows)

    assert summary["policy_label"] == "long_profile_pattern_shift_window_variable_rejects_short_transfer"
    assert math.isclose(summary["best_offset_spread_ns"], 0.07)
