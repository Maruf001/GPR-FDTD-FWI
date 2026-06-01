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
- [x] Stage 3A: exact wider-window geometry stress test.
- [x] Stage 3B: noisy wider-window geometry stress test.
- [x] Stage 4A: fixed-position multi-rebar common-radius confidence profile.
- [x] Stage 4B: per-rebar radius identifiability in multi-rebar scene.
- [x] Stage 4C-left: left-rebar x/z/r coupling under 10% noise.
- [x] Stage 4C-center: center-rebar x/z/r coupling under 10% noise.
- [x] Stage 4C-right: final right-rebar x/z/r coupling check.
- [x] Stage 5: confidence/reporting layer for local multi-rebar geometry.
- [x] Stage 6: replicate Stage 4C confidence over additional noise seeds.
- [x] Stage 7: ambiguity interval / fallback reporting before full optimizer promotion.
- [x] Stage 8: reporting-first full multi-rebar optimizer design.
- [x] Stage 8A: coordinate optimizer 10% noise/source-mismatch replication.
- [x] Stage 8B: guarded revisit for 2 mm seed-offset coordinate stress.
- [x] Stage 9: radius-confidence objective comparison for weak edge targets.
- [x] Add validated wavefield animation support for recent/future experiment folders.
- [x] Backfill scientifically labelled animations for previous single-rebar experiments 052-062.
- [x] Stage 10A: initial B-scan hyperbola detector and detection-to-refinement smoke.
- [x] Stage 10B: detector-only depth/radius/noise/source/multi-rebar smoke benchmarks.
- [x] Stage 10C smoke: manual coarse-to-fine detector-seeded refinement.
- [x] Stage 10D: packaged detector-seeded two-stage refinement runner.
- [x] Stage 10E: scenario-aware single-rebar truth refactor and non-default smoke.
- [x] Stage 10F: packaged source-mismatch/noise stress for non-default depth/radius.
- [x] Stage 10G: shallow small-radius packaged stress and confidence warning.
- [x] Stage 10H: aggregate reporting layer for packaged two-stage runs.
- [x] Stage 10I: first shallow small-radius noise-seed replication.
- [x] Stage 10J: third shallow small-radius seed confirming weak confidence.
- [x] Stage 10K: aggregate report confirming replicated weak-margin branch.
- [x] Stage 10L: dense-radius diagnostic proving shallow branch ambiguity.
- [x] Stage 10M: radius ambiguity interval reporting.
- [x] Stage 10N: subcell geometry diagnostic for shallow small-radius branch.
- [x] Stage 10O: hard/subcell aggregate comparison.
- [x] Stage 10P: aggregate zero-error plot repair.
- [x] Stage 10Q: equal-weight 1.0+1.5 GHz multifrequency diagnostic.
- [x] Stage 10R: equal-weight 1.5+2.0 GHz high-frequency diagnostic.
- [x] Stage 11A: variable-radius acquisition-density x-ambiguity diagnostic.
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

### Stage 3A: Exact Wider-Window Geometry Stress

Status:

```text
passed exact geometry-window gate
```

Output:

```text
outputs/experiments/061_source_profiled_geometry_window_exact_mismatch
```

Tracker:

```text
docs/experiments/33_geometry_window_stress.md
```

Result:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| nominal | 250.0 | 90.0 | 6.0 | 6.2 | 9.815e-04 |
| source_mismatch | 250.0 | 90.0 | 6.0 | 6.2 | 1.146e-03 |

Decision:

```text
Run the same wider geometry window under 10% noise before moving to multi-rebar.
Exact data rejects nearby wrong x/z cells, but the top-k list shows a deeper
high-radius competitor around z=91 mm and r=6.8-7.0 mm that should be tested
under noise.
```

### Stage 3B: Noisy Wider-Window Geometry Stress

Status:

```text
passed noisy geometry-window gate
```

Output:

```text
outputs/experiments/062_source_profiled_geometry_window_noise10
```

Tracker:

```text
docs/experiments/33_geometry_window_stress.md
```

Result:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| nominal_noise10_seed13 | 250.0 | 90.0 | 6.0 | 6.2 | 5.236e-04 |
| source_mismatch_noise10_seed13 | 250.0 | 90.0 | 6.0 | 6.2 | 6.715e-04 |

Decision:

```text
Move to Stage 4 multi-rebar extension. Keep confidence reporting mandatory:
under 10% noise, the correct radius wins in the wider window but margins are
small relative to the noisy objective floor.
```

### Stage 4A: Multi-Rebar Common-Radius Profile

Status:

```text
passed fixed-position common-radius gate
```

Implementation:

```text
run_multi_rebar_common_radius_profile.py
tests/test_multi_rebar_common_radius_profile.py
```

Output:

```text
outputs/experiments/063_multi_rebar_common_radius_profile
```

Tracker:

```text
docs/experiments/34_multi_rebar_common_radius.md
```

Result:

| Case | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: |
| nominal | 6.0 | 6.2 | 1.122e-03 |
| noise10_seed13 | 6.0 | 6.2 | 9.930e-04 |
| source_mismatch | 6.0 | 6.2 | 1.221e-03 |
| source_mismatch_noise10_seed13 | 6.0 | 6.2 | 1.090e-03 |

Decision:

```text
Proceed to per-rebar radius identifiability before full 9-parameter
multi-rebar optimization. The common-radius result is strong, but it does not
yet prove that individual rebar sizes are separable when neighboring rebars
remain fixed.
```

### Stage 4B: Per-Rebar Radius Identifiability

Status:

```text
passed fixed-position one-at-a-time radius gates, with weaker margins than the
common-radius sweep
```

Outputs:

```text
outputs/experiments/064_multi_rebar_center_radius_profile
outputs/experiments/065_multi_rebar_left_radius_profile
outputs/experiments/066_multi_rebar_right_radius_profile
```

Tracker:

```text
docs/experiments/34_multi_rebar_common_radius.md
```

Margin summary:

| Swept rebar | Nominal margin | 10% noise margin | Mismatch margin | Mismatch 10% noise margin |
| --- | ---: | ---: | ---: | ---: |
| left index 0 | 3.737e-04 | 2.263e-04 | 4.235e-04 | 3.117e-04 |
| center index 1 | 4.145e-04 | 3.194e-04 | 4.591e-04 | 3.314e-04 |
| right index 2 | 3.658e-04 | 4.766e-04 | 4.013e-04 | 5.033e-04 |

Decision:

```text
Run a one-rebar-at-a-time local x/z/r coupling diagnostic before full
multi-rebar optimization. Fixed-position per-rebar sizing is correct, but the
smaller margins mean position/radius ambiguity could be important.
```

### Stage 4C-Left: Multi-Rebar Local X/Z/R Coupling

Status:

```text
passed left-rebar local geometry gate under 10% noise
```

Implementation:

```text
run_multi_rebar_local_geometry_profile.py
tests/test_multi_rebar_local_geometry_profile.py
```

Output:

```text
outputs/experiments/067_multi_rebar_left_local_geometry_noise10
```

Tracker:

```text
docs/experiments/35_multi_rebar_local_geometry_coupling.md
```

Result:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| noise10_seed13 | 150.0 | 90.0 | 6.0 | 6.2 | 2.263e-04 |
| source_mismatch_noise10_seed13 | 150.0 | 90.0 | 6.0 | 6.2 | 3.117e-04 |

Decision:

```text
Run center-rebar local x/z/r coupling next. The weakest fixed-position rebar
passed, but the margins are small enough that a confidence layer remains
mandatory before full multi-rebar optimization.
```

### Stage 4C-Center: Multi-Rebar Local X/Z/R Coupling

Status:

```text
passed center-rebar local geometry gate under 10% noise
```

Output:

```text
outputs/experiments/068_multi_rebar_center_local_geometry_noise10
```

Result:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| noise10_seed13 | 250.0 | 90.0 | 6.0 | 6.2 | 3.194e-04 |
| source_mismatch_noise10_seed13 | 250.0 | 90.0 | 6.0 | 6.2 | 3.314e-04 |

Decision:

```text
Run the right-rebar local coupling check to complete Stage 4C, then build a
confidence/reporting layer before considering full 9-parameter multi-rebar
optimization.
```

### Stage 4C-Right: Multi-Rebar Local X/Z/R Coupling

Status:

```text
passed right-rebar local geometry gate under 10% noise
```

Output:

```text
outputs/experiments/069_multi_rebar_right_local_geometry_noise10
```

Result:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| noise10_seed13 | 350.0 | 90.0 | 6.0 | 6.2 | 4.766e-04 |
| source_mismatch_noise10_seed13 | 350.0 | 90.0 | 6.0 | 6.2 | 5.033e-04 |

Stage 4C decision:

```text
All left, center, and right one-rebar-at-a-time local x/z/r coupling checks
pass in the 3-rebar scene under 10% noise and source mismatch. Correct
geometry/radius candidates win, but margins are still thin enough that full
multi-rebar optimization needs explicit confidence and ambiguity reporting
before it is promoted.
```

### Stage 5: Confidence/Reporting Layer Before Full Multi-Rebar Optimization

Goal:

```text
Turn the local geometry profiles into decision-grade outputs instead of only
single best estimates.
```

Required fields:

```text
best x/z/r,
top-k geometry candidates,
best-vs-next distinct-radius margin,
relative margin against best objective,
competing z/r branch,
selected source frequency scale,
selected source time shift,
selected amplitude scale,
plot validation metadata.
```

Decision gate:

```text
Only promote a full 9-parameter multi-rebar optimizer after the reporting layer
can clearly label strong, weak, and ambiguous radius estimates across the
single-rebar and 3-rebar synthetic cases.
```

Status:

```text
implemented and applied to Stage 4C runs in Experiment 36
```

Output:

```text
outputs/experiments/070_multi_rebar_stage4c_confidence_report
docs/experiments/36_multi_rebar_confidence_reporting.md
```

Result:

| Target/case group | Correct x/z/r? | Confidence label outcome |
| --- | --- | --- |
| left 10% noise cases | yes | weak, weak |
| center 10% noise cases | yes | weak, weak |
| right 10% noise cases | yes | weak, moderate |

Decision:

```text
Confidence reporting is now mandatory. The next GPU branch should replicate
Stage 4C over more noise seeds before full 9-parameter optimization, because
correct estimates are repeatable in the tested seed but mostly weak-confidence.
```

### Stage 6: Additional Noise-Seed Confidence Replication

Goal:

```text
Measure how often each target rebar keeps the true radius and how often the
confidence label stays weak/moderate/strong across multiple 10% noise seeds.
```

Recommended first run:

```text
repeat local x/z/r coupling for the weakest left-rebar target with another
10% noise seed and source-mismatch case, using --backend gpu-cpml.
```

Decision gate:

```text
If additional seeds continue to recover x/z/r truth but remain weak-confidence,
build a full reporting-first optimizer. If any seed flips to the deeper/larger
branch, add a fallback rule that reports an ambiguous radius interval rather
than a single radius estimate.
```

First result:

```text
run 071, left rebar, seed 21, passed true x/z/r in nominal and source-mismatch
10% noise cases.
```

Confidence:

| Case | Best x/z/r | Margin | Relative margin | Label |
| --- | --- | ---: | ---: | --- |
| noise10_seed21 | 150 / 90 / 6.0 | 5.112e-04 | 0.647% | moderate |
| source_mismatch_noise10_seed21 | 150 / 90 / 6.0 | 3.894e-04 | 0.442% | weak |

Decision:

```text
Continue left-rebar seed replication, batching multiple observed seed/source
cases in one GPU candidate-grid run so candidate wavefields are reused.
```

Left-rebar aggregate:

```text
seeds 13, 21, 34, 55: 8/8 nominal/source-mismatch 10% noise cases recovered
true x=150 mm, z=90 mm, r=6.0 mm.
```

Confidence aggregate:

| Cases | Weak | Moderate | Strong | Margin min | Margin mean | Margin max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 7 | 1 | 0 | 2.263e-04 | 3.635e-04 | 5.112e-04 |

Updated decision:

```text
Move seed replication to center and right rebars. The left-rebar radius is
repeatable but weak-confidence, so final output must report uncertainty.
```

Center-rebar aggregate:

```text
seeds 13, 21, 34, 55: 8/8 nominal/source-mismatch 10% noise cases recovered
true x=250 mm, z=90 mm, r=6.0 mm.
```

Confidence aggregate:

| Cases | Weak | Moderate | Strong | Margin min | Margin mean | Margin max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 8 | 0 | 0 | 1.257e-04 | 3.202e-04 | 3.992e-04 |

Updated decision:

```text
Move seed replication to the right rebar. The center-rebar radius is repeatable
but all tested cases are weak-confidence, so ambiguity reporting remains
mandatory.
```

Right-rebar aggregate:

```text
seeds 13, 21, 34, 55: 8/8 nominal/source-mismatch 10% noise cases recovered
true x=350 mm, z=90 mm, r=6.0 mm.
```

Confidence aggregate:

| Cases | Weak | Moderate | Strong | Margin min | Margin mean | Margin max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 7 | 1 | 0 | 1.947e-04 | 3.344e-04 | 5.033e-04 |

Stage 6 synthesis:

```text
24/24 left/center/right seed-replication cases recover the true target x/z/r.
22/24 are weak-confidence, 2/24 are moderate-confidence, and 0/24 are
strong-confidence.
```

Output:

```text
outputs/experiments/079_multi_rebar_stage6_all_targets_confidence_report
docs/experiments/40_stage6_all_target_confidence_synthesis.md
```

Stage 6 decision:

```text
The local source-profiled geometry selector is repeatable, but the result must
not be reported as a single unqualified radius. Implement ambiguity intervals
and fallback warnings before promoting full 9-parameter optimization.
```

### Stage 7: Ambiguity Interval / Fallback Reporting

Goal:

```text
Convert weak-confidence ranked candidates into honest report fields:
best estimate, plausible radius interval, competing geometry branch, and
fallback warning.
```

Initial rule:

```text
For weak-confidence cases, include all top candidates within a small objective
tolerance above the best candidate and report the radius/x/z span. The default
tolerance should be configurable and tested; it should not hide the recurring
1 mm deeper / larger-radius branch.
```

Decision gate:

```text
Do not launch full 9-parameter optimization until the ambiguity report can
turn the Stage 6 weak cases into a clear interval/warning instead of only a
single x/z/r number.
```

Status:

```text
implemented and applied to the 24-case Stage 6 matrix
```

Output:

```text
outputs/experiments/080_multi_rebar_stage7_ambiguity_interval_report
docs/experiments/41_ambiguity_interval_reporting.md
```

Result:

| Metric | Value |
| --- | ---: |
| Stage 6 rows | 24 |
| Fallback warning rows | 22 |
| Rows without fallback warning | 2 |
| Rows with ambiguity z max = 91 mm | 24 |
| Rows with ambiguity radius max = 6.8 mm | 9 |
| Rows with ambiguity radius max = 7.0 mm | 15 |

Stage 7 decision:

```text
Ambiguity/fallback reporting is now available and must be included in future
optimizer outputs. The next optimizer branch should be reporting-first: no
single x/z/r result is acceptable without confidence label, interval, and
competing branch fields.
```

### Stage 8: Reporting-First Full Multi-Rebar Optimizer Design

Goal:

```text
Design a full multi-rebar search/refinement workflow that reuses the local
source-profiled candidate machinery and emits the Stage 7 confidence fields.
```

Initial scope:

```text
avoid a blind 9-parameter black-box search,
use staged one-target-at-a-time coordinate windows,
reuse modeled candidate wavefields across observed cases where possible,
write a combined report with per-target ambiguity intervals.
```

Status:

```text
implemented and passed the compact exact/source-mismatch GPU gate
```

Implementation:

```text
inversion/multi_rebar_coordinate.py
run_multi_rebar_coordinate_optimizer.py
tests/test_multi_rebar_coordinate.py
tests/test_multi_rebar_coordinate_optimizer.py
```

Output:

```text
outputs/experiments/081_coordinate_optimizer_cpu_smoke
outputs/experiments/082_coordinate_optimizer_gpu_compact_perturbed_seed
docs/experiments/42_reporting_first_coordinate_optimizer.md
```

Result:

| Target | Initial x/z/r [mm] | Final x/z/r [mm] | Nominal label |
| ---: | --- | --- | --- |
| 0 | 149 / 91 / 6.2 | 150 / 90 / 6.0 | weak |
| 1 | 251 / 89 / 5.8 | 250 / 90 / 6.0 | strong |
| 2 | 349 / 91 / 6.2 | 350 / 90 / 6.0 | weak |

Decision:

```text
The reporting-first coordinate optimizer is ready for robustness replication,
not for unqualified production use. Keep confidence labels, fallback warnings,
and ambiguity intervals mandatory. The next stage is 10% noise/source-mismatch
seed replication for the full sequential coordinate loop.
```

### Stage 8A: Coordinate Optimizer Replication

Status:

```text
complete
```

Output:

```text
outputs/experiments/083_coordinate_optimizer_noise10_seed13
outputs/experiments/084_coordinate_optimizer_noise10_seed21
outputs/experiments/086_coordinate_optimizer_noise10_seed34
outputs/experiments/088_coordinate_optimizer_noise10_seed55
outputs/experiments/089_coordinate_optimizer_noise_seed13_21_34_55_aggregate
docs/experiments/43_coordinate_optimizer_noise_replication.md
```

Result:

```text
compact 1 mm x/z, 0.2 mm radius seed offset:
  4/4 seeds recovered true final x/z/r
  24/24 confidence rows selected true x/z/r
  edge targets remained mostly weak
  center target remained strong
```

Decision:

```text
the compact coordinate loop is robust enough to stress with larger seed errors
instead of adding more compact replications.
```

### Stage 8B: Guarded Revisit For 2 mm Coordinate Stress

Status:

```text
complete
```

Output:

```text
outputs/experiments/090_coordinate_optimizer_seed_offset2mm_noise10_seed13
outputs/experiments/091_coordinate_optimizer_seed_offset2mm_target0_revisit_seed13
outputs/experiments/092_coordinate_optimizer_seed_offset2mm_order120_noise10_seed13
outputs/experiments/093_coordinate_optimizer_seed_offset2mm_target2_revisit_seed13
outputs/experiments/094_coordinate_optimizer_seed_offset2mm_guarded_revisit_seed13
outputs/experiments/095_coordinate_optimizer_seed_offset2mm_guarded_revisit_seed21
outputs/experiments/097_coordinate_optimizer_seed_offset2mm_guarded_revisit_seed34
outputs/experiments/098_coordinate_optimizer_seed_offset2mm_guarded_seed13_21_34_aggregate
docs/experiments/44_coordinate_optimizer_seed_offset_stress.md
```

Result:

```text
unguarded 2 mm stress:
  coordinate loop can choose a weak high-radius edge branch

manual focused revisit:
  recovers the true lower-radius branch after neighboring targets improve

automated guarded revisit:
  3/3 guarded seeds recovered true final x/z/r
  row-level radius confidence still weak for edge targets
  source mismatch can leave target 2 nearly flat between 6.0 and 6.2 mm
```

Decision:

```text
promote guarded revisit for larger-offset coordinate searches. Do not claim
radius certainty from the final state alone; keep confidence labels and
ambiguity intervals mandatory.
```

### Stage 9: Radius-Confidence Objective Comparison

Goal:

```text
improve edge-target radius discrimination after coordinate recovery, especially
under source mismatch, without hiding ambiguity.
```

Initial scope:

```text
reuse the existing GPU candidate machinery,
compare current source-profiled LS against frequency/time weighting variants,
evaluate on the seed-offset guarded cases where target 2 is weak,
rank objectives by true-radius margin and ambiguity interval shrinkage.
```

Paper motivation:

```text
progressive bandwidth and cumulative-frequency papers:
  test whether later-stage radius polish needs high-frequency or time-window
  emphasis instead of a uniform full-trace norm

Wasserstein / OT papers:
  use only if the objective landscape becomes smoother or more discriminative;
  do not promote OT machinery merely because it is available

implicit multiparameter paper:
  keep material/radius ambiguity visible in confidence reporting rather than
  collapsing weakly identifiable candidates into a single answer
```

Result:

```text
experiments 100, 102, 103, 104:
  post-correction target-0/target-2 radius matrices select the true 6.0 mm
  radius across seeds 13 and 34

experiment 101:
  high-band and early-reflection variants strengthen the wrong target-0
  high-radius branch before guarded revisit, so they cannot replace the guard

experiment 106:
  guarded seed-55 coordinate optimizer recovers the true final geometry, while
  diagnostics show high-band helps some post-correction margins and early
  reflection is not robust enough for production use
```

Decision:

```text
keep source-profiled LS plus guarded revisit as the update rule,
keep radius confidence labels and ambiguity intervals mandatory,
use high-band as a diagnostic/reporting variant only,
do not promote early-reflection or OT/W2 into the production optimizer yet.
```

Visualization completion:

```text
animations now distinguish true forward, candidate forward, true-vs-candidate,
and residual back-propagation products. Previous single-rebar experiments
052-062 have scientifically labelled GIFs and validation metadata. Stage 9
animations 100-104 were regenerated or supplemented with Tx/Rx markers.
Experiment 056 now has material-aware forward animation support for the actual
low-conductivity steel candidate.
```

### Stage 10A: Detection-To-FWI Seed Layer

Goal:

```text
bridge from observed B-scan to FWI candidate windows instead of assuming known
target locations.
```

Result:

```text
experiment 107:
  no detector time offset gave correct x but a false deep z, proving source
  timing calibration is required

experiment 109:
  offset-grid detector found the default single rebar at x=250 mm, z=95 mm,
  within a 5 mm depth error of truth

experiment 110:
  offset-grid detector found all three same-depth rebars at x errors of 2 mm
  and z errors of 0 mm

experiment 111:
  detector-seeded source-profiled polish recovered x=250 mm, z=90 mm,
  r=6.0 mm, but the 1 mm source-profiled grid took 1060.8 s for 66 candidates
```

Decision:

```text
keep the detector as an x/z seed-window generator, not a radius estimator.
Use a small detector time-offset grid for synthetic Ricker-source benchmarks.
Before large benchmark sweeps, build a cheaper two-stage refinement: 2 mm
coarse screen first, then narrow 1 mm source-profiled polish only for
surviving windows.
```

### Stage 10B: Detector-Only Generalization

Result:

```text
experiment 112:
  single-rebar nominal detector matrix hit 48/48 across depths 70-130 mm,
  radii 4-10 mm, and 0-10% noise

experiment 113:
  same matrix under source mismatch also hit 48/48

experiment 114:
  close-spacing 3-rebar same-depth scene under 10% noise/source mismatch found
  all three rebars within tolerance

experiment 115:
  variable-depth 3-rebar scene under 10% noise/source mismatch found all three
  rebars within tolerance, but produced alias candidates that must be filtered
  by refinement/confidence
```

Decision:

```text
the detector is ready to become the x/z seed stage for a 2D pipeline. The next
research/development stage is not more detector tuning; it is a two-stage
detector-to-refinement runner that screens top-k windows cheaply before
running 1 mm source-profiled polish.
```

### Stage 10C Smoke: Coarse-To-Fine Refinement

Result:

```text
experiment 111 direct 1 mm source-profiled grid:
  66 candidates, 1060.8 s, final r=6.0 mm, margin=9.8148e-04

experiments 116-117 manual two-stage path:
  2 mm screen: 66 candidates, 238.5 s, true branch selected but radius margin
  tied at zero
  narrow 1 mm polish: 15 candidates, 240.3 s, final r=6.0 mm,
  margin=9.8148e-04
```

Decision:

```text
package the two-stage coarse-to-fine logic as a repeatable runner. It preserved
the final radius result while cutting runtime by about 55% in the first smoke.
```

### Stage 10D: Packaged Two-Stage Refinement Runner

Implementation:

```text
run_detection_seeded_two_stage_refinement.py
tests/test_detection_seeded_two_stage_refinement.py
```

Result:

```text
experiment 118:
  detector rank 1 seed: x=250 mm, z=95 mm
  2 mm coarse screen: 77 candidates, best x=250 mm, z=90 mm, r=6.0 mm,
  radius margin=0.0
  1 mm fine polish: 15 candidates, best x=250 mm, z=90 mm, r=6.0 mm,
  radius margin=9.8148e-04
  final truth errors: x=0 mm, z=0 mm, radius=0 mm
  overall wall time=545.6 s
```

Decision:

```text
use this runner as the default packaged single-rebar prototype. Before a large
replication matrix, refactor the source-profiled polish runner so arbitrary
single-rebar truth x/z/r can be passed through the same code path. This avoids
silently reusing the default x=250 mm, z=90 mm, r=6 mm truth for scenarios that
look different in the detector stage.
```

### Stage 10E: Scenario-Aware Single-Rebar Refinement

Implementation:

```text
run_single_rebar_source_profiled_polish.py:
  added --truth-x-mm, --truth-z-mm, --truth-radius-mm
  added optional --initial-x-mm, --initial-z-mm, --initial-radius-mm

run_detection_seeded_two_stage_refinement.py:
  passes truth geometry into coarse and fine polish subprocesses
```

Result:

```text
experiment 119:
  truth x=250 mm, z=110 mm, r=8 mm
  detector rank 1 seed: x=250 mm, z=110 mm
  2 mm coarse screen: 49 candidates, best x=250 mm, z=110 mm, r=8.0 mm,
  radius margin=0.0
  1 mm fine polish: 15 candidates, best x=250 mm, z=110 mm, r=8.0 mm,
  radius margin=2.1871e-03
  final truth errors: x=0 mm, z=0 mm, radius=0 mm
```

Decision:

```text
the packaged runner is now scenario-aware for one-rebar synthetic cases. Run a
small stress replication next: source mismatch and 5-10% noise, then a
shallower/smaller-radius case where detector aliases are more likely.
```

### Stage 10F: Source-Mismatch/Noise Packaged Stress

Result:

```text
experiment 120:
  truth x=250 mm, z=110 mm, r=8 mm
  observed source frequency scale=1.1, time shift=-50 ps, amplitude=1.1
  observed noise=10% RMS
  detector rank 1 seed: x=250 mm, z=110 mm
  2 mm coarse screen: best x=250 mm, z=110 mm, r=8.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.08994,
  radius margin=0.0
  1 mm fine polish: best x=250 mm, z=110 mm, r=8.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.09609,
  radius margin=2.4303e-03 absolute / 1.288% relative
  final truth errors: x=0 mm, z=0 mm, radius=0 mm
```

Decision:

```text
the packaged single-rebar pipeline survives the first non-default
source-mismatch/noise stress. Test one shallow small-radius case next, because
small bars and shallow arrivals should be a harder radius/aliasing regime than
the r=8 mm deeper case.
```

### Stage 10G: Shallow Small-Radius Packaged Stress

Result:

```text
experiment 121:
  truth x=250 mm, z=70 mm, r=4 mm
  observed source frequency scale=1.1, time shift=-50 ps, amplitude=1.1
  observed noise=10% RMS
  detector rank 1 seed: x=250 mm, z=75 mm
  2 mm coarse screen: best x=250 mm, z=70 mm, r=4.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.10453,
  radius margin=0.0
  1 mm fine polish: best x=250 mm, z=70 mm, r=4.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.09765,
  radius margin=5.99997e-04 absolute / 0.203% relative
  final truth errors: x=0 mm, z=0 mm, radius=0 mm
```

Decision:

```text
point estimation passed, but the radius confidence is much weaker for shallow
r=4 mm than for deeper r=8 mm. Build an aggregate layer for packaged two-stage
runs and replicate this hard case across noise seeds before promoting the
single-rebar pipeline as robust.
```

### Stage 10H: Packaged Two-Stage Aggregate Reporting

Implementation:

```text
run_two_stage_refinement_aggregate.py
tests/test_two_stage_refinement_aggregate.py
```

Result:

```text
experiment 122:
  aggregated packaged runs 118-121
  all four point estimates recovered x/z/r exactly
  confidence labels:
    118 strong
    119 strong
    120 strong
    121 weak
```

Decision:

```text
use aggregate reports after every small batch of packaged two-stage runs. The
next experiment batch should replicate the weak-margin shallow r=4 mm
source-mismatch/noise case across additional noise seeds, not expand to a broad
matrix prematurely.
```

### Stage 10I: Shallow Small-Radius Seed Replication

Result:

```text
experiment 123:
  same geometry/source/noise level as 121, noise seed 21
  detector rank 1 seed: x=250 mm, z=75 mm
  2 mm coarse screen: best x=250 mm, z=70 mm, r=4.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.10366,
  radius margin=0.0
  1 mm fine polish: best x=250 mm, z=70 mm, r=4.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.08687,
  radius margin=6.62067e-04 absolute / 0.225% relative
  final truth errors: x=0 mm, z=0 mm, radius=0 mm
```

Decision:

```text
the weak-margin shallow r=4 mm behavior repeated under a second noise seed.
Run at least one more seed and regenerate the aggregate report before deciding
whether this branch needs a refined objective or simply a lower confidence
label.
```

### Stage 10J: Third Shallow Small-Radius Seed

Result:

```text
experiment 124:
  same geometry/source/noise level as 121 and 123, noise seed 34
  detector rank 1 seed: x=250 mm, z=75 mm
  2 mm coarse screen: best x=250 mm, z=70 mm, r=4.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.10576,
  radius margin=0.0
  1 mm fine polish: best x=250 mm, z=70 mm, r=4.0 mm,
  recovered source scale=1.1, shift=-50 ps, amplitude=1.09842,
  radius margin=5.67544e-04 absolute / 0.194% relative
  final truth errors: x=0 mm, z=0 mm, radius=0 mm
```

Decision:

```text
the shallow r=4 mm source-mismatch/noise case is consistently correct but
weakly separated. Regenerate the aggregate report and then test whether denser
radius sampling around 4 mm improves confidence or merely reveals a flat
objective around the correct size.
```

### Stage 10K: Replicated Weak-Margin Aggregate

Result:

```text
experiment 125:
  aggregate over 118, 119, 120, 121, 123, 124
  all point estimates have x/z/r error 0
  strong confidence: 118, 119, 120
  weak confidence: 121, 123, 124
  weak branch = z=70 mm, r=4 mm, source mismatch, 10% noise
```

Decision:

```text
the shallow/small-radius branch is a confidence limitation, not a point
estimate failure in the current seeds. Next test denser radius sampling around
4 mm to determine whether the objective has a meaningful narrow minimum or
should be reported as an interval.
```

### Stage 10L: Dense-Radius Ambiguity Diagnostic

Result:

```text
experiment 126:
  same shallow r=4 mm mismatch/noise seed-13 case as 121
  fine radius grid 3.7:4.3:0.1 mm
  best x=250 mm, z=70 mm, r=4.0 mm
  next radius r=4.1 mm ties exactly
  fine radius margin=0.0
  local objective at z=70:
    r=3.7/3.8/3.9 -> 0.2960123712
    r=4.0/4.1 -> 0.2952422893
```

Decision:

```text
the shallow r=4 mm branch needs ambiguity-interval reporting. Add interval
calculation to the packaged runner/aggregate layer, then test whether 1 mm
subcell fine geometry reduces the 4.0-4.1 mm tie or simply changes the bias.
```

### Stage 10M: Radius Ambiguity Interval Reporting

Implementation:

```text
inversion/radius_confidence.py
run_single_rebar_source_profiled_polish.py
run_detection_seeded_two_stage_refinement.py
run_two_stage_refinement_aggregate.py
tests/test_radius_confidence.py
```

Result:

```text
experiment 127 aggregate with interval columns:
  118 exact interval 6.0-6.0, weak interval 6.0-6.2
  119 exact interval 8.0-8.0, weak interval 8.0-8.0
  120 exact interval 8.0-8.0, weak interval 8.0-8.0
  121/123/124 exact interval 4.0-4.0, weak interval 3.8-4.2
  126 exact interval 4.0-4.1, weak interval 3.7-4.2
```

Decision:

```text
the current production-style report should include radius intervals for weak
branches. The next physics/objective test is 1 mm subcell fine geometry on the
same shallow r=4 mm case, to see whether the exact 4.0-4.1 tie is a hard-grid
geometry quantization artifact or a true waveform ambiguity.
```

### Stage 10N: Subcell Geometry Diagnostic

Implementation:

```text
run_single_rebar_source_profiled_polish.py exposes --geometry-mode and
--subcell-samples

run_detection_seeded_two_stage_refinement.py exposes detection/refinement
geometry-mode controls
```

Result:

```text
experiment 128:
  same shallow r=4 mm mismatch/noise seed-13 case as 126
  detection/refinement geometry = subcell, 5 samples
  detector rank 1 seed: x=250 mm, z=75 mm
  coarse best: x=250 mm, z=70 mm, r=4.0 mm, margin=1.2718e-04
  fine best: x=250 mm, z=70 mm, r=4.0 mm
  next radius: 3.9 mm
  fine margin=8.6199e-05 absolute / 0.0285% relative
  exact interval=4.0-4.0 mm
  weak interval=3.7-4.3 mm
```

Decision:

```text
subcell geometry breaks the exact hard-grid 4.0-4.1 mm tie but does not produce
a confident radius. Keep interval reporting. The next method test should focus
on objective information content, likely multifrequency/bandwidth weighting,
rather than more geometry smoothing alone.
```

### Stage 10O: Hard/Subcell Aggregate Comparison

Result:

```text
experiment 129:
  compares hard dense-radius run 126 and subcell dense-radius run 128
  hard exact interval: 4.0-4.1 mm
  hard weak interval: 3.7-4.2 mm
  subcell exact interval: 4.0-4.0 mm
  subcell weak interval: 3.7-4.3 mm
```

Decision:

```text
geometry smoothing reduces exact quantization ties but does not create enough
information to report a confident radius in the shallow r=4 mm noisy/source
mismatched case. The next test should add objective information, not just more
geometry smoothing.
```

### Stage 10P: Aggregate Zero-Error Plot Repair

Result:

```text
experiment 130:
  regenerated the aggregate plot with explicit zero-error markers
  fixed the misleading blank-looking top panel when all radius errors are zero
```

Decision:

```text
keep zero-valued metrics visibly marked in future plots. Continue to the
objective-information branch: multifrequency or bandwidth-weighted
source-profiled fine refinement for the shallow r=4 mm case.
```

### Stage 10Q: Equal-Weight Multifrequency Diagnostic

Implementation:

```text
run_single_rebar_source_profiled_polish.py supports --frequencies-ghz and
--frequency-weights, with shared source frequency-scale/time-shift across base
frequencies and per-frequency amplitude fits.
```

Result:

```text
experiment 131:
  shallow r=4 mm mismatch/noise seed-13 case
  refinement base frequencies 1.0 and 1.5 GHz, equal weights
  best x=250 mm, z=70 mm, r=4.0 mm
  next radius r=4.1 mm ties exactly
  fine radius margin=0.0
  exact interval=4.0-4.1 mm
  weak interval=3.7-4.3 mm
  runtime=1514.5 s
```

Decision:

```text
equal-weight lower+nominal frequency does not sharpen radius confidence and
costs about twice as much. Do not promote it. Next test high-frequency
information: 1.5+2.0 GHz or high-frequency-weighted multifrequency refinement.
```

### Stage 10R: Equal-Weight High-Frequency Diagnostic

Result:

```text
experiment 132:
  shallow r=4 mm mismatch/noise seed-13 case
  refinement base frequencies 1.5 and 2.0 GHz, equal weights
  best x=250 mm, z=70 mm, r=4.0 mm
  next radius r=4.1 mm ties exactly
  fine radius margin=0.0
  exact interval=4.0-4.1 mm
  weak interval=3.7-4.3 mm
  runtime=1514.7 s
```

Decision:

```text
equal-weight high-frequency LS also fails to sharpen the interval. Do not
spend more GPU budget on brute-force equal-weight frequency pairs until a
better weighting or objective-selection rule is implemented and justified.
```

### Stage 10S: Multifrequency Aggregate Synthesis

Result:

```text
experiment 133:
  aggregates experiments 118, 119, 120, 121, 123, 124, 126, 128, 131, 132
  weak-confidence rows: 121, 123, 124, 126, 128, 131, 132
  all final point-radius errors remain 0.0 mm
```

Decision:

```text
the point estimate is no longer the limiting metric. Radius interval width,
radius margin, source/profile fit, and runtime must drive the next branch
selection.
```

### Stage 10T: Interval And Runtime Reporting

Implementation:

```text
run_two_stage_refinement_aggregate.py now writes an interval/runtime plot
alongside the repaired radius-error/margin plot.
```

Result:

```text
experiment 134:
  widest weak interval width=0.600 mm
  widest weak interval runs=128, 131, 132
  equal-weight multifrequency runs 131 and 132 roughly double runtime
  no practical confidence improvement over dense single-frequency reporting
```

Decision:

```text
stop brute-force equal-weight multifrequency sweeps. The next test-driven
development step is per-candidate diagnostic instrumentation: record
per-frequency objective terms and then use those curves to choose selective
weights or reject the branch before another expensive GPU run.
```

### Stage 10U: Per-Candidate Frequency Diagnostics

Implementation:

```text
run_single_rebar_source_profiled_polish.py now writes per-frequency misfit and
amplitude columns in the candidate CSV and creates a multifrequency
decomposition plot of the combined-best radius curve.
```

Result:

```text
experiment 135:
  GPU smoke on shallow z=70 mm, r=4 mm, noise/source-mismatch case
  candidate radii=3.9, 4.0, 4.1 mm
  best radius=4.0 mm
  next radius=4.1 mm
  radius margin=0.0
  exact interval=4.0-4.1 mm
  per-frequency misfit at best: 1.0 GHz=0.02031, 1.5 GHz=0.26119
```

Decision:

```text
diagnostics are now sufficient to inspect frequency contributions before
longer sweeps. The 4.0 and 4.1 mm hard-grid candidates remain identical in the
stored per-frequency terms, so the next branch should test whether the tie is
primarily a geometry rasterization/shape-discretization issue rather than a
frequency-weighting issue.
```

### Stage 10V: Hard-Grid Geometry Quantization

Result:

```text
experiment 136:
  1 mm grid, x=250 mm, z=70 mm, radius=3.7:4.3:0.1 mm
  hard-grid zero adjacent deltas at 3.8, 3.9, and 4.1 mm
  hard-grid 4.0 -> 4.1 mm log-conductivity delta=0.000
  subcell 4.0 -> 4.1 mm log-conductivity delta=23.400
```

Decision:

```text
the hard-grid 4.0/4.1 mm exact tie is physically unresolvable because the
FDTD material arrays are identical. Future radius polishing for small shallow
rebars should not rely on hard-grid radii finer than the grid can represent.
Use subcell geometry or a finer forward grid for radius claims, and keep
interval reporting when waveform information remains weak.
```

### Stage 10W: Subcell Tie Diagnostic

Result:

```text
experiment 137:
  same small multifrequency diagnostic as 135
  geometry=subcell with 5x5 samples
  best radius=3.9 mm
  next radius=4.0 mm
  margin=3.2492e-05
  exact interval=3.9-3.9 mm
  weak interval=3.9-4.0 mm
```

Decision:

```text
subcell geometry resolves the impossible hard-grid equality but introduces a
slight low-radius preference under this noisy/source-mismatched setup. Treat
the result as interval evidence, not a final point-size improvement. Next,
test whether increasing subcell samples stabilizes the subcell geometry before
paying for a finer forward grid.
```

### Stage 10X: Subcell-Sample Convergence

Result:

```text
experiment 138:
  same diagnostic as 137 but with 9x9 subcell samples
  best radius=4.0 mm
  next radius=3.9 mm
  margin=1.13348e-05
  exact interval=4.0-4.0 mm
  weak interval=3.9-4.1 mm
```

Decision:

```text
higher subcell sampling stabilizes the point estimate back to truth, but the
confidence margin remains too small. Use 9x9 subcell sampling for future
small-radius diagnostics when affordable, but still report a radius interval.
The next meaningful escalation is either a slightly wider 9x9 subcell radius
profile or a finer forward grid, chosen by GPU budget.
```

### Stage 10Y: Wider 9x9 Subcell Profile

Result:

```text
experiment 139:
  fixed true x/z, radii=3.7:4.3:0.1 mm
  geometry=subcell, 9x9 samples
  frequencies=1.0 and 1.5 GHz
  best radius=4.0 mm
  next radius=3.9 mm
  margin=1.13348e-05
  exact interval=4.0-4.0 mm
  weak interval=3.7-4.1 mm
```

Decision:

```text
9x9 subcell gives the correct point radius at the true location, but the
objective landscape is still too flat for a confident point-size claim. Do not
spend more time on equal-weight frequency tuning for this branch. Escalate to
one of: calibrated noise-threshold reporting, more acquisition information, or
a small finer-grid forward smoke.
```

### Stage 10Z: Acquisition-Density Diagnostic

Result:

```text
experiment 140:
  same 9x9 subcell radius profile as 139 but with 9 sources instead of 3
  best radius=4.0 mm
  next radius=3.9 mm
  margin=8.08056e-05
  exact interval=4.0-4.0 mm
  weak interval=3.7-4.0 mm
```

Decision:

```text
more acquisition positions improve radius separation and shrink the weak
interval upper side, but not enough for a high-confidence point-size claim.
Acquisition density is a useful lever and should be considered in the eventual
pipeline, especially before trying much more expensive grid refinement.
```

### Stage 10AA: Post-Hoc Frequency Reweighting

Implementation:

```text
run_source_profiled_frequency_reweight_diagnostic.py reuses per-frequency
candidate CSV terms to evaluate frequency weights without rerunning FDTD.
```

Result:

```text
experiment 141:
  source CSV from experiment 140
  weights equal, hi2, hi4, hi8, hi16
  best radius=4.0 mm for every case
  margin improves from 8.08056e-05 to 1.31868e-04
  weak interval remains 3.7-4.0 mm for every case
```

Decision:

```text
high-frequency weighting improves the numeric margin but does not shrink the
practical interval. Do not run a full weighted GPU sweep yet. Prefer calibrated
uncertainty/noise-floor reporting or acquisition-density experiments.
```

### Stage 10AB: Noise-Seed Robustness

Result:

```text
experiments 142 and 143:
  repeat experiment 140 with noise seeds 21 and 34
  both recover best radius=4.0 mm
  both keep weak interval=3.7-4.0 mm
  margins: 1.68790e-04 and 8.52847e-05
```

Aggregate:

```text
experiment 144:
  rows=140, 142, 143
  best radii=4.0, 4.0, 4.0 mm
  weak intervals=3.7-4.0 mm for all rows
  margin range=8.08056e-05 to 1.68790e-04
```

Decision:

```text
the current best fixed-location shallow-radius setup is point-stable across
noise seeds but remains interval-limited. The result is publishable as an
uncertainty-aware finding: correct radius point estimate, stable lower-side
ambiguity, and a clear reason not to overstate size precision. Next, either
connect this fixed-location result back into detector-seeded two-stage runs or
test a small finer-grid smoke to see whether the lower-side interval is a
grid-resolution artifact.
```

### Stage 10AC: 0.5 mm Geometry Feasibility

Result:

```text
experiment 145:
  geometry-only diagnostic at 0.5 mm grid
  hard-grid zero adjacent deltas remain only at 3.8 mm
  hard-grid 4.0 -> 4.1 mm log-conductivity delta=144.000
  subcell 4.0 -> 4.1 mm log-conductivity delta=85.320
```

Decision:

```text
0.5 mm geometry is materially distinct around the target radius. A tightly
scoped 0.5 mm FDTD smoke is justified to test whether the lower-side radius
interval is partly a 1 mm grid-resolution artifact. Keep the first 0.5 mm run
small: fixed x/z, few sources, and three radii around 4.0 mm.
```

### Stage 10AD: 0.5 mm FDTD Smoke

Result:

```text
experiment 146:
  grid step=0.5 mm
  hard geometry
  fixed x=250 mm, z=70 mm
  radii=3.9, 4.0, 4.1 mm
  sources=3
  frequencies=1.0 and 1.5 GHz
  best radius=4.0 mm
  next radius=3.9 mm
  margin=9.47026e-05
  weak interval=3.9-4.1 mm
  runtime=372.9 s
```

Decision:

```text
0.5 mm removes the exact hard-grid tie and recovers the correct point radius,
but the interval remains weak and runtime is high. Treat 0.5 mm as a
verification tool, not the default. The stronger practical branch remains
1 mm grid with 9x9 subcell geometry, denser acquisition, and explicit
interval reporting.
```

### Stage 10AE: Local Depth-Radius Coupling

Result:

```text
experiment 147:
  1 mm grid, 9x9 subcell, 9 sources
  x=250 mm
  z=69,70,71 mm
  radii=3.9,4.0,4.1 mm
  best z=70 mm, radius=4.0 mm
  next radius=3.9 mm at z=70 mm
  margin=8.08056e-05
  weak interval across tested radii=3.9-4.0 mm
```

Decision:

```text
local depth-radius coupling does not explain the remaining ambiguity. The
pipeline can keep location/depth as a strength and report size as an
uncertainty interval. The next full-pipeline step should package this branch
as a guarded local refinement around detector/coarse seeds rather than widen
the local x/z search blindly.
```

### Stage 10AF: Guarded Polish Pipeline Packaging

Implementation:

```text
run_detection_seeded_two_stage_refinement.py now has an optional
--enable-guarded-polish stage. The guarded stage runs after the existing
detection/coarse/fine stages and records guarded_* plus final_* fields in the
root summary.
```

Result:

```text
experiment 148:
  detector rank 1: x=250 mm, z=75 mm
  coarse best: x=250 mm, z=70 mm, r=4.0 mm
  fine best: x=250 mm, z=70 mm, r=4.0 mm
  guarded final best: x=250 mm, z=70 mm, r=4.0 mm
  guarded setup: 1 mm grid, subcell 9x9, 9 sources, 1.0+1.5 GHz
  guarded weak interval=3.9-4.0 mm
  overall runtime=620.7 s
```

Aggregate:

```text
experiment 149:
  final-stage-aware aggregate for runs 118-132 plus 148
  run 148 weak interval=3.9-4.0 mm
  all final point radius errors remain 0.0 mm
```

Decision:

```text
guarded polish successfully connects the best fixed-location research branch
back to the detector-seeded pipeline. It improves the shallow-case practical
interval while preserving point accuracy. It should not yet be called strong:
repeat on additional noise seeds before making it the default final stage.
```

### Stage 10AG: Guarded Polish Seed Replication

Status:

```text
complete for shallow r=4 mm branch
```

Completed:

```text
[x] run packaged guarded pipeline on shallow r=4 mm, z=70 mm, noise seed 13
[x] run packaged guarded pipeline on shallow r=4 mm, z=70 mm, noise seed 21
[x] run packaged guarded pipeline on shallow r=4 mm, z=70 mm, noise seed 34
[x] aggregate guarded-package seeds and decide whether guarded polish is the default final stage
```

Evidence so far:

```text
seed 13 final: x=250 mm, z=70 mm, r=4.0 mm; weak interval=3.9-4.0 mm
seed 21 final: x=250 mm, z=70 mm, r=4.0 mm; weak interval=3.9-4.0 mm
seed 34 final: x=250 mm, z=70 mm, r=4.0 mm; weak interval=3.9-4.0 mm
```

Decision:

```text
guarded polish is now the recommended detector-seeded final confidence stage
for the shallow r=4 mm branch. The point estimate is exact across three noise
seeds, but the honest size report remains an interval: best r=4.0 mm with weak
interval 3.9-4.0 mm. The next test is generalization to the deeper/larger
r=8 mm branch using the same packaged guarded stage before adding new
optimizer machinery.
```

### Stage 10AH: Guarded Polish Deep/Larger-Radius Generalization

Status:

```text
complete for first deep r=8 mm probe
```

Planned evidence:

```text
[x] run the same guarded detector-seeded package on z=110 mm, r=8 mm with
    source mismatch and 10% noise
[x] compare final point error, radius margin, exact interval, weak interval,
    and runtime against the earlier non-guarded strong run 120
[x] decide whether guarded polish is a default final stage across both tested
    single-rebar regimes, or only a shallow-small-radius confidence tool
```

Reason:

```text
run 120 already solved the deeper r=8 mm case with a strong fine-stage
margin. The guarded stage should preserve that result without widening the
uncertainty interval. If it degrades confidence, then the guarded subcell
multifrequency polish is useful mainly for shallow/small-radius ambiguity and
should not be applied blindly.
```

Result:

```text
experiment 153:
  detector rank 1: x=250 mm, z=110 mm
  fine hard-grid polish: x=250 mm, z=110 mm, r=8.0 mm,
    margin=2.36584e-03, weak interval=8.0-8.0 mm
  guarded subcell multifrequency polish: x=250 mm, z=110 mm, r=8.0 mm,
    margin=1.14084e-04, weak interval=7.9-8.0 mm
  truth errors all 0.0 mm
```

Decision:

```text
guarded polish generalizes for point accuracy, but it can downgrade apparent
radius confidence by testing a finer 0.1 mm subcell/multifrequency comparison.
Use guarded polish as the final honest uncertainty report, but preserve
fine-stage margin in summaries so a strong hard-grid result is not lost. Next,
add an aggregate/reporting view that displays fine-stage and guarded-stage
confidence side by side before running more broad sweeps.
```

Reporting follow-through:

```text
experiment 154 added fine-stage and final-stage margin fields to the aggregate
CSV and generated two_stage_stage_confidence_summary.png. The aggregate shows
run 153 as the only downgrade case so far: fine-stage confidence is strong,
final guarded confidence is weak. This supports using guarded polish as the
conservative final uncertainty report while retaining the fine-stage margin as
diagnostic evidence.
```

Next branch:

```text
investigate why guarded subcell multifrequency polish lowers the r=8 mm margin:
1. compare per-frequency radius curves at 1.0 GHz and 1.5 GHz,
2. compare hard versus subcell geometry on the same r=7.9,8.0,8.1 grid,
3. test whether fitting one amplitude across frequencies versus per-frequency
   amplitudes changes the margin.
Start with reporting-only diagnostics before launching another broad GPU
sweep.
```

Diagnostic result:

```text
experiments 155-158 completed the first two checks:
  subcell 1.0+1.5 GHz: margin=1.14084e-04, weak interval=7.9-8.0 mm
  hard 1.0+1.5 GHz: margin=2.42030e-04, weak interval=7.9-8.0 mm
  subcell 1.5 GHz only: margin=5.09885e-04, weak interval=7.9-8.0 mm
  subcell 1.0 GHz only: margin=1.70963e-05, weak interval=7.9-8.1 mm
```

Conclusion:

```text
all diagnostics keep the correct best radius, so point accuracy is stable.
The weak final interval is a real resolution/confidence limit at 0.1 mm radius
spacing: the low-frequency band is nearly size-insensitive, the high-frequency
band helps but is still not strong by the current margin threshold, and
geometry mode is not the sole cause. Next, test objective weighting/source
amplitude choices on this same small grid before changing the broader
detector-to-FWI pipeline.
```

Amplitude diagnostic:

```text
experiment 159 disabled amplitude fitting on the same r=8 mm local grid.
Result: best radius shifted to 7.9 mm, radius error=0.1 mm, weak interval
7.9-8.1 mm. Experiment 161 aggregated the objective-design variants and
recorded fit_amplitude in the CSV.
```

Decision:

```text
do not remove amplitude fitting to gain margin. Under source-amplitude
mismatch, no-fit amplitude makes geometry absorb source error and biases the
radius. Keep source-profiled amplitude fitting as the physically safer
objective, and report the resulting weak interval as an honest confidence
limit. The next objective-design work should test gentle frequency weighting
with amplitude fitting still enabled, not amplitude freezing.
```

Frequency-weighting diagnostic:

```text
experiment 162 used 1.0 GHz weight=0.25 and 1.5 GHz weight=1.0 with amplitude
fitting enabled. It kept the correct best radius r=8.0 mm and improved the
margin from 1.14084e-04 to 1.72277e-04, but the weak interval stayed
7.9-8.0 mm. Experiment 163 aggregated the weighted, unweighted, single-band,
hard/subcell, and no-amplitude-fit variants with frequency_weights recorded in
the CSV.
```

Decision:

```text
gentle high-frequency weighting is directionally helpful but insufficient to
make r=8 mm a strong 0.1 mm radius claim under noise and source mismatch.
Do not promote weighting as a default yet. Use it as a reporting diagnostic,
and only consider a weighted guarded stage after replication across noise
seeds and the shallow r=4 mm branch.
```

Shallow cross-check:

```text
experiment 164 repeated the 0.25/1.0 frequency weighting on the shallow
r=4 mm guarded grid from seed 13. It kept the correct best radius and improved
the margin from 8.08056e-05 to 1.15528e-04, but the weak interval remained
3.9-4.0 mm. Experiment 165 aggregated the equal-weight and weighted shallow
diagnostics.
```

Decision:

```text
frequency weighting is useful as a diagnostic but should not become the
default guarded objective yet. It gives small margin gains in both r=4 mm and
r=8 mm cases, but no confidence-class change. The next meaningful improvement
probably requires either more informative acquisition bandwidth, a different
uncertainty criterion, or subcell/finer-grid resolution studies rather than
another 0.1 mm local weighting tweak.
```

High-band acquisition diagnostic:

```text
experiments 166-168 tested controlled shallow r=4 mm acquisitions at 2.0 GHz
and 2.5 GHz. Best radius stayed correct at 4.0 mm. Margins increased from
8.08056e-05 for the baseline 1.0+1.5 GHz guarded stage to 7.41854e-04 at
2.0 GHz and 1.85997e-03 at 2.5 GHz. The weak interval remained 3.9-4.0 mm
under the current relative-tolerance rule.
```

Decision:

```text
higher acquisition bandwidth is a genuinely promising path for radius
confidence, unlike mild post-hoc weighting. Treat this as an acquisition
design result: it does not mean the existing lower-band data can produce the
same margin. Next, replicate high-band diagnostics on r=8 mm and at another
noise seed before proposing a bandwidth-ladder pipeline.
```

r=8 mm high-band cross-check:

```text
experiment 169 repeated the 2.5 GHz acquisition-design diagnostic on the
deeper r=8 mm local grid. It kept the correct best radius, margin=3.05578e-03,
and collapsed the weak interval to 8.0-8.0 mm. Experiment 171 compared r=4 and
r=8 guarded baselines against 2.5 GHz high-band acquisitions with corrected
aggregate labels.
```

Decision:

```text
high-band acquisition is the strongest new branch from this marathon. It
improves radius confidence far more than local frequency weighting and does
not require disabling source-amplitude fitting. Next, run one seed-replication
check at 2.5 GHz for r=4 and r=8, then design a progressive bandwidth ladder
that starts with lower frequencies for detection/location and uses high-band
data only for final size confidence.
```

Shallow high-band replication:

```text
experiments 172-174 replicated the r=4 mm 2.5 GHz local diagnostic on seeds
13, 21, and 34. All seeds recovered r=4.0 mm with zero point error and
absolute margins above 1e-3:
  seed 13 margin=1.85997e-03
  seed 21 margin=1.17733e-03
  seed 34 margin=1.38477e-03
The weak interval remained 3.9-4.0 mm for all seeds.
```

Decision:

```text
2.5 GHz acquisition reproducibly improves shallow r=4 mm radius confidence,
but it still should be reported with the lower-side weak interval. This is now
strong enough to justify a progressive-bandwidth pipeline prototype:
low/mid-band data for detection and location, high-band local data for final
radius confidence.
```

r=8 mm high-band replication:

```text
experiments 175-177 replicated the r=8 mm 2.5 GHz local diagnostic on seeds
13, 21, and 34. All seeds recovered r=8.0 mm with zero point error and
collapsed weak interval 8.0-8.0 mm:
  seed 13 margin=3.05578e-03
  seed 21 margin=3.25265e-03
  seed 34 margin=3.14797e-03
```

Decision:

```text
the high-band branch now has robust local evidence on both shallow r=4 mm and
deeper r=8 mm targets. It should become the next pipeline prototype: preserve
lower/mid-band detector-seeded location, then add a clearly labeled high-band
local radius-confidence stage. The prototype must keep acquisition bands
separate in summaries so we do not imply 2.5 GHz information exists in lower
band data.
```

Packaged prototype:

```text
experiments 178-180 implemented and smoked the optional high-band stage in the
detector-seeded runner. Run 178 uses lower-band detection/coarse/fine and a
separate 2.5 GHz highband_polish stage. It recovers x=250 mm, z=70 mm,
r=4.0 mm with final margin=1.85997e-03 and weak interval=3.9-4.0 mm.
Run 180 compares packaged guarded run 148 against high-band run 178 and shows
the high-band stage upgrades final confidence while keeping zero point error.
```

Decision:

```text
the progressive-bandwidth prototype is viable. Next steps should be:
1. run the packaged high-band stage on r=4 seeds 21 and 34,
2. run the packaged high-band stage on the r=8 branch,
3. add summary text that explicitly labels lower-band versus high-band
   acquisition data in any paper/presentation figures.
```

Packaged shallow replication:

```text
experiments 181-183 replicated the packaged high-band r=4 mm branch on seeds
13, 21, and 34. All three runs have final_stage=highband_polish, exact point
location/radius, and strong final margins:
  seed 13 margin=1.85997e-03
  seed 21 margin=1.17733e-03
  seed 34 margin=1.38477e-03
All three still report weak interval 3.9-4.0 mm.
```

Decision:

```text
packaged high-band polishing is the current best shallow single-rebar pipeline:
it preserves lower-band detector-seeded location and upgrades radius
confidence reproducibly. It should be tested on the r=8 packaged branch next.
Do not remove interval reporting for r=4 mm; the high-band stage improves
confidence but does not eliminate the lower-side interval under the current
tolerance rule.
```

Packaged r=8 mm seed replication:

```text
experiments 184-188 tested and replicated the packaged high-band stage on the
r=8 mm branch. Runs 184, 186, and 187 recovered x=250 mm, z=110 mm, r=8.0 mm
on noise seeds 13, 21, and 34. Final highband_polish margins were:
  seed 13: 3.05578e-03
  seed 21: 3.25265e-03
  seed 34: 3.14797e-03
All three high-band runs have weak interval=8.0-8.0 mm. Aggregate 188 shows
the only weak-confidence row is guarded run 153, which kept weak interval
7.9-8.0 mm.
```

Decision:

```text
the best current single-rebar pipeline is now:
1. lower-band detector seed,
2. lower-band coarse/fine FWI for location and rough size,
3. optional high-band local polish for final radius confidence.
For r=4 mm this upgrades margin but keeps a lower-side weak interval; for
r=8 mm it collapses the interval reproducibly across three noise seeds. Next,
do not spend more GPU time proving r=8 seed robustness unless a new stressor
is added. The next focused branch is shallow small-radius confidence: subcell
sample convergence, finer radius spacing below 0.1 mm, and source/material
coupling checks around the high-band local window.
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

## Next Stage

Continue Days 11-14 with shallow-radius confidence hardening:

```text
first close the shallow r=4 mm high-band ambiguity:
1. [x] run subcell-sample convergence in the existing high-band local window,
2. [x] test radius spacing finer than 0.1 mm after convergence is stable,
3. [x] compare amplitude-fitted and non-amplitude-fitted profiles to check
   whether source scaling is absorbing radius information,
4. [x] test whether small material/source-property changes explain the same
   shallow-radius objective valley,
5. [ ] add material/source animation examples only when they correspond to actual
   candidate branches,
6. [ ] keep a handoff matrix separating location accuracy, radius confidence,
   source mismatch, material ambiguity, visualization evidence, and runtime.
```

This keeps the next optimizer work grounded in reproducible confidence behavior
rather than promoting a single best candidate from one noise seed.

Shallow r=4 mm ambiguity update:

```text
experiments 189-193 closed the first three shallow-radius tasks. Hard-grid
geometry cannot represent several 0.05 mm radius steps at 1 mm grid, but
subcell-13 geometry changes smoothly. With subcell-13 high-band modeling,
the coarse 0.1 mm curve still has exact best r=4.0 mm, while the fine
0.025 mm curve reveals a weak interval of 3.925-4.100 mm. Removing amplitude
fitting shifts the best radius to 4.025 mm and keeps the same weak interval.
Therefore the current best statement for shallow r=4 mm is:
  point estimate: 4.0 mm when amplitude uncertainty is profiled,
  honest interval: about 3.925-4.100 mm under the current tolerance,
  source/amplitude handling: must be reported, not silently fixed.
```

Material/source ambiguity update:

```text
experiment 194 added explicit shallow r=4 mm material/source profiling. The
best material-profiled candidate shifted to r=4.05 mm with concrete epsr=6.0
and effective rebar log10 sigma=6.0. The true-material r=4.0, log10 sigma=7.0
candidate was nearly tied, only 2.04e-05 above the best objective, and the
best-radius margin was 1.27841e-05. The weak interval over the tested radii
was 3.95-4.10 mm.
```

Decision:

```text
do not add free material parameters directly to the production point-estimate
optimizer yet. Use material profiling as an uncertainty diagnostic. For shallow
r=4 mm, report the nominal point estimate and a material/source-aware interval.
Next, run the same bounded material/source profiling on the replicated r=8 mm
case. If r=8 stays stable, prioritize radius-interval reporting only for
shallow/small-radius cases; if r=8 shifts too, make material-calibrated
intervals a default reporting product.
```

r=8 material/source control:

```text
experiment 195 repeated the bounded material/source profile at x=250 mm,
z=110 mm, r=8.0 mm. The point minimum stayed at r=8.0 mm with concrete
epsr=6.0 and effective rebar log10 sigma=7.0. The nearest material-profiled
competitor was r=8.05 mm with log10 sigma=6.0, only 1.14060e-06 worse. The
weak interval over tested radii was 8.0-8.05 mm.
```

Decision:

```text
material/source uncertainty is not only a shallow r=4 issue, but its effect is
different by size/depth. For r=4 it can shift the point from 4.0 to 4.05 mm
inside a 3.95-4.10 mm interval. For r=8 it preserves the 8.0 mm point but
widens the material/source-aware interval to 8.0-8.05 mm. The production
reporting path should therefore provide:
  nominal high-band point estimate,
  nominal radius confidence interval,
  optional material/source-aware radius interval,
  nuisance parameters that achieved the material/source-profiled best.
```

Reporting product update:

```text
experiments 196-197 added a reusable radius uncertainty report. Run 196 filled
the missing nominal r=8 fine-radius curve at 8.05 mm spacing. Run 197 combined
nominal and material/source-aware summaries for shallow_r4 and deeper_r8.
```

Decision:

```text
make radius uncertainty reporting a first-class post-processing product:
  shallow_r4: nominal 4.0 mm, nominal interval 3.925-4.100 mm,
              material/source-aware point 4.05 mm, interval 3.950-4.100 mm
  deeper_r8:  nominal 8.0 mm, nominal interval 8.000-8.000 mm,
              material/source-aware point 8.0 mm, interval 8.000-8.050 mm

The next packaged pipeline change should add this as an optional reporting
stage after high-band polish. It should not silently change the optimizer's
point estimate; it should expose nuisance-aware uncertainty.
```

Packaged uncertainty report update:

```text
experiment 198 verified the optional packaged material/source uncertainty
branch. The detector-seeded high-band estimate stayed x=250 mm, z=70 mm,
r=4.0 mm. The material/source report, using a bounded smoke grid, reported
a separate material-aware point r=4.05 mm and interval 3.95-4.05 mm.
```

Decision:

```text
keep material/source profiling as a reporting/calibration stage, not as a
replacement for high-band point estimation. The packaged runner can now emit
both:
  final geometry point estimate from high-band polish,
  optional nuisance-aware radius report with separate paths and figure notes.
Next, improve aggregate reporting across packaged cases and keep runtime
explicit so the user can choose when the material uncertainty stage is worth
the extra GPU cost.
```

Aggregate reporting update:

```text
experiment 199 updated the packaged aggregate to include optional
material/source-aware uncertainty columns and a dedicated material uncertainty
plot. Runs without the optional stage remain valid and show NaN material
fields; runs with the optional stage expose material best radius, interval,
point shift, concrete epsr, and rebar log10 sigma.
```

Decision:

```text
short-term single-rebar stack is now:
  detector seed,
  coarse/fine nominal FWI,
  optional high-band final radius confidence,
  optional bounded material/source uncertainty report,
  aggregate plots that keep nominal and nuisance-aware results separate.

Before returning to broader multi-rebar research, run one packaged r=8
material-uncertainty smoke to confirm the optional branch behaves consistently
for the deeper/larger case inside the packaged flow.
```

Packaged r=8 uncertainty smoke update:

```text
experiments 200-201 completed the packaged r=8 material/source uncertainty
validation. Run 200 recovered x=250 mm, z=110 mm, r=8.0 mm with final
high-band margin=3.05578e-03 and nominal weak interval=8.0-8.0 mm. Its
optional material/source report kept the point at r=8.0 mm and added interval
8.0-8.05 mm. Aggregate 201 compares r4 and r8 packaged runs with and without
the optional material report.
```

Decision:

```text
single-rebar packaged reporting is ready for broader use:
  nominal detector/high-band point estimates remain exact on the tested cases,
  material/source-aware intervals expose nuisance uncertainty separately,
  aggregate reports now show the optional material interval and point shift.

Return to multi-rebar research next and apply the same reporting discipline:
do not only show best radii; show ambiguity intervals, material/source caveats
where feasible, and runtime/plot validation.
```

Multi-rebar objective diagnostic reporting update:

```text
experiment 202 added a reporting-only coordinate objective diagnostic report.
On guarded seed55 diagnostic run 106, highband improved the base margin ratio
in every row with mean ratio=1.693, while early_reflection had mean ratio
1.005 and one very poor ratio. Highband still strengthened the wrong target-0
main-pass high-radius branch, so it remains a diagnostic, not an update rule.
```

Decision:

```text
recommended multi-rebar coordinate objective policy:
  update rule: base objective,
  guard: revisit weak high-radius branches,
  diagnostic: highband only,
  not recommended by default: early_reflection.
```

Seed34 replication update:

```text
experiments 203-205 replicated the same-depth three-rebar policy on seed34
with the recommended diagnostic set only. Run 203 ended at the exact final
state x=[150,250,350], z=[90,90,90], r=[6,6,6]. It again started with a weak
target-0 high-radius branch, then corrected that branch during the guarded
revisit after neighboring bars were updated.

The combined seed55+seed34 diagnostic report gives highband 16 rows:
  truth rows=12,
  base truth rows=11,
  geometry changes=1,
  mean margin ratio to base=1.584.

Highband still strengthens the wrong target-0 main-pass branch, so it should
not become the coordinate update objective. It also corrected one seed34
source-mismatch target-2 diagnostic row from r=6.2 to r=6.0, so it remains
valuable as a diagnostic/confidence objective.
```

Decision:

```text
same-depth multi-rebar coordinate FWI is now ready for the next generalization
test. Move to close-spacing three-rebar detector-seeded FWI before variable
depth, because close spacing stresses rebar interaction while keeping the
z-search window controlled. Continue to report weak/ambiguous radius rows
instead of only point estimates.
```

Close-spacing update:

```text
experiment 206 tested detector-seeded close-spacing three-rebar FWI with
60 mm spacing and source-mismatch/noise as the update case. The x coordinates
were exact, but the final z/r state was biased:
  x=[190,250,310],
  z=[90,89,91],
  r=[6.0,5.8,6.6].

The true candidates were close in objective value, so this is a shallow-
objective ambiguity problem rather than a detector miss. The original guarded
revisit was too narrow because it only caught weak high-radius endpoint rows.
It missed moderate broad intervals and low-radius branches.
```

Decision:

```text
promote broad ambiguity revisits to the next experimental method:
  old guard: weak high-radius endpoint revisit,
  new opt-in guard: latest update-case row has broad radius interval even when
  labelled moderate.

Run the same close-spacing case with both guards before changing target order
or widening all search windows. If the broad revisit fixes 206, this becomes
the close-spacing default. If not, run target-order sensitivity next.
```

Corrected close-spacing update:

```text
experiment 208 reran the close-spacing detector-seeded case with broad radius
ambiguity revisits enabled. The main pass reproduced 206, then the revisits
corrected the model to the exact final state:
  x=[190,250,310],
  z=[90,90,90],
  r=[6.0,6.0,6.0].

Target 1 became strong after revisit. Target 2 corrected to the true point but
remained moderate with a 6.0-6.8 mm ambiguity interval. This means the point
pipeline works for this close-spacing case, while the reporting still needs to
carry radius uncertainty honestly.
```

Decision:

```text
make broad radius ambiguity revisits the default policy for close-spacing and
harder multi-rebar cases. Keep highband out of the update rule: in close
spacing it did not improve margins on average and sometimes moved a diagnostic
row away from truth. The next generalization should be variable-depth
multi-rebar detector-seeded FWI with broad ambiguity revisits enabled from the
start.
```

Variable-depth update:

```text
experiment 210 tested variable-depth three-rebar FWI using truth-matched
detector candidates from experiment 115:
  initial x=[148,252,352], z=[85,105,120], r=[6.4,5.6,6.4],
  truth   x=[150,250,350], z=[80,100,120], r=[6,6,6].

The main pass recovered target 1 exactly and target 2 exactly, but target 0
first chose a source-mismatch high-radius branch at z=81, r=6.8. Broad
ambiguity revisit corrected it to z=80, r=6.0, producing the exact final
state across all three rebars.
```

Decision:

```text
the current multi-rebar coordinate policy is now validated on three important
2D synthetic classes:
  same-depth 100 mm spacing,
  close-spacing 60 mm spacing,
  variable-depth detector-seeded cases.

The next bottleneck is detector-to-FWI assignment, not local coordinate FWI
itself. Experiment 115 contains a false shallow duplicate near x=252,z=65.
Next, build and test an assignment policy that chooses the physical three-bar
seed set from the detector candidate list before running coordinate FWI.
```

Detector assignment update:

```text
experiment 212 added and tested a detector-to-FWI assignment policy. It chooses
the highest-scoring set of N detector candidates that satisfies a configurable
minimum x-separation. On experiment 115, the policy selected ranks 1, 2, and 4:
  (148,85), (252,105), (352,120) mm.

It rejected the rank-3 shallow duplicate at (252,65) mm because it shares the
same x with the stronger rank-2 candidate. Those assigned seeds are exactly the
seeds used in experiment 210, so the variable-depth detector-to-FWI chain is:
  detector -> assignment -> broad-ambiguity coordinate FWI -> exact final model.
```

Decision:

```text
next, run assignment reports for the remaining multi-rebar detector scenarios,
starting with close spacing experiment 114. If the assigned seeds match the
already validated FWI runs, avoid duplicate GPU reruns and document the chain.
If an assignment differs, run coordinate FWI for that assigned seed set.
```

Close-spacing assignment update:

```text
experiment 213 applied the assignment report to close-spacing detector
experiment 114. It selected detector ranks 3, 1, and 2, sorted left-to-right:
  (188,90), (248,90), (312,90) mm.

Those are the seeds used in experiments 206 and 208. Therefore the validated
close-spacing detector-to-FWI chain is:
  114 detector -> 213 assignment -> 208 broad-ambiguity coordinate FWI.
```

Decision:

```text
the next engineering step is packaging. Manual transfer of assigned x/z seeds
into run_multi_rebar_coordinate_optimizer.py is now the weak link. Build a
small wrapper that reads a detection_candidates.csv file, assigns seeds, and
launches or at least emits the coordinate-FWI command with broad ambiguity
revisits enabled.
```

Packaging update:

```text
experiments 214 and 215 added run_assigned_coordinate_command_report.py and
used it on the two validated hard detector cases:
  variable depth: 115 detector -> 212 assignment -> 214 command -> 210 FWI,
  close spacing: 114 detector -> 213 assignment -> 215 command -> 208 FWI.

The command reports save assigned candidates and shell-safe coordinate-FWI
commands with broad radius-ambiguity revisits enabled. Negative range values
are emitted as equals-form arguments, such as --z-offsets-mm=-5:1:1, so the
saved command is directly runnable from a shell.
```

Decision:

```text
the next stage should turn the command emitter into an optional launcher with
dry-run as the default and run as an explicit opt-in. That makes the detector
-> assignment -> GPU coordinate-FWI chain executable as one reproducible
pipeline while keeping manual inspection available before expensive runs.
After the launcher is tested, use it for the next new synthetic generalization
case instead of assembling optimizer commands manually.
```

Variable-radius branch update:

```text
experiments 216-218 opened the next generalization class: close-spacing
multi-rebar data with unequal radii 5,6,8 mm. The detector still found all
three physical bars within tolerance, but the smallest bar seed was biased
10 mm too deep. The assignment step selected ranks 3,2,1 left-to-right, and
the wrapper emitted/launched a coordinate-FWI command with per-target truth
radii and a wider z/radius search window.
```

Finding from experiment 219:

```text
experiment 219 completed as a controlled failure. Left-to-right target order
ended at:
  truth: x=[190,250,310], z=[90,90,90], r=[5,6,8],
  final: x=[189,250,310], z=[94,91,90], r=[7.5,7,8].

The right/large 8 mm bar was recovered exactly, but the small and medium bars
were over-estimated under the source-mismatch update case. Broad revisits did
not repair them because the revisit windows were built from local wrong
high-radius ambiguity intervals.
```

Decision:

```text
run the same variable-radius scene with target order 2,1,0, so the strongest
detector candidate/largest bar is updated first. This tests whether the size
over-estimation is mainly an update-order/coupling problem. If order 2,1,0
still fails, the next method should use a radius-prior or joint block update
rather than per-target greedy updates.
```

Order-sensitivity result:

```text
experiment 221 tested target order 2,1,0 and also failed:
  truth: x=[190,250,310], z=[90,90,90], r=[5,6,8],
  final: x=[187,248,311], z=[95,91,90], r=[7.5,7,7.5].

This is worse than 219 for the large bar and still over-estimates the small
and center bars. Target order alone is not the fix.
```

Decision:

```text
run a joint radius-tuple diagnostic at fixed x/z. First use true x/z as an
oracle diagnostic to ask whether the source-profiled objective can identify
the correct radius tuple [5,6,8] when coordinate coupling is removed. If it
can, build a block radius update around assigned x/z. If it cannot, the next
method must change the objective or add a radius prior/regularizer before
more greedy FWI runs.
```

Joint-radius oracle result:

```text
experiment 222 held x/z fixed to truth and searched all radius tuples with
each radius in 5:8:0.5 mm. The true tuple [5,6,8] ranked first for both
noise10_seed13 and source_mismatch_noise10_seed13.
```

Decision:

```text
the objective can estimate unequal radii when radii are updated jointly. The
next diagnostic is the same joint radius tuple search at detector-assigned
x/z seeds. This separates radius-block viability from coordinate-seed error.
```

Assigned-x/z joint-radius result:

```text
experiment 223 fixed x/z to detector-assigned seeds:
  x=[188,248,312], z=[100,90,95].

The true radius tuple [5,6,8] was not in the top 20 for either nominal/noisy
or source-mismatch cases. The source-mismatch case preferred inflated tuples
such as [8,7,8].
```

Decision:

```text
coordinate correction must happen before block radius estimation. The next
stage should run a location-only coordinate pass with radii fixed at 6 mm, so
radius cannot compensate for detector depth errors. Then rerun the joint
radius tuple diagnostic at the corrected x/z.
```

Location-first result:

```text
experiment 225 fixed radii at 6 mm and corrected target 0 and target 1
exactly, but target 2 moved to z=85 mm:
  final x=[190,250,310], z=[90,90,85], r=[6,6,6].

experiment 226 then ran joint radii at that x/z state. It still failed:
the truth tuple [5,6,8] was not in the top 20, and the source-mismatch case
preferred small-right-radius tuples such as [5,6.5,5].
```

Decision:

```text
the remaining hard subproblem is target 2 depth/radius coupling. Run a focused
target-2 local x/z/r polish after targets 0 and 1 are corrected. If target 2
can recover z=90,r=8 in that focused context, the staged pipeline should be:
detector assignment -> location-only pass -> focused large/deep target polish
-> joint/block radius confirmation.
```

Launcher logging update:

```text
run_assigned_coordinate_command_report.py now has --coordinate-log-mode file.
Future wrapper-launched GPU runs can write optimizer stdout/stderr directly to
data/coordinate_launcher_stdout.txt and data/coordinate_launcher_stderr.txt
while the process runs, instead of holding all optimizer progress in memory
until the subprocess exits. The launcher also forces PYTHONUNBUFFERED=1 for
future file-log launches so Python progress prints flush promptly.
```

Focused large-bar polish result:

```text
experiment 227 took the location-only seed-13 state
  x=[190,250,310], z=[90,90,85], r=[6,6,6]
and updated only target 2 over a local x/z/r grid. It recovered
  target 2: x=310, z=90, r=8
for both noise10_seed13 and source_mismatch_noise10_seed13, with strong
radius margins. The z/radius landscape report confirmed that the true
z=90,r=8 pair ranked first after reducing over x.
```

Seed replication result:

```text
experiments 230-234 repeated the staged variable-radius pipeline on noise
seed 21. The detector assignment differed from seed 13:
  x=[188,248,312], z=[85,100,95].

The location-only stage again corrected the small/medium x/z coordinates but
represented the large right bar as a small/shallow surrogate:
  after location-only: x=[190,250,310], z=[90,90,85], r=[6,6,6].

The focused target-2 coupled polish again recovered:
  target 2: x=310, z=90, r=8,
with strong margins in both nominal/noisy and source-mismatch/noisy cases.
The seed-21 z/radius landscapes also ranked the true z=90,r=8 pair first.
```

Current staged policy:

```text
the variable-radius evidence now supports a staged policy rather than greedy
all-parameter per-target updates:
  1. detector and assignment choose one physical seed per bar;
  2. run a location-only x/z correction with radii fixed at the nominal value;
  3. run focused coupled x/z/r polishing for bars that fixed-radius correction
     moves into an obvious depth/radius compensation branch;
  4. estimate remaining per-bar radii jointly at the corrected x/z state.

This policy is paper-consistent: it delays higher-resolution or higher-degree
parameter updates until lower-dimensional updates have reduced cycle-skipping
and parameter tradeoff.
```

Decision:

```text
run seed-21 joint radius-tuple estimation at the staged x/z state
x=[190,250,310], z=[90,90,90]. If the true tuple [5,6,8] ranks first, the
next engineering step is to package the staged variable-radius pipeline into a
reproducible runner/report. If it fails, the joint-radius success in seed 13
was not robust and the next method must add source/material nuisance
uncertainty or stronger regularization before packaging.
```

Seed-21 block-radius result:

```text
experiment 235 ran the joint radius-tuple diagnostic at the seed-21 staged
x/z state. The true radius tuple [5,6,8] ranked first for both noise10_seed21
and source_mismatch_noise10_seed21. In the source-mismatch case, the next
competitors were [5.5,6,8], [5,6,7.5], [5,5.5,8], and [5,6.5,8].
```

Decision:

```text
the staged variable-radius pipeline is now supported across seed 13 and seed
21:
  detector assignment -> location-only x/z correction -> focused target-2
  x/z/r polish -> joint radius tuple estimation.

Move from manual execution to packaging/reporting. The next code stage should
create a reproducible staged-pipeline report/runner that records each stage,
required commands, final geometry, radius tuple rank, figure paths, and
plain-language figure notes. After that, replicate the packaged flow on a
third noise seed or a harder geometry variation.
```

Seed-34 staged replication update:

```text
experiments 239-248 extended the variable-radius close-spacing staged policy
to seed 34. Detection and assignment worked. The location-only stage again
corrected targets 0 and 1 while leaving the large right bar as a shallow
fixed-radius surrogate. Focused target-2 polishing recovered z=90 mm and
r=8 mm, but the source-mismatch update chose x=309 mm instead of x=310 mm by
only 9.92e-05 objective difference.

Joint radii at the realistic x=[190,250,309] state gave nominal/noisy truth
rank 1, but source-mismatch ranked [5.5,6,8] ahead of true [5,6,8] by only
1.73e-05. The staged summary therefore reports seed34_x309 as a weak
uncertainty case, not a confident failure.

Experiment 247 then held x=[190,250,310], z=[90,90,90] and recovered the true
[5,6,8] tuple for both seed-34 cases, with source-mismatch top-2 margin
4.02e-03. This confirms the remaining issue is lateral x ambiguity at the
right bar, not radius-objective failure.
```

Decision:

```text
the three-seed evidence supports the staged variable-radius policy, with
explicit uncertainty reporting:
  seed13 and seed21: exact x/z/r after joint radius stage;
  seed34: exact depth and large-bar radius, target-2 x interval 309-310 mm,
  and left-radius tuple ambiguity only on the x=309 branch.

The next method work should improve lateral x disambiguation/reporting for the
focused target-2 stage before claiming a single deterministic x coordinate.
```

Lateral ambiguity reporting update:

```text
experiment 249 extended the coordinate-confidence aggregate with explicit
ambiguity-width fields and a coordinate_ambiguity_widths.png plot. The target-2
focused-polish aggregate across seeds 13, 21, and 34 has strong radius margins
in all six rows, but all six rows retain a 1 mm x ambiguity interval. This
turns the seed34 behavior from an apparent isolated mistake into a systematic
reporting requirement: radius/depth confidence can be strong while lateral x
is still an interval.
```

Decision:

```text
promote x-ambiguity intervals into the standard focused-polish reporting. The
next physics/method stage should test whether additional acquisition geometry,
source-position density, or a lateral-focused objective can reduce the
309-310 mm target-2 tie; until then, report x as an interval.
```

Acquisition-density update:

```text
experiment 250 reran the seed34 target-2 focused x/z/r polish with 9 scan
positions instead of the standard 5. Both nominal/noisy and source-mismatch
cases selected x=310 mm, z=90 mm, r=8 mm, and both collapsed the ambiguity
interval from 309-310 mm to 310-310 mm. Experiment 251 aggregated the 5-source
and 9-source rows and confirmed that radius confidence stays strong while the
lateral ambiguity disappears only in the denser acquisition.
```

Decision:

```text
acquisition density is now the leading method lever for the seed34 target-2
lateral tie. Before promoting 9 sources as the default, run a 7-source
dose-response check: if 7 sources also collapses the x interval, prefer it as
the cheaper disambiguation setting; if not, report 5-source intervals and use
9 sources as an optional high-confidence refinement.
```

7-source dose-response update:

```text
experiment 252 reran the same focused seed34 target-2 polish with 7 scan
positions at 50, 114, 178, 250, 314, 378, and 450 mm. Both cases recovered
x=310 mm, z=90 mm, r=8 mm with ambiguity interval 310-310 mm. The
source-mismatch x=309-minus-x=310 objective gap changed from -9.92e-05 at
5 sources to +1.74e-03 at 7 sources, so the intermediate acquisition already
breaks the lateral tie.

experiment 253 aggregated the 5/7/9-source rows with source-count-aware
reporting: 5 sources had two x-ambiguity rows and one wrong point x; 7 and
9 sources had zero x-ambiguity rows and both rows at the true geometry.
```

Decision:

```text
for this controlled variable-radius close-spacing seed34 case, prefer
7-source focused polishing as the cheaper lateral-disambiguation refinement.
Keep x-ambiguity interval reporting for standard 5-source runs, and use
9 sources as a confirmation setting rather than the default. The next
robustness question is whether the 7-source rule generalizes across the
other variable-radius seeds or nearby geometries without unnecessary cost.
```

Cross-seed 7-source update:

```text
experiments 254 and 255 repeated the 7-source focused target-2 polish for
seeds 13 and 21. Both seeds recovered x=310 mm, z=90 mm, r=8 mm in both
nominal/noisy and source-mismatch/noisy rows, and both collapsed the x
ambiguity interval to 310-310 mm. Experiment 256 aggregated the 5-source and
7-source focused-polish rows across seeds 13, 21, and 34: 5 sources had
six x-ambiguity rows and one wrong point x; 7 sources had zero x-ambiguity
rows and all six rows at the true point geometry.
```

Decision:

```text
the target-2 variable-radius staged policy now has a validated acquisition
density refinement: keep 5-source focused polishing as the economical default
when interval reporting is acceptable, but use 7-source focused polishing when
a single lateral coordinate is required. The next engineering step is to make
this a packaged option in the staged variable-radius runner/report instead of
manual one-off reruns.
```

Packaged staged-report update:

```text
experiment 257 extended the staged variable-radius summary/report path with an
optional focused_refinement_json per case. The report now records standard
focused x-ambiguity rows, refined focused x-ambiguity rows, refined stage
errors, and a focused_policy field. The seed13/21/34 packaged report marks all
three cases as use_refined_focus_for_point_x: standard 5-source focused
polishing has two x-ambiguity rows per seed, while the 7-source focused
refinement has zero x-ambiguity rows per seed.
```

Decision:

```text
the staged close-spacing variable-radius policy is ready to be treated as a
reproducible report product: detector assignment, location-only correction,
5-source focused polishing with interval reporting, optional 7-source focused
refinement for point x, and joint radius estimation. The next useful work is
either broader geometry robustness or converting this report packaging into a
single orchestration command.
```

Nearer-spacing robustness update:

```text
experiments 258-260 started the broader-geometry check by moving the large
right bar from x=310 mm to x=300 mm, reducing the center-right spacing from
60 mm to 50 mm. With 5 sources, the nominal/noisy row selected x=299 mm while
the true x=300 mm remained inside the 299-300 mm ambiguity interval. With
7 sources, the nominal/noisy point estimate moved to the true x=300 mm, but
x=299 mm still remained inside the ambiguity interval. Source-mismatch was
point-correct at both source counts.
```

Decision:

```text
7-source focused polishing generalizes as a point-correction refinement, but
not as a full interval-collapse rule at 50 mm spacing. Test 9 sources on the
same close-50 geometry before extending the 7-source recommendation beyond
the original 60 mm spacing; if 9 sources collapses the interval, report the
spacing-dependent policy explicitly.
```

Close-50 9-source update:

```text
experiment 261 tested 9 sources on the same x=[190,250,300] mm close-spacing
geometry. The nominal/noisy and source-mismatch/noisy rows both selected the
true x=300 mm, z=90 mm, r=8 mm. However, the nominal/noisy row still retained
a 299-300 mm x ambiguity interval. Experiment 262 aggregated the close-50
5/7/9-source rows: all source counts kept strong radius confidence, 7 and
9 sources fixed the selected point x, but every source count still had one
x-ambiguity row.
```

Decision:

```text
the acquisition-density policy is spacing-dependent. At 60 mm center-right
spacing, 7 sources remove target-2 x ambiguity across seeds. At 50 mm spacing,
even 9 sources do not collapse the nominal/noisy x interval under the current
objective and threshold. Report close-50 target-2 x as an interval unless a new
disambiguation lever is tested, such as a stricter ambiguity threshold
calibrated to noise, different Tx/Rx geometry, or multi-target joint x/r
evaluation.
```

Threshold sensitivity update:

```text
experiment 263 computed the nearest-left lateral gap relative to the true
x misfit for close60 and close50 dose-response rows. With the default 1.5%
ambiguity threshold, close60 moves from below threshold at 5 sources to above
threshold at 7 and 9 sources. Close50 nominal/noisy remains below threshold
at 5, 7, and 9 sources: -0.35%, 1.28%, and 1.12%, respectively.
```

Decision:

```text
do not solve close50 by silently tightening the threshold. The current 1.5%
interval is acting as intended: it exposes a lateral evidence gap that remains
near the noise/objective floor. Future close50 work should target the physics
or objective, not just reporting: try a different Tx/Rx offset geometry,
multi-target joint x/r evaluation, or an explicit noise-calibrated likelihood
before claiming deterministic x at 50 mm spacing.
```

Objective-diagnostic reporting update:

```text
experiment 264 added and smoke-tested coordinate_objective_top_candidates.csv
for the coordinate optimizer. Runs that use --diagnostic-objective-variants now
write ranked top candidates per objective, case, pass, target, and step kind,
with full x/z/r geometry and source-profile metadata. This closes the reporting
gap exposed by the close50 high-band diagnostic summaries: future objective
tests can inspect the near-best lateral competitors directly instead of only
the best row per objective.
```

Decision:

```text
use the new top-candidate objective CSV before drawing close50 conclusions
from high-band or other objective variants. The next objective experiment
should rerun a focused close50 target-2 diagnostic with enough top candidates
to compare x=299 and x=300 under base and high-band objectives.
```

Close-50 objective top-candidate update:

```text
experiment 265 reran the close50 sources=5 target-2 polish with ranked
objective top candidates. The new CSV confirms that high-band weighting flips
the nominal/noisy point estimate from the base objective's x=299 mm to the true
x=300 mm. However, the high-band x=299 competitor is still only 1.466% above
the x=300 misfit, just below the current 1.5% ambiguity threshold. The
source-mismatch/noisy row is clearly separated under high-band, with the x=299
competitor 12.58% above x=300.
```

Decision:

```text
do not promote high-band weighting alone as a deterministic close50 solution.
It improves the point estimate, but the nominal/noisy separation is still at
the ambiguity threshold. The next close50 lever should change measurement
geometry or the joint inversion structure, not only the post-processing
threshold.
```

Tx/Rx geometry update:

```text
experiment 266 added and smoke-tested a --tx-rx-offset-mm option for the
coordinate optimizer. The summary now records the Tx/Rx offset and scan x
positions. This makes Tx/Rx separation a controlled experiment variable for
the close50 ambiguity problem while keeping the same candidate grid,
replication cases, source-profile fitting, and objective-variant reporting.
```

Decision:

```text
run the next close50 target-2 diagnostic with a wider 40 mm Tx/Rx offset and
the same sources=5 setup used in experiment 265. Compare base and high-band
x=299/x=300 top-candidate gaps against the default 20 mm offset before
deciding whether offset geometry is a useful disambiguation lever.
```

Close-50 Tx/Rx offset result:

```text
experiment 267 changed only the Tx/Rx separation from 20 mm to 40 mm for the
close50 sources=5 target-2 diagnostic. Both nominal/noisy and
source-mismatch/noisy rows selected x=300 mm, z=90 mm, r=8 mm with x ambiguity
interval 300-300 mm. In the nominal/noisy base objective, the x=299 competitor
moved from 0.349% better than x=300 at the 20 mm offset to 4.06% worse than
x=300 at the 40 mm offset. The nominal/noisy high-band gap also improved from
1.466% to 17.57%.
```

Decision:

```text
Tx/Rx geometry is now the leading close50 disambiguation lever. The immediate
next step is a compact comparison report for experiments 265 and 267, followed
by replication across seeds or source counts before changing the staged
pipeline recommendation.
```

Tx/Rx comparison report update:

```text
experiment 268 summarized the default 20 mm and widened 40 mm Tx/Rx offset
runs. The nominal/noisy base objective moved from x299 being 0.349% better
than x300 at 20 mm to x299 being 4.06% worse than x300 at 40 mm, crossing the
1.5% ambiguity threshold by a clear margin. The high-band nominal/noisy gap
also improved from 1.466% to 17.57%.
```

Decision:

```text
replicate the 40 mm Tx/Rx offset on additional close50 noise seeds before
changing the staged workflow. Use the same sources=5 grid and top-candidate
objective reporting so the replication tests isolate seed robustness.
```

Seed13 Tx/Rx replication update:

```text
experiment 269 repeated the close50 sources=5, 40 mm Tx/Rx offset diagnostic
with seed13. Both nominal/noisy and source-mismatch/noisy rows recovered
x=300 mm, z=90 mm, r=8 mm with x interval 300-300 mm. The nominal/noisy base
x299-minus-x300 gap was 5.26%, and the high-band gap was 22.81%.
```

Decision:

```text
the 40 mm Tx/Rx offset result has now replicated on seeds 34 and 13. Run seed21
with the same setup to complete the three-seed check before making a staged
workflow recommendation.
```

Three-seed Tx/Rx replication update:

```text
experiment 270 completed the seed21 close50 40 mm Tx/Rx replication. Like
seeds 34 and 13, both observed cases recovered x=300 mm, z=90 mm, r=8 mm with
x interval 300-300 mm. Experiment 271 summarized all three seeds: every one of
the six confidence rows is strong and interval-collapsed, and every x=299
competitor is above the 1.5% ambiguity threshold. The weakest relative gap is
3.44% for source-mismatch/noisy base on seed21; nominal/noisy base gaps span
4.06%-5.26%.
```

Decision:

```text
promote 40 mm Tx/Rx offset to the leading close50 target-2 disambiguation
setting for synthetic staged runs, with the caveat that the observation
geometry changed and should be represented explicitly in reports. The next
engineering task is to make staged summaries carry acquisition geometry
metadata so 20 mm and 40 mm workflows are not mixed silently.
```

Staged acquisition-metadata update:

```text
experiment 272 smoke-tested staged summary acquisition metadata. The staged
case CSV now records sources, Tx/Rx offset when present, and frequency for
location, focused, refined-focused, and joint stages. Figure notes also list
focused/refined-focused acquisition settings per case. Older inputs that do
not have tx_rx_offset_mm remain blank, making missing geometry metadata visible
instead of silently assuming the default.
```

Decision:

```text
future staged close50 reports should include the 40 mm focused-polish run as an
explicit acquisition setting, not merely as another focused refinement. When
old 20 mm summaries are reused, leave their missing Tx/Rx field visible or
rerun them with the newer metadata-bearing optimizer.
```

Acquisition-aware aggregate update:

```text
experiment 273 updated and smoke-tested coordinate confidence aggregation so it
reports acquisition groups keyed by source count plus Tx/Rx offset. In the
close50 sources=5 comparison, the source-only summary has 8 rows with one
x-ambiguity row, but the acquisition summary separates this into a 40 mm Tx/Rx
group with 6/6 truth rows and zero x ambiguity, and a not-recorded/default
group with 1/2 truth rows and one x ambiguity row.
```

Decision:

```text
use acquisition-aware summaries for any future close50 policy statement.
Avoid comparing source count without Tx/Rx offset because it masks the
dominant disambiguation lever identified in experiments 267-271.
```

40 mm Tx/Rx source-count reduction update:

```text
experiment 274 tested whether the close50 40 mm Tx/Rx acquisition could drop
from 5 to 3 scan positions. It was faster but failed: both main rows and both
revisit rows selected x=299 mm, r=7.5 mm with weak radius confidence and
nonzero x/radius ambiguity. Experiment 275 aggregated sources=3 and sources=5
at 40 mm Tx/Rx for seed34: 3 sources had 0/4 truth rows and 4 x-ambiguity
rows, while 5 sources had 2/2 truth rows and zero x ambiguity.
```

Decision:

```text
keep 5 sources as the minimum validated close50 40 mm Tx/Rx setting. The
40 mm offset is the key geometry lever, but the scan aperture still needs at
least the five-position sampling used in experiments 267, 269, and 270.
```

Four-source boundary update:

```text
experiment 276 tested 4 sources at 40 mm Tx/Rx for close50 seed34. Unlike the
3-source run, it recovered x=300 mm, z=90 mm, r=8 mm for both observed cases
with strong confidence and x interval 300-300 mm. It finished in 1309 s,
faster than the 5-source seed34 run at 1685 s. Experiment 277 aggregated
sources 3/4/5: 3 sources had 0/4 truth rows and 4 x-ambiguity rows, while
4 and 5 sources both had 2/2 truth rows and zero x ambiguity.
```

Decision:

```text
the seed34 source-count threshold at 40 mm Tx/Rx is between 3 and 4 sources.
Do not replace the cross-seed 5-source recommendation yet; first replicate
4 sources on seeds 13 and 21 using the same acquisition geometry and reporting.
```

Four-source seed-replication update:

```text
experiment 278 replicated the 4-source 40 mm Tx/Rx close50 diagnostic on
seed13. Both observed cases recovered x=300 mm, z=90 mm, r=8 mm with strong
confidence and x interval 300-300 mm. The weakest x299-minus-x300 gap was
4.30%, above the 1.5% ambiguity threshold.
```

Decision:

```text
experiment 279 completed the seed21 replication. Both observed cases recovered
x=300 mm, z=90 mm, r=8 mm with strong confidence and x interval 300-300 mm.
The weakest x299-minus-x300 gap was 3.99%, above the 1.5% ambiguity threshold.
Experiment 280 aggregated seeds 34, 13, and 21: 6/6 rows were truth geometry,
all were strong, and no row had x ambiguity. Treat 4 sources with 40 mm Tx/Rx
as the current minimum validated close50 40 mm Tx/Rx acquisition. Keep the
failed 3-source result as the lower-bound warning and keep 5 sources as the
conservative backup.
```

Intermediate Tx/Rx offset update:

```text
experiment 281 tested the 4-source close50 seed34 acquisition with Tx/Rx
offset reduced from 40 mm to 30 mm. It recovered x=300 mm, z=90 mm, r=8 mm
for both nominal and source-mismatch observations with strong confidence and
x interval 300-300 mm. The nearest base lateral competitor shifted to x=301 mm
and sat only 1.96-2.05% above the truth, tighter than the replicated 40 mm
setting but still above the 1.5% ambiguity threshold.
```

Decision:

```text
experiment 282 replicated 30 mm Tx/Rx on seed13 as another truth-geometry
pass, but the nominal base x301-minus-x300 gap was only 1.5888%, barely above
the 1.5% ambiguity threshold. Experiment 283 completed seed21 as another pass
with weakest base gap 1.8585%. Experiment 284 aggregated seeds 34, 13, and 21:
6/6 rows were truth geometry, all were strong, and no row had x ambiguity.
Classify 30 mm as the minimum replicated close50 offset only with
margin-aware reporting. Keep 40 mm as the robust default because its weakest
base lateral gap is much larger and its aggregate radius margin mean is about
three times higher.
```

Next offset-threshold decision:

```text
experiment 285 tested 25 mm Tx/Rx on seed34 and failed the lower-bound probe.
The main and revisit reports stayed weak, kept x=300-301 mm and radius
7.5-8.0 mm ambiguity intervals, and the source-mismatch case selected x=301 mm.
The source-mismatch base gap between x=300 and x=301 was only 0.0941%, far
below the 1.5% ambiguity threshold. The practical recommendation is now
30 mm minimum replicated / 40 mm robust default.
```

Next robust-offset decision:

```text
run one seed34 probe at 35 mm Tx/Rx with the same 4-source scan to see whether
there is a smaller robust default between the borderline 30 mm and robust
40 mm settings. If 35 mm shows 40 mm-like margins, replicate it; otherwise
keep 40 mm as the robust default and move to geometry-separation stress tests.
```
