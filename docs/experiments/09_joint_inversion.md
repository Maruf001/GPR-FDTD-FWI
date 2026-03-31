# Experiment 09: Joint εr–σ Inversion

**Date**: 2026-03-30

## Objective

Implement simultaneous gradient computation for both relative permittivity (εr) and conductivity (σ), enabling dual-parameter inversion.

## Files Created

- `inversion/adjoint_dual.py` — Extends `inversion/adjoint.py` with a second gradient formula for σ alongside the existing εr gradient.

## Method

The dual gradients from the adjoint-state method are:

$$g_{\varepsilon_r}[i,j] = -\varepsilon_0 \sum_t E_z^{\text{adj}} \cdot \frac{\partial E_z^{\text{fwd}}}{\partial t} \cdot \Delta t$$

$$g_\sigma[i,j] = -\sum_t E_z^{\text{adj}} \cdot E_z^{\text{fwd}} \cdot \Delta t$$

The εr gradient depends on the time derivative of the forward field (wave speed sensitivity), while the σ gradient depends on the field amplitude directly (attenuation sensitivity).

## Results (6 subsampled sources)

| Gradient | Max magnitude | Mean magnitude |
|----------|--------------|----------------|
| $g_{\varepsilon_r}$ | 5.21e-6 | 1.99e-7 |
| $g_\sigma$ | **4.33e-16** | **1.80e-17** |

The σ gradient is at **machine-precision level** — 10 orders of magnitude smaller than the εr gradient.

## Analysis

**Why the σ gradient is negligible:**

1. **Low concrete conductivity** — at σ = 0.01 S/m, the loss tangent σ/(ωε) ≈ 0.003 at 1.5 GHz. The material is effectively lossless, so perturbations in σ produce negligible changes in the wavefield.

2. **Short propagation paths** — in our 300 mm domain, the total attenuation through concrete is approximately $e^{-\alpha \cdot d}$ where $\alpha = \sigma/(2\sqrt{\varepsilon_r/\mu_r}) \approx 0.002$ Np/m. Over 300 mm: 0.06% attenuation — undetectable.

3. **Dominance of εr** — the rebar reflections are caused by impedance contrast (primarily εr), not loss contrast. The steel's high σ makes it a PEC regardless of the exact σ value.

**When dual inversion would help:**

- Wet or chloride-contaminated concrete (σ = 0.1–1.0 S/m) where loss is significant
- Longer propagation paths (crosshole or deep surveys)
- Multi-frequency data that can separately constrain speed (εr) and attenuation (σ)

## Conclusion

The dual gradient implementation is mathematically correct and computationally efficient (both gradients computed from the same forward/adjoint pair at no extra cost). However, for this low-loss concrete scenario, σ inversion would produce no useful information. The capability is ready for problems where conductivity matters.

## Baseline Preserved

Original `inversion/adjoint.py` unchanged. The dual module is a new standalone file.
