# Project Context — Read This First

**Purpose**: This document contains full context for continuing work on this project. When opening this project on a new machine (e.g., DGX Spark), tell Claude to read this file first and it will know exactly what to do.

## Current Migration Note - 2026-06-14

This file contains useful historical architecture context, but the project has
advanced substantially since the original 2026-03-23 state below. On a new
machine, read these files first:

- `MIGRATION.md`
- `SETUP.md`
- `docs/update/summary/005_2026-06-11_summary_update.md`
- `docs/migration/2026-06-14_project_audit.md`

Important: `outputs/experiments/` is intentionally ignored by Git. Restore it
from the local artifact archive described in `MIGRATION.md` if an exact working
copy is needed.

---

## What This Project Is

A 2D FDTD electromagnetic simulation + adjoint-state full-waveform inversion for GPR concrete/rebar scanning. It's a technical assessment for a Cambridge/Inframind research position (Haibing Wu, Brian Sheil). The candidate (the user) must demonstrate a working implementation and explain the theory during a screen-share interview.

### Deliverables

| Part | Description | Status |
|------|-------------|--------|
| **A** | Theory discussion (FDTD, adjoint, GPU) | DONE — see `docs/theory_guide.md` and `docs/parameter_justifications.md` |
| **B.1** | Forward FDTD simulation with B-scan + animation | DONE — `python run_forward.py` produces correct outputs |
| **B.2** | Adjoint-state FWI to recover rebar geometry | CODE COMPLETE — needs full run on GPU |
| **B.3** | GPU/CUDA acceleration with benchmarks | CODE COMPLETE — needs CuPy on GPU machine |

---

## Current State (as of 2026-03-23)

### What Works

1. **Forward simulation**: `python run_forward.py` — runs 101-position B-scan, produces geometry plot, B-scan radargram with 3 clear rebar hyperbolas, and wave propagation GIF. Verified stable (1885 steps, fields decay properly).

2. **Tests**: `python tests/test_fdtd_basic.py` — 6/6 pass (CFL, wavelet, materials, free-space stability, rebar stability, wave speed at 1.8% error).

3. **Inversion code**: All modules import and work. Single-source gradient computation verified (direction matches finite differences). 1-iteration test completed on CPU in 56 minutes — too slow for full 30 iterations on CPU but proves the pipeline works.

4. **GPU code**: `gpu/fdtd_gpu.py` ready (CuPy drop-in), `gpu/benchmark.py` ready. Needs `pip install cupy-cuda12x`.

### What Needs To Be Done (on DGX Spark)

**Step 1: Setup**
```bash
git clone <repo-url>
cd GPR-FDTD-FWI
pip install numpy scipy matplotlib numba pillow
pip install cupy-cuda12x  # for GPU
```

**Step 2: Verify forward simulation**
```bash
python run_forward.py
```
Check that `outputs/figures/bscan.png` shows 3 rebar hyperbolas.

**Step 3: Run full-waveform inversion (B.2)**
```bash
python run_inversion.py --iterations 30 --method lbfgs
```
This is the main deliverable that requires GPU-class hardware. Expected runtime: 30-60 minutes with 51 sources. Outputs:
- `outputs/figures/inversion_comparison.png` (initial vs inverted vs true model)
- `outputs/figures/convergence.png` (misfit reduction curve)
- `outputs/data/inversion_results.npz`

**Step 4: Run GPU benchmark (B.3)**
```bash
python run_benchmark.py
```
Reports CPU vs GPU speedup for forward simulation.

**Step 5: If inversion results are poor, tune parameters**
- Adjust `TV_WEIGHT` in `config.py` (currently 0.01)
- Try `--method steepest_descent` if L-BFGS-B converges poorly
- Increase `--iterations` if convergence is slow
- The gradient normalization in `inversion/adjoint.py` may need adjustment

---

## Architecture Overview

### Array Convention
`[iz, ix]` where iz = z (depth, rows), ix = x (lateral, columns). z increases downward.

### Yee Grid (TMz polarization)
- `Ez[iz, ix]` at integer grid point `(iz*dz, ix*dx)`
- `Hx[iz, ix]` at half-step in z: `((iz+½)*dz, ix*dx)` — affected by z-PML
- `Hy[iz, ix]` at half-step in x: `(iz*dz, (ix+½)*dx)` — affected by x-PML

### Time-stepping (leapfrog)
```
for each step:
    1. Update H from E  (H^{n-½} → H^{n+½})
    2. CPML corrections to H
    3. Update E from H  (E^n → E^{n+1})
    4. CPML corrections to E
    5. Inject source into Ez (soft/additive)
```

### Key Files

| File | Purpose |
|------|---------|
| `config.py` | ALL parameters — grid, materials, source, PML, scanning, inversion |
| `core/fdtd.py` | FDTD engine — `FDTDSimulator` class with `update_H()`, `update_E()`, `step()`, `run()` |
| `core/cpml.py` | CFS-PML absorbing boundaries — `update_H()` and `update_E()` corrections |
| `core/materials.py` | `MaterialModel` — eps_r, sigma, mu_r arrays + update coefficients Ca, Cb, Dh |
| `core/geometry.py` | `build_rebar_model()`, `build_initial_model()`, `model_from_epsilon_r()` |
| `core/scan.py` | `Scanner` — multi-position B-scan acquisition |
| `core/source.py` | `ricker_wavelet()`, `generate_time_array()` |
| `inversion/adjoint.py` | `compute_gradient_single_source()`, `compute_gradient_all_sources()` |
| `inversion/inversion_engine.py` | `InversionEngine` — orchestrates full FWI workflow |
| `inversion/optimizer.py` | `run_steepest_descent()`, `run_lbfgs()` |
| `inversion/regularization.py` | `tv_penalty()`, `tv_gradient()` |
| `gpu/fdtd_gpu.py` | `FDTDSimulatorGPU` — CuPy drop-in for forward sim (no CPML on GPU) |

---

## Bugs That Were Fixed (don't re-introduce these)

1. **FDTD update equations** (both CPU `core/fdtd.py` and GPU `gpu/fdtd_gpu.py`): H and E updates had x/z derivative directions swapped. Hx uses dEz/dz (1st index), Hy uses dEz/dx (2nd index).

2. **CPML sigma_max** (`core/cpml.py`): Was missing `ETA0` (~377 Ohm) in denominator. Formula: `sigma_max = 0.8 * (m+1) / (ETA0 * dh)`.

3. **CPML boundary overreach** (`core/cpml.py`): PML corrections were applied to cells not covered by the standard FDTD update (iz=0, ix=0 for E; iz=Nz-1 for Hx; ix=Nx-1 for Hy). Caused positive feedback → NaN. Fixed with `continue` guards.

4. **Adjoint gradient scaling** (`inversion/adjoint.py`): Raw formula `g = -eps0 * Σ(Ez_adj * dEz/dt * dt)` produces ~1e-17 magnitudes. Gradient is now normalized to unit max so L-BFGS-B can work.

5. **Steepest descent line search** (`inversion/optimizer.py`): Armijo line search called `objective_and_gradient()` at each trial step, recomputing the full gradient (51 sources × forward + adjoint). Replaced with fixed normalized step.

---

## Config Gotchas

- Frequency variable is `cfg.F_CENTER` (not `FC`)
- `MaterialModel(Nz, Nx)` — do NOT pass DX/DZ as positional args (they'd become eps_r_bg/sigma_bg)
- `generate_time_array(cfg.NT, cfg.DT)` — requires both args
- Grid includes PML: `NX = NX_INNER + 2*NPML = 280`, `NZ = NZ_INNER + 2*NPML = 180`
- Physical coords to grid: `iz = round(z_m / dz) + NPML`

---

## Potential Issues to Watch For

1. **Inversion not converging**: The adjoint gradient is normalized to max=1. If L-BFGS-B makes no progress, try steepest descent with `initial_step=0.05`. The gradient direction has been verified correct via finite differences.

2. **Memory on GPU**: Adjoint stores all forward Ez fields: 1885 × 180 × 280 × 8 bytes ≈ 760 MB. Should fit on any modern GPU.

3. **CuPy kernel compilation**: First run is slow due to JIT compilation. Subsequent runs are cached.

4. **GPU FDTD has no CPML**: The `FDTDSimulatorGPU` class doesn't include CPML absorbing boundaries. It's used only for benchmarking the core field updates. The inversion uses the CPU `FDTDSimulator` which has full CPML.

---

## Important: README Policy

**NEVER mention "interview", "interview prep", or any interview-related language in `README.md`.** The README is public-facing and should present this as a research project only. Interview context belongs here in PROJECT_CONTEXT.md and other internal docs, not in the README.

---

## Interview Prep Files

- `docs/theory_guide.md` — Comprehensive Part A answers (FDTD, adjoint-state, GPU topics)
- `docs/parameter_justifications.md` — Why every parameter was chosen (for walk-through)
- `docs/dgx_spark_guide.md` — Step-by-step deployment and what each script produces
