import math

from run_local_2d_detector_rank_budget_diagnostic import (
    build_budget_rows,
    build_case_rows,
    build_objective_rows,
    budget_label,
    summarize,
)


def _row(case: str, score_sum: float, score_span: float, all_truth: bool, targets: tuple[bool, bool, bool]) -> dict:
    return {
        "case_label": case,
        "branch_key": "branch",
        "seed": "13",
        "case_variant": "nominal",
        "score_sum": str(score_sum),
        "score_span_bonus": str(score_span),
        "unique_all_truths_within_tolerance": str(all_truth),
        "unique_target0_hit": str(targets[0]),
        "unique_target1_hit": str(targets[1]),
        "unique_target2_hit": str(targets[2]),
    }


def test_budget_label_buckets_candidate_ranks():
    assert budget_label(5) == "top10_candidate"
    assert budget_label(30) == "top50_candidate"
    assert budget_label(80) == "top100_candidate"
    assert budget_label(150) == "top200_candidate"
    assert budget_label(300) == "deep_candidate_space"
    assert budget_label(math.inf) == "not_in_candidate_space"


def test_case_and_objective_rows_track_first_truth_rank_and_target_hits():
    rows = [
        _row("case_a", 3.0, 1.0, False, (False, True, True)),
        _row("case_a", 2.0, 3.0, True, (True, True, True)),
        _row("case_b", 4.0, 1.0, False, (False, True, False)),
        _row("case_b", 3.0, 2.0, False, (False, True, True)),
        _row("case_b", 2.0, 3.0, True, (True, True, True)),
    ]

    case_rows = build_case_rows(rows, objectives=("sum", "span_bonus"))
    objective_rows = build_objective_rows(rows, objectives=("sum", "span_bonus"))

    by_case = {row["case_label"]: row for row in case_rows}
    assert by_case["case_a"]["sum_first_all_truth_rank"] == 2
    assert by_case["case_b"]["sum_first_all_truth_rank"] == 3
    assert by_case["case_a"]["span_bonus_first_all_truth_rank"] == 1
    assert by_case["case_b"]["span_bonus_first_all_truth_rank"] == 1
    assert by_case["case_b"]["all_truth_manifold_label"] == "sparse_all_truth_manifold"

    by_objective = {row["objective"]: row for row in objective_rows}
    assert by_objective["sum"]["top1_all_truth_case_count"] == 0
    assert by_objective["sum"]["top1_target0_hit_count"] == 0
    assert by_objective["sum"]["top1_target1_hit_count"] == 2
    assert by_objective["span_bonus"]["top1_all_truth_case_count"] == 2
    assert by_objective["span_bonus"]["top1_target0_hit_count"] == 2


def test_summary_identifies_minimal_all_case_budget_without_fwi_readiness():
    rows = [
        _row("case_a", 3.0, 1.0, False, (False, True, True)),
        _row("case_a", 2.0, 3.0, True, (True, True, True)),
        _row("case_b", 4.0, 1.0, False, (False, True, False)),
        _row("case_b", 3.0, 2.0, False, (False, True, True)),
        _row("case_b", 2.0, 3.0, True, (True, True, True)),
    ]
    case_rows = build_case_rows(rows, objectives=("sum", "span_bonus"))
    objective_rows = build_objective_rows(rows, objectives=("sum", "span_bonus"))
    budget_rows = build_budget_rows(objective_rows)

    summary = summarize(rows, case_rows, objective_rows, budget_rows, {"policy_label": "source"})

    assert summary["source_policy_label"] == "source"
    assert summary["all_truth_combo_available_case_count"] == 2
    assert summary["best_top20_case_count"] == 2
    assert summary["minimal_all_case_candidate_triple_budget"] == 1
    assert summary["minimal_all_case_objectives"] == ["span_bonus"]
    assert summary["ready_for_rank_gated_upper_bound_study"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
