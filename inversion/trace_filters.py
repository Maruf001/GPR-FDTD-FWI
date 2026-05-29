"""Frequency-domain trace filters for staged GPR waveform objectives."""

import numpy as np


def _cosine_ramp(x):
    x = np.clip(x, 0.0, 1.0)
    return 0.5 - 0.5 * np.cos(np.pi * x)


def bandpass_response(freqs, low_hz=None, high_hz=None, taper_hz=0.0):
    """Build a tapered bandpass response for non-negative FFT frequencies."""
    freqs = np.asarray(freqs, dtype=np.float64)
    response = np.ones_like(freqs)
    if low_hz is not None and low_hz < 0.0:
        raise ValueError("low_hz must be non-negative")
    if high_hz is not None and high_hz <= 0.0:
        raise ValueError("high_hz must be positive")
    if low_hz is not None and high_hz is not None and low_hz >= high_hz:
        raise ValueError("low_hz must be smaller than high_hz")
    if taper_hz < 0.0:
        raise ValueError("taper_hz must be non-negative")

    if low_hz is not None:
        response[freqs < low_hz] = 0.0
        if taper_hz > 0.0:
            start = max(0.0, low_hz - taper_hz)
            mask = (freqs >= start) & (freqs < low_hz)
            response[mask] = _cosine_ramp((freqs[mask] - start) / (low_hz - start))

    if high_hz is not None:
        response[freqs > high_hz] = 0.0
        if taper_hz > 0.0:
            stop = high_hz + taper_hz
            mask = (freqs > high_hz) & (freqs <= stop)
            response[mask] = 1.0 - _cosine_ramp((freqs[mask] - high_hz) / (stop - high_hz))

    return response


def apply_bandpass_traces(traces, dt, low_hz=None, high_hz=None, taper_hz=0.0):
    """Apply the same FFT bandpass filter to each trace column."""
    data = np.asarray(traces, dtype=np.float64)
    if data.ndim == 1:
        squeeze = True
        data_2d = data[:, None]
    elif data.ndim == 2:
        squeeze = False
        data_2d = data
    else:
        raise ValueError("traces must have shape (nt,) or (nt, n_traces)")
    if dt <= 0.0:
        raise ValueError("dt must be positive")

    freqs = np.fft.rfftfreq(data_2d.shape[0], d=dt)
    response = bandpass_response(freqs, low_hz=low_hz, high_hz=high_hz, taper_hz=taper_hz)
    spectrum = np.fft.rfft(data_2d, axis=0)
    filtered = np.fft.irfft(spectrum * response[:, None], n=data_2d.shape[0], axis=0)
    return filtered[:, 0] if squeeze else filtered

