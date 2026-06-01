"""Tests for source-profiled polish aggregate reporting."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_source_profiled_polish_aggregate import (  # noqa: E402
    first_noise_seed,
    interval_width,
    run_id_from_path,
    summarize_source_profiled_summary,
)


def _summary():
    return {
        "sources": 9,
        "frequencies_ghz": [1.0, 1.5],
        "frequency_weights": {"1GHz": 0.25, "1.5GHz": 1.0},
        "truth_params": {"radius_mm": 4.0},
        "observed_source": {
            "noise": {
                "1GHz": {"seed": 21},
                "1.5GHz": {"seed": 22},
            },
        },
        "geometry_mode": "subcell",
        "subcell_samples": 9,
        "source_profile_grid": {"fit_amplitude": True},
        "elapsed_time_s": 270.0,
        "margin": {
            "best_radius_mm": 4.0,
            "next_radius_mm": 3.9,
            "radius_margin_abs": 0.0001,
            "radius_margin_rel": 0.001,
        },
        "radius_ambiguity": {
            "exact_tie": {"radius_min_mm": 4.0, "radius_max_mm": 4.0, "radius_count": 1},
            "weak_interval": {"radius_min_mm": 3.7, "radius_max_mm": 4.0, "radius_count": 4},
        },
    }


def test_first_noise_seed_reads_frequency_noise_dict():
    assert first_noise_seed(_summary()) == 21


def test_interval_width_is_non_negative():
    assert interval_width({"radius_min_mm": 4.0, "radius_max_mm": 3.7}) == 0.0
    assert interval_width({"radius_min_mm": 3.7, "radius_max_mm": 4.0}) == pytest.approx(0.3)


def test_run_id_from_path_reads_numbered_grandparent_for_stage_dir():
    path = "outputs/experiments/153_example/stages/guarded_polish"

    assert run_id_from_path(path) == "153"


def test_summarize_source_profiled_summary_flattens_fields():
    row = summarize_source_profiled_summary(_summary(), "outputs/experiments/142_example")

    assert row["run_id"] == "142"
    assert row["noise_seed"] == 21
    assert row["frequencies_ghz"] == "1.0,1.5"
    assert row["frequency_weights"] == "1.5GHz:1.0,1GHz:0.25"
    assert row["fit_amplitude"] is True
    assert row["best_radius_mm"] == 4.0
    assert row["radius_error_mm"] == 0.0
    assert row["weak_interval_width_mm"] == pytest.approx(0.3)
