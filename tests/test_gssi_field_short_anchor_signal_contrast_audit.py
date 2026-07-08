import numpy as np

from run_gssi_field_short_anchor_signal_contrast_audit import (
    build_signal_contrast_rows,
    gate_rows,
    summarize_signal_contrast,
    window_contrast_metrics,
)


def _profile(event_time=0.5, event_value=10.0, noise_value=1.0):
    x_m = np.linspace(0.0, 0.04, 5)
    time_ns = np.linspace(0.0, 1.0, 101)
    corrected = np.full((time_ns.size, x_m.size), noise_value, dtype=float)
    event = (time_ns >= event_time - 0.04) & (time_ns <= event_time + 0.08)
    corrected[event, :] = event_value
    return corrected, x_m, time_ns


def _alignment_rows():
    return [
        {
            "pair_index": "2",
            "anchor_content_backed": "True",
            "reference_file": "reference.DZT",
            "comparison_file": "comparison.DZT",
            "reference_apex_group": "2",
            "comparison_apex_group": "2",
            "reference_x_m": "0.02",
            "comparison_aligned_x_m": "0.02",
            "reference_phase_time_ns": "0.50",
            "corrected_comparison_minus_reference_phase_time_ns": "0.00",
        }
    ]


def test_window_contrast_metrics_returns_rms_and_peak_ratios():
    corrected, x_m, time_ns = _profile()
    metrics = window_contrast_metrics(
        corrected,
        x_m,
        time_ns,
        center_x_m=0.02,
        event_time_ns=0.50,
        aperture_half_width_m=0.02,
        event_pre_ns=0.04,
        event_post_ns=0.08,
        noise_pre_start_ns=0.40,
        noise_pre_end_ns=0.20,
    )

    assert metrics["valid_window"] is True
    assert metrics["event_sample_count"] > 0
    assert metrics["noise_sample_count"] > 0
    assert metrics["event_to_noise_rms"] == 10.0
    assert metrics["event_to_noise_rms_db"] > 19.9
    assert metrics["peak_to_noise_p95"] == 10.0


def test_signal_contrast_rows_use_reference_and_aligned_comparison_windows():
    reference = _profile(event_value=12.0)
    comparison = _profile(event_value=9.0)
    processed = {
        "reference.DZT": {"corrected": reference[0]},
        "comparison.DZT": {"corrected": comparison[0]},
    }
    axes = {
        "reference.DZT": (reference[1], reference[2]),
        "comparison.DZT": (comparison[1], comparison[2]),
    }
    rows = build_signal_contrast_rows(
        _alignment_rows(),
        processed,
        axes,
        aperture_half_width_m=0.02,
        event_pre_ns=0.04,
        event_post_ns=0.08,
        noise_pre_start_ns=0.40,
        noise_pre_end_ns=0.20,
        min_event_to_noise_rms=3.0,
        min_peak_to_noise_p95=8.0,
    )
    by_side = {row["side"]: row for row in rows}

    assert len(rows) == 2
    assert by_side["reference"]["signal_contrast_supported"] is True
    assert by_side["comparison_aligned"]["signal_contrast_supported"] is True
    assert by_side["reference"]["ready_for_absolute_amplitude_calibration"] is False
    assert by_side["comparison_aligned"]["ready_for_field_fwi"] is False


def test_summary_keeps_signal_contrast_qc_separate_from_amplitude_calibration_and_fwi():
    reference = _profile(event_value=12.0)
    comparison = _profile(event_value=9.0)
    rows = build_signal_contrast_rows(
        _alignment_rows(),
        {
            "reference.DZT": {"corrected": reference[0]},
            "comparison.DZT": {"corrected": comparison[0]},
        },
        {
            "reference.DZT": (reference[1], reference[2]),
            "comparison.DZT": (comparison[1], comparison[2]),
        },
        aperture_half_width_m=0.02,
        event_pre_ns=0.04,
        event_post_ns=0.08,
        noise_pre_start_ns=0.40,
        noise_pre_end_ns=0.20,
        min_event_to_noise_rms=3.0,
        min_peak_to_noise_p95=8.0,
    )
    summary = summarize_signal_contrast(
        rows,
        {"policy_label": "alignment"},
        {"policy_label": "signed", "ready_for_signed_waveform_morphology_qc": True},
        {"policy_label": "timing", "ready_for_content_only_morphology_timing_qc": True},
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["side_window_count"] == 2
    assert summary["signal_contrast_supported_count"] == 2
    assert summary["ready_for_signal_contrast_qc"] is True
    assert summary["ready_for_signed_morphology_qc"] is True
    assert summary["ready_for_absolute_amplitude_calibration"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
    assert gates["signal_contrast_qc"]["ready"] is True
    assert gates["absolute_amplitude_calibration"]["ready"] is False
    assert gates["field_fwi"]["ready"] is False
