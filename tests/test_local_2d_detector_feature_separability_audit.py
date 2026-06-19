import math

from run_local_2d_detector_feature_separability_audit import (
    build_case_summary_rows,
    build_objective_case_rows,
    cross_validate_objectives,
    enriched_row,
    minimal_all_case_budget,
    score_value,
    summarize_audit,
    summarize_objectives,
)


def _row(case, xs, ranks, hits, score_sum):
    return enriched_row(
        {
            "branch_key": case[0],
            "seed": str(case[1]),
            "case_variant": case[2],
            "run_name": f"{case[0]}_{case[1]}_{case[2]}",
            "candidate_x_values_mm": ",".join(str(x) for x in xs),
            "candidate_z_values_mm": "90,90,90",
            "candidate_ranks": ",".join(str(rank) for rank in ranks),
            "x_span_mm": str(max(xs) - min(xs)),
            "gap_balance_mm": "0",
            "score_sum": str(score_sum),
            "score_span_bonus": str(score_sum),
            "score_min": str(score_sum),
            "score_min_span": str(score_sum),
            "score_balanced": str(score_sum),
            "score_mask": str(score_sum),
            "score_component_sum": str(score_sum),
            "score_component_min": str(score_sum),
            "score_component_mean_min": str(score_sum),
            "score_component_floor_span": str(score_sum),
            "score_component_balanced": str(score_sum),
            "score_component_left_floor": str(score_sum),
            "score_hybrid_span_component": str(score_sum),
            "unique_truth_hit_count": str(sum(hits)),
            "unique_all_truths_within_tolerance": str(all(hits)),
            "unique_target0_hit": str(hits[0]),
            "unique_target1_hit": str(hits[1]),
            "unique_target2_hit": str(hits[2]),
        }
    )


def test_score_value_handles_derived_rank_and_span_features():
    row = _row(("target2_close50", 13, "nominal"), [195, 250, 305], [5, 10, 40], (True, True, True), 1.0)

    assert score_value(row, "rank_sum_inverse") == -55.0
    assert score_value(row, "max_rank_inverse") == -40.0
    assert score_value(row, "x_span_width") == 110.0
    assert score_value(row, "x_span_target110_inverse") == 0.0
    assert score_value(row, "center250_inverse") == 0.0


def test_objective_summary_finds_rank_gated_truth_not_top1():
    rows = [
        _row(("branch", 13, "nominal"), [240, 250, 260], [1, 2, 3], (False, True, False), 10.0),
        _row(("branch", 13, "nominal"), [190, 250, 270], [4, 5, 6], (True, True, True), 9.0),
        _row(("branch", 21, "nominal"), [190, 250, 270], [3, 4, 5], (True, True, True), 8.0),
    ]

    objective_cases = build_objective_case_rows(rows, features=("score_sum",))
    objective_rows = summarize_objectives(objective_cases, features=("score_sum",))
    case_rows = build_case_summary_rows(objective_cases)

    assert objective_rows[0]["top1_all_truth_case_count"] == 1
    assert objective_rows[0]["first_truth_top3_case_count"] == 2
    assert minimal_all_case_budget(objective_rows, 2) == (3, "score_sum")
    assert case_rows[0]["best_budget_label"] == "top10_rank_gate"


def test_cross_validation_and_summary_keep_detector_fwi_blocked():
    rows = [
        _row(("branch", 13, "nominal"), [240, 250, 260], [1, 2, 3], (False, True, False), 10.0),
        _row(("branch", 13, "nominal"), [190, 250, 270], [4, 5, 6], (True, True, True), 9.0),
        _row(("branch", 21, "nominal"), [240, 250, 260], [1, 2, 3], (False, True, False), 10.0),
        _row(("branch", 21, "nominal"), [190, 250, 270], [4, 5, 6], (True, True, True), 9.0),
    ]
    objective_cases = build_objective_case_rows(rows, features=("score_sum", "rank_sum_inverse"))
    objective_rows = summarize_objectives(objective_cases, features=("score_sum", "rank_sum_inverse"))
    case_rows = build_case_summary_rows(objective_cases)
    cv_summary, _cv_cases = cross_validate_objectives(objective_cases, "leave_one_case")
    summary = summarize_audit(
        rows,
        objective_rows,
        case_rows,
        [{"branch_key": "branch", "case_count": 2}],
        [cv_summary, {"cv_strategy": "leave_one_seed"}, {"cv_strategy": "leave_one_branch"}],
        {},
    )

    assert cv_summary["top1_all_truth_case_count"] == 0
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["ready_for_rank_gated_upper_bound_claim"] is True
    assert summary["gpu_priority"] == "none"
    assert math.isclose(summary["all_truth_triple_fraction"], 0.5)
