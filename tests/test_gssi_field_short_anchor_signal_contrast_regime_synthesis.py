from run_gssi_field_short_anchor_signal_contrast_regime_synthesis import (
    build_regime_rows,
    gate_rows,
    summarize_regimes,
)


def _combo_rows():
    rows = []
    for event in ["tight", "default", "broad"]:
        for noise in ["near", "default", "far"]:
            supported = event == "broad"
            rows.append(
                {
                    "combo_key": f"a20mm_{event}_{noise}",
                    "aperture_half_width_m": "0.02",
                    "event_window_label": event,
                    "noise_window_label": noise,
                    "all_side_windows_supported": supported,
                    "min_event_to_noise_rms": 5.0 if supported else 1.2,
                    "min_peak_to_noise_p95": 12.0 if supported else 2.0,
                }
            )
    return rows


def test_regime_rows_identify_broad_event_window():
    event_rows, aperture_rows, noise_rows = build_regime_rows(_combo_rows())
    event_lookup = {row["group_key"]: row for row in event_rows}

    assert event_lookup["broad"]["all_combos_supported"] is True
    assert event_lookup["broad"]["all_supported_combo_count"] == 3
    assert event_lookup["tight"]["all_combos_supported"] is False
    assert aperture_rows[0]["all_supported_combo_count"] == 3
    assert len(noise_rows) == 3


def test_regime_summary_keeps_field_fwi_blocked():
    combo_rows = _combo_rows()
    event_rows, _, _ = build_regime_rows(combo_rows)
    summary = summarize_regimes(
        combo_rows,
        {"policy_label": "sensitivity", "ready_for_default_signal_contrast_qc": True},
        event_rows,
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["ready_for_broad_event_signal_contrast_regime"] is True
    assert summary["ready_for_default_signal_contrast_qc"] is True
    assert summary["ready_for_strict_window_invariant_signal_contrast_claim"] is False
    assert summary["ready_for_absolute_amplitude_calibration"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["gpu_priority"] == "none"
    assert gates["broad_event_signal_contrast_regime"]["ready"] is True
    assert gates["field_fwi_or_3d_hpc"]["ready"] is False
