import pytest

from run_local_2d_detector_seed_geometry_error_audit import (
    best_coordinate_assignment,
    build_branch_rows,
    build_gate_rows,
    build_geometry_error_rows,
    build_grid_budget_rows,
    build_half_width_rows,
    coordinate_grid_points,
    parse_positive_numbers,
    summarize_audit,
)


def _plan_rows():
    return [
        {
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "case_label": "noise_seed13",
            "truth_x_values_mm": "190,250,264",
            "truth_z_values_mm": "90,90,90",
        },
        {
            "branch_key": "target2_close14",
            "seed": "21",
            "case_variant": "nominal",
            "case_label": "noise_seed21",
            "truth_x_values_mm": "190,250,264",
            "truth_z_values_mm": "90,90,90",
        },
        {
            "branch_key": "target2_close50_linear29p5",
            "seed": "21",
            "case_variant": "source_mismatch",
            "case_label": "source_seed21",
            "truth_x_values_mm": "190,250,300",
            "truth_z_values_mm": "90,90,90",
        },
        {
            "branch_key": "target2_close50_linear29p5",
            "seed": "34",
            "case_variant": "nominal",
            "case_label": "noise_seed34",
            "truth_x_values_mm": "190,250,300",
            "truth_z_values_mm": "90,90,90",
        },
    ]


def _contract_rows():
    return [
        {
            "case_label": "target2_close14|seed13|nominal",
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "selected_x_values_mm": "185,250,265",
            "selected_z_values_mm": "97,81,85",
            "selected_component_count": "3",
            "component_candidate_count": "20",
            "max_target_slot_abs_error_mm": "5",
            "candidate_component_seed_ready": "True",
            "review_assignment": "False",
            "truth_free_stable_assignment": "True",
        },
        {
            "case_label": "target2_close14|seed21|nominal",
            "branch_key": "target2_close14",
            "seed": "21",
            "case_variant": "nominal",
            "selected_x_values_mm": "191,254,266",
            "selected_z_values_mm": "86,89,89",
            "selected_component_count": "3",
            "component_candidate_count": "20",
            "max_target_slot_abs_error_mm": "4",
            "candidate_component_seed_ready": "True",
            "review_assignment": "False",
            "truth_free_stable_assignment": "True",
        },
        {
            "case_label": "target2_close50_linear29p5|seed21|source_mismatch",
            "branch_key": "target2_close50_linear29p5",
            "seed": "21",
            "case_variant": "source_mismatch",
            "selected_x_values_mm": "193,247,303",
            "selected_z_values_mm": "78,80,79",
            "selected_component_count": "3",
            "component_candidate_count": "20",
            "max_target_slot_abs_error_mm": "3",
            "candidate_component_seed_ready": "True",
            "review_assignment": "False",
            "truth_free_stable_assignment": "True",
        },
        {
            "case_label": "target2_close50_linear29p5|seed34|nominal",
            "branch_key": "target2_close50_linear29p5",
            "seed": "34",
            "case_variant": "nominal",
            "selected_x_values_mm": "197,256,304",
            "selected_z_values_mm": "83,81,76",
            "selected_component_count": "3",
            "component_candidate_count": "20",
            "max_target_slot_abs_error_mm": "7",
            "candidate_component_seed_ready": "False",
            "review_assignment": "True",
            "truth_free_stable_assignment": "False",
        },
    ]


def test_parse_positive_numbers_sorts_and_rejects_invalid_values():
    assert parse_positive_numbers("12,5,12,8") == [5.0, 8.0, 12.0]
    with pytest.raises(ValueError):
        parse_positive_numbers("0,1")
    with pytest.raises(ValueError):
        parse_positive_numbers("")


def test_best_coordinate_assignment_reports_matched_xz_errors():
    assignment = best_coordinate_assignment(
        [(190.0, 90.0), (250.0, 90.0), (264.0, 90.0)],
        [(185.0, 97.0), (250.0, 81.0), (265.0, 85.0)],
    )

    assert assignment["max_x_error_mm"] == 5.0
    assert assignment["max_z_error_mm"] == 9.0
    assert assignment["max_linf_error_mm"] == 9.0
    assert assignment["component_rows"][1]["z_abs_error_mm"] == 9.0


def test_seed_geometry_summary_promotes_xz_sizing_but_blocks_refinement_and_fwi():
    case_rows, component_rows = build_geometry_error_rows(_plan_rows(), _contract_rows())
    half_width_rows = build_half_width_rows(case_rows, [5.0, 8.0, 10.0, 12.0, 15.0])
    branch_rows = build_branch_rows(case_rows, [5.0, 8.0, 10.0, 12.0, 15.0])
    grid_rows = build_grid_budget_rows(half_width_rows, [1.0, 2.0, 5.0])
    summary = summarize_audit(
        case_rows,
        half_width_rows,
        branch_rows,
        grid_rows,
        {"policy_label": "contract"},
        {
            "policy_label": "lateral",
            "min_lateral_x_half_width_all_stable_seed_cases_mm": 10.0,
        },
    )
    gates = {row["gate_key"]: row for row in build_gate_rows(summary)}

    assert len(component_rows) == 12
    assert coordinate_grid_points(12.0, 2.0, dimensions=6) == 4826809
    assert summary["policy_label"] == "local_2d_detector_seed_geometry_error_audit_cpu_no_fwi"
    assert summary["coverage_dimension"] == "matched_xz_linf"
    assert summary["stable_seed_case_count"] == 3
    assert summary["review_case_count"] == 1
    assert summary["max_stable_x_error_mm"] == 5.0
    assert summary["max_stable_z_error_mm"] == 12.0
    assert summary["max_stable_linf_error_mm"] == 12.0
    assert summary["min_xz_half_width_all_stable_seed_cases_mm"] == 12.0
    assert summary["source_lateral_min_half_width_all_stable_seed_cases_mm"] == 10.0
    assert summary["stable_xz_coverage_at_5mm"] == 1.0
    assert summary["stable_xz_coverage_at_10mm"] == 2.0
    assert summary["stable_xz_coverage_at_12mm"] == 3.0
    assert summary["per_case_xz_grid_points_h10_step2"] == 1771561.0
    assert summary["per_case_xz_grid_points_h12_step2"] == 4826809.0
    assert summary["ready_for_xz_seed_neighborhood_design"]
    assert not summary["ready_for_narrow_refinement_contract"]
    assert not summary["ready_for_detector_seeded_fwi"]
    assert gates["xz_seed_neighborhood_design"]["ready"]
    assert not gates["naive_full_tensor_refinement"]["ready"]
    assert not gates["detector_seeded_fwi"]["ready"]
