import math

from run_gssi_field_cue_spacing_context_audit import (
    build_pair_spacing_rows,
    build_profile_context_rows,
    pair_kind,
    summarize_spacing,
)


def test_pair_kind_separates_duplicate_same_time_and_time_separated():
    assert pair_kind(0.001, 0.30, same_time_ns=0.15, duplicate_x_m=0.005) == "same_x_time_separated_or_vertical"
    assert pair_kind(0.30, 0.10, same_time_ns=0.15, duplicate_x_m=0.005) == "same_time_lateral_spacing"
    assert pair_kind(0.30, 0.40, same_time_ns=0.15, duplicate_x_m=0.005) == "time_separated_lateral_spacing"


def test_pair_spacing_rows_classify_same_time_lateral_pairs():
    rows = [
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 1, "x_m": 0.10, "time_ns": 0.70},
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 2, "x_m": 0.40, "time_ns": 0.72},
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 3, "x_m": 0.40, "time_ns": 1.02},
    ]

    pairs = build_pair_spacing_rows(rows, same_time_ns=0.15, duplicate_x_m=0.005)
    by_kind = {row["pair_kind"]: row for row in pairs}

    assert len(pairs) == 3
    assert math.isclose(by_kind["same_time_lateral_spacing"]["dx_mm"], 300.0)
    assert by_kind["same_x_time_separated_or_vertical"]["dt_ns"] > 0.15


def test_profile_context_and_summary_block_resolution_claims():
    cue_rows = [
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 1, "x_m": 0.10, "time_ns": 0.70, "relative_strength": 10},
        {"file": "PROJECT001C__014.DZT", "rank_in_profile": 2, "x_m": 0.40, "time_ns": 0.72, "relative_strength": 9},
        {"file": "PROJECT001C__015.DZT", "rank_in_profile": 1, "x_m": 0.10, "time_ns": 2.70, "relative_strength": 8},
        {"file": "PROJECT001C__015.DZT", "rank_in_profile": 2, "x_m": 0.80, "time_ns": 2.74, "relative_strength": 7},
    ]
    pairs = build_pair_spacing_rows(cue_rows, same_time_ns=0.15, duplicate_x_m=0.005)
    profiles = build_profile_context_rows(cue_rows, pairs)
    summary = summarize_spacing(
        profiles,
        pairs,
        same_time_ns=0.15,
        geometry={"classification": "independent_2d_line_profiles", "profile_count": 2},
        apparent_depth={"policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth"},
        field_policy={"policy_label": "field_2d_qc_not_3d_or_fwi"},
    )

    assert summary["policy_label"] == "field_cue_spacing_context_not_resolution_benchmark"
    assert summary["min_dataset_same_time_lateral_spacing_mm"] == 300.00000000000006
    assert summary["same_time_visible_cues_wider_than_synthetic_close_context"] is True
    assert summary["ready_for_resolution_benchmark"] is False
    assert summary["gpu_priority"] == "none"
