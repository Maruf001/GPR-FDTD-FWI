import math

import numpy as np

from run_gssi_field_short_profile_stack_policy import (
    align_comparison_to_reference,
    aligned_event_x_m,
    build_stack_rows,
    find_stack_anchor_candidates,
    reversed_event_pairs,
    summarize_policy,
)


def test_align_comparison_to_reference_positive_lag():
    comparison = np.array([10, 11, 12, 13, 14], dtype=float)

    aligned = align_comparison_to_reference(comparison, "direct", lag_samples=2)

    assert np.allclose(aligned[:3], [12, 13, 14])
    assert math.isnan(aligned[3])
    assert math.isnan(aligned[4])


def test_aligned_event_x_reverses_and_shifts():
    assert round(aligned_event_x_m(0.2, 1.0, "reversed", 0.1), 6) == 0.7
    assert round(aligned_event_x_m(0.2, 1.0, "direct", -0.1), 6) == 0.3


def test_find_stack_anchor_candidates_requires_repeat_agreement():
    x_m = np.arange(7, dtype=float) * 0.1
    ref = np.array([0.0, 0.2, 2.5, 0.2, 0.1, 2.0, 0.1])
    cmp = np.array([0.0, 0.1, 2.3, 0.3, 0.1, 0.2, 0.1])
    rows = build_stack_rows(x_m, ref, cmp)

    anchors = find_stack_anchor_candidates(
        rows,
        min_separation_m=0.15,
        min_stack_z=1.0,
        max_repeat_delta_z=0.5,
        max_count=4,
    )

    assert len(anchors) == 1
    assert anchors[0]["candidate_index"] == 1
    assert round(anchors[0]["x_m"], 3) == 0.2
    assert anchors[0]["stability_label"] == "stable_stack_anchor"


def test_reversed_event_pairs_pairs_nearest_aligned_events():
    rows = [
        {"file": "PROJECT001C__014.DZT", "apex_group": 1, "x_m": 0.10, "accepted_phase_time_ns": 0.5, "best_radius_mm": 5, "best_abs_correlation": 0.8},
        {"file": "PROJECT001C__014.DZT", "apex_group": 2, "x_m": 0.40, "accepted_phase_time_ns": 0.6, "best_radius_mm": 5, "best_abs_correlation": 0.82},
        {"file": "PROJECT001C__016.DZT", "apex_group": 1, "x_m": 0.58, "accepted_phase_time_ns": 0.7, "best_radius_mm": 6, "best_abs_correlation": 0.81},
        {"file": "PROJECT001C__016.DZT", "apex_group": 2, "x_m": 0.28, "accepted_phase_time_ns": 0.8, "best_radius_mm": 6, "best_abs_correlation": 0.83},
    ]

    pairs = reversed_event_pairs(
        rows,
        "PROJECT001C__014",
        "PROJECT001C__016",
        comparison_profile_length_m=0.7,
        orientation="reversed",
        lag_m=0.0,
        max_pair_distance_m=0.05,
    )

    assert [row["comparison_apex_group"] for row in pairs] == [1, 2]
    assert [round(row["aligned_x_residual_mm"], 3) for row in pairs] == [20.0, 20.0]
    assert pairs[0]["comparison_minus_reference_phase_time_ns"] == 0.19999999999999996


def test_summarize_policy_labels_ready_when_stack_and_events_are_stable():
    best = {"orientation": "reversed", "lag_mm": 80.0, "lag_m": 0.08, "normalized_correlation": 0.93}
    direct = {"normalized_correlation": 0.7}
    reversed_best = {"normalized_correlation": 0.93}
    anchors = [{"stability_label": "stable_stack_anchor"} for _ in range(3)]
    pairs = [
        {"aligned_x_residual_mm": 10.0, "comparison_minus_reference_phase_time_ns": 0.1, "radius_match": False},
        {"aligned_x_residual_mm": -20.0, "comparison_minus_reference_phase_time_ns": 0.2, "radius_match": False},
        {"aligned_x_residual_mm": 15.0, "comparison_minus_reference_phase_time_ns": 0.15, "radius_match": True},
    ]

    summary = summarize_policy(best, direct, reversed_best, anchors, pairs)

    assert summary["policy_label"] == "repeat_stack_timing_qc_ready"
    assert summary["radius_match_count"] == 1
