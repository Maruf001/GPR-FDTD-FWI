from run_local_2d_detector_blind_component_envelope_assembly import (
    leave_one_case_validation,
    select_components_for_variant,
    summarize_envelope_assembly,
    summarize_variant,
    target_slot_evaluation,
)


def _component(x_mm):
    return {"x_mm": float(x_mm), "z_mm": 90.0, "rank": 1.0, "component_score": 0.3}


def test_target_slot_evaluation_uses_unique_nearest_assignment():
    selected = [_component(264), _component(190), _component(250)]

    evaluation = target_slot_evaluation(selected, (190.0, 250.0, 264.0))

    assert evaluation["target_slot_hit_count"] == 3
    assert evaluation["all_target_slots_hit"] is True
    assert evaluation["target_slot_abs_errors_mm"] == [0.0, 0.0, 0.0]


def test_blind_selector_respects_edge_envelope_over_high_inner_score():
    case_feature = {
        "case_label": "case_a",
        "observed_support_span_mm": 110.0,
        "candidate_triples": [
            {
                "selected_components": [_component(188), _component(250), _component(300)],
                "selected_x": (188.0, 250.0, 300.0),
                "selected_z": (90.0, 90.0, 90.0),
                "selected_ranks": (1.0, 2.0, 3.0),
                "base_sum": 0.9,
                "edge_envelope_score": -0.1,
                "support_score": 5.0,
                "regular_structure_score": -0.2,
                "pair_structure_score": -1.1,
                "regular_center_score": -0.05,
                "x_span_mm": 112.0,
                "gap_left_mm": 62.0,
                "gap_right_mm": 50.0,
            },
            {
                "selected_components": [_component(250), _component(270), _component(300)],
                "selected_x": (250.0, 270.0, 300.0),
                "selected_z": (90.0, 90.0, 90.0),
                "selected_ranks": (1.0, 2.0, 3.0),
                "base_sum": 1.5,
                "edge_envelope_score": -2.1,
                "support_score": 6.0,
                "regular_structure_score": -0.16,
                "pair_structure_score": -0.8,
                "regular_center_score": -0.12,
                "x_span_mm": 50.0,
                "gap_left_mm": 20.0,
                "gap_right_mm": 30.0,
            },
        ],
    }
    variant = {
        "variant_label": "env6_struct0p6_support0p12_center0_span100",
        "envelope_weight": 6.0,
        "structural_weight": 0.6,
        "support_weight": 0.12,
        "center_weight": 0.0,
        "span_threshold_mm": 100.0,
    }

    selected = select_components_for_variant(case_feature, variant)

    assert selected["selection_mode"] == "regular"
    assert selected["selected_x"] == (188.0, 250.0, 300.0)


def test_summary_keeps_blind_envelope_probe_no_fwi_ready():
    variant = {
        "variant_label": "v1",
        "envelope_weight": 6.0,
        "structural_weight": 0.6,
        "support_weight": 0.12,
        "center_weight": 0.0,
        "span_threshold_mm": 100.0,
    }
    selected_rows = [
        {
            **variant,
            "case_label": "case_a",
            "all_target_slots_hit": True,
            "target_slot_hit_count": 3,
            "max_target_slot_abs_error_mm": 2.0,
            "component_candidate_count": 16,
            "selection_mode": "regular",
        },
        {
            **variant,
            "case_label": "case_b",
            "all_target_slots_hit": True,
            "target_slot_hit_count": 3,
            "max_target_slot_abs_error_mm": 3.0,
            "component_candidate_count": 18,
            "selection_mode": "close_pair",
        },
    ]
    variant_rows = [summarize_variant(selected_rows, variant)]

    leave_one_rows, leave_one_summary = leave_one_case_validation(selected_rows)
    summary = summarize_envelope_assembly(
        variant_rows,
        selected_rows,
        candidate_row_count=42,
        depth_slot_summary={"base_all_truth_case_count": 3, "best_all_truth_case_count": 5},
        slot_component_summary={"best_all_target_slot_case_count": 12},
    )

    assert len(leave_one_rows) == 2
    assert leave_one_summary["leave_one_case_all_target_slot_case_count"] == 2
    assert summary["policy_label"] == "local_2d_detector_blind_component_envelope_assembly_cpu_no_fwi"
    assert summary["best_all_target_slot_case_count"] == 2
    assert summary["known_slot_component_upper_bound_case_count"] == 12
    assert summary["truth_free_selection_at_inference"] is True
    assert summary["uses_branch_slots_for_selection"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
