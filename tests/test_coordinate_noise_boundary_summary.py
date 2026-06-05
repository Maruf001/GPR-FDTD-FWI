"""Tests for coordinate noise-boundary summaries."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_coordinate_noise_boundary_summary import (  # noqa: E402
    build_boundary_row,
    parse_noise_seed,
    summarize_boundary,
)


def _confidence_row(case_label, x_width, margin_to_cutoff, source_mismatch=False):
    best = 0.1 if not source_mismatch else 0.14
    threshold = best + 0.015
    competing = threshold + margin_to_cutoff
    return {
        "case_label": case_label,
        "step_kind": "main",
        "step_target_index": 2,
        "candidate_count": 105,
        "best_x_mm": 264.0,
        "best_z_mm": 90.0,
        "best_radius_mm": 8.0,
        "confidence_label": "strong",
        "fallback_warning": "",
        "radius_margin_abs": 0.002,
        "radius_margin_rel": 0.02,
        "best_misfit": best,
        "competing_geometry_x_mm": 263.0,
        "competing_geometry_z_mm": 90.0,
        "competing_geometry_radius_mm": 8.0,
        "competing_geometry_misfit": competing,
        "ambiguity_misfit_threshold": threshold,
        "ambiguity_candidate_count": 1 if x_width == 0.0 else 2,
        "ambiguity_x_min_mm": 264.0 - x_width,
        "ambiguity_x_max_mm": 264.0,
        "ambiguity_z_min_mm": 90.0,
        "ambiguity_z_max_mm": 90.0,
        "ambiguity_radius_min_mm": 8.0,
        "ambiguity_radius_max_mm": 8.0,
    }


def _summary(noise="19p642333984375", nominal_x_width=0.0, nominal_margin_to_cutoff=4.0e-9):
    nominal = f"noise{noise}_seed34"
    mismatch = f"source_mismatch_noise{noise}_seed34"
    return {
        "run_name": f"coordinate_optimizer_noise{noise}",
        "sources": 4,
        "tx_rx_offset_mm": 50.0,
        "frequency_ghz": 1.5,
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "confidence_rows": [
            _confidence_row(nominal, nominal_x_width, nominal_margin_to_cutoff),
            _confidence_row(mismatch, 0.0, 3.0e-4, source_mismatch=True),
        ],
        "objective_diagnostic_rows": [
            {"case_label": nominal, "objective_label": "highband", "radius_margin_abs": 0.003},
            {"case_label": mismatch, "objective_label": "highband", "radius_margin_abs": 0.006},
        ],
    }


def test_parse_noise_seed_reads_case_label():
    noise, seed = parse_noise_seed("source_mismatch_noise19p64237213134765625_seed34")

    assert noise == pytest.approx(19.64237213134765625)
    assert seed == 34


def test_build_boundary_row_marks_clean_cutoff_margin_positive():
    row = build_boundary_row(_summary(), "outputs/experiments/409_run/data/summary.json")

    assert row["experiment_id"] == 409
    assert row["clean_for_scalar_bracket"] is True
    assert row["decision_class"] == "clean"
    assert row["nominal_status"] == "clean"
    assert row["source_mismatch_status"] == "clean"
    assert row["nominal_competing_margin_to_cutoff"] == pytest.approx(4.0e-9)
    assert row["nominal_highband_radius_margin_abs"] == pytest.approx(0.003)


def test_build_boundary_row_marks_point_correct_x_ambiguous():
    row = build_boundary_row(
        _summary(
            noise="19p64237213134765625",
            nominal_x_width=1.0,
            nominal_margin_to_cutoff=-7.4e-10,
        ),
        "outputs/experiments/417_run/data/summary.json",
    )

    assert row["experiment_id"] == 417
    assert row["clean_for_scalar_bracket"] is False
    assert row["decision_class"] == "point_correct_not_clean"
    assert row["nominal_status"] == "point_correct_x_ambiguous"
    assert row["nominal_ambiguity_x_width_mm"] == pytest.approx(1.0)
    assert row["nominal_competing_margin_to_cutoff"] == pytest.approx(-7.4e-10)


def test_summarize_boundary_stops_at_numerical_edge():
    clean = build_boundary_row(_summary(), "outputs/experiments/409_run/data/summary.json")
    ambiguous = build_boundary_row(
        _summary(
            noise="19p64237213134765625",
            nominal_x_width=1.0,
            nominal_margin_to_cutoff=-7.4e-10,
        ),
        "outputs/experiments/417_run/data/summary.json",
    )

    summary = summarize_boundary(
        [clean, ambiguous],
        promoted_clean_noise_rms_percent=19.642333984375,
        tolerance=1.0e-9,
    )

    assert summary["clean_row_count"] == 1
    assert summary["point_correct_not_clean_row_count"] == 1
    assert summary["final_ambiguous_upper_experiment_id"] == 417
    assert summary["final_bracket_width_percent_rms"] == pytest.approx(
        19.64237213134765625 - 19.642333984375
    )
    assert summary["stop_due_to_numerical_edge"] is True
