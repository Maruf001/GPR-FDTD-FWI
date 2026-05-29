"""Tests for spectrum diagnostics."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.spectrum_analysis import (  # noqa: E402
    average_amplitude_spectrum,
    band_energy_fraction,
    spectral_energy_band,
)


def test_average_amplitude_spectrum_detects_sine_peak():
    dt = 0.001
    time = np.arange(0.0, 2.0, dt)
    trace = np.sin(2.0 * np.pi * 8.0 * time)

    freqs, amplitude = average_amplitude_spectrum(trace, dt)

    peak_hz = freqs[int(np.argmax(amplitude))]
    assert abs(peak_hz - 8.0) < 0.25


def test_spectral_energy_band_returns_peak_and_band():
    dt = 0.001
    time = np.arange(0.0, 2.0, dt)
    trace = np.sin(2.0 * np.pi * 8.0 * time)
    freqs, amplitude = average_amplitude_spectrum(trace, dt)

    band = spectral_energy_band(freqs, amplitude, low_fraction=0.01, high_fraction=0.99)

    assert abs(band["peak_hz"] - 8.0) < 0.25
    assert band["low_hz"] <= band["peak_hz"] <= band["high_hz"]
    assert band["total_energy"] > 0.0


def test_band_energy_fraction_handles_zero_spectrum():
    freqs = np.array([0.0, 1.0, 2.0])
    amplitude = np.zeros_like(freqs)

    assert band_energy_fraction(freqs, amplitude, low_hz=0.5, high_hz=1.5) == 0.0
