from run_gssi_field_long_profile_pattern_holdout_width_sensitivity import (
    anchor_summary_rows,
    parse_widths,
    summarize_width_sensitivity,
    width_summary_rows,
)


def test_parse_widths_sorts_and_deduplicates_positive_values():
    assert parse_widths("0.05,0.035,0.05") == [0.035, 0.05]


def test_anchor_and_width_summary_rows_count_support():
    rows = [
        {
            "anchor_index": 1,
            "center_x_m": 0.2,
            "center_x_mm": 200,
            "stability_label": "stable_stack_anchor",
            "anchor_half_width_m": 0.035,
            "is_supported": True,
            "pattern_shift_abs_correlation_gain": 0.1,
            "pattern_shift_abs_correlation": 0.9,
        },
        {
            "anchor_index": 1,
            "center_x_m": 0.2,
            "center_x_mm": 200,
            "stability_label": "stable_stack_anchor",
            "anchor_half_width_m": 0.05,
            "is_supported": False,
            "pattern_shift_abs_correlation_gain": -0.02,
            "pattern_shift_abs_correlation": 0.8,
        },
    ]

    anchors = anchor_summary_rows(rows)
    widths = width_summary_rows(rows)

    assert anchors[0]["supported_width_count"] == 1
    assert anchors[0]["all_widths_supported"] is False
    assert anchors[0]["min_pattern_shift_gain"] == -0.02
    assert widths[0]["supported_anchor_count"] == 1
    assert widths[1]["supported_anchor_count"] == 0


def test_summarize_width_sensitivity_marks_all_widths_supported():
    anchor_rows = [
        {
            "anchor_index": 1,
            "stability_label": "stable_stack_anchor",
            "all_widths_supported": True,
            "supported_width_count": 3,
        },
        {
            "anchor_index": 2,
            "stability_label": "repeat_limited_anchor",
            "all_widths_supported": True,
            "supported_width_count": 3,
        },
    ]
    width_rows = [
        {
            "anchor_half_width_m": 0.035,
            "all_anchors_supported": True,
        },
        {
            "anchor_half_width_m": 0.05,
            "all_anchors_supported": True,
        },
    ]
    rows = [
        {
            "is_supported": True,
            "pattern_shift_abs_correlation_gain": 0.1,
            "pattern_shift_abs_correlation": 0.9,
        }
    ]

    summary = summarize_width_sensitivity(rows, anchor_rows, width_rows, pattern_shift_ns=0.06)

    assert summary["policy_label"] == "long_profile_pattern_holdout_width_sensitivity_all_candidate_anchors_all_widths_supported"
    assert summary["all_width_supported_anchor_count"] == 2
    assert summary["widths_all_anchors_supported_count"] == 2
    assert summary["gpu_priority"] == "none"


def test_summarize_width_sensitivity_marks_stable_only_when_repeat_limited_fails():
    anchor_rows = [
        {
            "anchor_index": 1,
            "stability_label": "stable_stack_anchor",
            "all_widths_supported": True,
        },
        {
            "anchor_index": 2,
            "stability_label": "repeat_limited_anchor",
            "all_widths_supported": False,
        },
    ]
    width_rows = [
        {
            "anchor_half_width_m": 0.035,
            "all_anchors_supported": False,
        }
    ]

    summary = summarize_width_sensitivity([], anchor_rows, width_rows, pattern_shift_ns=0.06)

    assert summary["policy_label"] == "long_profile_pattern_holdout_width_sensitivity_stable_all_widths_repeat_limited_mixed"
