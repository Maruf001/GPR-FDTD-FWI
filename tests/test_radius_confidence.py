"""Tests for radius ambiguity interval helpers."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.radius_confidence import radius_interval_from_curve  # noqa: E402


def test_radius_interval_reports_exact_ties():
    curve = [
        {"misfit": 1.0, "params": {"radius_mm": 3.9}},
        {"misfit": 0.9, "params": {"radius_mm": 4.0}},
        {"misfit": 0.9, "params": {"radius_mm": 4.1}},
        {"misfit": 1.2, "params": {"radius_mm": 4.2}},
    ]

    interval = radius_interval_from_curve(curve, abs_tolerance=0.0, rel_tolerance=0.0)

    assert interval["radius_min_mm"] == 4.0
    assert interval["radius_max_mm"] == 4.1
    assert interval["radius_count"] == 2


def test_radius_interval_uses_absolute_or_relative_tolerance():
    curve = [
        {"misfit": 10.0, "params": {"radius_mm": 4.0}},
        {"misfit": 10.04, "params": {"radius_mm": 4.1}},
        {"misfit": 10.2, "params": {"radius_mm": 4.2}},
    ]

    interval = radius_interval_from_curve(curve, abs_tolerance=0.01, rel_tolerance=0.005)

    assert interval["objective_tolerance"] == 0.05
    assert interval["radii_mm"] == [4.0, 4.1]


def test_radius_interval_rejects_empty_curve():
    with pytest.raises(ValueError, match="at least one"):
        radius_interval_from_curve([])
