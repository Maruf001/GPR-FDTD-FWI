"""
Entry point: CPU vs GPU benchmark (bonus Part B.3).

Usage:
    python run_benchmark.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config as cfg
from core.geometry import build_rebar_model
from gpu.benchmark import benchmark_forward, get_hardware_info


def main():
    print("=" * 60)
    print("FDTD CPU vs GPU Benchmark")
    print("=" * 60)

    # Hardware info
    hw = get_hardware_info()
    print(f"\nHardware:")
    print(f"  Platform: {hw['platform']}")
    print(f"  CPU: {hw['processor']}")
    print(f"  GPU: {hw['gpu_name']}")
    if hw['gpu_memory_mb']:
        print(f"  GPU Memory: {hw['gpu_memory_mb']:.0f} MB")
    print(f"  CUDA: {hw['cuda_version']}")

    # Build model
    print("\nBuilding model...")
    model = build_rebar_model()

    # Run benchmark
    print(f"\nBenchmarking ({cfg.NT} time steps, {cfg.NZ}x{cfg.NX} grid)...")
    result = benchmark_forward(model, cfg, n_runs=3)

    print(f"\nResults:")
    print(f"  CPU time: {result['cpu_time']:.3f} s")
    if result['gpu_time']:
        print(f"  GPU time: {result['gpu_time']:.3f} s")
        print(f"  Speedup: {result['speedup']:.1f}x")
    else:
        print(f"  GPU: not available")

    print(f"\nOperations moved to GPU:")
    print(f"  - H-field update (Hx, Hy stencil operations)")
    print(f"  - E-field update (Ez stencil operations)")
    print(f"  - Source injection")
    print(f"  - Receiver recording")
    print(f"  Note: CPML not yet ported to GPU in this version")


if __name__ == "__main__":
    main()
