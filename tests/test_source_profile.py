"""Tests for source-profiled trace objective helpers."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.source_profile import (  # noqa: E402
    best_amplitude_scale,
    normalized_ls_misfit,
    shift_traces_zero_fill,
    source_profiled_ls,
)


def test_shift_traces_zero_fill_shifts_without_wraparound():
    traces = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])

    shifted = shift_traces_zero_fill(traces, dt=1.0, shift_s=1.0)

    assert np.allclose(shifted, [[0.0, 0.0], [1.0, 10.0], [2.0, 20.0]])


def test_best_amplitude_scale_recovers_scalar():
    synthetic = np.array([[1.0, 2.0], [3.0, 4.0]])
    observed = 1.5 * synthetic

    assert np.isclose(best_amplitude_scale(observed, synthetic, np.ones(2)), 1.5)


def test_normalized_ls_misfit_is_zero_for_scaled_match():
    synthetic = np.array([1.0, 2.0, 3.0])
    observed = 2.0 * synthetic

    value = normalized_ls_misfit(observed, synthetic, np.ones(3), amplitude_scale=2.0)

    assert value == 0.0


def test_source_profiled_ls_picks_frequency_shift_and_amplitude():
    base = np.array([0.0, 1.0, 2.0, 0.0])
    observed = 3.0 * shift_traces_zero_fill(base, dt=1.0, shift_s=1.0)
    synthetics = {
        0.9: np.zeros_like(base),
        1.0: base,
    }

    result = source_profiled_ls(
        observed,
        synthetics,
        np.ones(4),
        dt=1.0,
        time_shift_values_s=[0.0, 1.0],
        fit_amplitude=True,
    )

    assert result.frequency_scale == 1.0
    assert result.time_shift_s == 1.0
    assert np.isclose(result.amplitude_scale, 3.0)
    assert result.misfit == 0.0


def test_source_profiled_ls_rejects_missing_synthetics():
    with pytest.raises(ValueError, match="non-empty"):
        source_profiled_ls(np.zeros(4), {}, np.ones(4), dt=1.0)
