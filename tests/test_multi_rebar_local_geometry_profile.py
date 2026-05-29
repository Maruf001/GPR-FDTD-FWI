"""Tests for the multi-rebar local geometry profile runner."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    best_curve_by_radius,
    candidate_rebar_arrays,
    rank_case,
)


def test_candidate_rebar_arrays_updates_only_target():
    x_values, z_values, radii = candidate_rebar_arrays(
        [150.0, 250.0, 350.0],
        [90.0, 90.0, 90.0],
        6.0,
        0,
        148.0,
        89.0,
        5.8,
    )

    assert x_values == [148.0, 250.0, 350.0]
    assert z_values == [89.0, 90.0, 90.0]
    assert radii == [5.8, 6.0, 6.0]


def test_candidate_rebar_arrays_rejects_bad_target():
    with pytest.raises(ValueError, match="valid"):
        candidate_rebar_arrays([150.0], [90.0], 6.0, 1, 150.0, 90.0, 6.0)


def test_rank_case_sorts_local_geometry_candidates():
    candidates = [
        {
            "params": {"x_mm": 148.0, "z_mm": 90.0, "radius_mm": 6.2},
            "case_results": {
                "case": {
                    "misfit": 2.0,
                    "source_profile": {"frequency_scale": 1.0},
                }
            },
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {
                "case": {
                    "misfit": 1.0,
                    "source_profile": {"frequency_scale": 1.1},
                }
            },
        },
    ]

    ranked = rank_case(candidates, "case")

    assert ranked[0]["params"]["x_mm"] == 150.0
    assert ranked[0]["source_profile"]["frequency_scale"] == 1.1


def test_best_curve_by_radius_profiles_over_xz():
    candidates = [
        {
            "params": {"x_mm": 148.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {"case": {"misfit": 2.0, "source_profile": {}}},
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {"case": {"misfit": 1.0, "source_profile": {}}},
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.2},
            "case_results": {"case": {"misfit": 1.5, "source_profile": {}}},
        },
    ]

    curve = best_curve_by_radius(candidates, "case")

    assert curve[0]["radius_mm"] == 6.0
    assert curve[0]["params"]["x_mm"] == 150.0
    assert curve[1]["radius_mm"] == 6.2
