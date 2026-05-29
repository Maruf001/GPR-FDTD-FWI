"""Tests for source-profiled radius polish runner helpers."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_source_profiled_polish import (  # noqa: E402
    best_curve_by_radius,
    observed_wavelet,
    rank_candidates,
)


def test_rank_candidates_sorts_by_misfit():
    candidates = [
        {"misfit": 2.0, "params": {"radius_mm": 6.2}},
        {"misfit": 1.0, "params": {"radius_mm": 6.0}},
    ]

    ranked = rank_candidates(candidates)

    assert ranked[0]["params"]["radius_mm"] == 6.0


def test_best_curve_by_radius_profiles_over_source_and_depth():
    candidates = [
        {"misfit": 2.0, "params": {"radius_mm": 6.0, "z_mm": 90.0}},
        {"misfit": 1.0, "params": {"radius_mm": 6.0, "z_mm": 90.5}},
        {"misfit": 1.5, "params": {"radius_mm": 6.2, "z_mm": 90.0}},
    ]

    curve = best_curve_by_radius(candidates)

    assert curve == [
        {"misfit": 1.0, "params": {"radius_mm": 6.0, "z_mm": 90.5}},
        {"misfit": 1.5, "params": {"radius_mm": 6.2, "z_mm": 90.0}},
    ]


def test_observed_wavelet_applies_amplitude_scale():
    time = np.linspace(0.0, 2e-9, 128)
    base = observed_wavelet(time, 1.5e9, amplitude_scale=1.0)
    scaled = observed_wavelet(time, 1.5e9, amplitude_scale=2.0)

    assert np.allclose(scaled, 2.0 * base)
