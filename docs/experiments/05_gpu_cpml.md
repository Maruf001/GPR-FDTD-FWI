# Experiment 05: Port CPML to GPU

**Date**: 2026-03-30

## Objective

Port the Convolutional Perfectly Matched Layer (CPML) absorbing boundary conditions from CPU (NumPy) to GPU (CuPy), creating a fully GPU-resident FDTD time-stepping loop.

## Files Created

- `gpu/cpml_gpu.py` — CuPy port of `core/cpml.py`. Replaces per-layer Python loops with vectorised 2D array operations. All 8 psi arrays and coefficient profiles reside on GPU.
- `gpu/fdtd_gpu_v2.py` — Extends `gpu/fdtd_gpu.py` (v1) to integrate GPU CPML. The complete time-stepping loop (H update → CPML H → E update → CPML E → source) now executes entirely on GPU.

## Approach

The CPU CPML uses explicit `for ip in range(npml)` loops (8 loops total, 4 for H and 4 for E corrections). Each loop iteration operates on a single PML layer — a 1D slice of the boundary.

The GPU port replaces these loops with **vectorised 2D operations**: all PML layers are updated simultaneously using CuPy array broadcasting. The 1D coefficient arrays (`b`, `c`) are broadcast against the 2D psi arrays using `[:, None]` or `[None, :]` indexing.

Reversed coefficient arrays (`bz_h_rev`, etc.) are pre-computed at init time for the high-side boundaries, avoiding per-step index reversal.

## Correctness Verification

| Metric | Value |
|--------|-------|
| Max absolute difference (CPU vs GPU v2 trace) | **0.0** |
| Relative error | **0.0** |
| Bit-identical | **Yes** |

The GPU v2 trace is **bit-for-bit identical** to the CPU reference trace, confirming that the CPML port is mathematically exact.

## Performance Results

Benchmark: 180×280 grid, 1885 time steps, 3 runs averaged.

| Configuration | Time [s] | Speedup vs CPU |
|--------------|----------|----------------|
| CPU (with CPML) | 1.699 | 1.0× |
| GPU v1 (no CPML) | 0.365 | 4.7× |
| **GPU v2 (with CPML)** | **1.101** | **1.5×** |

## Analysis

GPU v2 is 1.5× faster than CPU with full CPML — a fair apples-to-apples comparison. The GPU v1 number (4.7×) was artificially inflated because it had no absorbing boundaries at all.

The moderate speedup (1.5× instead of 4-7×) is due to the CPML operating on thin boundary regions (15 cells × Nx or Nz × 15 cells) where GPU parallelism is under-utilised. Each boundary correction launches a separate CuPy kernel, and the overhead of many small kernel launches reduces the GPU advantage.

For larger grids (e.g., 1000×1000), the CPML cost grows linearly with boundary length while the field update cost grows quadratically. Thus the CPML overhead would be proportionally smaller, and the overall GPU speedup would approach the v1 numbers.

## Key Insight

Porting CPML to GPU is worthwhile for correctness (enables fully GPU-resident simulation) but the performance gain at this grid size is modest. The real benefit appears at larger grid sizes or when running many simulations (e.g., during inversion with 275 forward evaluations), where the cumulative time savings add up.

## Baseline Preserved

Original files `gpu/fdtd_gpu.py` and `core/cpml.py` are unchanged. The v2 files are new additions.
