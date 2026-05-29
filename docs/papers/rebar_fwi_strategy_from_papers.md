# Paper-Driven Strategy For Better Rebar Size And Location Estimation

This document synthesizes three papers the user asked to study:

```text
paper/Wavefield Reconstruction_2022.pdf
paper/FWI_improvement_by_progressively expanded bandwidths of the data.pdf
paper/FWI_Optimal_Transport_2025.pdf
```

Separate notes:

```text
docs/papers/01_wavefield_reconstruction_2022.md
docs/papers/02_progressive_bandwidth_fwi_2021.md
docs/papers/03_optimal_transport_fwi_2025.md
```

## Current Project State

The current single-rebar pipeline has made real progress:

```text
2 mm bounded global search
-> 1 mm Powell local refinement
-> 1 mm coarse local grid polish
```

Current behavior:

- location is accurate,
- Powell alone still tends to prefer a slightly deeper/larger-radius basin,
- deterministic grid polish corrects radius in exact and controlled-noise
  synthetic cases,
- coarse polish reduces polish cost from 160 to 40 candidates for the current
  local setup,
- top-candidate tracking now exposes ambiguity near the chosen radius.

The next improvement should not be another blind optimizer sweep. The papers
suggest the next gains should come from better objective scheduling and better
diagnostics.

## Main Lessons Across The Three Papers

### 1. Standard Least Squares Is A Good Final Objective, Not Always A Good Early Objective

Both the progressive-bandwidth paper and the optimal-transport paper emphasize
that least-squares waveform matching can fail when modeled and observed traces
are shifted too far apart. This is the cycle-skipping problem.

For us, this means the current normalized least-squares objective is appropriate
for final local comparisons, but may not be the best way to guide early basin
selection.

### 2. Low-Frequency Or Low-Band Information Should Guide Large-Scale Structure

The WRI paper uses cumulative frequency sequences. The progressive-bandwidth
paper filters both observed and modeled data, then expands the bandwidth.

For us, this suggests:

```text
use low-band data to stabilize x/z location and avoid radius/depth tradeoffs;
add higher-band information only after the geometry is in the right basin.
```

### 3. Do Not Let High Frequencies Dominate Too Early

High-frequency data carry detail, but they make the inverse problem more
nonlinear. The WRI paper explicitly weights frequencies to reduce high-frequency
dominance.

For us:

```text
multi-frequency objective should report and optionally weight per-frequency
misfit contributions.
```

### 4. Switch Objectives When Diagnostics Say The Model Is Close Enough

The optimal-transport paper uses a trace-shift criterion. It switches from OT
to least squares when enough traces are within half a dominant period.

For us:

```text
do not switch to fine LS-only refinement just because an optimizer ran out of
evaluations;
switch when trace-shift diagnostics indicate LS is safe.
```

### 5. Track Ambiguity, Not Only The Best Model

The current top-candidate polish metadata matches the spirit of the OT paper's
diagnostic thinking. A single best model is not enough when nearby candidates
have nearly identical objective values.

For radius estimation, we should report:

```text
best radius
next-best radius
objective margin
trace-shift margin
data NRMS
model NRMS for synthetic cases
```

## What We Should Not Do Next

Avoid these shortcuts:

- Do not immediately implement a full frequency-domain WRI solver. It is a
  large branch and our current simulator is time-domain FDTD.
- Do not add many optimizer types before improving the objective and staging.
- Do not use full-band LS as the only metric for radius confidence.
- Do not trust a single noisy seed for robustness claims.
- Do not add material degrees of freedom before geometry behavior is stable.

## Recommended Development Path

### Phase 1: Diagnostics First

Add trace-shift diagnostics inspired by the OT paper.

Implementation target:

```text
inversion/trace_distances.py
```

Initial functions:

```text
least_squares_distance(obs, syn, mute)
trace_shift_diagnostics(obs, syn, dt, mute)
```

Diagnostics to save:

```text
dominant_period_s
median_abs_shift_s
max_abs_shift_s
nrccc_fraction_lt_half_period
per_trace_shift_s
```

Where to save:

```text
single_rebar_summary.json
grid_polish.top_candidates
```

First experiment:

```text
Compare trace-shift diagnostics for:
  Powell high-radius result
  true-radius grid-polish result
  5% noisy top candidates
  10% noisy top candidates
```

Decision:

```text
If true-radius candidates have better trace alignment than high-radius
candidates, trace-shift diagnostics can help detect radius ambiguity.
```

### Phase 2: Bandpass Objective Schedule

Adapt the progressive-bandwidth paper before implementing full OT.

Implementation target:

```text
inversion/trace_filters.py
run_single_rebar_bandwidth_schedule.py
```

Add CLI support:

```text
--objective-bandpass-ghz LOW,HIGH
```

Important rule:

```text
Apply the same bandpass to observed and modeled traces before computing the
objective.
```

Initial schedule:

```text
stage 1: low-to-mid band
stage 2: expanded band
stage 3: full useful band
stage 4: unfiltered or full target objective
final:   --grid-polish --grid-polish-preset coarse
```

The exact band edges should be chosen after plotting the source and residual
spectra. Do not copy the MHz values from crosshole papers directly.

Success criteria:

```text
Powell radius before polish moves closer to 6.0 mm,
or true-radius top-candidate margin improves,
or noisy robustness improves without increasing total runtime too much.
```

### Phase 3: Cumulative Frequency Schedule

Adapt the WRI paper's cumulative frequency concept using our existing
multi-frequency hooks.

Implementation target:

```text
run_single_rebar_frequency_schedule.py
```

Example schedule:

```text
stage 1: 1.0 GHz
stage 2: 1.0,1.2 GHz
stage 3: 1.0,1.2,1.5 GHz
final:   coarse grid polish
```

Add per-frequency objective reporting:

```text
frequency_ghz
raw_misfit
weighted_misfit
weight
```

This tells us whether high-frequency components dominate the radius decision.

### Phase 4: OT-Like Objective Prototype

Implement after trace diagnostics are in place.

Start with objective-landscape tools, not the optimizer:

```text
LS z/r landscape
trace-shift z/r landscape
OT-like or fingerprint-OT z/r landscape
```

Only use OT inside optimization after it shows a better basin on the current
diagnostic landscapes.

Potential modules:

```text
inversion/trace_distances.py
run_single_rebar_distance_landscape.py
```

Exact fingerprint OT should be implemented separately and compared against
cheaper alternatives. If cheaper alternatives work for our geometry problem,
that is acceptable, but they should not be mislabeled as the paper's OT method.

### Phase 5: Consider True WRI Later

Full WRI is a later branch because the paper's method is frequency-domain and
solves reconstructed wavefields through a Helmholtz/PDE operator.

A faithful implementation would require:

```text
frequency-domain GPR forward operator
reconstructed wavefield least-squares solve
model-gradient calculation for permittivity/conductivity
frequency weighting and cumulative schedule
regularization/depth weighting
```

This could become important for multi-rebar or field-data inversion, but it is
not the next fastest reliable improvement for the current single-rebar
pipeline.

## Proposed Immediate Experiments

### Experiment 15: Trace-Shift Diagnostics

Goal:

```text
Quantify whether radius-biased Powell solutions are phase/shift worse than
true-radius polished candidates.
```

Outputs:

```text
docs/experiments/15_trace_shift_diagnostics.md
outputs/experiments/024_...
```

### Experiment 16: PEBDD-Style Bandpass Schedule

Goal:

```text
Test whether progressively expanded trace bandwidth reduces the high-radius
basin before grid polish.
```

Outputs:

```text
docs/experiments/16_bandwidth_schedule.md
outputs/experiments/...
```

### Experiment 17: Cumulative Frequency Schedule

Goal:

```text
Test whether cumulative center-frequency stages improve radius/depth
separation compared with the current one-frequency objective.
```

Outputs:

```text
docs/experiments/17_cumulative_frequency_schedule.md
outputs/experiments/...
```

## Recommended Priority

Order:

```text
1. Trace-shift diagnostics
2. Bandpass schedule
3. Cumulative frequency schedule
4. OT/fingerprint distance landscapes
5. Hybrid OT-LS optimization
6. Full WRI research branch
```

Reason:

```text
Trace diagnostics are low risk and immediately useful.
Bandpass and cumulative frequency schedules reuse the current solver.
OT requires new distance machinery but can be isolated first.
Full WRI requires a major solver branch and should wait until simpler
paper-backed improvements are exhausted.
```

## Status After Experiment 15

Experiment 15 implemented trace-shift diagnostics and tested them on the known
single-rebar radius ambiguity:

```text
docs/experiments/15_trace_shift_diagnostics.md
```

Result:

```text
NRCCC = 1.0 for the true-radius polished candidates and for the high-radius
Powell candidates.
```

That means the current radius bias is not mainly a cycle-skipping or large
phase-shift problem. The high-radius basin is already phase-aligned enough for
least-squares by the half-period criterion used in the OT paper.

Updated priority:

```text
1. Keep trace-shift diagnostics as a safety report.
2. Move next to PEBDD-style progressive bandwidth scheduling.
3. Defer OT-LS optimization until we find a case where NRCCC is not saturated.
```

## Status After Experiment 16

Experiment 16 implemented the PEBDD-style bandpass objective prototype:

```text
docs/experiments/16_bandwidth_schedule.md
inversion/trace_filters.py
--objective-bandpass-ghz LOW,HIGH
```

Result:

```text
0.2-0.8 GHz low-band Powell:
  x=249.823 mm, z=90.591 mm, radius=6.573 mm

0.2-1.1 GHz expanded-band Powell:
  x=249.735 mm, z=90.731 mm, radius=6.864 mm

full-band Powell from the low-band seed:
  x=249.533 mm, z=90.653 mm, radius=6.955 mm

low-band seed directly to full-band coarse polish:
  x=250.000 mm, z=90.000 mm, radius=6.000 mm
```

Interpretation:

```text
The low-band objective helps by moving the radius estimate away from the old
high-radius basin.

Expanding back to normal full-band least squares with Powell pulls the solution
back into the high-radius basin.

For the current exact single-rebar case, the useful PEBDD adaptation is:

2 mm coarse seed
-> 1 mm low-band Powell objective, 0.2-0.8 GHz
-> full-band coarse grid polish
```

Updated priority:

```text
1. Validate the low-band-seed plus coarse-polish workflow under controlled
   noise, because exact synthetic recovery is already solved.
2. Add cumulative-frequency reporting to see which frequencies favor the
   high-radius basin.
3. Build objective-landscape tools before any OT-LS optimizer, because trace
   shifts are currently not the main failure mode.
4. Keep full WRI as a later branch; it is not the next cheapest route to
   better radius estimates in this codebase.
```

## Status After Experiment 17

Experiment 17 tested the low-band-seed plus full-band coarse-polish workflow
under controlled 5% and 10% observed-data noise:

```text
docs/experiments/17_bandwidth_noise_robustness.md
outputs/experiments/034_...
outputs/experiments/035_...
outputs/experiments/036_...
outputs/experiments/037_...
```

Result:

```text
5% noise low-band Powell:
  x=250.353 mm, z=90.527 mm, radius=6.999 mm

5% noise full-band coarse polish:
  x=250.000 mm, z=90.000 mm, radius=6.000 mm

10% noise low-band Powell:
  x=249.858 mm, z=90.769 mm, radius=6.927 mm

10% noise full-band coarse polish:
  x=250.000 mm, z=90.000 mm, radius=6.000 mm
```

Interpretation:

```text
The low-band objective is not robustly radius-correcting under noise.
It keeps the solution in the local x-z basin, but radius remains near 7 mm.

The full-band coarse grid polish remains the reliable radius selector.

If a seed is already inside the coarse-polish x-z-radius window, skip low-band
Powell and polish directly.
```

Updated priority:

```text
1. Add cumulative frequency and per-frequency misfit reporting.
2. Use that reporting to identify which frequency content favors the
   high-radius basin.
3. Then test whether frequency weighting or cumulative schedules improve the
   radius margin before adding OT machinery.
```

## Status After Experiment 18

Experiment 18 added per-frequency objective reporting and ran a two-frequency
diagnostic polish. It also added optional frequency weights:

```text
docs/experiments/18_cumulative_frequency_diagnostics.md
outputs/experiments/038_...
outputs/experiments/039_...
outputs/experiments/040_...
outputs/experiments/041_...
--frequency-weights W1,W2,...
```

Key result from the exact 1.0+1.5 GHz polish:

```text
r=6.2 mm candidate:
  average J = 5.3636e-04
  1.0 GHz J = 3.5600e-05
  1.5 GHz J = 1.0371e-03

r=6.8 mm, z=91.0 mm candidate:
  average J = 1.0846e-03
  1.0 GHz J = 8.6443e-05
  1.5 GHz J = 2.0828e-03
```

Interpretation:

```text
The lower 1.0 GHz center frequency is much less sensitive to radius
differences than 1.5 GHz.

Naively averaging lower and higher frequencies reduces radius separation.
```

Updated priority:

```text
1. Use low-frequency stages for x-z basin selection only.
2. Use high-frequency-weighted or full-band polish for radius selection.
3. Test weighted multi-frequency polish under noise if the 10% margin needs
   improvement.
4. Keep OT/fingerprint objectives isolated to landscape diagnostics until a
   case appears where trace shifts are not already saturated.
```

## Reread And Expanded Paper Set Update

The current paper set is now five papers, indexed here:

```text
docs/papers/00_paper_index.md
docs/papers/01_wavefield_reconstruction_2022.md
docs/papers/02_progressive_bandwidth_fwi_2021.md
docs/papers/03_optimal_transport_fwi_2025.md
docs/papers/04_quadratic_wasserstein_gpr_fwi_2024.md
docs/papers/05_implicit_multiparameter_gpr_fwi_2025.md
```

The detailed two-week research plan is:

```text
docs/papers/master_rebar_fwi_research_plan_from_5_papers.md
```

Revised strategic view:

```text
PEBDD:
  still important, but needs a more faithful spectrum-driven schedule and
  wavelet-mismatch testing before judgment.

Cumulative frequency / WRI:
  per-frequency reporting has already shown that lower center frequencies can
  dilute radius separation; frequency weights and staged use are required.

OT / W2:
  trace-shift diagnostics say the current high-radius basin is not a large
  phase-shift failure, but the 2024 W2 paper still motivates Softplus-Sinkhorn
  objective landscapes for noise and basin-shape testing.

IFWI:
  not the next single-rebar fix, but a later branch for multiparameter and
  field-data inversion after objective behavior is understood.
```

Immediate next step:

```text
Create the baseline result matrix and top-candidate margin extractor, then run
the spectrum-driven PEBDD design step from the two-week plan.
```
