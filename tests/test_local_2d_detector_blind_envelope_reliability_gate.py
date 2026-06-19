from run_local_2d_detector_blind_envelope_reliability_gate import (
    branch_reliability_rows,
    case_reliability_rows,
    parse_number_list,
    reliability_label,
    summarize_reliability,
)


def _row(case, branch, seed, selected_x, hit=True, score="1.0"):
    return {
        "case_label": case,
        "branch_key": branch,
        "seed": str(seed),
        "case_variant": "nominal",
        "selected_x_values_mm": selected_x,
        "selected_z_values_mm": "90,90,90",
        "selection_score": score,
        "all_target_slots_hit": str(hit),
    }


def test_parse_number_list_and_label_handle_bad_values():
    assert parse_number_list("190, 250, bad, 300") == [190.0, 250.0, 300.0]
    assert reliability_label(5.0) == "stable_truth_free_assignment"
    assert reliability_label(5.1) == "review_policy_grid_position_drift"


def test_case_reliability_rows_use_truth_free_x_slot_range():
    rows = [
        _row("stable", "target2_close14", 13, "190,250,264", True),
        _row("stable", "target2_close14", 13, "191,250,264", True),
        _row("review", "target2_close50_linear29p5", 34, "183,237,296", False),
        _row("review", "target2_close50_linear29p5", 34, "183,256,296", True),
    ]

    cases = {row["case_label"]: row for row in case_reliability_rows(rows)}

    assert cases["stable"]["truth_free_stable_assignment"] is True
    assert cases["stable"]["max_slot_x_range_mm"] == 1.0
    assert cases["stable"]["success_fraction_truth_eval"] == 1.0
    assert cases["review"]["truth_free_stable_assignment"] is False
    assert cases["review"]["max_slot_x_range_mm"] == 19.0
    assert cases["review"]["tuning_sensitive_truth_eval"] is True


def test_summary_marks_reliability_gate_without_fwi_trigger():
    selected = [
        _row("stable", "target2_close14", 13, "190,250,264", True),
        _row("stable", "target2_close14", 13, "191,250,264", True),
        _row("review", "target2_close50_linear29p5", 34, "183,237,296", False),
        _row("review", "target2_close50_linear29p5", 34, "183,256,296", True),
    ]
    cases = case_reliability_rows(selected)
    branches = branch_reliability_rows(cases)
    summary = summarize_reliability(
        cases,
        branches,
        {"policy_label": "source", "variant_count": 2},
        {"policy_label": "stability"},
        {"policy_label": "tuning"},
    )

    assert summary["stable_assignment_case_count"] == 1
    assert summary["review_assignment_case_count"] == 1
    assert summary["stable_assignment_partial_success_count"] == 0
    assert summary["tuning_sensitive_detected_by_gate_count"] == 1
    assert summary["tuning_sensitive_missed_by_gate_count"] == 0
    assert summary["truth_free_gate_uses_truth"] is False
    assert summary["truth_evaluation_used_for_audit"] is True
    assert summary["ready_for_reliability_claim"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
