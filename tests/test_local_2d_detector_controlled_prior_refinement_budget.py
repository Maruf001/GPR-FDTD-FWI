from run_local_2d_detector_controlled_prior_refinement_budget import (
    build_budget_rows,
    gate_rows,
    radius_scope_rows,
    summarize_budget,
)


def _branch_rows():
    return [
        {
            "branch_key": "target2_close14",
            "recommended_half_width_mm": "10",
            "fine_step_mm": "2",
            "coarse_step_mm": "5",
            "stable_seed_case_count": "6",
            "review_case_count": "0",
            "per_case_xz_grid_points_fine": "1771561",
            "stable_total_xz_grid_points_fine": "10629366",
            "per_case_xz_grid_points_coarse": "15625",
            "stable_total_xz_grid_points_coarse": "93750",
        },
        {
            "branch_key": "target2_close50_linear29p5",
            "recommended_half_width_mm": "12",
            "fine_step_mm": "2",
            "coarse_step_mm": "5",
            "stable_seed_case_count": "4",
            "review_case_count": "2",
            "per_case_xz_grid_points_fine": "4826809",
            "stable_total_xz_grid_points_fine": "19307236",
            "per_case_xz_grid_points_coarse": "15625",
            "stable_total_xz_grid_points_coarse": "62500",
        },
    ]


def _prior_case_rows():
    rows = []
    for index in range(10):
        rows.append(
            {
                "case_label": f"stable-{index}",
                "truth_radius_pattern_key": "5,6,8",
                "controlled_synthetic_prior_contract_ready": "True",
                "review_assignment": "False",
            }
        )
    for index in range(2):
        rows.append(
            {
                "case_label": f"review-{index}",
                "truth_radius_pattern_key": "5,6,8",
                "controlled_synthetic_prior_contract_ready": "False",
                "review_assignment": "True",
            }
        )
    return rows


def test_radius_scope_rows_distinguish_fixed_permutation_and_independent_choices():
    rows = {row["radius_scope_key"]: row for row in radius_scope_rows([5.0, 6.0, 8.0], 3)}

    assert rows["fixed_slot_radii"]["radius_combination_count"] == 1
    assert rows["fixed_slot_radii"]["uses_truth_slot_assignment"] is True
    assert rows["known_radius_permutations"]["radius_combination_count"] == 6
    assert rows["known_radius_permutations"]["uses_truth_slot_assignment"] is False
    assert rows["independent_known_radius_choices"]["radius_combination_count"] == 27
    assert rows["independent_known_radius_choices"]["ready_for_launch"] is False


def test_budget_rows_multiply_xz_grid_by_radius_scope_without_launch_permission():
    radius_rows = radius_scope_rows([5.0, 6.0, 8.0], 3)
    rows = build_budget_rows(_branch_rows(), radius_rows)
    by_scope_branch = {(row["radius_scope_key"], row["branch_key"]): row for row in rows}

    close14_fixed = by_scope_branch[("fixed_slot_radii", "target2_close14")]
    assert close14_fixed["stable_total_coordinate_radius_points_fine"] == 10_629_366
    assert close14_fixed["uses_truth_slot_assignment"] is True
    assert close14_fixed["ready_for_launch"] is False

    close50_permuted = by_scope_branch[
        ("known_radius_permutations", "target2_close50_linear29p5")
    ]
    assert close50_permuted["stable_total_coordinate_radius_points_fine"] == 19_307_236 * 6
    assert close50_permuted["ready_for_detector_seeded_fwi"] is False


def test_summary_scopes_fixed_radius_budget_but_blocks_search_fwi_and_gpu():
    radius_rows = radius_scope_rows([5.0, 6.0, 8.0], 3)
    budget_rows = build_budget_rows(_branch_rows(), radius_rows)
    summary = summarize_budget(
        _branch_rows(),
        _prior_case_rows(),
        radius_rows,
        budget_rows,
        {
            "policy_label": "xz",
            "ready_for_branch_specific_xz_seed_neighborhood_contract": True,
        },
        {
            "policy_label": "prior",
            "ready_for_controlled_synthetic_prior_contract": True,
        },
        [5.0, 6.0, 8.0],
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["stable_controlled_prior_case_count"] == 10
    assert summary["review_case_excluded_count"] == 2
    assert summary["radius_pattern_mm"] == "5,6,8"
    assert summary["fixed_slot_radii_stable_total_points_fine"] == 29_936_602
    assert summary["known_radius_permutations_stable_total_points_fine"] == 29_936_602 * 6
    assert summary["independent_known_radius_choices_stable_total_points_fine"] == 29_936_602 * 27
    assert summary["ready_for_controlled_fixed_radius_budget"] is True
    assert summary["ready_for_independent_radius_search"] is False
    assert summary["ready_for_refinement_launch"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["ready_for_gpu_work"] is False
    assert gates["controlled_fixed_radius_budget"]["ready"] is True
    assert gates["detector_seeded_fwi"]["ready"] is False
