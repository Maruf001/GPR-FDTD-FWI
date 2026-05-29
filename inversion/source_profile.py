"""Source-profiled trace objective helpers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SourceProfileResult:
    """Best source nuisance profile for one candidate comparison."""

    misfit: float
    frequency_scale: float
    time_shift_s: float
    amplitude_scale: float

    def as_dict(self):
        return {
            "misfit": float(self.misfit),
            "frequency_scale": float(self.frequency_scale),
            "time_shift_s": float(self.time_shift_s),
            "time_shift_ps": float(self.time_shift_s * 1e12),
            "amplitude_scale": float(self.amplitude_scale),
        }


def _as_trace_matrix(data):
    array = np.asarray(data, dtype=np.float64)
    if array.ndim == 1:
        return array[:, None]
    if array.ndim != 2:
        raise ValueError("trace data must have shape (nt,) or (nt, n_traces)")
    return array


def shift_traces_zero_fill(traces, dt, shift_s):
    """Shift trace matrix columns in time with interpolation and no wraparound."""
    data = _as_trace_matrix(traces)
    if dt <= 0.0:
        raise ValueError("dt must be positive")
    time = np.arange(data.shape[0], dtype=np.float64) * float(dt)
    shifted = np.empty_like(data)
    source_time = time - float(shift_s)
    for index in range(data.shape[1]):
        shifted[:, index] = np.interp(
            source_time,
            time,
            data[:, index],
            left=0.0,
            right=0.0,
        )
    return shifted[:, 0] if np.asarray(traces).ndim == 1 else shifted


def best_amplitude_scale(observed, synthetic, mute):
    """Return least-squares scalar multiplying synthetic toward observed."""
    observed = _as_trace_matrix(observed)
    synthetic = _as_trace_matrix(synthetic)
    if observed.shape != synthetic.shape:
        raise ValueError("observed and synthetic traces must have matching shapes")
    weight = np.asarray(mute, dtype=np.float64)
    if weight.ndim != 1 or weight.shape[0] != observed.shape[0]:
        raise ValueError("mute must have shape (nt,)")

    observed_w = observed * weight[:, None]
    synthetic_w = synthetic * weight[:, None]
    denominator = float(np.sum(synthetic_w ** 2))
    if denominator <= 1e-30:
        return 1.0
    return float(np.sum(observed_w * synthetic_w) / denominator)


def normalized_ls_misfit(observed, synthetic, mute, amplitude_scale=1.0):
    """Compute normalized least-squares objective for trace matrices."""
    observed = _as_trace_matrix(observed)
    synthetic = _as_trace_matrix(synthetic)
    if observed.shape != synthetic.shape:
        raise ValueError("observed and synthetic traces must have matching shapes")
    weight = np.asarray(mute, dtype=np.float64)
    if weight.ndim != 1 or weight.shape[0] != observed.shape[0]:
        raise ValueError("mute must have shape (nt,)")

    residual = (float(amplitude_scale) * synthetic - observed) * weight[:, None]
    numerator = 0.5 * float(np.sum(residual ** 2))
    denominator = max(0.5 * float(np.sum((observed * weight[:, None]) ** 2)), 1e-30)
    return numerator / denominator


def source_profiled_ls(
        observed,
        synthetic_by_frequency_scale,
        mute,
        dt,
        time_shift_values_s=(0.0,),
        fit_amplitude=False):
    """
    Return the best LS objective over source nuisance parameters.

    Parameters
    ----------
    observed : ndarray
        Observed trace matrix.
    synthetic_by_frequency_scale : mapping
        Maps modeled source frequency scale to synthetic trace matrix.
    mute : ndarray
        Time-domain mute/weight.
    dt : float
        Time step for interpolation-based time shifts.
    time_shift_values_s : iterable
        Candidate synthetic trace shifts in seconds.
    fit_amplitude : bool
        If true, fit one scalar synthetic amplitude per candidate profile.
    """
    observed = _as_trace_matrix(observed)
    if not synthetic_by_frequency_scale:
        raise ValueError("synthetic_by_frequency_scale must be non-empty")
    shifts = list(time_shift_values_s or [0.0])
    if not shifts:
        shifts = [0.0]

    best = None
    for frequency_scale, synthetic in synthetic_by_frequency_scale.items():
        synthetic = _as_trace_matrix(synthetic)
        for shift_s in shifts:
            shifted = (
                shift_traces_zero_fill(synthetic, dt, shift_s)
                if shift_s != 0.0
                else synthetic
            )
            amplitude_scale = (
                best_amplitude_scale(observed, shifted, mute)
                if fit_amplitude
                else 1.0
            )
            misfit = normalized_ls_misfit(
                observed,
                shifted,
                mute,
                amplitude_scale=amplitude_scale,
            )
            result = SourceProfileResult(
                misfit=float(misfit),
                frequency_scale=float(frequency_scale),
                time_shift_s=float(shift_s),
                amplitude_scale=float(amplitude_scale),
            )
            if best is None or result.misfit < best.misfit:
                best = result
    return best
