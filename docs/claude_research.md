The plan is written. Here's a summary of what I've designed:

  Project Overview

  A complete 2D TMz FDTD electromagnetic simulator + adjoint-state full-waveform inversion for GPR concrete/rebar
  scanning, built from scratch in Python (NumPy + Numba for speed).

  Structure — 5 phases:

  1. Core Forward Engine — FDTD with CPML absorbing boundaries, Ricker wavelet source, material models for
  concrete/rebar/air
  2. Scanning & Visualization — Multi-position B-scan acquisition, geometry plots, wave propagation animation
  3. Adjoint-State Inversion — Gradient computation via forward+adjoint cross-correlation, TV regularization, L-BFGS-B
   optimization to recover rebar εr
  4. GPU Acceleration (bonus) — CuPy or Numba CUDA for field updates
  5. Documentation & Tests — Theory guide for Part A interview prep, parameter justification doc, gradient
  verification tests

  Key parameters (all justified):

  - 1.5 GHz Ricker wavelet, 2mm grid spacing, 0.9 Courant factor
  - 3 rebars at 50mm cover, 100mm spacing, 6mm radius in concrete (εr=6, σ=0.01)
  - CPML with 15 layers, 280×180 grid, ~1887 time steps

  Deliverables:

  - Well-organized folder structure (core/, inversion/, gpu/, visualization/, tests/, docs/)
  - Three entry-point scripts: run_forward.py, run_inversion.py, run_benchmark.py
  - Theory guide + parameter justification docs for interview preparation

⏺ User approved Claude's plan
  ⎿  Plan saved to: ~/.claude/plans/eager-pondering-moore.md · /plan to edit
     FDTD GPR Simulation & Adjoint-State Inversion — Implementation Plan

     Context

     This project implements a 2D FDTD (Finite-Difference Time-Domain) electromagnetic wave simulator and
     adjoint-state full-waveform inversion for a GPR (Ground Penetrating Radar) reinforced concrete scanning scenario.
      It is for a Cambridge/Inframind research position interview (Haibing Wu, Brian Sheil). The candidate must
     demonstrate a working implementation and explain the theory during a screen-share interview.

     The deliverables are:
     - Part A: Theory discussion preparation (FDTD, adjoint-state, GPU/CUDA)
     - Part B.1: Forward FDTD simulation with B-scan and animation outputs
     - Part B.2: Adjoint-state inversion to recover rebar geometry
     - Part B.3 (bonus): CUDA/GPU acceleration with benchmarks

     ---
     Project Structure

     FTDT_Project/
     ├── note.txt                              # (existing)
     ├── EM_wave_inversion_tests_for_Infra_applicants.pdf  # (existing)
     ├── research_plan.md                      # This research plan (high-level)
     ├── requirements.txt                      # Dependencies
     │
     ├── config.py                             # All parameters with justifications
     ├── run_forward.py                        # Entry: forward sim → B-scan + animation
     ├── run_inversion.py                      # Entry: adjoint-state FWI
     ├── run_benchmark.py                      # Entry: CPU vs GPU timing (bonus)
     │
     ├── core/
     │   ├── __init__.py
     │   ├── materials.py                      # MaterialModel class (eps_r, sigma, mu_r arrays)
     │   ├── geometry.py                       # Build rebar model + initial model
     │   ├── source.py                         # Ricker wavelet generation
     │   ├── fdtd.py                           # 2D TMz FDTD engine (update_H, update_E, FDTDSimulator)
     │   ├── cpml.py                           # CPML absorbing boundary (coefficients + psi fields)
     │   ├── scan.py                           # B-scan multi-position scanning
     │   └── utils.py                          # CFL check, wavelength calc, helpers
     │
     ├── inversion/
     │   ├── __init__.py
     │   ├── objective.py                      # L2 misfit + residual computation
     │   ├── adjoint.py                        # Adjoint wavefield + gradient cross-correlation
     │   ├── regularization.py                 # Total Variation (TV) regularization
     │   ├── optimizer.py                      # L-BFGS-B wrapper (scipy)
     │   └── inversion_engine.py              # Full inversion loop orchestration
     │
     ├── gpu/                                  # (bonus)
     │   ├── __init__.py
     │   ├── fdtd_gpu.py                       # CuPy/Numba CUDA FDTD
     │   └── benchmark.py                      # Timing utilities
     │
     ├── visualization/
     │   ├── __init__.py
     │   ├── plot_geometry.py                  # Ground-truth model plot
     │   ├── plot_bscan.py                     # B-scan radargram
     │   ├── plot_wavefield.py                 # EM wave propagation animation
     │   ├── plot_inversion.py                 # Initial/inverted/true model comparison
     │   └── plot_signals.py                   # Signal comparison + convergence
     │
     ├── tests/
     │   ├── test_fdtd_free_space.py           # Wave speed verification
     │   ├── test_reflection.py               # Reflection coefficient at interface
     │   ├── test_cpml.py                      # PML absorption quality
     │   ├── test_ricker.py                    # Wavelet spectrum check
     │   ├── test_gradient.py                  # Adjoint vs finite-difference gradient
     │   └── test_cfl.py                       # Stability condition
     │
     ├── outputs/                              # Generated at runtime
     │   ├── figures/
     │   ├── animations/
     │   └── data/
     │
     └── docs/
         ├── theory_guide.md                   # Part A interview prep (FDTD, adjoint, GPU)
         └── parameter_justifications.md       # Why each parameter was chosen

     ---
     Implementation Phases

     Phase 1: Core Forward Engine

     Files: config.py, core/utils.py, core/materials.py, core/geometry.py, core/source.py, core/cpml.py, core/fdtd.py

     1. config.py — All constants and parameters:
       - Physical: C0, EPS0, MU0
       - Materials: concrete (εr=6, σ=0.01), rebar (εr=1, σ=1e7, effectively PEC), air (εr=1, σ=0), all μr=1
       - Source: Ricker wavelet at fc=1.5 GHz (standard for concrete GPR)
       - Geometry: 500mm × 300mm domain, 40mm air layer, 3 rebars at 50mm cover depth, 100mm spacing, 6mm radius
       - Grid: dx=dz=2mm (≥16 points/wavelength in concrete), Courant=0.9 → dt≈4.24ps
       - CPML: 15 layers, cubic grading, kappa_max=5, alpha_max=0.05
       - Scanning: 50–450mm range, 4mm step, 20mm Tx-Rx offset
       - Total grid: 280×180 cells, ~1887 time steps for 8ns window
     2. core/fdtd.py — TMz mode with Ez, Hx, Hy:
       - Yee grid: Ez at (i,j), Hx at (i,j+½), Hy at (i+½,j)
       - Leapfrog: H update → CPML H correction → E update → CPML E correction → source inject
       - Update equations:
       Hx[i,j] -= dt/(μ·dz) · (Ez[i,j+1] - Ez[i,j])
     Hy[i,j] += dt/(μ·dx) · (Ez[i+1,j] - Ez[i,j])
     Ez[i,j]  = Ca·Ez[i,j] + Cb·((Hy[i,j]-Hy[i-1,j])/dx - (Hx[i,j]-Hx[i,j-1])/dz)
       - Use Numba @njit for inner loops (clear mapping to equations, near-C speed)
       - Also provide vectorized NumPy fallback
     3. core/cpml.py — Convolutional PML:
       - CFS-PML stretching: s(ω) = κ + σ/(α + jω)
       - Auxiliary variables: ψ updated recursively with b,a coefficients
       - Graded profiles: σ(d) = σ_max·(d/L)^3, κ(d) = 1+(κ_max-1)·(d/L)^3, α(d) = α_max·(1-d/L)

     Phase 2: Scanning & Visualization

     Files: core/scan.py, visualization/plot_*.py, run_forward.py

     4. core/scan.py — For each scan position: reset fields → run forward → record trace → assemble B-scan
     5. Visualizations: geometry plot, B-scan (seismic colormap), wavefield animation (FuncAnimation → GIF/MP4)

     Phase 3: Adjoint-State Inversion

     Files: inversion/objective.py, inversion/adjoint.py, inversion/regularization.py, inversion/optimizer.py,
     inversion/inversion_engine.py, run_inversion.py

     6. Objective: J = ½ ||d_obs - d_syn||², residual r = d_syn - d_obs
     7. Adjoint gradient: For each source:
       - Forward sim → store all Ez fields
       - Adjoint sim: inject time-reversed residual at Rx, run same FDTD
       - Gradient: g_εr[i,j] = -ε0 · Σ_t { Ez_adj · ∂Ez_fwd/∂t } · dt
       - Sum over all sources
     8. TV regularization: TV(m) = Σ √(|∇m|² + β²), gradient = -div(∇m/|∇m|_β)
     9. Optimizer: scipy L-BFGS-B with bounds εr ∈ [1, 15]
     10. Inversion loop: generate d_obs from true model → iterate (forward → residual → adjoint → gradient + TV →
     L-BFGS update → clip bounds) × 30 iterations

     Phase 4: GPU Acceleration (Bonus)

     Files: gpu/fdtd_gpu.py, gpu/benchmark.py, run_benchmark.py

     11. CuPy drop-in replacement for NumPy arrays on GPU
     12. Alternatively: Numba CUDA kernels for explicit thread control
     13. Operations on GPU: H update, E update, CPML, source inject, gradient accumulation
     14. Minimize CPU↔GPU transfers: only receiver trace goes to CPU each step

     Phase 5: Documentation & Tests

     Files: docs/theory_guide.md, docs/parameter_justifications.md, tests/*

     15. Theory guide covering all Part A discussion points
     16. Parameter justification document (for interview walk-through)
     17. Key tests: free-space wave speed, reflection coefficient, CPML absorption, gradient verification

     ---
     Key Design Decisions

     ┌──────────────────┬──────────────────┬───────────────────────────────────────────────────────────────────────┐
     │     Decision     │      Choice      │                               Rationale                               │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Polarization     │ TMz (Ez, Hx, Hy) │ Standard for 2D GPR, rebars are perpendicular to scan plane           │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Grid spacing     │ 2mm              │ ≥16 pts/wavelength at f_max in concrete, resolves 12mm rebars         │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Frequency        │ 1.5 GHz          │ Standard for concrete inspection, good penetration/resolution balance │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Boundary         │ CPML             │ Wideband, media-independent, no field splitting needed                │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Inversion target │ εr only          │ Sufficient contrast for PEC rebars; σ fixed (simplifying prior)       │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Optimizer        │ L-BFGS-B         │ Quasi-Newton with bounds; robust, well-tested in scipy                │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Regularization   │ TV               │ Promotes sharp boundaries — ideal for concrete/rebar interface        │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ Acceleration     │ Numba @njit      │ Near-C speed, readable code, easy interview walkthrough               │
     ├──────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────┤
     │ GPU              │ CuPy             │ Drop-in NumPy replacement, minimal code changes                       │
     └──────────────────┴──────────────────┴───────────────────────────────────────────────────────────────────────┘

     ---
     Verification Strategy

     1. Free-space wave speed: Measure arrival time → verify v = c0 ± 1%
     2. Reflection coefficient: Air-concrete interface → R_theory = -0.420
     3. CPML absorption: Compare truncated vs large domain → reflections < -40 dB
     4. Ricker spectrum: FFT peak at f_center
     5. Gradient test (critical): Adjoint gradient vs finite-difference gradient on small grid → relative error < 1%

     ---
     Reference Repositories (studied during research)

     - Fast-GPR-FWI (PyTorch+CUDA, dual-parameter) — architecture reference for inversion
     - GPR-FWI-Py (pure Python, multi-scale+TV) — closest to our approach
     - gprMax (Cython/CUDA, mature) — forward modeling reference
     - MEEP (C++/Python, adjoint solver) — adjoint implementation reference
     - FDTDX (JAX, time-reversible AD) — gradient computation concepts

     Key Papers

     - Ernst et al. (2007) — FWI of crosshole radar with 2D FDTD
     - Meles et al. (2010) — Simultaneous εr + σ inversion
     - Meles et al. (2012) — FDTD adjoint sensitivity analysis
     - Kuroda et al. (2007) — Conjugate gradient FWI for GPR
     - Roden & Gedney (2000) — CPML formulation