"""Tests for multi-rebar material-profiled radius reporting."""

import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_multi_rebar_material_radius_profile import (  # noqa: E402
    best_material_curve_by_radius,
    build_parser,
    rank_material_case,
    write_candidate_csv,
)


def _candidate(radius, misfit, epsr=6.0, log_sigma=7.0):
    return {
        "params": {
            "target_index": 1,
            "x_mm": 250.0,
            "z_mm": 90.0,
            "radius_mm": radius,
            "x_values_mm": [150.0, 250.0, 350.0],
            "z_values_mm": [90.0, 90.0, 90.0],
            "radii_mm": [6.0, radius, 6.0],
        },
        "material": {
            "concrete_epsr": epsr,
            "concrete_sigma": 1.0e-3,
            "rebar_epsr": 1.0,
            "rebar_sigma": 10.0 ** log_sigma,
            "rebar_log10_sigma": log_sigma,
        },
        "case_results": {
            "case": {
                "misfit": misfit,
                "source_profile": {
                    "frequency_scale": 1.1,
                    "time_shift_ps": -50.0,
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


def test_rank_material_case_preserves_material_metadata():
    ranked = rank_material_case([
        _candidate(6.2, 2.0, epsr=5.8, log_sigma=5.0),
        _candidate(6.0, 1.0, epsr=6.0, log_sigma=7.0),
    ], "case")

    assert ranked[0]["params"]["radius_mm"] == 6.0
    assert ranked[0]["material"]["concrete_epsr"] == 6.0
    assert ranked[1]["material"]["rebar_log10_sigma"] == 5.0


def test_best_material_curve_by_radius_profiles_over_materials():
    curve = best_material_curve_by_radius([
        _candidate(6.0, 2.0, epsr=5.8),
        _candidate(6.0, 1.0, epsr=6.0),
        _candidate(6.2, 1.5, epsr=6.2),
    ], "case")

    assert [row["radius_mm"] for row in curve] == [6.0, 6.2]
    assert curve[0]["material"]["concrete_epsr"] == 6.0


def test_parser_accepts_material_and_ringdown_options():
    args = build_parser().parse_args([
        "--target-rebar-index",
        "2",
        "--target-radius-values-mm",
        "6.0,6.2",
        "--concrete-epsr-values",
        "5.8,6.0,6.2",
        "--rebar-log10-sigma-values",
        "5,7",
        "--fit-ringdown-coefficient",
        "--source-time-shift-ps-values=-50,0",
    ])

    assert args.target_rebar_index == 2
    assert args.target_radius_values_mm == [6.0, 6.2]
    assert args.concrete_epsr_values == [5.8, 6.0, 6.2]
    assert args.rebar_log10_sigma_values == [1.0e5, 1.0e7]
    assert args.fit_ringdown_coefficient is True
    assert args.source_time_shift_ps_values == [-50.0, 0.0]


def test_write_candidate_csv_includes_material_and_ringdown_fields(tmp_path):
    path = tmp_path / "candidates.csv"
    write_candidate_csv(path, [_candidate(6.0, 1.0)], ["case"])

    with path.open("r", encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))
    assert row["concrete_epsr"] == "6.0"
    assert row["rebar_log10_sigma"] == "7.0"
    assert row["source_ringdown_coefficient"] == "0.25"
