# DGX Spark Deployment Guide

This project is designed to run on an NVIDIA DGX Spark for GPU-accelerated
FDTD simulation, synthetic coordinate-optimizer experiments, and field-data QC.

For complete setup and migration instructions, see:

```text
SETUP.md
MIGRATION.md
```

## Setup On DGX Spark

Clone the repository:

```bash
git clone https://github.com/Maruf001/GPR-FDTD-FWI.git
cd GPR-FDTD-FWI
```

Create the Python environment:

```bash
conda env create -f environment.yml
conda activate gpr-fdtd-fwi
```

Or use pip:

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-gpu.txt
```

Verify GPU access:

```bash
python - <<'PY'
import cupy as cp
print("cupy", cp.__version__)
print("runtime", cp.cuda.runtime.runtimeGetVersion())
print("device", cp.cuda.Device(0))
print(cp.asnumpy(cp.arange(8) ** 2))
PY
```

---

## What to Run

### Step 1: Forward Simulation

```bash
python run_forward.py
```

**What it does**:
- Builds the ground-truth model (concrete + 3 rebars)
- Runs a multi-position GPR scan (100 positions along the surface)
- Each scan position: reset fields → inject Ricker wavelet → record Ez at receiver → assemble B-scan
- Saves: geometry plot, B-scan radargram, wave propagation animation

**Expected outputs** in `outputs/`:
- `figures/geometry.png` — true permittivity model showing air, concrete, and rebars
- `figures/bscan.png` — B-scan radargram with 3 rebar hyperbolas
- `animations/wavefield.gif` — wave propagation through concrete

**Runtime**: ~2-5 minutes on CPU, ~10-30 seconds on GPU

### Step 2: Full-Waveform Inversion

```bash
python run_inversion.py --iterations 30 --method lbfgs
```

**What it does**:
1. Generates "observed" data from the true rebar model
2. Starts from a homogeneous concrete model (no rebars)
3. Iteratively updates the permittivity distribution:
   - Forward simulation → synthetic data
   - Compute residual (synthetic - observed)
   - Adjoint simulation → gradient via cross-correlation
   - Add TV regularization gradient
   - L-BFGS-B optimizer updates εr with bounds [1, 15]
4. Saves inversion results and convergence plots

**Expected outputs**:
- `figures/inversion_result.png` — true vs initial vs recovered model
- `figures/convergence.png` — misfit reduction over iterations
- `data/inverted_model.npy` — final εr distribution

**Runtime**: ~30-60 minutes (30 iterations × ~50 sources × 2 simulations each)

### Step 3: GPU Benchmark

```bash
python run_benchmark.py
```

**What it does**:
- Runs the forward FDTD simulation on CPU (NumPy) and GPU (CuPy)
- Reports timing and speedup factor
- The GPU version uses CuPy as a drop-in replacement for NumPy arrays

**Expected speedup**: 30-80x for the FDTD field updates

---

## GPU Architecture Notes

The DGX Spark has an NVIDIA GPU with substantial VRAM. Key considerations:

### Memory Budget

| Component | Size | Notes |
|-----------|------|-------|
| Field arrays (Ez, Hx, Hy) | 3 × 180 × 280 × 8 = 1.2 MB | Trivial |
| CPML auxiliary fields | ~0.5 MB | 8 psi arrays |
| Update coefficients (Ca, Cb, Dh) | 3 × 180 × 280 × 8 = 1.2 MB | Trivial |
| Forward fields for adjoint | 1885 × 180 × 280 × 8 = 760 MB | Largest component |
| **Total** | **~765 MB** | Fits easily on any modern GPU |

### What Runs on GPU

- H-field update (embarrassingly parallel stencil)
- E-field update (embarrassingly parallel stencil)
- Source injection + receiver recording
- Gradient accumulation (element-wise multiply-accumulate)

### What Stays on CPU

- Parameter setup and model construction (one-time cost)
- Optimization loop control (L-BFGS iterations)
- File I/O and visualization

---

## Troubleshooting

### CuPy not found

```bash
pip install cupy-cuda12x  # adjust for your CUDA version
```

### Out of GPU memory

The adjoint method stores all forward Ez fields (~760 MB). If memory is tight:
- Reduce `NT` in config.py (shorter simulation time)
- Use checkpointing (store every Nth field, recompute between)

### Slow first run

CuPy compiles CUDA kernels on first use. Subsequent runs will be faster due to kernel caching.

### Import errors

Make sure you run from the project root directory:
```bash
cd GPR-FDTD-FWI
python run_forward.py
```

## Migration Note

`outputs/experiments/` is ignored by Git. To recreate this machine's full
working copy on another DGX Spark, restore the local artifact archive described
in `MIGRATION.md` after cloning.
