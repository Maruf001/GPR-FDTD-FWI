"""Tests for the multi-rebar local geometry profile runner."""

import os
import sys

import argparse
import csv
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg  # noqa: E402
from run_multi_rebar_common_radius_profile import build_scan_positions  # noqa: E402
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    best_curve_by_radius,
    build_objective_results,
    candidate_rebar_arrays,
    candidate_rebar_arrays_from_base,
    parse_vector_mm,
    rank_case,
    truth_radius_values_for_run,
    write_case_summary_csv,
    write_candidate_csv,
)


def test_parse_vector_mm_preserves_duplicate_rebar_coordinates():
    assert parse_vector_mm("90,90,90") == [90.0, 90.0, 90.0]
    assert parse_vector_mm("5.8:6.2:0.2,6.0") == [5.8, 6.0, 6.2, 6.0]


def test_parse_vector_mm_rejects_empty_values():
    with pytest.raises(argparse.ArgumentTypeError, match="at least one"):
        parse_vector_mm("")


def test_truth_radius_values_for_run_accepts_per_target_values():
    radii = truth_radius_values_for_run(6.0, [5.0, 6.0, 8.0], target_count=3)

    assert radii == [5.0, 6.0, 8.0]


def test_truth_radius_values_for_run_rejects_wrong_length():
    with pytest.raises(ValueError, match="truth radius"):
        truth_radius_values_for_run(6.0, [5.0, 6.0], target_count=3)


def test_candidate_rebar_arrays_updates_only_target():
    x_values, z_values, radii = candidate_rebar_arrays(
        [150.0, 250.0, 350.0],
        [90.0, 90.0, 90.0],
        6.0,
        0,
        148.0,
        89.0,
        5.8,
    )

    assert x_values == [148.0, 250.0, 350.0]
    assert z_values == [89.0, 90.0, 90.0]
    assert radii == [5.8, 6.0, 6.0]


def test_candidate_rebar_arrays_from_base_preserves_non_target_radii():
    x_values, z_values, radii = candidate_rebar_arrays_from_base(
        [150.0, 250.0, 350.0],
        [90.0, 91.0, 92.0],
        [5.8, 6.4, 6.8],
        1,
        251.0,
        89.0,
        6.0,
    )

    assert x_values == [150.0, 251.0, 350.0]
    assert z_values == [90.0, 89.0, 92.0]
    assert radii == [5.8, 6.0, 6.8]


def test_candidate_rebar_arrays_rejects_bad_target():
    with pytest.raises(ValueError, match="valid"):
        candidate_rebar_arrays([150.0], [90.0], 6.0, 1, 150.0, 90.0, 6.0)


def test_build_scan_positions_accepts_tx_rx_offset_override():
    default_positions, _ = build_scan_positions(cfg.INVERSION_SCAN_STEP, 1)
    wider_positions, _ = build_scan_positions(
        cfg.INVERSION_SCAN_STEP,
        1,
        tx_rx_offset_m=cfg.TX_RX_OFFSET + 3.0 * cfg.DX,
    )

    default_src_ix = default_positions[0][1]
    default_rec_ix = default_positions[0][3]
    wider_src_ix = wider_positions[0][1]
    wider_rec_ix = wider_positions[0][3]
    assert wider_src_ix == default_src_ix
    assert wider_rec_ix > default_rec_ix

    with pytest.raises(ValueError, match="non-negative"):
        build_scan_positions(cfg.INVERSION_SCAN_STEP, 1, tx_rx_offset_m=-cfg.DX)


def test_rank_case_sorts_local_geometry_candidates():
    candidates = [
        {
            "params": {"x_mm": 148.0, "z_mm": 90.0, "radius_mm": 6.2},
            "case_results": {
                "case": {
                    "misfit": 2.0,
                    "source_profile": {"frequency_scale": 1.0},
                }
            },
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {
                "case": {
                    "misfit": 1.0,
                    "source_profile": {"frequency_scale": 1.1},
                }
            },
        },
    ]

    ranked = rank_case(candidates, "case")

    assert ranked[0]["params"]["x_mm"] == 150.0
    assert ranked[0]["source_profile"]["frequency_scale"] == 1.1


def test_best_curve_by_radius_profiles_over_xz():
    candidates = [
        {
            "params": {"x_mm": 148.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {"case": {"misfit": 2.0, "source_profile": {}}},
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {"case": {"misfit": 1.0, "source_profile": {}}},
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.2},
            "case_results": {"case": {"misfit": 1.5, "source_profile": {}}},
        },
    ]

    curve = best_curve_by_radius(candidates, "case")

    assert curve[0]["radius_mm"] == 6.0
    assert curve[0]["params"]["x_mm"] == 150.0
    assert curve[1]["radius_mm"] == 6.2


def test_rank_case_supports_objective_variant_results():
    candidates = [
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {
                "case": {"misfit": 5.0, "source_profile": {"frequency_scale": 1.0}}
            },
            "objective_results": {
                "case": {
                    "base": {"misfit": 5.0, "source_profile": {"frequency_scale": 1.0}},
                    "late": {"misfit": 1.0, "source_profile": {"frequency_scale": 1.1}},
                }
            },
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 91.0, "radius_mm": 6.2},
            "case_results": {
                "case": {"misfit": 4.0, "source_profile": {"frequency_scale": 1.0}}
            },
            "objective_results": {
                "case": {
                    "base": {"misfit": 4.0, "source_profile": {"frequency_scale": 1.0}},
                    "late": {"misfit": 2.0, "source_profile": {"frequency_scale": 1.1}},
                }
            },
        },
    ]

    ranked = rank_case(candidates, "case", objective_label="late")

    assert ranked[0]["params"]["radius_mm"] == 6.0
    assert ranked[0]["source_profile"]["frequency_scale"] == 1.1


def test_build_objective_results_computes_margin_per_variant():
    candidates = [
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.0},
            "case_results": {"case": {"misfit": 1.0, "source_profile": {}}},
            "objective_results": {
                "case": {
                    "base": {"misfit": 1.0, "source_profile": {}},
                    "late": {"misfit": 3.0, "source_profile": {}},
                }
            },
        },
        {
            "params": {"x_mm": 150.0, "z_mm": 90.0, "radius_mm": 6.2},
            "case_results": {"case": {"misfit": 2.0, "source_profile": {}}},
            "objective_results": {
                "case": {
                    "base": {"misfit": 2.0, "source_profile": {}},
                    "late": {"misfit": 1.0, "source_profile": {}},
                }
            },
        },
    ]

    results = build_objective_results(candidates, ["case"], ["base", "late"], top_k=2)

    assert results["case"]["base"]["margin"]["best_radius_mm"] == 6.0
    assert results["case"]["base"]["margin"]["next_radius_mm"] == 6.2
    assert results["case"]["late"]["margin"]["best_radius_mm"] == 6.2
    assert results["case"]["late"]["top_candidates"][0]["misfit"] == 1.0


def test_write_candidate_csv_includes_source_shape_coefficients(tmp_path):
    candidates = [
        {
            "params": {
                "target_index": 0,
                "x_mm": 150.0,
                "z_mm": 90.0,
                "radius_mm": 6.0,
                "x_values_mm": [150.0, 250.0, 350.0],
                "z_values_mm": [90.0, 90.0, 90.0],
                "radii_mm": [6.0, 6.0, 6.0],
            },
            "case_results": {
                "ringdown": {
                    "misfit": 0.1,
                    "source_profile": {
                        "frequency_scale": 1.0,
                        "time_shift_ps": 0.0,
                        "amplitude_scale": 1.0,
                        "ringdown_scale": 0.25,
                        "ringdown_delay_ps": 180.0,
                        "ringdown_frequency_scale": 0.8,
                        "primary_coefficient": 1.0,
                        "ringdown_coefficient": 0.25,
                    },
                }
            },
        }
    ]
    path = tmp_path / "candidates.csv"

    write_candidate_csv(path, candidates, ["ringdown"])

    with path.open("r", encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))
    assert row["source_ringdown_scale"] == "0.25"
    assert row["source_primary_coefficient"] == "1.0"
    assert row["source_ringdown_coefficient"] == "0.25"


def test_write_case_summary_csv_includes_source_shape_coefficients(tmp_path):
    results = {
        "ringdown": {
            "top_candidates": [
                {
                    "params": {"x_mm": 150.0, "z_mm": 90.0},
                    "source_profile": {
                        "frequency_scale": 1.0,
                        "time_shift_ps": 0.0,
                        "amplitude_scale": 1.0,
                        "ringdown_scale": 0.25,
                        "ringdown_delay_ps": 180.0,
                        "ringdown_frequency_scale": 0.8,
                        "primary_coefficient": 1.0,
                        "ringdown_coefficient": 0.25,
                    },
                }
            ],
            "margin": {
                "best_radius_mm": 6.0,
                "next_radius_mm": 6.2,
                "radius_margin_abs": 0.1,
                "best_radius_misfit": 0.2,
            },
        }
    }
    path = tmp_path / "summary.csv"

    write_case_summary_csv(path, results)

    with path.open("r", encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))
    assert row["best_source_ringdown_scale"] == "0.25"
    assert row["best_source_primary_coefficient"] == "1.0"
    assert row["best_source_ringdown_coefficient"] == "0.25"
