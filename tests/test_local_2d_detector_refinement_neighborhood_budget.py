import pytest

from run_local_2d_detector_refinement_neighborhood_budget import (
    build_gate_rows,
    build_grid_budget_rows,
    build_half_width_rows,
    coordinate_grid_points,
    hypothetical_xz_tensor_grid_points,
    parse_positive_numbers,
    summarize_budget,
)


def _contract_rows():
    rows = []
    for label, branch, error, ready, review in [
        ("close14_s13_nominal", "target2_close14", 5.0, True, False),
        ("close14_s13_source", "target2_close14", 2.0, True, False),
        ("close14_s21_nominal", "target2_close14", 4.0, True, False),
        ("close14_s21_source", "target2_close14", 2.0, True, False),
        ("close14_s34_nominal", "target2_close14", 10.0, True, False),
        ("close14_s34_source", "target2_close14", 3.0, True, False),
        ("close50_s13_nominal", "target2_close50_linear29p5", 3.0, False, True),
        ("close50_s13_source", "target2_close50_linear29p5", 3.0, True, False),
        ("close50_s21_nominal", "target2_close50_linear29p5", 3.0, True, False),
        ("close50_s21_source", "target2_close50_linear29p5", 6.0, True, False),
        ("close50_s34_nominal", "target2_close50_linear29p5", 7.0, False, True),
        ("close50_s34_source", "target2_close50_linear29p5", 8.0, True, False),
    ]:
        rows.append(
            {
                "case_label": label,
                "branch_key": branch,
                "max_target_slot_abs_error_mm": str(error),
                "candidate_component_seed_ready": str(ready),
                "review_assignment": str(review),
            }
        )
    return rows


def test_parse_positive_numbers_sorts_deduplicates_and_rejects_invalid():
    assert parse_positive_numbers("10,2,10,5") == [2.0, 5.0, 10.0]
    with pytest.raises(ValueError):
        parse_positive_numbers("1,0")
    with pytest.raises(ValueError):
        parse_positive_numbers("")


def test_half_width_rows_capture_stable_and_review_coverage():
    rows = build_half_width_rows(_contract_rows(), [5.0, 8.0, 10.0])
    by_width = {row["half_width_mm"]: row for row in rows}

    assert by_width[5.0]["stable_seed_covered_count"] == 7
    assert by_width[8.0]["stable_seed_covered_count"] == 9
    assert by_width[10.0]["stable_seed_covered_count"] == 10
    assert by_width[10.0]["review_case_covered_count"] == 2
    assert by_width[10.0]["coverage_dimension"] == "lateral_x_slot_only"
    assert by_width[10.0]["ready_for_lateral_x_slot_neighborhood_design"]
    assert not by_width[10.0]["ready_for_xz_neighborhood_design"]
    assert not by_width[10.0]["ready_for_refinement_launch"]


def test_summary_sizes_lateral_x_neighborhood_but_keeps_xz_refinement_and_fwi_blocked():
    half_width_rows = build_half_width_rows(_contract_rows(), [5.0, 8.0, 10.0])
    grid_rows = build_grid_budget_rows(half_width_rows, [1.0, 2.0, 5.0])
    summary = summarize_budget(
        _contract_rows(),
        half_width_rows,
        [],
        grid_rows,
        {
            "policy_label": "contract",
            "active_blocker_count": 6,
            "active_blocker_keys": "radius_material_contract_missing;review_cases_present",
        },
        {"policy_label": "seed_export"},
    )
    gates = {row["gate_key"]: row for row in build_gate_rows(summary)}

    assert coordinate_grid_points(10.0, 2.0) == 1331
    assert hypothetical_xz_tensor_grid_points(10.0, 2.0) == 1771561
    assert summary["policy_label"] == "local_2d_detector_lateral_slot_neighborhood_budget_cpu_no_fwi"
    assert summary["coverage_dimension"] == "lateral_x_slot_only"
    assert summary["stable_seed_case_count"] == 10
    assert summary["review_case_count"] == 2
    assert summary["min_lateral_x_half_width_all_stable_seed_cases_mm"] == 10.0
    assert summary["stable_lateral_x_coverage_at_5mm"] == 7.0
    assert summary["stable_lateral_x_coverage_at_8mm"] == 9.0
    assert summary["stable_lateral_x_coverage_at_10mm"] == 10.0
    assert summary["per_case_lateral_x_grid_points_h10_step2"] == 1331.0
    assert summary["stable_total_lateral_x_grid_points_h10_step2"] == 13310.0
    assert summary["hypothetical_per_case_xz_tensor_points_h10_step2"] == 1771561.0
    assert summary["ready_for_lateral_x_slot_neighborhood_design"]
    assert not summary["z_coverage_validated"]
    assert not summary["ready_for_xz_neighborhood_design"]
    assert not summary["ready_for_narrow_refinement_contract"]
    assert not summary["ready_for_naive_full_tensor_refinement"]
    assert not summary["ready_for_detector_seeded_fwi"]
    assert summary["gpu_priority"] == "none"
    assert gates["lateral_x_slot_neighborhood_design"]["ready"]
    assert not gates["xz_neighborhood_design"]["ready"]
    assert not gates["naive_full_tensor_refinement"]["ready"]
    assert not gates["detector_seeded_fwi"]["ready"]
