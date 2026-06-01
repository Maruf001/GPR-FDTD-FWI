"""Tests for joint multi-rebar radius profile helpers."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_multi_rebar_joint_radius_profile import (  # noqa: E402
    checkpoint_prefix_matches_grid,
    radius_tuple_grid,
    read_candidates_csv,
    rank_joint_radius_candidates,
    write_checkpoint_artifacts,
)


def test_radius_tuple_grid_builds_cartesian_radius_search():
    tuples = radius_tuple_grid([5.0, 6.0], count=3)

    assert tuples == [
        (5.0, 5.0, 5.0),
        (5.0, 5.0, 6.0),
        (5.0, 6.0, 5.0),
        (5.0, 6.0, 6.0),
        (6.0, 5.0, 5.0),
        (6.0, 5.0, 6.0),
        (6.0, 6.0, 5.0),
        (6.0, 6.0, 6.0),
    ]


def test_rank_joint_radius_candidates_sorts_by_case_misfit():
    candidates = [
        {
            "radii_mm": [5.0, 6.0, 7.0],
            "case_results": {"case": {"misfit": 2.0, "source_profile": {}}},
        },
        {
            "radii_mm": [5.0, 6.0, 8.0],
            "case_results": {"case": {"misfit": 1.0, "source_profile": {}}},
        },
    ]

    ranked = rank_joint_radius_candidates(candidates, "case")

    assert ranked[0]["radii_mm"] == [5.0, 6.0, 8.0]
    assert ranked[0]["misfit"] == 1.0


def test_write_checkpoint_artifacts_preserves_partial_candidates(tmp_path):
    candidates = [
        {
            "radii_mm": [5.0, 6.0, 8.0],
            "case_results": {
                "case_a": {
                    "misfit": 0.12,
                    "source_profile": {
                        "frequency_scale": 1.0,
                        "time_shift_ps": 0.0,
                        "amplitude_scale": 0.95,
                    },
                },
            },
        },
    ]

    csv_path, metadata_path = write_checkpoint_artifacts(
        tmp_path,
        candidates,
        ["case_a"],
        completed_count=1,
        total_count=3,
        elapsed_time_s=12.5,
    )

    csv_text = csv_path.read_text(encoding="utf-8")
    metadata_text = metadata_path.read_text(encoding="utf-8")

    assert "case_a" in csv_text
    assert "[5.0, 6.0, 8.0]" in csv_text
    assert '"completed_count": 1' in metadata_text
    assert '"total_count": 3' in metadata_text

    loaded = read_candidates_csv(csv_path)
    assert loaded == candidates


def test_checkpoint_prefix_matches_expected_radius_order():
    candidates = [
        {"radii_mm": [5.0, 5.0], "case_results": {}},
        {"radii_mm": [5.0, 6.0], "case_results": {}},
    ]
    radius_tuples = [(5.0, 5.0), (5.0, 6.0), (6.0, 5.0)]

    assert checkpoint_prefix_matches_grid(candidates, radius_tuples)
    assert not checkpoint_prefix_matches_grid(candidates, list(reversed(radius_tuples)))
