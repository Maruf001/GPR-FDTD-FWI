import pytest

from run_local_2d_detector_refreshed_selector_gap_audit import (
    build_gap_rows,
    missing_targets,
    rank_gate_label,
    summarize_gap_audit,
)


def selector_case(case_label, feature="score_component_balanced", branch="target2_close14"):
    return {
        "feature_family": "component_only",
        "selector_strategy": "branch",
        "case_label": case_label,
        "branch_key": branch,
        "seed": "13",
        "case_variant": "nominal",
        "run_name": f"{case_label}_run",
        "selected_feature": feature,
    }


def objective_case(
    case_label,
    feature,
    rank,
    *,
    false_gap=0.1,
    target0=False,
    target1=True,
    target2=True,
):
    return {
        "case_label": case_label,
        "branch_key": "target2_close14",
        "seed": "13",
        "case_variant": "nominal",
        "run_name": f"{case_label}_run",
        "feature": feature,
        "candidate_triple_count": "20",
        "all_truth_triple_count": "2",
        "first_all_truth_rank": str(rank),
        "best_false_minus_best_truth_score_gap": str(false_gap),
        "top_unique_truth_hit_count": "2",
        "top_target0_hit": str(target0),
        "top_target1_hit": str(target1),
        "top_target2_hit": str(target2),
        "top_candidate_x_values_mm": "220,250,264",
        "top_candidate_ranks": "2,1,3",
    }


def selector_summary():
    return {
        "policy_label": "local_2d_detector_selector_feature_family_audit_cpu_no_fwi",
        "best_feature_family": "component_only",
        "best_selector_strategy": "branch",
    }


def test_rank_gate_label_boundaries():
    assert rank_gate_label(1) == "top1"
    assert rank_gate_label(10) == "top10"
    assert rank_gate_label(50) == "top50"
    assert rank_gate_label(100) == "top100"
    assert rank_gate_label(200) == "top200"
    assert rank_gate_label(201) == "deeper_than_top200"


def test_missing_targets_reports_false_top_hits():
    assert missing_targets({"top_target0_hit": "False", "top_target1_hit": "True", "top_target2_hit": "False"}) == "target0,target2"
    assert missing_targets({"top_target0_hit": "True", "top_target1_hit": "True", "top_target2_hit": "True"}) == "none"


def test_build_gap_rows_compares_refreshed_selector_to_case_best():
    selectors = [selector_case("case_a")]
    objectives = [
        objective_case("case_a", "score_component_balanced", 40, target0=False),
        objective_case("case_a", "rank_sum_inverse", 12, false_gap=-0.2, target0=True),
    ]

    rows = build_gap_rows(selectors, objectives, selector_summary())

    assert len(rows) == 1
    assert rows[0]["selected_first_all_truth_rank"] == 40
    assert rows[0]["selected_rank_gate_label"] == "top50"
    assert rows[0]["case_best_feature"] == "rank_sum_inverse"
    assert rows[0]["rank_penalty_vs_case_best"] == pytest.approx(28)
    assert rows[0]["selected_top_missing_targets"] == "target0"


def test_summary_keeps_detector_seeded_fwi_blocked_without_top1_truth():
    selectors = [selector_case("case_a"), selector_case("case_b", branch="target2_close50_linear29p5")]
    objectives = [
        objective_case("case_a", "score_component_balanced", 12, target0=False),
        objective_case("case_a", "rank_sum_inverse", 5, false_gap=-0.1, target0=True),
        objective_case("case_b", "score_component_balanced", 151, false_gap=0.4, target0=False, target1=False),
        objective_case("case_b", "rank_sum_inverse", 80, false_gap=0.2, target0=False, target1=False),
    ]

    gap_rows = build_gap_rows(selectors, objectives, selector_summary())
    summary = summarize_gap_audit(gap_rows, [], selector_summary())

    assert summary["case_count"] == 2
    assert summary["selected_top1_case_count"] == 0
    assert summary["selected_top200_case_count"] == 2
    assert summary["rank_penalty_vs_case_best_case_count"] == 2
    assert summary["ready_for_rank_gated_selector_claim"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
