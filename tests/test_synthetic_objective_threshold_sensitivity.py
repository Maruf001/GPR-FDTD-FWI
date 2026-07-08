from run_synthetic_objective_threshold_sensitivity import (
    is_target2_close14_known_x,
    parse_scales,
    summarize_threshold_sensitivity,
    threshold_sensitivity_rows,
)


def _row(sources, txrx, gap, width, tier="competitor_separated"):
    return {
        "target_index": "2",
        "run_name": "coordinate_optimizer_close14_seed34_sources5_txrx45_objectives",
        "sources": str(sources),
        "tx_rx_offset_mm": str(txrx),
        "geometry_delta_class": "x",
        "best_misfit": "10.0",
        "ambiguity_misfit_threshold": str(10.0 + width),
        "competitor_objective_gap_abs": str(gap),
        "near_tie_tier": tier,
    }


def test_is_target2_close14_known_x_requires_target_family_metadata_and_delta():
    assert is_target2_close14_known_x(_row(5, 45, 0.2, 1.0))
    bad_target = _row(5, 45, 0.2, 1.0)
    bad_target["target_index"] = "1"
    assert not is_target2_close14_known_x(bad_target)
    bad_delta = _row(5, 45, 0.2, 1.0)
    bad_delta["geometry_delta_class"] = "z+radius"
    assert not is_target2_close14_known_x(bad_delta)
    missing_offset = _row(5, 45, 0.2, 1.0)
    missing_offset["tx_rx_offset_mm"] = ""
    assert not is_target2_close14_known_x(missing_offset)


def test_threshold_sensitivity_rows_count_scaled_near_ties():
    rows = threshold_sensitivity_rows(
        [
            _row(5, 45, 0.2, 1.0),
            _row(5, 45, 0.6, 1.0),
            _row(4, 45, 0.95, 1.0),
        ],
        parse_scales("0.5,0.75,1.0"),
    )
    by_key = {(row["sources"], row["tx_rx_offset_mm"], row["threshold_scale"]): row for row in rows}

    assert by_key[(5, 45.0, 0.5)]["near_tie_count_at_scale"] == 1
    assert by_key[(5, 45.0, 0.75)]["near_tie_count_at_scale"] == 2
    assert by_key[(4, 45.0, 0.75)]["near_tie_count_at_scale"] == 0
    assert by_key[(4, 45.0, 1.0)]["near_tie_count_at_scale"] == 1
    assert by_key[(4, 45.0, 1.0)]["interpretation"] == "default_threshold_near_tie"


def test_summarize_threshold_sensitivity_marks_source5_persistent():
    rows = threshold_sensitivity_rows(
        [
            _row(5, 45, 0.2, 1.0),
            _row(5, 45, 0.4, 1.0),
            _row(4, 45, 0.99, 1.0),
            _row(7, 45, 0.99, 1.0),
            _row(4, 50, 1.1, 1.0),
        ],
        parse_scales("0.5,0.75,1.0,1.25"),
    )

    summary = summarize_threshold_sensitivity(rows)

    assert summary["policy_label"] == "close14_target2_objective_threshold_sensitivity_source5_persistent_cpu_no_gpu"
    assert summary["near_tie_count_at_scale_0p5"] == 2
    assert summary["near_tie_count_at_scale_1p0"] == 4
    assert summary["near_tie_count_at_scale_1p25"] == 5
    assert summary["source5_txrx45_near_tie_count_at_scale_0p5"] == 2
    assert summary["source4_txrx45_default_threshold_edge_count"] == 1
    assert summary["source7_txrx45_default_threshold_edge_count"] == 1
    assert summary["source4_txrx50_default_near_tie_count"] == 0
    assert summary["source4_txrx50_loose_1p25_near_tie_count"] == 1
    assert summary["gpu_priority"] == "none_now"
    assert "future GPU work should wait" in summary["decision"]
