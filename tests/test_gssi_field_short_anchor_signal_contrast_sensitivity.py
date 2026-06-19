from run_gssi_field_short_anchor_signal_contrast_sensitivity import (
    gate_rows,
    parse_float_list,
    parse_window_specs,
    summarize_sensitivity,
)


def _combo_rows():
    return [
        {
            "combo_key": "a20mm_default_default",
            "aperture_half_width_m": 0.020,
            "event_window_label": "default",
            "noise_window_label": "default",
            "side_window_count": 4,
            "supported_side_window_count": 4,
            "all_side_windows_supported": True,
            "min_event_to_noise_rms": 4.1,
            "min_peak_to_noise_p95": 12.4,
        },
        {
            "combo_key": "a10mm_tight_near",
            "aperture_half_width_m": 0.010,
            "event_window_label": "tight",
            "noise_window_label": "near",
            "side_window_count": 4,
            "supported_side_window_count": 2,
            "all_side_windows_supported": False,
            "min_event_to_noise_rms": 1.05,
            "min_peak_to_noise_p95": 1.44,
        },
    ]


def test_parse_float_list_and_window_specs():
    assert parse_float_list("0.01,0.02") == [0.01, 0.02]
    assert parse_window_specs("tight:0.05:0.12,default:0.08:0.18") == [
        {"label": "tight", "start": 0.05, "end": 0.12},
        {"label": "default", "start": 0.08, "end": 0.18},
    ]


def test_summary_keeps_default_qc_but_blocks_window_invariant_claim():
    summary = summarize_sensitivity(_combo_rows(), {"policy_label": "baseline"})
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["sensitivity_combo_count"] == 2
    assert summary["all_supported_combo_count"] == 1
    assert summary["default_combo_all_supported"] is True
    assert summary["default_combo_min_event_to_noise_rms"] == 4.1
    assert summary["worst_rms_combo_key"] == "a10mm_tight_near"
    assert summary["ready_for_default_signal_contrast_qc"] is True
    assert summary["ready_for_window_invariant_signal_contrast_claim"] is False
    assert summary["ready_for_absolute_amplitude_calibration"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
    assert gates["default_signal_contrast_qc"]["ready"] is True
    assert gates["window_invariant_signal_contrast_claim"]["ready"] is False
    assert gates["field_fwi"]["ready"] is False
