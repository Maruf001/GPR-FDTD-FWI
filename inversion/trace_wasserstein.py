"""Trace-level Softplus/Sinkhorn distances for objective diagnostics."""

from __future__ import annotations

import numpy as np


def _as_trace_matrix(data):
    array = np.asarray(data, dtype=np.float64)
    if array.ndim == 1:
        return array[:, None]
    if array.ndim != 2:
        raise ValueError("trace data must have shape (nt,) or (nt, n_traces)")
    return array


def _validate_density(values, floor=1e-300):
    density = np.asarray(values, dtype=np.float64)
    if density.ndim != 1:
        raise ValueError("density must be one-dimensional")
    if density.size == 0:
        raise ValueError("density must be non-empty")
    if np.any(~np.isfinite(density)) or np.any(density < 0.0):
        raise ValueError("density must be finite and non-negative")
    total = float(np.sum(density))
    if total <= 0.0:
        raise ValueError("density must have positive mass")
    normalized = density / total
    return np.maximum(normalized, floor) / np.sum(np.maximum(normalized, floor))


def softplus_density(trace, beta=8.0, amplitude_scale=None, floor=1e-12):
    """
    Convert a signed trace into a positive unit-mass density.

    The trace is scaled by its max absolute amplitude by default. That keeps the
    Softplus parameter dimensionless for both normalized test traces and small
    GPR amplitudes.
    """
    values = np.asarray(trace, dtype=np.float64)
    if values.ndim != 1:
        raise ValueError("trace must be one-dimensional")
    if beta <= 0.0:
        raise ValueError("beta must be positive")

    if amplitude_scale is None:
        amplitude_scale = max(float(np.max(np.abs(values))) if values.size else 0.0, floor)
    if amplitude_scale <= 0.0:
        raise ValueError("amplitude_scale must be positive")

    scaled = values / float(amplitude_scale)
    transformed = np.logaddexp(0.0, beta * scaled)
    transformed = transformed + float(floor)
    return transformed / np.sum(transformed)


def quadratic_cost_matrix(length, dt=1.0, normalize_time=True):
    """Build a squared-time-distance cost matrix for one trace."""
    length = int(length)
    if length <= 0:
        raise ValueError("length must be positive")
    if dt <= 0.0:
        raise ValueError("dt must be positive")

    time = np.arange(length, dtype=np.float64) * float(dt)
    if normalize_time and length > 1:
        time = (time - time[0]) / (time[-1] - time[0])
    return (time[:, None] - time[None, :]) ** 2


def sinkhorn_transport_cost(a, b, cost, epsilon=0.02, max_iter=500, tol=1e-10):
    """Compute entropy-regularized transport cost between two 1D densities."""
    a = _validate_density(a)
    b = _validate_density(b)
    cost = np.asarray(cost, dtype=np.float64)
    if cost.shape != (a.size, b.size):
        raise ValueError("cost matrix shape must match density lengths")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if max_iter <= 0:
        raise ValueError("max_iter must be positive")

    kernel = np.exp(-cost / float(epsilon))
    kernel = np.maximum(kernel, 1e-300)
    u = np.ones_like(a)
    v = np.ones_like(b)
    for _ in range(int(max_iter)):
        u_prev = u
        kv = np.maximum(kernel @ v, 1e-300)
        u = a / kv
        ktu = np.maximum(kernel.T @ u, 1e-300)
        v = b / ktu
        if np.max(np.abs(u - u_prev)) < tol:
            break

    plan = (u[:, None] * kernel) * v[None, :]
    return float(np.sum(plan * cost))


def sinkhorn_divergence(a, b, cost=None, epsilon=0.02, max_iter=500, tol=1e-10):
    """
    Return debiased Sinkhorn divergence.

    Entropic transport has a positive self-cost. The divergence subtracts half
    the two self-costs so identical densities evaluate near zero.
    """
    a = _validate_density(a)
    b = _validate_density(b)
    if a.size != b.size:
        raise ValueError("densities must have the same length")
    if cost is None:
        cost = quadratic_cost_matrix(a.size)
    ab = sinkhorn_transport_cost(a, b, cost, epsilon=epsilon, max_iter=max_iter, tol=tol)
    aa = sinkhorn_transport_cost(a, a, cost, epsilon=epsilon, max_iter=max_iter, tol=tol)
    bb = sinkhorn_transport_cost(b, b, cost, epsilon=epsilon, max_iter=max_iter, tol=tol)
    return float(max(0.0, ab - 0.5 * aa - 0.5 * bb))


def _downsample_mean(data, factor):
    factor = int(factor)
    if factor <= 1:
        return data
    usable = (data.shape[0] // factor) * factor
    if usable == 0:
        raise ValueError("downsample factor is larger than trace length")
    trimmed = data[:usable]
    return trimmed.reshape(usable // factor, factor, data.shape[1]).mean(axis=1)


def softplus_sinkhorn_distance(
        observed,
        synthetic,
        beta=8.0,
        epsilon=0.02,
        dt=1.0,
        mute=None,
        downsample=1,
        max_iter=500,
        tol=1e-10):
    """Average Softplus/Sinkhorn divergence over columns of a trace matrix."""
    observed = _as_trace_matrix(observed)
    synthetic = _as_trace_matrix(synthetic)
    if observed.shape != synthetic.shape:
        raise ValueError("observed and synthetic traces must have matching shapes")
    if dt <= 0.0:
        raise ValueError("dt must be positive")

    if mute is not None:
        weight = np.asarray(mute, dtype=np.float64)
        if weight.ndim != 1 or weight.shape[0] != observed.shape[0]:
            raise ValueError("mute must have shape (nt,)")
        observed = observed * weight[:, None]
        synthetic = synthetic * weight[:, None]

    observed = _downsample_mean(observed, downsample)
    synthetic = _downsample_mean(synthetic, downsample)
    cost = quadratic_cost_matrix(observed.shape[0], dt=dt * max(1, int(downsample)))

    distances = []
    for index in range(observed.shape[1]):
        scale = max(
            float(np.max(np.abs(observed[:, index]))),
            float(np.max(np.abs(synthetic[:, index]))),
            1e-12,
        )
        obs_density = softplus_density(observed[:, index], beta=beta, amplitude_scale=scale)
        syn_density = softplus_density(synthetic[:, index], beta=beta, amplitude_scale=scale)
        distances.append(
            sinkhorn_divergence(
                obs_density,
                syn_density,
                cost=cost,
                epsilon=epsilon,
                max_iter=max_iter,
                tol=tol,
            )
        )
    return float(np.mean(distances)) if distances else 0.0
