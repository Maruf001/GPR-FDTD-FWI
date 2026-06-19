from run_gssi_field_long_profile_stack_policy import summarize_long_policy


def test_summarize_long_policy_marks_pattern_only_when_comparison_missing_phase():
    best = {"orientation": "direct", "lag_mm": -413.0, "normalized_correlation": 0.724}
    direct = {"normalized_correlation": 0.724}
    reversed_best = {"normalized_correlation": 0.575}
    anchors = [{"stability_label": "stable_stack_anchor"} for _ in range(3)]
    skipped = [{"stem": "PROJECT001C__013", "reason": "no_phase_anchor_picks"}]

    summary = summarize_long_policy(best, direct, reversed_best, anchors, skipped)

    assert summary["policy_label"] == "long_repeat_stack_pattern_only_qc"
    assert summary["comparison_profile_missing_phase_anchor_picks"] is True
    assert "does not support field event pairing" in summary["policy"]


def test_summarize_long_policy_requires_stable_anchors_for_candidate():
    best = {"orientation": "direct", "lag_mm": -413.0, "normalized_correlation": 0.724}
    direct = {"normalized_correlation": 0.724}
    reversed_best = {"normalized_correlation": 0.575}
    anchors = [{"stability_label": "stable_stack_anchor"}]

    summary = summarize_long_policy(best, direct, reversed_best, anchors, [])

    assert summary["policy_label"] == "long_repeat_stack_weak_pattern_qc"
    assert summary["stable_stack_anchor_count"] == 1
