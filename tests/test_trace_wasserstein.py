"""Tests for trace-level Softplus/Sinkhorn Wasserstein diagnostics."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.trace_wasserstein import (  # noqa: E402
    quadratic_cost_matrix,
    sinkhorn_divergence,
    softplus_density,
    softplus_sinkhorn_distance,
)


def _ricker(length=192, center=0.45, width=0.06):
    time = np.linspace(0.0, 1.0, length)
    tau = (time - center) / width
    return (1.0 - 2.0 * tau ** 2) * np.exp(-tau ** 2)


def test_softplus_density_is_positive_unit_mass_for_signed_trace():
    trace = np.array([-2.0, 0.0, 1.0, 3.0])

    density = softplus_density(trace, beta=3.0)

    assert np.all(density > 0.0)
    assert np.isclose(np.sum(density), 1.0)


def test_sinkhorn_divergence_is_zero_for_identical_density():
    density = np.array([0.1, 0.2, 0.4, 0.3])
    cost = quadratic_cost_matrix(density.size)

    value = sinkhorn_divergence(density, density, cost=cost, epsilon=0.05)

    assert value < 1e-12


def test_sinkhorn_divergence_is_symmetric():
    a = np.array([0.1, 0.6, 0.2, 0.1])
    b = np.array([0.2, 0.1, 0.2, 0.5])
    cost = quadratic_cost_matrix(a.size)

    ab = sinkhorn_divergence(a, b, cost=cost, epsilon=0.05)
    ba = sinkhorn_divergence(b, a, cost=cost, epsilon=0.05)

    assert np.isclose(ab, ba, rtol=1e-10, atol=1e-12)
    assert ab > 0.0


def test_softplus_sinkhorn_distance_increases_for_larger_shift():
    trace = _ricker()
    small_shift = np.roll(trace, 3)
    large_shift = np.roll(trace, 16)

    d_small = softplus_sinkhorn_distance(trace, small_shift, beta=8.0, epsilon=0.02)
    d_large = softplus_sinkhorn_distance(trace, large_shift, beta=8.0, epsilon=0.02)

    assert d_large > d_small > 0.0


def test_softplus_sinkhorn_distance_handles_trace_matrices_and_downsampling():
    trace = _ricker(length=128)
    observed = np.column_stack([trace, np.roll(trace, 2)])
    synthetic = np.column_stack([np.roll(trace, 4), np.roll(trace, 5)])

    value = softplus_sinkhorn_distance(
        observed,
        synthetic,
        beta=6.0,
        epsilon=0.03,
        downsample=2,
    )

    assert value > 0.0


def test_softplus_sinkhorn_distance_rejects_shape_mismatch():
    with pytest.raises(ValueError, match="matching shapes"):
        softplus_sinkhorn_distance(np.zeros(8), np.zeros((8, 2)))
