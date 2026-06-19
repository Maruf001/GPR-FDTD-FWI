from run_gssi_field_anchor_interval_reconciliation import (
    build_reconciliation_rows,
    interval_contains_x,
    nearest_interval,
    summarize,
)


def _anchor(anchor_id, x_mm, category="short_content_backed_time_zero_anchor"):
    return {
        "support_anchor_id": anchor_id,
        "support_family": "short_relative_timing",
        "support_category": category,
        "support_label": "supported",
        "is_claim_supporting": str(category == "short_content_backed_time_zero_anchor"),
        "anchor_x_mm": x_mm,
        "delta_to_short_content_half_widths": 0.2,
        "timing_envelope_class": "short_anchor_inside_conservative_envelope",
        "allowed_use": "short QC",
        "blocked_use": "field FWI",
    }


def _interval(index, start_mm, end_mm):
    return {
        "support_key": "all_window_supported",
        "selected_interval_index": index,
        "start_x_mm": start_mm,
        "end_x_mm": end_mm,
        "interval_abs_correlation_improvement": 0.4,
        "corrected_interval_abs_correlation": 0.91,
    }


def test_interval_contains_x_is_inclusive():
    interval = _interval(1, 100, 150)

    assert interval_contains_x(interval, 100)
    assert interval_contains_x(interval, 125)
    assert interval_contains_x(interval, 150)
    assert not interval_contains_x(interval, 151)


def test_nearest_interval_returns_zero_distance_when_inside():
    intervals = [_interval(1, 100, 150), _interval(2, 300, 350)]

    matched, distance = nearest_interval(intervals, 125)

    assert matched["selected_interval_index"] == 1
    assert distance == 0.0


def test_build_reconciliation_rows_matches_supported_intervals():
    timing_rows = [
        _anchor("short_1", 125, "short_timing_only_limited_cue"),
        _anchor("short_2", 325),
    ]
    interval_rows = [_interval(1, 100, 150), _interval(2, 300, 350)]

    rows = build_reconciliation_rows(timing_rows, interval_rows)

    assert len(rows) == 2
    assert all(row["inside_all_window_supported_interval"] for row in rows)
    assert rows[0]["matched_interval_index"] == 1
    assert rows[1]["matched_interval_index"] == 2
    assert rows[0]["margin_to_supported_interval_edge_mm"] == 25


def test_summary_marks_short_qc_ready_but_keeps_inversion_blocked():
    rows = build_reconciliation_rows(
        [
            _anchor("short_1", 125, "short_timing_only_limited_cue"),
            _anchor("short_2", 325),
            _anchor("short_3", 525),
        ],
        [_interval(1, 100, 150), _interval(2, 300, 350), _interval(3, 500, 550)],
    )

    summary = summarize(
        rows,
        {"ready_for_short_relative_timing_qc": True},
        {"policy_label": "supported_interval_visual_qc_ready"},
    )

    assert summary["short_anchor_inside_supported_interval_count"] == 3
    assert summary["short_content_anchor_inside_supported_interval_count"] == 2
    assert summary["short_timing_only_anchor_inside_supported_interval_count"] == 1
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["gpu_priority"] == "none"
