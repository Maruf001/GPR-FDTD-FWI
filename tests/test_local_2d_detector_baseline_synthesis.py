from inversion.rebar_detection import RebarDetectionCandidate
from run_local_2d_detector_baseline_synthesis import (
    branch_summary_rows,
    build_case_row,
    case_outcome,
    summarize,
    unique_truth_assignment,
)


def _plan_row(branch="target2_close14"):
    return {
        "branch_key": branch,
        "seed": "13",
        "case_variant": "nominal",
        "case_label": "noise_seed13",
        "run_name": "detector_run",
        "existing_output_dir": "outputs/experiments/001_detector_run",
    }


def _summary(hits, truth_x_values=None, candidates=None):
    if truth_x_values is None:
        truth_x_values = [190.0, 250.0, 264.0]
    if candidates is None:
        candidates = [
            {"rank": 1, "x_mm": 261.0, "z_mm": 88.0, "normalized_score": 1.2},
            {"rank": 2, "x_mm": 249.0, "z_mm": 89.0, "normalized_score": 1.1},
            {"rank": 3, "x_mm": 257.0, "z_mm": 90.0, "normalized_score": 0.9},
        ]
    metrics = []
    for truth_x, hit, x_error in zip(truth_x_values, hits, [60.0, 1.0, 2.0]):
        metrics.append({
            "truth_x_mm": truth_x,
            "truth_z_mm": 90.0,
            "matched_rank": 1,
            "x_error_mm": x_error,
            "z_error_mm": 1.0,
            "within_tolerance": hit,
        })
    return {
        "all_truths_within_tolerance": all(hits),
        "elapsed_time_s": 80.0,
        "candidates": candidates,
        "match_metrics": metrics,
    }


def test_case_outcome_labels_close14_pair_hit():
    assert case_outcome("target2_close14", [False, True, True]) == "close_pair_detected_left_target_missed"
    assert case_outcome("target2_close50_linear29p5", [False, True, False]) == "middle_target_only_detected"
    assert case_outcome("target2_close14", [True, True, True]) == "all_truths_detected"


def test_build_case_row_extracts_truth_hits_and_candidate_span():
    row = build_case_row(_plan_row(), _summary([False, True, True]))

    assert row["truth_hit_count"] == 2
    assert row["target0_hit"] is False
    assert row["target1_hit"] is True
    assert row["target2_hit"] is True
    assert row["unique_truth_hit_count"] == 2
    assert row["unique_target0_hit"] is False
    assert row["unique_target1_hit"] is True
    assert row["unique_target2_hit"] is True
    assert row["missed_truth_x_values_mm"] == "190"
    assert row["matched_truth_x_values_mm"] == "250,264"
    assert row["candidate_x_span_mm"] == 12.0
    assert row["outcome"] == "close_pair_detected_left_target_missed"


def test_unique_truth_assignment_requires_distinct_candidates():
    metrics = _summary([True, True, False])["match_metrics"]
    candidates = [
        {"rank": 1, "x_mm": 220.0, "z_mm": 90.0},
        {"rank": 2, "x_mm": 250.0, "z_mm": 90.0},
        {"rank": 3, "x_mm": 251.0, "z_mm": 91.0},
    ]

    assignment = unique_truth_assignment(candidates, metrics)

    assert assignment["unique_truth_hit_count"] == 1
    assert assignment["unique_truth_hits"] == [False, True, False]


def test_unique_truth_assignment_accepts_live_detector_candidates():
    metrics = _summary([True, True, False])["match_metrics"]
    candidates = [
        RebarDetectionCandidate(
            x_m=0.220,
            z_m=0.090,
            score=1.0,
            normalized_score=1.0,
            support_fraction=1.0,
        ),
        RebarDetectionCandidate(
            x_m=0.250,
            z_m=0.090,
            score=0.9,
            normalized_score=0.9,
            support_fraction=1.0,
        ),
        RebarDetectionCandidate(
            x_m=0.251,
            z_m=0.091,
            score=0.8,
            normalized_score=0.8,
            support_fraction=1.0,
        ),
    ]

    assignment = unique_truth_assignment(candidates, metrics)

    assert assignment["unique_truth_hit_count"] == 1
    assert assignment["unique_truth_hits"] == [False, True, False]


def test_branch_and_global_summary_mark_detector_as_weak_baseline():
    rows = [
        build_case_row(_plan_row("target2_close14"), _summary([False, True, True])),
        build_case_row(
            _plan_row("target2_close50_linear29p5"),
            _summary(
                [False, True, False],
                truth_x_values=[190.0, 250.0, 300.0],
                candidates=[
                    {"rank": 1, "x_mm": 252.0, "z_mm": 88.0, "normalized_score": 1.2},
                    {"rank": 2, "x_mm": 274.0, "z_mm": 80.0, "normalized_score": 1.1},
                    {"rank": 3, "x_mm": 220.0, "z_mm": 90.0, "normalized_score": 0.9},
                ],
            ),
        ),
    ]
    branches = branch_summary_rows(rows)
    summary = summarize(rows, branches, {"policy_label": "plan"})

    assert len(branches) == 2
    assert summary["case_count"] == 2
    assert summary["all_truth_case_count"] == 0
    assert summary["target0_hit_count"] == 0
    assert summary["target1_hit_count"] == 2
    assert summary["target2_hit_count"] == 1
    assert summary["unique_all_truth_case_count"] == 0
    assert summary["unique_target0_hit_count"] == 0
    assert summary["unique_target1_hit_count"] == 2
    assert summary["unique_target2_hit_count"] == 1
    assert summary["gpu_used"] is False
    assert summary["detector_baseline_status"] == "completed_but_not_positive_comparator"
