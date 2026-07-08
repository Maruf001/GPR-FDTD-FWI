from run_local_2d_detector_coupled_middle_right_search import (
    branch_summary_rows,
    retained_target_branches,
    summarize_search,
)


def test_retained_target_branches_keeps_best_and_near_ties():
    rows = [
        {"x_mm": 252.0, "z_mm": 89.0, "radius_mm": 6.0, "misfit": 0.066},
        {"x_mm": 250.0, "z_mm": 89.0, "radius_mm": 6.0, "misfit": 0.072},
        {"x_mm": 250.0, "z_mm": 91.0, "radius_mm": 6.0, "misfit": 0.073},
        {"x_mm": 248.0, "z_mm": 91.0, "radius_mm": 6.0, "misfit": 0.084},
    ]

    retained = retained_target_branches(
        rows,
        abs_gap_cutoff=0.01,
        rel_gap_cutoff=0.10,
        max_branches=4,
    )

    assert [row["branch_rank"] for row in retained] == [1, 2]
    assert retained[1]["target1_x_mm"] == 250.0
    assert round(retained[1]["target1_gap_abs"], 6) == 0.006


def test_summarize_search_keeps_broad_gpu_and_fwi_blocked():
    greedy_summary = {
        "run_name": "greedy",
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "final_state": {
            "x_values_mm": [191.0, 252.0, 266.0],
            "z_values_mm": [90.0, 89.0, 91.0],
        },
    }
    branches = [
        {
            "branch_rank": 1,
            "target1_x_mm": 252.0,
            "target1_z_mm": 89.0,
            "target1_radius_mm": 6.0,
            "target1_misfit": 0.066,
            "target1_gap_abs": 0.0,
            "target1_gap_rel": 0.0,
        },
        {
            "branch_rank": 2,
            "target1_x_mm": 250.0,
            "target1_z_mm": 89.0,
            "target1_radius_mm": 6.0,
            "target1_misfit": 0.072,
            "target1_gap_abs": 0.006,
            "target1_gap_rel": 0.091,
        },
    ]
    candidate_rows = [
        {
            "branch_rank": 1,
            "candidate_rank": 1,
            "target1_x_mm": 252.0,
            "target1_z_mm": 89.0,
            "target2_x_mm": 266.0,
            "target2_z_mm": 91.0,
            "coupled_misfit": 0.066,
            "final_linf_error_mm": 2.0,
        },
        {
            "branch_rank": 2,
            "candidate_rank": 1,
            "target1_x_mm": 250.0,
            "target1_z_mm": 89.0,
            "target2_x_mm": 264.0,
            "target2_z_mm": 91.0,
            "coupled_misfit": 0.070,
            "final_linf_error_mm": 1.0,
        },
    ]

    summary = summarize_search(branches, candidate_rows, greedy_summary)
    branch_rows = branch_summary_rows(branches, candidate_rows)

    assert summary["retained_target1_branch_count"] == 2
    assert summary["candidate_count"] == 2
    assert summary["objective_linf_improvement_mm"] == 0.0
    assert summary["oracle_linf_improvement_mm"] == 1.0
    assert summary["target2_true_lateral_selected_by_objective"] is False
    assert summary["target2_true_lateral_available_in_oracle"] is True
    assert summary["ready_for_branch_preserving_selector_evaluation"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert branch_rows[1]["best_final_linf_error_mm"] == 1.0
