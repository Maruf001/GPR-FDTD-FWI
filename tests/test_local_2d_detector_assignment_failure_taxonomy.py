from run_local_2d_detector_assignment_failure_taxonomy import (
    best_case_rows,
    branch_summary_rows,
    failure_label,
    summarize,
)


def _row(seed, hits, hit_count, status="assigned", config="cfg_a", policy="top20_minx8"):
    return {
        "branch_key": "target2_close14",
        "seed": str(seed),
        "case_variant": "nominal",
        "run_name": f"case_{seed}",
        "config_key": config,
        "assignment_policy_key": policy,
        "assignment_method": "score",
        "candidate_budget": "20",
        "min_x_separation_mm": "8",
        "assignment_status": status,
        "unique_truth_hit_count": str(hit_count),
        "unique_all_truths_within_tolerance": all(hits),
        "unique_target0_hit": hits[0],
        "unique_target1_hit": hits[1],
        "unique_target2_hit": hits[2],
        "assigned_x_values_mm": "190,250,264" if status == "assigned" else "",
        "assigned_detection_ranks": "3,5,7" if status == "assigned" else "",
    }


def test_failure_label_names_missed_targets():
    assert failure_label(_row(13, (True, True, True), 3)) == "all_truth"
    assert failure_label(_row(13, (False, True, False), 1)) == "middle_only_target0_target2_missed"
    assert failure_label(_row(13, (False, True, True), 2)) == "target0_missed"
    assert failure_label(_row(13, (False, False, False), 0, status="no_assignment")) == "no_assignment"


def test_best_case_rows_choose_highest_hit_row_and_branch_summary():
    rows = [
        _row(13, (False, True, False), 1, config="weak"),
        _row(13, (False, True, True), 2, config="better"),
        _row(21, (True, True, True), 3, config="all"),
    ]

    cases = best_case_rows(rows)
    branches = branch_summary_rows(cases)
    summary = summarize(
        cases,
        branches,
        [],
        {
            "best_unique_all_truth_case_count": 1,
            "best_mean_unique_truth_hit_count": 1.5,
            "best_config_key": "shared_cfg",
            "best_assignment_policy_key": "shared_policy",
        },
    )

    assert len(cases) == 2
    assert cases[0]["best_config_key"] == "better"
    assert cases[0]["failure_label"] == "target0_missed"
    assert branches[0]["case_count"] == 2
    assert branches[0]["all_truth_case_count"] == 1
    assert summary["all_truth_case_count"] == 1
    assert summary["oracle_all_truth_case_count"] == 1
    assert summary["selection_scope"] == "per_case_best_assignment_policy_oracle"
    assert summary["deployable_shared_policy_all_truth_case_count"] == 1
    assert summary["deployable_shared_policy_config_key"] == "shared_cfg"
    assert summary["target1_hit_count"] == 2
    assert summary["gpu_used"] is False
