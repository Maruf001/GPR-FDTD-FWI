from run_cross_target_objective_reporting_tiers import (
    reporting_tier,
    summarize_cross_target,
    target_summary_rows,
)


def test_reporting_tier_separates_geometry_zero_width_and_separated():
    assert reporting_tier({
        "geometry_ambiguous": True,
        "competitor_within_ambiguity_threshold": True,
        "ambiguity_candidate_count": 2,
    }) == "geometry_ambiguous_near_tie"
    assert reporting_tier({
        "geometry_ambiguous": False,
        "competitor_within_ambiguity_threshold": True,
        "ambiguity_candidate_count": 2,
    }) == "zero_width_objective_near_tie"
    assert reporting_tier({
        "geometry_ambiguous": False,
        "competitor_within_ambiguity_threshold": False,
        "ambiguity_candidate_count": 1,
    }) == "strict_location_clean_margin_separated"


def test_target_summary_rows_counts_each_target_tier():
    rows = [
        {
            "target_index": 1,
            "strict_location_clean": True,
            "geometry_ambiguous": False,
            "reporting_tier": "zero_width_objective_near_tie",
            "competitor_within_ambiguity_threshold": True,
            "competitor_objective_gap_abs": 0.001,
        },
        {
            "target_index": 2,
            "strict_location_clean": False,
            "geometry_ambiguous": True,
            "reporting_tier": "geometry_ambiguous_near_tie",
            "competitor_within_ambiguity_threshold": True,
            "competitor_objective_gap_abs": 0.002,
        },
        {
            "target_index": 2,
            "strict_location_clean": True,
            "geometry_ambiguous": False,
            "reporting_tier": "strict_location_clean_margin_separated",
            "competitor_within_ambiguity_threshold": False,
            "competitor_objective_gap_abs": 0.003,
        },
    ]

    summary_rows = target_summary_rows(rows)

    assert summary_rows[0]["target_index"] == 1
    assert summary_rows[0]["zero_width_objective_near_tie_count"] == 1
    assert summary_rows[1]["target_index"] == 2
    assert summary_rows[1]["geometry_ambiguous_count"] == 1
    assert summary_rows[1]["strict_clean_margin_separated_count"] == 1


def test_summarize_cross_target_marks_target2_geometry_target1_target2_zero_width():
    summary_rows = [
        {
            "target_index": 0,
            "geometry_ambiguous_count": 0,
            "zero_width_objective_near_tie_count": 0,
            "strict_clean_margin_separated_count": 3,
        },
        {
            "target_index": 1,
            "geometry_ambiguous_count": 0,
            "zero_width_objective_near_tie_count": 9,
            "strict_clean_margin_separated_count": 44,
        },
        {
            "target_index": 2,
            "geometry_ambiguous_count": 21,
            "zero_width_objective_near_tie_count": 9,
            "strict_clean_margin_separated_count": 237,
        },
    ]

    summary = summarize_cross_target([{}] * 323, summary_rows)

    assert summary["policy_label"] == "cross_target_reporting_tiers_target2_geometry_target1_target2_zero_width_cpu_no_gpu"
    assert summary["geometry_ambiguous_targets"] == "2"
    assert summary["zero_width_objective_near_tie_targets"] == "1;2"
    assert summary["gpu_priority"] == "none_now"
