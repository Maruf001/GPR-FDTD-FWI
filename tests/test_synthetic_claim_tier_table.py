from run_synthetic_claim_tier_table import claim_tier_rows, summarize_claim_tiers


def test_claim_tier_rows_merge_geometry_and_competitor_summaries():
    geometry_rows = [
        {
            "target_index": "0",
            "exact_strong_row_count": "3",
            "strict_location_clean_count": "3",
            "geometry_ambiguous_count": "0",
        },
        {
            "target_index": "2",
            "exact_strong_row_count": "10",
            "strict_location_clean_count": "8",
            "geometry_ambiguous_count": "2",
        },
    ]
    competitor_rows = [
        {
            "target_index": "0",
            "competitor_separated_count": "3",
            "reported_width_near_tie_count": "0",
            "zero_width_competing_geometry_near_tie_count": "0",
        },
        {
            "target_index": "2",
            "competitor_separated_count": "7",
            "reported_width_near_tie_count": "2",
            "zero_width_competing_geometry_near_tie_count": "1",
        },
    ]

    rows = claim_tier_rows(geometry_rows, competitor_rows)

    assert rows[0]["claim_tier_label"] == "all_objective_unique"
    assert rows[0]["objective_unique_fraction"] == 1.0
    assert rows[1]["claim_tier_label"] == "geometry_and_objective_near_ties"
    assert rows[1]["geometry_clean_row_count"] == 8
    assert rows[1]["objective_unique_row_count"] == 7


def test_claim_tier_rows_marks_geometry_clean_but_objective_caveated():
    rows = claim_tier_rows(
        [{
            "target_index": "1",
            "exact_strong_row_count": "5",
            "strict_location_clean_count": "5",
            "geometry_ambiguous_count": "0",
        }],
        [{
            "target_index": "1",
            "competitor_separated_count": "4",
            "reported_width_near_tie_count": "0",
            "zero_width_competing_geometry_near_tie_count": "1",
        }],
    )

    assert rows[0]["claim_tier_label"] == "geometry_clean_but_objective_near_ties"
    assert "objective uniqueness needs caveats" in rows[0]["recommended_wording"]


def test_summarize_claim_tiers_reports_geometry_and_objective_separation():
    rows = [
        {
            "exact_strong_row_count": 3,
            "geometry_clean_row_count": 3,
            "objective_unique_row_count": 3,
            "reported_width_near_tie_count": 0,
            "zero_width_competing_geometry_near_tie_count": 0,
        },
        {
            "exact_strong_row_count": 10,
            "geometry_clean_row_count": 8,
            "objective_unique_row_count": 7,
            "reported_width_near_tie_count": 2,
            "zero_width_competing_geometry_near_tie_count": 1,
        },
    ]

    summary = summarize_claim_tiers(rows)

    assert summary["policy_label"] == "synthetic_claim_tiers_geometry_clean_and_objective_unique_separated_cpu_no_gpu"
    assert summary["exact_strong_row_count"] == 13
    assert summary["geometry_clean_row_count"] == 11
    assert summary["objective_unique_row_count"] == 10
    assert summary["gpu_priority"] == "none_now"
