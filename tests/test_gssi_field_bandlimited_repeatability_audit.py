import math

import numpy as np

from run_gssi_field_bandlimited_repeatability_audit import (
    audit_pair_bands,
    band_energy_fraction,
    bandpass_time_axis,
    parse_bands,
    summarize_band_audit,
)


def test_parse_bands_accepts_labels_and_limits():
    bands = parse_bands("0.4:1.0:low,1.0:2.0")

    assert bands[0] == {"band_label": "low", "low_ghz": 0.4, "high_ghz": 1.0}
    assert bands[1]["band_label"] == "1_2ghz"


def test_bandpass_time_axis_selects_requested_frequency():
    time_ns = np.linspace(0.0, 20.0, 401)
    low_signal = np.sin(2.0 * np.pi * 0.5 * time_ns)
    high_signal = 0.5 * np.sin(2.0 * np.pi * 2.0 * time_ns)
    matrix = (low_signal + high_signal).reshape(-1, 1)

    low_band = bandpass_time_axis(matrix, time_ns, 0.4, 0.7)
    high_band = bandpass_time_axis(matrix, time_ns, 1.8, 2.2)

    assert band_energy_fraction(low_band, matrix) > band_energy_fraction(high_band, matrix)
    assert np.nanmax(np.abs(low_band)) > np.nanmax(np.abs(high_band))


def test_audit_pair_bands_marks_improved_supported_band():
    time_ns = np.linspace(0.0, 20.0, 401)
    reference = np.sin(2.0 * np.pi * 0.8 * time_ns).reshape(-1, 1)
    raw = np.roll(reference, 10, axis=0)
    corrected = reference.copy()
    windows = {
        "time_ns": time_ns,
        "reference_window": reference,
        "raw_aligned_comparison": raw,
        "corrected_aligned_comparison": corrected,
    }

    rows = audit_pair_bands(
        pair_label="short_014_016",
        claim_scope="relative_time_zero_qc",
        windows=windows,
        bands=[{"band_label": "signal", "low_ghz": 0.7, "high_ghz": 0.9}],
    )
    signal = next(row for row in rows if row["band_label"] == "signal")

    assert signal["supported_band"]
    assert signal["corrected_abs_correlation"] > 0.99
    assert signal["abs_correlation_gain"] > 0.02


def test_summarize_band_audit_keeps_long_pattern_only_scope():
    rows = [
        {
            "pair_label": "short_014_016",
            "band_label": "unfiltered",
            "raw_abs_correlation": 0.5,
            "corrected_abs_correlation": 0.8,
            "abs_correlation_gain": 0.3,
            "supported_band": True,
        },
        *[
            {
                "pair_label": "short_014_016",
                "band_label": label,
                "raw_abs_correlation": 0.5,
                "corrected_abs_correlation": 0.8,
                "abs_correlation_gain": 0.3,
                "supported_band": True,
            }
            for label in ["low", "mid", "broad"]
        ],
        {
            "pair_label": "long_015_013",
            "band_label": "unfiltered",
            "raw_abs_correlation": 0.7,
            "corrected_abs_correlation": 0.9,
            "abs_correlation_gain": 0.2,
            "supported_band": True,
        },
        {
            "pair_label": "long_015_013",
            "band_label": "broad",
            "raw_abs_correlation": 0.7,
            "corrected_abs_correlation": 0.9,
            "abs_correlation_gain": 0.2,
            "supported_band": True,
        },
    ]

    summary = summarize_band_audit(rows)

    assert summary["policy_label"] == "field_bandlimited_repeatability_short_pair_supported_long_pattern_only"
    assert summary["short_supported_band_count"] == 3
    assert summary["long_pattern_supported_band_count"] == 1
    assert summary["field_gpu_fwi_priority"] == "none"
    assert "pattern-only" in summary["decision"]
