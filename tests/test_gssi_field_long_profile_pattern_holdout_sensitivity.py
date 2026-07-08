from run_gssi_field_long_profile_pattern_holdout_sensitivity import (
    anchor_summary_rows,
    summarize_sensitivity,
    window_label,
)


def test_window_label_formats_range():
    assert window_label((0.4, 1.15)) == "0.40-1.15 ns"


def test_anchor_summary_rows_counts_all_window_support():
    rows = [
        {
            "anchor_index": 1,
            "center_x_m": 0.2,
            "center_x_mm": 200,
            "stability_label": "repeat_limited_anchor",
            "is_supported": True,
            "pattern_shift_abs_correlation_gain": 0.1,
            "pattern_shift_abs_correlation": 0.9,
        },
        {
            "anchor_index": 1,
            "center_x_m": 0.2,
            "center_x_mm": 200,
            "stability_label": "repeat_limited_anchor",
            "is_supported": False,
            "pattern_shift_abs_correlation_gain": -0.1,
            "pattern_shift_abs_correlation": 0.8,
        },
    ]

    summary = anchor_summary_rows(rows)

    assert summary[0]["supported_window_count"] == 1
    assert summary[0]["all_windows_supported"] is False
    assert summary[0]["min_pattern_shift_gain"] == -0.1


def test_summarize_sensitivity_marks_all_candidate_windows_supported():
    anchor_rows = [
        {
            "anchor_index": 1,
            "stability_label": "stable_stack_anchor",
            "all_windows_supported": True,
            "supported_window_count": 3,
        },
        {
            "anchor_index": 2,
            "stability_label": "repeat_limited_anchor",
            "all_windows_supported": True,
            "supported_window_count": 3,
        },
    ]
    rows = [
        {
            "window_label": "a",
            "is_supported": True,
            "pattern_shift_abs_correlation_gain": 0.1,
            "pattern_shift_abs_correlation": 0.9,
        },
        {
            "window_label": "b",
            "is_supported": True,
            "pattern_shift_abs_correlation_gain": 0.2,
            "pattern_shift_abs_correlation": 0.8,
        },
    ]

    summary = summarize_sensitivity(rows, anchor_rows, pattern_shift_ns=0.06)

    assert summary["policy_label"] == "long_profile_pattern_holdout_sensitivity_all_candidate_anchors_all_windows_supported"
    assert summary["all_window_supported_anchor_count"] == 2
    assert summary["stable_all_window_supported_count"] == 1
    assert summary["repeat_limited_all_window_supported_count"] == 1
    assert summary["gpu_priority"] == "none"


def test_summarize_sensitivity_marks_stable_only_when_repeat_limited_fails():
    anchor_rows = [
        {
            "anchor_index": 1,
            "stability_label": "stable_stack_anchor",
            "all_windows_supported": True,
            "supported_window_count": 3,
        },
        {
            "anchor_index": 2,
            "stability_label": "repeat_limited_anchor",
            "all_windows_supported": False,
            "supported_window_count": 2,
        },
    ]

    summary = summarize_sensitivity([], anchor_rows, pattern_shift_ns=0.06)

    assert summary["policy_label"] == "long_profile_pattern_holdout_sensitivity_stable_all_windows_repeat_limited_mixed"
