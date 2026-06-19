from pathlib import Path

from run_close50_legacy_policy_audit import (
    build_summary,
    classify_acquisition_policy,
    classify_single_seed_policy,
    confidence_summary_from_optimizer,
    pilot_evidence_label,
    threshold_decision,
)


def test_classify_acquisition_policy_identifies_clean_replicated():
    assert classify_acquisition_policy(6, 6, 0, 0.0017) == "clean_replicated"
    assert classify_acquisition_policy(6, 6, 0, 0.0004) == "exact_but_low_margin"
    assert classify_acquisition_policy(12, 4, 12, 0.00006) == "mixed_or_ambiguous"


def test_classify_single_seed_policy_does_not_promote_pilot_to_replicated_clean():
    assert classify_single_seed_policy(2, 2, 0, 0.002) == "single_seed_clean_pilot_not_replicated"
    assert classify_single_seed_policy(4, 4, 4, 0.00047) == "single_seed_exact_but_nonclean"


def test_threshold_decision_uses_first_clean_offset():
    rows = [
        {"tx_rx_offset_mm": 25.0, "branch_policy_label": "mixed_or_ambiguous"},
        {"tx_rx_offset_mm": 30.0, "branch_policy_label": "clean_replicated"},
        {"tx_rx_offset_mm": 35.0, "branch_policy_label": "clean_replicated"},
    ]

    decision = threshold_decision(rows)

    assert decision["policy_label"] == "close50_target2_threshold_resolved_no_gpu_repeat"
    assert decision["first_clean_tx_rx_offset_mm"] == 30.0
    assert decision["ambiguous_tx_rx_offsets_mm"] == "25"
    assert decision["non_clean_tx_rx_offsets_mm"] == "25"
    assert decision["clean_tx_rx_offsets_mm"] == "30,35"


def test_threshold_decision_keeps_nonclean_midpoint_below_clean_threshold():
    rows = [
        {"tx_rx_offset_mm": 25.0, "branch_policy_label": "mixed_or_ambiguous", "replication_scope": "replicated_aggregate"},
        {"tx_rx_offset_mm": 27.5, "branch_policy_label": "single_seed_exact_but_nonclean", "replication_scope": "single_seed_pilot"},
        {"tx_rx_offset_mm": 28.75, "branch_policy_label": "single_seed_exact_but_nonclean", "replication_scope": "single_seed_pilot"},
        {"tx_rx_offset_mm": 30.0, "branch_policy_label": "clean_replicated", "replication_scope": "replicated_aggregate"},
    ]

    decision = threshold_decision(rows)

    assert decision["policy_label"] == "close50_target2_threshold_refined_midpoint_not_clean"
    assert decision["first_clean_tx_rx_offset_mm"] == 30.0
    assert decision["non_clean_tx_rx_offsets_mm"] == "25,27.5,28.75"
    assert decision["single_seed_pilot_tx_rx_offsets_mm"] == "27.5,28.75"
    assert decision["single_seed_nonclean_pilot_tx_rx_offsets_mm"] == "27.5,28.75"


def test_threshold_decision_marks_replicated_nonclean_midpoint():
    rows = [
        {"tx_rx_offset_mm": 25.0, "branch_policy_label": "mixed_or_ambiguous", "replication_scope": "replicated_aggregate"},
        {"tx_rx_offset_mm": 28.75, "branch_policy_label": "single_seed_exact_but_nonclean", "replication_scope": "single_seed_pilot"},
        {"tx_rx_offset_mm": 28.75, "branch_policy_label": "single_seed_exact_but_nonclean", "replication_scope": "single_seed_pilot"},
        {"tx_rx_offset_mm": 30.0, "branch_policy_label": "clean_replicated", "replication_scope": "replicated_aggregate"},
    ]

    decision = threshold_decision(rows)

    assert decision["policy_label"] == "close50_target2_threshold_refined_replicated_midpoint_not_clean"
    assert decision["first_clean_tx_rx_offset_mm"] == 30.0
    assert decision["replicated_midpoint_pilot_tx_rx_offsets_mm"] == "28.75"
    assert decision["replicated_nonclean_midpoint_tx_rx_offsets_mm"] == "28.75"
    assert decision["non_clean_tx_rx_offsets_mm"] == "25,28.75"


def test_confidence_summary_from_optimizer_marks_ambiguous_midpoint_nonclean():
    summary = {
        "run_name": "pilot",
        "sources": 4,
        "tx_rx_offset_mm": 27.5,
        "true_x_values_mm": [190, 250, 300],
        "true_z_values_mm": [90, 90, 90],
        "truth_radius_values_mm": [5, 6, 8],
        "confidence_rows": [
            {
                "step_target_index": 2,
                "best_x_mm": 300,
                "best_z_mm": 90,
                "best_radius_mm": 8,
                "radius_margin_abs": 0.00047,
                "ambiguity_x_min_mm": 300,
                "ambiguity_x_max_mm": 301,
                "ambiguity_radius_min_mm": 7.5,
                "ambiguity_radius_max_mm": 8.0,
            }
        ],
    }

    row = confidence_summary_from_optimizer(summary, "dummy.json", "pilot")

    assert row["tx_rx_offset_mm"] == 27.5
    assert row["truth_geometry_count"] == 1
    assert row["x_ambiguity_row_count"] == 1
    assert row["branch_policy_label"] == "single_seed_exact_but_nonclean"


def test_pilot_evidence_label_extracts_seed_from_run_name():
    summary = {
        "run_name": "coordinate_optimizer_close50_seed13_sources4_txrx28p75_objectives",
        "sources": 4,
        "tx_rx_offset_mm": 28.75,
    }

    assert (
        pilot_evidence_label(summary, Path("outputs/experiments/1316_run/data/summary.json"))
        == "run1316_sources4_txrx28p75_seed13_single_seed_pilot"
    )


def test_confidence_summary_from_optimizer_keeps_x_ambiguous_strong_pilot_nonclean():
    summary = {
        "run_name": "pilot",
        "sources": 4,
        "tx_rx_offset_mm": 28.75,
        "true_x_values_mm": [190, 250, 300],
        "true_z_values_mm": [90, 90, 90],
        "truth_radius_values_mm": [5, 6, 8],
        "confidence_rows": [
            {
                "step_target_index": 2,
                "best_x_mm": 300,
                "best_z_mm": 90,
                "best_radius_mm": 8,
                "radius_margin_abs": 0.0012,
                "ambiguity_x_min_mm": 300,
                "ambiguity_x_max_mm": 301,
                "ambiguity_radius_min_mm": 8,
                "ambiguity_radius_max_mm": 8,
            }
        ],
    }

    row = confidence_summary_from_optimizer(summary, "dummy.json", "pilot")

    assert row["tx_rx_offset_mm"] == 28.75
    assert row["truth_geometry_count"] == 1
    assert row["x_ambiguity_row_count"] == 1
    assert row["branch_policy_label"] == "single_seed_exact_but_nonclean"


def test_build_summary_counts_tracker_mismatches():
    run270 = {"truth_geometry_fraction": 1.0, "radius_margin_abs_min": 0.0025}
    run280 = [{"truth_geometry_fraction": 1.0, "radius_margin_abs_min": 0.0048}]
    threshold = [
        {"tx_rx_offset_mm": 25.0, "branch_policy_label": "mixed_or_ambiguous", "row_count": 12},
        {"tx_rx_offset_mm": 30.0, "branch_policy_label": "clean_replicated", "row_count": 6},
    ]
    tracker = [
        {"tracker_output_slug_match": False},
        {"tracker_output_slug_match": True},
    ]

    summary = build_summary(run270, run280, threshold, tracker)

    assert summary["first_clean_tx_rx_offset_mm"] == 30.0
    assert summary["threshold_row_count"] == 18
    assert summary["tracker_output_mismatch_count"] == 1
