from run_local_2d_detector_baseline_evidence_reconciliation import (
    evidence_rows,
    gate_rows,
    summarize_reconciliation,
)


def test_reconciliation_separates_weak_simple_detector_from_upper_bound():
    simple = {
        "case_count": 12,
        "all_truth_case_count": 0,
        "target0_hit_count": 0,
        "target1_hit_count": 12,
        "target2_hit_count": 6,
    }
    sensitivity = {
        "case_count": 12,
        "rescued_case_count": 12,
        "any_config_target0_case_count": 12,
        "any_config_target2_case_count": 12,
        "best_config_max_assigned_rank": 36,
    }
    rank = {
        "case_count": 12,
        "minimal_rank_cap_for_full_case_recovery": 40,
        "best_case_count_by_rank_cap": {"top40": 12},
    }
    upper = {
        "case_count": 12,
        "best_rank_gated_upper_bound_all_truth_case_count": 12,
        "minimal_all_case_rank_gated_triples_per_case": 200,
        "ready_for_rank_gated_upper_bound_claim": True,
        "ready_for_detector_seeded_fwi": False,
    }
    source_density_rows = [
        {
            "family": "close14",
            "source_count": 3,
            "row_count": 6,
            "truth_geometry_count": 5,
        }
    ]
    source_density_summary = {"near_exact_nonclose50_source3_families": "close14"}

    rows = evidence_rows(simple, sensitivity, rank, upper, source_density_rows)
    summary = summarize_reconciliation(rows, upper, source_density_summary)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["simple_detector_all_truth_fraction"] == 0.0
    assert summary["sensitivity_rescued_fraction"] == 1.0
    assert summary["minimal_rank_cap_for_full_case_recovery"] == 40
    assert summary["ready_for_rank_gated_upper_bound_claim"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
    assert gates["rank_gated_upper_bound_claim"]["ready"] is True
    assert gates["detector_seeded_fwi"]["ready"] is False
    assert gates["broad_gpu_queue"]["ready"] is False


def test_reconciliation_keeps_detector_seeded_fwi_blocked_when_upper_bound_not_ready():
    rows = [
        {"evidence_key": "simple_top20_detector", "case_count": 2, "all_truth_case_count": 0},
        {"evidence_key": "saved_bscan_parameter_sensitivity", "case_count": 2, "all_truth_case_count": 1},
        {"evidence_key": "candidate_rank_policy", "rank_or_budget": "minimal all-case rank cap 0"},
        {"evidence_key": "rank_gated_upper_bound", "all_truth_case_count": 1},
    ]
    upper = {
        "ready_for_rank_gated_upper_bound_claim": False,
        "ready_for_detector_seeded_fwi": False,
    }
    summary = summarize_reconciliation(rows, upper, {})
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["ready_for_rank_gated_upper_bound_claim"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert gates["rank_gated_upper_bound_claim"]["ready"] is False
    assert gates["detector_seeded_fwi"]["ready"] is False
