from run_synthetic_objective_uniqueness_family_gap_context import (
    family_gap_rows,
    family_label,
    summarize_family_gaps,
)


def test_family_label_classifies_close14_before_generic_target2():
    assert family_label({"target_index": "2", "run_name": "coordinate_optimizer_close14_seed34"}) == "target2_close14"
    assert (
        family_label({"target_index": "2", "run_name": "coordinate_optimizer_variable_depth_radius_seed55"})
        == "target2_variable_depth_radius"
    )
    assert (
        family_label({"target_index": "1", "run_name": "coordinate_optimizer_noise10_seed13"})
        == "target1_legacy_archive"
    )


def test_family_gap_rows_identify_known_close14_target2_x_gap():
    rows = family_gap_rows([
        {
            "target_index": "2",
            "run_name": "coordinate_optimizer_close14_seed34_sources5_txrx45",
            "sources": "5",
            "tx_rx_offset_mm": "45",
            "near_tie_tier": "reported_width_near_tie",
            "geometry_delta_class": "x",
            "competitor_objective_gap_abs": "0.0003",
        },
        {
            "target_index": "2",
            "run_name": "coordinate_optimizer_close14_seed34_sources5_txrx45",
            "sources": "5",
            "tx_rx_offset_mm": "45",
            "near_tie_tier": "competitor_separated",
            "geometry_delta_class": "x",
            "competitor_objective_gap_abs": "0.002",
        },
        {
            "target_index": "1",
            "run_name": "coordinate_optimizer_noise10_seed13",
            "sources": "",
            "tx_rx_offset_mm": "",
            "near_tie_tier": "zero_width_competing_geometry_near_tie",
            "geometry_delta_class": "z+radius",
            "competitor_objective_gap_abs": "0.0011",
        },
    ])
    by_action = {row["actionability_label"]: row for row in rows}

    close14 = by_action["known_close14_target2_x_gap"]
    assert close14["family_label"] == "target2_close14"
    assert close14["known_acquisition_near_tie_count"] == 1
    assert close14["near_tie_source_labels"] == "5"
    assert close14["near_tie_tx_rx_offset_labels"] == "45mm"
    assert close14["gpu_priority"] == "low_conditional_after_objective_scope"

    archive = by_action["archive_or_metadata_claim_caveat"]
    assert archive["family_label"] == "target1_legacy_archive"
    assert archive["gpu_priority"] == "none_archive_claim_caveat"


def test_summarize_family_gaps_separates_close14_from_close50():
    summary = summarize_family_gaps([
        {
            "family_label": "target2_close14",
            "near_tie_row_count": 4,
            "known_acquisition_near_tie_count": 4,
            "actionability_label": "known_close14_target2_x_gap",
        },
        {
            "family_label": "target2_variable_depth_radius",
            "near_tie_row_count": 2,
            "known_acquisition_near_tie_count": 2,
            "actionability_label": "known_target2_depth_radius_gap",
        },
        {
            "family_label": "target1_legacy_archive",
            "near_tie_row_count": 9,
            "known_acquisition_near_tie_count": 0,
            "actionability_label": "archive_or_metadata_claim_caveat",
        },
        {
            "family_label": "target2_close50",
            "near_tie_row_count": 2,
            "known_acquisition_near_tie_count": 0,
            "actionability_label": "archive_or_metadata_claim_caveat",
        },
    ])

    assert summary["policy_label"] == "objective_uniqueness_family_context_close14_target2_cpu_no_gpu"
    assert summary["near_tie_row_count"] == 17
    assert summary["known_close14_target2_x_near_tie_count"] == 4
    assert summary["known_target2_depth_radius_near_tie_count"] == 2
    assert summary["target1_legacy_archive_near_tie_count"] == 9
    assert summary["target2_close50_known_near_tie_count"] == 0
    assert summary["gpu_priority"] == "none_now"
    assert "not close50" in summary["decision"]
