from run_local_2d_branch_preservation_threshold_sensitivity import (
    build_threshold_rows,
    retained_count,
    summarize_sensitivity,
    summarize_threshold,
)


def _records():
    return [
        {
            "target_index": 1,
            "selected_truth_lateral": False,
            "truth_lateral_available": True,
            "truth_lateral_gap_abs": 0.006,
            "truth_lateral_gap_rel": 0.09,
            "candidate_gaps": [(0.0, 0.0), (0.006, 0.09), (0.02, 0.3)],
        },
        {
            "target_index": 2,
            "selected_truth_lateral": True,
            "truth_lateral_available": True,
            "truth_lateral_gap_abs": 0.0,
            "truth_lateral_gap_rel": 0.0,
            "candidate_gaps": [(0.0, 0.0), (0.004, 0.05)],
        },
    ]


def test_retained_count_keeps_best_and_threshold_rows():
    assert retained_count([(0.0, 0.0), (0.006, 0.09), (0.02, 0.3)], 0.01, 0.10) == 2
    assert retained_count([(0.0, 0.0), (0.006, 0.09), (0.02, 0.3)], 0.005, 0.10) == 1


def test_summarize_threshold_recovers_missed_truth_lateral_with_cost():
    summary = summarize_threshold(_records(), 0.01, 0.10)

    assert summary["audited_step_count"] == 2
    assert summary["missed_truth_lateral_available_count"] == 1
    assert summary["missed_truth_lateral_recovered_count"] == 1
    assert summary["mean_extra_candidates_per_step"] == 1.0


def test_sensitivity_summary_keeps_gpu_blocked():
    rows = build_threshold_rows(_records(), [0.005, 0.01], [0.05, 0.10])
    summary = summarize_sensitivity(rows, default_abs=0.01, default_rel=0.10)

    assert summary["default_recovered_count"] == 1
    assert summary["max_recovered_count"] == 1
    assert summary["default_recovers_max_count"] is True
    assert summary["ready_for_default_threshold_policy"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
