"""Tests for material tradeoff runner helpers."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_material_tradeoff import (  # noqa: E402
    best_curve_by_radius,
    build_parser,
    parse_log10_sigma_values,
    write_csv,
)


def test_parse_log10_sigma_values_converts_to_sigma():
    values = parse_log10_sigma_values("5,7")

    assert values == [1e5, 1e7]


def test_best_curve_by_radius_profiles_over_materials():
    candidates = [
        {"misfit": 2.0, "params": {"radius_mm": 6.0}, "material": {"concrete_epsr": 5.5}},
        {"misfit": 1.0, "params": {"radius_mm": 6.0}, "material": {"concrete_epsr": 6.0}},
        {"misfit": 1.5, "params": {"radius_mm": 6.2}, "material": {"concrete_epsr": 6.0}},
    ]

    curve = best_curve_by_radius(candidates)

    assert curve == [
        {"misfit": 1.0, "params": {"radius_mm": 6.0}, "material": {"concrete_epsr": 6.0}},
        {"misfit": 1.5, "params": {"radius_mm": 6.2}, "material": {"concrete_epsr": 6.0}},
    ]


def test_parse_log10_sigma_values_rejects_empty():
    with pytest.raises(Exception):
        parse_log10_sigma_values("")


def test_parser_accepts_shallow_source_profile_options():
    args = build_parser().parse_args([
        "--truth-z-mm",
        "70",
        "--truth-radius-mm",
        "4",
        "--source-frequency-scales",
        "1.0,1.1",
        "--source-time-shift-ps-values=-50,0",
        "--fit-amplitude",
        "--geometry-mode",
        "subcell",
        "--subcell-samples",
        "13",
    ])

    assert args.truth_z_mm == 70.0
    assert args.truth_radius_mm == 4.0
    assert args.source_frequency_scales == [1.0, 1.1]
    assert args.source_time_shift_ps_values == [-50.0, 0.0]
    assert args.fit_amplitude is True
    assert args.geometry_mode == "subcell"
    assert args.subcell_samples == 13


def test_write_csv_includes_source_profile_fields(tmp_path):
    csv_path = tmp_path / "material.csv"
    write_csv(
        csv_path,
        [
            {
                "misfit": 0.1,
                "params": {"x_mm": 250.0, "z_mm": 70.0, "radius_mm": 4.0},
                "material": {
                    "concrete_epsr": 6.0,
                    "rebar_sigma": 1.0e7,
                    "rebar_log10_sigma": 7.0,
                },
                "source_profile": {
                    "frequency_scale": 1.1,
                    "time_shift_ps": -50.0,
                    "amplitude_scale": 1.08,
                },
            }
        ],
    )

    text = csv_path.read_text(encoding="utf-8")
    assert "source_frequency_scale" in text
    assert "1.08" in text
