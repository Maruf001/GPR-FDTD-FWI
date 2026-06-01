"""Tests for post-hoc frequency reweight diagnostics."""

import argparse
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_source_profiled_frequency_reweight_diagnostic import (  # noqa: E402
    evaluate_weight_cases,
    infer_frequency_keys,
    parse_weight_cases,
    weighted_misfit,
)


def test_infer_frequency_keys_from_csv_fields():
    fields = ["misfit", "frequency_misfit_1GHz", "frequency_misfit_1.5GHz"]

    assert infer_frequency_keys(fields) == ["1GHz", "1.5GHz"]


def test_parse_weight_cases_validates_frequency_count():
    cases = parse_weight_cases("equal:1,1|hi:1,4", ["1GHz", "1.5GHz"])

    assert cases[1]["weights"] == {"1GHz": 1.0, "1.5GHz": 4.0}
    with pytest.raises(argparse.ArgumentTypeError):
        parse_weight_cases("bad:1,2,3", ["1GHz", "1.5GHz"])


def test_weighted_misfit_uses_normalized_weights():
    row = {"frequency_misfit_1GHz": "1.0", "frequency_misfit_1.5GHz": "3.0"}

    assert weighted_misfit(row, ["1GHz", "1.5GHz"], {"1GHz": 1.0, "1.5GHz": 3.0}) == 2.5


def test_evaluate_weight_cases_changes_margin():
    rows = [
        {
            "x_mm": "250",
            "z_mm": "70",
            "radius_mm": "4.0",
            "source_frequency_scale": "1.0",
            "source_time_shift_ps": "0",
            "source_amplitude_scale": "1.0",
            "frequency_misfit_1GHz": "0.20",
            "frequency_misfit_1.5GHz": "0.10",
        },
        {
            "x_mm": "250",
            "z_mm": "70",
            "radius_mm": "4.1",
            "source_frequency_scale": "1.0",
            "source_time_shift_ps": "0",
            "source_amplitude_scale": "1.0",
            "frequency_misfit_1GHz": "0.19",
            "frequency_misfit_1.5GHz": "0.15",
        },
    ]
    cases = parse_weight_cases("equal:1,1|hi:1,4", ["1GHz", "1.5GHz"])

    results = evaluate_weight_cases(rows, ["1GHz", "1.5GHz"], cases)

    assert results["equal"]["margin"]["best_radius_mm"] == 4.0
    assert results["hi"]["margin"]["radius_margin_abs"] > results["equal"]["margin"]["radius_margin_abs"]
