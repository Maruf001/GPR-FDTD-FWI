"""Tests for source-profiled radius polish runner helpers."""

import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_source_profiled_polish import (  # noqa: E402
    best_curve_by_radius,
    format_mm_value,
    observed_wavelet,
    parse_frequency_weights,
    profile_frequency_keys,
    rank_candidates,
    ringdown_component_wavelet,
    resolve_initial_params_mm,
    source_profiled_multifrequency_ls,
    write_candidate_csv,
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


def test_observed_wavelet_ringdown_changes_shape_without_changing_default():
    time = np.linspace(0.0, 3e-9, 256)
    base = observed_wavelet(time, 1.5e9)
    explicit_default = observed_wavelet(time, 1.5e9, ringdown_scale=0.0)
    ringing = observed_wavelet(
        time,
        1.5e9,
        ringdown_scale=0.25,
        ringdown_delay_ps=180.0,
        ringdown_frequency_scale=0.8,
    )

    assert np.allclose(explicit_default, base)
    assert not np.allclose(ringing, base)
    assert np.linalg.norm(ringing - base) > 0.0


def test_ringdown_component_matches_observed_wavelet_difference():
    time = np.linspace(0.0, 3e-9, 256)
    base = observed_wavelet(time, 1.5e9)
    component = ringdown_component_wavelet(
        time,
        1.5e9,
        ringdown_delay_ps=180.0,
        ringdown_frequency_scale=0.8,
    )
    ringing = observed_wavelet(
        time,
        1.5e9,
        ringdown_scale=0.25,
        ringdown_delay_ps=180.0,
        ringdown_frequency_scale=0.8,
    )

    np.testing.assert_allclose(ringing - base, 0.25 * component)


def test_format_mm_value_preserves_fine_radius_steps():
    assert format_mm_value(4.025) == "4.025"
    assert format_mm_value(4.0) == "4.0"


def test_resolve_initial_params_defaults_to_truth_location_and_larger_radius():
    params = resolve_initial_params_mm(248.0, 96.0, 7.0)

    assert params.as_mm() == {
        "x_mm": 248.0,
        "z_mm": 96.0,
        "radius_mm": 7.8,
    }


def test_parse_frequency_weights_matches_frequency_count():
    weights = parse_frequency_weights("1,2", [1.0e9, 1.5e9])

    assert weights == {1.0e9: 1.0, 1.5e9: 2.0}


def test_source_profiled_multifrequency_ls_uses_shared_scale_and_shift():
    time = np.linspace(0.0, 1.0, 8)
    observed_by_frequency = {
        1.0e9: time[:, None],
        1.5e9: (2.0 * time)[:, None],
    }
    synthetic_by_frequency_scale = {
        1.0e9: {
            1.0: time[:, None],
            1.1: (0.5 * time)[:, None],
        },
        1.5e9: {
            1.0: (2.0 * time)[:, None],
            1.1: (0.25 * time)[:, None],
        },
    }

    result = source_profiled_multifrequency_ls(
        observed_by_frequency,
        synthetic_by_frequency_scale,
        mute=np.ones(time.size),
        dt=1.0,
        frequency_weights={1.0e9: 1.0, 1.5e9: 1.0},
        time_shift_values_s=[0.0],
        fit_amplitude=False,
    )

    assert result["frequency_scale"] == 1.0
    assert result["misfit"] == 0.0
    assert result["misfit_by_frequency"]["1GHz"] == 0.0


def test_write_candidate_csv_includes_per_frequency_diagnostics(tmp_path):
    candidates = [
        {
            "misfit": 0.25,
            "params": {"x_mm": 250.0, "z_mm": 70.0, "radius_mm": 4.0},
            "source_profile": {
                "frequency_scale": 1.1,
                "time_shift_ps": -50.0,
                "amplitude_scale": 1.05,
                "misfit_by_frequency": {"1GHz": 0.1, "1.5GHz": 0.4},
                "amplitude_scale_by_frequency": {"1GHz": 1.0, "1.5GHz": 1.1},
            },
        },
    ]
    csv_path = tmp_path / "candidates.csv"

    write_candidate_csv(csv_path, candidates)

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert profile_frequency_keys(candidates) == ["1GHz", "1.5GHz"]
    assert rows[0]["frequency_misfit_1GHz"] == "0.1"
    assert rows[0]["frequency_misfit_1.5GHz"] == "0.4"
    assert rows[0]["frequency_amplitude_scale_1.5GHz"] == "1.1"
