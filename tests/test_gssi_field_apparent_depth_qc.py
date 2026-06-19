import math

from run_gssi_field_apparent_depth_qc import (
    profile_cue_rows,
    short_pair_depth_rows,
    summarize_depth_qc,
    two_way_depth_mm,
)


def test_two_way_depth_mm_uses_nominal_dielectric():
    depth = two_way_depth_mm(0.1, 2.25)

    assert math.isclose(depth, 9.993081933333334)


def test_profile_cue_rows_groups_short_and_long_profiles():
    rows = profile_cue_rows([
        {
            "file": "PROJECT001C__014.DZT",
            "time_ns": "0.7",
            "x_m": "0.1",
            "approx_depth_m": "0.07",
            "relative_strength": "3.0",
        },
        {
            "file": "PROJECT001C__014.DZT",
            "time_ns": "0.8",
            "x_m": "0.2",
            "approx_depth_m": "0.08",
            "relative_strength": "4.0",
        },
        {
            "file": "PROJECT001C__013.DZT",
            "time_ns": "2.7",
            "x_m": "1.0",
            "approx_depth_m": "0.27",
            "relative_strength": "5.0",
        },
    ])
    by_file = {row["file"]: row for row in rows}

    assert by_file["PROJECT001C__014.DZT"]["profile_group"] == "short_014_016"
    assert by_file["PROJECT001C__014.DZT"]["cue_count"] == 2
    assert by_file["PROJECT001C__014.DZT"]["median_apparent_depth_mm"] == 75.0
    assert by_file["PROJECT001C__013.DZT"]["profile_group"] == "long_013_015"


def test_short_pair_depth_rows_marks_budget_support_and_content_status():
    applied_rows = [
        {
            "pair_index": "1",
            "reference_apex_group": "1",
            "comparison_apex_group": "1",
            "reference_x_m": "0.1",
            "comparison_aligned_x_m": "0.11",
            "aligned_x_residual_mm": "10",
            "reference_phase_time_ns": "0.50",
            "comparison_phase_time_ns": "0.63",
            "applied_transfer_offset_ns": "0.13",
            "abs_raw_phase_residual_ns": "0.13",
            "abs_corrected_phase_residual_ns": "0.0",
        },
        {
            "pair_index": "2",
            "reference_apex_group": "2",
            "comparison_apex_group": "2",
            "reference_x_m": "0.2",
            "comparison_aligned_x_m": "0.2",
            "aligned_x_residual_mm": "0",
            "reference_phase_time_ns": "0.50",
            "comparison_phase_time_ns": "0.70",
            "applied_transfer_offset_ns": "0.13",
            "abs_raw_phase_residual_ns": "0.20",
            "abs_corrected_phase_residual_ns": "0.07",
        },
    ]
    content_rows = [
        {"pair_index": "1", "content_backed": "True", "pair_min_absolute_correlation": "0.9"},
        {"pair_index": "2", "content_backed": "False", "pair_min_absolute_correlation": "0.8"},
    ]
    rows = short_pair_depth_rows(applied_rows, content_rows, 2.25, conservative_depth_equivalent_mm=5.0)
    by_pair = {row["pair_index"]: row for row in rows}

    assert by_pair[1]["content_backed"] is True
    assert by_pair[1]["within_conservative_depth_equivalent"] is True
    assert by_pair[1]["claim_status"] == "content_backed_relative_depth_scale_qc"
    assert by_pair[2]["within_conservative_depth_equivalent"] is False
    assert by_pair[2]["claim_status"] == "outside_relative_depth_uncertainty"


def test_summary_keeps_depth_scale_separate_from_cover_depth():
    profile_rows = profile_cue_rows([
        {
            "file": "PROJECT001C__014.DZT",
            "time_ns": "0.7",
            "x_m": "0.1",
            "approx_depth_m": "0.07",
            "relative_strength": "3.0",
        },
        {
            "file": "PROJECT001C__013.DZT",
            "time_ns": "2.7",
            "x_m": "1.0",
            "approx_depth_m": "0.27",
            "relative_strength": "5.0",
        },
    ])
    pair_rows = [
        {
            "content_backed": True,
            "raw_depth_residual_mm": 10.0,
            "corrected_depth_residual_mm": 2.0,
            "within_conservative_depth_equivalent": True,
        },
        {
            "content_backed": False,
            "raw_depth_residual_mm": 8.0,
            "corrected_depth_residual_mm": 3.0,
            "within_conservative_depth_equivalent": True,
        },
    ]
    summary = summarize_depth_qc(
        profile_rows,
        pair_rows,
        2.25,
        {"conservative_half_width_ns": 0.05},
        {"time_zero_two_way_depth_equivalent_mm": 5.0},
    )

    assert summary["policy_label"] == "field_apparent_depth_qc_relative_scale_not_cover_depth"
    assert summary["cue_count"] == 2
    assert summary["short_pair_corrected_depth_support_count"] == 2
    assert summary["ready_for_apparent_depth_scale_qc"] is True
    assert summary["ready_for_cover_depth_recovery"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
