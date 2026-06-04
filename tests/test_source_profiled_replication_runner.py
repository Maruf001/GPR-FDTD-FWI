"""Tests for source-profiled replication runner helpers."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_source_profiled_replication import (  # noqa: E402
    best_curve_by_radius,
    parse_nonnegative_values,
    parse_replication_cases,
    rank_case,
)


def test_parse_replication_cases_parses_source_and_noise():
    cases = parse_replication_cases("nominal:1,0,1,0,13|noisy:1.1,-50,0.9,0.05,21")

    assert cases == [
        {
            "label": "nominal",
            "frequency_scale": 1.0,
            "time_shift_ps": 0.0,
            "amplitude_scale": 1.0,
            "noise_fraction": 0.0,
            "noise_seed": 13,
            "ringdown_scale": 0.0,
            "ringdown_delay_ps": 180.0,
            "ringdown_frequency_scale": 0.8,
        },
        {
            "label": "noisy",
            "frequency_scale": 1.1,
            "time_shift_ps": -50.0,
            "amplitude_scale": 0.9,
            "noise_fraction": 0.05,
            "noise_seed": 21,
            "ringdown_scale": 0.0,
            "ringdown_delay_ps": 180.0,
            "ringdown_frequency_scale": 0.8,
        },
    ]


def test_parse_replication_cases_accepts_optional_ringdown_shape():
    cases = parse_replication_cases("ringing:1,0,1,0,13,0.25,180,0.8")

    assert cases == [
        {
            "label": "ringing",
            "frequency_scale": 1.0,
            "time_shift_ps": 0.0,
            "amplitude_scale": 1.0,
            "noise_fraction": 0.0,
            "noise_seed": 13,
            "ringdown_scale": 0.25,
            "ringdown_delay_ps": 180.0,
            "ringdown_frequency_scale": 0.8,
        }
    ]


def test_parse_replication_cases_rejects_duplicate_labels():
    with pytest.raises(Exception, match="unique"):
        parse_replication_cases("same:1,0,1,0,13|same:1,0,1,0,14")


def test_parse_replication_cases_rejects_negative_noise():
    with pytest.raises(Exception, match="noise"):
        parse_replication_cases("bad:1,0,1,-0.1,13")


def test_parse_nonnegative_values_accepts_zero_and_rejects_negative():
    assert parse_nonnegative_values("0,0.25") == [0.0, 0.25]
    with pytest.raises(Exception, match="non-negative"):
        parse_nonnegative_values("0,-0.1")


def test_rank_case_sorts_and_keeps_source_profile():
    candidates = [
        {
            "params": {"radius_mm": 6.2},
            "case_results": {
                "nominal": {
                    "misfit": 2.0,
                    "source_profile": {"frequency_scale": 1.0},
                }
            },
        },
        {
            "params": {"radius_mm": 6.0},
            "case_results": {
                "nominal": {
                    "misfit": 1.0,
                    "source_profile": {"frequency_scale": 1.1},
                }
            },
        },
    ]

    ranked = rank_case(candidates, "nominal")

    assert ranked[0]["params"]["radius_mm"] == 6.0
    assert ranked[0]["source_profile"]["frequency_scale"] == 1.1


def test_best_curve_by_radius_profiles_over_depth_and_source():
    candidates = [
        {
            "params": {"radius_mm": 6.0, "z_mm": 90.0},
            "case_results": {"case": {"misfit": 2.0, "source_profile": {}}},
        },
        {
            "params": {"radius_mm": 6.0, "z_mm": 90.5},
            "case_results": {"case": {"misfit": 1.0, "source_profile": {}}},
        },
        {
            "params": {"radius_mm": 6.2, "z_mm": 90.0},
            "case_results": {"case": {"misfit": 1.5, "source_profile": {}}},
        },
    ]

    curve = best_curve_by_radius(candidates, "case")

    assert curve == [
        {
            "radius_mm": 6.0,
            "misfit": 1.0,
            "params": {"radius_mm": 6.0, "z_mm": 90.5},
            "source_profile": {},
        },
        {
            "radius_mm": 6.2,
            "misfit": 1.5,
            "params": {"radius_mm": 6.2, "z_mm": 90.0},
            "source_profile": {},
        },
    ]
