from inversion.rebar_detection import RebarDetectionCandidate
from run_local_2d_detector_blind_assignment_policy import (
    assignment_policy_rows,
    summarize,
    summarize_by_branch,
    summarize_by_policy,
    try_assign_candidates,
)


def _candidate(x_mm, z_mm=90.0, score=1.0):
    return RebarDetectionCandidate(
        x_m=x_mm / 1000.0,
        z_m=z_mm / 1000.0,
        score=score,
        normalized_score=score,
        support_fraction=1.0,
    )


def _row(config_key, policy_key, branch, seed, variant, unique_hits, all_truth=False):
    budget = int(policy_key.split("_")[0].replace("top", ""))
    min_x = float(policy_key.split("minx")[1])
    return {
        "branch_key": branch,
        "seed": seed,
        "case_variant": variant,
        "run_name": f"{branch}_{seed}_{variant}",
        "config_key": config_key,
        "background_mode": config_key.split("_")[0],
        "top_k": 40,
        "separation_profile": "moderate12",
        "time_offset_family": "baseline",
        "assignment_policy_key": policy_key,
        "candidate_budget": budget,
        "min_x_separation_mm": min_x,
        "assignment_status": "assigned",
        "all_truths_within_tolerance": all_truth,
        "unique_all_truths_within_tolerance": all_truth,
        "unique_truth_hit_count": unique_hits,
        "unique_target0_hit": unique_hits >= 1,
        "unique_target1_hit": unique_hits >= 2,
        "unique_target2_hit": unique_hits >= 3,
        "elapsed_time_s": 0.01,
    }


def test_try_assign_candidates_honors_min_x_separation():
    candidates = [
        _candidate(190.0, score=1.0),
        _candidate(250.0, score=0.9),
        _candidate(264.0, score=0.8),
        _candidate(300.0, score=0.7),
    ]

    assigned, status = try_assign_candidates(candidates, 3, 4, 12.0)

    assert status == "assigned"
    assert [round(candidate.x_m * 1000.0) for candidate in assigned] == [190, 250, 264]

    assigned, status = try_assign_candidates(candidates, 3, 3, 20.0)

    assert assigned == []
    assert status == "no_assignment_satisfies_separation"


def test_assignment_policy_rows_include_score_and_span_bonus_methods():
    rows = assignment_policy_rows()

    assert len(rows) == 48
    assert "top40_minx20" in {row["assignment_policy_key"] for row in rows}
    assert "top40_minx20_span1" in {row["assignment_policy_key"] for row in rows}


def test_span_bonus_can_prefer_wider_candidate_combo():
    candidates = [
        _candidate(250.0, score=1.0),
        _candidate(264.0, score=0.95),
        _candidate(270.0, score=0.94),
        _candidate(190.0, score=0.5),
    ]

    score_assigned, score_status = try_assign_candidates(candidates, 3, 4, 5.0)
    assigned, status = try_assign_candidates(candidates, 3, 4, 5.0, span_bonus_weight=2.0)

    assert score_status == "assigned"
    assert [round(candidate.x_m * 1000.0) for candidate in score_assigned] == [250, 264, 270]
    assert status == "assigned"
    assert 190 in [round(candidate.x_m * 1000.0) for candidate in assigned]


def test_blind_assignment_summary_ranks_full_recovery_policy():
    rows = [
        _row("none_top40_moderate12_baseline", "top40_minx12", "close14", 13, "nominal", 3, True),
        _row("none_top40_moderate12_baseline", "top40_minx12", "close50", 13, "nominal", 3, True),
        _row("median_top20_dense4_single667", "top20_minx45", "close14", 13, "nominal", 2),
        _row("median_top20_dense4_single667", "top20_minx45", "close50", 13, "nominal", 1),
    ]

    policy_summary = summarize_by_policy(rows)
    branch_summary = summarize_by_branch(rows)
    summary = summarize(rows, policy_summary, branch_summary)

    assert policy_summary[0]["config_key"] == "none_top40_moderate12_baseline"
    assert policy_summary[0]["unique_all_truth_case_count"] == 2
    assert summary["full_recovery_policy_count"] == 1
    assert summary["best_assignment_policy_key"] == "top40_minx12"
    assert summary["gpu_used"] is False
