# Experiment 29: IFWI Feasibility

## Goal

Decide whether implicit full-waveform inversion (IFWI) should be implemented
for the current single-rebar pipeline.

Source notes:

```text
docs/papers/05_implicit_multiparameter_gpr_fwi_2025.md
```

## Paper Idea

The IFWI paper represents subsurface material properties with a neural implicit
function:

```text
(x, z) -> neural network -> epsilon_r, sigma
```

The useful property is the neural frequency principle:

```text
smooth/low-frequency structure tends to be learned before fine detail
```

That can act like an automatic multiscale prior.

## Current Single-Rebar Reality

The current problem is low-dimensional:

```text
x,
z,
radius,
source wavelet nuisance parameters,
optional material nuisance parameters.
```

Recent experiments show:

```text
radius evidence is strong under matched/source-profiled data;
W2 is not useful as a final radius objective;
material conductivity/permittivity sweeps do not explain radius bias at fixed
x/z;
source wavelet mismatch can strongly bias radius, but low-dimensional source
profiling fixes the tested cases.
```

That means a neural implicit field is not the next clean fix for the current
single-rebar radius estimator.

## Why Full IFWI Is Risky Here

A neural residual field could easily hide the thing we are trying to measure:

```text
wrong radius + flexible local material residual -> good data fit
```

Without strong guardrails, this would make the radius estimate less meaningful,
not more accurate.

A faithful differentiable-FDTD IFWI branch would also require:

```text
automatic differentiation through time stepping,
memory/checkpointing strategy,
network architecture choices,
regularization and held-out source validation,
and multiparameter scaling.
```

That is larger than the present geometry/source-profile pipeline.

## Safe IFWI-Inspired Prototype

The only safe near-term prototype is constrained:

```text
explicit geometry stays primary:
  x, z, radius

source profile stays explicit:
  amplitude, time-zero, center-frequency/bandwidth

optional neural residual is small and local:
  around recovered target only,
  smooth output,
  strong L2/TV penalty,
  held-out scan positions,
  disabled during final radius confidence report.
```

Success would require:

```text
improved held-out source prediction,
no radius drift,
and residual field that remains physically small.
```

Failure condition:

```text
if the residual field absorbs radius errors, reject it.
```

## Day 10 Decision

Do not implement IFWI for the current single-rebar marathon stage.

Defer IFWI until:

```text
single-rebar source-profiled radius workflow is locked,
multi-rebar cases expose residual material/background errors,
or field data require a smooth local model correction that explicit nuisance
parameters cannot explain.
```

Near-term priority remains:

```text
productionizing source-profiled local radius selection,
replicating robustness across noise/source seeds,
then extending to multi-rebar geometry.
```
