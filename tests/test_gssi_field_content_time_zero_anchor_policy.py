from run_gssi_field_content_time_zero_anchor_policy import (
    build_anchor_rows,
    summarize_anchor_policy,
)


def _event(pair, *, content, residual):
    return {
        "pair_index": str(pair),
        "content_backed": str(content),
        "content_label": "repeat_content_anchor" if content else "timing_only_no_stable_content_anchor",
        "reference_apex_group": str(pair),
        "comparison_apex_group": str(pair),
        "reference_x_mm": "400.0",
        "comparison_aligned_x_mm": "395.0",
        "aligned_x_residual_mm": "-5.0",
        "nearest_anchor_distance_mm": "8.0" if content else "260.0",
        "timing_residual_to_bootstrap_median_ns": str(residual),
        "within_bootstrap_ci_envelope": str(content),
    }


def _match(pair, corr):
    return {
        "pair_index": str(pair),
        "pair_min_absolute_correlation": str(corr),
        "pair_mean_absolute_correlation": str(corr + 0.02),
        "waveform_support_label": "content_backed_waveform_supported_qc",
    }


def _panels(pair, corr=0.84, residual=0.58, shift=0.2):
    return [
        {
            "pair_index": str(pair),
            "simulation_valid": "True",
            "absolute_correlation": str(corr),
            "normalized_residual_rms": str(residual),
            "synthetic_time_shift_ns": str(shift),
        },
        {
            "pair_index": str(pair),
            "simulation_valid": "True",
            "absolute_correlation": str(corr + 0.03),
            "normalized_residual_rms": str(residual - 0.05),
            "synthetic_time_shift_ns": str(shift),
        },
    ]


def test_build_anchor_rows_excludes_timing_only_pair_from_content_support():
    rows = build_anchor_rows(
        [_event(1, content=False, residual=0.06), _event(2, content=True, residual=0.01)],
        [_match(1, 0.83), _match(2, 0.82)],
        _panels(2),
        max_abs_content_residual_ns=0.02,
        min_abs_correlation=0.8,
        max_shift_span_ns=0.05,
    )

    assert rows[0]["anchor_policy_label"] == "timing_only_no_content_anchor"
    assert rows[1]["anchor_policy_label"] == "content_time_zero_anchor_supported"
    assert rows[1]["valid_panel_count"] == 2


def test_summarize_anchor_policy_supported_for_two_content_pairs():
    rows = build_anchor_rows(
        [_event(2, content=True, residual=-0.01), _event(3, content=True, residual=0.01)],
        [_match(2, 0.82), _match(3, 0.84)],
        _panels(2, corr=0.82) + _panels(3, corr=0.84),
        max_abs_content_residual_ns=0.02,
        min_abs_correlation=0.8,
        max_shift_span_ns=0.05,
    )

    summary = summarize_anchor_policy(
        rows,
        max_abs_content_residual_ns=0.02,
        min_abs_correlation=0.8,
        max_shift_span_ns=0.05,
        min_supported_content_pairs=2,
    )

    assert summary["policy_label"] == "short_profile_content_time_zero_anchor_supported_for_visual_qc"
    assert summary["supported_content_anchor_pair_count"] == 2
    assert summary["max_abs_content_timing_residual_ns"] == 0.01
    assert summary["min_content_pair_absolute_correlation"] == 0.82


def test_summarize_anchor_policy_limited_when_content_residual_is_large():
    rows = build_anchor_rows(
        [_event(2, content=True, residual=0.05), _event(3, content=True, residual=0.01)],
        [_match(2, 0.82), _match(3, 0.84)],
        _panels(2, corr=0.82) + _panels(3, corr=0.84),
        max_abs_content_residual_ns=0.02,
        min_abs_correlation=0.8,
        max_shift_span_ns=0.05,
    )

    summary = summarize_anchor_policy(
        rows,
        max_abs_content_residual_ns=0.02,
        min_abs_correlation=0.8,
        max_shift_span_ns=0.05,
        min_supported_content_pairs=2,
    )

    assert summary["policy_label"] == "short_profile_content_time_zero_anchor_limited"
    assert summary["supported_content_anchor_pair_count"] == 1
