"""Tests for single-rebar experiment summary helpers."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.single_rebar_result_summary import (  # noqa: E402
    distinct_radius_margin,
    experiment_label,
    summarize_single_rebar_summary,
)


def test_distinct_radius_margin_skips_duplicate_best_radius():
    candidates = [
        {"misfit": 0.10, "params": {"radius_mm": 6.0}},
        {"misfit": 0.10, "params": {"radius_mm": 6.0}},
        {"misfit": 0.13, "params": {"radius_mm": 6.2}},
    ]

    margin = distinct_radius_margin(candidates)

    assert margin["best_radius_mm"] == 6.0
    assert margin["next_radius_mm"] == 6.2
    assert abs(margin["radius_margin_abs"] - 0.03) < 1e-12
    assert abs(margin["radius_margin_rel"] - 0.3) < 1e-12


def test_experiment_label_finds_numbered_parent():
    label = experiment_label("outputs/experiments/037_example/data/single_rebar_summary.json")

    assert label == "037_example"


def test_summarize_single_rebar_summary_flattens_key_metrics(tmp_path):
    path = tmp_path / "outputs" / "experiments" / "099_case" / "data" / "single_rebar_summary.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        """
{
  "backend": "gpu-cpml",
  "optimizer": "powell",
  "frequencies_ghz": [1.5],
  "observed_noise": {"rms_fraction": 0.05, "seed": 13},
  "grid_polish": {
    "evaluations": 40,
    "top_candidates": [
      {"misfit": 0.10, "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0}},
      {"misfit": 0.12, "params": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.2}}
    ]
  },
  "elapsed_time_s": 12.5,
  "best_misfit": 0.10,
  "nrms_data_by_frequency": {"1.5GHz": 0.05},
  "nrms_model": 0.0,
  "recovered": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
  "optimizer_final": {"x_mm": 249.5, "z_mm": 90.5, "radius_mm": 7.0},
  "true": {"x_mm": 250.0, "z_mm": 90.0, "radius_mm": 6.0},
  "trace_shift_by_frequency": {"1.5GHz": {"nrccc_fraction_lt_half_period": 1.0, "max_rccc": 0.003}}
}
""",
        encoding="utf-8",
    )

    row = summarize_single_rebar_summary(path)

    assert row["experiment"] == "099_case"
    assert row["noise_fraction"] == 0.05
    assert row["grid_polish_enabled"] is True
    assert row["x_error_mm"] == 0.0
    assert row["radius_error_mm"] == 0.0
    assert row["optimizer_radius_mm"] == 7.0
    assert row["best_radius_mm"] == 6.0
    assert row["next_radius_mm"] == 6.2
    assert row["nrccc_primary"] == 1.0
