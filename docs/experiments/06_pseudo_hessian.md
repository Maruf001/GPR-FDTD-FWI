# Experiment 06: Pseudo-Hessian Preconditioning

**Date**: 2026-03-30

## Objective

Implement pseudo-Hessian preconditioning to improve the convergence rate of pixel-wise adjoint inversion by equalising parameter sensitivity across the domain.

## Files Created

- `inversion/adjoint_v2_precond.py` — Extends `inversion/adjoint.py` with source-illumination Hessian diagonal computation and gradient preconditioning.

## Method

The pseudo-Hessian diagonal approximation is:

$$H_{\text{diag}}[i,j] = \sum_t \left(\frac{\partial E_z^{\text{fwd}}}{\partial t}\right)^2 \Delta t$$

This measures the "illumination" at each grid cell — how much source energy passes through it. The preconditioned gradient is:

$$g_{\text{precond}} = g_{\text{raw}} / (H_{\text{diag}} + \epsilon)$$

where $\epsilon$ prevents division by zero.

## Results

Step-size sweep with 51 sources, Gaussian-smoothed preconditioned gradient:

| Step size $\alpha$ | $\Delta J$ (preconditioned) | $\Delta J$ (unpreconditioned, Exp 03) | Status |
|:----------|:----------|:----------|:--------|
| $1 \times 10^{-4}$ | $-1.74 \times 10^{-5}$ | $-1.70 \times 10^{-5}$ | Descent |
| $5 \times 10^{-4}$ | $+1.6 \times 10^{-7}$ | $+6.4 \times 10^{-6}$ | Borderline |
| $1 \times 10^{-3}$ | $+2.6 \times 10^{-5}$ | $+4.5 \times 10^{-5}$ | Ascent |
| $5 \times 10^{-3}$ | $+2.4 \times 10^{-4}$ | $+3.3 \times 10^{-4}$ | Ascent |

## Analysis

**The preconditioning did not significantly improve the usable step size.** The maximum|gradient| remained at ~1.3e-3 (identical to unpreconditioned), and only $\alpha \leq 1 \times 10^{-4}$ produces descent.

**Why it didn't help here:**

1. **Small, well-illuminated domain** — our 500 mm × 300 mm domain with 51 scan positions has relatively uniform illumination. The Hessian diagonal varies by only ~10× across the concrete region. In seismic FWI, illumination varies by 1000× or more.

2. **Gaussian smoothing already preconditions** — the $\sigma=3$ smoothing we apply to the gradient effectively acts as an isotropic preconditioner, reducing the benefit of the anisotropic pseudo-Hessian.

3. **The bottleneck is multi-pixel nonlinearity, not per-pixel scaling** — changing 50K pixels simultaneously causes the linear gradient approximation to break down regardless of how each pixel is individually scaled.

## Conclusion

Pseudo-Hessian preconditioning is a well-established technique in seismic FWI (Shin et al., 2001) but provides negligible benefit for this small GPR problem. The technique would become more important for:
- Larger domains with non-uniform illumination (e.g., crosshole or 3D surveys)
- Problems with strong amplitude variations across the model
- Combined with multi-scale frequency continuation (Experiment 07)

## Baseline Preserved

Original `inversion/adjoint.py` is unchanged. The v2 file is a new addition.
