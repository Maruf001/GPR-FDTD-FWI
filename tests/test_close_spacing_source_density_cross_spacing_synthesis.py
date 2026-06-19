from run_close_spacing_source_density_cross_spacing_synthesis import (
    build_comparison_rows,
    gate_rows,
    synthesize_policy,
)


def _source_row(
    family,
    source_count,
    truth_fraction,
    strong_fraction,
    weak_fraction,
    max_x_error,
    *,
    replicated_failure=False,
    near_exact=False,
):
    row_count = 6
    return {
        "family": family,
        "spacing_mm": 50.0 if family == "close50" else 14.0,
        "source_count": source_count,
        "tx_rx_offset_mm": 40.0 if family == "close50" else 45.0,
        "source_summary_csv": "test.csv",
        "archive_evidence_scope": "test_scope",
        "archive_evidence_role": "test_role",
        "row_count": row_count,
        "seed_count": 3,
        "seed_values": "13,21,34",
        "truth_geometry_count": int(round(truth_fraction * row_count)),
        "truth_geometry_fraction": truth_fraction,
        "strong_count": int(round(strong_fraction * row_count)),
        "strong_fraction": strong_fraction,
        "weak_count": int(round(weak_fraction * row_count)),
        "weak_fraction": weak_fraction,
        "selected_wrong_x_count": row_count if replicated_failure else (1 if max_x_error > 0 else 0),
        "min_radius_margin_abs": 0.002 if strong_fraction == 1.0 else 0.0001,
        "max_x_abs_error_mm": max_x_error,
        "max_radius_abs_error_mm": 0.0 if not replicated_failure else 0.5,
        "max_ambiguity_x_width_mm": max_x_error,
        "three_seed_exact": truth_fraction == 1.0,
        "three_seed_near_exact_context": near_exact,
        "replicated_failure": replicated_failure,
    }


def _policy_inputs():
    return (
        {"source_count_transition_supported": True},
        {"source3_near_exact_three_seed_context": True},
        {"source_count_transition_supported_for_close50_txrx40": True},
    )


def test_cross_spacing_policy_blocks_universal_source3_failure():
    rows = [
        _source_row("close50", 3, 0.0, 0.0, 1.0, 1.0, replicated_failure=True),
        _source_row("close50", 4, 1.0, 1.0, 0.0, 0.0),
        _source_row("close50", 5, 1.0, 1.0, 0.0, 0.0),
        _source_row("close14", 3, 5 / 6, 1.0, 0.0, 1.0, near_exact=True),
        _source_row("close14", 4, 1.0, 1.0, 0.0, 0.0),
        _source_row("close14", 5, 1.0, 1.0, 0.0, 0.0),
    ]

    comparisons = build_comparison_rows(rows)
    summary = synthesize_policy(rows, comparisons, *_policy_inputs())
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["source3_spacing_dependent_contrast"] is True
    assert summary["close50_source4_rescue_supported"] is True
    assert summary["close14_source4_incremental_cleanup_supported"] is True
    assert summary["universal_source3_failure_supported"] is False
    assert summary["manuscript_table_ready"] is True
    assert gates["manuscript_source_density_table"]["ready"] is True
    assert gates["cross_spacing_generalization"]["ready"] is False
    assert gates["broad_gpu_queue"]["ready"] is False
    assert summary["gpu_priority"] == "none"


def test_cross_spacing_comparison_rows_capture_directional_deltas():
    rows = [
        _source_row("close50", 3, 0.0, 0.0, 1.0, 1.0, replicated_failure=True),
        _source_row("close50", 4, 1.0, 1.0, 0.0, 0.0),
        _source_row("close50", 5, 1.0, 1.0, 0.0, 0.0),
        _source_row("close14", 3, 5 / 6, 1.0, 0.0, 1.0, near_exact=True),
        _source_row("close14", 4, 1.0, 1.0, 0.0, 0.0),
        _source_row("close14", 5, 1.0, 1.0, 0.0, 0.0),
    ]

    comparisons = {row["comparison_label"]: row for row in build_comparison_rows(rows)}

    assert comparisons["close50_source3_to_source4"]["truth_geometry_fraction_delta"] == 1.0
    assert comparisons["close50_source3_to_source4"]["weak_fraction_delta"] == -1.0
    assert comparisons["source3_close50_to_close14"]["truth_geometry_fraction_delta"] == 5 / 6
    assert comparisons["source3_close50_to_close14"]["right_near_exact"] is True
    assert comparisons["source4_close50_to_close14"]["truth_geometry_fraction_delta"] == 0.0
