"""Tests for W2 landscape runner helpers."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_w2_landscape import (  # noqa: E402
    best_curve_by_radius,
    rank_by_objective,
)


def test_rank_by_objective_sorts_and_preserves_scores():
    candidates = [
        {"params": {"radius_mm": 6.2}, "ls_misfit": 2.0, "w2_misfit": 0.1},
        {"params": {"radius_mm": 6.0}, "ls_misfit": 1.0, "w2_misfit": 0.2},
    ]

    ranked = rank_by_objective(candidates, "ls_misfit")

    assert ranked[0]["params"]["radius_mm"] == 6.0
    assert ranked[0]["misfit"] == 1.0
    assert ranked[0]["w2_misfit"] == 0.2


def test_best_curve_by_radius_minimizes_over_other_parameters():
    candidates = [
        {"params": {"radius_mm": 6.0, "z_mm": 90.0}, "ls_misfit": 2.0, "w2_misfit": 0.2},
        {"params": {"radius_mm": 6.0, "z_mm": 90.5}, "ls_misfit": 1.0, "w2_misfit": 0.3},
        {"params": {"radius_mm": 6.2, "z_mm": 90.0}, "ls_misfit": 1.5, "w2_misfit": 0.1},
    ]

    curve = best_curve_by_radius(candidates, "ls_misfit")

    assert curve == [
        {"radius_mm": 6.0, "misfit": 1.0, "params": {"radius_mm": 6.0, "z_mm": 90.5}},
        {"radius_mm": 6.2, "misfit": 1.5, "params": {"radius_mm": 6.2, "z_mm": 90.0}},
    ]
