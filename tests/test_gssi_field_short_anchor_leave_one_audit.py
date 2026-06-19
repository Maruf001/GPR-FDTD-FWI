from run_gssi_field_short_anchor_leave_one_audit import (
    build_leave_one_rows,
    short_support_anchors,
    summarize_leave_one,
)


def _support_rows():
    return [
        {
            "support_anchor_id": "short_pair_1",
            "support_family": "short_relative_timing",
            "support_category": "short_timing_only_limited_cue",
            "is_claim_supporting": "False",
            "anchor_x_mm": "129.987",
            "offset_ns": "0.17681728880157166",
            "quality_metric_value": "0.8103354845949436",
        },
        {
            "support_anchor_id": "short_pair_2",
            "support_family": "short_relative_timing",
            "support_category": "short_content_backed_time_zero_anchor",
            "is_claim_supporting": "True",
            "anchor_x_mm": "403.293",
            "offset_ns": "0.10805500982318272",
            "quality_metric_value": "0.8194940543205603",
        },
        {
            "support_anchor_id": "short_pair_3",
            "support_family": "short_relative_timing",
            "support_category": "short_content_backed_time_zero_anchor",
            "is_claim_supporting": "True",
            "anchor_x_mm": "693.264",
            "offset_ns": "0.12770137524557956",
            "quality_metric_value": "0.8339957215615591",
        },
    ]


def _interval_rows():
    return [
        {
            "support_anchor_id": "short_pair_1",
            "inside_all_window_supported_interval": "True",
            "margin_to_supported_interval_edge_mm": "26.664",
        },
        {
            "support_anchor_id": "short_pair_2",
            "inside_all_window_supported_interval": "True",
            "margin_to_supported_interval_edge_mm": "13.332",
        },
        {
            "support_anchor_id": "short_pair_3",
            "inside_all_window_supported_interval": "True",
            "margin_to_supported_interval_edge_mm": "19.998",
        },
    ]


def test_short_support_anchors_join_catalog_to_interval_evidence():
    anchors = short_support_anchors(_support_rows(), _interval_rows())

    assert [row["support_anchor_id"] for row in anchors] == [
        "short_pair_1",
        "short_pair_2",
        "short_pair_3",
    ]
    assert sum(row["is_content_backed"] for row in anchors) == 2
    assert all(row["inside_supported_interval"] for row in anchors)
    assert anchors[1]["margin_to_supported_interval_edge_mm"] == 13.332


def test_leave_one_rows_show_content_only_support_but_not_full_content_redundancy():
    anchors = short_support_anchors(_support_rows(), _interval_rows())
    rows = build_leave_one_rows(
        anchors,
        nominal_offset_ns=0.12770137524557956,
        conservative_half_width_ns=0.058939096267190516,
    )
    by_key = {row["case_key"]: row for row in rows}

    assert len(rows) == 5
    assert by_key["content_backed_only"]["short_relative_timing_supported"] is True
    assert by_key["content_backed_only"]["content_anchor_count"] == 2
    assert by_key["leave_out_short_pair_1"]["short_relative_timing_supported"] is True
    assert by_key["leave_out_short_pair_2"]["status"] == "degraded_single_content_anchor"
    assert by_key["leave_out_short_pair_3"]["status"] == "degraded_single_content_anchor"
    assert by_key["content_backed_only"]["offset_half_range_ns"] < by_key["all_short_anchors"]["offset_half_range_ns"]


def test_leave_one_summary_keeps_field_claim_short_qc_only():
    anchors = short_support_anchors(_support_rows(), _interval_rows())
    rows = build_leave_one_rows(
        anchors,
        nominal_offset_ns=0.12770137524557956,
        conservative_half_width_ns=0.058939096267190516,
    )

    summary = summarize_leave_one(rows, anchors)

    assert summary["policy_label"] == "gssi51600s_field_short_anchor_leave_one_content_redundancy_qc_only"
    assert summary["short_anchor_count"] == 3
    assert summary["short_content_anchor_count"] == 2
    assert summary["content_only_supported"] is True
    assert summary["leave_one_supported_count"] == 1
    assert summary["leave_one_degraded_single_content_count"] == 2
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_leave_one_content_anchor_claim"] is False
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
