"""Tests for multi-rebar coordinate-search helpers."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.multi_rebar_coordinate import (  # noqa: E402
    CoordinateState,
    choose_case_label,
    interval_offsets,
    is_weak_high_radius_branch,
    offset_window,
    revisit_radius_offsets_from_row,
    step_report,
    target_window,
    update_state_from_candidate,
    weak_high_radius_revisit_targets,
)


def test_coordinate_state_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="same length"):
        CoordinateState.from_lists([150.0], [90.0, 90.0], [6.0])


def test_offset_window_returns_sorted_unique_values():
    values = offset_window(250.0, [1.0, 0.0, -1.0, 1.0])

    assert values == [249.0, 250.0, 251.0]


def test_target_window_uses_current_state_center():
    state = CoordinateState.from_lists(
        [150.0, 249.0, 350.0],
        [90.0, 91.0, 90.0],
        [6.0, 6.4, 6.0],
    )

    window = target_window(state, 1, [-1.0, 0.0, 1.0], [-2.0, 0.0], [-0.2, 0.0])

    assert window == {
        "target_index": 1,
        "x_values_mm": [248.0, 249.0, 250.0],
        "z_values_mm": [89.0, 91.0],
        "radius_values_mm": [6.2, 6.4],
    }


def test_update_state_from_candidate_updates_only_target():
    state = CoordinateState.from_lists(
        [150.0, 249.0, 350.0],
        [90.0, 91.0, 90.0],
        [6.0, 6.4, 6.0],
    )

    updated = update_state_from_candidate(
        state,
        {"target_index": 1, "x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
    )

    assert updated.x_values_mm == (150.0, 250.0, 350.0)
    assert updated.z_values_mm == (90.0, 90.0, 90.0)
    assert updated.radii_mm == (6.0, 6.0, 6.0)


def test_choose_case_label_defaults_or_validates_preference():
    assert choose_case_label(["nominal", "mismatch"]) == "nominal"
    assert choose_case_label(["nominal", "mismatch"], "mismatch") == "mismatch"

    with pytest.raises(ValueError, match="not found"):
        choose_case_label(["nominal"], "missing")


def test_step_report_serializes_state_transition():
    before = CoordinateState.from_lists([150.0], [91.0], [6.8])
    after = CoordinateState.from_lists([150.0], [90.0], [6.0])
    result = {
        "top_candidates": [
            {"misfit": 0.1, "params": {"target_index": 0, "x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0}}
        ],
        "margin": {"best_radius_mm": 6.0, "radius_margin_abs": 0.01},
    }

    report = step_report(0, 0, "nominal", before, after, result)

    assert report["state_before"]["z_values_mm"] == [91.0]
    assert report["state_after"]["radii_mm"] == [6.0]
    assert report["margin"]["best_radius_mm"] == 6.0


def test_is_weak_high_radius_branch_detects_ambiguous_high_endpoint():
    row = {
        "fallback_warning": "radius_weak_confidence",
        "best_radius_mm": 6.8,
        "ambiguity_radius_min_mm": 6.0,
        "ambiguity_radius_max_mm": 6.8,
    }

    assert is_weak_high_radius_branch(row) is True

    row["best_radius_mm"] = 6.0
    assert is_weak_high_radius_branch(row) is False

    row["fallback_warning"] = ""
    row["best_radius_mm"] = 6.8
    assert is_weak_high_radius_branch(row) is False


def test_weak_high_radius_revisit_targets_filters_by_case_and_target_once():
    rows = [
        {
            "case_label": "noise",
            "step_target_index": 0,
            "fallback_warning": "radius_weak_confidence",
            "best_radius_mm": 6.8,
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.8,
        },
        {
            "case_label": "noise",
            "step_target_index": 0,
            "fallback_warning": "radius_weak_confidence",
            "best_radius_mm": 6.8,
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.8,
        },
        {
            "case_label": "other",
            "step_target_index": 1,
            "fallback_warning": "radius_weak_confidence",
            "best_radius_mm": 6.8,
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.8,
        },
    ]

    assert weak_high_radius_revisit_targets(rows, "noise") == [0]


def test_interval_offsets_cover_interval_relative_to_center():
    assert interval_offsets(6.8, 6.0, 6.8, 0.2) == [-0.8, -0.6, -0.4, -0.2, 0.0]

    with pytest.raises(ValueError, match="positive"):
        interval_offsets(6.8, 6.0, 6.8, 0.0)


def test_revisit_radius_offsets_from_row_uses_ambiguity_interval():
    row = {
        "ambiguity_radius_min_mm": 6.0,
        "ambiguity_radius_max_mm": 6.8,
    }

    assert revisit_radius_offsets_from_row(row, 6.8, step_mm=0.2) == [
        -0.8,
        -0.6,
        -0.4,
        -0.2,
        0.0,
    ]
