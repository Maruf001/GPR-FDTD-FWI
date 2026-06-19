import numpy as np

from run_gssi_field_content_backed_waveform_panels import (
    center_trace,
    select_content_backed_candidates,
    summarize_panel_rows,
)


def test_select_content_backed_candidates_uses_reference_and_comparison_only():
    event_rows = [
        {
            "pair_index": "1",
            "content_backed": "False",
            "reference_candidate_id": "ref1",
            "comparison_candidate_id": "cmp1",
        },
        {
            "pair_index": "2",
            "content_backed": "True",
            "content_label": "repeat_content_anchor",
            "reference_candidate_id": "ref2",
            "comparison_candidate_id": "cmp2",
            "pair_min_absolute_correlation": "0.82",
            "pair_mean_absolute_correlation": "0.85",
            "waveform_support_label": "content_backed_waveform_supported_qc",
        },
    ]
    probe_rows = [{"candidate_id": "ref2"}, {"candidate_id": "cmp2"}]

    selected = select_content_backed_candidates(event_rows, probe_rows)

    assert [row["candidate_id"] for row in selected] == ["cmp2", "ref2"]
    assert {row["side"] for row in selected} == {"reference", "comparison"}
    assert all(row["available"] for row in selected)
    assert all(row["pair_index"] == 2 for row in selected)


def test_center_trace_returns_middle_column():
    window = np.arange(12, dtype=float).reshape(4, 3)

    trace = center_trace(window)

    assert trace.tolist() == [1.0, 4.0, 7.0, 10.0]


def test_summarize_panel_rows_reports_visual_qc_scope():
    rows = [
        {"pair_index": 2, "simulation_valid": True, "absolute_correlation": 0.82},
        {"pair_index": 2, "simulation_valid": True, "absolute_correlation": 0.88},
        {"pair_index": 3, "simulation_valid": True, "absolute_correlation": 0.84},
        {"pair_index": 3, "simulation_valid": False, "absolute_correlation": ""},
    ]

    summary = summarize_panel_rows(rows)

    assert summary["policy_label"] == "content_backed_waveform_visual_qc"
    assert summary["panel_count"] == 4
    assert summary["valid_panel_count"] == 3
    assert summary["content_backed_pair_count"] == 2
    assert summary["min_absolute_correlation"] == 0.82
    assert "no field inversion" in summary["policy"]
