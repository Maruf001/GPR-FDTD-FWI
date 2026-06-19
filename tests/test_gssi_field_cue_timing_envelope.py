from run_gssi_field_cue_timing_envelope import build_anchor_rows, envelope_class, summarize


def _support(anchor_id: str, family: str, category: str, offset: float) -> dict:
    return {
        "support_anchor_id": anchor_id,
        "profile_group": "group",
        "support_family": family,
        "support_category": category,
        "support_label": "supported",
        "is_claim_supporting": "True",
        "anchor_x_mm": "100",
        "offset_ns": str(offset),
        "allowed_use": "allowed",
        "blocked_use": "blocked",
    }


def test_envelope_class_keeps_short_inside_and_long_transfer_rejected():
    assert envelope_class({"support_family": "short_relative_timing"}, 0.8) == (
        "short_anchor_inside_conservative_envelope"
    )
    assert envelope_class({"support_family": "short_relative_timing"}, 1.2) == (
        "short_anchor_outside_conservative_envelope"
    )
    assert envelope_class({"support_family": "long_pattern_only"}, 1.2) == (
        "long_pattern_rejects_short_transfer"
    )


def test_build_anchor_rows_adds_delta_half_widths_and_reference_rows():
    support_rows = [
        _support("short_1", "short_relative_timing", "short_content_backed_time_zero_anchor", 0.12),
        _support("long_1", "long_pattern_only", "long_stable_pattern_only_anchor", 0.06),
    ]
    timing_rows = [
        {
            "timing_discriminant": "early_common_mode",
            "representative_offset_ns": "0.0",
            "strength_label": "near_zero",
            "allowed_use": "early QC",
            "blocked_use": "absolute",
        },
        {
            "timing_discriminant": "long_pattern_only",
            "representative_offset_ns": "0.06",
            "strength_label": "long",
            "allowed_use": "long QC",
            "blocked_use": "short transfer",
        },
    ]
    time_zero = {"relative_anchor_offset_ns": 0.12, "conservative_half_width_ns": 0.05}

    rows = build_anchor_rows(support_rows, timing_rows, time_zero)
    by_id = {row["support_anchor_id"]: row for row in rows}

    assert by_id["short_1"]["delta_to_short_content_half_widths"] == 0
    assert by_id["short_1"]["timing_envelope_class"] == "short_anchor_inside_conservative_envelope"
    assert round(by_id["long_1"]["delta_to_short_content_half_widths"], 6) == 1.2
    assert by_id["long_1"]["timing_envelope_class"] == "long_pattern_rejects_short_transfer"
    assert "discriminant_early_common_mode" in by_id
    assert "discriminant_long_pattern_only" in by_id


def test_summary_blocks_absolute_time_zero_and_field_fwi():
    rows = [
        {
            "support_anchor_id": "short_1",
            "support_family": "short_relative_timing",
            "support_category": "short_content_backed_time_zero_anchor",
            "delta_to_short_content_half_widths": 0.0,
        },
        {
            "support_anchor_id": "long_1",
            "support_family": "long_pattern_only",
            "support_category": "long_stable_pattern_only_anchor",
            "delta_to_short_content_half_widths": 1.2,
        },
        {
            "support_anchor_id": "discriminant_early_common_mode",
            "support_family": "timing_discriminant_reference",
            "support_category": "early_common_mode",
            "delta_to_short_content_half_widths": 2.4,
        },
    ]
    summary = summarize(
        rows,
        {"relative_anchor_offset_ns": 0.12, "conservative_half_width_ns": 0.05},
        {"short_content_anchor_support_fraction": 2 / 3},
    )

    assert summary["short_anchor_inside_envelope_count"] == 1
    assert summary["short_content_anchor_inside_envelope_count"] == 1
    assert summary["long_pattern_reject_short_transfer_count"] == 1
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_long_short_transfer"] is False
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
