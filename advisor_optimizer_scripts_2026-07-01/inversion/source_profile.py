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
    ringdown_scale: float = 0.0
    ringdown_delay_s: float = 0.0
    ringdown_frequency_scale: float = 1.0
    primary_coefficient: float = 1.0
    ringdown_coefficient: float = 0.0

    def as_dict(self):
        return {
            "misfit": float(self.misfit),
            "frequency_scale": float(self.frequency_scale),
            "time_shift_s": float(self.time_shift_s),
            "time_shift_ps": float(self.time_shift_s * 1e12),
            "amplitude_scale": float(self.amplitude_scale),
            "ringdown_scale": float(self.ringdown_scale),
            "ringdown_delay_s": float(self.ringdown_delay_s),
            "ringdown_delay_ps": float(self.ringdown_delay_s * 1e12),
            "ringdown_frequency_scale": float(self.ringdown_frequency_scale),
            "primary_coefficient": float(self.primary_coefficient),
            "ringdown_coefficient": float(self.ringdown_coefficient),
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
    if not synthetic_by_frequency_scale:
        raise ValueError("synthetic_by_frequency_scale must be non-empty")
    synthetic_profiles = [
        {
            "frequency_scale": float(frequency_scale),
            "traces": synthetic,
        }
        for frequency_scale, synthetic in synthetic_by_frequency_scale.items()
    ]
    return source_profiled_ls_over_profiles(
        observed,
        synthetic_profiles,
        mute,
        dt,
        time_shift_values_s=time_shift_values_s,
        fit_amplitude=fit_amplitude,
    )


def source_profiled_ls_over_profiles(
        observed,
        synthetic_profiles,
        mute,
        dt,
        time_shift_values_s=(0.0,),
        fit_amplitude=False):
    """
    Return the best LS objective over explicit source-profile synthetics.

    Each item in ``synthetic_profiles`` must contain ``traces`` and may include
    source metadata such as frequency scale or ringdown parameters. This helper
    is used when the modeled source profile has more than one free shape
    parameter, while ``source_profiled_ls`` keeps the legacy frequency-scale
    mapping interface.
    """
    observed = _as_trace_matrix(observed)
    profiles = list(synthetic_profiles or [])
    if not profiles:
        raise ValueError("synthetic_profiles must be non-empty")
    shifts = list(time_shift_values_s or [0.0])
    if not shifts:
        shifts = [0.0]

    best = None
    for profile in profiles:
        synthetic = _as_trace_matrix(profile["traces"])
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
                frequency_scale=float(profile.get("frequency_scale", 1.0)),
                time_shift_s=float(shift_s),
                amplitude_scale=float(amplitude_scale),
                ringdown_scale=float(profile.get("ringdown_scale", 0.0)),
                ringdown_delay_s=float(profile.get("ringdown_delay_s", 0.0)),
                ringdown_frequency_scale=float(profile.get("ringdown_frequency_scale", 1.0)),
                primary_coefficient=float(amplitude_scale),
                ringdown_coefficient=float(amplitude_scale) * float(profile.get("ringdown_scale", 0.0)),
            )
            if best is None or result.misfit < best.misfit:
                best = result
    return best


def best_basis_coefficients(observed, basis_traces, mute):
    """Fit source-basis coefficients by weighted least squares."""
    observed = _as_trace_matrix(observed)
    bases = [_as_trace_matrix(basis) for basis in basis_traces]
    if not bases:
        raise ValueError("basis_traces must be non-empty")
    for basis in bases:
        if basis.shape != observed.shape:
            raise ValueError("observed and basis traces must have matching shapes")
    weight = np.asarray(mute, dtype=np.float64)
    if weight.ndim != 1 or weight.shape[0] != observed.shape[0]:
        raise ValueError("mute must have shape (nt,)")

    weighted_observed = (observed * weight[:, None]).reshape(-1)
    design = np.column_stack([
        (basis * weight[:, None]).reshape(-1)
        for basis in bases
    ])
    if float(np.sum(design ** 2)) <= 1e-30:
        coefficients = np.zeros(len(bases), dtype=np.float64)
        coefficients[0] = 1.0
        return coefficients
    coefficients, *_ = np.linalg.lstsq(design, weighted_observed, rcond=None)
    return np.asarray(coefficients, dtype=np.float64)


def source_profiled_ls_over_basis_profiles(
        observed,
        basis_profiles,
        mute,
        dt,
        time_shift_values_s=(0.0,)):
    """Return the best LS objective over linear source-basis profiles."""
    observed = _as_trace_matrix(observed)
    profiles = list(basis_profiles or [])
    if not profiles:
        raise ValueError("basis_profiles must be non-empty")
    shifts = list(time_shift_values_s or [0.0])
    if not shifts:
        shifts = [0.0]

    best = None
    for profile in profiles:
        bases = [_as_trace_matrix(basis) for basis in profile["basis_traces"]]
        for shift_s in shifts:
            shifted_bases = [
                shift_traces_zero_fill(basis, dt, shift_s)
                if shift_s != 0.0
                else basis
                for basis in bases
            ]
            coefficients = best_basis_coefficients(observed, shifted_bases, mute)
            synthetic = np.zeros_like(observed)
            for coefficient, basis in zip(coefficients, shifted_bases):
                synthetic = synthetic + float(coefficient) * basis
            misfit = normalized_ls_misfit(
                observed,
                synthetic,
                mute,
                amplitude_scale=1.0,
            )
            primary_coefficient = float(coefficients[0]) if len(coefficients) >= 1 else 1.0
            ringdown_coefficient = float(coefficients[1]) if len(coefficients) >= 2 else 0.0
            ringdown_scale = (
                ringdown_coefficient / primary_coefficient
                if abs(primary_coefficient) > 1e-12
                else 0.0
            )
            result = SourceProfileResult(
                misfit=float(misfit),
                frequency_scale=float(profile.get("frequency_scale", 1.0)),
                time_shift_s=float(shift_s),
                amplitude_scale=primary_coefficient,
                ringdown_scale=float(ringdown_scale),
                ringdown_delay_s=float(profile.get("ringdown_delay_s", 0.0)),
                ringdown_frequency_scale=float(profile.get("ringdown_frequency_scale", 1.0)),
                primary_coefficient=primary_coefficient,
                ringdown_coefficient=ringdown_coefficient,
            )
            if best is None or result.misfit < best.misfit:
                best = result
    return best
