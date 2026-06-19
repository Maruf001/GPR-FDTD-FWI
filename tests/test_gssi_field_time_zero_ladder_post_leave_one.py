from run_gssi_field_time_zero_ladder_post_leave_one import (
    build_post_leave_one_rows,
    summarize_post_leave_one,
)


def test_post_leave_one_rows_append_content_only_gate():
    base_rows = [
        {
            "gate_key": "short_relative_timing_budget",
            "status": "supported",
            "readiness_score": 0.95,
            "evidence": "offset=0.127701 ns",
            "allowed_use": "short QC",
            "blocked_use": "absolute time-zero",
        }
    ]
    leave_one = {
        "content_only_supported": True,
        "ready_for_leave_one_content_anchor_claim": False,
        "content_only_offset_half_range_ns": 0.00982318271119842,
        "all_short_offset_half_range_ns": 0.03438113948919447,
        "leave_one_supported_count": 1,
        "leave_one_case_count": 3,
        "leave_one_degraded_single_content_count": 2,
    }

    rows = build_post_leave_one_rows(base_rows, leave_one)

    assert len(rows) == 2
    assert rows[-1]["gate_key"] == "short_anchor_content_only_redundancy"
    assert rows[-1]["status"] == "supported_content_only_not_leave_one_content"
    assert rows[-1]["readiness_score"] == 0.88
    assert "content_half_range=0.009823 ns" in rows[-1]["evidence"]


def test_post_leave_one_summary_keeps_field_ladder_qc_only():
    rows = [
        {"gate_key": "short_relative_timing_budget"},
        {"gate_key": "short_anchor_content_only_redundancy"},
    ]
    base_summary = {
        "policy_label": "base_ladder",
        "ready_for_short_relative_timing_qc": True,
        "short_relative_offset_ns": 0.12770137524557956,
        "short_conservative_half_width_ns": 0.058939096267190516,
        "short_anchor_inside_supported_interval_count": 3,
        "long_pattern_reject_short_transfer_count": 8,
        "median_long_to_short_distance_mm": 701.5965,
    }
    leave_one = {
        "policy_label": "leave_one",
        "content_only_supported": True,
        "ready_for_leave_one_content_anchor_claim": False,
        "content_only_offset_half_range_ns": 0.00982318271119842,
        "all_short_offset_half_range_ns": 0.03438113948919447,
        "leave_one_supported_count": 1,
        "leave_one_degraded_single_content_count": 2,
    }

    summary = summarize_post_leave_one(rows, base_summary, leave_one)

    assert summary["policy_label"] == "gssi51600s_field_time_zero_evidence_ladder_post_leave_one_short_qc_only"
    assert summary["ladder_row_count"] == 2
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_content_only_short_qc"] is True
    assert summary["ready_for_leave_one_content_anchor_claim"] is False
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["content_only_offset_half_range_ns"] == 0.00982318271119842
    assert summary["gpu_priority"] == "none"
