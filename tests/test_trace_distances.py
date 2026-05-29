"""Tests for trace-level distance and shift diagnostics."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.trace_distances import (  # noqa: E402
    dominant_frequency_hz,
    least_squares_distance,
    trace_shift_diagnostics,
)


def test_least_squares_distance_is_zero_for_identical_traces():
    trace = np.array([[0.0, 1.0], [1.0, 0.0], [0.0, -1.0]])

    assert least_squares_distance(trace, trace) == 0.0


def test_dominant_frequency_detects_sine_peak():
    dt = 0.001
    time = np.arange(0.0, 1.0, dt)
    trace = np.sin(2.0 * np.pi * 5.0 * time)

    frequency = dominant_frequency_hz(trace, dt)

    assert abs(frequency - 5.0) < 0.25


def test_trace_shift_diagnostics_reports_known_shift():
    dt = 0.001
    time = np.arange(0.0, 1.0, dt)
    observed = np.sin(2.0 * np.pi * 5.0 * time)
    synthetic = np.roll(observed, 10)

    diagnostics = trace_shift_diagnostics(
        observed,
        synthetic,
        dt,
        dominant_frequency=5.0,
    )

    assert diagnostics["trace_count"] == 1
    assert abs(abs(diagnostics["shift_samples"][0]) - 10) <= 1
    assert abs(diagnostics["max_rccc"] - 0.05) < 0.01
    assert diagnostics["nrccc_fraction_lt_half_period"] == 1.0


if __name__ == "__main__":
    tests = [
        ("least-squares zero for identical traces", test_least_squares_distance_is_zero_for_identical_traces),
        ("dominant frequency detects sine peak", test_dominant_frequency_detects_sine_peak),
        ("trace shift reports known shift", test_trace_shift_diagnostics_reports_known_shift),
    ]

    print("=" * 50)
    print("Trace Distance Tests")
    print("=" * 50)

    passed = 0
    failed = 0
    for name, test_fn in tests:
        try:
            print(f"\n[{name}]")
            test_fn()
            print("  PASSED")
            passed += 1
        except Exception as exc:
            print(f"  FAILED: {exc}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    if failed:
        raise SystemExit(1)

