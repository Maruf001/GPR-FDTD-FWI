# EM Wave Inversion Project Research Plan

Prepared on 2026-03-21

## 1. Goal

Build a focused, interview-ready solution for the electromagnetic wave simulation and inversion task:

- 2D or simplified 2.5D FDTD forward model for reinforced concrete scanning.
- Synthetic GPR-like B-scan generation from a moving transmitter/receiver pair.
- Geometry-oriented inversion to recover rebar location and approximate size/shape.
- Optional GPU acceleration for the forward and inversion loop.

This plan intentionally prioritizes a working, explainable implementation over a maximally general solver.

## 2. What to optimize for

The task is best approached as an engineering demonstration, not as a full research-grade commercial codebase.
The strongest submission will show:

1. Clear modeling assumptions.
2. A forward solver that actually runs and produces plausible radargrams.
3. A constrained inversion that visibly improves the model.
4. Honest discussion of tradeoffs, failure modes, and runtime bottlenecks.

## 3. Recommended technical scope

### 3.1 Forward solver

Use a **2D TMz FDTD solver on a Yee grid**.

State variables:
- `Ez`
- `Hx`
- `Hy`

Why this choice:
- It is explicitly acceptable in the task.
- It is the simplest physically meaningful reduction for a line-scan style GPR setup.
- It keeps implementation and debugging manageable while still allowing proper wave propagation, reflections, and B-scan generation.

### 3.2 Scene model

Use a rectangular concrete slab / half-space with embedded circular rebars.

Suggested base geometry:
- Domain width: `0.40-0.60 m`
- Domain depth: `0.20-0.30 m`
- Concrete cover above rebar center: `40-70 mm`
- Rebar radius: `8-16 mm`
- Number of rebars: start with `1`, then extend to `2-3`

Suggested material simplification:
- Concrete: relative permittivity fixed to a plausible constant, light conductivity.
- Steel: approximate as PEC for the first working version.
- Magnetic permeability fixed to `mu_r = 1` everywhere.

This is enough to recover the geometry while avoiding a harder dual-parameter inversion at the start.

### 3.3 Source / receiver / scan path

Use a moving bistatic scan:
- transmitter and receiver near the top surface,
- fixed Tx-Rx offset,
- both moved laterally across the model.

Suggested parameters:
- Center frequency: `1.0-1.5 GHz`
- Wavelet: Ricker or Gaussian-derivative pulse
- Tx-Rx offset: `30-50 mm`
- Lateral step: `2-4 mm`
- Number of A-scans: `60-120`

### 3.4 Boundary treatment

Use **PML or CPML**, with at least `10-12` cells per side.

If implementation time becomes tight:
- start with a simpler absorbing boundary or a basic PML,
- then upgrade to CPML if needed.

### 3.5 Grid spacing and time step

Choose `dx = dy` small enough to resolve both the wavelength in concrete and the rebar diameter.

Good starting point:
- `dx = dy = 2 mm`

Reasoning:
- for concrete with `eps_r ~ 6`, a `1.5 GHz` wave has wavelength about `8 cm / sqrt(6) ~ 3.3 cm`,
- 2 mm gives roughly 16 cells per wavelength,
- a 20 mm diameter bar is represented by ~10 cells.

Time step:
- enforce the 2D CFL condition,
- use a safety factor such as `0.95`.

## 4. Recommended inversion strategy

Do **not** begin with a full pixel-wise inversion over every grid cell.
That is harder to stabilize, slower, and harder to explain in an interview.

### Stage 1: geometry-parameter inversion (recommended baseline)

Represent each rebar with a small parameter vector:
- center x,
- center y,
- radius.

Optional global parameter:
- concrete permittivity.

Then optimize these parameters by minimizing waveform misfit:

`J(m) = 1/2 || d_sim(m) - d_obs ||^2 + R(m)`

Why this is the best baseline:
- small search space,
- robust enough to show successful recovery,
- easy to compare with ground truth,
- easy to discuss priors.

### Stage 2: weakly pixelated refinement (optional)

After recovering approximate rebar centers, allow local refinement on a coarse image grid around each target.

Use:
- TV regularization,
- box constraints,
- optional smoothness.

### Stage 3: dual-parameter inversion (bonus only)

Only attempt joint conductivity + permittivity inversion if the geometry-only version already works.

## 5. How to compute gradients

### Option A — practical interview path

Use a **parameterized forward model** and compute gradients with:
- automatic differentiation in JAX/PyTorch if the solver is differentiable enough, or
- finite differences over the low-dimensional parameter vector if the parameter count is tiny.

This is acceptable for a small number of parameters and is the fastest route to a successful demo.

### Option B — more faithful to the task statement

Implement an **adjoint-state method**:
- store or checkpoint the forward wavefield,
- compute data residuals at receivers,
- backpropagate the residuals through the adjoint system,
- correlate forward and adjoint wavefields to form a gradient.

For the interview, the ideal position is:
- understand the full adjoint derivation,
- implement either a simplified adjoint or a low-dimensional differentiable inversion,
- explain clearly why this was the best engineering choice under time constraints.

## 6. Software stack recommendation

### Most practical stack

- Python
- NumPy for baseline CPU version
- Matplotlib for plots/animation
- CuPy or JAX for GPU acceleration
- SciPy optimization (`L-BFGS-B`, `least_squares`) for parameter updates

### Best optional stack if GPU and autodiff are desired

- JAX for array ops, JIT, and gradients
- optional comparison to FDTDX ideas for differentiable FDTD design

### What not to do first

- do not start by modifying a huge external codebase,
- do not rely on Meep or gprMax as the main submitted solver unless the task explicitly allows wrapping an external simulator,
- do not begin with deep learning inversion.

Use external tools mainly as:
- validation references,
- parameter sanity checks,
- inspiration for solver structure.

## 7. Concrete implementation milestones

### Milestone 1 — forward solver core

Deliverables:
- Yee-grid arrays
- TMz update loop
- source injection
- simple absorbing boundary / PML
- field snapshots

Checks:
- stable run under CFL
- wave propagates outward without obvious blow-up
- metal cylinder creates reflections

### Milestone 2 — scanning and B-scan

Deliverables:
- moving Tx/Rx positions
- multi-shot acquisition loop
- stacked radargram / B-scan image
- ground-truth geometry plot

Checks:
- direct wave visible,
- hyperbola-like reflection over rebars,
- reasonable travel times.

### Milestone 3 — inversion baseline

Deliverables:
- initial model with wrong rebar positions/radii
- misfit function
- optimizer loop
- recovered model
- data comparison plots
- error metrics

Suggested metrics:
- normalized L2 data misfit,
- center-position error,
- radius error,
- IoU or overlap score of binary masks.

### Milestone 4 — animation and presentation polish

Deliverables:
- one propagation animation,
- clean figures for ground truth / initial / inverted model,
- brief explanation of assumptions and limitations.

### Milestone 5 — GPU acceleration (bonus)

Move to GPU:
- FDTD field update kernels,
- batch shot simulation,
- residual and gradient accumulation.

Benchmark:
- CPU vs GPU runtime for the same number of shots and time steps,
- note memory footprint and transfer overhead.

## 8. Key risks and mitigation

### Risk 1 — unstable solver

Mitigation:
- verify CFL,
- start with homogeneous medium,
- test source and boundaries before adding rebars.

### Risk 2 — poor inversion convergence

Mitigation:
- begin with one bar only,
- invert geometry parameters not all cells,
- window the data in time,
- normalize traces,
- use multi-scale strategy from low to high frequency.

### Risk 3 — too slow

Mitigation:
- reduce domain,
- shorten time window,
- use coarser grid for inversion than for final forward plots,
- batch shots or JIT-compile kernels.

### Risk 4 — hard to explain

Mitigation:
- keep the physical story simple,
- prepare a whiteboard-style explanation of forward wavefield, residual, adjoint wavefield, and gradient,
- show what each array means in code.

## 9. Recommended final deliverable structure

1. `README.md`
2. `fdtd_forward.py`
3. `scan_simulation.py`
4. `inversion.py`
5. `materials.py`
6. `plotting.py`
7. `outputs/`
   - geometry plot
   - B-scan image
   - animation
   - initial vs inverted vs truth
   - signal comparisons
   - runtime table

## 10. Interview talking points to prepare

Be ready to explain:
- why TMz is enough for a first-pass GPR-style line scan,
- why a circular-parameterized rebar model is a smart prior,
- why adjoint-state is more scalable than brute-force perturbation,
- where GPU acceleration matters most,
- what would be needed to extend from 2D to 2.5D / 3D,
- why conductivity-permittivity joint inversion is harder than geometry-only inversion.

## 11. Recommended order of execution

1. Homogeneous-medium pulse propagation.
2. Single PEC cylinder reflection.
3. Moving scan and B-scan.
4. One-bar inversion.
5. Two-bar inversion.
6. Add PML polish.
7. Add GPU path.
8. Add more advanced regularization only if time remains.

## 12. Bottom-line recommendation

The best version of this project is:

- **custom 2D TMz FDTD implementation**,
- **synthetic reinforced concrete B-scan generation**,
- **constrained inversion over rebar geometry parameters**,
- **clear plots, metrics, and explanation**,
- **GPU acceleration as a bonus layer**.

That scope is technically credible, realistically completable, and highly defensible in an interview.
