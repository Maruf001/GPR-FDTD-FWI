from run_local_2d_detector_component_waveform_gate import (
    build_case_objective_rows,
    build_objective_rows,
    component_variant_scores,
    summarize,
)
from run_local_2d_detector_rank_budget_diagnostic import build_budget_rows


def _base_row(case: str, all_truth: bool, targets: tuple[bool, bool, bool], **scores) -> dict:
    row = {
        "case_label": case,
        "branch_key": "branch",
        "seed": "13",
        "case_variant": "nominal",
        "unique_all_truths_within_tolerance": str(all_truth),
        "unique_truth_hit_count": "3" if all_truth else "1",
        "unique_target0_hit": str(targets[0]),
        "unique_target1_hit": str(targets[1]),
        "unique_target2_hit": str(targets[2]),
        "candidate_ranks": "1,2,3",
        "candidate_x_values_mm": "190,250,264",
        "x_span_mm": "74",
        "gap_balance_mm": "46",
        "score_span_bonus": "2.5",
    }
    row.update(scores)
    return row


def test_component_variant_scores_include_floor_span_and_hybrid_terms():
    row = {"x_span_mm": "100", "gap_balance_mm": "20", "score_span_bonus": "3.0"}
    scores = component_variant_scores(row, [0.2, 0.4, 0.6])

    assert round(scores["score_component_sum"], 6) == 1.2
    assert scores["score_component_min"] == 0.2
    assert scores["score_component_mean_min"] == 0.6
    assert scores["score_component_floor_span"] == 0.45
    assert round(scores["score_component_balanced"], 6) == 1.79
    assert scores["score_component_left_floor"] == 0.7
    assert scores["score_hybrid_span_component"] == 3.2


def test_component_objective_summary_tracks_top_rank_and_target_hits():
    rows = [
        _base_row("case_a", False, (False, True, True), score_component_balanced="4", score_component_floor_span="1"),
        _base_row("case_a", True, (True, True, True), score_component_balanced="3", score_component_floor_span="5"),
        _base_row("case_b", False, (False, True, False), score_component_balanced="5", score_component_floor_span="1"),
        _base_row("case_b", True, (True, True, True), score_component_balanced="4", score_component_floor_span="5"),
    ]

    case_rows = build_case_objective_rows(rows, objectives=("component_balanced", "component_floor_span"))
    objective_rows = build_objective_rows(case_rows)

    by_objective = {row["objective"]: row for row in objective_rows}
    assert by_objective["component_balanced"]["top1_all_truth_case_count"] == 0
    assert by_objective["component_balanced"]["top1_target0_hit_count"] == 0
    assert by_objective["component_balanced"]["first_truth_top3_case_count"] == 2
    assert by_objective["component_floor_span"]["top1_all_truth_case_count"] == 2
    assert by_objective["component_floor_span"]["top1_target0_hit_count"] == 2


def test_component_summary_reports_improvement_but_blocks_fwi():
    rows = [
        _base_row("case_a", False, (False, True, True), score_component_balanced="4"),
        _base_row("case_a", True, (True, True, True), score_component_balanced="3"),
        _base_row("case_b", False, (False, True, False), score_component_balanced="5"),
        _base_row("case_b", True, (True, True, True), score_component_balanced="4"),
    ]
    case_rows = build_case_objective_rows(rows, objectives=("component_balanced",))
    objective_rows = build_objective_rows(case_rows)
    budget_rows = build_budget_rows(objective_rows)

    summary = summarize(
        rows,
        case_rows,
        objective_rows,
        budget_rows,
        component_candidate_count=4,
        source_summary={
            "policy_label": "source_policy",
            "best_top10_case_count": 1,
            "best_top50_case_count": 1,
        },
    )

    assert summary["source_policy_label"] == "source_policy"
    assert summary["best_top10_case_count"] == 2
    assert summary["top10_improvement_over_source"] == 1
    assert summary["top50_improvement_over_source"] == 1
    assert summary["component_candidate_count"] == 4
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
