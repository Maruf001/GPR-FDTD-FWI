from run_local_2d_detector_separability_blocker_triage import (
    blocker_label,
    budget_label,
    build_branch_rows,
    build_case_triage_rows,
    summarize_triage,
)


def test_budget_and_blocker_labels_separate_rank_gate_from_feature_failure():
    assert budget_label(1) == "top1"
    assert budget_label(10) == "top10"
    assert budget_label(50) == "top50"
    assert budget_label(200) == "top200"
    assert budget_label(201) == "deeper_than_top200"

    assert blocker_label(5, 30) == "top1_selector_gap_rank_gate_ok"
    assert blocker_label(5, 120) == "cv_rank_gate_deep_but_bounded"
    assert blocker_label(5, 400) == "feature_generalization_failure"
    assert blocker_label(250, 400) == "candidate_space_gap"


def test_case_triage_uses_leave_one_case_rows():
    case_rows = [
        {
            "case_label": "branch|seed13|nominal",
            "branch_key": "branch",
            "seed": "13",
            "case_variant": "nominal",
            "all_truth_triple_count": "2",
            "best_feature": "span",
            "best_first_all_truth_rank": "4",
            "best_false_minus_truth_score_gap": "0.1",
            "positive_gap_feature_count": "3",
        },
    ]
    cv_rows = [
        {
            "case_label": "branch|seed13|nominal",
            "cv_strategy": "leave_one_case",
            "trained_feature": "component",
            "first_all_truth_rank": "300",
            "top_unique_truth_hit_count": "1",
            "top_candidate_x_values_mm": "1,2,3",
        },
    ]

    rows = build_case_triage_rows(case_rows, cv_rows)

    assert rows[0]["blocker_label"] == "feature_generalization_failure"
    assert rows[0]["leave_one_feature"] == "component"
    assert rows[0]["recommended_next"] == "branch_conditioned_cpu_selector_or_holdout_robustness_audit"


def test_summary_keeps_detector_fwi_blocked_and_counts_branch_failures():
    rows = [
        {
            "case_label": "branch|seed13|nominal",
            "branch_key": "branch",
            "seed": 13,
            "case_variant": "nominal",
            "all_truth_triple_count": 2,
            "best_feature": "span",
            "best_first_all_truth_rank": 4,
            "best_budget_label": "top10",
            "leave_one_feature": "component",
            "leave_one_first_all_truth_rank": 300,
            "leave_one_budget_label": "deeper_than_top200",
            "leave_one_top_truth_hit_count": 1,
            "leave_one_top_candidate_x_values_mm": "1,2,3",
            "best_false_minus_truth_score_gap": 0.1,
            "positive_gap_feature_count": 3,
            "blocker_label": "feature_generalization_failure",
            "recommended_next": "branch_conditioned_cpu_selector_or_holdout_robustness_audit",
        },
        {
            "case_label": "branch|seed21|nominal",
            "branch_key": "branch",
            "seed": 21,
            "case_variant": "nominal",
            "all_truth_triple_count": 2,
            "best_feature": "component",
            "best_first_all_truth_rank": 20,
            "best_budget_label": "top50",
            "leave_one_feature": "component",
            "leave_one_first_all_truth_rank": 40,
            "leave_one_budget_label": "top50",
            "leave_one_top_truth_hit_count": 1,
            "leave_one_top_candidate_x_values_mm": "1,2,3",
            "best_false_minus_truth_score_gap": 0.1,
            "positive_gap_feature_count": 3,
            "blocker_label": "top1_selector_gap_rank_gate_ok",
            "recommended_next": "report_detector_as_candidate_list_baseline",
        },
    ]
    branch_rows = build_branch_rows(rows)
    summary = summarize_triage(rows, branch_rows, {"all_truth_triple_count": 4, "ready_for_rank_gated_upper_bound_claim": True})

    assert branch_rows[0]["feature_generalization_failure_count"] == 1
    assert summary["best_top50_case_count"] == 2
    assert summary["leave_one_top50_case_count"] == 1
    assert summary["feature_generalization_failure_count"] == 1
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
