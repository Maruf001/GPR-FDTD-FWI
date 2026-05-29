"""Tests for trace bandpass filters."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.trace_filters import apply_bandpass_traces, bandpass_response  # noqa: E402


def _amplitude_at(trace, dt, frequency):
    freqs = np.fft.rfftfreq(trace.size, d=dt)
    spectrum = np.abs(np.fft.rfft(trace))
    index = int(np.argmin(np.abs(freqs - frequency)))
    return float(spectrum[index])


def test_bandpass_response_rejects_invalid_bounds():
    try:
        bandpass_response(np.array([0.0, 1.0]), low_hz=2.0, high_hz=1.0)
    except ValueError:
        return
    raise AssertionError("expected invalid bounds to raise")


def test_apply_bandpass_keeps_in_band_tone_and_rejects_out_of_band_tone():
    dt = 0.001
    time = np.arange(0.0, 2.0, dt)
    low = np.sin(2.0 * np.pi * 5.0 * time)
    high = 0.5 * np.sin(2.0 * np.pi * 80.0 * time)
    trace = low + high

    filtered = apply_bandpass_traces(trace, dt, low_hz=1.0, high_hz=20.0, taper_hz=0.0)

    low_amp = _amplitude_at(filtered, dt, 5.0)
    high_amp = _amplitude_at(filtered, dt, 80.0)
    assert low_amp > 100.0
    assert high_amp < 1e-8


def test_apply_bandpass_handles_trace_matrix():
    dt = 0.001
    time = np.arange(0.0, 1.0, dt)
    traces = np.column_stack([
        np.sin(2.0 * np.pi * 5.0 * time),
        np.sin(2.0 * np.pi * 50.0 * time),
    ])

    filtered = apply_bandpass_traces(traces, dt, low_hz=1.0, high_hz=20.0)

    assert filtered.shape == traces.shape
    assert _amplitude_at(filtered[:, 0], dt, 5.0) > 100.0
    assert _amplitude_at(filtered[:, 1], dt, 50.0) < 1e-8


if __name__ == "__main__":
    tests = [
        ("bandpass response rejects invalid bounds", test_bandpass_response_rejects_invalid_bounds),
        ("bandpass keeps in-band tone", test_apply_bandpass_keeps_in_band_tone_and_rejects_out_of_band_tone),
        ("bandpass handles trace matrix", test_apply_bandpass_handles_trace_matrix),
    ]

    print("=" * 50)
    print("Trace Filter Tests")
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

