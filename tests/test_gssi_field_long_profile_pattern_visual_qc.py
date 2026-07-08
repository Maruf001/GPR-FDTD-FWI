from run_gssi_field_long_profile_pattern_visual_qc import (
    select_stable_anchors,
    summarize_pattern_visual_qc,
)


def test_select_stable_anchors_filters_and_limits_by_rank_score():
    rows = [
        {"x_m": "0.3", "stability_label": "stable_stack_anchor", "candidate_rank_score": "3.0"},
        {"x_m": "0.1", "stability_label": "repeat_limited_anchor", "candidate_rank_score": "9.0"},
        {"x_m": "0.2", "stability_label": "stable_stack_anchor", "candidate_rank_score": "5.0"},
        {"x_m": "0.4", "stability_label": "stable_stack_anchor", "candidate_rank_score": "1.0"},
    ]

    selected = select_stable_anchors(rows, max_anchor_windows=2)

    assert [row["x_m"] for row in selected] == ["0.2", "0.3"]


def test_summarize_pattern_visual_qc_marks_ready_when_all_anchor_windows_improve():
    rows = [
        {"pattern_shift_abs_correlation_gain": 0.12, "pattern_shift_abs_correlation": 0.91},
        {"pattern_shift_abs_correlation_gain": 0.08, "pattern_shift_abs_correlation": 0.86},
    ]

    summary = summarize_pattern_visual_qc(rows, pattern_shift_ns=0.06)

    assert summary["policy_label"] == "long_profile_pattern_visual_qc_ready"
    assert summary["selected_anchor_window_count"] == 2
    assert summary["supported_anchor_window_count"] == 2
    assert summary["min_pattern_shift_gain"] == 0.08
    assert "pattern-QC visualization only" in summary["policy"]


def test_summarize_pattern_visual_qc_marks_limited_when_some_windows_fail():
    rows = [
        {"pattern_shift_abs_correlation_gain": 0.12, "pattern_shift_abs_correlation": 0.91},
        {"pattern_shift_abs_correlation_gain": -0.02, "pattern_shift_abs_correlation": 0.88},
    ]

    summary = summarize_pattern_visual_qc(rows, pattern_shift_ns=0.06)

    assert summary["policy_label"] == "long_profile_pattern_visual_qc_limited"
    assert summary["supported_anchor_window_count"] == 1
