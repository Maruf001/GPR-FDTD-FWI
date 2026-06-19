from run_local_2d_detector_upper_bound_policy import (
    best_budget_row,
    build_policy_rows,
    minimal_all_case_budget,
    summarize_policy,
)


def _budget(objective: str, budget: int, count: int, case_count: int = 2) -> dict:
    return {
        "objective": objective,
        "candidate_triple_budget": budget,
        "first_all_truth_case_count": count,
        "case_count": case_count,
        "case_fraction": count / case_count,
    }


def test_best_budget_row_and_minimal_all_case_budget():
    rows = [
        _budget("a", 50, 1),
        _budget("b", 50, 2),
        _budget("b", 100, 2),
    ]

    assert best_budget_row(rows, 50)["objective"] == "b"
    assert minimal_all_case_budget(rows) == (50, "b")


def test_policy_rows_separate_selector_failure_from_upper_bound():
    handoff = {
        "case_count": 2,
        "cheapest_full_candidate_triples_per_case": 1140,
        "cheapest_full_candidate_strategy": "branch_top20_candidate_list",
    }
    simple_rows = [_budget("span_bonus", 50, 1), _budget("span_bonus", 200, 2)]
    component_rows = [
        _budget("component_balanced", 50, 1),
        _budget("component_balanced", 100, 1),
        _budget("component_balanced", 200, 2),
    ]
    selector = {
        "leave_one_case_all_truth_case_count": 0,
        "best_in_sample_selector_label": "selector",
    }

    rows = build_policy_rows(
        handoff_summary=handoff,
        rank_budget_rows=simple_rows,
        component_budget_rows=component_rows,
        selector_summary=selector,
    )

    by_strategy = {row["strategy"]: row for row in rows}
    assert by_strategy["component_selector_validated_top1"]["deployable_top1_selector"] is True
    assert by_strategy["component_selector_validated_top1"]["all_truth_case_count"] == 0
    assert by_strategy["component_gate_minimal_all_case_upper_bound"]["rank_gated_upper_bound_ready"] is True
    assert by_strategy["component_gate_minimal_all_case_upper_bound"]["candidate_triples_per_case"] == 200
    assert all(row["ready_for_detector_seeded_fwi"] is False for row in rows)


def test_summary_marks_upper_bound_ready_but_fwi_blocked():
    rows = [
        {
            "strategy": "component_selector_validated_top1",
            "case_count": 2,
            "all_truth_case_count": 0,
            "candidate_triples_per_case": 1,
            "objective": "selector",
            "deployable_top1_selector": True,
            "rank_gated_upper_bound_ready": False,
        },
        {
            "strategy": "component_gate_minimal_all_case_upper_bound",
            "case_count": 2,
            "all_truth_case_count": 2,
            "candidate_triples_per_case": 200,
            "objective": "component_balanced",
            "deployable_top1_selector": False,
            "rank_gated_upper_bound_ready": True,
        },
    ]
    summary = summarize_policy(
        rows,
        {"leave_one_case_all_truth_case_count": 0, "selector_candidate_count": 975},
        {"best_top50_case_count": 10, "top50_improvement_over_source": 2},
    )

    assert summary["best_rank_gated_upper_bound_strategy"] == "component_gate_minimal_all_case_upper_bound"
    assert summary["minimal_all_case_rank_gated_triples_per_case"] == 200
    assert summary["best_deployable_selector_all_truth_case_count"] == 0
    assert summary["ready_for_rank_gated_upper_bound_claim"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
