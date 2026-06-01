"""Tests for detector-seeded two-stage refinement runner helpers."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_detection_seeded_two_stage_refinement import (  # noqa: E402
    axis_values_mm,
    best_source_profiled_candidate,
    build_material_uncertainty_command,
    build_polish_command,
    build_parser,
    build_radius_uncertainty_report_command,
    format_values_arg,
    select_detection_candidate,
)


def test_axis_values_mm_builds_inclusive_centered_axis():
    values = axis_values_mm(95.0, 15.0, 5.0)

    assert values == [80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0]


def test_axis_values_mm_clips_bounds_and_handles_decimal_steps():
    values = axis_values_mm(6.4, 1.0, 0.2, min_value_mm=5.4, max_value_mm=7.4)

    assert values == [5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4]


def test_format_values_arg_removes_float_noise():
    assert format_values_arg([5.800000000000001, 6.0, 6.2]) == "5.8,6,6.2"


def test_select_detection_candidate_uses_one_based_rank():
    summary = {
        "candidates": [
            {"rank": 1, "x_mm": 250.0},
            {"rank": 2, "x_mm": 246.0},
        ],
    }

    assert select_detection_candidate(summary, 2)["x_mm"] == 246.0


def test_best_source_profiled_candidate_uses_lowest_misfit():
    summary = {
        "top_candidates": [
            {"misfit": 2.0, "params": {"radius_mm": 6.2}},
            {"misfit": 1.0, "params": {"radius_mm": 6.0}},
        ],
    }

    assert best_source_profiled_candidate(summary)["params"]["radius_mm"] == 6.0


def test_parser_accepts_negative_source_shift_default():
    args = build_parser().parse_args([])

    assert args.source_time_shift_ps_values == "-50,0,50"
    assert not args.enable_guarded_polish
    assert args.guarded_sources == 9
    assert not args.enable_highband_polish
    assert args.highband_frequency_ghz == 2.5
    assert args.highband_sources == 9
    assert not args.enable_material_uncertainty_report
    assert args.material_uncertainty_subcell_samples == 13


def test_build_polish_command_passes_truth_geometry(tmp_path):
    args = build_parser().parse_args([
        "--truth-x-mm",
        "248",
        "--truth-z-mm",
        "96",
        "--truth-radius-mm",
        "7",
        "--refinement-geometry-mode",
        "subcell",
        "--refinement-subcell-samples",
        "7",
        "--refinement-frequencies-ghz",
        "1.0,1.5",
        "--refinement-frequency-weights",
        "1,2",
    ])

    command = build_polish_command(
        args,
        tmp_path,
        "coarse",
        2.0,
        [248.0],
        [91.0, 96.0, 101.0],
        [6.8, 7.0, 7.2],
        10,
    )

    assert "--truth-x-mm" in command
    assert command[command.index("--truth-x-mm") + 1] == "248"
    assert command[command.index("--truth-z-mm") + 1] == "96"
    assert command[command.index("--truth-radius-mm") + 1] == "7"
    assert command[command.index("--geometry-mode") + 1] == "subcell"
    assert command[command.index("--subcell-samples") + 1] == "7"
    assert command[command.index("--frequencies-ghz") + 1] == "1.0,1.5"
    assert command[command.index("--frequency-weights") + 1] == "1,2"


def test_build_polish_command_accepts_guarded_overrides(tmp_path):
    args = build_parser().parse_args([
        "--refinement-sources",
        "3",
        "--refinement-geometry-mode",
        "hard",
    ])

    command = build_polish_command(
        args,
        tmp_path,
        "guarded",
        1.0,
        [250.0],
        [69.0, 70.0, 71.0],
        [3.9, 4.0, 4.1],
        1,
        sources=9,
        geometry_mode="subcell",
        subcell_samples=9,
        frequencies_ghz="1.0,1.5",
        frequency_weights="1,4",
    )

    assert command[command.index("--sources") + 1] == "9"
    assert command[command.index("--geometry-mode") + 1] == "subcell"
    assert command[command.index("--subcell-samples") + 1] == "9"
    assert command[command.index("--frequencies-ghz") + 1] == "1.0,1.5"
    assert command[command.index("--frequency-weights") + 1] == "1,4"


def test_build_polish_command_accepts_highband_base_frequency(tmp_path):
    args = build_parser().parse_args(["--frequency-ghz", "1.5"])

    command = build_polish_command(
        args,
        tmp_path,
        "highband",
        1.0,
        [250.0],
        [69.0, 70.0, 71.0],
        [3.9, 4.0, 4.1],
        1,
        sources=9,
        geometry_mode="subcell",
        subcell_samples=9,
        base_frequency_ghz=2.5,
        frequencies_ghz=None,
    )

    assert command[command.index("--frequency-ghz") + 1] == "2.5"
    assert "--frequencies-ghz" not in command


def test_build_material_uncertainty_command_uses_final_window(tmp_path):
    args = build_parser().parse_args([
        "--enable-highband-polish",
        "--highband-frequency-ghz",
        "2.5",
        "--truth-z-mm",
        "70",
        "--truth-radius-mm",
        "4",
        "--observed-frequency-scale",
        "1.1",
        "--observed-time-shift-ps",
        "-50",
        "--observed-amplitude-scale",
        "1.1",
        "--observed-noise-rms-fraction",
        "0.1",
        "--material-uncertainty-concrete-epsr-values",
        "5.8,6.0,6.2",
        "--material-uncertainty-rebar-log10-sigma-values",
        "6,7",
    ])

    command = build_material_uncertainty_command(
        args,
        tmp_path,
        x_mm=250.0,
        z_mm=70.0,
        radius_values_mm=[3.95, 4.0, 4.05],
    )

    assert command[command.index("--frequency-ghz") + 1] == "2.5"
    assert command[command.index("--truth-radius-mm") + 1] == "4"
    assert command[command.index("--radius-values-mm") + 1] == "3.95,4,4.05"
    assert command[command.index("--geometry-mode") + 1] == "subcell"
    assert command[command.index("--subcell-samples") + 1] == "13"
    assert "--fit-amplitude" in command


def test_build_radius_uncertainty_report_command_passes_case(tmp_path):
    args = build_parser().parse_args(["--material-uncertainty-case-label", "shallow_r4"])

    command = build_radius_uncertainty_report_command(
        args,
        tmp_path / "report",
        tmp_path / "nominal.json",
        tmp_path / "material.json",
    )

    assert command[command.index("--case") + 1] == "shallow_r4"
    assert command[command.index("--case") + 2].endswith("nominal.json")
    assert command[command.index("--case") + 3].endswith("material.json")
    assert command[command.index("--outdir") + 1].endswith("report")
