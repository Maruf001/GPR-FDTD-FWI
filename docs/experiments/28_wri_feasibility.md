# Experiment 28: WRI Feasibility

## Goal

Decide whether wavefield reconstruction inversion (WRI) should become an
implementation branch in this repo now, later, or not at all.

This follows the 2022 WRI paper:

```text
paper/Wavefield Reconstruction_2022.pdf
docs/papers/01_wavefield_reconstruction_2022.md
```

## What Faithful WRI Requires

The paper's method is frequency-domain WRI. For each model and frequency, it
solves a wavefield reconstruction problem:

```text
min_u ||P u - d||^2 + lambda ||A(m) u - q||^2
```

where:

```text
u: frequency-domain wavefield
P: receiver sampling operator
d: observed frequency-domain data
A(m): discretized frequency-domain wave operator
q: source term
lambda: penalty weight tying reconstructed wavefield to the wave equation
```

Then variable projection reduces the problem back to a model update.

## Current Repo Gap

The current production path is time-domain FDTD:

```text
core/fdtd.py
gpu/fdtd_gpu_v2.py
inversion/single_rebar_pipeline.py
```

It does not have:

```text
frequency-domain Helmholtz/Maxwell operator assembly,
complex sparse linear solves,
receiver/source projection matrices,
frequency-domain adjoint gradients for WRI,
penalty continuation logic,
or variable-projection model updates.
```

## Rough Scale

The current 1 mm grid uses about:

```text
NX x NZ = 560 x 360 = 201,600 cells including PML
```

A 2D scalar frequency-domain operator would have roughly one complex unknown
per cell and about five stencil entries per row:

```text
unknowns: ~2.0e5 per frequency
nonzeros: ~1.0e6 per frequency
```

That sparse matrix is not the real blocker by itself. The blocker is repeated
complex solves for:

```text
multiple sources,
multiple frequencies,
multiple model iterations,
multiple WRI penalty stages.
```

Direct sparse solves at this size can become memory-heavy. Iterative solves
need preconditioning. A faithful implementation would become a parallel solver
project, not a small inversion-objective change.

## Time-Domain WRI Alternative

A time-domain WRI analog would treat the whole time history as the reconstructed
wavefield. That is larger:

```text
201,600 cells x 3,769 time samples ~= 7.6e8 field samples per source
```

That is not a practical first branch for this repo.

## What We Already Reused From The Paper

The useful paper ideas that did transfer have already been tested:

```text
cumulative/frequency-weighted objectives:
  docs/experiments/23_frequency_weighting_radius_margins.md

progressive bandwidth schedules:
  docs/experiments/22_faithful_pebdd_schedule.md

objective landscape gating before optimizer integration:
  docs/experiments/25_w2_rebar_landscape.md

source-wavelet handling:
  docs/experiments/26_wavelet_mismatch_and_update.md
```

Important conclusions so far:

```text
low frequencies help basin logic but dilute final radius evidence if averaged
equally;

W2 improves shifted trace convexity but destroys radius margin in the local
single-rebar landscape;

source amplitude/time/frequency profiling is essential before field-data
radius estimation.
```

## Feasibility Decision

Do not implement full WRI in this marathon.

Reason:

```text
The current radius problem is already well explained by source-wavelet
mismatch, frequency weighting, and local radius profiling.

Full WRI would require a new frequency-domain solver and adjoint path.
```

Recommended future route if WRI becomes necessary:

```text
1. Build a separate toy frequency-domain scalar operator on a much smaller grid.
2. Validate source/receiver projection and complex sparse solves.
3. Implement WRI wavefield reconstruction for fixed permittivity.
4. Compare WRI and FDTD LS on tiny synthetic targets.
5. Only then consider porting to the full GPR grid.
```

## Day 9 Decision

WRI is documented and deferred.

For the current single-rebar pipeline, continue with:

```text
source-update/profiled radius pipeline,
robustness replication across noise/source seeds,
multi-rebar extension after the single-rebar workflow is stable.
```
