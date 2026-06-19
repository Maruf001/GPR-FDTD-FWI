from run_gssi_field_short_anchor_spatial_consistency_audit import (
    short_anchor_rows,
    summarize_spatial_consistency,
)


def test_short_anchor_rows_join_interval_support():
    support_rows = [
        {
            "support_anchor_id": "short_pair_2",
            "support_family": "short_relative_timing",
            "support_category": "short_content_backed_time_zero_anchor",
            "support_label": "content",
            "is_claim_supporting": "True",
            "anchor_x_mm": "403.293",
            "comparison_aligned_x_mm": "393.294",
            "aligned_x_residual_mm": "-9.999",
            "offset_ns": "0.108055",
            "quality_metric_value": "0.819",
        },
        {
            "support_anchor_id": "long_anchor_1",
            "support_family": "long_pattern_only",
        },
    ]
    interval_rows = [
        {
            "support_anchor_id": "short_pair_2",
            "inside_all_window_supported_interval": "True",
            "margin_to_supported_interval_edge_mm": "13.332",
        }
    ]

    rows = short_anchor_rows(support_rows, interval_rows)

    assert len(rows) == 1
    assert rows[0]["support_anchor_id"] == "short_pair_2"
    assert rows[0]["is_claim_supporting"] is True
    assert rows[0]["inside_all_window_supported_interval"] is True
    assert rows[0]["residual_sign"] == "negative"


def test_summary_blocks_spatial_calibration_when_content_residuals_disagree():
    rows = [
        {
            "support_anchor_id": "short_pair_1",
            "support_category": "short_timing_only_limited_cue",
            "is_claim_supporting": False,
            "aligned_x_residual_mm": -9.999,
            "offset_ns": 0.1768,
            "inside_all_window_supported_interval": True,
            "margin_to_supported_interval_edge_mm": 26.664,
        },
        {
            "support_anchor_id": "short_pair_2",
            "support_category": "short_content_backed_time_zero_anchor",
            "is_claim_supporting": True,
            "aligned_x_residual_mm": -9.999,
            "offset_ns": 0.108055,
            "inside_all_window_supported_interval": True,
            "margin_to_supported_interval_edge_mm": 13.332,
        },
        {
            "support_anchor_id": "short_pair_3",
            "support_category": "short_content_backed_time_zero_anchor",
            "is_claim_supporting": True,
            "aligned_x_residual_mm": 19.998,
            "offset_ns": 0.127701,
            "inside_all_window_supported_interval": True,
            "margin_to_supported_interval_edge_mm": 19.998,
        },
    ]

    summary = summarize_spatial_consistency(
        rows,
        {"ready_for_short_relative_timing_qc": True},
        {"ready_for_short_relative_timing_qc": True},
    )

    assert summary["short_anchor_count"] == 3
    assert summary["content_anchor_count"] == 2
    assert summary["content_anchor_inside_supported_interval_count"] == 2
    assert summary["content_residual_range_mm"] == 29.997
    assert summary["content_residual_sign_consistent"] is False
    assert summary["content_single_translation_inside_margin"] is False
    assert summary["content_single_translation_supported"] is False
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_profile_spatial_calibration"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
