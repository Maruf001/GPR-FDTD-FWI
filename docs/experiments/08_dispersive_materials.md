# Experiment 08: Dispersive Materials (Debye Model)

**Date**: 2026-03-30

## Objective

Implement frequency-dependent permittivity in the FDTD solver using a single-pole Debye relaxation model via Auxiliary Differential Equations (ADE).

## Files Created

- `core/materials_dispersive.py` — `DispersiveMaterialModel` extending `MaterialModel` with Debye parameters (eps_inf, eps_static, tau) and ADE coefficient computation.
- `core/fdtd_dispersive.py` — `FDTDSimulatorDispersive` extending `FDTDSimulator` with polarisation current (Jp) update in the time-stepping loop.

## Method

The Debye relaxation model:

$$\varepsilon(\omega) = \varepsilon_\infty + \frac{\varepsilon_s - \varepsilon_\infty}{1 + j\omega\tau}$$

is implemented as an ADE that introduces a polarisation current $J_p$:

$$J_p^{n+1} = C_1 \cdot J_p^n + C_2 \cdot E_z^{n+1}$$

where $C_1 = \exp(-\Delta t / \tau)$ and $C_2 = \varepsilon_0 (\varepsilon_s - \varepsilon_\infty) / \tau \cdot (1 - \exp(-\Delta t / \tau))$.

The E-field update uses $\varepsilon_\infty$ (not $\varepsilon_s$) for the instantaneous permittivity, with the polarisation current subtracted from the curl term.

## Test Setup

- Homogeneous concrete domain (no rebars)
- Non-dispersive: $\varepsilon_r = 6.0$ (constant)
- Dispersive: $\varepsilon_\infty = 5.0$, $\varepsilon_s = 7.0$, $\tau = 0.1$ ns
- Source: 1.5 GHz Ricker wavelet
- Receiver: 200 mm depth in concrete

## Results

| Metric | Value |
|--------|-------|
| Max amplitude (non-dispersive) | 6.74e-3 |
| Max amplitude (dispersive) | 2.14e-3 |
| RMS trace difference | 1.38e-3 |
| **Relative RMS difference** | **20.4%** |
| Numerically stable | Yes |

## Analysis

The dispersive model produces a **20% RMS difference** from the non-dispersive reference — a physically significant effect. The key observations:

1. **Lower amplitude** in the dispersive case (2.1e-3 vs 6.7e-3) because the Debye relaxation converts EM energy into heat at a rate proportional to $(\varepsilon_s - \varepsilon_\infty) / \tau$.

2. **Pulse broadening** due to frequency-dependent velocity: lower frequencies see $\varepsilon_s = 7.0$ (slower) while higher frequencies see $\varepsilon_\infty = 5.0$ (faster), spreading the pulse in time.

3. **Stability confirmed** — the ADE formulation is unconditionally stable for $\tau > 0$ (exponential decay in $C_1$).

**Practical relevance**: For dry concrete at 1–2 GHz, the dispersion is moderate ($\varepsilon_r$ varies by ~1–2 units across the band). The 20% effect is significant enough to matter for quantitative FWI but may be negligible for rebar detection (which is primarily a travel-time problem).

## Baseline Preserved

Original `core/materials.py` and `core/fdtd.py` unchanged. Dispersive files are new additions that extend the originals via inheritance.
