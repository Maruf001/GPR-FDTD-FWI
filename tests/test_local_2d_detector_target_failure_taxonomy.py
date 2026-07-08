from run_local_2d_detector_target_failure_taxonomy import (
    build_target_failure_rows,
    missing_targets,
    summarize_branches,
    summarize_target_failures,
)


def _gap_row(
    *,
    case_label="case_a",
    branch_key="target2_close14",
    seed=13,
    selected_all_truth=False,
    failure_label="missing_target1",
    required_gain=0.2,
    all_truth_count=4,
):
    return {
        "case_label": case_label,
        "branch_key": branch_key,
        "seed": seed,
        "case_variant": "nominal",
        "selected_all_truth": str(selected_all_truth),
        "selected_failure_label": failure_label,
        "selected_unique_truth_hit_count": 2 if not selected_all_truth else 3,
        "best_truth_unique_truth_hit_count": 3,
        "all_truth_triple_count": all_truth_count,
        "required_selector_gain_to_choose_truth": required_gain,
        "dominant_loss_feature": "signed_gap_prior_score",
        "selected_candidate_ranks": "9,3,2",
        "selected_candidate_x_values_mm": "188,250,266",
        "selected_candidate_z_values_mm": "85,78,90",
        "best_truth_candidate_ranks": "9,4,2",
        "best_truth_candidate_x_values_mm": "188,252,266",
        "best_truth_candidate_z_values_mm": "85,87,90",
    }


def test_missing_targets_parses_compound_failure_labels():
    assert missing_targets("all_truth") == []
    assert missing_targets("missing_target1") == ["target1"]
    assert missing_targets("missing_target0_target1_target2") == ["target0", "target1", "target2"]


def test_target_failure_rows_classify_single_and_multi_target_losses():
    rows = build_target_failure_rows(
        [
            _gap_row(failure_label="missing_target1"),
            _gap_row(case_label="case_b", failure_label="missing_target0_target2"),
            _gap_row(case_label="case_c", selected_all_truth=True, failure_label="all_truth", required_gain=0.0),
        ]
    )
    by_case = {row["case_label"]: row for row in rows}

    assert by_case["case_a"]["target_failure_scope"] == "single_target_missing"
    assert by_case["case_a"]["missing_target1"] is True
    assert by_case["case_b"]["target_failure_scope"] == "multi_target_missing"
    assert by_case["case_b"]["missing_target0"] is True
    assert by_case["case_b"]["missing_target2"] is True
    assert by_case["case_c"]["target_failure_scope"] == "selected_truth"


def test_summary_marks_target1_as_dominant_and_keeps_fwi_blocked():
    case_rows = build_target_failure_rows(
        [
            _gap_row(case_label="case_a", branch_key="target2_close14", failure_label="missing_target1", required_gain=0.2),
            _gap_row(case_label="case_b", branch_key="target2_close14", failure_label="missing_target1_target2", required_gain=0.3),
            _gap_row(case_label="case_c", branch_key="target2_close50_linear29p5", failure_label="missing_target0_target1", required_gain=0.5),
            _gap_row(
                case_label="case_d",
                branch_key="target2_close50_linear29p5",
                selected_all_truth=True,
                failure_label="all_truth",
                required_gain=0.0,
            ),
        ]
    )
    branch_rows = summarize_branches(case_rows)

    summary = summarize_target_failures(case_rows, branch_rows, {"policy_label": "source_gap"})

    assert summary["policy_label"] == "local_2d_detector_target_failure_taxonomy_cpu_no_fwi"
    assert summary["source_gap_policy_label"] == "source_gap"
    assert summary["case_count"] == 4
    assert summary["failed_selector_case_count"] == 3
    assert summary["missing_target1_case_count"] == 3
    assert summary["dominant_missing_target"] == "target1"
    assert summary["multi_target_missing_case_count"] == 2
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
