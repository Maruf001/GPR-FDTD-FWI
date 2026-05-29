# Quadratic Wasserstein GPR-FWI 2024: Technical Notes

Source PDF:

```text
paper/FWI_twoParam_GPR_Quadratic-Wasserstein-Distance_2024.pdf
```

Paper:

```text
Lu, Wang, Han, Zhong, Zheng.
Full-Waveform Inversion of Two-Parameter Ground-Penetrating Radar Based on
Quadratic Wasserstein Distance.
Remote Sensing, 2024.
```

## Why This Paper Matters

This is directly relevant because it is GPR-specific, two-parameter FWI, and it
replaces the usual least-squares waveform mismatch with the quadratic
Wasserstein distance. The paper targets the exact weaknesses we are seeing in
the rebar work:

```text
least-squares local minima,
initial-model dependence,
noise sensitivity,
weak conductivity/attenuation recovery,
and the need for multi-scale frequency scheduling.
```

The paper is not a geometry-only rebar inversion paper, but the objective
lessons carry over cleanly: use a distance that sees global waveform transport,
not just pointwise amplitude difference.

## Core Method

The paper compares standard `L2` mismatch with the quadratic Wasserstein
distance `W2`.

Least squares compares traces point by point:

```text
large local penalty when observed and modeled events are shifted.
```

Quadratic Wasserstein compares two distributions through a transport cost:

```text
penalize how much "mass" must move, and how far, to transform one signal into
the other.
```

This makes the objective more convex for shifted oscillatory signals, which is
why the authors use it to reduce cycle skipping.

## Sinkhorn Approximation

Exact optimal transport is too expensive for repeated FWI evaluations. The
paper uses entropy regularization and the Sinkhorn algorithm.

Important pieces:

```text
C[i,j] = squared distance between sample positions i and j
epsilon = entropy regularization strength
K = exp(-C / epsilon)
P = diag(u) K diag(v)
W2 = <C, P>
```

Tradeoff:

```text
smaller epsilon:
  more accurate transport, higher cost, more numerical sensitivity

larger epsilon:
  smoother/cheaper transport, less exact objective
```

For our codebase, this means any first implementation should be in a separate
distance module with explicit tests for stability, scaling, and runtime.

## Softplus Normalization

Raw GPR traces are signed and oscillate around zero. Standard Wasserstein
distance assumes non-negative distributions with equal total mass.

The paper handles this by applying Softplus scaling and normalization:

```text
softplus(x, b) = log(exp(b*x) + 1)
normalized = softplus / sum(softplus)
```

The scale `b` controls how strongly the signed waveform is transformed before
normalization.

Paper finding:

```text
Softplus-normalized W2 has better convexity than L2 for shifted Ricker-like
signals.
```

Project implication:

```text
Do not implement OT/W2 directly on raw signed traces.
Start with Softplus-normalized trace windows and sweep b.
```

## Multi-Scale Frequency-Domain FWI

The paper applies W2 inside a multi-scale frequency-domain FWI loop for
relative permittivity and conductivity.

The inversion:

```text
starts from low frequencies,
adds higher frequencies through batches,
uses L-BFGS,
updates both relative permittivity and conductivity.
```

One example uses:

```text
Ricker center frequency: 100 MHz
discrete inversion frequencies: 1 MHz to 120 MHz
15 batches
4 frequencies per batch
10 iterations per batch
```

The exact frequencies do not transfer to our 1.0-1.5 GHz rebar setup, but the
methodology does:

```text
low-frequency/low-band information for large structure,
high-frequency information for detail,
objective choice that does not collapse under shifts/noise.
```

## Results That Matter

The paper reports three numerical examples. The relevant conclusions are:

```text
W2-FWI depends less on the initial model than L2-FWI.
W2-FWI is more robust to random noise.
W2-FWI improves conductivity recovery more strongly than permittivity recovery.
L2-FWI can generate high-frequency artifacts and obscure targets when the
starting model is poor.
Adding higher frequencies did not always improve results.
```

The conductivity result matters for us because radius and metal response are
not purely kinematic. If radius remains ambiguous under permittivity/geometry
only, conductivity or effective scattering strength may need to become a
controlled parameter. The paper warns that this should be done with objective
and scale control, not by simply adding degrees of freedom.

## How To Adapt This Without Overclaiming

A faithful reproduction would require:

```text
frequency-domain GPR operator,
two-parameter adjoint gradients,
L-BFGS over epsilon and sigma grids,
Sinkhorn W2 adjoint source.
```

That is a major branch. The safe adaptation path is:

1. Implement trace/window-level Softplus W2 with Sinkhorn.
2. Validate convexity on shifted Ricker traces.
3. Compare radius/depth objective landscapes for `L2`, W2, and fingerprint OT.
4. Only after landscape evidence, wire W2 into geometry optimization.
5. Keep full grid-based two-parameter W2-FWI as a later research branch.

## Immediate Experiments For Our Rebar Problem

### 1. Convexity Unit Tests

Create synthetic shifted traces and compare:

```text
L2 objective versus shift
Softplus W2 objective versus shift
effect of Softplus b
effect of Sinkhorn epsilon
```

Success:

```text
W2 should have fewer local minima and smoother behavior over time shifts.
```

### 2. Radius/Depth Landscape

Use current saved single-rebar observations and evaluate a local grid:

```text
z around 88-93 mm
radius around 5.4-7.4 mm
fixed x near 250 mm
```

Compare:

```text
L2 landscape
Softplus W2 landscape
W2 + high-frequency weighting
W2 under 5% and 10% noise
```

Success:

```text
true-radius basin is broader or better separated than with L2.
```

### 3. Hybrid W2-LS Schedule

Only if the landscape is better:

```text
W2 for basin search
LS for final polish
NRCCC trace-shift diagnostic as a switch/safety report
```

## Risks And Guardrails

```text
Risk: Softplus normalization can hide amplitude information.
Guardrail: report both W2 and raw LS for final candidates.

Risk: Sinkhorn cost can be high for long traces.
Guardrail: start on muted/downsampled trace windows and benchmark.

Risk: W2 may help cycle skipping but not radius ambiguity if traces are already
phase aligned.
Guardrail: compare objective landscapes before optimizer runs.

Risk: Adding conductivity too early can create non-identifiability.
Guardrail: introduce material parameters only after geometry-only landscapes are
understood.
```

## Bottom Line

This paper justifies a real W2 objective prototype, but not a blind full
rewrite. For the current single-rebar pipeline, the first serious use is
objective-landscape evidence and noise robustness, followed by a hybrid W2-LS
geometry optimizer only if the landscape improves radius separation.
