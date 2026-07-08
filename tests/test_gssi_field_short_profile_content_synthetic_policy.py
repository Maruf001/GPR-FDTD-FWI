from run_gssi_field_short_profile_content_synthetic_policy import (
    best_waveform_candidate,
    build_event_waveform_rows,
    summarize_policy,
)


def test_best_waveform_candidate_prefers_absolute_correlation_then_residual():
    rows = [
        {"file": "A.DZT", "apex_group": 2, "phase_convention": "top", "geometry_valid": "True", "skip_reason": "", "absolute_correlation": "0.82", "normalized_residual_rms": "0.4", "candidate_id": "low"},
        {"file": "A.DZT", "apex_group": 2, "phase_convention": "top", "geometry_valid": "True", "skip_reason": "", "absolute_correlation": "0.90", "normalized_residual_rms": "0.7", "candidate_id": "best"},
        {"file": "A.DZT", "apex_group": 2, "phase_convention": "cue", "geometry_valid": "True", "skip_reason": "", "absolute_correlation": "0.95", "normalized_residual_rms": "0.3", "candidate_id": "wrong_phase"},
    ]

    best = best_waveform_candidate(rows, file_name="A.DZT", apex_group=2, phase_convention="top")

    assert best["candidate_id"] == "best"


def test_build_event_waveform_rows_labels_content_backed_support():
    events = [
        {"pair_index": 1, "content_backed": "True", "content_label": "repeat_content_anchor", "reference_apex_group": 2, "comparison_apex_group": 3, "reference_x_mm": 400, "comparison_aligned_x_mm": 390, "timing_residual_to_bootstrap_median_ns": 0.01},
        {"pair_index": 2, "content_backed": "False", "content_label": "timing_only", "reference_apex_group": 1, "comparison_apex_group": 1, "reference_x_mm": 100, "comparison_aligned_x_mm": 120, "timing_residual_to_bootstrap_median_ns": 0.06},
    ]
    waveform = [
        {"file": "R.DZT", "apex_group": 2, "phase_convention": "top", "geometry_valid": "True", "skip_reason": "", "absolute_correlation": "0.88", "normalized_residual_rms": "0.5", "candidate_id": "r2"},
        {"file": "C.DZT", "apex_group": 3, "phase_convention": "top", "geometry_valid": "True", "skip_reason": "", "absolute_correlation": "0.83", "normalized_residual_rms": "0.6", "candidate_id": "c3"},
        {"file": "R.DZT", "apex_group": 1, "phase_convention": "top", "geometry_valid": "True", "skip_reason": "", "absolute_correlation": "0.86", "normalized_residual_rms": "0.5", "candidate_id": "r1"},
        {"file": "C.DZT", "apex_group": 1, "phase_convention": "top", "geometry_valid": "True", "skip_reason": "", "absolute_correlation": "0.84", "normalized_residual_rms": "0.6", "candidate_id": "c1"},
    ]

    rows = build_event_waveform_rows(
        events,
        waveform,
        reference_file="R.DZT",
        comparison_file="C.DZT",
        phase_convention="top",
        min_abs_correlation=0.8,
    )

    assert rows[0]["waveform_support_label"] == "content_backed_waveform_supported_qc"
    assert rows[1]["waveform_support_label"] == "timing_only_waveform_supported_limited"


def test_summarize_policy_requires_two_content_supported_pairs():
    rows = [
        {"content_backed": True, "waveform_support_label": "content_backed_waveform_supported_qc", "pair_min_absolute_correlation": 0.82},
        {"content_backed": True, "waveform_support_label": "content_backed_waveform_supported_qc", "pair_min_absolute_correlation": 0.83},
        {"content_backed": False, "waveform_support_label": "timing_only_waveform_supported_limited", "pair_min_absolute_correlation": 0.81},
    ]

    summary = summarize_policy(rows, min_abs_correlation=0.8, min_content_pairs=2)

    assert summary["policy_label"] == "content_backed_field_to_synthetic_qc_supported"
    assert summary["content_backed_waveform_supported_count"] == 2
    assert summary["timing_only_waveform_supported_count"] == 1
