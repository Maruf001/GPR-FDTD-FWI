from run_local_2d_detector_blind_envelope_robustness_audit import (
    heldout_split_rows,
    ranked_triples_for_case,
    summarize_audit,
)


def _selected_row(variant, case, seed, branch, hit=True, hit_count=3):
    return {
        "variant_label": variant,
        "envelope_weight": 2.0 if variant == "v_good" else 1.0,
        "structural_weight": 0.4,
        "support_weight": 0.12,
        "center_weight": 0.1,
        "span_threshold_mm": 90.0,
        "case_label": case,
        "seed": str(seed),
        "branch_key": branch,
        "case_variant": "nominal",
        "target_slot_hit_count": hit_count,
        "all_target_slots_hit": str(hit),
        "max_target_slot_abs_error_mm": 2.0,
        "component_candidate_count": 16,
        "selection_mode": "regular",
    }


def _component(x_mm):
    return {"x_mm": float(x_mm), "z_mm": 90.0, "rank": 1.0, "component_score": 0.3}


def test_heldout_split_rows_selects_training_best_variant():
    selected_rows = [
        _selected_row("v_good", "case_a", 13, "target2_close14", True),
        _selected_row("v_good", "case_b", 21, "target2_close14", True),
        _selected_row("v_bad", "case_a", 13, "target2_close14", False, 2),
        _selected_row("v_bad", "case_b", 21, "target2_close14", True),
    ]

    rows = heldout_split_rows(selected_rows, "seed")

    assert len(rows) == 2
    assert {row["selected_variant_label"] for row in rows} == {"v_good"}
    assert sum(row["heldout_all_target_slot_case_count"] for row in rows) == 2
    assert sum(row["heldout_failed_case_count"] for row in rows) == 0


def test_ranked_triples_for_case_scores_truth_and_wrong_candidates():
    case_feature = {
        "branch_key": "target2_close50_linear29p5",
        "observed_support_span_mm": 110.0,
        "candidate_triples": [
            {
                "selected_components": [_component(190), _component(250), _component(300)],
                "selected_x": (190.0, 250.0, 300.0),
                "selected_z": (90.0, 90.0, 90.0),
                "selected_ranks": (1.0, 2.0, 3.0),
                "base_sum": 1.0,
                "edge_envelope_score": -0.05,
                "regular_structure_score": -0.1,
                "pair_structure_score": -1.0,
                "support_score": 5.0,
                "regular_center_score": -0.1,
            },
            {
                "selected_components": [_component(190), _component(270), _component(300)],
                "selected_x": (190.0, 270.0, 300.0),
                "selected_z": (90.0, 90.0, 90.0),
                "selected_ranks": (1.0, 2.0, 3.0),
                "base_sum": 0.9,
                "edge_envelope_score": -0.2,
                "regular_structure_score": -0.2,
                "pair_structure_score": -0.9,
                "support_score": 4.0,
                "regular_center_score": -0.2,
            },
        ],
    }
    variant = {
        "variant_label": "v",
        "envelope_weight": 2.0,
        "structural_weight": 0.4,
        "support_weight": 0.12,
        "center_weight": 0.1,
        "span_threshold_mm": 90.0,
    }

    ranked = ranked_triples_for_case(case_feature, variant)

    assert ranked[0]["all_target_slots_hit"] is True
    assert ranked[0]["target_slot_hit_count"] == 3
    assert ranked[1]["all_target_slots_hit"] is False
    assert ranked[1]["target_slot_hit_count"] == 2


def test_summarize_audit_marks_branch_boundary_and_no_fwi():
    variant_rows = [
        {"variant_label": "v1", "all_target_slot_case_count": 2},
        {"variant_label": "v2", "all_target_slot_case_count": 1},
    ]
    split_rows = [
        {
            "split_field": "seed",
            "heldout_case_count": 2,
            "heldout_all_target_slot_case_count": 2,
            "heldout_mean_target_slot_hit_count": 3.0,
        },
        {
            "split_field": "branch_key",
            "heldout_case_count": 2,
            "heldout_all_target_slot_case_count": 1,
            "heldout_mean_target_slot_hit_count": 2.5,
        },
        {
            "split_field": "case_variant",
            "heldout_case_count": 2,
            "heldout_all_target_slot_case_count": 2,
            "heldout_mean_target_slot_hit_count": 3.0,
        },
    ]
    margins = [
        {"truth_vs_wrong_score_margin": 0.05, "margin_below_review_threshold": True, "first_all_target_slot_rank": 1},
        {"truth_vs_wrong_score_margin": 0.30, "margin_below_review_threshold": False, "first_all_target_slot_rank": 1},
    ]

    summary = summarize_audit(
        variant_rows,
        split_rows,
        margins,
        {
            "policy_label": "source",
            "case_count": 2,
            "best_all_target_slot_case_count": 2,
            "leave_one_case_all_target_slot_case_count": 2,
        },
    )

    assert summary["full_success_variant_count"] == 1
    assert summary["leave_one_seed_all_target_slot_case_count"] == 2
    assert summary["leave_one_branch_all_target_slot_case_count"] == 1
    assert summary["robustness_boundary"] == "seed_and_condition_robust_but_not_branch_independent"
    assert summary["best_variant_low_margin_case_count"] == 1
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
