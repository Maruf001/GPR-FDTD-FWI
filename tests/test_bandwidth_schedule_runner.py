"""Tests for PEBDD bandwidth schedule runner helpers."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_single_rebar_bandwidth_schedule import (  # noqa: E402
    coarse_polish_config,
    parse_band_schedule,
)


def test_parse_band_schedule_accepts_pipe_separated_ghz_pairs():
    bands = parse_band_schedule("0.35,1.1|0.35,2.5")

    assert bands == [(0.35e9, 1.1e9), (0.35e9, 2.5e9)]


def test_parse_band_schedule_rejects_decreasing_band():
    try:
        parse_band_schedule("1.1,0.35")
    except argparse.ArgumentTypeError:
        return
    raise AssertionError("expected invalid band to raise")


def test_coarse_polish_config_records_top_k():
    config = coarse_polish_config(top_k=12)

    assert config["preset"] == "coarse"
    assert config["top_k"] == 12
    assert config["radius_step_mm"] == 0.2
