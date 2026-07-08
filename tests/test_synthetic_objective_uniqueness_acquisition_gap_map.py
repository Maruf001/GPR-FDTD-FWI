from run_synthetic_objective_uniqueness_acquisition_gap_map import (
    acquisition_gap_rows,
    summarize_gap_map,
)


def test_acquisition_gap_rows_separate_known_target2_x_gap_from_archive_caveat():
    rows = acquisition_gap_rows([
        {
            "target_index": "2",
            "sources": "5",
            "tx_rx_offset_mm": "45",
            "near_tie_tier": "reported_width_near_tie",
            "geometry_delta_class": "x",
            "competitor_objective_gap_abs": "0.0002",
        },
        {
            "target_index": "2",
            "sources": "5",
            "tx_rx_offset_mm": "45",
            "near_tie_tier": "competitor_separated",
            "geometry_delta_class": "x",
            "competitor_objective_gap_abs": "0.002",
        },
        {
            "target_index": "1",
            "sources": "",
            "tx_rx_offset_mm": "",
            "near_tie_tier": "zero_width_competing_geometry_near_tie",
            "geometry_delta_class": "z+radius",
            "competitor_objective_gap_abs": "0.0011",
        },
    ])
    by_action = {row["actionability_label"]: row for row in rows}

    known = by_action["known_acquisition_x_resolution_gap"]
    assert known["target_index"] == 2
    assert known["sources_label"] == "5"
    assert known["tx_rx_offset_label"] == "45mm"
    assert known["exact_strong_row_count"] == 2
    assert known["near_tie_row_count"] == 1
    assert known["objective_unique_fraction"] == 0.5
    assert known["gpu_priority"] == "low_conditional_after_objective_scope"

    archive = by_action["archive_metadata_gap"]
    assert archive["target_index"] == 1
    assert archive["near_tie_row_count"] == 1
    assert archive["gpu_priority"] == "none_archive_claim_caveat"
    assert "archive metadata" in archive["recommended_action"]


def test_summarize_gap_map_keeps_gpu_priority_cpu_first():
    rows = [
        {
            "target_index": 2,
            "metadata_status": "known_sources_and_txrx",
            "exact_strong_row_count": 2,
            "near_tie_row_count": 1,
            "actionability_label": "known_acquisition_x_resolution_gap",
            "sources_label": "5",
            "tx_rx_offset_label": "45mm",
        },
        {
            "target_index": 1,
            "metadata_status": "archive_missing_sources_and_txrx",
            "exact_strong_row_count": 3,
            "near_tie_row_count": 3,
            "actionability_label": "archive_metadata_gap",
            "sources_label": "unknown",
            "tx_rx_offset_label": "unknown",
        },
    ]

    summary = summarize_gap_map(rows)

    assert summary["policy_label"] == "objective_uniqueness_gap_map_known_target2_x_gaps_cpu_no_gpu"
    assert summary["exact_strong_row_count"] == 5
    assert summary["near_tie_row_count"] == 4
    assert summary["known_acquisition_near_tie_row_count"] == 1
    assert summary["archive_metadata_near_tie_row_count"] == 3
    assert summary["target1_known_acquisition_near_tie_row_count"] == 0
    assert summary["target2_known_acquisition_near_tie_row_count"] == 1
    assert summary["known_actionable_cell_count"] == 1
    assert summary["top_actionable_target_index"] == 2
    assert summary["gpu_priority"] == "none_now"
    assert "narrow target2 probe" in summary["decision"]
