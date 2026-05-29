"""Spectrum helpers for GPR trace and residual diagnostics."""
import numpy as np


def average_amplitude_spectrum(traces, dt, window=None):
    """Return frequency bins and mean single-sided amplitude spectrum."""
    data = np.asarray(traces, dtype=np.float64)
    if data.ndim == 1:
        data = data[:, None]
    if data.ndim != 2:
        raise ValueError("traces must be a 1D trace or 2D (nt, n_traces) array")
    if data.shape[0] < 2:
        raise ValueError("at least two time samples are required")

    if window is not None:
        weights = np.asarray(window, dtype=np.float64)
        if weights.shape != (data.shape[0],):
            raise ValueError("window must have one value per time sample")
        data = data * weights[:, None]

    freqs = np.fft.rfftfreq(data.shape[0], d=float(dt))
    spectrum = np.abs(np.fft.rfft(data, axis=0))
    return freqs, np.mean(spectrum, axis=1)


def spectral_energy_band(freqs, amplitude, low_fraction=0.05, high_fraction=0.95):
    """Return frequency band containing the requested cumulative energy range."""
    freqs = np.asarray(freqs, dtype=np.float64)
    amplitude = np.asarray(amplitude, dtype=np.float64)
    if freqs.shape != amplitude.shape:
        raise ValueError("freqs and amplitude must have matching shapes")
    if not 0.0 <= low_fraction < high_fraction <= 1.0:
        raise ValueError("fractions must satisfy 0 <= low < high <= 1")

    energy = amplitude ** 2
    total = float(np.sum(energy))
    if total <= 0.0:
        return {
            "low_hz": None,
            "high_hz": None,
            "peak_hz": None,
            "total_energy": 0.0,
        }

    cumulative = np.cumsum(energy) / total
    low_index = int(np.searchsorted(cumulative, low_fraction, side="left"))
    high_index = int(np.searchsorted(cumulative, high_fraction, side="left"))
    peak_index = int(np.argmax(amplitude))
    return {
        "low_hz": float(freqs[min(low_index, freqs.size - 1)]),
        "high_hz": float(freqs[min(high_index, freqs.size - 1)]),
        "peak_hz": float(freqs[peak_index]),
        "total_energy": total,
    }


def band_energy_fraction(freqs, amplitude, low_hz=None, high_hz=None):
    """Return fraction of spectral energy inside a band."""
    freqs = np.asarray(freqs, dtype=np.float64)
    amplitude = np.asarray(amplitude, dtype=np.float64)
    energy = amplitude ** 2
    total = float(np.sum(energy))
    if total <= 0.0:
        return 0.0

    mask = np.ones_like(freqs, dtype=bool)
    if low_hz is not None:
        mask &= freqs >= float(low_hz)
    if high_hz is not None:
        mask &= freqs <= float(high_hz)
    return float(np.sum(energy[mask]) / total)
