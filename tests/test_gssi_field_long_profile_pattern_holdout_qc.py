from run_gssi_field_long_profile_pattern_holdout_qc import (
    annotate_support,
    select_anchor_candidates,
    summarize_holdout_qc,
)


def test_select_anchor_candidates_sorts_and_can_filter_labels():
    rows = [
        {"x_m": "0.3", "stability_label": "stable_stack_anchor"},
        {"x_m": "0.1", "stability_label": "repeat_limited_anchor"},
        {"x_m": "", "stability_label": "stable_stack_anchor"},
        {"x_m": "0.2", "stability_label": "stable_stack_anchor"},
    ]

    selected = select_anchor_candidates(rows, labels={"stable_stack_anchor"})

    assert [row["x_m"] for row in selected] == ["0.2", "0.3"]


def test_annotate_support_requires_positive_gain_and_min_correlation():
    rows = annotate_support([
        {
            "pattern_shift_abs_correlation_gain": 0.03,
            "pattern_shift_abs_correlation": 0.80,
        },
        {
            "pattern_shift_abs_correlation_gain": 0.03,
            "pattern_shift_abs_correlation": 0.70,
        },
    ])

    assert rows[0]["support_label"] == "supported"
    assert rows[0]["is_supported"] is True
    assert rows[1]["support_label"] == "not_supported"
    assert rows[1]["is_supported"] is False


def test_summarize_holdout_qc_keeps_stable_claim_when_repeat_limited_fails():
    rows = annotate_support([
        {
            "stability_label": "stable_stack_anchor",
            "pattern_shift_abs_correlation_gain": 0.08,
            "pattern_shift_abs_correlation": 0.91,
        },
        {
            "stability_label": "repeat_limited_anchor",
            "pattern_shift_abs_correlation_gain": -0.02,
            "pattern_shift_abs_correlation": 0.85,
        },
    ])

    summary = summarize_holdout_qc(rows, pattern_shift_ns=0.06)

    assert summary["policy_label"] == "long_profile_pattern_holdout_qc_stable_supported_repeat_limited_mixed"
    assert summary["stable_supported_anchor_count"] == 1
    assert summary["repeat_limited_supported_anchor_count"] == 0
    assert summary["gpu_priority"] == "none"
