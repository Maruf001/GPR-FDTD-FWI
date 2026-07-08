from run_gssi_field_short_anchor_waveform_coherence_audit import (
    build_gate_rows,
    build_waveform_coherence_rows,
    summarize_waveform_coherence,
)


def _alignment_row(pair_index, radius_match=False):
    return {
        "pair_index": str(pair_index),
        "reference_file": "PROJECT001C__014.DZT",
        "comparison_file": "PROJECT001C__016.DZT",
        "reference_apex_group": str(pair_index),
        "comparison_apex_group": str(pair_index),
        "anchor_content_backed": "True",
        "anchor_reference_x_mm": "403.293",
        "anchor_comparison_aligned_x_mm": "393.294",
        "anchor_aligned_x_residual_mm": "-9.999",
        "reference_best_radius_mm": "8.0",
        "comparison_best_radius_mm": "5.0",
        "radius_match": str(radius_match),
        "raw_field_trace_abs_correlation": "0.30",
        "corrected_field_trace_abs_correlation": "0.94",
        "event_local_field_trace_abs_correlation": "0.98",
        "field_trace_abs_correlation_improvement": "0.64",
        "corrected_field_trace_residual_rms": "0.34",
        "corrected_comparison_minus_reference_phase_time_ns": "0.015",
    }


def _panel_rows(pair_index):
    return [
        {
            "pair_index": str(pair_index),
            "side": "reference",
            "available": "True",
            "radius_mm": "8.0",
            "absolute_correlation": "0.89",
            "normalized_residual_rms": "0.50",
        },
        {
            "pair_index": str(pair_index),
            "side": "comparison",
            "available": "True",
            "radius_mm": "5.0",
            "absolute_correlation": "0.82",
            "normalized_residual_rms": "0.63",
        },
    ]


def test_waveform_rows_mark_morphology_supported_but_not_geometry_seed():
    rows = build_waveform_coherence_rows(
        [_alignment_row(2)],
        _panel_rows(2),
    )

    assert len(rows) == 1
    assert rows[0]["morphology_supported"] is True
    assert rows[0]["radius_match"] is False
    assert rows[0]["geometry_seed_ready"] is False
    assert rows[0]["radius_seed_ready"] is False
    assert rows[0]["panel_radius_span_mm"] == 3.0


def test_summary_allows_waveform_qc_but_blocks_fwi_and_radius():
    rows = build_waveform_coherence_rows(
        [_alignment_row(2), _alignment_row(3)],
        _panel_rows(2) + _panel_rows(3),
    )
    summary = summarize_waveform_coherence(
        rows,
        {"policy_label": "panels"},
        {"policy_label": "alignment"},
        {
            "ready_for_short_relative_timing_qc": True,
            "ready_for_leave_one_content_anchor_claim": False,
        },
        {
            "content_residual_range_mm": 29.997,
            "content_single_translation_supported": False,
        },
        {"ready_for_field_fwi": False},
    )
    gates = build_gate_rows(summary)

    assert summary["content_pair_count"] == 2
    assert summary["waveform_coherent_pair_count"] == 2
    assert summary["ready_for_waveform_morphology_qc"] is True
    assert summary["ready_for_relative_timing_qc"] is True
    assert summary["radius_match_pair_count"] == 0
    assert summary["ready_for_geometry_seed"] is False
    assert summary["ready_for_radius_recovery"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
    assert [row["gate_key"] for row in gates] == [
        "waveform_morphology_qc",
        "relative_timing_qc",
        "geometry_seed",
        "radius_recovery",
        "field_fwi",
    ]
