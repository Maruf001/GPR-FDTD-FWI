"""
Smoke tests for the one-rebar inversion pipeline.

These tests avoid a full optimizer run. They verify that the synthetic
objective is well-posed enough to prefer the true geometry over a clearly
wrong candidate.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg
from core.geometry import build_single_rebar_model
from inversion.single_rebar_pipeline import (
    SingleRebarInversionEngine,
    default_single_rebar_truth,
)


def test_single_rebar_model_center_cell():
    params = default_single_rebar_truth()
    model = build_single_rebar_model(params.x, params.z, params.radius)

    iz = int(np.round(params.z / cfg.DZ)) + cfg.NPML
    ix = int(np.round(params.x / cfg.DX)) + cfg.NPML

    assert model.epsilon_r[iz, ix] == cfg.REBAR_EPSR
    assert model.sigma[iz, ix] == cfg.REBAR_SIGMA


def test_single_rebar_objective_prefers_truth():
    engine = SingleRebarInversionEngine(
        n_sources=3,
        frequencies=(cfg.F_CENTER,),
        backend="cpu",
        log_every=999,
    )

    true_values = engine.true_params.as_array()
    wrong_values = true_values + np.array([0.040, 0.020, 0.004])

    j_true = engine.objective(true_values)
    j_wrong = engine.objective(wrong_values)

    assert np.isfinite(j_true)
    assert np.isfinite(j_wrong)
    assert j_true < 1e-12
    assert j_wrong > j_true


if __name__ == "__main__":
    tests = [
        ("single rebar model center cell", test_single_rebar_model_center_cell),
        ("single rebar objective prefers truth", test_single_rebar_objective_prefers_truth),
    ]

    print("=" * 50)
    print("Single-Rebar Pipeline Tests")
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

    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 50}")

    if failed:
        raise SystemExit(1)
