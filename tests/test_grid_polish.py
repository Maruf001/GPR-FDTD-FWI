"""Lightweight tests for deterministic grid-polish helpers."""
import os
import sys
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.single_rebar_pipeline import (
    SingleRebarInversionEngine,
    SingleRebarParams,
    _quantized_axis_mm,
)
from run_single_rebar_inversion import _grid_polish_config_from_args


def test_quantized_axis_clips_and_snaps_to_absolute_grid():
    values = _quantized_axis_mm(
        center_mm=90.6526,
        half_window_mm=1.0,
        step_mm=0.25,
        lower_mm=70.0,
        upper_mm=110.0,
    )

    expected = np.array([89.75, 90.0, 90.25, 90.5, 90.75, 91.0, 91.25, 91.5])
    np.testing.assert_allclose(values, expected)


def test_quantized_axis_single_value_when_window_is_zero():
    values = _quantized_axis_mm(
        center_mm=249.533,
        half_window_mm=0.0,
        step_mm=1.0,
        lower_mm=220.0,
        upper_mm=280.0,
    )

    np.testing.assert_allclose(values, np.array([250.0]))


def test_quantized_axis_respects_bounds():
    values = _quantized_axis_mm(
        center_mm=4.2,
        half_window_mm=1.0,
        step_mm=0.5,
        lower_mm=4.0,
        upper_mm=5.0,
    )

    np.testing.assert_allclose(values, np.array([4.0, 4.5, 5.0]))


def test_local_grid_polish_records_sorted_top_candidates():
    class BoundsStub:
        lb = np.array([0.220, 0.070, 0.004])
        ub = np.array([0.280, 0.110, 0.010])

    class EngineStub:
        def objective(self, values):
            params = SingleRebarParams.from_array(values)
            x_mm = params.x * 1000.0
            z_mm = params.z * 1000.0
            radius_mm = params.radius * 1000.0
            return (
                (x_mm - 250.0) ** 2
                + (z_mm - 90.0) ** 2
                + (radius_mm - 6.0) ** 2
            )

    seed = SingleRebarParams(x=0.2496, z=0.0906, radius=0.0069)
    result = SingleRebarInversionEngine._local_grid_polish(
        EngineStub(),
        seed.as_array(),
        BoundsStub(),
        {
            "x_half_window_mm": 0.0,
            "z_half_window_mm": 1.0,
            "radius_half_window_mm": 1.0,
            "x_step_mm": 1.0,
            "z_step_mm": 0.5,
            "radius_step_mm": 0.2,
            "progress_every": 0,
            "top_k": 3,
        },
    )

    assert result["evaluations"] == 40
    assert len(result["top_candidates"]) == 3
    misfits = [item["misfit"] for item in result["top_candidates"]]
    assert misfits == sorted(misfits)
    assert result["top_candidates"][0]["params"] == {
        "x_mm": 250.0,
        "z_mm": 90.0,
        "radius_mm": 6.0,
    }


def test_grid_polish_coarse_preset_can_be_overridden():
    args = SimpleNamespace(
        grid_polish_preset="coarse",
        polish_x_half_window_mm=None,
        polish_z_half_window_mm=None,
        polish_radius_half_window_mm=None,
        polish_x_step_mm=None,
        polish_z_step_mm=0.25,
        polish_radius_step_mm=None,
        polish_progress_every=None,
        polish_top_k=5,
        polish_stop_misfit=None,
    )

    config = _grid_polish_config_from_args(args)

    assert config["preset"] == "coarse"
    assert config["z_step_mm"] == 0.25
    assert config["radius_step_mm"] == 0.2
    assert config["progress_every"] == 10
    assert config["top_k"] == 5


if __name__ == "__main__":
    tests = [
        ("quantized axis clips and snaps", test_quantized_axis_clips_and_snaps_to_absolute_grid),
        ("quantized axis zero window", test_quantized_axis_single_value_when_window_is_zero),
        ("quantized axis respects bounds", test_quantized_axis_respects_bounds),
        ("local grid polish records top candidates", test_local_grid_polish_records_sorted_top_candidates),
        ("grid polish coarse preset can be overridden", test_grid_polish_coarse_preset_can_be_overridden),
    ]

    print("=" * 50)
    print("Grid Polish Tests")
    print("=" * 50)

    passed = 0
    failed = 0
    for name, test_fn in tests:
        try:
            print(f"\n[{name}]")
            test_fn()
            print("  PASSED")
            passed += 1
        except Exception as exc:
            print(f"  FAILED: {exc}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    if failed:
        raise SystemExit(1)
