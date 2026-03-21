# Theory Discussion Guide — Interview Preparation (Part A)

This guide covers all topics from Section 3 of the test document. Use it to prepare clear, concise explanations for the interview.

---

## 3.1 FDTD-Based EM Forward Modeling

### Purpose of FDTD

FDTD (Finite-Difference Time-Domain) directly discretizes Maxwell's curl equations in both space and time. It converts the continuous PDE system into explicit algebraic update equations that are marched forward in time step by step. Key advantages over frequency-domain methods:

- **Wideband**: A single simulation covers all frequencies in the source bandwidth
- **Handles complex media**: Inhomogeneous, lossy, dispersive, nonlinear materials
- **Intuitive**: The fields evolve physically in time — easy to visualize and debug
- **Scalable**: Embarrassingly parallel for GPU acceleration

### The Yee Grid (1966)

The fundamental innovation by Kane Yee: E and H field components are **staggered** in space by half a grid cell and in time by half a time step.

For 2D TMz polarization:
```
Ez lives at integer grid points:        (i, j)
Hx lives at half-step in z direction:   (i, j+1/2)
Hy lives at half-step in x direction:   (i+1/2, j)
```

Why staggering matters:
1. Central-difference approximations become **second-order accurate** automatically
2. The divergence conditions (∇·B = 0, ∇·D = ρ) are **satisfied implicitly**
3. Combined with leapfrog time stepping, the scheme is **dissipation-free** (energy-conserving in lossless media)

### Main Time-Stepping Loop (Leapfrog)

Each time step alternates between H and E updates:

```
for n = 0 to Nt:
    1. Update H from E:   H^{n+1/2} from E^n        [H jumps half step forward]
    2. Apply CPML corrections to H
    3. Update E from H:   E^{n+1}   from H^{n+1/2}   [E jumps one step forward]
    4. Apply CPML corrections to E
    5. Inject source into Ez
    6. Record Ez at receiver
```

The leapfrog structure means E and H are never known at the same instant — they interleave in time.

### Update Equations (2D TMz)

Maxwell's equations for TMz (no variation in y-direction):

```
∂Hx/∂t = -(1/μ) · ∂Ez/∂z
∂Hy/∂t =  (1/μ) · ∂Ez/∂x
∂Ez/∂t =  (1/ε) · (∂Hy/∂x - ∂Hx/∂z) - (σ/ε) · Ez
```

Discretized with central differences on the Yee grid:

```
Hx^{n+1/2}[i,j] = Hx^{n-1/2}[i,j] - (dt/(μ·dz)) · (Ez^n[i,j+1] - Ez^n[i,j])

Hy^{n+1/2}[i,j] = Hy^{n-1/2}[i,j] + (dt/(μ·dx)) · (Ez^n[i+1,j] - Ez^n[i,j])

Ez^{n+1}[i,j] = Ca · Ez^n[i,j] + Cb · ((Hy[i,j]-Hy[i-1,j])/dx - (Hx[i,j]-Hx[i,j-1])/dz)
```

where the coefficients incorporate conductivity losses:
```
Ca = (1 - σ·dt/(2ε)) / (1 + σ·dt/(2ε))
Cb = (dt/ε) / (1 + σ·dt/(2ε))
```

Ca < 1 introduces exponential damping (loss). For σ = 0 (lossless), Ca = 1 and Cb = dt/ε.

### Source Injection

We use a **soft source** (additive): `Ez[src] += source_value`

This is preferred over a hard source (`Ez[src] = source_value`) because:
- It does not create artificial reflections from the source point
- The source acts like a current density Jz driving the field

The **Ricker wavelet** (second derivative of Gaussian) is used:
```
w(t) = (1 - 2(π·fc·τ)²) · exp(-(π·fc·τ)²),   τ = t - 1/fc
```

Properties: zero DC component, peaked at fc, bandwidth ~ 2.5·fc.

### Boundary Conditions

Without absorbing boundaries, waves reflect from domain edges (PEC boundary by default).

**CPML** (Convolutional Perfectly Matched Layer):
- Creates an artificial absorbing layer at domain boundaries
- Impedance-matched at the interface → zero theoretical reflection
- Exponential attenuation inside the layer
- Uses polynomial-graded conductivity: σ(d) = σ_max · (d/L)^m
- CFS variant adds κ and α parameters for wideband performance
- Implemented via recursive auxiliary variables (ψ fields)

### Numerical Stability

**CFL condition** (Courant-Friedrichs-Lewy):
```
dt ≤ 1 / (c · √(1/dx² + 1/dz²))
```

For a square grid (dx = dz): `dt ≤ dx / (c · √2)`

Physical meaning: information cannot propagate more than one grid cell per time step. Violating this causes exponential field growth (instability).

**Numerical dispersion**: discrete waves travel slightly slower than continuous waves. Controlled by using ≥15-20 grid points per wavelength.

---

## 3.2 Adjoint-State Inversion from EM Data

### Objective Function

The least-squares misfit measures data discrepancy:

```
J(m) = (1/2) · Σ_{s,r,t} |d_obs(s,r,t) - d_syn(s,r,t; m)|²
```

where m is the model (e.g., εr distribution), d_obs is observed data, d_syn is synthetic data from forward simulation.

### Why Direct Perturbation is Too Expensive

To compute ∂J/∂m_i for each of N model parameters:
- Finite-difference approach: perturb m_i → run forward simulation → compute ΔJ
- Cost: **N forward simulations** (one per parameter)
- For a 250×150 grid = 37,500 parameters → 37,500 forward simulations
- Completely impractical!

### How the Adjoint-State Method Computes Gradients Efficiently

The adjoint method uses the **Lagrangian formulation** with the PDE as a constraint:

```
L(m, u, λ) = J(u) + <λ, F(m,u)>
```

where u is the wavefield, F(m,u) = 0 is the wave equation, λ is the Lagrange multiplier (adjoint field).

Setting ∂L/∂u = 0 gives the **adjoint equation** — a wave equation with a special source. The gradient is then:

```
dJ/dm = ∂L/∂m = <λ, ∂F/∂m · u>
```

**Cost: only 2 simulations** (one forward + one adjoint) regardless of the number of parameters!

### Wavefield Meanings

| Term | Description | How it's computed |
|------|-------------|-------------------|
| **Forward wavefield** (u_fwd) | Physical wave propagation from Tx through current model | Standard FDTD forward simulation |
| **Residual** (r) | Data discrepancy: r = d_syn - d_obs | Difference of traces at Rx |
| **Adjoint wavefield** (u_adj) | Sensitivity carrier: propagates time-reversed residual backward | FDTD simulation with time-reversed residual injected at Rx |
| **Gradient** (g) | Sensitivity of J to model parameters at each grid point | Cross-correlation of forward and adjoint fields |

### Gradient Formula

For relative permittivity εr:

```
g_εr[i,j] = -ε0 · Σ_t { Ez_adj[i,j,t] · ∂Ez_fwd[i,j,t]/∂t } · dt
```

Intuition:
- The forward field carries information about how the source illuminates each point
- The adjoint field carries information about how sensitive the data residual is to each point
- Their cross-correlation identifies where model changes would most reduce the misfit

### Model Parameter Updates

1. Compute gradient g via adjoint method
2. Choose search direction d (steepest descent: d = -g; L-BFGS: d ≈ -H⁻¹g)
3. Line search for step length α: find α that sufficiently reduces J
4. Update: m_{k+1} = m_k + α · d
5. Apply bounds: εr ∈ [1, 15]
6. Add regularization (TV) to gradient for sharp boundary recovery
7. Repeat until convergence

---

## 3.3 GPU/CUDA Acceleration

### Which Operations to Move to GPU

The FDTD update equations are **embarrassingly parallel**: each grid cell's update depends only on its immediate neighbors. This maps perfectly to CUDA's SIMT model.

| Operation | GPU suitability | Reasoning |
|-----------|----------------|-----------|
| H-field update | Excellent | Each cell reads 2 values of Ez, writes 1 H value — independent per cell |
| E-field update | Excellent | Each cell reads 2 values of H, writes 1 E value — independent per cell |
| CPML auxiliary updates | Good | Same stencil pattern, restricted to PML boundary regions |
| Source injection | Trivial | Single point write |
| Gradient accumulation | Excellent | Element-wise multiply-accumulate at every cell |

**Typical speedup**: 30-80x over CPU implementations for FDTD.

### What Stays on CPU

- **Parameter setup** (one-time cost, negligible)
- **Optimization loop control** (L-BFGS iterations, very lightweight)
- **I/O** (saving results to disk)

### Practical Issues

**Memory usage**:
- Field arrays (Ez, Hx, Hy): 3 × Nz × Nx × 8 bytes = ~1.2 MB for our grid
- CPML auxiliary variables: ~0.5 MB
- For adjoint: storing all forward fields = Nt × Nz × Nx × 8 ≈ 770 MB (fits on modern GPUs with 8+ GB VRAM)
- Total for our problem: well within GPU memory limits

**Memory access patterns**:
- FDTD stencils access neighboring cells in both x and z directions
- **Row-major (C-order) storage** ensures that x-direction neighbors are contiguous in memory
- Adjacent threads should process adjacent x-indices → **coalesced memory access** → maximum bandwidth utilization
- Thread block size: typically 16×16 or 32×8, tuned to GPU architecture

**CPU-GPU communication**:
- **Minimize transfers**: keep all field arrays on GPU throughout the simulation
- **Only transfer receiver trace** back to CPU each step (single float64 value — negligible overhead)
- **Transfer gradient** back to CPU once per inversion iteration (single Nz×Nx array)
- Avoid transferring entire field arrays unless needed for visualization/checkpointing

### Implementation Options

1. **CuPy** (drop-in NumPy replacement): minimal code changes, same vectorized syntax
2. **Numba CUDA kernels**: explicit thread control, custom kernels for maximum performance
3. **PyTorch**: automatic differentiation for gradients, but overhead for small problems

For this project, CuPy is the best choice: it demonstrates GPU awareness without excessive implementation complexity.
