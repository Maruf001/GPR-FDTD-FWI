"""Tests for material tradeoff runner helpers."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_material_tradeoff import (  # noqa: E402
    best_curve_by_radius,
    parse_log10_sigma_values,
)


def test_parse_log10_sigma_values_converts_to_sigma():
    values = parse_log10_sigma_values("5,7")

    assert values == [1e5, 1e7]


def test_best_curve_by_radius_profiles_over_materials():
    candidates = [
        {"misfit": 2.0, "params": {"radius_mm": 6.0}, "material": {"concrete_epsr": 5.5}},
        {"misfit": 1.0, "params": {"radius_mm": 6.0}, "material": {"concrete_epsr": 6.0}},
        {"misfit": 1.5, "params": {"radius_mm": 6.2}, "material": {"concrete_epsr": 6.0}},
    ]

    curve = best_curve_by_radius(candidates)

    assert curve == [
        {"misfit": 1.0, "params": {"radius_mm": 6.0}, "material": {"concrete_epsr": 6.0}},
        {"misfit": 1.5, "params": {"radius_mm": 6.2}, "material": {"concrete_epsr": 6.0}},
    ]


def test_parse_log10_sigma_values_rejects_empty():
    with pytest.raises(Exception):
        parse_log10_sigma_values("")
