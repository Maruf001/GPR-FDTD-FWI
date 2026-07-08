"""
Entry point: CPU vs GPU benchmark (Part B.3).

Tests FDTD performance at multiple grid sizes to demonstrate
when GPU acceleration becomes advantageous.

Usage:
    python run_benchmark.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import config as cfg
from core.geometry import build_rebar_model
from gpu.benchmark import benchmark_forward, benchmark_scaling, get_hardware_info


def plot_scaling(results, save_path=None):
    """Plot CPU vs GPU scaling and speedup."""
    import matplotlib.pyplot as plt

    cells = [r['cells'] for r in results]
    cpu = [r['cpu_time'] for r in results]
    gpu = [r['gpu_time'] for r in results if r['gpu_time']]
    gpu_cells = [r['cells'] for r in results if r['gpu_time']]
    speedups = [r['speedup'] for r in results if r['speedup']]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Runtime comparison
    ax1.loglog(cells, cpu, 'bo-', linewidth=2, markersize=8, label='CPU (NumPy)')
    if gpu:
        ax1.loglog(gpu_cells, gpu, 'rs-', linewidth=2, markersize=8, label='GPU (CuPy)')
    ax1.set_xlabel('Grid cells', fontsize=12)
    ax1.set_ylabel('Runtime [s]', fontsize=12)
    ax1.set_title('FDTD Runtime: CPU vs GPU', fontsize=14)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Speedup
    if speedups:
        ax2.semilogx(gpu_cells, speedups, 'g^-', linewidth=2, markersize=10)
        ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Break-even')
        ax2.set_xlabel('Grid cells', fontsize=12)
        ax2.set_ylabel('GPU Speedup (x)', fontsize=12)
        ax2.set_title('GPU Speedup vs Grid Size', fontsize=14)
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3)

        # Annotate each point
        for c, s in zip(gpu_cells, speedups):
            ax2.annotate(f'{s:.1f}x', (c, s), textcoords='offset points',
                         xytext=(0, 12), ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {save_path}")
    plt.close()


def main():
    print("=" * 60)
    print("FDTD CPU vs GPU Benchmark")
    print("=" * 60)

    os.makedirs("outputs/figures", exist_ok=True)

    # Hardware info
    hw = get_hardware_info()
    print(f"\nHardware:")
    print(f"  Platform: {hw['platform']}")
    print(f"  CPU: {hw['processor']}")
    print(f"  GPU: {hw['gpu_name']}")
    if hw['gpu_memory_mb']:
        print(f"  GPU Memory: {hw['gpu_memory_mb']:.0f} MB")
    print(f"  CUDA: {hw['cuda_version']}")

    # --- Single-size benchmark (project grid) ---
    print(f"\n{'─' * 50}")
    print(f"Single-shot benchmark ({cfg.NZ}x{cfg.NX} grid, {cfg.NT} steps)")
    print(f"{'─' * 50}")

    model = build_rebar_model()
    result = benchmark_forward(model, cfg, n_runs=3)

    print(f"  CPU time: {result['cpu_time']:.3f} s")
    if result['gpu_time']:
        print(f"  GPU time: {result['gpu_time']:.3f} s")
        print(f"  Speedup: {result['speedup']:.1f}x")
    else:
        print(f"  GPU: not available")

    # --- Multi-size scaling benchmark ---
    print(f"\n{'─' * 50}")
    print("Scaling benchmark (500 time steps, varying grid size)")
    print(f"{'─' * 50}")

    scaling_results = benchmark_scaling(
        cfg,
        grid_sizes=[
            (180, 280),       # 50K cells (project size)
            (360, 560),       # 200K cells
            (720, 1120),      # 806K cells
            (1000, 1000),     # 1M cells
            (1440, 2240),     # 3.2M cells
        ],
        nt=500,
        n_runs=2,
    )

    # Print summary table
    print(f"\n{'─' * 60}")
    print(f"{'Grid':>12s} {'Cells':>10s} {'CPU [s]':>10s} {'GPU [s]':>10s} {'Speedup':>10s}")
    print(f"{'─' * 60}")
    for r in scaling_results:
        sp = f"{r['speedup']:.1f}x" if r['speedup'] else "N/A"
        gpu_str = f"{r['gpu_time']:.3f}" if r['gpu_time'] else "N/A"
        print(f"  {r['Nz']}x{r['Nx']:>4d}  {r['cells']:>10,d}  {r['cpu_time']:>10.3f}  {gpu_str:>10s}  {sp:>10s}")
    print(f"{'─' * 60}")

    # Plot
    plot_scaling(scaling_results, save_path="outputs/figures/gpu_scaling.png")

    print(f"\nKey observations:")
    print(f"  - GPU overhead dominates for small grids (<100K cells)")
    print(f"  - Crossover typically occurs around 200K-500K cells")
    print(f"  - GPU speedup increases with grid size (more parallelism)")
    print(f"  - CPML is not ported to GPU; full speedup would be higher")


if __name__ == "__main__":
    main()
