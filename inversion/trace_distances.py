"""Trace-level distances and alignment diagnostics for GPR inversions."""

import numpy as np


def _as_trace_matrix(data):
    array = np.asarray(data, dtype=np.float64)
    if array.ndim == 1:
        return array[:, None]
    if array.ndim != 2:
        raise ValueError("trace data must have shape (nt,) or (nt, n_traces)")
    return array


def _as_time_weight(mute, nt):
    if mute is None:
        return np.ones(nt, dtype=np.float64)
    weight = np.asarray(mute, dtype=np.float64)
    if weight.ndim != 1 or weight.shape[0] != nt:
        raise ValueError("mute must have shape (nt,)")
    return weight


def least_squares_distance(observed, synthetic, mute=None, normalize=True):
    """Return the current waveform least-squares distance for B-scan traces."""
    observed = _as_trace_matrix(observed)
    synthetic = _as_trace_matrix(synthetic)
    if observed.shape != synthetic.shape:
        raise ValueError("observed and synthetic traces must have matching shapes")

    weight = _as_time_weight(mute, observed.shape[0])
    residual = (synthetic - observed) * weight[:, None]
    value = 0.5 * float(np.sum(residual ** 2))
    if not normalize:
        return value

    norm = 0.5 * float(np.sum((observed * weight[:, None]) ** 2))
    return value / max(norm, 1e-30)


def dominant_frequency_hz(traces, dt, mute=None):
    """Estimate dominant frequency from the mean muted amplitude spectrum."""
    traces = _as_trace_matrix(traces)
    if dt <= 0.0:
        raise ValueError("dt must be positive")

    weight = _as_time_weight(mute, traces.shape[0])
    weighted = traces * weight[:, None]
    weighted = weighted - np.mean(weighted, axis=0, keepdims=True)
    spectrum = np.mean(np.abs(np.fft.rfft(weighted, axis=0)), axis=1)
    freqs = np.fft.rfftfreq(traces.shape[0], d=dt)
    if spectrum.size <= 1 or np.all(spectrum[1:] <= 0.0):
        return 0.0
    index = int(np.argmax(spectrum[1:]) + 1)
    return float(freqs[index])


def _trace_shift_samples(observed_trace, synthetic_trace):
    obs = np.asarray(observed_trace, dtype=np.float64)
    syn = np.asarray(synthetic_trace, dtype=np.float64)
    obs = obs - np.mean(obs)
    syn = syn - np.mean(syn)
    if np.allclose(obs, 0.0) or np.allclose(syn, 0.0):
        return 0
    corr = np.correlate(syn, obs, mode="full")
    return int(np.argmax(corr) - (obs.size - 1))


def trace_shift_diagnostics(observed, synthetic, dt, mute=None, dominant_frequency=None):
    """
    Compute cross-correlation shift diagnostics for observed/synthetic traces.

    RCCC follows the optimal-transport FWI paper's idea: absolute trace shift
    divided by dominant period. NRCCC is the fraction of traces with RCCC < 0.5.
    """
    observed = _as_trace_matrix(observed)
    synthetic = _as_trace_matrix(synthetic)
    if observed.shape != synthetic.shape:
        raise ValueError("observed and synthetic traces must have matching shapes")
    if dt <= 0.0:
        raise ValueError("dt must be positive")

    weight = _as_time_weight(mute, observed.shape[0])
    obs_weighted = observed * weight[:, None]
    syn_weighted = synthetic * weight[:, None]

    frequency = (
        float(dominant_frequency)
        if dominant_frequency is not None
        else dominant_frequency_hz(obs_weighted, dt, mute=None)
    )
    period = 1.0 / frequency if frequency > 0.0 else np.inf

    shifts = []
    for index in range(observed.shape[1]):
        shift = _trace_shift_samples(obs_weighted[:, index], syn_weighted[:, index])
        shifts.append(shift)

    shift_samples = np.asarray(shifts, dtype=np.int64)
    abs_shift_s = np.abs(shift_samples.astype(np.float64) * dt)
    rccc = abs_shift_s / period if np.isfinite(period) else np.zeros_like(abs_shift_s)

    return {
        "dominant_frequency_hz": float(frequency),
        "dominant_period_s": float(period) if np.isfinite(period) else None,
        "trace_count": int(observed.shape[1]),
        "shift_samples": [int(value) for value in shift_samples],
        "shift_s": [float(value * dt) for value in shift_samples],
        "abs_shift_s": [float(value) for value in abs_shift_s],
        "rccc": [float(value) for value in rccc],
        "nrccc_fraction_lt_half_period": float(np.mean(rccc < 0.5)) if rccc.size else 0.0,
        "median_abs_shift_s": float(np.median(abs_shift_s)) if abs_shift_s.size else 0.0,
        "mean_abs_shift_s": float(np.mean(abs_shift_s)) if abs_shift_s.size else 0.0,
        "max_abs_shift_s": float(np.max(abs_shift_s)) if abs_shift_s.size else 0.0,
        "median_rccc": float(np.median(rccc)) if rccc.size else 0.0,
        "mean_rccc": float(np.mean(rccc)) if rccc.size else 0.0,
        "max_rccc": float(np.max(rccc)) if rccc.size else 0.0,
        "least_squares_distance": least_squares_distance(
            observed,
            synthetic,
            mute=mute,
            normalize=True,
        ),
    }

