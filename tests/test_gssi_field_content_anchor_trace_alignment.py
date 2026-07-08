import numpy as np

from run_gssi_field_content_anchor_trace_alignment import (
    compare_traces,
    summarize_alignment,
    supported_anchor_pairs,
)


def test_supported_anchor_pairs_keeps_only_content_time_zero_supported_pairs():
    anchor_rows = [
        {
            "pair_index": "1",
            "anchor_policy_label": "timing_only_no_content_anchor",
        },
        {
            "pair_index": "2",
            "anchor_policy_label": "content_time_zero_anchor_supported",
            "content_backed": "True",
        },
    ]
    applied_rows = [
        {"pair_index": "1", "reference_file": "ref", "comparison_file": "cmp"},
        {"pair_index": "2", "reference_file": "ref", "comparison_file": "cmp"},
    ]

    selected = supported_anchor_pairs(anchor_rows, applied_rows)

    assert [row["pair_index"] for row in selected] == ["2"]
    assert selected[0]["anchor_content_backed"] == "True"


def test_compare_traces_reports_higher_correlation_after_shift_alignment():
    x = np.linspace(-1.0, 1.0, 101)
    reference = np.exp(-((x - 0.0) / 0.20) ** 2)
    raw = np.exp(-((x - 0.35) / 0.20) ** 2)
    corrected = np.exp(-((x - 0.0) / 0.20) ** 2)

    raw_cmp = compare_traces(reference, raw)
    corrected_cmp = compare_traces(reference, corrected)

    assert corrected_cmp["absolute_correlation"] > raw_cmp["absolute_correlation"]
    assert corrected_cmp["absolute_correlation"] > 0.99


def test_summarize_alignment_labels_all_improved_pairs():
    rows = [
        {
            "raw_field_trace_abs_correlation": 0.2,
            "corrected_field_trace_abs_correlation": 0.7,
            "field_trace_abs_correlation_improvement": 0.5,
            "corrected_comparison_minus_reference_phase_time_ns": 0.01,
        },
        {
            "raw_field_trace_abs_correlation": 0.4,
            "corrected_field_trace_abs_correlation": 0.8,
            "field_trace_abs_correlation_improvement": 0.4,
            "corrected_comparison_minus_reference_phase_time_ns": -0.02,
        },
    ]

    summary = summarize_alignment(rows)

    assert summary["policy_label"] == "content_anchor_field_trace_alignment_improves_after_time_zero"
    assert summary["supported_anchor_pair_count"] == 2
    assert summary["field_trace_alignment_improved_count"] == 2
    assert summary["mean_abs_correlation_improvement"] == 0.45
