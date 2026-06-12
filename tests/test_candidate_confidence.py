"""Tests for candidate confidence reporting helpers."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.candidate_confidence import (  # noqa: E402
    ConfidenceThresholds,
    ambiguity_interval,
    confidence_label,
    first_competing_geometry,
    load_profile_confidence_rows,
    summarize_case_confidence,
)


def test_confidence_label_uses_abs_and_relative_thresholds():
    thresholds = ConfidenceThresholds(
        moderate_abs=5.0e-4,
        moderate_rel=5.0e-3,
        strong_abs=1.0e-3,
        strong_rel=1.0e-2,
    )

    assert confidence_label(None, 0.1, thresholds) == "missing"
    assert confidence_label(float("nan"), 0.1, thresholds) == "missing"
    assert confidence_label(0.1, float("inf"), thresholds) == "missing"
    assert confidence_label("bad", 0.1, thresholds) == "missing"
    assert confidence_label(0.0, 0.1, thresholds) == "ambiguous"
    assert confidence_label(2.0e-4, 2.0e-3, thresholds) == "weak"
    assert confidence_label(5.0e-4, 5.0e-3, thresholds) == "moderate"
    assert confidence_label(1.0e-3, 1.0e-2, thresholds) == "strong"


def test_first_competing_geometry_skips_same_xz_radius_neighbor():
    top_candidates = [
        {"misfit": 1.0, "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0}},
        {"misfit": 1.1, "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.2}},
        {"misfit": 1.2, "params": {"x_mm": 150.0, "z_mm": 91.0, "radius_mm": 6.8}},
    ]

    competing = first_competing_geometry(top_candidates)

    assert competing["params"]["z_mm"] == 91.0
    assert competing["params"]["radius_mm"] == 6.8


def test_ambiguity_interval_includes_near_deeper_radius_branch():
    top_candidates = [
        {"misfit": 0.0800, "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0}},
        {"misfit": 0.0803, "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.2}},
        {"misfit": 0.0810, "params": {"x_mm": 250.0, "z_mm": 91.0, "radius_mm": 6.8}},
        {"misfit": 0.0830, "params": {"x_mm": 251.0, "z_mm": 92.0, "radius_mm": 7.4}},
    ]

    interval = ambiguity_interval(top_candidates)

    assert interval["ambiguity_candidate_count"] == 3
    assert interval["ambiguity_x_min_mm"] == 250.0
    assert interval["ambiguity_x_max_mm"] == 250.0
    assert interval["ambiguity_z_min_mm"] == 90.0
    assert interval["ambiguity_z_max_mm"] == 91.0
    assert interval["ambiguity_radius_min_mm"] == 6.0
    assert interval["ambiguity_radius_max_mm"] == 6.8


def test_ambiguity_interval_ignores_nonfinite_misfits():
    top_candidates = [
        {"misfit": "nan", "params": {"x_mm": 249.0, "z_mm": 89.0, "radius_mm": 5.8}},
        {"misfit": 0.0800, "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0}},
        {"misfit": "inf", "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.2}},
        {"misfit": 0.0803, "params": {"x_mm": 250.0, "z_mm": 91.0, "radius_mm": 6.8}},
    ]

    interval = ambiguity_interval(top_candidates)

    assert interval["ambiguity_candidate_count"] == 2
    assert interval["ambiguity_x_min_mm"] == 250.0
    assert interval["ambiguity_x_max_mm"] == 250.0
    assert interval["ambiguity_z_min_mm"] == 90.0
    assert interval["ambiguity_z_max_mm"] == 91.0
    assert interval["ambiguity_radius_min_mm"] == 6.0
    assert interval["ambiguity_radius_max_mm"] == 6.8


def test_summarize_case_confidence_flattens_source_and_competitor():
    result = {
        "margin": {
            "best_radius_mm": 6.0,
            "best_radius_misfit": 0.080,
            "next_radius_mm": 6.2,
            "next_radius_misfit": 0.0806,
            "radius_margin_abs": 6.0e-4,
            "radius_margin_rel": 7.5e-3,
        },
        "top_candidates": [
            {
                "misfit": 0.080,
                "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
                "source_profile": {
                    "frequency_scale": 1.1,
                    "time_shift_ps": -50.0,
                    "amplitude_scale": 1.099,
                    "ringdown_scale": 0.25,
                    "ringdown_delay_ps": 180.0,
                    "ringdown_frequency_scale": 0.8,
                    "primary_coefficient": 1.099,
                    "ringdown_coefficient": 0.27475,
                },
            },
            {
                "misfit": 0.0806,
                "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.2},
                "source_profile": {},
            },
            {
                "misfit": 0.081,
                "params": {"x_mm": 250.0, "z_mm": 91.0, "radius_mm": 6.8},
                "source_profile": {},
            },
        ],
    }

    row = summarize_case_confidence(
        "run",
        "case",
        result,
        {"backend": "gpu-cpml", "target_rebar_index": 1},
    )

    assert row["confidence_label"] == "moderate"
    assert row["fallback_warning"] == ""
    assert row["best_x_mm"] == 250.0
    assert row["next_radius_mm"] == 6.2
    assert row["competing_geometry_z_mm"] == 91.0
    assert row["source_frequency_scale"] == 1.1
    assert row["source_time_shift_ps"] == -50.0
    assert row["source_ringdown_scale"] == 0.25
    assert row["source_ringdown_delay_ps"] == 180.0
    assert row["source_ringdown_coefficient"] == 0.27475
    assert row["ambiguity_radius_max_mm"] == 6.8


def test_summarize_case_confidence_marks_nonfinite_margins_missing():
    result = {
        "margin": {
            "best_radius_mm": 6.0,
            "radius_margin_abs": "nan",
            "radius_margin_rel": "inf",
        },
        "top_candidates": [
            {
                "misfit": "nan",
                "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
            }
        ],
    }

    row = summarize_case_confidence("run", "case", result)

    assert row["confidence_label"] == "missing"
    assert row["fallback_warning"] == ""
    assert row["ambiguity_candidate_count"] == 0
    assert row["ambiguity_misfit_threshold"] is None


def test_summarize_case_confidence_nulls_nonfinite_numeric_fields():
    result = {
        "margin": {
            "best_radius_mm": float("nan"),
            "best_radius_misfit": float("inf"),
            "next_radius_mm": "bad",
            "next_radius_misfit": float("nan"),
            "radius_margin_abs": float("nan"),
            "radius_margin_rel": float("inf"),
        },
        "top_candidates": [
            {
                "misfit": float("nan"),
                "params": {
                    "x_mm": float("nan"),
                    "z_mm": "bad",
                    "radius_mm": float("inf"),
                },
                "source_profile": {
                    "frequency_scale": float("nan"),
                    "time_shift_ps": "bad",
                    "amplitude_scale": float("inf"),
                },
            },
            {
                "misfit": 0.08,
                "params": {"x_mm": 251.0, "z_mm": 91.0, "radius_mm": 6.8},
            },
        ],
    }

    row = summarize_case_confidence("run", "case", result)

    assert row["best_x_mm"] is None
    assert row["best_z_mm"] is None
    assert row["best_radius_mm"] is None
    assert row["next_radius_mm"] is None
    assert row["radius_margin_abs"] is None
    assert row["radius_margin_rel"] is None
    assert row["best_misfit"] is None
    assert row["next_radius_misfit"] is None
    assert row["source_frequency_scale"] is None
    assert row["source_time_shift_ps"] is None
    assert row["source_amplitude_scale"] is None
    assert row["competing_geometry_x_mm"] is None
    assert row["competing_geometry_z_mm"] is None
    assert row["competing_geometry_radius_mm"] is None


def test_summarize_case_confidence_nulls_nonfinite_metadata():
    result = {
        "margin": {
            "best_radius_mm": 6.0,
            "radius_margin_abs": 0.001,
            "radius_margin_rel": 0.01,
        },
        "top_candidates": [
            {
                "misfit": 0.08,
                "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
            },
        ],
    }
    row = summarize_case_confidence(
        "run",
        "case",
        result,
        {
            "backend": "cpu",
            "grid_step_mm": float("nan"),
            "target_rebar_index": float("inf"),
            "candidate_count": "bad",
            "case_count": 4.0,
        },
    )

    assert row["backend"] == "cpu"
    assert row["grid_step_mm"] is None
    assert row["target_rebar_index"] is None
    assert row["candidate_count"] is None
    assert row["case_count"] == 4
    json.dumps(row, allow_nan=False)


def test_load_profile_confidence_rows_reads_profile_summary(tmp_path):
    path = tmp_path / "summary.json"
    path.write_text(
        json.dumps({
            "run_name": "profile_run",
            "backend": "gpu-cpml",
            "grid_step_mm": 1.0,
            "target_rebar_index": 2,
            "candidate_count": 325,
            "case_count": 1,
            "results": {
                "noise": {
                    "margin": {
                        "best_radius_mm": 6.0,
                        "best_radius_misfit": 0.08,
                        "next_radius_mm": 6.2,
                        "next_radius_misfit": 0.0802,
                        "radius_margin_abs": 2.0e-4,
                        "radius_margin_rel": 2.5e-3,
                    },
                    "top_candidates": [
                        {
                            "misfit": 0.08,
                            "params": {"x_mm": 350.0, "z_mm": 90.0, "radius_mm": 6.0},
                            "source_profile": {"frequency_scale": 1.0},
                        }
                    ],
                }
            },
        }),
        encoding="utf-8",
    )

    rows = load_profile_confidence_rows(path)

    assert len(rows) == 1
    assert rows[0]["run_name"] == "profile_run"
    assert rows[0]["target_rebar_index"] == 2
    assert rows[0]["confidence_label"] == "weak"
    assert rows[0]["fallback_warning"] == "radius_weak_confidence"
    assert rows[0]["summary_path"] == str(path)
