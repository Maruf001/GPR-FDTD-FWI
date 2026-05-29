"""Tests for the multi-rebar common-radius profile runner."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_multi_rebar_common_radius_profile import (  # noqa: E402
    best_curve_by_radius,
    build_rebar_specs_mm,
    radii_for_candidate,
    rank_case,
)


def test_build_rebar_specs_mm_converts_to_z_x_radius_meters():
    specs = build_rebar_specs_mm([150.0, 250.0], [90.0, 91.0], 6.0)

    assert specs == [
        (0.09, 0.15, 0.006),
        (0.091, 0.25, 0.006),
    ]


def test_build_rebar_specs_mm_rejects_mismatched_lists():
    with pytest.raises(ValueError, match="same length"):
        build_rebar_specs_mm([150.0], [90.0, 91.0], 6.0)


def test_radii_for_candidate_supports_common_radius():
    assert radii_for_candidate(3, 6.0, 6.4, sweep_rebar_index=-1) == [6.4, 6.4, 6.4]


def test_radii_for_candidate_supports_one_rebar_sweep():
    assert radii_for_candidate(3, 6.0, 6.4, sweep_rebar_index=1) == [6.0, 6.4, 6.0]


def test_radii_for_candidate_rejects_bad_index():
    with pytest.raises(ValueError, match="valid"):
        radii_for_candidate(3, 6.0, 6.4, sweep_rebar_index=3)


def test_rank_case_sorts_common_radius_candidates():
    candidates = [
        {
            "params": {"radius_mm": 6.2, "common_radius_mm": 6.2},
            "case_results": {
                "nominal": {
                    "misfit": 2.0,
                    "source_profile": {"frequency_scale": 1.0},
                }
            },
        },
        {
            "params": {"radius_mm": 6.0, "common_radius_mm": 6.0},
            "case_results": {
                "nominal": {
                    "misfit": 1.0,
                    "source_profile": {"frequency_scale": 1.1},
                }
            },
        },
    ]

    ranked = rank_case(candidates, "nominal")

    assert ranked[0]["params"]["common_radius_mm"] == 6.0
    assert ranked[0]["source_profile"]["frequency_scale"] == 1.1


def test_best_curve_by_radius_returns_radius_order():
    candidates = [
        {
            "params": {"radius_mm": 6.2, "common_radius_mm": 6.2},
            "case_results": {"case": {"misfit": 2.0, "source_profile": {}}},
        },
        {
            "params": {"radius_mm": 6.0, "common_radius_mm": 6.0},
            "case_results": {"case": {"misfit": 1.0, "source_profile": {}}},
        },
    ]

    curve = best_curve_by_radius(candidates, "case")

    assert [item["radius_mm"] for item in curve] == [6.0, 6.2]
