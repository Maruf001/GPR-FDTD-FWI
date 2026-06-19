import math

from run_gssi_field_short_profile_content_window_policy import (
    build_content_windows,
    classify_event_content,
    nearest_anchor,
    summarize_content_policy,
)


def test_nearest_anchor_returns_distance():
    anchors = [
        {"x_m": 0.10, "candidate_index": 1},
        {"x_m": 0.40, "candidate_index": 2},
    ]

    anchor, distance = nearest_anchor(0.37, anchors)

    assert anchor["candidate_index"] == 2
    assert round(distance, 3) == 0.03


def test_build_content_windows_links_nearest_event():
    stack_rows = [
        {"x_m": 0.36, "x_mm": 360, "stack_signature_z": 4.0, "repeat_delta_z": 0.2, "repeat_score_z": 3.9, "both_profiles_present": True},
        {"x_m": 0.40, "x_mm": 400, "stack_signature_z": 5.0, "repeat_delta_z": 0.3, "repeat_score_z": 4.85, "both_profiles_present": True},
        {"x_m": 0.44, "x_mm": 440, "stack_signature_z": 4.5, "repeat_delta_z": 0.4, "repeat_score_z": 4.3, "both_profiles_present": True},
    ]
    anchors = [{"x_m": 0.40, "candidate_index": 7, "stability_label": "stable_stack_anchor", "stack_signature_z": 5.0, "repeat_delta_z": 0.3, "repeat_score_z": 4.85}]
    events = [{"pair_index": 2, "reference_x_m": 0.405}]

    windows = build_content_windows(stack_rows, anchors, events, half_width_m=0.05)

    assert len(windows) == 1
    assert windows[0]["anchor_candidate_index"] == 7
    assert windows[0]["nearest_event_pair_index"] == 2
    assert round(windows[0]["nearest_event_distance_mm"], 3) == 5.0
    assert round(windows[0]["window_median_repeat_delta_z"], 3) == 0.3


def test_classify_event_content_marks_timing_only_event():
    events = [
        {"pair_index": 1, "reference_apex_group": 1, "comparison_apex_group": 3, "reference_x_m": 0.13, "comparison_aligned_x_m": 0.12, "aligned_x_residual_mm": -10, "comparison_minus_reference_phase_time_ns": 0.18, "reference_best_radius_mm": 6, "comparison_best_radius_mm": 5, "radius_match": "False"},
        {"pair_index": 2, "reference_apex_group": 2, "comparison_apex_group": 2, "reference_x_m": 0.40, "comparison_aligned_x_m": 0.39, "aligned_x_residual_mm": -10, "comparison_minus_reference_phase_time_ns": 0.11, "reference_best_radius_mm": 8, "comparison_best_radius_mm": 5, "radius_match": "False"},
    ]
    anchors = [{"x_m": 0.397, "candidate_index": 1, "stability_label": "stable_stack_anchor"}]
    bootstrap = {"summary": {"observed_median_offset_ns": 0.12, "min_bootstrap_ci_lower_ns": 0.10, "max_bootstrap_ci_upper_ns": 0.15}}

    rows = classify_event_content(events, anchors, bootstrap, max_event_anchor_distance_m=0.04)

    assert rows[0]["content_label"] == "timing_only_no_stable_content_anchor"
    assert rows[1]["content_label"] == "repeat_content_anchor"
    assert rows[1]["within_bootstrap_ci_envelope"] is True
    assert math.isclose(rows[1]["timing_residual_to_bootstrap_median_ns"], -0.01)


def test_summarize_content_policy_labels_limited_when_one_event_timing_only():
    content_windows = [{"content_window_index": 1}, {"content_window_index": 2}]
    event_rows = [
        {"content_backed": True, "nearest_anchor_distance_mm": 5, "timing_residual_to_bootstrap_median_ns": 0.01},
        {"content_backed": True, "nearest_anchor_distance_mm": 10, "timing_residual_to_bootstrap_median_ns": -0.01},
        {"content_backed": False, "nearest_anchor_distance_mm": 250, "timing_residual_to_bootstrap_median_ns": 0.06},
    ]
    bootstrap = {"summary": {"policy_label": "bootstrap_relative_time_zero_supported_qc", "observed_median_offset_ns": 0.12, "min_bootstrap_ci_lower_ns": 0.10, "max_bootstrap_ci_upper_ns": 0.15}}

    summary = summarize_content_policy(content_windows, event_rows, bootstrap, min_content_windows=2)

    assert summary["policy_label"] == "repeat_content_windows_limited_qc"
    assert summary["content_backed_event_pair_count"] == 2
    assert summary["timing_only_event_pair_count"] == 1
    assert round(summary["max_abs_content_timing_residual_to_bootstrap_median_ns"], 3) == 0.01
