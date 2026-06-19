import pytest

from run_gssi_field_content_anchor_trace_alignment_sensitivity import (
    parse_window_configs,
    summarize_sensitivity,
)


def test_parse_window_configs_accepts_multiple_windows():
    configs = parse_window_configs("0.16:0.24:101,0.24:0.36:121")

    assert [config["window_label"] for config in configs] == [
        "pre0.16_post0.24_n101",
        "pre0.24_post0.36_n121",
    ]
    assert configs[1]["window_post_ns"] == 0.36
    assert configs[1]["sample_count"] == 121


def test_parse_window_configs_rejects_bad_shape():
    with pytest.raises(Exception):
        parse_window_configs("0.16:0.24")


def test_summarize_sensitivity_labels_all_pair_windows_improved():
    pair_rows = [
        {"field_trace_abs_correlation_improvement": 0.5, "corrected_field_trace_abs_correlation": 0.9},
        {"field_trace_abs_correlation_improvement": 0.4, "corrected_field_trace_abs_correlation": 0.8},
    ]
    window_rows = [{"window_label": "a"}, {"window_label": "b"}]

    summary = summarize_sensitivity(window_rows, pair_rows)

    assert summary["policy_label"] == "content_anchor_trace_alignment_window_robust"
    assert summary["improved_pair_window_count"] == 2
    assert summary["all_pair_windows_improved"]
    assert summary["min_abs_correlation_improvement"] == 0.4


def test_summarize_sensitivity_labels_mixed_when_one_pair_window_regresses():
    pair_rows = [
        {"field_trace_abs_correlation_improvement": 0.5, "corrected_field_trace_abs_correlation": 0.9},
        {"field_trace_abs_correlation_improvement": -0.1, "corrected_field_trace_abs_correlation": 0.5},
    ]

    summary = summarize_sensitivity([{"window_label": "a"}], pair_rows)

    assert summary["policy_label"] == "content_anchor_trace_alignment_window_mixed"
    assert summary["improved_pair_window_count"] == 1
    assert not summary["all_pair_windows_improved"]
