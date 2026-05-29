"""Tests for the trace W2 convexity runner helpers."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_trace_wasserstein_convexity import (  # noqa: E402
    compute_shift_curves,
    ricker_trace,
    shift_trace_zero_fill,
)


def test_shift_trace_zero_fill_does_not_wrap():
    trace = np.array([1.0, 2.0, 3.0, 4.0])

    assert np.allclose(shift_trace_zero_fill(trace, 1), [0.0, 1.0, 2.0, 3.0])
    assert np.allclose(shift_trace_zero_fill(trace, -1), [2.0, 3.0, 4.0, 0.0])


def test_ricker_trace_is_normalized():
    _, trace = ricker_trace(length=64)

    assert np.isclose(np.max(np.abs(trace)), 1.0)


def test_compute_shift_curves_has_zero_minimum_for_identical_trace():
    rows = compute_shift_curves(
        shifts=[-2, 0, 2],
        length=96,
        beta_values=(6.0,),
        epsilon=0.03,
        downsample=2,
    )
    by_shift = {row["shift_samples"]: row for row in rows}

    assert by_shift[0]["l2"] == 0.0
    assert by_shift[0]["w2_beta_6"] < by_shift[2]["w2_beta_6"]
