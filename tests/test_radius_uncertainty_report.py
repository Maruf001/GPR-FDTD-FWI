"""Tests for radius uncertainty reporting helpers."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_radius_uncertainty_report import (  # noqa: E402
    interval_width,
    summarize_case,
    summarize_material,
    summarize_nominal,
)


def test_interval_width_returns_nonnegative_width():
    assert interval_width({"radius_min_mm": 4.1, "radius_max_mm": 4.0}) == 0.0
    assert interval_width({"radius_min_mm": 3.9, "radius_max_mm": 4.1}) == pytest.approx(0.2)


def test_summarize_nominal_accepts_source_profiled_summary():
    summary = {
        "truth_params": {"radius_mm": 4.0},
        "margin": {"best_radius_mm": 4.0, "radius_margin_abs": 0.002, "radius_margin_rel": 0.01},
        "radius_ambiguity": {
            "weak_interval": {
                "radius_min_mm": 3.95,
                "radius_max_mm": 4.05,
                "radius_count": 3,
            }
        },
        "top_candidates": [
            {
                "params": {"radius_mm": 4.0},
                "source_profile": {
                    "frequency_scale": 1.1,
                    "time_shift_ps": -50.0,
                    "amplitude_scale": 1.08,
                },
            }
        ],
    }

    row = summarize_nominal(summary)

    assert row["stage"] == "source_profiled_polish"
    assert row["truth_radius_mm"] == 4.0
    assert row["best_radius_mm"] == 4.0
    assert row["weak_width_mm"] == pytest.approx(0.1)


def test_summarize_nominal_accepts_two_stage_summary():
    summary = {
        "truth": {"radius_mm": 8.0},
        "final_stage": "highband_polish",
        "final_best": {
            "params": {"radius_mm": 8.0},
            "source_profile": {"frequency_scale": 1.1},
        },
        "final_margin": {"best_radius_mm": 8.0, "radius_margin_abs": 0.003},
        "final_radius_ambiguity": {
            "weak_interval": {
                "radius_min_mm": 8.0,
                "radius_max_mm": 8.0,
                "radius_count": 1,
            }
        },
    }

    row = summarize_nominal(summary)

    assert row["stage"] == "highband_polish"
    assert row["best_radius_mm"] == 8.0
    assert row["weak_count"] == 1


def test_summarize_material_extracts_nuisance_fields():
    summary = {
        "margin": {"best_radius_mm": 4.05, "radius_margin_abs": 0.0001},
        "radius_ambiguity": {
            "weak_interval": {
                "radius_min_mm": 3.95,
                "radius_max_mm": 4.1,
                "radius_count": 4,
            }
        },
        "top_candidates": [
            {
                "params": {"radius_mm": 4.05},
                "material": {"concrete_epsr": 6.0, "rebar_log10_sigma": 6.0},
                "source_profile": {
                    "frequency_scale": 1.1,
                    "time_shift_ps": -50.0,
                    "amplitude_scale": 1.08,
                },
            }
        ],
    }

    row = summarize_material(summary)

    assert row["best_radius_mm"] == 4.05
    assert row["concrete_epsr"] == 6.0
    assert row["rebar_log10_sigma"] == 6.0


def test_summarize_case_reports_material_shift():
    nominal = {
        "truth_params": {"radius_mm": 4.0},
        "margin": {"best_radius_mm": 4.0, "radius_margin_abs": 0.002},
        "radius_ambiguity": {
            "weak_interval": {
                "radius_min_mm": 4.0,
                "radius_max_mm": 4.0,
                "radius_count": 1,
            }
        },
        "top_candidates": [{"params": {"radius_mm": 4.0}, "source_profile": {}}],
    }
    material = {
        "margin": {"best_radius_mm": 4.05, "radius_margin_abs": 0.0001},
        "radius_ambiguity": {
            "weak_interval": {
                "radius_min_mm": 3.95,
                "radius_max_mm": 4.1,
                "radius_count": 4,
            }
        },
        "top_candidates": [
            {
                "params": {"radius_mm": 4.05},
                "material": {"concrete_epsr": 6.0, "rebar_log10_sigma": 6.0},
                "source_profile": {},
            }
        ],
    }

    row = summarize_case("r4", nominal, material)

    assert row["material_minus_nominal_best_mm"] == pytest.approx(0.05)
    assert row["material_interval_extra_width_mm"] == pytest.approx(0.15)
