"""Tests for the multi-rebar coordinate optimizer runner helpers."""

import argparse
import csv
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_multi_rebar_coordinate_optimizer import (  # noqa: E402
    confidence_rows_for_step,
    is_broad_radius_ambiguity,
    latest_broad_radius_revisit_rows,
    latest_high_radius_revisit_rows,
    merge_revisit_rows,
    objective_diagnostic_rows_for_step,
    objective_top_candidate_rows_for_step,
    parse_target_indices,
    parse_vector_mm,
    results_from_candidates,
    truth_radius_values_for_run,
    write_coordinate_figure_notes,
    write_objective_top_candidate_csv,
)


def test_parse_vector_mm_preserves_duplicates_and_order():
    assert parse_vector_mm("90,90,89") == [90.0, 90.0, 89.0]
    assert parse_vector_mm("5.8:6.2:0.2,6.0") == [5.8, 6.0, 6.2, 6.0]


def test_parse_vector_mm_rejects_empty_vector():
    with pytest.raises(argparse.ArgumentTypeError, match="at least one"):
        parse_vector_mm("")


def test_parse_target_indices_rejects_negative_values():
    assert parse_target_indices("0,2") == [0, 2]

    with pytest.raises(argparse.ArgumentTypeError, match="non-negative"):
        parse_target_indices("0,-1")


def test_truth_radius_values_for_run_defaults_to_common_radius():
    radii = truth_radius_values_for_run(6.0, None, target_count=3)

    assert radii == [6.0, 6.0, 6.0]


def test_truth_radius_values_for_run_accepts_per_target_radii():
    radii = truth_radius_values_for_run(6.0, [5.0, 6.0, 8.0], target_count=3)

    assert radii == [5.0, 6.0, 8.0]


def test_truth_radius_values_for_run_rejects_wrong_length():
    with pytest.raises(ValueError, match="truth radius"):
        truth_radius_values_for_run(6.0, [5.0, 6.0], target_count=3)


def test_results_from_candidates_builds_ranked_case_results():
    candidates = [
        {
            "params": {"target_index": 0, "x_mm": 149.0, "z_mm": 90.0, "radius_mm": 6.2},
            "case_results": {"nominal": {"misfit": 2.0, "source_profile": {}}},
        },
        {
            "params": {"target_index": 0, "x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {"nominal": {"misfit": 1.0, "source_profile": {}}},
        },
    ]

    results = results_from_candidates(candidates, ["nominal"], top_k=1)

    assert results["nominal"]["top_candidates"][0]["params"]["x_mm"] == 150.0
    assert results["nominal"]["margin"]["best_radius_mm"] == 6.0


def test_confidence_rows_for_step_adds_coordinate_metadata():
    results = {
        "nominal": {
            "top_candidates": [
                {
                    "misfit": 1.0,
                    "params": {
                        "target_index": 1,
                        "x_mm": 250.0,
                        "z_mm": 90.0,
                        "radius_mm": 6.0,
                    },
                    "source_profile": {},
                },
                {
                    "misfit": 1.0001,
                    "params": {
                        "target_index": 1,
                        "x_mm": 250.0,
                        "z_mm": 90.0,
                        "radius_mm": 6.2,
                    },
                    "source_profile": {},
                }
            ],
            "margin": {
                "best_radius_mm": 6.0,
                "second_best_radius_mm": 6.2,
                "radius_margin_abs": 1.0e-4,
                "radius_margin_rel": 1.0e-4,
            },
            "best_curve_by_radius": [
                {
                    "radius_mm": 6.0,
                    "misfit": 1.0,
                    "params": {
                        "target_index": 1,
                        "x_mm": 250.0,
                        "z_mm": 90.0,
                        "radius_mm": 6.0,
                    },
                }
            ],
        }
    }

    rows = confidence_rows_for_step(
        "unit",
        pass_index=2,
        target_index=1,
        update_case_label="nominal",
        results=results,
        meta={"backend": "cpu", "grid_step_mm": 10.0},
    )

    assert rows[0]["pass_index"] == 2
    assert rows[0]["step_target_index"] == 1
    assert rows[0]["update_case_label"] == "nominal"
    assert rows[0]["step_kind"] == "main"
    assert rows[0]["confidence_label"] == "weak"


def test_objective_diagnostic_rows_for_step_flattens_variants():
    objective_results = {
        "nominal": {
            "base": {
                "top_candidates": [
                    {
                        "misfit": 1.0,
                        "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
                        "source_profile": {
                            "frequency_scale": 1.0,
                            "time_shift_ps": 0.0,
                            "amplitude_scale": 1.0,
                        },
                    }
                ],
                "margin": {
                    "best_radius_mm": 6.0,
                    "next_radius_mm": 6.2,
                    "radius_margin_abs": 0.1,
                    "radius_margin_rel": 0.01,
                    "best_radius_misfit": 1.0,
                },
            },
            "highband": {
                "top_candidates": [
                    {
                        "misfit": 0.2,
                        "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
                        "source_profile": {
                            "frequency_scale": 1.0,
                            "time_shift_ps": 0.0,
                            "amplitude_scale": 1.0,
                        },
                    }
                ],
                "margin": {
                    "best_radius_mm": 6.0,
                    "next_radius_mm": 6.2,
                    "radius_margin_abs": 0.3,
                    "radius_margin_rel": 1.5,
                    "best_radius_misfit": 0.2,
                },
            },
        }
    }

    rows = objective_diagnostic_rows_for_step(
        "unit",
        pass_index=0,
        target_index=2,
        update_case_label="nominal",
        objective_results=objective_results,
        meta={
            "backend": "cpu",
            "grid_step_mm": 1.0,
            "target_rebar_index": 2,
            "candidate_count": 9,
            "case_count": 1,
        },
    )

    assert [row["objective_label"] for row in rows] == ["base", "highband"]
    assert rows[1]["step_target_index"] == 2
    assert rows[1]["best_radius_mm"] == 6.0
    assert rows[1]["radius_margin_abs"] == 0.3


def test_objective_top_candidate_rows_for_step_flattens_ranked_variants(tmp_path):
    objective_results = {
        "nominal": {
            "base": {
                "top_candidates": [
                    {
                        "misfit": 1.0,
                        "params": {
                            "target_index": 2,
                            "x_mm": 300.0,
                            "z_mm": 90.0,
                            "radius_mm": 8.0,
                            "x_values_mm": [190.0, 250.0, 300.0],
                            "z_values_mm": [90.0, 90.0, 90.0],
                            "radii_mm": [6.0, 6.0, 8.0],
                        },
                        "source_profile": {
                            "frequency_scale": 1.0,
                            "time_shift_ps": 0.0,
                            "amplitude_scale": 1.0,
                        },
                    },
                    {
                        "misfit": 1.02,
                        "params": {
                            "target_index": 2,
                            "x_mm": 299.0,
                            "z_mm": 90.0,
                            "radius_mm": 8.0,
                        },
                        "source_profile": {
                            "frequency_scale": 0.9,
                            "time_shift_ps": 25.0,
                            "amplitude_scale": 0.98,
                        },
                    },
                ],
            },
            "highband": {
                "top_candidates": [
                    {
                        "misfit": 0.4,
                        "params": {
                            "target_index": 2,
                            "x_mm": 300.0,
                            "z_mm": 90.0,
                            "radius_mm": 8.0,
                        },
                        "source_profile": {
                            "frequency_scale": 1.1,
                            "time_shift_ps": -25.0,
                            "amplitude_scale": 1.02,
                        },
                    }
                ],
            },
        }
    }

    rows = objective_top_candidate_rows_for_step(
        "unit",
        pass_index=1,
        target_index=2,
        update_case_label="nominal",
        objective_results=objective_results,
        meta={
            "backend": "cpu",
            "grid_step_mm": 1.0,
            "target_rebar_index": 2,
            "candidate_count": 27,
            "case_count": 1,
        },
    )

    assert [(row["objective_label"], row["rank"]) for row in rows] == [
        ("base", 1),
        ("base", 2),
        ("highband", 1),
    ]
    assert rows[0]["x_values_mm"] == "[190.0, 250.0, 300.0]"
    assert rows[1]["x_mm"] == 299.0
    assert rows[2]["source_frequency_scale"] == 1.1

    path = tmp_path / "objective_top_candidates.csv"
    write_objective_top_candidate_csv(path, rows)

    with path.open("r", encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    assert written[0]["objective_label"] == "base"
    assert written[1]["rank"] == "2"
    assert written[1]["x_mm"] == "299.0"


def test_latest_high_radius_revisit_rows_uses_latest_update_case_rows():
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
            "fallback_warning": "",
            "best_radius_mm": 6.0,
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.0,
        },
        {
            "case_label": "noise",
            "step_target_index": 2,
            "fallback_warning": "radius_weak_confidence",
            "best_radius_mm": 6.6,
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.6,
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

    revisit_rows = latest_high_radius_revisit_rows(rows, "noise")

    assert [row["step_target_index"] for row in revisit_rows] == [2]


def test_broad_radius_ambiguity_includes_moderate_wide_intervals():
    row = {
        "confidence_label": "moderate",
        "ambiguity_radius_min_mm": 5.4,
        "ambiguity_radius_max_mm": 6.0,
    }

    assert is_broad_radius_ambiguity(row, min_width_mm=0.2)


def test_latest_broad_radius_revisit_rows_uses_latest_update_case_rows():
    rows = [
        {
            "case_label": "noise",
            "step_target_index": 1,
            "confidence_label": "moderate",
            "ambiguity_radius_min_mm": 5.4,
            "ambiguity_radius_max_mm": 6.0,
        },
        {
            "case_label": "noise",
            "step_target_index": 1,
            "confidence_label": "strong",
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.0,
        },
        {
            "case_label": "noise",
            "step_target_index": 2,
            "confidence_label": "weak",
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.8,
        },
        {
            "case_label": "other",
            "step_target_index": 0,
            "confidence_label": "moderate",
            "ambiguity_radius_min_mm": 5.8,
            "ambiguity_radius_max_mm": 6.2,
        },
    ]

    revisit_rows = latest_broad_radius_revisit_rows(rows, "noise", min_width_mm=0.2)

    assert [row["step_target_index"] for row in revisit_rows] == [2]


def test_merge_revisit_rows_deduplicates_targets_preserving_first_group():
    high_rows = [{"step_target_index": 2}, {"step_target_index": 0}]
    broad_rows = [{"step_target_index": 1}, {"step_target_index": 2}]

    rows = merge_revisit_rows(high_rows, broad_rows)

    assert [row["step_target_index"] for row in rows] == [2, 0, 1]


def test_write_coordinate_figure_notes_describes_weak_update_rows(tmp_path):
    rows = [
        {
            "case_label": "noise",
            "update_case_label": "noise",
            "confidence_label": "weak",
            "step_target_index": 0,
            "best_radius_mm": 6.8,
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.8,
        },
        {
            "case_label": "source_mismatch",
            "update_case_label": "noise",
            "confidence_label": "strong",
            "step_target_index": 0,
            "best_radius_mm": 6.0,
            "ambiguity_radius_min_mm": 6.0,
            "ambiguity_radius_max_mm": 6.0,
        },
    ]

    notes_path = tmp_path / "FIGURE_NOTES.md"
    write_coordinate_figure_notes(notes_path, rows)

    text = notes_path.read_text(encoding="utf-8")
    assert "coordinate_confidence_margins.png" in text
    assert "Rows in this run: 2" in text
    assert "weak=1" in text
    assert "target 0 best r=6.8 mm" in text
    assert "target 0 r=6.8 mm interval=6-6.8 mm" in text
