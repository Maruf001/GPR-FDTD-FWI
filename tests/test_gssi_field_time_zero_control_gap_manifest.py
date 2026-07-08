from run_gssi_field_time_zero_control_gap_manifest import gate_rows, summarize_gap


def _timing_row(source, support_fraction, status, absolute=False):
    return {
        "timing_source": source,
        "source_run": "test",
        "support_count": 1,
        "row_count": 1,
        "support_fraction": support_fraction,
        "representative_offset_ns": 0.0,
        "strength_metric": 1.0,
        "status": status,
        "absolute_time_zero_candidate": absolute,
        "allowed_use": "test allowed",
        "blocked_use": "test blocked",
        "evidence": "test evidence",
        "source_path": "test.json",
    }


def test_gap_blocks_absolute_time_zero_despite_relative_support():
    timing_rows = [
        _timing_row("early_common_mode", 1.0, "negative_control_common_mode"),
        _timing_row("short_content_relative", 1.0, "relative_timing_supported_not_absolute"),
        _timing_row("absolute_time_zero_control", 0.0, "must_have_control_unsatisfied"),
    ]
    summary = summarize_gap(
        timing_rows,
        {
            "short_pair_early_shift_ns": 0.0,
            "short_pair_conservative_half_width_ns": 0.058,
        },
        {"short_nominal_offset_ns": 0.128},
        {
            "satisfied_must_have_requirement_count": 0,
            "must_have_requirement_count": 5,
        },
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["relative_short_timing_supported"] is True
    assert summary["early_common_mode_negative_control"] is True
    assert summary["short_vs_early_exceeds_conservative_half_width"] is True
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert gates["absolute_time_zero_from_current_archive"]["ready"] is False
    assert gates["new_absolute_timing_reference"]["ready"] is True


def test_gap_counts_any_candidate_without_promoting_current_archive():
    timing_rows = [
        _timing_row("candidate", 1.0, "external_reference", absolute=True),
    ]
    summary = summarize_gap(
        timing_rows,
        {"short_pair_early_shift_ns": 0.0, "short_pair_conservative_half_width_ns": 0.1},
        {"short_nominal_offset_ns": 0.02},
        {"satisfied_must_have_requirement_count": 1, "must_have_requirement_count": 5},
    )

    assert summary["absolute_time_zero_candidate_count"] == 1
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["gpu_priority"] == "none"
