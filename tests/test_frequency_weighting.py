"""Tests for cumulative/weighted frequency objective helpers."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.frequency_weighting import (  # noqa: E402
    best_curve_by_radius,
    frequency_key,
    parse_frequency_list_ghz,
    parse_weight_sets,
    radius_margin_from_ranked,
    rank_weighted_candidates,
    weighted_misfit,
)


def test_parse_frequency_list_ghz_converts_to_hz():
    values = parse_frequency_list_ghz("1.0, 1.5")

    assert values == [1.0e9, 1.5e9]


def test_parse_weight_sets_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="2 frequencies"):
        parse_weight_sets("bad:1,2,3", ["1GHz", "1.5GHz"])


def test_weighted_misfit_uses_normalized_weights():
    value = weighted_misfit(
        {"1GHz": 4.0, "1.5GHz": 10.0},
        {"1GHz": 1.0, "1.5GHz": 3.0},
    )

    assert value == 8.5


def test_rank_and_radius_margin_prefer_weighted_candidate():
    candidates = [
        {
            "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
            "misfit_by_frequency": {"1GHz": 0.2, "1.5GHz": 0.0},
        },
        {
            "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.2},
            "misfit_by_frequency": {"1GHz": 0.0, "1.5GHz": 0.4},
        },
    ]

    ranked = rank_weighted_candidates(candidates, {"1GHz": 0.1, "1.5GHz": 1.0})
    margin = radius_margin_from_ranked(ranked)

    assert ranked[0]["params"]["radius_mm"] == 6.0
    assert margin["best_radius_mm"] == 6.0
    assert margin["next_radius_mm"] == 6.2
    assert margin["radius_margin_abs"] > 0.0


def test_best_curve_by_radius_minimizes_over_depth():
    candidates = [
        {
            "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
            "misfit_by_frequency": {"1GHz": 0.1},
        },
        {
            "params": {"x_mm": 250.0, "z_mm": 91.0, "radius_mm": 6.0},
            "misfit_by_frequency": {"1GHz": 0.05},
        },
    ]

    curve = best_curve_by_radius(candidates, {"1GHz": 1.0})

    assert curve == [{
        "radius_mm": 6.0,
        "misfit": 0.05,
        "params": {"x_mm": 250.0, "z_mm": 91.0, "radius_mm": 6.0},
    }]


def test_frequency_key_is_stable_for_json_maps():
    assert frequency_key(1.5e9) == "1.5GHz"
