"""Tests for wavelet mismatch runner helpers."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_wavelet_mismatch import (  # noqa: E402
    best_amplitude_scale,
    parse_positive_values,
    parse_wavelet_cases,
    shift_traces_zero_fill,
    shift_wavelet_zero_fill,
)


def test_parse_wavelet_cases_parses_labelled_cases():
    cases = parse_wavelet_cases("nominal:1,0,1|late:1.0,50,0.9")

    assert cases == [
        {"label": "nominal", "frequency_scale": 1.0, "time_shift_ps": 0.0, "amplitude_scale": 1.0},
        {"label": "late", "frequency_scale": 1.0, "time_shift_ps": 50.0, "amplitude_scale": 0.9},
    ]


def test_parse_wavelet_cases_rejects_duplicate_labels():
    with pytest.raises(ValueError, match="unique"):
        parse_wavelet_cases("same:1,0,1|same:1,1,1")


def test_shift_wavelet_zero_fill_does_not_wrap():
    wavelet = np.array([0.0, 1.0, 2.0, 0.0])
    shifted = shift_wavelet_zero_fill(wavelet, dt=1.0, shift_s=1.0)

    assert np.allclose(shifted, [0.0, 0.0, 1.0, 2.0])


def test_best_amplitude_scale_recovers_scalar():
    synthetic = np.array([[1.0, 2.0], [3.0, 4.0]])
    observed = 1.25 * synthetic
    mute = np.ones(2)

    assert np.isclose(best_amplitude_scale(observed, synthetic, mute), 1.25)


def test_shift_traces_zero_fill_shifts_columns():
    traces = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])

    shifted = shift_traces_zero_fill(traces, dt=1.0, shift_s=1.0)

    assert np.allclose(shifted, [[0.0, 0.0], [1.0, 10.0], [2.0, 20.0]])


def test_parse_positive_values_rejects_non_positive():
    with pytest.raises(Exception):
        parse_positive_values("0.9,0")
