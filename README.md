# GPR-FDTD-FWI

**2D FDTD Forward Modeling & Adjoint-State Full-Waveform Inversion for Ground Penetrating Radar**

A from-scratch implementation of 2D finite-difference time-domain (FDTD) electromagnetic simulation and adjoint-state full-waveform inversion (FWI) for GPR inspection of reinforced concrete.

## Problem Setup

- **Scenario**: GPR scanning of a concrete slab with 3 embedded steel rebars
- **Polarization**: TMz (Ez, Hx, Hy) in the x-z plane
- **Source**: 1.5 GHz Ricker wavelet (standard for concrete GPR)
- **Domain**: 500 mm x 300 mm (40 mm air standoff + 260 mm concrete)
- **Rebars**: 3 x 12 mm diameter, 50 mm cover depth, 100 mm spacing

## Project Structure

```
├── config.py                  # All simulation parameters (documented)
├── run_forward.py             # Forward simulation → B-scan + animation
├── run_inversion.py           # Adjoint-state FWI
├── run_benchmark.py           # CPU vs GPU timing (bonus)
│
├── core/
│   ├── materials.py           # Material property arrays (εr, σ, μr)
│   ├── geometry.py            # Rebar model construction
│   ├── source.py              # Ricker wavelet generation
│   ├── fdtd.py                # 2D TMz FDTD engine (Yee grid + leapfrog)
│   ├── cpml.py                # CPML absorbing boundaries (CFS-PML)
│   ├── scan.py                # Multi-position B-scan acquisition
│   └── utils.py               # CFL check, wavelength calculations
│
├── inversion/
│   ├── adjoint.py             # Adjoint wavefield + gradient computation
│   ├── objective.py           # L2 misfit function
│   ├── regularization.py      # Total Variation (TV) regularization
│   ├── optimizer.py           # Steepest descent + L-BFGS-B
│   └── inversion_engine.py   # Full FWI workflow orchestration
│
├── gpu/
│   ├── fdtd_gpu.py            # CuPy GPU-accelerated FDTD
│   └── benchmark.py           # CPU/GPU timing utilities
│
├── visualization/
│   ├── plot_geometry.py       # Ground-truth model visualization
│   ├── plot_bscan.py          # B-scan radargram plotting
│   ├── plot_wavefield.py      # Wave propagation animation
│   ├── plot_inversion.py      # Inversion results comparison
│   └── plot_signals.py        # Signal + convergence plots
│
├── docs/
│   ├── theory_guide.md        # Theory discussion notes (FDTD, adjoint, GPU)
│   ├── parameter_justifications.md  # Why each parameter was chosen
│   └── dgx_spark_guide.md    # DGX Spark deployment instructions
│
└── tests/                     # Verification tests
```

## Quick Start

### Install Dependencies

```bash
# CPU-only (works on any machine)
pip install numpy scipy matplotlib numba pillow

# GPU support (NVIDIA GPU required)
pip install cupy-cuda12x   # match your CUDA version
```

### Run Forward Simulation

```bash
python run_forward.py
```

Produces:
- Ground-truth geometry plot
- B-scan radargram (3 rebar hyperbolas)
- Wave propagation animation (GIF)

### Run Full-Waveform Inversion

```bash
python run_inversion.py --iterations 30 --method lbfgs
```

Recovers the permittivity distribution from synthetic GPR data using the adjoint-state method.

### Run GPU Benchmark

```bash
python run_benchmark.py
```

Compares CPU vs GPU execution time for the forward simulation.

## Key Technical Details

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Grid spacing | 2 mm | ≥16 pts/wavelength at f_max in concrete |
| Time step | 4.24 ps | 90% of CFL limit for stability |
| CPML layers | 15 | ~60 dB absorption, cubic grading |
| Inversion target | εr only | Sufficient contrast for PEC rebars |
| Optimizer | L-BFGS-B | Quasi-Newton with bounds [1, 15] |
| Regularization | TV | Promotes sharp concrete/rebar boundaries |

## Theory References

- Yee (1966) — FDTD method
- Roden & Gedney (2000) — CFS-PML formulation
- Taflove & Hagness (2005) — FDTD bible
- Meles et al. (2010, 2012) — GPR FWI with adjoint method
- Ernst et al. (2007) — FWI of crosshole radar

See `docs/theory_guide.md` for detailed theory discussion notes.
