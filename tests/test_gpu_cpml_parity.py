"""GPU CPML parity tests.

These tests keep the GPU forward path honest by comparing gpu/fdtd_gpu_v2.py
against the CPU CPML solver for the same model, source, and receiver.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg
from core.fdtd import FDTDSimulator
from core.geometry import build_single_rebar_model
from core.source import generate_time_array, ricker_wavelet
from core.utils import pos_to_index
from gpu.fdtd_gpu_v2 import FDTDSimulatorGPU_v2
from inversion.single_rebar_pipeline import default_single_rebar_truth


def _cupy_available():
    try:
        import cupy as cp

        return cp.cuda.runtime.getDeviceCount() > 0
    except Exception:
        return False


def _single_rebar_case():
    params = default_single_rebar_truth()
    model = build_single_rebar_model(params.x, params.z, params.radius)
    time = generate_time_array(cfg.NT, cfg.DT)
    source = ricker_wavelet(time, cfg.F_CENTER)
    return params, model, source


def _scan_position(x_pos):
    src_iz = pos_to_index(cfg.TX_Z, cfg.DZ, cfg.NPML)
    rec_iz = pos_to_index(cfg.RX_Z, cfg.DZ, cfg.NPML)
    src_ix = pos_to_index(x_pos, cfg.DX, cfg.NPML)
    rec_ix = pos_to_index(x_pos + cfg.TX_RX_OFFSET, cfg.DX, cfg.NPML)
    rec_ix = min(rec_ix, cfg.NX - cfg.NPML - 1)
    return src_iz, src_ix, rec_iz, rec_ix


def _assert_trace_close(cpu_trace, gpu_trace):
    abs_max = float(np.max(np.abs(cpu_trace - gpu_trace)))
    denom = max(float(np.max(np.abs(cpu_trace))), 1e-30)
    rel_max = abs_max / denom
    print(f"  GPU/CPU trace max abs diff={abs_max:.3e}, rel={rel_max:.3e}")

    assert np.all(np.isfinite(gpu_trace))
    assert rel_max < 1e-10


def test_gpu_cpml_trace_matches_cpu():
    """GPU v2 should match CPU CPML for a full one-rebar trace."""
    if not _cupy_available():
        print("  SKIPPED: CuPy/GPU is not available")
        return

    params, model, source = _single_rebar_case()
    position = _scan_position(params.x)
    cpu_trace = FDTDSimulator(model).run(source, *position)["trace"]
    gpu_trace = FDTDSimulatorGPU_v2(model, cfg).run(source, *position)["trace"]
    _assert_trace_close(cpu_trace, gpu_trace)


def test_gpu_cpml_batch_matches_cpu_traces():
    """Batched GPU B-scan should match independent CPU CPML traces."""
    if not _cupy_available():
        print("  SKIPPED: CuPy/GPU is not available")
        return

    _, model, source = _single_rebar_case()
    scan_x = [0.15, 0.25, 0.35]
    positions = [_scan_position(x_pos) for x_pos in scan_x]

    cpu_bscan = np.zeros((cfg.NT, len(positions)), dtype=np.float64)
    for i, position in enumerate(positions):
        cpu_bscan[:, i] = FDTDSimulator(model).run(source, *position)["trace"]

    gpu_bscan = FDTDSimulatorGPU_v2(model, cfg).run_batch(source, positions)["bscan"]
    _assert_trace_close(cpu_bscan, gpu_bscan)


if __name__ == "__main__":
    tests = [
        ("gpu cpml trace matches cpu", test_gpu_cpml_trace_matches_cpu),
        ("gpu cpml batch matches cpu traces", test_gpu_cpml_batch_matches_cpu_traces),
    ]

    print("=" * 50)
    print("GPU CPML Parity Tests")
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
