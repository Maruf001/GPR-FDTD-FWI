from run_synthetic_2d_publication_claim_boundary_refresh import (
    refreshed_claim_rows,
    summarize_claims,
)


def test_refreshed_claim_rows_replaces_gpu_claim_and_adds_reporting_tiers():
    base_rows = [
        {
            "claim_area": "resolution_limit",
            "allowed_claim": "allowed",
            "not_allowed": "not allowed",
        },
        {
            "claim_area": "gpu_next_step",
            "allowed_claim": "old gpu wording",
            "not_allowed": "old not allowed",
        },
    ]
    tier_summary = {
        "zero_width_objective_near_tie_targets": "1;2",
        "geometry_ambiguous_targets": "2",
    }
    target_rows = [{"target_index": "2", "strict_location_clean_fraction": "0.921348"}]

    rows = refreshed_claim_rows(base_rows, tier_summary, target_rows)
    areas = [row["claim_area"] for row in rows]

    assert areas.count("gpu_next_step") == 1
    assert "resolution_limit" in areas
    assert "reporting_tiers" in areas
    assert "objective_uniqueness" in areas
    assert "target_specificity" in areas
    assert "old gpu wording" not in [row["allowed_claim"] for row in rows]


def test_refreshed_claim_rows_embeds_target_specificity_values():
    rows = refreshed_claim_rows(
        [],
        {
            "zero_width_objective_near_tie_targets": "1;2",
            "geometry_ambiguous_targets": "2",
        },
        [{"target_index": "2", "strict_location_clean_fraction": "0.5"}],
    )

    target_row = next(row for row in rows if row["claim_area"] == "target_specificity")

    assert "target(s) 2" in target_row["allowed_claim"]
    assert "0.500000" in target_row["allowed_claim"]


def test_refreshed_claim_rows_adds_completed_close14_limit():
    rows = refreshed_claim_rows(
        [],
        {
            "zero_width_objective_near_tie_targets": "1;2",
            "geometry_ambiguous_targets": "2",
        },
        [{"target_index": "2", "strict_location_clean_fraction": "0.5"}],
        {
            "row_count": 6,
            "strong_confidence_count": 6,
            "near_tie_count_at_scale_0p5": 6,
        },
    )

    close14_row = next(row for row in rows if row["claim_area"] == "target2_close14_objective_limit")
    gpu_row = next(row for row in rows if row["claim_area"] == "gpu_next_step")

    assert "6 / 6 rows" in close14_row["allowed_claim"]
    assert "0.5x ambiguity gate" in close14_row["allowed_claim"]
    assert "clean lateral resolution" in close14_row["not_allowed"]
    assert "completed target2 close14" in gpu_row["allowed_claim"]


def test_refreshed_claim_rows_adds_close50_seed_frequency_caveat():
    rows = refreshed_claim_rows(
        [],
        {
            "zero_width_objective_near_tie_targets": "1;2",
            "geometry_ambiguous_targets": "2",
        },
        [{"target_index": "2", "strict_location_clean_fraction": "0.5"}],
        None,
        {
            "seed_count": 3,
            "strong_confidence_row_count": 6,
            "confidence_row_count": 6,
            "strict_clean_seed_count": 2,
            "ambiguous_seed_values": "seed13",
        },
    )

    close50_row = next(row for row in rows if row["claim_area"] == "target2_close50_linear29p5_seed_frequency")
    gpu_row = next(row for row in rows if row["claim_area"] == "gpu_next_step")

    assert "6 / 6 rows" in close50_row["allowed_claim"]
    assert "2 / 3 seeds" in close50_row["allowed_claim"]
    assert "seed13 remains" in close50_row["allowed_claim"]
    assert "Do not promote 29.5 mm" in close50_row["not_allowed"]
    assert "completed close50 linear 29.5 mm" in gpu_row["allowed_claim"]


def test_summarize_claims_marks_claim_table_ready_with_no_gpu():
    summary = summarize_claims(
        [{"claim_area": "a"}, {"claim_area": "b"}],
        {
            "policy_label": "tier_policy",
            "geometry_ambiguous_targets": "2",
            "zero_width_objective_near_tie_targets": "1;2",
        },
    )

    assert summary["policy_label"] == "synthetic_2d_publication_claim_boundaries_refreshed_cpu_no_gpu"
    assert summary["claim_boundary_count"] == 2
    assert summary["reporting_tier_policy"] == "tier_policy"
    assert summary["gpu_priority"] == "none"
    assert summary["ready_for_manuscript_claim_table"] is True


def test_summarize_claims_records_completed_close14_probe():
    summary = summarize_claims(
        [{"claim_area": "target2_close14_objective_limit"}],
        {
            "policy_label": "tier_policy",
            "geometry_ambiguous_targets": "2",
            "zero_width_objective_near_tie_targets": "1;2",
        },
        {
            "policy_label": "target2_close14_source5_txrx45_three_seed_persistent_x_near_tie",
            "near_tie_count_at_scale_0p5": 6,
        },
    )

    assert summary["policy_label"] == "synthetic_2d_publication_claim_boundaries_close14_limit_cpu_no_gpu"
    assert summary["close14_probe_included"] is True
    assert summary["close14_probe_near_tie_count_at_scale_0p5"] == 6
    assert summary["gpu_priority"] == "none"


def test_summarize_claims_records_close50_seed_frequency_policy():
    summary = summarize_claims(
        [{"claim_area": "target2_close50_linear29p5_seed_frequency"}],
        {
            "policy_label": "tier_policy",
            "geometry_ambiguous_targets": "2",
            "zero_width_objective_near_tie_targets": "1;2",
        },
        None,
        {
            "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
            "seed_count": 3,
            "ambiguous_seed_count": 1,
            "ambiguous_seed_values": "seed13",
        },
    )

    assert summary["policy_label"] == "synthetic_2d_publication_claim_boundaries_close50_seed_frequency_cpu_no_gpu"
    assert summary["close50_seed_frequency_included"] is True
    assert summary["close50_seed_count"] == 3
    assert summary["close50_ambiguous_seed_values"] == "seed13"
    assert summary["gpu_priority"] == "none"
