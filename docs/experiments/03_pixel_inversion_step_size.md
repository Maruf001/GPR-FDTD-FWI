# Experiment 03: Pixel-Wise Inversion — Step Size Analysis

**Date**: 2026-03-30

## Problem Statement

The adjoint gradient is mathematically correct (validated in Exp 02), but the L-BFGS-B and steepest descent optimizers fail to reduce the misfit.

## Setup

- 51 sources, initial model = homogeneous concrete, observed data from true model (3 rebars)
- Per-source normalized gradient + L-BFGS-B, or steepest descent with various step sizes
- Total parameters: 50,400 (every grid pixel)

## Root Causes Discovered

### Issue 1: Per-source gradient normalization breaks L-BFGS-B

Each source's gradient was normalized to max=1 independently. This:
- Gives equal weight to weak sources (far from rebars) and strong sources (above rebars)
- Destroys the curvature information L-BFGS-B needs (gradients at different iterations have artificially constant magnitude)
- Result: L-BFGS-B made one step then stalled at J=14.00123

**Fix**: Removed per-source normalization. Only normalize the total gradient once, or don't normalize at all for L-BFGS-B.

### Issue 2: Raw gradient magnitude too small for L-BFGS-B initial Hessian

With raw (unnormalized) gradient, max|grad| ≈ 1e-2. L-BFGS-B's initial step with H0=I is ~1e-2 in eps_r, producing negligible misfit change (dJ ≈ 1e-15).

**Fix**: Added fixed gradient scaling (1/max|grad|) applied consistently to ALL evaluations. This preserves relative gradient changes while making the initial step size ~1.

### Issue 3: 50K pixels changing simultaneously causes massive overshoot

Even with correct gradient, changing all 50K pixels simultaneously makes the linear approximation terrible.

**Step-size sweep results (51 sources, Gaussian smoothed gradient, sigma=3):**

| alpha | dJ | Status |
|-------|-----|--------|
| 5e-5 | -1.75e-5 | descent |
| 1e-4 | -1.70e-5 | descent |
| 3e-4 | -7.5e-6 | descent |
| 5e-4 | +6.4e-6 | ascent |
| 1e-3 | +5.8e-5 | ascent |
| 3e-3 | +2.3e-4 | ascent |

**Only alpha ≤ 3e-4 produces descent.**

### Issue 4: Convergence rate is impractically slow

At the best step (alpha=1e-4), dJ ≈ -1.7e-5 per iteration from J=14.0. To recover rebars (eps_r change from 6→1), would need:
- Change of 5 in eps_r at rebar pixels
- At alpha=1e-4 per iteration: ~50,000 iterations
- Runtime: ~50,000 × 3 min = ~100 days

### Why the gradient is so small

The adjoint gradient formula gives: g[i,j] ≈ -(1/eps_r) × dJ/d(eps_r[i,j])

This means the gradient we compute is the PHYSICAL gradient divided by eps_r (~6). The predicted descent per step:
```
dJ = -(alpha/eps_r) × ||grad||² / max(|grad|)
   = -(1e-4 / 6) × (3.7e-2)² / 1.3e-3
   = -1.76e-5
```
This matches the observed -1.7e-5 perfectly.

## Approaches Tried That Did NOT Work

| Approach | Result | Why |
|----------|--------|-----|
| L-BFGS-B with normalized gradient | Stalled at J=14.00123 | Curvature estimation broken by normalization |
| L-BFGS-B with raw + fixed scaling | Stalled after 1 iteration | Line search couldn't find descent |
| Steepest descent (alpha=0.1) | J increased to 41.7 | Step way too large |
| Steepest descent (alpha=2e-4) | J increased over 8 iter | Still too large without smoothing |
| Gaussian smoothing + small step | Descent at alpha=1e-4 but impractically slow | ~50,000 iter needed |
| Time-domain muting | No improvement | Dominant misfit from rebar reflections, not direct wave |

## Conclusion

Pixel-wise adjoint inversion with 50K parameters is theoretically correct but converges impractically slowly for this problem:
1. The usable step size is O(1e-4) due to 50K simultaneous pixel changes
2. The convergence rate is O(1e-5) per iteration from J=14
3. Would need advanced preconditioning (pseudo-Hessian, source-illumination normalization) for practical convergence

**Decision**: Switch to geometry-based inversion (9 parameters instead of 50K) which is fast, practical, and demonstrates the concept effectively.
