from run_close50_sampling_boundary_synthesis import (
    linear_boundary_rows,
    nearest_boundary_rows,
    summarize_sampling_boundary,
)


def test_nearest_boundary_rows_group_replicated_midpoint_nonclean():
    rows = nearest_boundary_rows(
        [
            {
                "tx_rx_offset_mm": "28.75",
                "row_count": "2",
                "truth_geometry_count": "2",
                "x_ambiguity_row_count": "2",
                "radius_margin_abs_min": "0.0012",
                "branch_policy_label": "single_seed_exact_but_nonclean",
                "replication_scope": "single_seed_pilot",
            },
            {
                "tx_rx_offset_mm": "28.75",
                "row_count": "2",
                "truth_geometry_count": "2",
                "x_ambiguity_row_count": "1",
                "radius_margin_abs_min": "0.0017",
                "branch_policy_label": "single_seed_exact_but_nonclean",
                "replication_scope": "single_seed_pilot",
            },
            {
                "tx_rx_offset_mm": "30",
                "row_count": "6",
                "truth_geometry_count": "6",
                "x_ambiguity_row_count": "0",
                "radius_margin_abs_min": "0.0017",
                "branch_policy_label": "clean_replicated",
                "replication_scope": "replicated_aggregate",
            },
        ]
    )

    by_offset = {row["tx_rx_offset_mm"]: row for row in rows}
    assert by_offset[28.75]["boundary_status"] == "replicated_nonclean"
    assert by_offset[28.75]["evidence_row_count"] == 4
    assert by_offset[28.75]["x_ambiguity_row_count"] == 3
    assert by_offset[30.0]["boundary_status"] == "clean_replicated"
    assert by_offset[30.0]["clean_threshold_candidate"] is True


def test_linear_boundary_rows_include_three_seed_29p5_and_seed13_29p75():
    rows = linear_boundary_rows(
        {
            "policy_label": "linear29",
            "seed_count": 3,
            "confidence_row_count": 6,
            "truth_geometry_row_count": 6,
            "strict_clean_row_count": 5,
            "x_ambiguity_row_count": 1,
            "radius_margin_abs_min": 0.0014,
        },
        [],
        [
            {
                "seed_label": "seed13",
                "tx_rx_offset_mm": "29.75",
                "truth_geometry_match": "True",
                "strict_clean_row": "False",
                "x_ambiguity_width_mm": "1.0",
                "radius_margin_abs": "0.002",
            },
            {
                "seed_label": "seed13",
                "tx_rx_offset_mm": "29.75",
                "truth_geometry_match": "True",
                "strict_clean_row": "True",
                "x_ambiguity_width_mm": "0.0",
                "radius_margin_abs": "0.0021",
            },
        ],
    )

    by_offset = {row["tx_rx_offset_mm"]: row for row in rows}
    assert by_offset[29.5]["seed_or_replication_count"] == 3
    assert by_offset[29.5]["boundary_status"] == "exact_strong_not_clean"
    assert by_offset[29.75]["seed_or_replication_count"] == 1
    assert by_offset[29.75]["x_ambiguity_row_count"] == 1
    assert by_offset[29.75]["clean_threshold_candidate"] is False


def test_sampling_summary_keeps_30mm_nearest_clean_and_gpu_blocked():
    rows = [
        {
            "sampling_family": "nearest_receiver",
            "tx_rx_offset_mm": 28.75,
            "boundary_status": "replicated_nonclean",
        },
        {
            "sampling_family": "nearest_receiver",
            "tx_rx_offset_mm": 30.0,
            "boundary_status": "clean_replicated",
        },
        {
            "sampling_family": "linear_receiver",
            "tx_rx_offset_mm": 29.5,
            "boundary_status": "exact_strong_not_clean",
        },
    ]

    summary = summarize_sampling_boundary(
        rows,
        {
            "run270_truth_geometry_fraction": 1.0,
            "run280_txrx40_truth_geometry_fraction": 1.0,
        },
        {
            "seed_count": 3,
            "ambiguous_seed_count": 1,
            "ambiguous_seed_values": "seed13",
            "strict_clean_row_count": 5,
            "confidence_row_count": 6,
        },
        {"ready_for_manuscript_claim_table": True},
    )

    assert summary["nearest_first_clean_replicated_tx_rx_mm"] == 30.0
    assert summary["nearest_max_nonclean_below_clean_mm"] == 28.75
    assert summary["linear_exact_strong_not_clean_offsets_mm"] == "29.5"
    assert summary["ready_for_paper_sampling_boundary"] is True
    assert summary["ready_for_sub30_clean_threshold_claim"] is False
    assert summary["ready_for_gpu_probe"] is False
    assert summary["gpu_priority"] == "none"
