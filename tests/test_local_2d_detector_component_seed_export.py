from run_local_2d_detector_component_seed_export import (
    build_branch_rows,
    build_component_seed_rows,
    build_excluded_case_rows,
    build_gate_rows,
    summarize_seed_export,
)


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
            "detector_reliability_label": "stable_truth_free_assignment",
            "truth_free_stable_assignment": "True",
            "review_assignment": "False",
            "best_variant_all_slots_hit": "True",
            "success_fraction_truth_eval": "1.0",
            "max_target_slot_abs_error_mm": "5",
            "coarse_error_gate_mm": "10",
            "coarse_error_gate_pass": "True",
            "candidate_component_seed_ready": "True",
            "launch_blocker": "missing_radius_material_and_independent_validation",
        },
        {
            "case_label": "target2_close50_linear29p5|seed13|nominal",
            "branch_key": "target2_close50_linear29p5",
            "seed": "13",
            "case_variant": "nominal",
            "selected_x_values_mm": "187,250,299",
            "selected_z_values_mm": "85,84,79",
            "selected_component_count": "3",
            "component_candidate_count": "17",
            "detector_reliability_label": "review_policy_grid_position_drift",
            "truth_free_stable_assignment": "False",
            "review_assignment": "True",
            "best_variant_all_slots_hit": "True",
            "success_fraction_truth_eval": "0.875",
            "max_target_slot_abs_error_mm": "3",
            "coarse_error_gate_mm": "10",
            "coarse_error_gate_pass": "True",
            "candidate_component_seed_ready": "False",
            "launch_blocker": "review_assignment",
        },
    ]


def test_component_seed_rows_split_stable_cases_into_coordinate_components():
    rows = build_component_seed_rows(_contract_rows())

    assert len(rows) == 3
    assert [row["component_role"] for row in rows] == ["left", "middle", "right"]
    assert [row["x_seed_mm"] for row in rows] == [185.0, 250.0, 265.0]
    assert all(row["coordinate_seed_ready"] for row in rows)
    assert not any(row["radius_seed_available"] for row in rows)
    assert not any(row["detector_seeded_fwi_ready"] for row in rows)


def test_excluded_rows_keep_review_cases_out_of_seed_export():
    excluded = build_excluded_case_rows(_contract_rows())

    assert len(excluded) == 1
    assert excluded[0]["case_label"] == "target2_close50_linear29p5|seed13|nominal"
    assert excluded[0]["review_assignment"] is True
    assert excluded[0]["exclusion_reason"] == "review_assignment"


def test_summary_exports_coordinate_table_but_blocks_refinement_and_fwi():
    seed_rows = build_component_seed_rows(_contract_rows())
    excluded_rows = build_excluded_case_rows(_contract_rows())
    branch_rows = build_branch_rows(seed_rows, excluded_rows, _contract_rows())
    summary = summarize_seed_export(
        seed_rows,
        excluded_rows,
        branch_rows,
        {
            "policy_label": "contract",
            "case_count": 2,
            "active_blocker_count": 6,
            "active_blocker_keys": "radius_material_contract_missing;review_cases_present",
        },
    )
    gates = {row["gate_key"]: row for row in build_gate_rows(summary)}

    assert summary["policy_label"] == "local_2d_detector_component_seed_export_coordinate_only_no_fwi"
    assert summary["exported_seed_case_count"] == 1
    assert summary["exported_component_row_count"] == 3
    assert summary["excluded_review_case_count"] == 1
    assert summary["ready_for_coordinate_seed_table"] is True
    assert summary["ready_for_radius_material_contract"] is False
    assert summary["ready_for_narrow_refinement_contract"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
    assert gates["coordinate_seed_table"]["ready"] is True
    assert gates["detector_seeded_fwi"]["ready"] is False
