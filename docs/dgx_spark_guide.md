# DGX Spark Deployment Guide

This project is designed to run on an NVIDIA DGX Spark for GPU-accelerated FDTD simulation and full-waveform inversion.

---

## Setup on DGX Spark

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/FTDT_Project.git
cd FTDT_Project
```

### 2. Install Dependencies

```bash
# Core packages
pip install numpy scipy matplotlib numba pillow

# GPU support — match your CUDA version
# Check CUDA version:
nvcc --version
# or:
nvidia-smi

# Install CuPy for your CUDA version
pip install cupy-cuda12x   # for CUDA 12.x
# pip install cupy-cuda11x  # for CUDA 11.x
```

### 3. Verify GPU Access

```bash
python -c "
import cupy as cp
print(f'CuPy version: {cp.__version__}')
print(f'CUDA version: {cp.cuda.runtime.runtimeGetVersion()}')
d = cp.cuda.Device(0)
print(f'GPU: {d.attributes[\"DeviceName\"]}' if hasattr(d, 'attributes') else f'GPU device 0 available')
print(f'Memory: {d.mem_info[1] / 1e9:.1f} GB')
"
```

---

## What to Run

### Step 1: Forward Simulation (Part B.1)

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

### Step 2: Full-Waveform Inversion (Part B.2)

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

### Step 3: GPU Benchmark (Part B.3 — Bonus)

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
cd FTDT_Project
python run_forward.py
```

---

## File Checklist for Interview

Before the interview, verify these outputs exist:
- [ ] `outputs/figures/geometry.png` — model geometry
- [ ] `outputs/figures/bscan.png` — B-scan with rebar hyperbolas
- [ ] `outputs/animations/wavefield.gif` — wave propagation
- [ ] `outputs/figures/inversion_result.png` — FWI recovered model
- [ ] `outputs/figures/convergence.png` — misfit convergence
- [ ] GPU benchmark results (terminal output or saved)
