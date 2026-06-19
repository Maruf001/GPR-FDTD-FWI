from run_gssi_field_short_anchor_signed_morphology_audit import (
    build_gate_rows,
    build_signed_morphology_rows,
    signed_correlation,
    summarize_signed_morphology,
)


def _alignment_rows():
    return [
        {
            "pair_index": "1",
            "anchor_content_backed": "False",
            "raw_field_trace_abs_correlation": "0.1",
            "raw_field_trace_polarity": "same",
            "corrected_field_trace_abs_correlation": "0.2",
            "corrected_field_trace_polarity": "same",
        },
        {
            "pair_index": "2",
            "reference_file": "ref.dzt",
            "comparison_file": "cmp.dzt",
            "reference_apex_group": "2",
            "comparison_apex_group": "2",
            "anchor_content_backed": "True",
            "anchor_reference_x_mm": "403",
            "anchor_comparison_aligned_x_mm": "393",
            "anchor_aligned_x_residual_mm": "-10",
            "reference_best_radius_mm": "8",
            "comparison_best_radius_mm": "5",
            "radius_match": "False",
            "raw_field_trace_abs_correlation": "0.35",
            "raw_field_trace_polarity": "same",
            "corrected_field_trace_abs_correlation": "0.94",
            "corrected_field_trace_polarity": "same",
            "event_local_field_trace_abs_correlation": "0.99",
            "field_trace_abs_correlation_improvement": "0.59",
            "corrected_comparison_minus_reference_phase_time_ns": "-0.02",
            "corrected_field_trace_residual_rms": "0.35",
        },
        {
            "pair_index": "3",
            "reference_file": "ref.dzt",
            "comparison_file": "cmp.dzt",
            "reference_apex_group": "3",
            "comparison_apex_group": "1",
            "anchor_content_backed": "True",
            "anchor_reference_x_mm": "693",
            "anchor_comparison_aligned_x_mm": "713",
            "anchor_aligned_x_residual_mm": "20",
            "reference_best_radius_mm": "8",
            "comparison_best_radius_mm": "5",
            "radius_match": "False",
            "raw_field_trace_abs_correlation": "0.25",
            "raw_field_trace_polarity": "same",
            "corrected_field_trace_abs_correlation": "0.98",
            "corrected_field_trace_polarity": "same",
            "event_local_field_trace_abs_correlation": "0.98",
            "field_trace_abs_correlation_improvement": "0.73",
            "corrected_comparison_minus_reference_phase_time_ns": "0.0",
            "corrected_field_trace_residual_rms": "0.15",
        },
    ]


def _radius_summary():
    return {
        "policy_label": "radius_degenerate",
        "weak_radius_side_count": 4,
        "selected_radius_mismatch_pair_count": 2,
        "common_radius_near_tie_pair_count": 2,
        "ready_for_radius_seed": False,
        "ready_for_radius_recovery": False,
        "ready_for_geometry_seed": False,
        "ready_for_field_fwi": False,
    }


def test_signed_correlation_encodes_polarity():
    assert signed_correlation("0.75", "same") == 0.75
    assert signed_correlation("0.75", "opposite") == -0.75


def test_build_rows_filters_to_content_backed_pairs_and_requires_same_polarity():
    rows = build_signed_morphology_rows(_alignment_rows(), _radius_summary())

    assert [row["pair_index"] for row in rows] == [2, 3]
    assert all(row["corrected_field_trace_polarity"] == "same" for row in rows)
    assert all(row["signed_morphology_supported"] for row in rows)
    assert not any(row["amplitude_calibration_ready"] for row in rows)
    assert not any(row["radius_seed_ready"] for row in rows)


def test_summary_allows_signed_morphology_qc_but_blocks_inversion():
    rows = build_signed_morphology_rows(_alignment_rows(), _radius_summary())
    summary = summarize_signed_morphology(
        rows,
        {"policy_label": "alignment"},
        {"policy_label": "coherence"},
        _radius_summary(),
    )
    gates = {row["gate_key"]: row for row in build_gate_rows(summary)}

    assert summary["policy_label"] == "gssi51600s_field_short_anchor_signed_morphology_qc_only"
    assert summary["content_pair_count"] == 2
    assert summary["signed_morphology_supported_pair_count"] == 2
    assert summary["corrected_same_polarity_pair_count"] == 2
    assert summary["min_corrected_signed_correlation"] == 0.94
    assert summary["ready_for_signed_waveform_morphology_qc"]
    assert not summary["ready_for_absolute_amplitude_calibration"]
    assert not summary["ready_for_radius_seed"]
    assert not summary["ready_for_field_fwi"]
    assert summary["gpu_priority"] == "none"
    assert gates["signed_waveform_morphology_qc"]["ready"]
    assert not gates["absolute_amplitude_calibration"]["ready"]
    assert not gates["field_fwi"]["ready"]
