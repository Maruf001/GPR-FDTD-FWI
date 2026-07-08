import pytest

from run_gssi_field_cue_spacing_sensitivity_audit import (
    build_threshold_rows,
    parse_thresholds,
    summarize_threshold_sensitivity,
)


def test_parse_thresholds_sorts_deduplicates_and_rejects_invalid():
    assert parse_thresholds("0.20,0.10,0.10") == [0.10, 0.20]
    with pytest.raises(ValueError):
        parse_thresholds("0.1,0")


def test_threshold_sensitivity_preserves_not_resolution_benchmark():
    cue_rows = [
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 1, "x_m": 0.10, "time_ns": 0.70},
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 2, "x_m": 0.40, "time_ns": 0.72},
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 3, "x_m": 0.80, "time_ns": 1.10},
    ]
    rows = build_threshold_rows(
        cue_rows,
        [0.05, 0.50],
        duplicate_x_m=0.005,
        geometry={"classification": "independent_2d_line_profiles"},
        apparent_depth={"policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth"},
        field_policy={"policy_label": "field_2d_qc_not_3d_or_fwi"},
    )
    summary = summarize_threshold_sensitivity(rows, close_context_max_mm=50.0)

    assert rows[0]["same_time_lateral_pair_count"] == 1
    assert rows[1]["same_time_lateral_pair_count"] == 3
    assert summary["policy_label"] == "field_cue_spacing_context_threshold_robust_not_resolution_benchmark"
    assert summary["all_thresholds_wider_than_synthetic_close_context"] is True
    assert summary["ready_for_resolution_benchmark"] is False
    assert summary["gpu_priority"] == "none"
