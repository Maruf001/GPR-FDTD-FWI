from run_local_2d_detector_blind_envelope_reliability_threshold_sensitivity import (
    summarize_thresholds,
    threshold_sensitivity_rows,
)


def _case(label, max_range, success_fraction, tuning):
    return {
        "case_label": label,
        "max_slot_x_range_mm": str(max_range),
        "success_fraction_truth_eval": str(success_fraction),
        "tuning_sensitive_truth_eval": str(tuning),
    }


def test_threshold_rows_separate_false_review_and_tuning_miss_modes():
    cases = [
        _case("stable_a", 4.0, 1.0, False),
        _case("stable_b", 5.0, 1.0, False),
        _case("review", 20.0, 0.5, True),
    ]

    rows = {
        row["threshold_mm"]: row
        for row in threshold_sensitivity_rows(cases, [4.0, 5.0, 19.0, 20.0])
    }

    assert rows[4.0]["false_review_all_variant_success_count"] == 1
    assert rows[4.0]["clean_gate"] is False
    assert rows[5.0]["clean_gate"] is True
    assert rows[19.0]["clean_gate"] is True
    assert rows[20.0]["tuning_sensitive_missed_count"] == 1
    assert rows[20.0]["clean_gate"] is False


def test_summary_marks_default_threshold_clean_no_fwi():
    cases = [
        _case("stable_a", 4.0, 1.0, False),
        _case("stable_b", 5.0, 1.0, False),
        _case("review", 20.0, 0.5, True),
    ]
    rows = threshold_sensitivity_rows(cases, [4.0, 5.0, 19.0, 20.0])
    summary = summarize_thresholds(
        rows,
        {"policy_label": "reliability", "stable_slot_range_threshold_mm": 5.0},
        {"policy_label": "tuning"},
    )

    assert summary["clean_threshold_count"] == 2
    assert summary["clean_threshold_min_mm"] == 5.0
    assert summary["clean_threshold_max_mm"] == 19.0
    assert summary["default_threshold_clean"] is True
    assert summary["default_threshold_tuning_missed"] == 0
    assert summary["default_threshold_false_review"] == 0
    assert summary["ready_for_reliability_claim"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
