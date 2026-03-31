# Interview Cheat Sheet — Tough Questions & Strong Answers

Complements `theory_guide.md`. Focus: questions an expert interviewer would ask to probe depth of understanding.

---

## Forward Modeling Questions

### "Why TMz and not TEz?"

TMz has Ez, Hx, Hy. The rebars are infinitely long cylinders perpendicular to the scan plane (into the page). For this geometry, the electric field polarized along the rebar axis (Ez) creates the strongest scattering response. TEz would have Hz polarized along the rebar — weaker contrast because the magnetic permeability contrast is negligible (mu_r = 1 everywhere). TMz is the standard choice for GPR line scans over parallel rebars.

### "Why not use a higher-order FDTD scheme?"

Second-order Yee scheme is standard and sufficient at 16+ points per wavelength. Higher-order (4th-order in space) would allow coarser grids but: (1) complicates PML implementation significantly, (2) wider stencil creates issues at material interfaces, (3) the grid is small enough that computation isn't the bottleneck. The trade-off doesn't pay off for this problem size.

### "What happens if you reduce grid points per wavelength to 5?"

Severe numerical dispersion — waves travel slower than they should in the discrete grid. The B-scan hyperbolas would shift to later arrival times, giving incorrect depth estimates. At 5 pts/wavelength, the dispersion error can exceed 5%. The Yee scheme needs 10+ for acceptable accuracy, and 15-20 for good accuracy.

### "Why is your time step 90% of CFL, not 99%?"

At exactly CFL, numerical dispersion is zero along the grid axes but maximum along diagonals (45 degrees). A slight reduction (0.9) provides a margin for rounding errors and reduces anisotropic dispersion. Going lower (e.g., 0.5) wastes computation. 0.9 is a well-established practical choice (Taflove & Hagness recommend 0.9-0.95).

### "How does your PML handle evanescent waves?"

That's exactly why we use CFS-PML (Complex Frequency Shifted). Standard PML absorbs propagating waves but can amplify evanescent/near-field waves, causing late-time instability. The CFS extension adds the alpha parameter (alpha_max = 0.05) which shifts the pole away from the origin in frequency domain, stabilizing evanescent wave absorption. The kappa parameter (kappa_max = 5) provides coordinate stretching that improves absorption of waves at grazing incidence.

### "Why a soft source instead of hard source?"

Hard source (`Ez = value`) creates an artificial PEC point — waves reflect off the source location. Soft source (`Ez += value`) is equivalent to injecting a current density Jz, which radiates freely without creating spurious reflections. Critical for GPR simulation where the source is inside the computational domain, not on a boundary.

---

## Inversion Questions

### "Walk me through the adjoint gradient derivation"

1. Define the Lagrangian: L = J(d) + <lambda, A*u - s> where A is the wave operator, u is the field, s is the source
2. Take dL/du = 0 → get the adjoint equation: A^T * lambda = -dJ/dd (data residual injected at receivers)
3. The adjoint equation is the same FDTD but run backward in time with time-reversed residual as source
4. Then dJ/dm = <lambda, dA/dm * u> which, for epsilon_r, gives the cross-correlation formula: g = -eps0 * sum_t(Ez_adj * dEz_fwd/dt) * dt
5. Key insight: this costs only 2 simulations per source (forward + adjoint) regardless of parameter count

### "Why normalize the gradient instead of using the physical magnitude?"

The raw adjoint gradient has magnitude ~1e-17 because it's the product of two very small field quantities (Ez values ~1e-3) times eps0 (~8.85e-12) times dt (~4.24e-12). While physically correct, this magnitude is near machine precision, making finite-precision line search impossible. Normalizing to unit max preserves the direction (which determines WHERE to update) while letting L-BFGS-B's line search determine HOW MUCH to update. This is a standard practice in seismic FWI (see Virieux & Operto 2009).

### "What are the limitations of your inversion?"

1. **Local minimum**: Gradient-based methods find local minima. If the initial model is too far from truth, inversion can converge to a wrong model. Mitigation: start from a reasonable prior (homogeneous concrete).
2. **Cycle-skipping**: If predicted and observed waveforms differ by more than half a cycle, the gradient points the wrong way. Mitigation: use low-frequency content first (multi-scale approach, not implemented here).
3. **Crosstalk**: We invert only epsilon_r but conductivity also affects the data. Any epsilon_r change that compensates for conductivity effects is a false positive. Mitigation: TV regularization helps by penalizing smooth gradients.
4. **Resolution**: Limited by wavelength — cannot recover features smaller than ~lambda/2 (about 40 mm in concrete at 1.5 GHz). The rebars (12 mm) are detected by their impedance contrast, not geometrically resolved.

### "Why TV regularization specifically?"

TV (Total Variation) promotes piecewise-constant models with sharp interfaces. This is physically appropriate because the concrete/rebar boundary IS a sharp discontinuity — there's no smooth gradient between concrete (eps_r=6) and steel (eps_r~1). L2 regularization would smooth this boundary, reducing recovery quality. TV is the right prior for this geometry.

### "How would you extend this to dual-parameter inversion (eps_r AND sigma)?"

1. Derive a second gradient formula for sigma: g_sigma = -sum_t(Ez_adj * Ez_fwd) * dt (different kernel, no time derivative)
2. Apply separate step sizes for each parameter (they have different sensitivities)
3. Use cross-gradient regularization to enforce structural similarity between eps_r and sigma models
4. Main challenge: ill-posedness increases — more unknowns with the same data. Would need more data (multiple frequencies, wider aperture) or stronger priors.

---

## GPU Questions

### "Why is your GPU slower at the project grid size?"

The project grid (180x280 = 50K cells) is too small to saturate the GPU's parallelism. Each CUDA kernel launch has ~10-50 microsecond overhead, and memory transfer latency dominates when there's not enough arithmetic to amortize it. Our scaling benchmark shows the crossover: GPU becomes faster at ~50K cells and reaches 7x speedup at 800K cells. Real-world GPR problems (3D, fine grids) have millions of cells where GPU speedup is 30-100x.

### "Why CuPy instead of writing CUDA kernels?"

1. **Correctness first**: CuPy is a drop-in NumPy replacement — same code, same equations, easy to verify
2. **Development speed**: Writing custom CUDA kernels for the FDTD stencil is straightforward but requires managing thread blocks, shared memory, boundary handling
3. **Sufficient for this grid**: At our problem size, CuPy's overhead is negligible compared to custom kernels
4. **Production path**: If we needed maximum performance, I'd write custom CUDA kernels for the stencil operations (3x3 stencil maps cleanly to GPU shared memory tiles) and use PyTorch for autodiff-based gradient computation

### "What would you do differently for a production GPU implementation?"

1. **Port CPML to GPU**: Currently only field updates are on GPU. CPML corrections add ~10-20% overhead
2. **Fuse kernels**: Combine H-update + CPML into a single kernel to reduce memory traffic
3. **Use shared memory**: Load 2D tile + halo into shared memory for the stencil operations
4. **Checkpointing**: Instead of storing all forward fields (760 MB), use binomial checkpointing to reduce memory to O(sqrt(N)) with modest recomputation cost
5. **Multi-GPU**: Domain decomposition along x-axis with halo exchange (1 cell overlap needed for Yee stencil)

---

## Extension Questions

### "How would you go from 2D to 3D?"

1. Add the third field components: Ex, Ey, Hz (full 6-component Maxwell)
2. Grid becomes 3D: memory scales as N^3 instead of N^2
3. PML needed on 6 faces instead of 4 edges
4. Computation scales dramatically — GPU acceleration becomes essential
5. Main challenge: memory for adjoint (storing all fields) — would need checkpointing

### "How would you handle dispersive concrete?"

Real concrete is dispersive — permittivity and conductivity vary with frequency. Model using auxiliary differential equations (ADE): add Debye or Cole-Cole relaxation terms to the E-field update. Each pole adds one auxiliary variable per cell. For GPR in concrete, a single Debye pole is usually sufficient to capture the frequency dependence across the 0.5-3 GHz band.

### "What about antenna modeling?"

Our point source is an idealization. Real GPR antennas have:
1. Finite size (bow-tie pattern, ~10 cm)
2. Radiation pattern (not omnidirectional)
3. Feed impedance and matching
4. Near-field coupling with the ground

For more realistic simulation: model the antenna geometry explicitly (metallic arms + feed gap) or use a measured/computed antenna transfer function convolved with the source wavelet. gprMax uses explicit antenna modeling.

---

## DGX Spark Specific

### Hardware specs to mention:
- NVIDIA GB10 GPU
- 128 GB unified memory (no separate CPU/GPU memory — simplifies large-problem deployment)
- CUDA 13.0
- ARM architecture (aarch64)

### Results to show:
- Forward B-scan: 3 clear rebar hyperbolas
- Inversion: rebar recovery from blind start
- GPU scaling: 3-7x speedup (would be 30-100x for production-size 3D problems)
- All tests passing (6/6)
