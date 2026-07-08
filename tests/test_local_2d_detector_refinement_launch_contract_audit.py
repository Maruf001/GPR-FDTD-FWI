from run_local_2d_detector_refinement_launch_contract_audit import (
    build_blocker_rows,
    build_branch_rows,
    build_contract_rows,
    summarize_contract,
)


def _selected(case, stable=True, max_error=5.0):
    return {
        "case_label": case,
        "branch_key": case.split("|")[0],
        "seed": "13",
        "case_variant": case.split("|")[-1],
        "selection_mode": "regular",
        "selected_x_values_mm": "185,250,295",
        "selected_z_values_mm": "90,90,90",
        "selected_component_count": "3",
        "component_candidate_count": "20",
        "all_target_slots_hit": "True",
        "max_target_slot_abs_error_mm": str(max_error),
    }


def _reliability(case, stable=True):
    return {
        "case_label": case,
        "truth_free_stable_assignment": str(stable),
        "truth_free_reliability_label": "stable_truth_free_assignment" if stable else "review",
        "success_fraction_truth_eval": "1.0" if stable else "0.875",
    }


def test_contract_rows_export_stable_component_seed_table_but_not_gpu_launch():
    selected = [
        _selected("target2_close14|seed13|nominal", stable=True, max_error=5.0),
        _selected("target2_close50_linear29p5|seed13|nominal", stable=False, max_error=3.0),
    ]
    reliability = [
        _reliability("target2_close14|seed13|nominal", stable=True),
        _reliability("target2_close50_linear29p5|seed13|nominal", stable=False),
    ]

    rows = build_contract_rows(selected, reliability, coarse_error_gate_mm=10.0)

    assert rows[0]["candidate_component_seed_ready"] is True
    assert rows[0]["radius_seed_available"] is False
    assert rows[0]["gpu_refinement_launch_ready"] is False
    assert rows[1]["candidate_component_seed_ready"] is False
    assert rows[1]["launch_blocker"] == "review_assignment"


def test_summary_keeps_detector_seeded_fwi_blocked_with_active_blockers():
    selected = [_selected("target2_close14|seed13|nominal", stable=True, max_error=5.0)]
    reliability = [_reliability("target2_close14|seed13|nominal", stable=True)]
    contract_rows = build_contract_rows(selected, reliability, coarse_error_gate_mm=10.0)
    branch_rows = build_branch_rows(contract_rows)
    blocker_rows = build_blocker_rows(
        {"uses_truth_for_grid_scoring": True},
        {
            "heldout_branch_robust": False,
            "leave_one_branch_all_target_slot_case_count": 11,
            "leave_one_branch_case_count": 12,
        },
        {"review_assignment_case_count": 0},
        {
            "ready_for_per_seed_physics_equivalence_claim": False,
            "review_cases_with_synthetic_x_ambiguity_count": 1,
            "detector_review_case_count": 2,
        },
        {
            "best_deployable_selector_all_truth_case_count": 0,
            "case_count": 12,
            "best_rank_gated_upper_bound_all_truth_case_count": 12,
        },
    )
    summary = summarize_contract(
        contract_rows,
        branch_rows,
        blocker_rows,
        {"policy_label": "blind", "best_variant_label": "best"},
        {"policy_label": "reliability"},
        {"policy_label": "upper", "best_deployable_selector_all_truth_case_count": 0},
    )

    assert summary["candidate_component_seed_ready_count"] == 1
    assert summary["ready_for_component_seed_table"] is True
    assert summary["active_blocker_count"] > 0
    assert summary["radius_seed_available"] is False
    assert summary["ready_for_narrow_refinement_contract"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
