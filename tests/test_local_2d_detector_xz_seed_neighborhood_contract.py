from run_local_2d_detector_xz_seed_neighborhood_contract import (
    branch_contract_rows,
    contract_case_rows,
    coordinate_grid_points,
    gate_rows,
    summarize_contract,
)


def _branch_rows():
    return [
        {
            "branch_key": "target2_close14",
            "half_width_mm": "8",
            "stable_seed_case_count": "6",
            "stable_seed_xz_coverage_fraction": "0.3333333333",
            "review_case_count": "0",
            "review_case_xz_covered_count": "0",
        },
        {
            "branch_key": "target2_close14",
            "half_width_mm": "10",
            "stable_seed_case_count": "6",
            "stable_seed_xz_coverage_fraction": "1.0",
            "review_case_count": "0",
            "review_case_xz_covered_count": "0",
        },
        {
            "branch_key": "target2_close50_linear29p5",
            "half_width_mm": "10",
            "stable_seed_case_count": "4",
            "stable_seed_xz_coverage_fraction": "0.5",
            "review_case_count": "2",
            "review_case_xz_covered_count": "0",
        },
        {
            "branch_key": "target2_close50_linear29p5",
            "half_width_mm": "12",
            "stable_seed_case_count": "4",
            "stable_seed_xz_coverage_fraction": "1.0",
            "review_case_count": "2",
            "review_case_xz_covered_count": "1",
        },
    ]


def _case_rows():
    return [
        {
            "case_label": "close14-a",
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "candidate_component_seed_ready": "True",
            "review_assignment": "False",
            "matched_max_x_error_mm": "10",
            "matched_max_z_error_mm": "5",
            "matched_max_linf_error_mm": "10",
        },
        {
            "case_label": "close50-a",
            "branch_key": "target2_close50_linear29p5",
            "seed": "21",
            "case_variant": "nominal",
            "candidate_component_seed_ready": "True",
            "review_assignment": "False",
            "matched_max_x_error_mm": "3",
            "matched_max_z_error_mm": "11",
            "matched_max_linf_error_mm": "11",
        },
        {
            "case_label": "close50-review",
            "branch_key": "target2_close50_linear29p5",
            "seed": "34",
            "case_variant": "nominal",
            "candidate_component_seed_ready": "False",
            "review_assignment": "True",
            "matched_max_x_error_mm": "7",
            "matched_max_z_error_mm": "14",
            "matched_max_linf_error_mm": "14",
        },
    ]


def test_coordinate_grid_points_matches_xz_six_dimensional_budget():
    assert coordinate_grid_points(10, 2, 3) == 1_771_561
    assert coordinate_grid_points(12, 2, 3) == 4_826_809
    assert coordinate_grid_points(12, 5, 3) == 15_625


def test_branch_contract_selects_minimum_covering_half_widths():
    rows = branch_contract_rows(_branch_rows())
    by_branch = {row["branch_key"]: row for row in rows}

    assert by_branch["target2_close14"]["recommended_half_width_mm"] == 10
    assert by_branch["target2_close50_linear29p5"]["recommended_half_width_mm"] == 12
    assert by_branch["target2_close14"]["stable_total_xz_grid_points_fine"] == 6 * 1_771_561
    assert by_branch["target2_close50_linear29p5"]["stable_total_xz_grid_points_fine"] == 4 * 4_826_809
    assert by_branch["target2_close50_linear29p5"]["ready_for_detector_seeded_fwi"] is False


def test_contract_summary_reduces_global_h12_but_keeps_launch_blocked():
    branches = branch_contract_rows(_branch_rows())
    cases = contract_case_rows(_case_rows(), branches)
    summary = summarize_contract(
        branches,
        cases,
        {"policy_label": "seed_geometry"},
        {
            "policy_label": "seed_export",
            "active_blocker_keys": "radius_material_contract_missing;review_cases_present",
        },
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["stable_contract_case_count"] == 2
    assert summary["review_case_excluded_count"] == 1
    assert summary["branch_half_widths_mm"] == "target2_close14:10;target2_close50_linear29p5:12"
    assert summary["global_stable_total_xz_grid_points_fine"] == 2 * 4_826_809
    assert summary["branch_specific_stable_total_xz_grid_points_fine"] == 1_771_561 + 4_826_809
    assert summary["branch_specific_grid_reduction_fraction_fine"] > 0
    assert summary["all_stable_cases_covered_by_branch_contract"] is True
    assert summary["ready_for_branch_specific_xz_seed_neighborhood_contract"] is True
    assert summary["ready_for_narrow_refinement_launch"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert gates["branch_specific_xz_seed_neighborhood_contract"]["ready"] is True
    assert gates["detector_seeded_fwi"]["ready"] is False
