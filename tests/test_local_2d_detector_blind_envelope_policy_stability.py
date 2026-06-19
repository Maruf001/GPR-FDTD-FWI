from run_local_2d_detector_blind_envelope_policy_stability import (
    branch_stability_rows,
    case_stability_rows,
    stability_label,
    summarize_stability,
)


def _row(case, branch, seed, variant, selected_x, hit=True):
    return {
        "case_label": case,
        "branch_key": branch,
        "seed": str(seed),
        "case_variant": "nominal",
        "variant_label": variant,
        "selected_x_values_mm": selected_x,
        "all_target_slots_hit": str(hit),
        "max_target_slot_abs_error_mm": "3.0" if hit else "12.0",
    }


def test_stability_label_separates_partial_and_consensus_cases():
    assert stability_label(0.5, 2, 0.8) == "tuning_sensitive_partial_success"
    assert stability_label(0.95, 2, 0.8) == "near_stable_partial_success"
    assert stability_label(1.0, 1, 1.0) == "full_success_single_selection"
    assert stability_label(1.0, 2, 0.96) == "full_success_dominant_consensus"
    assert stability_label(1.0, 3, 0.5) == "full_success_multi_selection"


def test_case_and_branch_stability_rows_count_successful_variants():
    selected_rows = [
        _row("case_a", "target2_close14", 13, "v1", "190,250,264", True),
        _row("case_a", "target2_close14", 13, "v2", "190,250,264", True),
        _row("case_b", "target2_close50_linear29p5", 13, "v1", "190,250,300", True),
        _row("case_b", "target2_close50_linear29p5", 13, "v2", "190,270,300", False),
    ]

    cases = case_stability_rows(selected_rows)
    branches = branch_stability_rows(cases)
    by_case = {row["case_label"]: row for row in cases}
    by_branch = {row["branch_key"]: row for row in branches}

    assert by_case["case_a"]["success_fraction"] == 1.0
    assert by_case["case_a"]["unique_success_selection_count"] == 1
    assert by_case["case_b"]["success_fraction"] == 0.5
    assert by_case["case_b"]["stability_label"] == "tuning_sensitive_partial_success"
    assert by_branch["target2_close50_linear29p5"]["partial_success_case_count"] == 1


def test_summary_marks_close50_stability_limit_no_fwi():
    case_rows = [
        {
            "case_label": "case_a",
            "branch_key": "target2_close14",
            "success_fraction": 1.0,
            "unique_success_selection_count": 1,
            "dominant_success_fraction_of_all": 1.0,
            "stability_label": "full_success_single_selection",
        },
        {
            "case_label": "case_b",
            "branch_key": "target2_close50_linear29p5",
            "success_fraction": 0.5,
            "unique_success_selection_count": 2,
            "dominant_success_fraction_of_all": 0.25,
            "stability_label": "tuning_sensitive_partial_success",
        },
    ]
    summary = summarize_stability(
        case_rows,
        branch_stability_rows(case_rows),
        {"policy_label": "source", "variant_count": 2},
        {"policy_label": "robust", "robustness_boundary": "branch_limit"},
    )

    assert summary["all_variant_success_case_count"] == 1
    assert summary["partial_success_case_count"] == 1
    assert summary["tuning_sensitive_case_count"] == 1
    assert summary["close50_partial_success_case_count"] == 1
    assert summary["close14_partial_success_case_count"] == 0
    assert summary["tuning_sensitive_case_labels"] == "case_b"
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
