import math

from run_synthetic_2d_resolution_claim_map import resolution_claim_rows, summarize_map


def _inputs():
    physical_summary = {
        "group_count": 4,
        "clean_nonoverlap_group_count": 2,
        "clean_overlap_stress_group_count": 1,
        "decision": "close14 tangent non-overlap; close10 overlap stress",
    }
    physical_group_rows = [
        {
            "close_spacing_mm": "14",
            "policy_label": "clean_replicated",
            "is_physical_nonoverlap": "True",
        },
        {
            "close_spacing_mm": "20",
            "policy_label": "clean_replicated",
            "is_physical_nonoverlap": "True",
        },
        {
            "close_spacing_mm": "10",
            "policy_label": "clean_replicated",
            "is_physical_nonoverlap": "False",
        },
        {
            "close_spacing_mm": "25",
            "policy_label": "mixed_or_failed",
            "is_physical_nonoverlap": "True",
        },
    ]
    claim_tier_summary = {
        "policy_label": "synthetic_claim_tiers_geometry_clean_and_objective_unique_separated_cpu_no_gpu",
    }
    claim_tier_rows = [
        {
            "target_index": "0",
            "exact_strong_row_count": "3",
            "objective_unique_row_count": "3",
            "objective_unique_fraction": "1.0",
            "claim_tier_label": "all_objective_unique",
            "recommended_wording": "all wording",
        },
        {
            "target_index": "2",
            "exact_strong_row_count": "267",
            "objective_unique_row_count": "237",
            "objective_unique_fraction": "0.8876404494382022",
            "claim_tier_label": "geometry_and_objective_near_ties",
            "recommended_wording": "needs caveats",
        },
    ]
    close14_summary = {
        "policy_label": "target2_close14_source5_txrx45_three_seed_persistent_x_near_tie",
        "row_count": 6,
        "strong_confidence_count": 6,
        "near_tie_count_at_scale_0p5": 6,
    }
    close50_summary = {
        "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
        "seed_count": 3,
        "strict_clean_seed_count": 2,
        "ambiguous_seed_values": "seed13",
    }
    claim_boundary_summary = {
        "policy_label": "synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu",
    }
    next_matrix_summary = {
        "policy_label": "synthetic_2d_next_question_matrix_cpu_first_no_gpu",
        "candidate_count": 7,
        "conditional_gpu_candidate_count": 0,
    }
    return (
        physical_summary,
        physical_group_rows,
        claim_tier_summary,
        claim_tier_rows,
        close14_summary,
        close50_summary,
        claim_boundary_summary,
        next_matrix_summary,
    )


def test_resolution_claim_rows_keep_physical_spacing_and_overlap_stress_separate():
    rows = resolution_claim_rows(*_inputs())
    by_key = {row["map_key"]: row for row in rows}

    assert by_key["physical_nonoverlap_guardrail"]["primary_metric_value"] == 14
    assert by_key["physical_nonoverlap_guardrail"]["support_fraction"] == 0.5
    assert "overlapping-cylinder stress tests" in by_key["physical_nonoverlap_guardrail"]["not_allowed"]
    assert by_key["overlap_stress_test_boundary"]["primary_metric_value"] == 10
    assert by_key["overlap_stress_test_boundary"]["claim_status"] == "blocked_for_physical_spacing"
    assert by_key["target2_claim_tier"]["support_fraction"] == 237 / 267


def test_resolution_claim_rows_encode_close14_close50_and_no_gpu_caveats():
    rows = resolution_claim_rows(*_inputs())
    by_key = {row["map_key"]: row for row in rows}

    close14 = by_key["target2_close14_source5_txrx45_objective_limit"]
    close50 = by_key["target2_close50_linear29p5_seed_frequency"]
    gpu = by_key["current_synthetic_gpu_queue"]

    assert close14["support_fraction"] == 1.0
    assert close14["primary_metric_value"] == 6
    assert "+1 mm x competitor" in close14["not_allowed"]
    assert close50["support_fraction"] == 2 / 3
    assert close50["primary_metric_value"] == 2 / 3
    assert "seed13 remains x-ambiguous" in close50["not_allowed"]
    assert gpu["primary_metric_value"] == 0
    assert gpu["claim_status"] == "no_current_gpu_candidate"


def test_summarize_map_reports_current_resolution_endpoint():
    inputs = _inputs()
    rows = resolution_claim_rows(*inputs)
    summary = summarize_map(rows, inputs[4], inputs[5], inputs[7])

    assert summary["policy_label"] == "synthetic_2d_resolution_claim_map_close14_close50_current_cpu_no_gpu"
    assert summary["row_count"] == len(rows)
    assert summary["blocked_physical_claim_row_count"] == 1
    assert summary["physical_nonoverlap_guardrail_mm"] == 14
    assert summary["overlap_stress_min_clean_spacing_mm"] == 10
    assert summary["target2_close14_near_tie_rows_at_0p5"] == 6
    assert summary["target2_close50_strict_clean_seed_count"] == 2
    assert summary["target2_close50_ambiguous_seed_values"] == "seed13"
    assert summary["conditional_gpu_candidate_count"] == 0
    assert summary["gpu_priority"] == "none_now"
    assert math.isfinite(summary["physical_nonoverlap_guardrail_mm"])
