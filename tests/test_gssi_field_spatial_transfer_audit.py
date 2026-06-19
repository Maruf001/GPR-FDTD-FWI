from run_gssi_field_spatial_transfer_audit import (
    build_spatial_transfer_rows,
    nearest_anchor,
    summarize,
)


def _anchor(anchor_id, family, category, x_mm, offset_ns=0.1, delta_half_widths=0.0):
    return {
        "support_anchor_id": anchor_id,
        "support_family": family,
        "support_category": category,
        "anchor_x_mm": x_mm,
        "offset_ns": offset_ns,
        "delta_to_short_content_half_widths": delta_half_widths,
        "timing_envelope_class": "short_anchor_inside_conservative_envelope"
        if family == "short_relative_timing"
        else "long_pattern_rejects_short_transfer",
        "transfer_scope": "short_relative_timing_qc"
        if family == "short_relative_timing"
        else "long_pattern_only_no_short_transfer",
    }


def test_nearest_anchor_returns_distance_in_mm():
    source = _anchor("short_1", "short_relative_timing", "short_content_backed_time_zero_anchor", 100)
    candidates = [
        _anchor("long_1", "long_pattern_only", "long_stable_pattern_only_anchor", 240),
        _anchor("long_2", "long_pattern_only", "long_stable_pattern_only_anchor", 130),
    ]

    nearest, distance = nearest_anchor(source, candidates)

    assert nearest["support_anchor_id"] == "long_2"
    assert distance == 30


def test_build_spatial_transfer_rows_is_bidirectional_and_thresholded():
    rows = [
        _anchor("short_1", "short_relative_timing", "short_content_backed_time_zero_anchor", 100),
        _anchor("short_2", "short_relative_timing", "short_content_backed_time_zero_anchor", 500),
        _anchor("long_1", "long_pattern_only", "long_stable_pattern_only_anchor", 130),
        _anchor("long_2", "long_pattern_only", "long_stable_pattern_only_anchor", 900),
    ]

    transfer_rows = build_spatial_transfer_rows(rows, spatial_match_threshold_mm=100)

    assert len(transfer_rows) == 4
    assert sum(row["transfer_direction"] == "short_content_to_nearest_long_pattern" for row in transfer_rows) == 2
    assert sum(row["transfer_direction"] == "long_pattern_to_nearest_short_content" for row in transfer_rows) == 2
    assert sum(row["within_spatial_threshold"] for row in transfer_rows) == 2


def test_summary_blocks_short_to_long_transfer_when_long_coverage_is_sparse():
    rows = [
        _anchor("short_1", "short_relative_timing", "short_content_backed_time_zero_anchor", 100),
        _anchor("short_2", "short_relative_timing", "short_content_backed_time_zero_anchor", 500),
        _anchor("long_1", "long_pattern_only", "long_stable_pattern_only_anchor", 130),
        _anchor("long_2", "long_pattern_only", "long_stable_pattern_only_anchor", 900),
    ]
    transfer_rows = build_spatial_transfer_rows(rows, spatial_match_threshold_mm=100)

    summary = summarize(
        transfer_rows,
        {"ready_for_long_short_transfer": False},
        spatial_match_threshold_mm=100,
    )

    assert summary["short_content_anchor_count"] == 2
    assert summary["long_pattern_anchor_count"] == 2
    assert summary["short_content_with_nearest_long_within_threshold_count"] == 1
    assert summary["long_pattern_with_nearest_short_content_within_threshold_count"] == 1
    assert summary["ready_for_short_to_long_timing_transfer"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["gpu_priority"] == "none"
