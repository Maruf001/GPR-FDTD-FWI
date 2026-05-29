# Optimal-Transport And Least-Squares FWI 2025: Working Notes

Source PDF:

```text
paper/FWI_Optimal_Transport_2025.pdf
```

Paper:

```text
Hunziker, Meles, Linde.
Crosshole ground-penetrating radar full-waveform inversion by combining
optimal-transport and least-squares distances.
Journal of Applied Geophysics, 2025.
```

## Why This Paper Matters For Our Project

Our current single-rebar objective is normalized least squares between muted
B-scans. Least squares is precise near the correct solution, but it can have
local minima when the modeled and observed traces are shifted or when geometry
parameters trade off against each other.

This paper gives a proven strategy:

```text
Use an optimal-transport distance early because its objective landscape is
broad and less cycle-skipping-prone. Once the model is close enough, switch
back to least squares because least squares has a sharper optimum.
```

That aligns well with our recent work:

```text
broad/coarse stage -> local refinement -> deterministic polish
```

The difference is that the paper changes the objective itself, not only the
optimizer or grid resolution.

## Core Method

The paper introduces an OT-LS-FWI algorithm for crosshole GPR.

The main pieces are:

1. Convert each trace into a probability-like representation suitable for
   optimal transport.
2. Use an optimal-transport distance for early iterations.
3. Measure whether enough modeled traces are within half a period of observed
   traces.
4. Switch to least squares after that condition is met.
5. Use sparse explicit gradients based on random master points and
   interpolation.
6. Use stochastic subsets of the data during the OT phase to reduce cost.

## How The OT Trace Distance Works

Optimal transport normally compares positive distributions with equal total
mass. Raw GPR traces do not satisfy this because they oscillate around zero and
can have different energy.

The paper follows a trace "fingerprint" idea:

```text
raw trace
-> 2D pseudo probability density over time/amplitude
-> two 1D marginal distributions
-> Wasserstein-style distances on those marginals
-> combined OT trace distance
```

The important practical effect is the objective shape. The paper shows a simple
example where least squares has local minima and points the optimizer in the
wrong direction, while the OT distance has a broad global basin.

For our project, this means OT can be used as a safer basin-finding objective.

## Why They Switch Back To Least Squares

The paper does not argue that OT should replace least squares everywhere.

OT is helpful early because the basin is broad and cycle skipping is reduced.
But OT is also:

- more expensive than least squares,
- less sharply defined near the optimum,
- sensitive to numerical approximations near the solution.

Least squares is still preferable once the model is close enough.

Plain interpretation:

```text
OT is for getting into the right basin.
LS is for final accuracy.
```

This is very relevant to radius estimation. We want the optimizer to avoid the
wrong high-radius basin, but we still want a sharp final objective for
sub-millimeter/local polish decisions.

## Switching Criterion

The paper defines a relative cross-correlation criterion:

```text
RCCC = trace time shift / dominant period
```

For each modeled/observed trace pair, estimate the time shift by
cross-correlation. If:

```text
RCCC < 0.5
```

then that trace is close enough that least-squares FWI should no longer be
cycle-skipped for that trace.

The fraction of traces satisfying that condition is called `NRCCC`.

The algorithm switches from OT to LS when:

```text
NRCCC > Cs
```

The paper found that `Cs` around `0.7` to `0.8` worked for their synthetic
example and recommends starting around `0.7`.

For our codebase, this is directly reusable as a diagnostic even before we
implement OT:

```text
track trace-shift fractions for each candidate or stage;
report whether the current model is in a least-squares-safe basin.
```

## Gradient And Regularization Idea

The paper also addresses a known crosshole GPR issue: gradients can be huge
near antennas, causing updates to concentrate in the wrong places.

Their solution is to compute explicit gradients only at random master points
that are not too close to antennas, then interpolate to the full model grid.

Effects:

- avoids extreme antenna-local sensitivities,
- smooths the gradient naturally,
- provides implicit regularization,
- makes it easier to test new distance measures because the gradient is not
  tied to a hand-derived adjoint for each objective.

For our current geometry inversion, we do not need pixel-wise master-point
gradients immediately. But the concept translates to finite-difference
geometry gradients:

```text
start with low-dimensional geometry parameters;
test objective alternatives by direct evaluation before deriving adjoints;
use smoothing/ranking/diagnostics to avoid overreacting to local waveform
features.
```

## Results

The paper uses a synthetic crosshole model with a large circular anomaly. The
starting model is homogeneous and deliberately not close enough for ordinary
least-squares FWI.

Findings:

- Pure least-squares FWI converged to bad local minima.
- Pure OT FWI moved toward the correct structure but did not resolve details
  well enough.
- OT followed by LS recovered good models for switching thresholds around
  `Cs = 0.7` to `0.75`.
- Runs that ended with `NRCCC = 1` and weighted RMS close to 1 were reliable.
- Runs that did not reach those diagnostics were not trustworthy.

The important takeaway is not a single metric value. It is the staged objective
logic:

```text
OT first, LS second, with a trace-shift-based switch.
```

## Relevance To Our Current Codebase

Current objective in `inversion/single_rebar_pipeline.py`:

```text
residual = (d_syn - d_obs) * mute
objective = normalized least-squares residual energy
```

This is a good final objective but not necessarily a robust early objective.

The OT paper suggests adding:

```text
objective_mode = "ls" | "ot" | "hybrid"
```

where:

```text
ls:     current objective
ot:     trace fingerprint / Wasserstein-style objective
hybrid: OT for early stage, LS after trace shifts are safe
```

However, implementing full fingerprint OT is nontrivial. We should not rush it
directly into the main inversion path.

## Practical Ideas To Reuse First

### 1. Add Trace-Shift Diagnostics Before OT

Implement a diagnostic that computes, for each source trace:

```text
time shift by cross-correlation
dominant period
RCCC = abs(shift) / period
NRCCC = fraction with RCCC < 0.5
```

Save this in run summaries and top-candidate polish metadata.

This gives us a paper-backed way to say whether Powell's high-radius solution
is merely close in least-squares value or also phase-aligned enough to trust.

### 2. Add A Cheap OT-Like Objective Prototype

Before implementing the full fingerprint OT distance, test cheaper
cycle-skipping-resistant objectives:

```text
trace envelope least squares
normalized cross-correlation distance
soft-DTW or shifted-window alignment penalty
```

These are not the paper's exact method, so they should be labeled prototypes.
The paper-backed exact method remains fingerprint OT.

### 3. Implement Fingerprint OT As A Separate Module

A clean implementation should live outside the inversion engine first:

```text
inversion/trace_distances.py
```

Functions:

```text
least_squares_distance(obs, syn, mute)
trace_shift_diagnostics(obs, syn, dt, mute)
fingerprint_ot_distance(obs, syn, ...)
```

Then compare objective landscapes:

```text
LS objective landscape over z/r
OT objective landscape over z/r
hybrid decision boundary using NRCCC
```

Only after those plots look sensible should OT be used inside Powell or a new
optimizer loop.

### 4. Hybrid Use In Geometry Pipeline

The current single-rebar workflow could become:

```text
2 mm global search with LS or coarse objective
-> OT or OT-like local basin search at 1 mm
-> LS Powell refinement
-> coarse grid polish
-> fine audit polish if top candidates are ambiguous
```

For exact synthetic data, this may be unnecessary. It becomes important for:

- bad starting models,
- multiple rebars,
- high noise,
- field-style wavelet errors,
- stronger material contrast ambiguity.

## Concrete Next Experiment

Add a non-invasive diagnostic first:

```text
trace_shift_diagnostics(results["d_obs"], results["d_syn_final"], dt)
```

and include it in:

```text
single_rebar_summary.json
grid_polish.top_candidates
```

Then run it on:

```text
009 Powell high-radius result
014/015 exact grid-polish result
020/021 5% noisy coarse-polish results
023 10% noisy top-k result
```

Question to answer:

```text
Does the high-radius basin have worse trace-shift diagnostics than the true
radius, even when least-squares misfit is close?
```

If yes, trace-shift diagnostics and OT-like objectives are likely valuable for
radius estimation.

