import math

from run_coordinate_weak_exact_exception_triage import (
    classify_exception,
    exception_run_ids,
    objective_top_candidate_metrics,
)


def test_exception_run_ids_collects_policy_exceptions():
    rows = [
        {"strongest_secondary_nonaccepted_run_ids": "1136"},
        {"strongest_secondary_nonaccepted_run_ids": ""},
        {"strongest_secondary_nonaccepted_run_ids": "785, 999"},
    ]

    assert exception_run_ids(rows) == [785, 999, 1136]


def test_classify_exception_marks_legacy_ringdown_as_low_gpu_priority():
    label = classify_exception(
        ringdown_value=0.25,
        margin_deficit=8.0e-5,
        relative_deficit=0.16,
        best_secondary_ratio_to_base=1.2,
    )

    assert label == "legacy_archive_exception_no_gpu_priority"


def test_classify_exception_marks_near_threshold_modern_case():
    label = classify_exception(
        ringdown_value=0.5,
        margin_deficit=4.7e-6,
        relative_deficit=0.0094,
        best_secondary_ratio_to_base=1.28,
    )

    assert label == "near_threshold_modern_exception_monitor"


def test_objective_top_candidate_metrics_reports_rank_gap():
    rows = [
        {
            "objective_label": "highband",
            "rank": "2",
            "radius_mm": "5.25",
            "misfit": "0.00072",
        },
        {
            "objective_label": "highband",
            "rank": "1",
            "radius_mm": "5.0",
            "misfit": "0.00023",
        },
    ]

    metrics = objective_top_candidate_metrics(rows, "highband")

    assert metrics["highband_rank1_radius_mm"] == 5.0
    assert metrics["highband_rank2_radius_mm"] == 5.25
    assert math.isclose(metrics["highband_rank2_minus_rank1_misfit"], 0.00049)
