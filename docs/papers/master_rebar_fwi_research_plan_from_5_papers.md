# Two-Week Research Plan: Rebar GPR-FWI Size And Location Estimation

## Goal

Improve single-rebar and near-term multi-rebar inversion so that location,
cover depth, and radius are estimated accurately and with quantified
confidence.

This plan is based on five papers:

```text
01 Wavefield Reconstruction / cumulative frequency strategy, 2022
02 Progressively expanded bandwidths of data, 2021
03 OT then LS FWI with trace-shift switching, 2025
04 Quadratic Wasserstein GPR-FWI, 2024
05 Implicit multiparameter GPR-FWI, 2025
```

The plan is dynamic. Each stage has a decision gate. If an idea fails on
objective landscapes or controlled synthetic tests, it is documented and not
forced into the main pipeline.

## Progress Ledger

This checklist is the marathon operating ledger. Update it after each
experiment or implementation stage.

- [x] Install and verify `pytest` in the `FNO` conda environment.
- [x] Re-read and index the five-paper set.
- [x] Add technical notes for the 2024 quadratic Wasserstein GPR-FWI paper.
- [x] Add technical notes for the 2025 implicit multiparameter GPR-FWI paper.
- [x] Refresh the PEBDD note with current experiment interpretation.
- [x] Rename this master plan so it is not confused with a sixth paper.
- [x] Add reusable marathon operating rule/skill.
- [x] Repair plotting infrastructure before generating new experiment figures.
- [x] Day 1: build baseline result matrix and top-candidate margin extractor.
- [x] Day 2: spectrum-driven PEBDD setup.
- [x] Day 3: faithful PEBDD schedule runner and first matrix.
- [x] Day 4: cumulative frequency and frequency-weighting radius-margin tests.
- [x] Day 5: Softplus W2 / Sinkhorn distance prototype.
- [ ] Weekend window: objective landscape comparison.
- [x] Day 6 gate: hybrid W2/OT-LS not promoted because W2 landscapes did not justify it.
- [x] Day 7: wavelet mismatch and source-update tests.
- [x] Day 8: geometry versus material ambiguity tests.
- [x] Day 9: WRI feasibility study.
- [x] Day 10: IFWI feasibility spike.
- [x] Stage 1: source-profiled local radius polish runner and smoke gates.
- [x] Stage 2A: compact exact/noise/source-mismatch replication matrix.
- [x] Stage 2B: broader source-profiled replication across noise/source seeds.
- [ ] Stage 3: stress accepted polish with offset x/z/r seeds.
- [ ] Stage 4: extend accepted confidence reporting to multi-rebar cases.
- [ ] Days 11-14: robustness, replication, and handoff.

## Current Baseline

Known from experiments so far:

```text
2 mm broad/coarse search -> 1 mm local refinement -> 1 mm coarse grid polish
```

Current behavior:

```text
location:
  accurate after local refinement

radius:
  Powell/full-band LS tends toward a high-radius basin around 6.9-7.0 mm

coarse grid polish:
  reliably recovers true r=6.0 mm in exact and controlled 5-10% noisy synthetic
  runs when the seed is inside the local polish window

trace-shift diagnostics:
  NRCCC is already saturated at 1.0 for the high-radius and true-radius
  candidates, so the current radius issue is not primarily large phase-shift
  cycle skipping

bandpass/PEBDD first pass:
  exact low-band objective improved the radius seed, but noisy low-band runs
  still stayed near the high-radius basin

cumulative-frequency first pass:
  1.0 GHz contribution is much less sensitive to radius than 1.5 GHz, so naive
  unweighted averaging dilutes radius separation
```

## Research Principles From The Papers

### PEBDD 2021

Use progressively expanded bandwidths as a starting-model improvement tool:

```text
filter observed and modeled data the same way,
use tapered bands,
expand bandwidth gradually,
then run final full-band inversion/polish.
```

### WRI 2022

Use cumulative frequency strategies and frequency weighting:

```text
do not let high frequencies dominate too early,
do not average frequencies blindly,
carry lower-frequency information into later stages.
```

Full WRI is a major branch because it needs a frequency-domain wavefield
reconstruction solve.

### OT-LS 2025

Use OT-like distances for basin finding and LS for final accuracy:

```text
OT first,
trace-shift diagnostic as a switch/safety check,
LS second.
```

### Quadratic W2 GPR-FWI 2024

Use Softplus-normalized quadratic Wasserstein distance for signed GPR traces:

```text
Softplus -> mass normalization -> Sinkhorn W2.
```

The paper strongly motivates noise-robust objective landscapes before optimizer
integration.

### IFWI 2025

Use implicit representations as a later route to automatic multiscale behavior:

```text
neural representations learn smooth/low-frequency structure first,
then fine detail.
```

This is not the first fix for the current low-dimensional single-rebar problem,
but it is important for multiparameter and field-data work.

## Required Experiment Hygiene

Every substantial run must write:

```text
outputs/experiments/NNN_run_name/
docs/experiments/NN_topic_tracker.md
```

Every tracker entry must include:

```text
command,
run output path,
recovered x/z/r,
objective value,
data NRMS,
model NRMS for synthetic cases,
top radius candidates and margin,
runtime and evaluation count,
interpretation,
next decision.
```

Every new objective must first pass:

```text
unit tests on simple traces,
convexity/shift sanity plots,
local z/r objective landscapes,
exact-data single-rebar smoke,
5% and 10% noise checks.
```

No optimizer run is considered proof by itself. Objective landscapes and
candidate margins are required.

## Metrics

Primary:

```text
absolute x error in mm,
absolute z error in mm,
absolute radius error in mm,
best-radius margin against next radius,
top-k candidate stability across noise seeds.
```

Secondary:

```text
normalized objective value,
full-data NRMS,
per-frequency objective contribution,
trace-shift NRCCC and max RCCC,
runtime,
number of FDTD solves.
```

Robustness:

```text
exact data,
1% noise,
5% noise,
10% noise,
multiple noise seeds,
seed offsets in x/z/r,
wavelet perturbation once PEBDD is revisited.
```

## Week 1: Objective Diagnostics And Faithful Paper Adaptations

### Day 1: Reproducibility And Baseline Consolidation

Tasks:

```text
install/verify pytest in FNO,
run full test suite,
make a baseline results table from runs 009, 020-023, 029-041,
create a machine-readable candidate-margin extractor,
define standard exact/noise seed set.
```

Deliverables:

```text
docs/experiments/19_baseline_result_matrix.md
script or module for summarizing top-k radius margins
pytest validation log in tracker
```

Decision gate:

```text
If existing summaries are missing required fields, patch the writer before any
new long experiment.
```

### Day 2: Spectrum-Driven PEBDD Setup

Tasks:

```text
compute source spectra,
compute observed spectra,
compute residual spectra for true, high-radius, and near-radius candidates,
save plots and CSV summaries,
choose candidate band edges from actual spectral energy.
```

Deliverables:

```text
docs/experiments/20_pebdd_spectrum_design.md
outputs/experiments/NNN_pebdd_spectrum_design/
```

Decision gate:

```text
If 0.2-0.8 GHz removes too much rebar-discriminating energy, replace it with
data-driven bands before more PEBDD runs.
```

### Day 3: Faithful PEBDD Schedule Runner

Tasks:

```text
build or extend a staged runner for objective-bandpass schedules,
support low-pass and bandpass stages,
carry params forward automatically,
record per-stage summaries,
optionally run final full-band coarse polish only at the end.
```

Experiment matrix:

```text
exact data:
  short schedule, medium schedule, wider schedule

noise:
  5% seed 13, 10% seed 13

controls:
  direct full-band coarse polish from same seed
  full-band Powell plus polish if runtime allows
```

Deliverables:

```text
docs/experiments/21_faithful_pebdd_schedule.md
run_single_rebar_bandwidth_schedule.py or equivalent
```

Decision gate:

```text
Continue PEBDD only if it improves either runtime, seed capture range, or
top-candidate radius margin. Do not require low-band Powell to solve radius
alone.
```

### Day 4: Cumulative Frequency And Weighting

Tasks:

```text
use per-frequency objective reporting,
evaluate candidate frequencies such as 0.8, 1.0, 1.2, 1.5 GHz,
test weighted objectives,
compare cumulative schedules versus simultaneous weighted objectives.
```

Experiment matrix:

```text
exact local z/r grid,
5% noise local z/r grid,
10% noise local z/r grid,
weighted polish from high-radius seed.
```

Deliverables:

```text
docs/experiments/22_frequency_weighting_radius_margin.md
weighted objective recommendation or rejection
```

Decision gate:

```text
If lower frequencies dilute radius margins, use them only for x-z basin stages.
If high-frequency weights improve noisy radius margin, integrate them into final
polish/objective comparisons.
```

### Day 5: Softplus W2 / Sinkhorn Distance Prototype

Tasks:

```text
implement Softplus normalization,
implement stable Sinkhorn W2 for 1D trace windows,
benchmark trace length/downsampling choices,
test b and epsilon sweeps,
compare L2 versus W2 on shifted Ricker traces.
```

Deliverables:

```text
inversion/trace_wasserstein.py
tests/test_trace_wasserstein.py
docs/experiments/23_w2_distance_convexity.md
```

Decision gate:

```text
Do not connect W2 to the optimizer unless shifted-trace tests and local
landscapes are numerically stable and interpretable.
```

### Weekend / Long-Run Window: Objective Landscapes

Tasks:

```text
run local z/r landscapes for L2, weighted L2, PEBDD-filtered L2, W2,
and simple OT/fingerprint alternatives if available.
```

Deliverables:

```text
docs/experiments/24_objective_landscape_comparison.md
figures comparing basins and radius margins
```

Decision gate:

```text
Promote only objectives that improve radius basin separation or noise
robustness without destroying final LS accuracy.
```

## Week 2: Hybrid Objectives, Material Ambiguity, And Larger Branches

### Day 6: Hybrid W2/OT-LS Schedule

Tasks:

```text
build a two-stage objective runner:
  W2 or OT-like objective for basin search,
  LS or weighted LS for final refinement,
  full-band coarse polish for final candidate selection.

use NRCCC diagnostics as a report and possible switch condition.
```

Experiment matrix:

```text
exact data from rough seed,
5% noise seeds,
10% noise seeds,
offset initial x/z/r seeds.
```

Deliverables:

```text
docs/experiments/25_hybrid_w2_ls_schedule.md
```

Decision gate:

```text
If W2/OT does not improve basin capture or margin, keep it as a diagnostic
tool and avoid adding it to the production path.
```

### Day 7: Wavelet Perturbation And PEBDD Source Update

Tasks:

```text
simulate source-wavelet mismatch:
  center-frequency shift,
  time shift,
  amplitude scaling,
  bandwidth change.

test whether PEBDD and W2 are more robust than LS.
prototype a deconvolution-style wavelet update for synthetic mismatch.
```

Deliverables:

```text
docs/experiments/26_wavelet_mismatch_and_update.md
```

Decision gate:

```text
If wavelet mismatch changes radius estimates, source-wavelet handling becomes a
first-class part of the pipeline before field data.
```

### Day 8: Geometry Versus Material Ambiguity

Tasks:

```text
test whether radius bias can be traded against rebar conductivity,
effective metal response,
or concrete permittivity/conductivity.

start with low-dimensional parameters, not grid FWI:
  x, z, radius,
  concrete epsr,
  optional concrete sigma,
  optional rebar effective sigma/log-sigma.
```

Deliverables:

```text
docs/experiments/27_geometry_material_tradeoff.md
parameter identifiability table
```

Decision gate:

```text
Only add material parameters to the normal inversion if they reduce radius bias
without creating new non-identifiability.
```

### Day 9: WRI Feasibility Study

Tasks:

```text
define what a faithful WRI branch would require in this repo,
evaluate frequency-domain operator options,
estimate memory/runtime,
prototype only a toy linear wavefield-reconstruction solve if feasible.
```

Deliverables:

```text
docs/experiments/28_wri_feasibility.md
```

Decision gate:

```text
If WRI requires a major solver rewrite, document the route and defer until
PEBDD/W2/weighted-LS have been exhausted.
```

### Day 10: IFWI / Neural Implicit Feasibility Spike

Tasks:

```text
define the smallest IFWI-inspired model that cannot hide geometry errors:
  explicit x/z/r geometry,
  optional small neural residual field around the target,
  strong regularization and held-out sources.

do not build full differentiable FDTD unless justified.
```

Deliverables:

```text
docs/experiments/29_ifwi_feasibility.md
prototype design, not necessarily production code
```

Decision gate:

```text
If the neural residual field fits noise or absorbs radius errors, reject it for
the current single-rebar pipeline.
```

### Days 11-14: Robustness, Replication, And Handoff

Tasks:

```text
replicate the best 2-3 workflows across noise seeds,
run seed-offset stress tests,
generate confidence intervals / top-k ambiguity reports,
write final method comparison.
```

Deliverables:

```text
docs/experiments/30_two_week_research_summary.md
plain-language result table
recommended production pipeline
known failure modes
next-month research branch list
```

Final decision:

```text
choose one main pipeline,
choose one fallback pipeline,
list objective methods rejected with evidence,
list methods worth deeper implementation.
```

## Post-Summary Stage Status

### Stage 1: Source-Profiled Local Radius Polish

Status:

```text
passed smoke gates
```

Implementation:

```text
inversion/source_profile.py
run_single_rebar_source_profiled_polish.py
tests/test_source_profile.py
tests/test_source_profiled_polish_runner.py
```

Tracker:

```text
docs/experiments/31_source_profiled_radius_polish.md
```

Key results:

| Run | Case | Best r [mm] | Next r [mm] | Margin | Source profile |
| --- | --- | ---: | ---: | ---: | --- |
| 057 | nominal exact | 6.0 | 6.2 | 9.815e-04 | fc=1.0, shift=0 ps, amp=1.0 |
| 058 | combined source mismatch | 6.0 | 6.2 | 1.146e-03 | fc=1.1, shift=-50 ps, amp=1.09994 |

Decision:

```text
Promote source-profiled local radius polish to Stage 2 replication. Keep top-k
candidate reporting and distinct-radius margins mandatory, because wrong-radius
candidates can still choose nearby nuisance source profiles.
```

### Stage 2A: Compact Replication Matrix

Status:

```text
passed compact replication gate
```

Implementation:

```text
run_single_rebar_source_profiled_replication.py
tests/test_source_profiled_replication_runner.py
```

Tracker:

```text
docs/experiments/32_source_profiled_replication_matrix.md
```

Key result:

| Case | Best r [mm] | Next r [mm] | Margin | Best source profile |
| --- | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 9.815e-04 | fc=1.0, shift=0 ps, amp=1.000 |
| noise05_seed13 | 6.0 | 6.2 | 7.697e-04 | fc=1.0, shift=0 ps, amp=1.000 |
| noise10_seed13 | 6.0 | 6.2 | 5.236e-04 | fc=1.0, shift=0 ps, amp=1.001 |
| source_mismatch | 6.0 | 6.2 | 1.146e-03 | fc=1.1, shift=-50 ps, amp=1.100 |
| source_mismatch_noise05_seed13 | 6.0 | 6.2 | 9.366e-04 | fc=1.1, shift=-50 ps, amp=1.103 |

Decision:

```text
Run broader seed replication before x/z/r seed-offset stress tests. The compact
matrix shows the method is stable for exact, 5%, 10%, and controlled source
mismatch cases, but only one noise seed has been tested in the production
matrix.
```

### Stage 2B: Noise And Source Seed Replication

Status:

```text
passed seed-replication gate
```

Output:

```text
outputs/experiments/060_source_profiled_replication_seed_matrix
```

Tracker:

```text
docs/experiments/32_source_profiled_replication_matrix.md
```

Summary:

| Group | n | Margin min | Margin mean | Margin max | Radius result |
| --- | ---: | ---: | ---: | ---: | --- |
| nominal_noise05 | 4 | 6.902e-04 | 8.793e-04 | 1.045e-03 | all r=6.0 |
| nominal_noise10 | 4 | 3.869e-04 | 5.923e-04 | 7.574e-04 | all r=6.0 |
| mismatch_noise05 | 3 | 9.366e-04 | 1.011e-03 | 1.137e-03 | all r=6.0 |
| mismatch_noise10 | 3 | 6.715e-04 | 7.952e-04 | 1.004e-03 | all r=6.0 |

Decision:

```text
Move to Stage 3 x/z/r local-window stress tests. The source-profiled polish is
stable across the tested exact, noisy, and source-mismatched synthetic cases at
the fixed local x/z window.
```

## Dynamic Branch Rules

### If PEBDD Helps

```text
make PEBDD the default rough-seed-to-local-window stage,
then run final weighted/full-band polish.
```

### If PEBDD Does Not Help

```text
keep bandpass objective for diagnostics only,
move effort to W2/OT and wavelet robustness.
```

### If W2 Helps

```text
build hybrid W2-LS runner,
test exact/noisy/seed-offset cases,
compare against current coarse polish.
```

### If W2 Does Not Help

```text
do not force OT machinery into optimization,
use W2 only as a diagnostic landscape,
focus on weighted LS, source wavelet, and material ambiguity.
```

### If Frequency Weighting Helps

```text
use lower frequencies for early x-z stages,
use high-frequency-weighted objective or full-band polish for radius.
```

### If Material Parameters Explain Radius Bias

```text
add material parameters with tight bounds and top-k ambiguity reporting.
```

### If Material Parameters Create Non-Identifiability

```text
freeze material parameters,
report radius confidence from geometry-only top-k candidates,
defer material inversion to WRI/IFWI branch.
```

## First Next Step

Start with Day 1:

```text
run pytest in FNO,
create baseline result matrix,
write a small top-candidate margin extractor,
verify all summaries contain fields needed for the two-week plan.
```

This keeps the next experiments grounded in repeatable baselines before
spending GPU time on new objective families.
