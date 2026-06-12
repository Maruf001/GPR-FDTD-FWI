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
- [x] Stage 11B: variable-depth/variable-radius seed55 replication and three-seed aggregate.
- [x] Stage 11C: variable-depth/variable-radius 7-source final-interval check.
- [x] Stage 11D: variable-depth/variable-radius 35 mm Tx/Rx final-interval check.
- [x] Stage 11E: variable-depth/variable-radius 50 mm Tx/Rx final-interval check.
- [x] Stage 11F: variable-depth/variable-radius 50 mm Tx/Rx seed replication.
- [x] Stage 11G: variable-depth/variable-radius 50 mm Tx/Rx three-seed summary.
- [x] Stage 11H: variable-depth/variable-radius Tx/Rx 50 mm objective diagnostic.
- [x] Stage 11I: objective-specific confidence rows for coordinate diagnostics.
- [x] Stage 11J: all-target Tx/Rx 50 mm objective guardrail.
- [x] Stage 11K: source-shape transfer check for veryhigh objective.
- [x] Stage 11L: fitted-ringdown seed replication across all variable-depth/radius targets.
- [x] Stage 11M: all-condition Tx/Rx 50 mm objective-confidence report.
- [x] Stage 11N: variable-depth/radius objective-use reporting handoff.
- [x] Stage 11O: close50 acquisition metadata repair.
- [x] Stage 11P: source-shape center interval reporting handoff.
- [x] Stage 11Q: shallow r=4 single-rebar reporting handoff.
- [x] Stage 11R: marathon recovery checkpoint.
- [x] Stage 11S: current evidence synthesis.
- [x] Stage 11T: results-section draft.
- [x] Stage 11U: methods paragraph and evidence table.
- [x] Stage 11V: combined report draft.
- [x] Stage 11W: decision-grade figure map.
- [x] Stage 11X: compact objective summary figure.
- [x] Stage 11Y: decision figure readiness audit.
- [x] Stage 11Z: report figure caption package.
- [x] Stage 11AA: report claim consistency audit.
- [x] Stage 11AB: reporting reproducibility bundle.
- [x] Stage 11AC: final report markdown.
- [x] Stage 11AD: final report editorial lint.
- [x] Stage 11AE: archive status checkpoint.
- [x] Stage 11AF: commit and archive inventory.
- [x] Stage 11AG: objective-note hardening from code self-review.
- [x] Stage 11AH: post-hardening resume checkpoint.
- [x] Stage 11AI: report dependency size audit.
- [x] Stage 11AJ: report dependency archive.
- [x] Stage 11AK: post-archive resume checkpoint.
- [x] Stage 11AL: commit/PR summary draft.
- [x] Stage 11AM: next-action queue and no-GPU guardrails.
- [x] Stage 11AN: final report reproducibility refresh.
- [x] Stage 11AO: revised final report lint.
- [x] Stage 11AP: next-action queue refresh.
- [x] Stage 11AQ: IMRAD manuscript draft.
- [x] Stage 11AR: IMRAD manuscript lint.
- [x] Stage 11AS: post-IMRAD resume checkpoint.
- [x] Stage 11AT: manuscript balance and guardrail audit.
- [x] Stage 11AU: next-action queue manuscript refresh.
- [x] Stage 11AV: manuscript guardrail prose polish.
- [x] Stage 11AW: post-manuscript polish checkpoint.
- [x] Stage 11AX: next-action queue post-polish refresh.
- [x] Stage 11AY: commit/PR summary refresh.
- [x] Stage 11AZ: coordinate aggregate note hardening.
- [x] Stage 11BA: commit/PR summary post-hardening refresh.
- [x] Stage 11BB: post-hardening resume checkpoint.
- [x] Stage 11BC: next-action queue post-hardening refresh.
- [x] Stage 11BD: IMRAD manuscript validation refresh.
- [x] Stage 11BE: next-action queue manuscript validation refresh.
- [x] Stage 11BF: commit/PR summary current refresh.
- [x] Stage 11BG: next-action queue commit summary refresh.
- [x] Stage 11BH: current handoff archive size audit.
- [x] Stage 11BI: current handoff archive.
- [x] Stage 11BJ: next-action queue current archive refresh.
- [x] Stage 11BK: current pre-commit validation checkpoint.
- [x] Stage 11BL: next-action queue pre-commit validation refresh.
- [x] Stage 11BM: objective confidence sparse-result hardening.
- [x] Stage 11BN: next-action queue objective sparse-hardening refresh.
- [x] Stage 11BO: commit/PR summary sparse-hardening refresh.
- [x] Stage 11BP: next-action queue commit-summary sparse-hardening refresh.
- [x] Stage 11BQ: post-sparse-hardening resume checkpoint.
- [x] Stage 11BR: next-action queue post-sparse-hardening resume refresh.
- [x] Stage 11BS: current artifact consistency audit.
- [x] Stage 11BT: IMRAD manuscript current validation refresh.
- [x] Stage 11BU: commit/PR summary current manuscript-validation refresh.
- [x] Stage 11BV: next-action queue current manuscript-validation refresh.
- [x] Stage 11BW: current handoff archive refresh size audit.
- [x] Stage 11BX: current handoff archive refresh.
- [x] Stage 11BY: commit/PR summary current archive refresh.
- [x] Stage 11BZ: next-action queue current archive refresh.
- [x] Stage 11CA: current pre-commit validation after archive refresh.
- [x] Stage 11CB: next-action queue current validation refresh.
- [x] Stage 11CC: commit/PR summary current validation refresh.
- [x] Stage 11CD: next-action queue commit-summary validation refresh.
- [x] Stage 11CE: objective diagnostic sparse-geometry hardening.
- [x] Stage 11CF: commit/PR summary current diagnostic-hardening refresh.
- [x] Stage 11CG: next-action queue diagnostic-hardening refresh.
- [x] Stage 11CH: current diagnostic-hardening state audit.
- [x] Stage 11CI: optional numeric non-finite reporting hardening.
- [x] Stage 11CJ: commit/PR summary current non-finite-hardening refresh.
- [x] Stage 11CK: next-action queue non-finite-hardening refresh.
- [x] Stage 11CL: reporting CLI non-finite smoke.
- [x] Stage 11CM: objective ratio null-serialization hardening.
- [x] Stage 11CN: objective CLI sparse/non-finite smoke.
- [x] Stage 11CO: current non-finite-hardening state audit.
- [x] Stage 11CP: commit/PR summary current smoke-audit refresh.
- [x] Stage 11CQ: next-action queue smoke-audit refresh.
- [x] Stage 11CR: current smoke-audit archive size audit.
- [x] Stage 11CS: current handoff archive smoke-audit refresh.
- [x] Stage 11CT: commit/PR summary current archive smoke-audit refresh.
- [x] Stage 11CU: next-action queue archive smoke-audit refresh.
- [x] Stage 11CV: IMRAD manuscript current archive validation refresh.
- [x] Stage 11CW: commit/PR summary current manuscript-archive refresh.
- [x] Stage 11CX: next-action queue manuscript-archive refresh.
- [x] Stage 11CY: current manuscript archive size audit.
- [x] Stage 11CZ: current handoff archive manuscript refresh.
- [x] Stage 11DA: commit/PR summary current manuscript-archive handoff refresh.
- [x] Stage 11DB: next-action queue manuscript-archive handoff refresh.
- [x] Stage 11DC: post-manuscript-archive resume checkpoint.
- [x] Stage 11DD: commit/PR summary current resume refresh.
- [x] Stage 11DE: next-action queue resume refresh.
- [x] Stage 11DF: current resume state audit.
- [x] Stage 11DG: commit/PR summary current resume-audit refresh.
- [x] Stage 11DH: next-action queue resume-audit refresh.
- [x] Stage 11DI: current resume archive size audit.
- [x] Stage 11DJ: current handoff archive resume refresh.
- [x] Stage 11DK: commit/PR summary current archive-resume refresh.
- [x] Stage 11DL: next-action queue archive-resume refresh.
- [x] Stage 11DM: IMRAD manuscript current resume-archive validation refresh.
- [x] Stage 11DN: commit/PR summary current manuscript resume-archive refresh.
- [x] Stage 11DO: next-action queue manuscript resume-archive refresh.
- [x] Stage 11DP: objective diagnostic manifest-artifact hardening.
- [x] Stage 11DQ: commit/PR summary current manifest-validation refresh.
- [x] Stage 11DR: next-action queue manifest-validation refresh.
- [x] Stage 11DS: objective diagnostic no-confidence manifest smoke.
- [x] Stage 11DT: commit/PR summary current manifest-smoke refresh.
- [x] Stage 11DU: next-action queue manifest-smoke refresh.
- [x] Stage 11DV: current manifest-smoke state audit.
- [x] Stage 11DW: commit/PR summary current manifest-audit refresh.
- [x] Stage 11DX: next-action queue manifest-audit refresh.
- [x] Stage 11DY: post-manifest-audit resume checkpoint.
- [x] Stage 11DZ: commit/PR summary current resume-checkpoint refresh.
- [x] Stage 11EA: next-action queue resume-checkpoint refresh.
- [x] Stage 11EB: current resume-checkpoint state audit.
- [x] Stage 11EC: commit/PR summary current state-audit refresh.
- [x] Stage 11ED: next-action queue state-audit refresh.
- [x] Stage 11EE: current state archive coverage audit.
- [x] Stage 11EF: commit/PR summary current archive-coverage refresh.
- [x] Stage 11EG: next-action queue archive-coverage refresh.
- [x] Stage 11EH: candidate confidence non-finite hardening.
- [x] Stage 11EI: commit/PR summary candidate-confidence refresh.
- [x] Stage 11EJ: next-action queue candidate-confidence refresh.
- [x] Stage 11EK: current candidate-confidence state audit.
- [x] Stage 11EL: commit/PR summary candidate-confidence audit refresh.
- [x] Stage 11EM: next-action queue candidate-confidence audit refresh.
- [x] Stage 11EN: candidate confidence row-sanitization hardening.
- [x] Stage 11EO: commit/PR summary candidate-row-sanitization refresh.
- [x] Stage 11EP: next-action queue candidate-row-sanitization refresh.
- [x] Stage 11EQ: current candidate-row-sanitization state audit.
- [x] Stage 11ER: commit/PR summary candidate-row-sanitization audit refresh.
- [x] Stage 11ES: next-action queue candidate-row-sanitization audit refresh.
- [x] Stage 11ET: objective diagnostic non-finite confidence smoke.
- [x] Stage 11EU: commit/PR summary non-finite confidence smoke refresh.
- [x] Stage 11EV: next-action queue non-finite confidence smoke refresh.
- [x] Stage 11EW: current non-finite confidence smoke state audit.
- [x] Stage 11EX: commit/PR summary non-finite confidence audit refresh.
- [x] Stage 11EY: next-action queue non-finite confidence audit refresh.
- [x] Stage 11EZ: coordinate aggregate row-sanitization hardening.
- [x] Stage 11FA: coordinate aggregate non-finite row smoke.
- [x] Stage 11FB: commit/PR summary coordinate aggregate smoke refresh.
- [x] Stage 11FC: next-action queue coordinate aggregate smoke refresh.
- [x] Stage 11FD: current coordinate aggregate smoke state audit.
- [x] Stage 11FE: commit/PR summary coordinate aggregate audit refresh.
- [x] Stage 11FF: next-action queue coordinate aggregate audit refresh.
- [x] Stage 11FG: current state archive coverage audit refresh.
- [x] Stage 11FH: commit/PR summary current archive-coverage refresh.
- [x] Stage 11FI: next-action queue current archive-coverage refresh.
- [x] Stage 11FJ: IMRAD manuscript current archive-coverage validation refresh.
- [x] Stage 11FK: commit/PR summary current manuscript validation refresh.
- [x] Stage 11FL: next-action queue current manuscript validation refresh.
- [x] Stage 11FM: current manuscript validation state audit.
- [x] Stage 11FN: coordinate confidence metadata-default hardening.
- [x] Stage 11FO: coordinate aggregate invalid-default smoke.
- [x] Stage 11FP: commit/PR summary current metadata-default refresh.
- [x] Stage 11FQ: next-action queue metadata-default refresh.
- [x] Stage 11FR: current metadata-default state audit.
- [x] Stage 11FS: current precommit validation after metadata-default audit.
- [x] Stage 11FT: commit/PR summary current validation after metadata-default audit.
- [x] Stage 11FU: next-action queue current validation after metadata-default audit.
- [x] Stage 11FV: current validation after metadata-default audit state audit.
- [x] Stage 11FW: code self-review current validation checkpoint.
- [x] Stage 11FX: commit/PR summary current review refresh.
- [x] Stage 11FY: next-action queue current review refresh.
- [x] Stage 11FZ: current review refresh state audit.
- [x] Stage 11GA: current state archive coverage audit refresh.
- [x] Stage 11GB: commit/PR summary current archive-coverage refresh.
- [x] Stage 11GC: next-action queue current archive-coverage refresh.
- [x] Stage 11GD: current archive-coverage refresh state audit.
- [x] Stage 11GE: current precommit validation after archive-coverage refresh.
- [x] Stage 11GF: commit/PR summary current validation refresh.
- [x] Stage 11GG: next-action queue current validation refresh.
- [x] Stage 11GH: current validation refresh state audit.
- [x] Stage 11GI: current state archive coverage audit refresh.
- [x] Stage 11GJ: commit/PR summary current archive-coverage refresh.
- [x] Stage 11GK: next-action queue current archive-coverage refresh.
- [x] Stage 11GL: current archive-coverage refresh state audit.
- [x] Stage 11GM: current precommit validation after archive-coverage refresh.
- [x] Stage 11GN: commit/PR summary current validation refresh.
- [x] Stage 11GO: next-action queue current validation refresh.
- [x] Stage 11GP: current validation refresh state audit.
- [x] Stage 11GQ: code self-review current validation refresh.
- [x] Stage 11GR: commit/PR summary current review refresh.
- [x] Stage 11GS: next-action queue current review refresh.
- [x] Stage 11GT: current review refresh state audit.
- [x] Stage 11GU: current state archive coverage audit refresh.
- [x] Stage 11GV: commit/PR summary current archive-coverage refresh.
- [x] Stage 11GW: next-action queue current archive-coverage refresh.
- [x] Stage 11GX: current archive-coverage refresh state audit.
- [x] Stage 11GY: current precommit validation after archive-coverage audit refresh.
- [x] Stage 11GZ: commit/PR summary current validation refresh.
- [x] Stage 11HA: next-action queue current validation refresh.
- [x] Stage 11HB: current validation refresh state audit.
- [x] Stage 11HC: IMRAD manuscript current validation refresh.
- [x] Stage 11HD: commit/PR summary current manuscript validation refresh.
- [x] Stage 11HE: next-action queue current manuscript validation refresh.
- [x] Stage 11HF: current manuscript validation refresh state audit.
- [x] Stage 11HG: current state archive coverage audit refresh.
- [x] Stage 11HH: commit/PR summary current archive coverage refresh.
- [x] Stage 11HI: next-action queue current archive coverage refresh.
- [x] Stage 11HJ: current archive coverage refresh state audit.
- [x] Stage 11HK: post-archive-coverage audit resume checkpoint.
- [x] Stage 11HL: experiment archive health report current.
- [x] Stage 11HM: seed21 target-0 Tx/Rx=50 fitted-ringdown diagnostic.
- [x] Stage 11HN: seed21 target-2 Tx/Rx=50 fitted-ringdown diagnostic.
- [x] Stage 11HO: seed21 target-1 Tx/Rx=50 fitted-ringdown diagnostic.
- [x] Stage 11HP: seed21 fitted-ringdown all-target summary.
- [x] Stage 13LK: seed53316291173 target0 8-source Tx/Rx=60 control.
- [x] Stage 13LL: coordinate optimizer decision-context figure upgrade.
- [x] Stage 13LM: seed53316291173 target2 5-source Tx/Rx=60 control.
- [x] Stage 13LN: seed53316291173 target2 7-source Tx/Rx=60 bracket.
- [x] Stage 13LO: seed53316291173 target2 9-source Tx/Rx=60 escalation.
- [x] Stage 13LP: seed53316291173 target2 11-source Tx/Rx=60 closeout.
- [x] Stage 13LQ: seed53316291173 target1 5-source Tx/Rx=60 control.
- [x] Stage 13LR: seed86267571272 target0 8-source Tx/Rx=60 control.
- [x] Stage 13LS: seed86267571272 target2 5-source Tx/Rx=60 control.
- [x] Stage 13LT: seed86267571272 target2 7-source Tx/Rx=60 bracket.
- [x] Stage 13LU: seed86267571272 target2 9-source Tx/Rx=60 escalation.
- [x] Stage 13LV: seed86267571272 target2 11-source Tx/Rx=60 closeout.
- [x] Stage 13LW: seed86267571272 target1 5-source Tx/Rx=60 control.
- [x] Stage 13LX: seed139583862445 target0 8-source Tx/Rx=60 control.
- [x] Stage 13LY: seed139583862445 target2 5-source Tx/Rx=60 control.
- [x] Stage 13LZ: seed139583862445 target1 5-source Tx/Rx=60 control.
- [x] Stage 13MA: seed139583862445 target1 9-source Tx/Rx=60 rescue.
- [x] Stage 13MB: seed225851433717 target0 8-source Tx/Rx=60 control.
- [x] Stage 13MC: seed225851433717 target2 5-source Tx/Rx=60 control.
- [x] Stage 13MD: seed225851433717 target1 5-source Tx/Rx=60 control.
- [x] Stage 13ME: scene visualization template and GSSI 51600S field-data intake plan.
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
low-conductivity steel candidate, and experiment 420 adds the matching
true-vs-candidate material comparison GIF.
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
5. [x] add material/source animation examples only when they correspond to actual
   candidate branches,
6. [x] keep a handoff matrix separating location accuracy, radius confidence,
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
experiment 286 tested 35 mm Tx/Rx on seed34 and passed as a strong
truth-geometry run. The weakest base lateral gap was 4.71%, comparable to the
40 mm seed34 result and much stronger than the 30 mm seed34 result.
Experiment 287 replicated seed13 with weakest base lateral gap 4.64%.
Experiment 288 replicated seed21 with weakest base lateral gap 4.64%.
Experiment 289 aggregated the three 35 mm seeds: 6/6 rows were truth geometry,
all were strong, no row had x ambiguity, and the radius margin mean was
5.18816e-03. Promote 35 mm to the robust close50 default. Keep 30 mm as the
minimum replicated margin-aware setting, 25 mm as the failed lower bound, and
40 mm as the extra-conservative backup.
```

Next geometry-stress decision:

```text
experiment 290 moved from acquisition-offset thresholding to geometry-
separation stress with close45 target 2: 4 sources, 35 mm Tx/Rx,
x=[190,250,295] mm, z=[90,90,90] mm, radii=[5,6,8] mm. Seed34 passed strongly:
truth geometry, strong labels, x interval 295-295 mm, and weakest base lateral
gap 4.64%. Experiment 291 replicated seed13 with truth geometry, strong
labels, x interval 295-295 mm, and weakest base lateral gap 4.44%.
Experiment 292 completed seed21 with truth geometry, strong labels, and
weakest base lateral gap 4.15%. Experiment 293 aggregated close45: 6/6 rows
were truth geometry, all were strong, and no row had x ambiguity. Treat
close45 as replicated under the 4-source 35 mm robust acquisition.
```

Next geometry-stress decision:

```text
run a close40 seed34 probe with the same robust acquisition: 4 sources,
35 mm Tx/Rx, x=[190,250,290] mm, z=[90,90,90] mm, radii=[5,6,8] mm. If it
passes, replicate seeds 13 and 21; if it fails, compare against the
extra-conservative 40 mm offset before setting the geometry-separation limit.
Experiment 294 completed the close40 seed34 probe as a strong pass: truth
geometry, x interval 290-290 mm, and weakest base lateral gap 6.61%. Replicate
close40 on seeds 13 and 21 before moving the geometry-stress branch tighter.
Experiment 295 replicated seed13 as another strong pass with x interval
290-290 mm and weakest base lateral gap 6.31%. Experiment 296 completed
seed21 as another strong pass with x interval 290-290 mm and weakest base
lateral gap 6.31% nominal / 8.03% under source mismatch. Experiment 297
aggregated close40 across seeds 34, 13, and 21: 6/6 rows were truth geometry,
all were strong, no row had x ambiguity, and the radius margin mean was
7.41450e-03. Treat close40 as replicated under the 4-source 35 mm robust
acquisition. Run a close35 seed34 probe next with x=[190,250,285] mm using
the same acquisition; if it fails, compare against the extra-conservative
40 mm Tx/Rx offset before setting the geometry-separation limit. Experiment
298 completed the close35 seed34 probe as a strong pass: truth geometry,
x interval 285-285 mm, no revisit, and weakest base lateral gap 7.28%.
Experiment 299 replicated seed13 as another strong pass with x interval
285-285 mm and weakest base lateral gap 7.55%. Experiment 300 completed
seed21 as another strong pass with x interval 285-285 mm and weakest base
lateral gap 7.20%. Experiment 301 aggregated close35 across seeds 34, 13,
and 21: 6/6 rows were truth geometry, all were strong, no row had x
ambiguity, and the radius margin mean was 5.74808e-03. Treat close35 as
replicated under the 4-source 35 mm robust acquisition. Run a close30 seed34
probe next with x=[190,250,280] mm using the same acquisition; if it fails,
compare against the extra-conservative 40 mm Tx/Rx offset before setting the
geometry-separation limit. Experiment 302 completed the close30 seed34 probe
as a truth-geometry pass with strong labels and zero x ambiguity, but the
nearest competitor is now a coupled x=281 mm, r=7.5 mm branch only 2.44% worse
under the nominal base objective. Treat close30 as a margin-aware pass and
replicate seeds 13 and 21 before calling it validated. Experiment 303
replicated seed13 as another truth-geometry, strong-label pass with zero x
ambiguity; the same x=281 mm, r=7.5 mm branch was 2.66% worse under nominal
base and 3.54% worse under source mismatch. Experiment 304 completed seed21
as another truth-geometry, strong-label pass with zero x ambiguity; the
coupled x=281 mm, r=7.5 mm branch was 2.18% worse under nominal base and
3.67% worse under source mismatch. Experiment 305 aggregated close30 across
seeds 34, 13, and 21: 6/6 rows were truth geometry, all were strong, no row
had x ambiguity, and the radius margin mean was 2.43348e-03. Treat close30 as
the current tightest replicated 35 mm-offset result with margin-aware
reporting. Run a close25 seed34 lower-bound probe with x=[190,250,275] mm
before claiming close30 as the final geometry-separation limit. Experiment
306 ran that close25 seed34 lower-bound probe and failed as a robust point
estimate: all four main/revisit rows were weak, x/r ambiguity remained
275-276 mm and 7.5-8.0 mm, and the nominal case selected the shifted
x=276 mm, r=7.5 mm branch over truth. Treat close30 as the tightest replicated
35 mm-offset result unless an extra-conservative 40 mm Tx/Rx close25 seed34
probe rescues the geometry. Experiment 307 ran that 40 mm-offset rescue probe
and partially rescued seed34: both cases selected truth and no revisit was
triggered, but the nominal row was only moderate, retained a 275-276 mm /
7.5-8.0 mm near-best interval, and the x276/r7.5 branch was only 1.24% worse
under the base objective. Experiment 308 replicated seed13 as the same
40 mm-offset rescue pattern: both cases selected truth and no revisit was
triggered, but the nominal row stayed moderate with the same 275-276 mm /
7.5-8.0 mm near-best interval and the x276/r7.5 branch only 1.35% worse under
the base objective. Experiment 309 completed seed21 as another truth-selected
40 mm run, but its nominal row was weak and the x276/r7.5 branch was only
0.9647% worse under the base objective. Experiment 310 aggregated seeds 34,
13, and 21: 6/6 rows selected truth geometry, but confidence was mixed
(strong=3, moderate=2, weak=1), three rows retained 1 mm x ambiguity, and the
radius-margin mean was only 1.13331e-03. Treat close25 with 40 mm Tx/Rx as a
margin-aware lower-bound recovery mode, not as the clean geometry-separation
limit. Keep close30 under the 35 mm robust acquisition as the tightest
replicated zero-ambiguity result, and run a close28 35 mm Tx/Rx bracket probe
to locate the transition between close30 pass and close25 fail. Experiment
311 ran the close28 seed34 bracket and selected truth in both observed cases
without a revisit, but the nominal row was weak, kept a 278-279 mm /
7.5-8.0 mm ambiguity interval, and the high-band x279/r7.5 branch was only
0.2796% above truth. Treat close28 as a transition-band point recovery that
requires seed replication and aggregate ambiguity reporting, not as a
validated geometry limit yet. Experiment 312 replicated seed13 as another
truth-selected close28 run with no revisit; the nominal row improved to
moderate, but still retained the same 278-279 mm / 7.5-8.0 mm ambiguity
interval and the base x279/r7.5 branch was only 0.8714% above truth. Run
seed21 and aggregate 311-313 before making any close28 policy statement.
Experiment 313 completed seed21 as another truth-selected close28 run, but the
nominal row was weak, kept the same 278-279 mm / 7.5-8.0 mm ambiguity
interval, and the high-band diagnostic ranked the shifted x279/r7.5 branch
above truth by 0.5322%. Experiment 314 aggregated seeds 34, 13, and 21:
6/6 rows selected truth geometry, but confidence was mixed (strong=3,
moderate=1, weak=2), three rows retained 1 mm x ambiguity, and the
radius-margin mean was only 9.92343e-04. Keep close30 as the tightest
replicated clean 35 mm-offset result. Classify close28 as a transition-band
point-recovery mode that requires interval reporting. Experiment 315 tested
whether a 40 mm Tx/Rx offset could clean close28 seed34. It improved the
landscape: truth won both base and high-band diagnostics, and the nominal
high-band gap rose from 0.2796% to 4.8776%. But the nominal base gap was still
only 1.2088%, so the row remained moderate with a 278-279 mm / 7.5-8.0 mm
ambiguity interval. Test a 45 mm Tx/Rx seed34 probe before deciding whether
close28 can be made clean by extra-conservative acquisition. Experiment 316
tested 45 mm Tx/Rx on seed34 and cleaned the close28 result: both rows were
strong, no x/radius ambiguity remained, and the nearest competitor became the
same-x x278/r7.5 branch with nominal base gap 5.4584%. Experiment 317
replicated seed13 as another clean 45 mm run: both rows were strong, no
ambiguity remained, and the weakest base gap was 5.4497%. Experiment 318
completed seed21 as the third clean 45 mm run: both rows were strong, no
x/radius ambiguity remained, every base/high-band diagnostic objective ranked
truth first, and the weakest base gap was 5.3608%. Aggregate 316-318 next; if
the six-row aggregate remains all-strong with zero ambiguity, promote 45 mm
Tx/Rx as a replicated clean close28 acquisition rescue while reporting the
increased acquisition offset relative to the clean close30 35 mm-offset limit.
Experiment 319 aggregated the 45 mm seed replicates: 6/6 rows selected truth
geometry, all six rows were strong, no row retained x/z/r ambiguity, and the
radius-margin mean rose to 3.20759e-03. Treat 45 mm Tx/Rx as a replicated
clean close28 acquisition rescue. Keep close30 as the tightest replicated clean
result under the standard 35 mm Tx/Rx offset, and report close28 as requiring
the larger 45 mm acquisition geometry. Run a close25 seed34 45 mm Tx/Rx
lower-bound rescue probe next to test whether 45 mm brackets between close25
and close28 or can push the clean separation limit lower. Experiment 320 ran
that close25 seed34 45 mm probe and passed cleanly: both rows were strong, no
x/radius ambiguity remained, all base/high-band diagnostics ranked truth
first, and the weakest base lateral gap was 4.1200% against the x274/r8
competitor. Replicate close25 45 mm Tx/Rx on seeds 13 and 21 before lowering
the clean separation guidance. Experiment 321 replicated seed13 as another
clean pass: both rows were strong, no ambiguity remained, all base/high-band
diagnostics ranked truth first, and the weakest base lateral gap was 4.2551%.
Run seed21 and aggregate 320-322 before promoting close25 under the 45 mm
Tx/Rx acquisition. Experiment 322 completed seed21 as another clean pass:
both rows were strong, no x/radius ambiguity remained, all base/high-band
diagnostics ranked truth first, and the weakest base lateral gap was 4.3456%.
Aggregate 320-322 next; if all six rows stay truth-selected, strong, and
zero-ambiguity, promote close25 as clean under 45 mm Tx/Rx while preserving the
distinction from the standard 35 mm acquisition. Experiment 323 aggregated the
close25 45 mm seed replicates: 6/6 rows selected truth geometry, all six rows
were strong, no row retained x/z/r ambiguity, and the radius-margin mean was
3.64800e-03. Promote close25 as a clean replicated result under the
extra-conservative 45 mm Tx/Rx acquisition. Keep close30 as the tightest clean
replicated result under the standard 35 mm Tx/Rx acquisition. Run a close20
seed34 45 mm Tx/Rx lower-bound probe next; if it fails, close25 is the current
practical 45 mm clean limit, and if it passes, replicate before lowering the
guidance again. Experiment 324 ran the close20 seed34 45 mm probe and passed
cleanly: both rows were strong, no ambiguity remained, all base/high-band
diagnostics ranked truth first, and the weakest base lateral gap was 2.7705%
against x269/r8. Replicate close20 45 mm Tx/Rx on seeds 13 and 21 before
promoting it. Experiment 325 replicated seed13 as another clean pass: both
rows were strong, no ambiguity remained, all base/high-band diagnostics ranked
truth first, and the weakest base lateral gap was 3.2599%. Run seed21 and
aggregate 324-326 before promoting close20 under 45 mm Tx/Rx. Experiment 326
completed seed21 as another clean pass: both rows were strong, no ambiguity
remained, all base/high-band diagnostics ranked truth first, and the weakest
base lateral gap was 3.0737%. Experiment 327 aggregated the close20 45 mm seed
replicates: 6/6 rows selected truth geometry, all six rows were strong, no row
retained x/z/r ambiguity, and the radius-margin mean was 3.97425e-03. Promote
close20 as clean under 45 mm Tx/Rx. Keep close30 as the tightest clean result
under the standard 35 mm acquisition, and report close20 as requiring the
extra-conservative 45 mm acquisition. Run a close15 seed34 45 mm Tx/Rx
lower-bound probe next. This is a near-touching case with about 1 mm gap
between the 6 mm and 8 mm bars, so failure would bracket the 45 mm clean limit
near close20, while a clean pass would require seed replication. Experiment
328 ran that close15 seed34 45 mm probe and passed cleanly: both rows were
strong, no x/z/r ambiguity remained, all base/high-band diagnostics ranked
truth first, and the weakest base lateral gap was 2.9713% against x264/r8.
The first smaller-radius branch was farther away: x266/r7.5 was 6.9892% worse
under nominal base and x265/r7.5 was 37.8211% worse under high-band source
mismatch. Replicate close15 45 mm Tx/Rx on seeds 13 and 21 before promoting
this near-touching case as a clean 45 mm acquisition limit. Experiment 329
replicated seed13 as another clean close15 pass: both rows were strong, no
ambiguity interval remained, all base/high-band diagnostics ranked truth first,
and the weakest base lateral gap was 3.5259% against x264/r8. Run seed21 and
aggregate 328-330 before promoting close15 under 45 mm Tx/Rx. Experiment 330
completed seed21 as another clean close15 pass: both rows were strong, no
ambiguity interval remained, all base/high-band diagnostics ranked truth first,
and the weakest base lateral gap was 3.3777% against x264/r8. Aggregate
328-330 next; if all six rows remain truth-selected, strong, and zero-ambiguity,
promote close15 as a clean near-touching result under 45 mm Tx/Rx. Experiment
331 aggregated the close15 45 mm seed replicates: 6/6 rows selected truth
geometry, all six rows were strong, no row retained x/z/r ambiguity, and the
radius-margin mean was 4.00048e-03. Promote close15 as a clean replicated
near-touching result under the extra-conservative 45 mm Tx/Rx acquisition.
Keep close30 as the tightest clean replicated result under the standard
35 mm acquisition. Run a close14 seed34 45 mm Tx/Rx tangent lower-bound probe
next; if it fails, close15 is the current practical 45 mm clean limit, and if
it passes, replicate before lowering the guidance again. Experiment 332 ran the
close14 seed34 tangent probe and passed cleanly: both rows were strong, no
ambiguity interval remained, all base/high-band diagnostics ranked truth first,
and the weakest base lateral gap was 3.0986% against x263/r8. Replicate close14
45 mm Tx/Rx on seeds 13 and 21 before promoting this tangent geometry as a
clean 45 mm acquisition limit. Experiment 333 replicated seed13 as another
clean close14 tangent pass: both rows were strong, no ambiguity interval
remained, all base/high-band diagnostics ranked truth first, and the weakest
base lateral gap was 3.6243% against x263/r8. Run seed21 and aggregate 332-334
before promoting close14 under 45 mm Tx/Rx. Experiment 334 completed seed21 as
another clean close14 tangent pass: both rows were strong, no ambiguity
interval remained, all base/high-band diagnostics ranked truth first, and the
weakest base lateral gap was 3.5299% against x263/r8. Aggregate 332-334 next;
if all six rows remain truth-selected, strong, and zero-ambiguity, promote
close14 as clean under 45 mm Tx/Rx. Experiment 335 aggregated the close14
45 mm seed replicates: 6/6 rows selected truth geometry, all six rows were
strong, no row retained x/z/r ambiguity, and the radius-margin mean was
3.97836e-03. Promote close14 as the clean physical spacing floor under the
4-source, 45 mm Tx/Rx acquisition. Do not probe smaller truth spacing for this
radius pair as a separate-bar geometry because close13 would overlap the
6 mm and 8 mm circles. Move next to acquisition-cost probes: run a close14
seed34 sources=3, Tx/Rx=45 mm diagnostic; if it fails, 4 sources remain the
minimum clean tangent acquisition, and if it passes, replicate before lowering
the source-count guidance. Experiment 336 ran that sources=3 cost probe. It was
faster, but it failed as a clean geometry update: the source-mismatch row chose
x265/r8 while truth x264/r8 was only 0.1702% worse, and both rows retained a
264-265 mm x-ambiguity interval. Keep sources=4 as the minimum clean close14
tangent acquisition under 45 mm Tx/Rx. Experiment 337 tested 20% RMS noise on
the close14 4-source 45 mm tangent case. It preserved truth-selected point
recovery in both rows, but both rows retained a 263-264 mm x-ambiguity interval.
Treat 20% noise as interval-reporting robustness, not clean zero-ambiguity
operation. Run a 15% noise seed34 probe next to bracket the clean noise
threshold between the replicated 10% clean result and the 20% interval result.
Experiment 338 ran that 15% RMS noise seed34 probe and recovered the clean
truth point in both rows: both were strong, both selected x264/z90/r8, and the
ambiguity interval collapsed to that single truth point. Treat 15% as a clean
seed34 bracket result, not yet as a replicated noise-robust operating point.
Replicate 15% noise on seeds 13 and 21 before promoting the close14 tangent
acquisition above the already replicated 10% RMS clean noise level. Experiment
339 replicated 15% RMS noise on seed13 and stayed clean: both rows selected
x264/z90/r8, both were strong, and no ambiguity interval remained. Run seed21
next; if it also stays clean, aggregate 338-340 and promote 15% RMS as a
replicated clean close14 tangent noise level. Experiment 340 completed seed21
and also stayed clean: both rows selected x264/z90/r8, both were strong, and
no ambiguity interval remained. Aggregate 338-340 next; if the six-row
aggregate confirms all truth-selected, strong, zero-ambiguity rows, promote
15% RMS as the replicated clean close14 tangent noise level while keeping
20% RMS as point-correct but interval-reporting. Experiment 341 aggregated
338-340 and confirmed the six-row result: 6/6 rows selected truth geometry, all
six were strong, no row retained x/z/r ambiguity, and the radius-margin mean
was 3.76005e-03. Promote 15% RMS as the replicated clean close14 tangent noise
level under the 4-source, 45 mm Tx/Rx acquisition. Keep 20% RMS as
point-correct but interval-reporting. If a tighter noise threshold is needed,
run a 17.5% RMS seed34 bracket before replicating higher noise levels.
Experiment 342 ran that 17.5% RMS seed34 bracket and recovered the truth point
in both rows with strong radius labels, but the nominal row retained a
263-264 mm x-ambiguity interval around the same-radius x263/r8 competitor.
Treat 17.5% RMS as point-correct but not clean. The clean-to-interval
transition is now bracketed between replicated-clean 15% RMS and
seed34-ambiguous 17.5% RMS. Run a 16.25% RMS seed34 bracket next if the
threshold needs a tighter midpoint. Experiment 343 ran the 16.25% RMS seed34
midpoint and again recovered truth in both rows with strong radius labels, but
the nominal row retained the same 263-264 mm x-ambiguity interval. Treat
16.25% RMS as point-correct but not clean. The clean-to-interval transition is
now bracketed between replicated-clean 15% RMS and seed34-ambiguous 16.25% RMS.
Run a 15.625% RMS seed34 midpoint if the threshold needs further tightening.
Experiment 344 ran that 15.625% RMS seed34 midpoint and again recovered truth
with strong radius labels, but the nominal row still retained the x263-r8 /
x264-r8 ambiguity interval. Treat 15.625% RMS as point-correct but not clean.
The clean-to-interval transition is now bracketed tightly between
replicated-clean 15% RMS and seed34-ambiguous 15.625% RMS. Run a 15.3125% RMS
seed34 midpoint only if the threshold needs finer resolution. Experiment 345
ran that 15.3125% RMS seed34 midpoint and was formally clean: both rows
selected x264/z90/r8, both were strong, and no ambiguity interval remained.
This was an edge-clean result because the nominal x263/r8 competitor sat only
about 6.27e-06 absolute misfit above the ambiguity cutoff. The seed34
clean-to-interval transition is now bracketed between clean 15.3125% RMS and
ambiguous 15.625% RMS. Keep the replicated clean noise level at 15% RMS unless
a higher bracket is replicated. Experiment 346 ran the 15.46875% RMS midpoint
and recovered truth, but the nominal row returned to a 263-264 mm x-ambiguity
interval. Treat 15.46875% RMS as point-correct but not clean. The seed34
transition is now bracketed between 15.3125% edge-clean and 15.46875%
ambiguous. Since 15.3125% is already edge-clean, the next useful step is
replicating 15.3125% on seed13 before treating it as more than a single-seed
bracket point. Experiment 347 replicated 15.3125% RMS on seed13 and stayed
clean: both nominal and source-mismatch rows selected x264/z90/r8, both were
strong, and both ambiguity intervals collapsed to the single truth point. This
replicate is less edge-like than seed34 because the x263/r8 competitor sits
3.20e-04 to 4.74e-04 absolute misfit above the ambiguity cutoff. Run seed21 at
15.3125% RMS before aggregating or promoting 15.3125% above the current
replicated-clean 15% RMS guidance. Experiment 348 ran seed21 at 15.3125% RMS
and also stayed clean: both rows selected x264/z90/r8 with strong labels and
single-point ambiguity intervals. The nearest x263/r8 competitor stayed
2.04e-04 to 2.42e-04 absolute misfit above the ambiguity cutoff. The
seed34/seed13/seed21 15.3125% RMS set is now ready for aggregate reporting
before promoting 15.3125% beyond the current replicated-clean 15% RMS level.
Experiment 349 aggregated the 15.3125% seed34/seed13/seed21 set: all six rows
selected truth geometry, all six labels were strong, and all x/z/r ambiguity
widths were zero. Promote 15.3125% RMS as the replicated clean close14 tangent
noise level under the 4-source, 45 mm Tx/Rx acquisition. Keep 15.46875% RMS as
a seed34 point-correct but interval-reporting bracket. If the goal is tighter
threshold localization, run a 15.390625% seed34 midpoint between
replicated-clean 15.3125% and seed34-ambiguous 15.46875%. Experiment 350 ran
that 15.390625% seed34 midpoint and recovered truth with strong labels, but
the nominal row retained the x263/r8 to x264/r8 ambiguity interval. It is only
4.33e-06 absolute misfit inside the ambiguity cutoff, so it is an edge
interval result. The seed34 transition is now bracketed between
replicated-clean 15.3125% and seed34-ambiguous 15.390625%. Run 15.3515625% RMS
as the next seed34 midpoint if tighter transition localization is still useful.
Experiment 351 ran that 15.3515625% midpoint and was formally clean, but only
by an edge margin: the nominal x263/r8 competitor sat 9.75e-07 absolute misfit
above the ambiguity cutoff. Keep the promoted replicated-clean guidance at
15.3125% RMS. The single-seed seed34 transition is now bracketed between
edge-clean 15.3515625% and ambiguous 15.390625%; run 15.37109375% RMS only if
the goal remains single-seed transition localization. Experiment 352 ran
15.37109375% RMS and recovered truth with strong labels, but the nominal row
again retained the x263/r8 to x264/r8 ambiguity interval. The x263/r8
competitor was only 1.67e-06 absolute misfit inside the ambiguity cutoff. The
single-seed transition is now bracketed between edge-clean 15.3515625% and
ambiguous 15.37109375%; 15.361328125% RMS is the next midpoint only if the
remaining value is tighter threshold localization. Keep the replicated clean
guidance at 15.3125% RMS. Experiment 353 ran 15.361328125% RMS and was
point-correct but not clean: the nominal x263/r8 competitor was only 3.49e-07
absolute misfit inside the ambiguity cutoff. The seed34 boundary is now
localized between 15.3515625% edge-clean and 15.361328125% ambiguous. Stop
bisection for now; the practical, replicated clean guidance remains 15.3125%
RMS, and the 15.35%-level boundary is too threshold-sensitive to promote.
Experiment 354 changed the acquisition instead of the threshold: sources=5 at
15.361328125% still selected truth, but both rows retained a 264-265 mm
x-ambiguity interval and the radius margins narrowed. A fifth source does not
rescue this edge case. If acquisition-density rescue remains useful, test
sources=7 next; otherwise keep 4 sources and 15.3125% RMS as the practical
clean guidance. Experiment 355 ran sources=7 at the same 15.361328125% RMS
noise level and again selected truth with strong radius labels. It improved
the acquisition-density result, because the source-mismatch row collapsed to
x=264 only and the nearest x263/r8 competitor missed the cutoff, but only by
2.79e-06 absolute misfit. The nominal row still retained a 263-264 mm
x-ambiguity interval, with x263/r8 inside the cutoff by 2.24e-04. Treat
sources=7 as a partial rescue, not a clean promoted operating point. Stop the
acquisition-density rescue branch here unless a new acquisition idea is being
tested; keep the replicated clean close14 guidance at 15.3125% RMS under the
4-source, 45 mm Tx/Rx acquisition. Experiment 356 aggregated the sources=4,
5, and 7 dose-response rows at the same seed34 15.361328125% RMS boundary.
All six rows were point-correct and strong, but four of six rows retained a
1 mm x-ambiguity interval. Five sources was the weakest setting, with two
x-ambiguity rows and the smallest radius margins. Seven sources recovered some
margin and improved the source-mismatch row, but still left nominal x
ambiguous. This closes the source-count branch: do not spend more GPU time on
source-count escalation for this boundary unless a new physics/objective lever
is introduced. Experiment 357 tested that new lever by keeping 4 sources but
raising the Tx/Rx offset from 45 mm to 50 mm at the same seed34
15.361328125% RMS boundary. This cleaned the case: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nearest nominal x263/r8 competitor cleared the ambiguity cutoff by
4.92e-04. Replicate the 50 mm Tx/Rx setting on seeds 13 and 21 before
promoting 15.361328125% RMS as clean under the larger-offset acquisition.
Experiment 358 replicated the 50 mm Tx/Rx result on seed13: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 6.67e-04. Run
seed21 next; if it also stays clean, aggregate 357-359 and promote the larger
50 mm offset as a replicated rescue for the 15.361328125% RMS close14 boundary.
Experiment 359 completed seed21 and again stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 7.04e-04.
Aggregate 357-359 next; if all six rows remain true, strong, and
zero-ambiguity, promote 4 sources with 50 mm Tx/Rx as the replicated
larger-offset rescue for 15.361328125% RMS close14 tangent operation.
Experiment 360 aggregated the seed34/13/21 Tx/Rx=50 set and confirmed the
replicated rescue: all six rows selected truth geometry, all six were strong,
and all x/z/r ambiguity widths were zero. Promote 4 sources with 50 mm Tx/Rx
as a clean close14 tangent operating point at 15.361328125% RMS. Keep the
cheaper 45 mm Tx/Rx guidance at 15.3125% RMS for replicated clean operation;
use the larger 50 mm offset when the extra noise margin is worth the
acquisition cost. Experiment 361 tested the next old 45 mm ambiguous bracket,
15.46875% RMS seed34, under the 50 mm Tx/Rx acquisition. It also cleaned:
both rows selected x264/z90/r8, both were strong, both x intervals collapsed
to 264-264 mm, and the nearest nominal x263/r8 competitor cleared the
ambiguity cutoff by 4.81e-04. Replicate 15.46875% RMS under Tx/Rx=50 on seeds
13 and 21 before promoting this higher noise level. Experiment 362 replicated
seed13 cleanly: both rows selected x264/z90/r8, both were strong, both x
intervals collapsed to 264-264 mm, and the nominal x263/r8 competitor cleared
the ambiguity cutoff by 6.56e-04. Run seed21 next and then aggregate 361-363
if it also remains clean. Experiment 363 completed seed21 and also stayed
clean: both rows selected x264/z90/r8, both were strong, both x intervals
collapsed to 264-264 mm, and the nominal x263/r8 competitor cleared the
ambiguity cutoff by 6.94e-04. Experiment 364 aggregated 361-363 and confirmed
the replicated clean result: all six rows selected truth geometry, all six were
strong, and all x/z/r ambiguity widths were zero. Promote 15.46875% RMS under
4-source 50 mm Tx/Rx as the current larger-offset close14 clean operating
point. Experiment 365 tested the next stress bracket, 15.625% RMS seed34,
under the same acquisition. It also cleaned: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the nearest
nominal x263/r8 competitor cleared the ambiguity cutoff by 4.65e-04. Do not
promote 15.625% RMS yet. Experiment 366 replicated seed13 cleanly: both rows
selected x264/z90/r8, both were strong, both x intervals collapsed to
264-264 mm, and the nominal x263/r8 competitor cleared the ambiguity cutoff
by 6.41e-04. Experiment 367 completed seed21 and also stayed clean: both rows
selected x264/z90/r8, both were strong, both x intervals collapsed to
264-264 mm, and the nominal x263/r8 competitor cleared the ambiguity cutoff
by 6.79e-04. Experiment 368 aggregated 365-367 and confirmed the replicated
clean result: all six rows selected truth geometry, all six were strong, and
all x/z/r ambiguity widths were zero. Promote 15.625% RMS under 4-source
50 mm Tx/Rx as the current larger-offset close14 clean operating point. The
next stress test is 16.25% RMS under the same acquisition. Experiment 369 ran
that seed34 16.25% RMS probe and stayed clean: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the nearest
nominal x263/r8 competitor cleared the ambiguity cutoff by 3.97e-04. This
margin is smaller than at 15.625% RMS, so replicate seeds 13 and 21 before
promoting 16.25% RMS. Experiment 370 replicated seed13 cleanly: both rows
selected x264/z90/r8, both were strong, both x intervals collapsed to
264-264 mm, and the nominal x263/r8 competitor cleared the ambiguity cutoff
by 5.80e-04. Run seed21 next; if it also remains clean, aggregate 369-371
before promoting 16.25% RMS. Experiment 371 completed seed21 and also stayed
clean: both rows selected x264/z90/r8, both were strong, both x intervals
collapsed to 264-264 mm, and the nominal x263/r8 competitor cleared the
ambiguity cutoff by 6.19e-04. Aggregate 369-371 next; if all six rows remain
true, strong, and zero-ambiguity, promote 16.25% RMS under 4-source 50 mm
Tx/Rx. Experiment 372 aggregated 369-371 and confirmed the replicated clean
result: all six rows selected truth geometry, all six were strong, and all
x/z/r ambiguity widths were zero. Promote 16.25% RMS under 4-source 50 mm
Tx/Rx as the current larger-offset close14 clean operating point. The next
stress test is 17.5% RMS under the same acquisition. Experiment 373 ran that
seed34 17.5% RMS probe and stayed clean: both rows selected x264/z90/r8, both
were strong, both x intervals collapsed to 264-264 mm, and the nearest nominal
x263/r8 competitor cleared the ambiguity cutoff by 2.57e-04. This rescues the
old 45 mm x-ambiguous bracket, but the nominal clearance margin is tight, so
replicate seeds 13 and 21 before promoting 17.5% RMS. Experiment 374
replicated seed13 cleanly: both rows selected x264/z90/r8, both were strong,
both x intervals collapsed to 264-264 mm, and the nominal x263/r8 competitor
cleared the ambiguity cutoff by 4.52e-04. Run seed21 next; if it also remains
clean, aggregate 373-375 before promoting 17.5% RMS. Experiment 375 completed
seed21 and also stayed clean: both rows selected x264/z90/r8, both were
strong, both x intervals collapsed to 264-264 mm, and the tighter
source-mismatch x263/r8 competitor cleared the ambiguity cutoff by 4.87e-04.
Aggregate 373-375 next; if all six rows remain true, strong, and
zero-ambiguity, promote 17.5% RMS under 4-source 50 mm Tx/Rx. Experiment 376
aggregated 373-375 and confirmed the replicated clean result: all six rows
selected truth geometry, all six were strong, and all x/z/r ambiguity widths
were zero. Promote 17.5% RMS under 4-source 50 mm Tx/Rx as the current
larger-offset close14 clean operating point. The next stress test is 20% RMS
under the same acquisition. Experiment 377 ran that seed34 20% RMS probe. It
selected the true x264/z90/r8 point in both rows and kept strong radius
margins, but the nominal row retained a 263-264 mm x interval: x263/r8 stayed
inside the ambiguity cutoff by 4.49e-05. Treat 20% RMS under 50 mm Tx/Rx as
point-correct but not clean. The clean-to-ambiguous transition is now bracketed
between replicated-clean 17.5% RMS and seed34-ambiguous 20% RMS. Run 18.75%
RMS seed34 next. Experiment 378 ran that midpoint and stayed clean: both rows
selected x264/z90/r8, both were strong, both x intervals collapsed to
264-264 mm, and the nearest nominal x263/r8 competitor cleared the ambiguity
cutoff by 1.10e-04. This is a tight clean result. Replicate seeds 13 and 21
before promoting 18.75% RMS. Experiment 379 replicated seed13 cleanly: both
rows selected x264/z90/r8, both were strong, both x intervals collapsed to
264-264 mm, and the nominal x263/r8 competitor cleared the ambiguity cutoff by
3.15e-04. Run seed21 next; if it also remains clean, aggregate 378-380 before
promoting 18.75% RMS. Experiment 380 completed seed21 and also stayed clean:
both rows selected x264/z90/r8, both were strong, both x intervals collapsed
to 264-264 mm, and the tighter source-mismatch x263/r8 competitor cleared the
ambiguity cutoff by 2.48e-04. Aggregate 378-380 next; if all six rows remain
true, strong, and zero-ambiguity, promote 18.75% RMS under 4-source 50 mm
Tx/Rx. Experiment 381 aggregated 378-380 and confirmed the replicated clean
result: all six rows selected truth geometry, all six were strong, and all
x/z/r ambiguity widths were zero. Promote 18.75% RMS under 4-source 50 mm
Tx/Rx as the current larger-offset close14 clean operating point. The
clean-to-ambiguous transition is now bracketed between replicated-clean
18.75% RMS and seed34-ambiguous 20% RMS. Run 19.375% RMS seed34 next.
Experiment 382 ran that midpoint and stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 3.32e-05. This
is the tightest clean seed34 result in the larger-offset bracket and remains
very close to the 20% seed34 x-ambiguous failure, so do not promote from one
seed. Replicate 19.375% RMS on seeds 13 and 21 before deciding whether to
promote the level or continue bracketing the transition.
Experiment 383 replicated seed13 cleanly: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the nominal
x263/r8 competitor cleared the ambiguity cutoff by 2.44e-04. Run seed21 next;
if it also remains clean, aggregate 382-384 before promoting 19.375% RMS.
Experiment 384 completed seed21 and also stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the tighter source-mismatch x263/r8 competitor cleared the ambiguity cutoff by
1.26e-04. Aggregate 382-384 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.375% RMS under 4-source 50 mm Tx/Rx.
Experiment 385 aggregated 382-384 and confirmed the replicated clean result:
all six rows selected truth geometry, all six were strong, and all x/z/r
ambiguity widths were zero. Promote 19.375% RMS under 4-source 50 mm Tx/Rx as
the current larger-offset close14 clean operating point. The clean-to-ambiguous
transition is now bracketed between replicated-clean 19.375% RMS and seed34
x-ambiguous 20% RMS. Run 19.6875% RMS seed34 next.
Experiment 386 ran that midpoint. It selected the true x264/z90/r8 point in
both rows and kept strong radius margins, but the nominal row retained a
263-264 mm x interval because x263/r8 stayed inside the ambiguity cutoff by
5.64e-06. Treat 19.6875% RMS as point-correct but not clean. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.375% RMS and seed34-ambiguous 19.6875% RMS. Run 19.53125% RMS seed34 next.
Experiment 387 ran that midpoint and stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 1.38e-05. This
is an extremely tight clean result, so do not promote from one seed. Replicate
19.53125% RMS on seeds 13 and 21 before deciding whether to promote it.
Experiment 388 replicated seed13 cleanly: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the nominal
x263/r8 competitor cleared the ambiguity cutoff by 2.26e-04. Run seed21 next;
if it also remains clean, aggregate 387-389 before promoting 19.53125% RMS.
Experiment 389 completed seed21 and also stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the tighter source-mismatch x263/r8 competitor cleared the ambiguity cutoff by
9.48e-05. Aggregate 387-389 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.53125% RMS under 4-source 50 mm Tx/Rx.
Experiment 390 aggregated 387-389 and confirmed the replicated clean result:
all six rows selected truth geometry, all six were strong, and all x/z/r
ambiguity widths were zero. Promote 19.53125% RMS under 4-source 50 mm Tx/Rx
as the current larger-offset close14 clean operating point. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.53125% RMS and seed34-ambiguous 19.6875% RMS. Run 19.609375% RMS seed34
next.
Experiment 391 ran that midpoint and stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 4.12e-06. This
is the tightest clean seed34 result so far and is almost on the ambiguity
boundary, so do not promote from one seed. Replicate 19.609375% RMS on seeds
13 and 21 before deciding whether to promote it.
Experiment 392 replicated seed13 cleanly: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the nominal
x263/r8 competitor cleared the ambiguity cutoff by 2.17e-04. Run seed21 next;
if it also remains clean, aggregate 391-393 before promoting 19.609375% RMS.
Experiment 393 completed seed21 and also stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the tighter source-mismatch x263/r8 competitor cleared the ambiguity cutoff by
7.93e-05. Aggregate 391-393 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.609375% RMS under 4-source 50 mm Tx/Rx.
Experiment 394 aggregated 391-393 and confirmed the replicated clean result:
all six rows selected truth geometry, all six were strong, and all x/z/r
ambiguity widths were zero. Promote 19.609375% RMS under 4-source 50 mm Tx/Rx
as the current larger-offset close14 clean operating point. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.609375% RMS and seed34-ambiguous 19.6875% RMS. Run 19.6484375% RMS seed34
next.
Experiment 395 ran that midpoint. It selected the true x264/z90/r8 point in
both rows and kept strong radius margins, but the nominal row retained a
263-264 mm x interval because x263/r8 stayed inside the ambiguity cutoff by
7.58e-07. Treat 19.6484375% RMS as point-correct but not clean. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.609375% RMS and seed34-ambiguous 19.6484375% RMS. Run 19.62890625% RMS
seed34 next.
Experiment 396 ran that midpoint and stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 1.68e-06. This
is the tightest clean seed34 result so far, so do not promote from one seed.
Replicate 19.62890625% RMS on seeds 13 and 21 before deciding whether to
promote it.
Experiment 397 replicated seed13 cleanly: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the nominal
x263/r8 competitor cleared the ambiguity cutoff by 2.15e-04. Run seed21 next;
if it also remains clean, aggregate 396-398 before promoting 19.62890625% RMS.
Experiment 398 completed seed21 and also stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the tighter source-mismatch x263/r8 competitor cleared the ambiguity cutoff by
7.54e-05. Aggregate 396-398 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.62890625% RMS under 4-source 50 mm Tx/Rx.
Experiment 399 aggregated 396-398 and confirmed the replicated clean result:
all six rows selected truth geometry, all six were strong, and all x/z/r
ambiguity widths were zero. Promote 19.62890625% RMS under 4-source 50 mm
Tx/Rx as the current larger-offset close14 clean operating point. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.62890625% RMS and seed34-ambiguous 19.6484375% RMS. Run 19.638671875% RMS
seed34 next.
Experiment 400 ran that midpoint and stayed clean: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 4.61e-07. This
is effectively on the ambiguity boundary, so do not promote from one seed.
Replicate 19.638671875% RMS on seeds 13 and 21 before deciding whether to
promote it. Experiment 401 replicated seed13 cleanly: both rows selected
x264/z90/r8, both were strong, both x intervals collapsed to 264-264 mm, and
the nominal x263/r8 competitor cleared the ambiguity cutoff by 2.14e-04. Run
seed21 next; if it also remains clean, aggregate 400-402 before promoting
19.638671875% RMS. Experiment 402 completed seed21 and also stayed clean:
both rows selected x264/z90/r8, both were strong, both x intervals collapsed
to 264-264 mm, and the tighter source-mismatch x263/r8 competitor cleared the
ambiguity cutoff by 7.34e-05. Aggregate 400-402 next; if all six rows remain
true, strong, and zero-ambiguity, promote 19.638671875% RMS under 4-source
50 mm Tx/Rx. Experiment 403 aggregated 400-402 and confirmed the replicated
clean result: all six rows selected truth geometry, all six were strong, and
all x/z/r ambiguity widths were zero. Promote 19.638671875% RMS under
4-source 50 mm Tx/Rx as the current larger-offset close14 clean operating
point. The clean-to-ambiguous transition is now bracketed between
replicated-clean 19.638671875% RMS and seed34-ambiguous 19.6484375% RMS. Run
19.6435546875% RMS seed34 next. Experiment 404 ran that midpoint. It
selected the true x264/z90/r8 point in both rows and kept strong radius
margins, but the nominal row retained a 263-264 mm x interval because x263/r8
stayed inside the ambiguity cutoff by 1.48e-07. Treat 19.6435546875% RMS as
point-correct but not clean. The clean-to-ambiguous transition is now
bracketed between replicated-clean 19.638671875% RMS and seed34-ambiguous
19.6435546875% RMS. Run 19.64111328125% RMS seed34 next. Experiment 405 ran
that lower midpoint and stayed clean: both rows selected x264/z90/r8, both
were strong, both x intervals collapsed to 264-264 mm, and the nominal
x263/r8 competitor cleared the ambiguity cutoff by 1.56e-07. This is
effectively on the boundary, so do not promote from one seed. Replicate
19.64111328125% RMS on seeds 13 and 21 before deciding whether to promote it.
Experiment 406 replicated seed13 cleanly: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the nominal
x263/r8 competitor cleared the ambiguity cutoff by 2.13e-04. Run seed21 next;
if it also remains clean, aggregate 405-407 before promoting
19.64111328125% RMS. Experiment 407 completed seed21 and also stayed clean:
both rows selected x264/z90/r8, both were strong, both x intervals collapsed
to 264-264 mm, and the tighter source-mismatch x263/r8 competitor cleared the
ambiguity cutoff by 7.30e-05. Aggregate 405-407 next; if all six rows remain
true, strong, and zero-ambiguity, promote 19.64111328125% RMS under 4-source
50 mm Tx/Rx. Experiment 408 aggregated 405-407 and confirmed the replicated
clean result: all six rows selected truth geometry, all six were strong, and
all x/z/r ambiguity widths were zero. Promote 19.64111328125% RMS under
4-source 50 mm Tx/Rx as the current larger-offset close14 clean operating
point. The clean-to-ambiguous transition is now bracketed between
replicated-clean 19.64111328125% RMS and seed34-ambiguous 19.6435546875% RMS.
Run 19.642333984375% RMS seed34 next. Experiment 409 ran that midpoint and
stayed technically clean: both rows selected x264/z90/r8, both were strong,
both x intervals collapsed to 264-264 mm, and the nominal x263/r8 competitor
cleared the ambiguity cutoff by only 4.02e-09. This is numerically on the
boundary, so do not promote from one seed. Replicate 19.642333984375% RMS on
seeds 13 and 21 before deciding whether to promote it. Experiment 410
replicated seed13 cleanly: both rows selected x264/z90/r8, both were strong,
both x intervals collapsed to 264-264 mm, and the nominal x263/r8 competitor
cleared the ambiguity cutoff by 2.13e-04. Run seed21 next; if it also remains
clean, aggregate 409-411 before promoting 19.642333984375% RMS. Experiment
411 completed seed21 and also stayed clean: both rows selected x264/z90/r8,
both were strong, both x intervals collapsed to 264-264 mm, and the tighter
source-mismatch x263/r8 competitor cleared the ambiguity cutoff by 7.27e-05.
Aggregate 409-411 next; if all six rows remain true, strong, and
zero-ambiguity, promote 19.642333984375% RMS under 4-source 50 mm Tx/Rx.
Experiment 412 aggregated 409-411 and confirmed the replicated clean result:
all six rows selected truth geometry, all six were strong, and all x/z/r
ambiguity widths were zero. Promote 19.642333984375% RMS under 4-source
50 mm Tx/Rx as the current larger-offset close14 clean operating point. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.6435546875% RMS. Run
19.6429443359375% RMS seed34 next. Experiment 413 ran that midpoint. It
selected the true x264/z90/r8 point in both rows and kept strong radius
margins, but the nominal row retained a 263-264 mm x interval because x263/r8
stayed inside the ambiguity cutoff by 7.22e-08. Treat 19.6429443359375% RMS
as point-correct but not clean. The clean-to-ambiguous transition is now
bracketed between replicated-clean 19.642333984375% RMS and seed34-ambiguous
19.6429443359375% RMS. Run 19.64263916015625% RMS seed34 next. Experiment
414 ran that lower midpoint. It again selected the true x264/z90/r8 point in
both rows and kept strong radius margins, but the nominal row retained a
263-264 mm x interval because x263/r8 stayed inside the ambiguity cutoff by
3.41e-08. Treat 19.64263916015625% RMS as point-correct but not clean. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.64263916015625% RMS. Run
19.642486572265625% RMS seed34 next. Experiment 415 ran that lower midpoint.
It again selected the true x264/z90/r8 point in both rows and kept strong
radius margins, but the nominal row retained a 263-264 mm x interval because
x263/r8 stayed inside the ambiguity cutoff by 1.50e-08. Treat
19.642486572265625% RMS as point-correct but not clean. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.642486572265625% RMS. Run
19.6424102783203125% RMS seed34 next. Experiment 416 ran that lower
midpoint. It again selected the true x264/z90/r8 point in both rows and kept
strong radius margins, but the nominal row retained a 263-264 mm x interval
because x263/r8 stayed inside the ambiguity cutoff by 5.51e-09. Treat
19.6424102783203125% RMS as point-correct but not clean. The
clean-to-ambiguous transition is now bracketed between replicated-clean
19.642333984375% RMS and seed34-ambiguous 19.6424102783203125% RMS. Run
19.64237213134765625% RMS seed34 next. Experiment 417 ran that lower
midpoint. It again selected the true x264/z90/r8 point in both rows and kept
strong radius margins, but the nominal row retained a 263-264 mm x interval
because x263/r8 stayed inside the ambiguity cutoff by 7.42e-10. Treat
19.64237213134765625% RMS as point-correct but not clean. This is essentially
the numerical edge of the configured ambiguity rule. Keep replicated-clean
19.642333984375% RMS as the promoted 4-source 50 mm Tx/Rx close14 operating
point and stop bisection of this scalar bracket. Experiment 418 packaged this
boundary into a CPU-only summary artifact: six seed34 rows, one clean endpoint,
five point-correct-not-clean upper rows, final ambiguous upper
19.642372131347656% RMS, bracket width 3.814697265625e-05% RMS, and final
nominal x263/r8 cutoff margin -7.41956e-10. The figure set confirms the
failure mode is lateral x ambiguity while radius margins remain strong, so the
next stage should not spend more GPU time bisecting this scalar noise bracket.
Experiment 419 returned to the staged variable-radius packaging branch and
added a dry-run replay/orchestration plan to the packaged three-seed summary.
It records 15/15 available stage commands from their run manifests, writes
staged_variable_radius_replay_plan.json plus a non-executable command-plan
text file, and preserves the prior policy result: all three cases use the
7-source refined focused stage for point x and all three joint-radius stages
rank the true [5,6,8] tuple first. This completes the immediate packaging gap
without launching more GPU work. The handoff matrix in
docs/experiments/48_research_handoff_matrix.md now separates location
accuracy, radius confidence, source/material caveats, visualization evidence,
runtime/cost, and next action across the main branches.
Experiment 420 closed the remaining material/source visualization checklist
item without opening a new physical inversion scene. The comparison runner now
accepts true/candidate material overrides, and the generated GIF compares the
experiment 056 true 1e7 S/m steel case against the actual same-radius
1e5 S/m branch. The package also points to the already validated experiment
052 source-mismatch comparison GIFs for the real wrong-radius source branches.
The decision is to add future material/source animations only when a new
objective matrix exposes a real competing branch.
Experiment 421 opened the field-like source-shape calibration branch. It kept
the accepted amplitude/time/frequency source-profile grid fixed, but injected a
delayed secondary pulse into the observed wavelet. Nominal and controlled
source-mismatch cases still selected r=6.0 mm, but the ringdown cases selected
the high-radius bound r=7.8 mm, both without and with 5% noise. This is a real
source-shape failure: the current low-dimensional source profile is not enough
for delayed source ringing. The next diagnostic should allow a small modeled
ringdown basis and verify whether that restores r=6.0 mm before any multi-rebar
scaling.
Experiment 422 ran that mitigation. It added modeled ringdown scales 0.0 and
0.25 to the source-profile grid, keeping the same geometry candidates and the
same four observed cases as experiment 421. Nominal and controlled source
mismatch stayed at r=6.0 mm with modeled ringdown 0.0. The ringdown and
ringdown+5% noise cases returned from the wrong r=7.8 mm branch to r=6.0 mm
with modeled ringdown 0.25. The field/lab branch should treat source-shape
profiling as a diagnostic calibration stage and replicate it across additional
ringdown amplitudes/noise seeds before multi-rebar scaling.
Experiment 423 ran the first amplitude/noise/source-mismatch scaling matrix
with the same coarse modeled ringdown grid. Most rows stayed correct, including
observed ringdown 0.30, 0.25 ringdown with 5% and 10% noise, and combined
source mismatch plus 0.25 ringdown. The observed ringdown 0.20 row failed,
selecting r=7.8 mm with modeled ringdown 0.25 and reduced global amplitude.
The failure shows that a discrete ringdown grid is brittle: the source profile
must fit primary-pulse and delayed-ringdown coefficients separately, not only
choose a fixed ringdown shape and one global amplitude.
Experiment 424 replaced the discrete ringdown choice with a linear
primary/ringdown source-basis coefficient fit. On the same seven-case matrix as
experiment 423, every row recovered r=6.0 mm. The previously failing
ringdown020 row recovered a fitted ringdown scale of 0.20; ringdown030
recovered 0.30; noisy and source-mismatch ringdown025 rows recovered about
0.25. This promotes source-basis coefficient fitting as the source-shape
diagnostic path and rejects the coarse discrete ringdown-grid path.
Experiment 425 moved the coefficient-fit source-shape diagnostic into a narrow
three-rebar local geometry gate. With the left rebar fixed at x=150 mm,
z=90 mm and radii 5.8/6.0/6.2/7.4/7.8 mm, nominal, ringdown020,
ringdown025+5% noise, and source-mismatch+ringdown025 cases all selected the
true r=6.0 mm. The fitted source profiles recovered ringdown 0.20 and about
0.25 where injected. This passes the first multi-rebar source-shape gate, but
only for a narrow fixed-x/z window; the next scale step should be a compact
x/z/r window, not a full 325-candidate Stage 4C sweep.
Experiment 426 ran that compact x/z/r window for the same left target:
x=149/150/151 mm, z=89/90/91 mm, and r=5.8/6.0/6.2 mm, for 27 candidates.
All four source-shape cases again selected the true x=150 mm, z=90 mm,
r=6.0 mm. The weakest radius margin stayed the same as the fixed-x/z gate,
2.936e-04 for the ringdown020 row, and the closest competitor was still
r=6.2 mm at the true x/z rather than a shifted-location branch. This supports
the coefficient-fit source-shape method for a compact local multi-rebar window,
but only for the left target with neighboring rebars fixed at truth. The next
source-shape scale step should be a compact center-target or harder-seed
replication before any full Stage 4C-sized source-shape sweep.
Experiment 427 repeated the compact x/z/r source-shape window on the center
target, using x=249/250/251 mm, z=89/90/91 mm, and r=5.8/6.0/6.2 mm. All four
source-shape cases selected the true x=250 mm, z=90 mm, r=6.0 mm. The weakest
row was the ringdown025+5% noise seed21 case, with a smaller but still positive
radius margin of 2.353e-04 against r=6.2 mm. The nearest competitors again
stayed at the true x/z with adjacent radius rather than shifting x or z. This
passes the center compact-window gate and makes the right-target compact gate
the next source-shape replication step.
Experiment 428 completed the all-target compact-window source-shape pass by
repeating the same x/z/r window on the right target: x=349/350/351 mm,
z=89/90/91 mm, and r=5.8/6.0/6.2 mm. All four source-shape cases selected the
true x=350 mm, z=90 mm, r=6.0 mm. The weakest right-target margin was
2.446e-04 in the ringdown025+5% noise seed21 row, while the weakest all-target
margin remained the center-target noisy-ringdown row from experiment 427 at
2.353e-04. This closes the compact all-target source-shape gate. The next
source-shape step should stress the center target with harder noise/source rows
before a full Stage 4C-sized source-shape sweep.
Experiment 429 ran that center-target hard-noise stress with the same compact
x/z/r window. Ringdown025 with 10% noise for seeds 13 and 21 both selected the
true x=250 mm, z=90 mm, r=6.0 mm; combined source mismatch, ringdown025, and
5-10% noise also selected the truth. The weakest margin dropped to 1.813e-04 in
the ringdown025_noise10_seed21 row, so noise tightens the radius separation but
does not create a compact-window geometry failure. The next source-shape step
should reintroduce the high-radius 7.4/7.8 mm candidates into the compact center
window, because r=7.8 mm was the original single-rebar ringdown failure branch.
Experiment 430 reintroduced those high-radius candidates in the compact center
window: x=249/250/251 mm, z=89/90/91 mm, and
r=5.8/6.0/6.2/7.4/7.8 mm. Nominal, ringdown020, ringdown025+10% noise seed21,
and source-mismatch+ringdown025+10% noise seed13 all selected the true
x=250 mm, z=90 mm, r=6.0 mm. The high-radius candidates did not enter the top
eight for any row; the closest branch remained r=6.2 mm at true x/z. This
closes the compact high-radius concern and makes a wider 5x5 x/z center window
the next controlled scale step before any full Stage 4C-sized source-shape run.
Experiment 431 ran that wider center window: x=248/249/250/251/252 mm,
z=88/89/90/91/92 mm, and r=5.8/6.0/6.2/7.4/7.8 mm. All four rows still selected
the true x=250 mm, z=90 mm, r=6.0 mm. The weakest margin remained 1.813e-04 in
the ringdown025_noise10_seed21 row, and the nearest competitor remained
r=6.2 mm at true x/z. The high-radius branches appeared only around ranks 9-12,
mostly at z=92 mm, so the widened x/z window did not turn them into near-ties.
The next source-shape step should use the full dense Stage 4C radius grid,
5.4:7.8:0.2 mm, on this center target.
Experiment 432 ran that dense Stage 4C center-target source-shape grid:
x=248/249/250/251/252 mm, z=88/89/90/91/92 mm, and r=5.4:7.8:0.2 mm. All four
rows selected the true x=250 mm, z=90 mm, r=6.0 mm. The weakest margin remained
1.813e-04 in the ringdown025_noise10_seed21 row. The dense grid exposed a
shifted-depth branch around z=91 mm and r=6.8-7.0 mm in the top candidates, but
it stayed below true r=6.0 and adjacent r=6.2 at the true x/z. This passes the
center dense source-shape gate. Next, run the same dense grid on the left target
to check target asymmetry.
Experiment 433 ran the same dense Stage 4C source-shape grid on the left target:
x=148/149/150/151/152 mm, z=88/89/90/91/92 mm, and r=5.4:7.8:0.2 mm. All four
rows selected the true x=150 mm, z=90 mm, r=6.0 mm. The weakest left-target
margin was 2.675e-04 in the source-mismatch+ringdown025+10% noise row. The same
secondary shifted-depth branch around z=91 mm and r=6.8-7.0 mm appeared in the
top candidates, but it remained below true r=6.0 and adjacent r=6.2 at true
x/z. This passes the left dense source-shape gate. Next, run the dense grid on
the right target to complete all-target dense coverage.
Experiment 434 completed that all-target dense coverage by running the same
Stage 4C source-shape grid on the right target:
x=348/349/350/351/352 mm, z=88/89/90/91/92 mm, and r=5.4:7.8:0.2 mm. All four
rows selected the true x=350 mm, z=90 mm, r=6.0 mm. The weakest right-target
margin was 2.288e-04 in the ringdown025_noise10_seed21 row. The same z=91 mm,
r=6.8-7.0 mm branch appeared, but stayed secondary. The all-target dense
source-shape gate passes; next build a CPU-only synthesis artifact for runs
425-434 before choosing seed replication or a broader coupled-geometry test.
Experiment 435 built that CPU-only synthesis artifact. It aggregates 40
source-shape rows from experiments 425-434, and all 40 selected the true target
x/z/r geometry. The weakest all-row and dense-grid margin is 1.813e-04 on the
center target, ringdown025_noise10_seed21. The synthesis figures show that the
dense Stage 4C secondary z=91 mm / r=6.8-7.0 mm branch is visible but not a
near-tie. This closes the local fixed-neighbor multi-rebar source-shape gate.
The next GPU branch should choose between seed replication and a coupled
neighbor-geometry stress where neighboring rebars are no longer held at truth.
Experiment 436 ran the first compact seed replication for the weakest center
source-shape branch, using 10% noise seeds 34 and 55 for ringdown-only and
source-mismatch+ringdown rows. All four rows selected the true x=250 mm,
z=90 mm, r=6.0 mm. The source-mismatch seed55 row created a new weakest margin,
1.006e-04 against r=6.2 at true x/z. This is still correct, but tight enough
that the next source-shape GPU step should widen/high-radius-check seed55 before
coupled-neighbor development.
Experiment 437 ran that seed55 wide/high-radius check on the center target:
x=248/249/250/251/252 mm, z=88/89/90/91/92 mm, and
r=5.8/6.0/6.2/7.4/7.8 mm. Both seed55 rows selected the true x=250 mm,
z=90 mm, r=6.0 mm. The source-mismatch seed55 margin remained 1.006e-04, and
the sparse high-radius 7.4/7.8 mm candidates stayed around ranks 10-12. The
next seed55 check should use the dense Stage 4C radius grid, because the known
secondary branch is around r=6.8-7.0 mm.
Experiment 438 ran that dense seed55 center grid with r=5.4:7.8:0.2 mm. Both
seed55 rows again selected the true x=250 mm, z=90 mm, r=6.0 mm. The
source-mismatch seed55 row remains the weakest observed source-shape result at
1.006e-04 against r=6.2, but the dense z=91 mm / r=6.8-7.0 mm branch stayed at
ranks 3-4 and did not become a near-tie. This closes the seed55 radius-grid
follow-up; update the synthesis and then move to coupled-neighbor geometry or a
different physics lever.
Experiment 439 updated the source-shape synthesis with experiments 436-438.
Across 48 rows from experiments 425-434 and 436-438, every row selected the
true target x/z/r geometry. The weakest row remains center
source_mismatch_ringdown025_noise10_seed55, with radius_margin_abs=1.006e-04
against r=6.2 at true x/z. The dense seed55 figure confirms that the z=91 mm /
r=6.8-7.0 mm branch remains secondary. Fixed-neighbor source-shape replication
is now sufficiently covered; the next meaningful step is coupled-neighbor
geometry development or a different explicit physics stress.
Experiment 440 added that first coupled-neighbor source-shape coordinate test.
The coordinate optimizer now supports `--fit-ringdown-coefficient` and reports
ringdown coefficient fields in confidence/objective diagnostics. The run
started all three radii at 6.2 mm, updated center, left, and right in one
compact sequential pass, and recovered the exact true final state
x=[150,250,350] mm, z=[90,90,90] mm, r=[6,6,6] mm. Margins were weak but
positive: 1.228e-04 for the center, 2.948e-04 for the left, and 2.185e-04 for
the right, with all ambiguity intervals limited to r=6.0-6.2 mm at true x/z.
The fitted nuisance source recovered fc=1.1, shift=-50 ps, and ringdown about
0.25 in every step. This is a correct first coupled pass, but not yet a
high-confidence radius claim. Next, repeat from a harder x/z/r perturbed seed
before spending GPU time on dense coupled sweeps.
Experiment 441 ran that harder coupled x/z/r-perturbed pass. The initial state
was x=[149,251,349] mm, z=[91,89,91] mm, r=[6.2,5.8,6.2] mm, and the update
order again corrected center, left, then right. The final state was exact truth
x=[150,250,350] mm, z=[90,90,90] mm, r=[6,6,6] mm. The center correction was
strong with margin 1.346e-03 even though both neighbors were initially wrong;
left and right remained point-correct but weak, with margins 3.283e-04 and
2.185e-04 and local 6.0-6.2 mm radius intervals. Experiment 442 aggregated
runs 440-441: 6/6 coupled rows are true geometry, no row has x/z ambiguity,
five rows are weak, one row is strong, and the maximum radius ambiguity width
is 0.2 mm. The next coupled source-shape step should be one independent
seed/order replication or a two-pass compact check; dense coupled Stage 4C
sweeps should still wait.
Experiment 443 ran the independent seed/order replication: initial
x=[151,249,351] mm, z=[89,91,89] mm, r=[5.8,6.2,5.8] mm, updating right,
center, then left. It also recovered the exact true final state. The right row
was moderate with margin 8.522e-04, the center row was weak with margin
4.022e-04, and the left row was strong with margin 1.399e-03. Experiment 444
aggregated runs 440, 441, and 443: all 9 coupled rows are true geometry, there
is no x ambiguity, and the maximum remaining z/r ambiguity is 1.0 mm and
0.4 mm. The next GPU branch should be a two-pass compact check from the harder
reversed-order seed before any dense coupled sweep.
Experiment 445 ran that two-pass compact check from the reversed-order seed.
Pass 0 reproduced experiment 443 exactly enough for the decision: right,
center, and left all corrected to truth. Pass 1 started from the true state and
kept all targets at truth, so the coupled coordinate update is point-stable.
The second pass did not remove the weak radius evidence: target 2 margin was
2.185e-04, target 1 margin was the branch minimum 1.006e-04, and target 0
margin was 3.456e-04, all against nearby radius alternatives. Experiment 446
aggregated all coupled source-shape coordinate rows from 440, 441, 443, and
445. Across 15 rows, every row is true geometry, no row has x ambiguity, 10
rows are weak, 2 are moderate, and 3 are strong. The branch should avoid dense
coupled Stage 4C sweeps for now; if source-shape work continues, target the
true-state r=6.0 versus r=6.2 ambiguity directly with a narrow refinement or
objective diagnostic. Experiments 447-448 completed that narrow true-state
diagnostic for the weakest center row. Base again selected x=250 mm, z=90 mm,
r=6.0 mm over r=6.2 mm by 1.006e-04. Highband preserved the same true geometry
and raised the absolute gap by only 1.139x to 1.146e-04. This is useful
diagnostic support but does not collapse the 6.0-6.2 mm ambiguity interval, so
the source-shape branch should remain interval-supported unless a new physics
or objective lever changes the evidence. Experiment 53 tested the nearest
material lever with a multi-rebar material-profiled radius runner. A CPU smoke
validated the new reporting path, then run 450 profiled the center true-state
radius over r=5.8/6.0/6.2 mm, concrete epsr=5.8/6.0/6.2, and steel
conductivity 1e5/1e7 S/m under the same source-mismatch/ringdown/noise case.
The best row still used concrete epsr=6.0 and r=6.0 mm; steel conductivity was
saturated, with 1e5 and 1e7 nearly tied. The material-profiled margin against
r=6.2 was 1.019e-04, essentially unchanged from experiment 447. Therefore free
material parameters should not be added to this production branch, and the
weak center-radius result should stay reported as a 6.0-6.2 mm interval.
Experiment 54 opened the next staged geometry branch by combining variable
depth and variable radius in one detector/assignment case:
x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm under source mismatch and
10% noise. Run 451's detector found all three truths within tolerance; ranks
1-3 were the physical center, left, and right seeds, while ranks 4-5 were
false shallow aliases. Run 452's assignment policy selected the physical
three-seed set and rejected the duplicate center alias. Run 453 packaged a
dry-run coordinate-FWI command with per-target truth radii and broad ambiguity
guards. The full broad radius command was deliberately not launched. The next
GPU step should be a bounded location-only x/z coordinate stage with radii
fixed at [6,6,6] mm, followed by focused radius refinement only after the
location stage is interpreted.
Runs 454-457 completed that staged follow-up. Run 455's location-only
coordinate step refined the assigned seeds to x/z errors of 1.41 mm, 0.00 mm,
and 1.00 mm while radii were fixed at [6,6,6] mm, and base/highband objectives
agreed on all three basins. Run 456 then recovered the right/deep radius
r=8 mm and kept the center r=6 mm; run 457 repeated the radius pass from
[6,6,8] and confirmed center/right stability. The left target still preferred
r=6.0 mm, but the target-0 revisit margin collapsed to 8.431e-05 against
r=5.75 mm, with highband giving a similarly tiny 6.994e-05 gap. Therefore the
branch should report left radius as a weak 5.5-6.0 mm interval rather than a
point-correct 5 mm recovery, and the broad all-parameter command should remain
deferred until a bounded target-0 diagnostic or acquisition/objective lever
changes that evidence.
Run 458 tested the first bounded acquisition lever for that left-target
ambiguity by profiling target 0 only with seven source positions and a
4.5-6.25 mm radius grid while keeping the 455/457 x/z and center/right radii
fixed. The main 7-source row still selected r=6.0 mm with a weak
3.888e-04 gap, and the fine revisit moved the best point to r=5.875 mm with a
weak 3.550e-04 gap against r=6.0 mm. Highband agreed with the 5.875 mm revisit
best point, but the true r=5.0 mm candidate remained only rank 6 in the main
objective. Extra source count alone therefore improves the interval but does
not solve the shallow-left radius recovery. The next bounded diagnostic should
test target-0 local x/z-radius coupling around the residual 1 mm location
error before trying broader acquisition changes or launching the dry-run
all-parameter command.
Run 459 then tested that local x/z-radius coupling directly with five sources:
target 0 was allowed to move over x=149-150 mm, z=80-81 mm, and
r=5.0-6.25 mm while center/right stayed fixed at r=[6,8] mm. The main row and
the fine revisit both recovered the true local point x=150 mm, z=80 mm,
r=5.0 mm. The update-case margin was 5.104e-04 against nearby 5.125-5.25 mm
radii, and highband agreed with a 4.453e-04 gap. The target-0 failure mode was
therefore residual x/z-radius coupling, not a need for the broad 453
all-parameter search. The staged final state is now x=[150,250,349] mm,
z=[80,100,120] mm, r=[5,6,8] mm. The next cheapest closure step is a tiny
target-2 x polish over x=349-350 mm with z/r fixed, after which the branch can
be summarized with intervals.
Run 460 completed that closure step. With x=[150,250,349] mm,
z=[80,100,120] mm, and r=[5,6,8] mm as the initial state, target 2 was profiled
only over x=349-350 mm with z/r fixed. Base and highband both selected
x=350 mm, z=120 mm, r=8 mm; the update-case base gap against x=349 mm was
2.672e-03, and the highband gap was 2.421e-03. The staged variable-depth /
variable-radius path therefore reaches the exact truth tuple for this
source-mismatch/noise seed. The result should be promoted as a staged
procedure with interval reporting, not as evidence that the broad all-parameter
command is necessary. Next build a CPU summary artifact for runs 451-460 and
then replicate the staged policy on one new seed before making a branch-level
claim.
Run 461 packaged that CPU summary artifact with the existing coordinate
confidence aggregate tool. Across the coordinate summaries 455-460 it records
30 confidence rows: 8 missing, 8 weak, 3 moderate, and 11 strong, with a
minimum radius margin of 8.431e-05 and maximum x/z/r ambiguity widths of
2.0/1.0/0.75 mm. Because the aggregate includes intermediate staged rows, the
11 truth-geometry rows are a diagnostic ledger rather than a final-success
denominator. It confirms that the weak evidence is concentrated on target 0
before the local x/z-radius coupling stage, while center/right focused rows are
stable. The next GPU step should replicate the staged policy on one new noise
seed, still avoiding the broad all-parameter command.
Runs 462-470 completed that seed replication with noise seed 34. The detector
again found all truths within tolerance and assignment selected the physical
left/center/right seeds, but the left detector seed was 10 mm shallow, so the
coordinate stage used target-specific z windows. Runs 464-466 corrected the
location state to x=[150,250,350] mm, z=[81,100,119] mm with radii fixed at
[6,6,6] mm. The radius-only pass then confirmed center r=6 mm but left target
0 at z=81/r=6 and right target 2 at z=119/r=7.25, exposing the same z/r
coupling mechanism as seed13. Run 468 locally coupled target 2 and recovered
z=120 mm, r=8 mm; run 469 locally coupled target 0 and recovered z=80 mm,
r=5 mm. The final seed34 staged tuple is exact truth, but the fine confidence
margins are weaker: the target-2 revisit gap is 1.424e-04 against r=7.875,
and the target-0 revisit gap is 3.571e-04 against r=5.125. Run 470 aggregated
seed34 coordinate confidence rows: 22 rows, 11 truth-geometry rows, 10 weak
rows, 3 moderate rows, 3 strong rows, and minimum radius margin 5.575e-05.
The next CPU step should build a combined seed13/seed34 summary before
deciding whether a harder seed55 replication is needed.
Run 471 built that combined seed13/seed34 coordinate confidence summary. Across
52 coordinate rows it records 22 truth-geometry rows, 18 weak rows, 6 moderate
rows, 14 strong rows, and 14 missing-radius rows from location/fixed-radius
steps. The combined minimum radius margin remains the seed34 target-2 fine
revisit margin, 5.575e-05, and the maximum x/z/r ambiguity widths are
2.0/1.0/1.0 mm. This is the current two-seed evidence package: exact staged
final geometry for seeds 13 and 34, with explicit weak fine-radius intervals
on target 0 and target 2. The next bounded step should be a seed55 detector
gate before deciding whether full seed55 staged replication is worth the GPU
time.
Runs 472-481 completed that seed55 replication and the three-seed staged
coordinate package. The detector again found all three physical truths within
tolerance, assignment selected the physical left/center/right seeds, and
location/radius/focused-coupling stages reached the exact truth tuple
x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm. Run 480 summarized seed55
with 16 rows, 7 truth-geometry rows, 6 missing rows, 3 weak rows, 2 moderate
rows, and 5 strong rows. Run 481 combined seed13, seed34, and seed55 into the
current staged-coordinate evidence package: 68 rows, 29 truth-geometry rows,
20 missing rows, 21 weak rows, 8 moderate rows, 19 strong rows, minimum radius
margin 5.575e-05, and maximum x/z/r ambiguity widths of 2.0/1.0/1.0 mm. The
staged policy is replicated across three seeds, but final target-0 and target-2
radius rows still need interval reporting.
Runs 482-484 tested whether adding source count alone collapses those
final-state intervals on seed55. Seven sources modestly improved target-0
source-mismatch separation to 6.572e-04, but target 2 still retained the
z=119-120 mm and r=7.25-8.0 mm interval. Run 484 aggregated the two seven-source
checks: 4/4 truth rows, weak=2, moderate=2, minimum margin 3.660e-04, and
maximum z/r ambiguity widths of 1.0/1.0 mm. Source count alone is therefore
not the default interval-collapse lever.
Runs 485-487 tested Tx/Rx=35 mm on the same seed55 final-state intervals. The
offset narrowed target 0 to z=80 mm and r=5.0-5.25 mm and collapsed the
target-2 source-mismatch row to z=120 mm, r=8.0 mm, while the clean target-2
row still carried z=119-120 mm and r=7.25-8.0 mm. Run 487 aggregated 4/4 truth
rows, weak=3, moderate=1, minimum margin 2.414e-04, and max z/r ambiguity
widths of 1.0/0.75 mm. Tx/Rx geometry is more effective than source count, but
35 mm is not enough to collapse both targets under both rows.
Runs 488-490 raised that geometry lever to Tx/Rx=50 mm on seed55. Target 0
kept an exact point estimate and collapsed the source-mismatch row to
z=80 mm, r=5.0 mm, while the clean row stayed at r=5.0-5.25 mm. Target 2
collapsed both rows to z=120 mm, r=8.0 mm. Run 490 aggregated 4/4 truth rows,
weak=3, moderate=1, minimum margin 1.922e-04, zero z ambiguity, and maximum
radius ambiguity width 0.25 mm. This made Tx/Rx=50 mm the best seed55
acquisition geometry tested, pending seed replication.
Runs 491-494 completed that Tx/Rx=50 mm seed replication on seed34 and packaged
the combined acquisition summary. Seed34 target 0 stayed point-correct with
z=80 mm and r=5.0 mm but retained a 5.0-5.25 mm radius interval in both rows;
seed34 target 2 collapsed both rows to z=120 mm, r=8.0 mm, with the
source-mismatch row moderate at 7.536e-04. Run 493 summarized seed34 alone:
4/4 truth rows, weak=3, moderate=1, minimum margin 2.541e-04, zero x/z
ambiguity, and maximum radius ambiguity width 0.25 mm. Run 494 combined seed34
and seed55: 8/8 truth rows, weak=6, moderate=2, minimum margin 1.922e-04, zero
x/z ambiguity, and maximum radius ambiguity width 0.25 mm. Tx/Rx=50 mm should
now be treated as the leading tested acquisition geometry for final-state
interval narrowing, but not as strong point-radius evidence. The next bounded
step is either seed13 Tx/Rx=50 replication for a three-seed acquisition package
or a weighted/high-frequency objective aimed at the residual target-0
5.0-5.25 mm interval.
Runs 495-498 completed that seed13 Tx/Rx=50 replication and closed the
three-seed acquisition package. Seed13 target 0 was exact at x=150 mm,
z=80 mm, r=5.0 mm but weak in both rows, with a 5.0-5.25 mm interval. Seed13
target 2 was exact at x=350 mm, z=120 mm, r=8.0 mm; the clean row was weak and
the source-mismatch row was moderate with a 5.634e-04 gap. Run 497 summarized
seed13 alone with 4/4 truth rows, weak=3, moderate=1, minimum margin
1.884e-04, zero x/z ambiguity, and maximum radius ambiguity width 0.25 mm.
Run 498 combined seeds 13, 34, and 55: 12/12 truth rows, weak=9, moderate=3,
minimum margin 1.884e-04, zero x/z ambiguity, and maximum radius ambiguity
width 0.25 mm. This closes scalar source-count and Tx/Rx geometry escalation
for the branch for now. The next meaningful GPU step should hold Tx/Rx=50 mm
fixed and test an objective lever aimed at the residual target-0 5.0-5.25 mm
interval.
Runs 499-502 tested that objective lever without changing acquisition geometry.
Run 499 reused the final truth state, Tx/Rx=50 mm, target 0, and six seed/case
rows, then compared base, highband, late, late_high, veryhigh, and early_high
objectives from the same 12-candidate grid. The veryhigh objective
(1.8-4.2 GHz over the 1.0-7.0 ns window) kept all six target-0 rows at truth,
raised the mean radius margin from 2.896e-04 to 4.856e-04, improved the
best-vs-next gap by 1.512-2.303x, and collapsed the veryhigh diagnostic
ambiguity interval to z=80 mm, r=5.0 mm in all rows. Run 500 packaged the
target-0 objective ratio report and showed veryhigh was the only tested
objective with a consistent margin improvement.
Run 501 repeated the objective guardrail on target 2. Veryhigh again kept all
six rows at truth, raised the mean radius margin from 4.966e-04 to 8.950e-04,
made all six rows moderate-or-better, and collapsed all veryhigh intervals to
z=120 mm, r=8.0 mm. Run 502 combined target 0 and target 2: veryhigh preserved
12/12 truth rows, had zero geometry changes, and reached a mean margin ratio
of 1.831. This is the first objective-level result that improves final-state
radius evidence after Tx/Rx=50 mm. It should remain diagnostic/reporting
evidence until objective-specific confidence rows or a center-target guardrail
are added.
Run 503 updated the objective diagnostic reporting layer so it also writes
objective-specific confidence and ambiguity rows from saved per-step
objective_results. Focused tests for the report pass. Re-running the combined
target-0/target-2 report records the base objective as 12/12 truth rows with
weak=9, moderate=3, and max radius ambiguity 0.25 mm. The veryhigh objective
records 12/12 truth rows with weak=4, moderate=6, strong=2, minimum/mean/maximum
margin 3.400e-04/6.903e-04/1.132e-03, and zero x/z/r ambiguity width. This
makes veryhigh a concrete reporting diagnostic for Tx/Rx=50 final-state target
0 and target 2. Before any global objective update, run the same guardrail on
the center target.
Runs 504-505 completed that center-target guardrail and the all-target
objective report. Run 504 used target 1 with x fixed, z=99-101 mm, r=5.0-7.0 mm
in 0.25 mm steps, all three seeds, and the same objective variants. The base
rows were all exact but weak, with mean margin 3.404e-04 and max radius
ambiguity 0.25 mm. Veryhigh kept all six center rows exact, raised the mean
margin to 5.734e-04, made 5/6 rows moderate-or-better, and collapsed ambiguity
widths to zero. Run 505 combined targets 0, 1, and 2: base has 18/18 truth rows
with weak=15, moderate=3, and max radius ambiguity 0.25 mm; veryhigh has
18/18 truth rows with weak=5, moderate=11, strong=2, mean margin 6.513e-04,
mean margin ratio 1.803, and zero x/z/r ambiguity width. This closes the
all-target veryhigh guardrail as diagnostic/reporting evidence.
Runs 506-507 tested whether that veryhigh objective transfers to the older
source-shape/ringdown center-radius interval. The setup repeats run 447:
same-depth x=[150,250,350] mm, z=[90,90,90] mm, r=[6,6,6] mm,
source_mismatch_ringdown025_noise10_seed55, fitted ringdown coefficient, target
1 only, x/z fixed, and radius 5.6-6.4 mm. Veryhigh preserved the correct
geometry but reduced the absolute margin from the base 1.006e-04 to
6.388e-05. Late_high was the best tested variant at 1.632e-04, a 1.622x ratio,
but still weak. Run 507's confidence report keeps every objective row weak.
Therefore the variable-depth veryhigh result is branch-specific; do not
promote it globally to source-shape/ringdown cases, and keep the source-shape
center radius as a 6.0-6.2 mm interval.
Runs 508-514 then started the branch-specific ringdown guardrail for the newer
variable-depth/variable-radius Tx/Rx=50 mm final state. Run 508 used target 0,
the true final tuple x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm, the
source_mismatch_ringdown025_noise10_seed55 row, fitted source primary and
ringdown coefficients, and the same six diagnostic objectives. The base update
remained exact at x=150 mm, z=80 mm, r=5 mm, reached a moderate 6.012e-04 gap
against r=5.25 mm, and collapsed the ambiguity interval to the single true
point. The fitted direct ringdown scale was 0.2503, close to the injected 0.25
stress. Run 509's objective confidence report shows every diagnostic variant
kept the truth geometry; veryhigh was the best target-0 diagnostic for this
branch, with a 7.714e-04 absolute margin and 1.283x ratio to base, while late
and late_high weakened the margin. Runs 510-511 replicated the same
fitted-ringdown stress on target 2 with z=119-120 mm and r=7.0-8.0 mm. The
base row again recovered exact truth with a moderate 9.585e-04 margin and a
single-point ambiguity interval; late_high was the best objective at
1.494e-03 and 1.559x, while veryhigh remained strong at 1.245e-03 and 1.299x.
Runs 512-513 closed the seed55 target-1 guardrail over z=99-101 mm and
r=5.0-7.0 mm. The base row stayed exact with a moderate 6.209e-04 margin,
late_high was best at 8.189e-04 and 1.319x, and veryhigh was only mildly
helpful at 6.572e-04 and 1.058x. Run 514 combined all three target summaries:
base has 3/3 exact moderate rows with zero ambiguity width, all diagnostic
variants preserve truth geometry, and veryhigh is the only variant with margin
ratio above 1.0 on every target, with ratio min/mean/max
1.058/1.213/1.299. This supports branch-specific reporting evidence under one
seed55 fitted-ringdown stress, but the next guardrail should replicate the
stress on another seed before any production update-rule change.
Runs 515-520 started that seed replication with target 0 on seed13, using the
same Tx/Rx=50 mm final state, fitted ringdown source model, and 12-candidate
z/r window as run 508. Run 515 stayed exact at x=150 mm, z=80 mm, r=5 mm, but
the base margin was weak at 4.836e-04. The fitted direct ringdown scale was
0.2490, again close to the injected 0.25. Run 516 showed veryhigh was the only
diagnostic variant that improved the seed13 target-0 margin, raising it to
6.397e-04 and a moderate label with a 1.323x ratio. Run 517 combined seed13
and seed55 target-0 ringdown rows: both are truth geometry, base has one weak
and one moderate row, and veryhigh has two moderate rows with ratio
min/mean/max 1.283/1.303/1.323. Runs 518-519 then repeated target 0 on seed34:
the base row was exact and moderate with a 5.476e-04 margin, and veryhigh was
again the only improving diagnostic at 6.928e-04 and 1.265x. Run 520 closed the
three-seed target-0 ringdown report: base is exact with weak=1/moderate=2,
veryhigh is exact with moderate=3, and veryhigh is the only objective with
consistent margin improvement, ratio min/mean/max 1.265/1.290/1.323. The next
bounded replication should move to target 2, starting with seed13.
Runs 521-522 then ran that target-2 seed13 replication with the same fitted
ringdown source model and the z=119-120 mm, r=7.0-8.0 mm guardrail used for
seed55. The base row stayed exact at x=350 mm, z=120 mm, r=8 mm with a
moderate 8.106e-04 margin and zero ambiguity width. Late_high remained the
best diagnostic at 1.310e-03 and 1.616x, late was 1.203e-03 and 1.484x, and
veryhigh was also strong at 1.137e-03 and 1.403x. The next bounded run should
repeat target 2 on seed34 to complete the three-seed target-2 ringdown package.
Runs 523-525 completed that target-2 replication. Seed34 target 2 stayed exact
with a strong base margin of 1.040e-03, fitted direct ringdown 0.2509, and
late_high again strongest at 1.715e-03 and 1.649x. Run 525 combined seed13,
seed34, and seed55 target-2 rows: all three are exact, base is moderate=2 and
strong=1, late/late_high/veryhigh are strong on all rows, and late_high has
ratio min/mean/max 1.559/1.608/1.649. The remaining fitted-ringdown seed
replication target is target 1, starting with seed13 despite its heavier
27-candidate grid.
Runs 526-527 started that target-1 seed replication on seed13. The center grid
used z=99-101 mm and r=5.0-7.0 mm, so it cost 874.9 s. The base row stayed
exact at x=250 mm, z=100 mm, r=6 mm with a moderate 6.009e-04 margin and zero
ambiguity width. Late_high was the strongest diagnostic at 7.513e-04 and
1.250x, late was 7.182e-04 and 1.195x, and veryhigh was mildly helpful at
6.596e-04 and 1.098x. The final bounded replication needed for a complete
three-seed ringdown package is target 1 on seed34.
Runs 528-531 completed that package. Run 528 repeated target 1 on seed34 and
stayed exact/moderate at x=250 mm, z=100 mm, r=6 mm with base margin
6.002e-04, fitted direct ringdown 0.2509, late_high margin 8.663e-04 and
1.443x, and veryhigh margin 6.444e-04 and 1.074x. Run 530 combined seed13,
seed34, and seed55 target-1 rows: all three are exact/moderate, late_high
improves every row with ratio 1.250-1.443, and veryhigh also improves every
row but only mildly at 1.058-1.098. Run 531 combined all targets and all three
seeds under the fitted-ringdown stress. All nine target/seed rows stay exact;
base labels are weak=1, moderate=7, strong=1; veryhigh is the only tested
objective with ratio above 1.0 on every row, ratio min/mean/max
1.058/1.231/1.403, labels moderate=6 and strong=3, and zero ambiguity width.
Late_high has a comparable mean ratio at 1.190 and is strongest on targets 1
and 2, but it weakens all target-0 rows. The branch-level conclusion is
therefore conservative: veryhigh is useful reporting evidence for the
variable-depth/variable-radius Tx/Rx=50 fitted-ringdown package, not a global
production update-rule replacement.
Run 532 then combined the non-ringdown Tx/Rx=50 objective packages from runs
499, 504, and 501 with the fitted-ringdown target/seed packages from runs 515,
518, 508, 526, 528, 512, 521, 523, and 510. The CPU-only report spans 27
coordinate-confidence rows. Every diagnostic objective preserves truth
geometry, but veryhigh is the only objective with ratio above 1.0 on every row,
with ratio min/mean/max 1.058/1.612/2.563. Objective-confidence labels improve
from base weak=16/moderate=10/strong=1 and max radius ambiguity 0.25 mm to
veryhigh weak=5/moderate=17/strong=5 and zero x/z/r ambiguity. This makes
veryhigh the branch-level reporting diagnostic for the Tx/Rx=50
variable-depth/variable-radius final-state package, while the base objective
remains the production coordinate update rule.
Run 533 packages that decision as a lightweight handoff artifact:
`outputs/experiments/533_variable_depth_radius_txrx50_objective_reporting_handoff`.
The artifact records base as the production coordinate-update objective,
veryhigh as the branch-level reporting diagnostic, and global veryhigh
promotion as rejected because experiment 62 failed the source-shape transfer
check. Future reports for this branch should show base-update coordinates
first and then include veryhigh confidence rows; if the two objectives ever
select different geometry, report the conflict and run a targeted guardrail
instead of treating the veryhigh margin as stronger evidence.
Run 534 closed the close50 acquisition-metadata warning without rerunning GPU
work. `run_coordinate_confidence_aggregate.py` now has an explicit
`--default-missing-tx-rx-offset-mm` option for legacy summaries that predate
`tx_rx_offset_mm`; filled rows are marked with `tx_rx_offset_inferred=True`
and `tx_rx_offset_source=default_missing`. The repaired run 273 comparison is
packaged as run 534. Its default-offset rows are labelled Tx/Rx=20 mm filled
default and still show the original limitation, 1/2 truth rows with one
1 mm x-ambiguity row, while the explicit Tx/Rx=40 mm rows remain 6/6 truth
with zero x ambiguity.
Run 535 packages the same-depth source-shape center-radius reporting decision.
The source-shape center target should be reported as r=6.0-6.2 mm rather than
as a high-precision point radius. The base row from run 506 is truth-geometry
correct but weak with margin 1.006e-04 and ambiguity 6.0-6.2 mm; late_high from
run 507 is the best tested diagnostic at 1.632e-04 and 1.622x but remains weak;
veryhigh preserves truth geometry but worsens the margin to 6.388e-05 and
0.635x. This run is the compact citation for keeping veryhigh branch-specific
and avoiding dense coupled source-shape sweeps under the current objective set.
Run 536 packages the shallow single-rebar r=4 mm reporting decision. The
nominal high-band point estimate is r=4.0 mm, but material/source profiling
shifts the best reporting radius to 4.05 mm. The packaged material/source-aware
interval is 3.95-4.05 mm, while the broader fine-grid diagnostic interval from
run 197 is about 3.925-4.100 mm. The r=8 control remains point-stable at
8.0 mm with only an upper-side nuisance interval, 8.0-8.05 mm. Therefore
shallow/small-radius reports should show the nominal point estimate plus a
nuisance-aware interval when material/source calibration is not independently
bounded.
Run 537 is the recovery checkpoint for the resumed marathon. It summarizes
runs 528-536, records the latest validation state (focused aggregate tests
6 passed, full suite 255 passed, `git diff --check` clean), and keeps the next
decision conservative: no GPU run is queued unless the handoff matrix exposes a
new concrete physics gap.
Run 538 packages the current evidence synthesis. Its strongest claims are the
replicated variable-depth/radius staged recovery, Tx/Rx=50 mm as the leading
tested interval-narrowing geometry for that branch, veryhigh as a branch-level
reporting diagnostic rather than an update rule, fitted-ringdown exactness
under the tested stress, and interval reporting for source-shape center and
shallow r=4 cases. It also records the main non-claims: no universal
high-precision radius recovery, no global veryhigh promotion, no free material
parameters in the default optimizer, and no broad all-parameter/dense coupled
source-shape sweeps under the current evidence.
Run 539 turns that synthesis into a concise results-section draft. It is stored
at `outputs/experiments/539_results_section_draft/results_section_draft.md` and
is intended as a paper/report seed, not a new experiment.
Run 540 adds a compact methods paragraph and evidence table to support that
draft. It is stored at
`outputs/experiments/540_results_methods_evidence_table/methods_and_evidence_table.md`.
Run 541 combines the results draft and methods/evidence table into a single
compact report draft at `outputs/experiments/541_combined_report_draft/report_draft.md`.
Run 542 maps that draft to existing decision-grade figures so new plots are not
generated before reviewing whether the current artifacts already support the
claims.
Run 543 packages a compact objective summary figure for report layout. It
replaces or augments the ultra-wide run 532 diagnostic plot with a two-panel
summary across runs 505, 531, and 532: veryhigh margin ratios remain above 1.0
in every selected row, weak labels decrease, moderate/strong labels increase,
and geometry changes remain zero. The figure is layout support for the existing
decision, not a promotion of veryhigh to a global production update rule.
Run 544 audits the mapped decision figures for report readiness. It checks 11
PNG files from runs 498, 543, 531, 507, 201, and 534. Ten are report-ready
candidates with full dynamic range, and the only layout flag is the too-wide
run 531 fitted-ringdown objective detail plot. Because run 543 now carries the
objective-summary slot, no additional compact figure is queued.
Run 545 assembles the report figure caption package. It symlinks the selected
primary figures from runs 498, 543, 507, 201, and 534, keeps the run 531
fitted-ringdown objective plot as a supplementary audit figure, and records
captions with explicit guardrails against global veryhigh promotion and
unqualified high-precision radius claims.
Run 546 audits the report draft, caption package, handoff matrix, and master
plan for claim consistency. It finds no conflicts in run numbers, row counts,
interval claims, objective scope, or non-claims, so the reporting branch can
move to final bundle packaging without a new GPU experiment.
Run 547 packages that final reporting bundle as a symlinked index over the
report draft, figure/caption package, figure-readiness audit, claim audit,
evidence synthesis, handoff matrix, and master plan. It records the current
validation state and keeps the next decision conservative: use the bundle for
report assembly, with no GPU experiment queued.
Run 548 assembles the final Markdown report from the reporting bundle. It
embeds the selected run 545 figures through run 547 symlinks, preserves the run
546 claim boundaries, and is intended for manuscript editing or formatting
rather than new experiment interpretation.
Run 549 lints the final report. It verifies that all 42 referenced run IDs have
numbered output folders, all seven embedded figure paths resolve through the
run 547 bundle, and no TODO/FIXME/TBD/XXX markers remain.
Run 550 records the archive status checkpoint after the final report lint. Full
tests pass at 255/255, GPU utilization is low, RAM headroom is high, and the
next decision remains reporting/archive work rather than a new GPU sweep.
Run 551 records a commit/archive inventory for the dirty worktree. It separates
the code/test edits, research trackers, planning docs, and ignored output
artifacts so cleanup or commit preparation can be done deliberately.
Run 552 hardens objective diagnostic figure-note generation after code
self-review. Missing optional numeric values are printed as `not_recorded`
instead of risking a formatting exception, and the full suite passes at
257/257.
Run 553 records the post-hardening resume checkpoint. It supersedes run 550 as
the current restart point, with focused objective tests and the full suite
passing and no GPU experiment queued.
Run 554 audits the output folders needed by the final report and latest
reporting checkpoints. All 48 referenced folders exist and the dependency set
is only 9.244 MiB, so an explicit report archive would be low-risk if requested.
Run 555 creates that report dependency archive from an explicit 89-path file
list. The compressed archive is 4.0M, contains 466 entries, and has SHA-256
c5560c13846b501f0c3e67c8dd4b895baa90c2863036cbec27181b15703d5de0.
Run 556 records the post-archive resume checkpoint. It is the current restart
point after archive creation, with the validated archive recorded and no GPU
experiment queued.
Run 557 drafts a commit/PR summary for review. It separates runtime code/tests,
research and reporting docs, and ignored output archive handling; no commit is
made.
Run 558 records the next-action queue and no-GPU guardrails. Default work is
manuscript/archive/commit preparation; GPU runs remain gated on a concrete
bounded question.
Run 559 refreshes the final report reproducibility block so the manuscript
artifact cites the current run 556 checkpoint and run 555 archive rather than
the older run 547 validation state.
Run 560 lints the revised run 559 report and confirms that all run references
and embedded figures resolve and no unresolved editing markers remain.
Run 561 refreshes the next-action queue so manuscript editing points to the
current run 559 revised report while keeping GPU work gated on a concrete
bounded question.
Run 562 converts the validated report into an IMRAD-style manuscript draft
without changing the underlying evidence or claim boundaries.
Run 563 lints the IMRAD manuscript draft and confirms that all run references
and embedded figures resolve and no editing markers remain.
Run 564 records the post-IMRAD resume checkpoint. It supersedes run 556 as the
current restart point and keeps the next action on CPU/reporting work unless a
concrete bounded GPU question is selected.
Run 565 audits the IMRAD manuscript for section balance and explicit guardrail
phrases. The draft now states the key non-claims and interval rules directly
and passes the audit.
Run 566 refreshes the next-action queue so manuscript editing points to the run
562 IMRAD draft while GPU work remains gated.
Run 567 polishes manuscript guardrail prose, removes a duplicated limitations
phrase, and reruns the manuscript lint and balance audit.
Run 568 records the post-manuscript polish checkpoint. It supersedes run 564 as
the current restart point after the guardrail audit and prose polish, with no
GPU experiment queued.
Run 569 refreshes the next-action queue so future resumes point to run 568
while manuscript editing remains on the polished run 562 IMRAD draft and GPU
work remains gated.
Run 570 refreshes the commit/PR summary and current inventory through the
post-polish queue. It keeps runtime code/tests, tracked docs, and ignored
output artifacts separated for commit or archive decisions.
Run 571 hardens coordinate aggregate figure notes so missing ambiguity-width
values render as `not_recorded`. This is a reporting robustness change with
focused and full tests passing at 17/17 and 258/258.
Run 572 refreshes the commit/PR summary after run 571, making it the current
commit-preparation artifact for the code, tests, docs, and ignored output
artifacts.
Run 573 records the post-hardening resume checkpoint with focused/full tests
passing, low GPU/RAM pressure, and no queued GPU experiment.
Run 574 refreshes the next-action queue so future resumes point to run 573 and
commit preparation points to run 572.
Run 575 refreshes the IMRAD manuscript validation/data-availability state after
the post-hardening checkpoint. The manuscript lint now checks 51 referenced
runs, all embedded images resolve, and guardrails remain present.
Run 576 refreshes the next-action queue so manuscript editing points to the
run 562 draft with current validation in run 575, while commit preparation
points to run 572 and GPU work remains gated.
Run 577 refreshes the commit/PR summary and inventory after run 575 and is
maintained as the current commit-preparation artifact pointed to by run 581,
with current validation refreshed through run 582.
Run 578 refreshes the next-action queue so commit preparation points to run 577
while manuscript validation remains on run 575 and GPU work remains gated.
Run 579 audits the current handoff dependency set. It finds 115 dependency
paths, 351 files, zero missing paths, 13.7 MiB total size, and 36 current paths
not covered by the older run 555 archive, so a refreshed archive is justified.
Run 580 packages that current handoff archive. The archive has 116 input paths,
487 entries, is 7.9M compressed, and records its SHA-256 in run 580 metadata.
Run 581 refreshes the next-action queue so optional current archive handoff
points to run 580 while manuscript validation stays on run 575, commit
preparation stays on run 577, and GPU work remains gated.
Run 582 records the current pre-commit validation checkpoint: focused
objective/confidence tests pass at 17/17, the full suite passes at 258/258,
`git diff --check` is clean, and GPU/RAM pressure remains low.
Run 583 refreshes the next-action queue so local validation points to run 582
while run 580 remains the current packaged archive and GPU work remains gated.
Run 584 hardens objective confidence reporting for sparse saved objective
results. Rows without complete top-candidate geometry now emit missing
geometry/error fields and a false truth-geometry flag instead of raising a
conversion exception. Focused objective/confidence tests pass at 18/18, the
full suite passes at 259/259, and run 580 remains the current packaged archive.
Run 585 refreshes the next-action queue after run 584. It points local
validation to run 584, keeps run 580 as the current packaged archive, keeps run
577 as the current commit-preparation artifact, and keeps GPU work gated on a
concrete bounded question.
Run 586 refreshes the commit/PR summary after the sparse-result hardening. It
supersedes run 577 for commit preparation, expands the inventory through
docs/experiments/119 and outputs/experiments/586, and records the 18/18 focused
and 259/259 full test validation state.
Run 587 refreshes the next-action queue after run 586. It points commit
preparation to run 586, local validation to run 584, keeps run 580 as the
current packaged archive, and leaves GPU work gated on a concrete bounded
question.
Run 588 records the post-sparse-hardening resume checkpoint. It supersedes run
573 as the current restart point, points validation to run 584, commit
preparation to run 586, queue state to run 587, and records low GPU/RAM
pressure.
Run 589 refreshes the next-action queue after run 588. It points future resumes
to run 588, local validation to run 584, commit preparation to run 586, keeps
run 580 as the packaged archive, and leaves GPU work gated.
Run 590 audits the current post-sparse-hardening artifact state. Runs 584-589
have parseable manifests and no missing declared artifacts, docs/experiments
117-122 and infrastructure symlinks are present, the run 580 archive checksum
and 487-entry count remain stable, and no new bounded GPU question is exposed.
Run 591 refreshes the run 562 IMRAD manuscript reproducibility pointers to the
current run 584 validation, run 586 commit-preparation, run 588 resume, run 589
queue, and run 590 audit state. Structural lint passes with 54 referenced runs,
zero missing runs, seven resolved embedded figures, and all five guardrails
present.
Run 592 refreshes the commit/PR summary after the current manuscript validation
refresh. It supersedes run 586 for commit preparation, expands the inventory
through docs/experiments/124 and outputs/experiments/591, and records the
current 54-run manuscript validation plus 259/259 full-test state.
Run 593 refreshes the next-action queue after run 592. It points manuscript
validation to run 591, commit preparation to run 592, restart to run 588, local
code validation to run 584, keeps run 580 as the packaged archive, and leaves
GPU work gated.
Run 594 audits the current handoff dependency set after the manuscript
validation refresh. It finds 138 base dependency paths, 402 files, zero missing
paths, 21.6 MiB total size, and 27 paths not covered by the run 580 archive, so
a refreshed current handoff archive is justified.
Run 595 packages the refreshed current handoff archive. The archive has 139
input paths, 554 entries, is 16M compressed, includes the run 594 audit folder,
excludes the run 595 self folder, and has SHA-256
a55cbf6c6540223bdb01874ca51bb2ab1063057833006e06a318f66ce84be280.
Run 596 refreshes the commit/PR summary after the archive refresh. It
supersedes run 592 for commit preparation, expands the inventory through
docs/experiments/128 and outputs/experiments/595, and records run 595 as the
current handoff archive.
Run 597 refreshes the next-action queue after run 596. It points optional
archive handoff to run 595, commit preparation to run 596, manuscript
validation to run 591, restart to run 588, local code validation to run 584,
and leaves GPU work gated.
Run 598 records the current pre-commit validation state after the archive
refresh. Focused objective/confidence tests pass at 18/18, the full suite
passes at 259/259, `git diff --check` is clean, and GPU/RAM pressure remains
low.
Run 599 refreshes the next-action queue after run 598. It points local code
validation to run 598 while keeping archive handoff on run 595, commit
preparation on run 596, manuscript validation on run 591, restart on run 588,
and GPU work gated.
Run 600 refreshes the commit/PR summary after the current validation queue
refresh. It supersedes run 596 for commit preparation, expands the inventory
through docs/experiments/133 and outputs/experiments/600, and preserves run 595
as the current handoff archive.
Run 601 refreshes the next-action queue after run 600. It points commit
preparation to run 600 while keeping local code validation on run 598,
manuscript validation on run 591, archive handoff on run 595, restart on run
588, and GPU work gated.
Run 602 hardens objective diagnostic ratio and enrichment rows for missing
best-candidate geometry. Sparse diagnostic rows now record unavailable geometry
comparison instead of crashing or claiming a geometry change, with 19/19
focused objective/confidence tests and 260/260 full tests passing.
Run 603 refreshes the commit/PR summary after run 602. It supersedes run 600
for commit preparation, expands the inventory through docs/experiments/136 and
outputs/experiments/603, records the 260/260 full-test state, and keeps run 595
as the current packaged archive.
Run 604 refreshes the next-action queue after run 603. It points local code
validation to run 602, commit preparation to run 603, manuscript validation to
run 591, archive handoff to run 595, restart to run 588, and leaves GPU work
gated.
Run 605 audits the current post-diagnostic-hardening state. Runs 602-604 have
parseable manifests and no missing declared artifacts, docs/experiments 135-137
and infrastructure symlinks are present, the run 595 archive checksum and
554-entry count remain stable, and no stale current pointer is found.
Run 606 hardens optional numeric handling in coordinate aggregate and objective
diagnostic reporting. Malformed or non-finite optional metrics now degrade to
missing values for errors, summaries, labels, plots, and figure notes, with
21/21 focused objective/confidence tests and 262/262 full tests passing.
Run 607 refreshes the commit/PR summary after run 606. It supersedes run 603
for commit preparation, expands the inventory through docs/experiments/140 and
outputs/experiments/607, records the 262/262 full-test state, and keeps run 595
as the current packaged archive.
Run 608 refreshes the next-action queue after run 607. It points local code
validation to run 606, commit preparation to run 607, state audit to run 605,
manuscript validation to run 591, archive handoff to run 595, restart to run
588, and leaves GPU work gated.
Run 609 runs the real coordinate confidence aggregate CLI on a synthetic
malformed/non-finite optional-metric input. The CLI exits cleanly, writes CSV,
JSON, two PNG figures, and figure notes, aggregate statistics contain zero
non-finite numeric values, and both figures are nonblank at 1719 x 971 px.
Run 610 hardens objective diagnostic ratio serialization. Unavailable
base/variant margins and margin ratios now emit JSON null instead of numeric
NaN, with 21/21 focused objective/confidence tests and 262/262 full tests
passing.
Run 611 runs the real objective diagnostic CLI on a sparse/non-finite synthetic
input. The CLI exits cleanly, writes ratio and confidence CSVs, JSON, a PNG
figure, and figure notes, the generated report contains zero non-finite numeric
values, and unavailable geometry/margin-ratio fields are explicit null values.
Run 612 audits the current non-finite-hardening state. Runs 606-611 have
parseable manifests and no missing declared artifacts, docs/experiments 139-144
and infrastructure symlinks are present, the run 609 aggregate and run 611
report contain zero non-finite numeric values, and the run 595 archive checksum
and 554-entry count remain stable.
Run 613 refreshes the commit/PR summary after runs 609-612. It supersedes run
607 for commit preparation, expands the inventory through docs/experiments/146
and outputs/experiments/613, records the 262/262 full-test state plus both CLI
smokes, and keeps run 595 as the current packaged archive.
Run 614 refreshes the next-action queue after run 613. It points local code
validation to run 610, CLI smokes to runs 609 and 611, state audit to run 612,
commit preparation to run 613, manuscript validation to run 591, archive
handoff to run 595, restart to run 588, and leaves GPU work gated.
Run 615 audits the current handoff dependency set after the smoke/audit queue
refresh. It finds 180 base dependency paths, 507 files, zero missing paths,
38.1 MiB total size, and 41 paths not covered by the run 595 archive, so a
refreshed current handoff archive is justified.
Run 616 packages the refreshed current handoff archive. The archive has 181
input paths, 696 entries, is 32M compressed, includes the run 615 audit folder,
excludes the run 616 self folder, preserves the previous run 595 archive
folder, and has SHA-256
a88eaef65502afa60555c11ed7baa3876129161e4fc5cb7f7ce7d155cc5f7b98.
Run 617 refreshes the commit/PR summary after run 616. It supersedes run 613
for commit preparation, expands the inventory through docs/experiments/150 and
outputs/experiments/617, records run 616 as the current handoff archive, and
preserves the 262/262 full-test state.
Run 618 refreshes the next-action queue after run 617. It points archive
handoff to run 616, commit preparation to run 617, local validation to run 610,
CLI smokes to runs 609 and 611, state audit to run 612, manuscript validation
to run 591, restart to run 588, and leaves GPU work gated.
Run 619 refreshes the run 562 IMRAD manuscript validation/archive pointers to
the current run 610-618 smoke, audit, commit, queue, and archive state.
Structural lint passes with 50 referenced runs, zero missing runs, seven
resolved embedded figures, and all five guardrails present.
Run 620 refreshes the commit/PR summary after run 619. It supersedes run 617
for commit preparation, expands the inventory through docs/experiments/153 and
outputs/experiments/620, records run 619 as the current manuscript validation
artifact, and preserves run 616 as the current packaged archive.
Run 621 refreshes the next-action queue after run 620. It points manuscript
validation to run 619, commit preparation to run 620, archive handoff to run
616, local validation to run 610, CLI smokes to runs 609 and 611, state audit
to run 612, restart to run 588, and leaves GPU work gated.
Run 622 audits the current handoff dependency set after the manuscript
validation refresh. It finds 194 base dependency paths, 540 files, zero missing
paths, 69.9 MiB total size, 13 paths not covered by run 616, 37 files missing
from run 616, and four changed files including the run 562 manuscript draft, so
a refreshed current handoff archive is justified.
Run 623 packages the refreshed current handoff archive. The archive has 195
input paths, 742 entries, is 64M compressed, includes the run 622 audit folder
and updated run 562 manuscript draft, excludes the run 623 self folder,
preserves the previous run 616 archive folder, and has SHA-256
d60e899a45b3528d773b9125a0654686f0554bb8bdf6f2e6b02b7d3c24cbcc18.
Run 624 refreshes the commit/PR summary after run 623. It supersedes run 620
for commit preparation, expands the inventory through docs/experiments/157 and
outputs/experiments/624, records run 623 as the current handoff archive, and
preserves run 619 as the current manuscript validation artifact.
Run 625 refreshes the next-action queue after run 624. It points archive
handoff to run 623, commit preparation to run 624, manuscript validation to run
619, local validation to run 610, CLI smokes to runs 609 and 611, state audit
to run 612, restart to run 588, and leaves GPU work gated.

Stage 11DC: post-manuscript-archive resume checkpoint.

Run 626 records the current restart checkpoint after the manuscript-aware
archive and queue refreshes. It supersedes run 588 as the active restart point,
keeps archive handoff on run 623, commit preparation on run 624, manuscript
validation on run 619, local code validation on run 610, CLI smokes on runs
609 and 611, state audit on run 612, and leaves GPU work gated.

Stage 11DD: commit summary current resume refresh.

Run 627 refreshes the commit/PR summary after run 626. It supersedes run 624
for commit preparation, records run 626 as the current restart checkpoint,
keeps archive handoff on run 623, manuscript validation on run 619, local code
validation on run 610, CLI smokes on runs 609 and 611, state audit on run 612,
and leaves GPU work gated.

Stage 11DE: next-action queue resume refresh.

Run 628 refreshes the current next-action queue after run 627. It points
restart to run 626, commit preparation to run 627, archive handoff to run 623,
manuscript validation to run 619, local code validation to run 610, CLI smokes
to runs 609 and 611, state audit to run 612, and leaves GPU work gated.

Stage 11DF: current resume state audit.

Run 629 audits the current post-resume-refresh state. Runs 626-628 have
parseable manifests and no missing declared artifacts, docs/experiments
159-161 and infrastructure symlinks are present, run 628 points restart to run
626 and commit preparation to run 627, the run 623 archive checksum and
742-entry count remain stable, and GPU work remains gated.

Stage 11DG: commit summary current resume-audit refresh.

Run 630 refreshes the commit/PR summary after run 629. It supersedes run 627
for commit preparation, records run 629 as the current state audit, keeps
restart on run 626, archive handoff on run 623, manuscript validation on run
619, local code validation on run 610, and leaves GPU work gated.

Stage 11DH: next-action queue resume-audit refresh.

Run 631 refreshes the current next-action queue after run 630. It points state
audit to run 629, commit preparation to run 630, restart to run 626, archive
handoff to run 623, manuscript validation to run 619, local code validation to
run 610, CLI smokes to runs 609 and 611, and leaves GPU work gated.

Stage 11DI: current resume archive size audit.

Run 632 audits the current handoff dependency set after the resume/audit queue
refresh. It finds 214 base dependency paths, 586 files, zero missing paths,
133.6 MiB total size, 19 paths not covered by run 623, 49 files missing from
run 623, and three changed planning files, so a refreshed current handoff
archive is justified.

Stage 11DJ: current handoff archive resume refresh.

Run 633 packages the refreshed current handoff archive. The archive has 215
input paths, 805 entries, is 128M compressed, includes the run 632 audit folder
and current resume/audit queue state, excludes the run 633 self folder,
preserves the previous run 623 archive folder, and has SHA-256
00637efb4a579591b0f529f693a7e722b94361b0a3ea129cde5695ba35e49aef.

Stage 11DK: commit summary current archive-resume refresh.

Run 634 refreshes the commit/PR summary after run 633. It supersedes run 630
for commit preparation, records run 633 as the current handoff archive, keeps
restart on run 626, state audit on run 629, manuscript validation on run 619,
local code validation on run 610, and leaves GPU work gated.

Stage 11DL: next-action queue archive-resume refresh.

Run 635 refreshes the current next-action queue after run 634. It points
archive handoff to run 633, commit preparation to run 634, restart to run 626,
state audit to run 629, manuscript validation to run 619, local code
validation to run 610, CLI smokes to runs 609 and 611, and leaves GPU work
gated.

Stage 11DM: IMRAD manuscript current resume-archive validation refresh.

Run 636 refreshes the run 562 IMRAD manuscript pointers to the current run
626/629/633/634/635 resume, audit, archive, commit, and queue state.
Structural lint passes with 57 referenced runs, zero missing runs, seven
resolved embedded figures, and all five guardrails present. No scientific claim
changed.

Stage 11DN: commit summary current manuscript resume-archive refresh.

Run 637 refreshes the commit/PR summary after run 636. It supersedes run 634
for commit preparation, records run 636 as the current manuscript validation
artifact, keeps archive handoff on run 633, restart on run 626, state audit on
run 629, local code validation on run 610, and leaves GPU work gated.

Stage 11DO: next-action queue manuscript resume-archive refresh.

Run 638 refreshes the current next-action queue after run 637. It points
manuscript validation to run 636, commit preparation to run 637, archive
handoff to run 633, restart to run 626, state audit to run 629, local code
validation to run 610, CLI smokes to runs 609 and 611, and leaves GPU work
gated.

Stage 11DP: objective diagnostic manifest artifact hardening.

Run 639 hardens objective diagnostic report manifests so optional confidence
CSV artifact entries are omitted when no confidence CSV is written. It adds a
CLI-style regression test for the no-confidence-row path and validates with
13/13 objective diagnostic tests, 22/22 reporting focused tests, 263/263 full
tests, and clean `git diff --check`.

Stage 11DQ: commit summary current manifest-validation refresh.

Run 640 refreshes the commit/PR summary after run 639. It supersedes run 637
for commit preparation, records run 639 as the current local validation
checkpoint, keeps manuscript validation on run 636, archive handoff on run 633,
restart on run 626, state audit on run 629, and leaves GPU work gated.

Stage 11DR: next-action queue manifest-validation refresh.

Run 641 refreshes the current next-action queue after run 640. It points local
validation to run 639, commit preparation to run 640, manuscript validation to
run 636, archive handoff to run 633, restart to run 626, state audit to run
629, CLI smokes to runs 609 and 611, and leaves GPU work gated.

Stage 11DS: objective diagnostic no-confidence manifest smoke.

Run 642 runs the real objective diagnostic CLI on a summary with diagnostic
ratio rows but no saved objective confidence rows. The manifest omits
`confidence_csv`, no confidence CSV is created, the report has zero non-finite
numeric values, and the generated 2059 x 1005 plot is nonblank with figure
notes.

Stage 11DT: commit summary current manifest-smoke refresh.

Run 643 refreshes the commit/PR summary after run 642. It supersedes run 640
for commit preparation, records run 642 as the current no-confidence manifest
CLI smoke, preserves run 639 as current local validation, keeps manuscript
validation on run 636, archive handoff on run 633, restart on run 626, and
state audit on run 629.

Stage 11DU: next-action queue manifest-smoke refresh.

Run 644 refreshes the current next-action queue after run 643. It points
objective CLI smokes to runs 611 and 642, aggregate CLI smoke to run 609, local
validation to run 639, commit preparation to run 643, manuscript validation to
run 636, archive handoff to run 633, restart to run 626, and state audit to
run 629.

Stage 11DV: current manifest-smoke state audit.

Run 645 audits the current post-manifest-smoke state. Runs 639-644 have
parseable manifests and no missing declared artifacts, docs/experiments
172-177 and infrastructure symlinks are present, run 642 omits the confidence
CSV manifest artifact and has zero non-finite report values, the run 642 plot
is nonblank, and the run 633 archive checksum and 805-entry count remain
stable.

Stage 11DW: commit summary current manifest-audit refresh.

Run 646 refreshes the commit/PR summary after run 645. It supersedes run 643
for commit preparation, records run 645 as the current state audit, preserves
run 642 as the no-confidence manifest CLI smoke, keeps local validation on run
639, manuscript validation on run 636, archive handoff on run 633, and restart
on run 626.

Stage 11DX: next-action queue manifest-audit refresh.

Run 647 refreshes the current next-action queue after run 646. It points state
audit to run 645, commit preparation to run 646, local validation to run 639,
objective CLI smokes to runs 611 and 642, manuscript validation to run 636,
archive handoff to run 633, restart to run 626, and leaves GPU work gated.

Stage 11DY: post-manifest-audit resume checkpoint.

Run 648 records the crash-recovery restart state after validating run 647. It
supersedes run 626 as the current restart checkpoint, keeps run 647 as the
current next-action queue, run 646 as commit preparation, run 645 as state
audit, run 639 as local validation, run 636 as manuscript validation, and run
633 as the current packaged archive.

Stage 11DZ: commit summary current resume-checkpoint refresh.

Run 649 refreshes the commit/PR summary after run 648. It supersedes run 646
for commit preparation, records run 648 as the current restart checkpoint,
keeps run 645 as the state audit, run 639 as local validation, run 636 as
manuscript validation, and run 633 as the current packaged archive.

Stage 11EA: next-action queue resume-checkpoint refresh.

Run 650 refreshes the current next-action queue after run 649. It points
restart to run 648, commit preparation to run 649, state audit to run 645,
local validation to run 639, objective CLI smokes to runs 611 and 642,
manuscript validation to run 636, archive handoff to run 633, and leaves GPU
work gated.

Stage 11EB: current resume-checkpoint state audit.

Run 651 audits the recovered resume chain. Runs 647-650 have parseable
manifests and no missing declared artifacts, docs/experiments 180-183 and
infrastructure symlinks are present, the run 650 queue points restart to run
648 and commit preparation to run 649, and the run 633 archive checksum and
805-entry count remain stable.

Stage 11EC: commit summary current state-audit refresh.

Run 652 refreshes the commit/PR summary after run 651. It supersedes run 649
for commit preparation, records run 651 as the current state audit, keeps run
648 as the restart checkpoint, run 639 as local validation, run 636 as
manuscript validation, and run 633 as the current packaged archive.

Stage 11ED: next-action queue state-audit refresh.

Run 653 refreshes the current next-action queue after run 652. It points state
audit to run 651, commit preparation to run 652, restart to run 648, local
validation to run 639, objective CLI smokes to runs 611 and 642, manuscript
validation to run 636, archive handoff to run 633, and leaves GPU work gated.

Stage 11EE: current state archive coverage audit.

Run 654 audits run 633 archive coverage against the current local state through
run 653. The archive checksum and 805-entry count remain valid, but 42 paths
are not covered, 99 files are missing from the archive, 6 covered files
changed, and the current candidate handoff set is about 260.7 MiB before
compression. A refreshed archive is justified for external handoff, but local
work should avoid rebuilding archives repeatedly.

Stage 11EF: commit summary current archive-coverage refresh.

Run 655 refreshes the commit/PR summary after run 654. It supersedes run 652
for commit preparation, records run 654 as the current archive coverage audit,
keeps run 651 as state audit, run 648 as restart, run 639 as local validation,
run 636 as manuscript validation, and run 633 as the checksum-valid but stale
packaged archive.

Stage 11EG: next-action queue archive-coverage refresh.

Run 656 refreshes the current next-action queue after run 655. It points
archive coverage to run 654, commit preparation to run 655, state audit to run
651, restart to run 648, local validation to run 639, objective CLI smokes to
runs 611 and 642, manuscript validation to run 636, archive handoff to run
633, and leaves GPU work gated.

Stage 11EH: candidate confidence non-finite hardening.

Run 657 hardens shared candidate confidence reporting. Confidence labels now
treat NaN, infinity, and non-numeric margins as missing, ambiguity intervals
ignore non-finite candidate misfits, and validation passes with 7/7
candidate-confidence tests, 22/22 reporting-focused tests, and 265/265 full
tests.

Stage 11EI: commit summary candidate-confidence refresh.

Run 658 refreshes the commit/PR summary after run 657. It supersedes run 655
for commit preparation, records run 657 as the current local validation
checkpoint, keeps run 654 as archive coverage audit, run 651 as state audit,
run 648 as restart, run 636 as manuscript validation, and run 633 as the
checksum-valid but stale packaged archive.

Stage 11EJ: next-action queue candidate-confidence refresh.

Run 659 refreshes the current next-action queue after run 658. It points local
validation to run 657, commit preparation to run 658, archive coverage to run
654, state audit to run 651, restart to run 648, objective CLI smokes to runs
611 and 642, manuscript validation to run 636, archive handoff to run 633, and
leaves GPU work gated.

Stage 11EK: current candidate-confidence state audit.

Run 660 audits the candidate-confidence hardening chain. Runs 657-659 have
parseable manifests and no missing declared artifacts, docs/experiments 190-192
and infrastructure symlinks are present, the run 659 queue points local
validation to run 657 and commit preparation to run 658, and run 657 records
265/265 full-suite validation.

Stage 11EL: commit summary candidate-confidence audit refresh.

Run 661 refreshes the commit/PR summary after run 660. It supersedes run 658
for commit preparation, records run 660 as the current state audit, keeps run
657 as local validation, run 654 as archive coverage audit, run 648 as
restart, run 636 as manuscript validation, and run 633 as the checksum-valid
but stale packaged archive.

Stage 11EM: next-action queue candidate-confidence audit refresh.

Run 662 refreshes the current next-action queue after run 661. It points state
audit to run 660, commit preparation to run 661, local validation to run 657,
archive coverage to run 654, restart to run 648, objective CLI smokes to runs
611 and 642, manuscript validation to run 636, archive handoff to run 633, and
leaves GPU work gated.

Stage 11EN: candidate confidence row-sanitization hardening.

Run 663 extends candidate confidence hardening to flattened output rows.
Non-finite optional numeric fields are serialized as null, competing-geometry
comparison tolerates malformed x/z fields, and validation passes with 8/8
candidate-confidence tests, 22/22 reporting-focused tests, and 266/266 full
tests.

Stage 11EO: commit summary candidate row-sanitization refresh.

Run 664 refreshes the commit/PR summary after run 663. It supersedes run 661
for commit preparation, records run 663 as the current local validation
checkpoint, keeps run 660 as state audit, run 654 as archive coverage audit,
run 648 as restart, run 636 as manuscript validation, and run 633 as the
checksum-valid but stale packaged archive.

Stage 11EP: next-action queue candidate row-sanitization refresh.

Run 665 refreshes the current next-action queue after run 664. It points local
validation to run 663, commit preparation to run 664, state audit to run 660,
archive coverage to run 654, restart to run 648, objective CLI smokes to runs
611 and 642, manuscript validation to run 636, archive handoff to run 633, and
leaves GPU work gated.

Stage 11EQ: current candidate row-sanitization state audit.

Run 666 audits the candidate row-sanitization hardening chain. Runs 663-665
have parseable manifests and no missing declared artifacts, docs/experiments
196-198 and infrastructure symlinks are present, the run 665 queue points local
validation to run 663 and commit preparation to run 664, and run 663 records
266/266 full-suite validation.

Stage 11ER: commit summary candidate row-sanitization audit refresh.

Run 667 refreshes the commit/PR summary after run 666. It supersedes run 664
for commit preparation, records run 666 as the current state audit, keeps run
663 as local validation, run 654 as archive coverage audit, run 648 as
restart, run 636 as manuscript validation, and run 633 as the checksum-valid
but stale packaged archive.

Stage 11ES: next-action queue candidate row-sanitization audit refresh.

Run 668 refreshes the current next-action queue after run 667. It points state
audit to run 666, commit preparation to run 667, local validation to run 663,
archive coverage to run 654, restart to run 648, objective CLI smokes to runs
611 and 642, manuscript validation to run 636, archive handoff to run 633, and
leaves GPU work gated.

Stage 11ET: objective diagnostic non-finite confidence smoke.

Run 669 validates row-sanitization through the real objective diagnostic CLI.
The report has zero invalid JSON tokens and zero non-finite numeric values, the
non-finite objective variant is labeled missing with blank CSV cells, the
manifest includes `confidence_csv`, and the 2059 x 1005 plot is nonblank with
figure notes.

Stage 11EU: commit summary non-finite confidence smoke refresh.

Run 670 refreshes the commit/PR summary after run 669. It supersedes run 667
for commit preparation, records run 669 as the current non-finite objective
confidence CLI smoke, keeps run 663 as local validation, run 666 as state
audit, run 654 as archive coverage audit, run 648 as restart, and run 633 as
the checksum-valid but stale packaged archive.

Stage 11EV: next-action queue non-finite confidence smoke refresh.

Run 671 refreshes the current next-action queue after run 670. It points
objective CLI smokes to runs 611, 642, and 669, commit preparation to run 670,
local validation to run 663, state audit to run 666, archive coverage to run
654, restart to run 648, manuscript validation to run 636, archive handoff to
run 633, and leaves GPU work gated.

Stage 11EW: current non-finite confidence smoke state audit.

Run 672 audits the non-finite confidence smoke chain. Runs 669-671 have
parseable manifests and no missing declared artifacts, docs/experiments 202-204
and infrastructure symlinks are present, run 669 smoke validation passes, and
run 671 points objective CLI smokes to runs 611, 642, and 669.

Stage 11EX: commit summary non-finite confidence audit refresh.

Run 673 refreshes the commit/PR summary after run 672. It supersedes run 670
for commit preparation, records run 672 as the current state audit, keeps run
669 as the non-finite objective confidence CLI smoke, run 663 as local
validation, run 654 as archive coverage audit, run 648 as restart, and run 633
as the checksum-valid but stale packaged archive.

Stage 11EY: next-action queue non-finite confidence audit refresh.

Run 674 refreshes the current next-action queue after run 673. It points state
audit to run 672, commit preparation to run 673, objective CLI smokes to runs
611, 642, and 669, local validation to run 663, archive coverage to run 654,
restart to run 648, manuscript validation to run 636, archive handoff to run
633, and leaves GPU work gated.

Stage 11EZ: coordinate aggregate row-sanitization hardening.

Run 675 hardens coordinate confidence aggregate row output. Summary metadata
and optional numeric confidence-row fields are finite-normalized before
aggregation/serialization, enriched rows are covered by JSON-safe regression
tests, and validation passes with 9/9 aggregate tests, 21/21 related reporting
tests, and 266/266 full tests.

Stage 11FA: coordinate aggregate non-finite row smoke.

Run 676 validates the aggregate row-sanitization through the real coordinate
confidence aggregate CLI. The emitted JSON, CSV, and manifest contain zero
invalid NaN/Infinity tokens and zero non-finite parsed numeric values,
non-finite optional row fields become blank CSV cells, the valid row remains a
truth-geometry row, source/acquisition summaries stay empty for non-finite
metadata, and both aggregate plots are nonblank with figure notes.

Stage 11FB: commit summary coordinate aggregate smoke refresh.

Run 677 refreshes the commit/PR summary after runs 675 and 676. It supersedes
run 673 for commit preparation, records run 675 as the current aggregate
row-sanitization validation checkpoint, records run 676 as the current
aggregate non-finite row CLI smoke, and preserves run 672 as state audit, run
654 as archive coverage audit, run 648 as restart, and run 633 as the
checksum-valid but stale packaged archive.

Stage 11FC: next-action queue coordinate aggregate smoke refresh.

Run 678 refreshes the current next-action queue after run 677. It points local
validation to run 675, aggregate CLI smokes to runs 609 and 676, objective CLI
smokes to runs 611, 642, and 669, commit preparation to run 677, state audit
to run 672, archive coverage to run 654, restart to run 648, manuscript
validation to run 636, archive handoff to run 633, and leaves GPU work gated.

Stage 11FD: current coordinate aggregate smoke state audit.

Run 679 audits runs 675-678. Their manifests parse, declared artifacts exist,
docs/experiments 208-211 and infrastructure symlinks are present, run 676
smoke validation passes, and run 678 points aggregate CLI smokes to runs 609
and 676 and commit preparation to run 677.

Stage 11FE: commit summary coordinate aggregate audit refresh.

Run 680 refreshes the commit/PR summary after run 679. It supersedes run 677
for commit preparation, records run 679 as the current state audit, keeps run
675 as local validation, run 676 as aggregate non-finite row CLI smoke, run 654
as archive coverage audit, run 648 as restart, and run 633 as the
checksum-valid but stale packaged archive.

Stage 11FF: next-action queue coordinate aggregate audit refresh.

Run 681 refreshes the current next-action queue after run 680. It points local
validation to run 675, aggregate CLI smokes to runs 609 and 676, objective CLI
smokes to runs 611, 642, and 669, state audit to run 679, commit preparation
to run 680, archive coverage to run 654, restart to run 648, manuscript
validation to run 636, archive handoff to run 633, and leaves GPU work gated.

Stage 11FG: current state archive coverage audit refresh.

Run 682 refreshes archive coverage without building a new archive. The run 633
archive remains checksum-valid with 805 entries, but the current state through
run 681 has 100 base paths not covered by run 633, 235 files missing from run
633, and 8 already-covered files changed. Archive rebuild remains gated to
external handoff needs.

Stage 11FH: commit summary current archive coverage refresh.

Run 683 refreshes the commit/PR summary after run 682. It supersedes run 680
for commit preparation, records run 682 as the current archive coverage audit,
keeps run 679 as state audit, run 675 as local validation, run 676 as aggregate
non-finite row CLI smoke, run 648 as restart, and run 633 as the
checksum-valid but stale packaged archive.

Stage 11FI: next-action queue current archive coverage refresh.

Run 684 refreshes the current next-action queue after run 683. It points local
validation to run 675, aggregate CLI smokes to runs 609 and 676, objective CLI
smokes to runs 611, 642, and 669, state audit to run 679, archive coverage to
run 682, commit preparation to run 683, restart to run 648, manuscript
validation to run 636, archive handoff to run 633, and leaves GPU work gated.

Stage 11FJ: IMRAD manuscript current archive-coverage validation refresh.

Run 685 refreshes the IMRAD manuscript validation/archive pointers to the
current run 675/676/679/682/683/684 state. The lint passes with 63 referenced
runs, 0 missing referenced runs, 7/7 embedded images resolved, 0 unresolved
editing markers, and the balance audit preserves all five guardrails without
changing scientific claims.

Stage 11FK: commit summary current manuscript validation refresh.

Run 686 refreshes the commit/PR summary after run 685. It supersedes run 683
for commit preparation, records run 685 as the current manuscript validation,
keeps run 682 as archive coverage audit, run 679 as state audit, run 675 as
local validation, run 676 as aggregate non-finite row CLI smoke, run 648 as
restart, and run 633 as the checksum-valid but stale packaged archive.

Stage 11FL: next-action queue current manuscript validation refresh.

Run 687 refreshes the current next-action queue after run 686. It points local
validation to run 675, aggregate CLI smokes to runs 609 and 676, objective CLI
smokes to runs 611, 642, and 669, state audit to run 679, archive coverage to
run 682, manuscript validation to run 685, commit preparation to run 686,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11FM: current manuscript/archive state audit.

Run 688 audits runs 682-687. Their manifests parse, declared artifacts exist,
docs/experiments 215-220 and infrastructure symlinks are present, run 682
archive coverage and run 685 manuscript validation pass, and run 687 points
manuscript validation to run 685, archive coverage to run 682, and commit
preparation to run 686.

Stage 11FN: commit summary current manuscript/archive audit refresh.

Run 689 refreshes the commit/PR summary after run 688. It supersedes run 686
for commit preparation, records run 688 as the current state audit, keeps run
685 as manuscript validation, run 682 as archive coverage audit, run 675 as
local validation, run 676 as aggregate non-finite row CLI smoke, run 648 as
restart, and run 633 as the checksum-valid but stale packaged archive.

Stage 11FO: next-action queue current manuscript/archive audit refresh.

Run 690 refreshes the current next-action queue after run 689. It points local
validation to run 675, aggregate CLI smokes to runs 609 and 676, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 682, manuscript
validation to run 685, state audit to run 688, commit preparation to run 689,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11FP: current precommit validation after manuscript/archive refresh.

Run 691 refreshes local validation after the manuscript/archive refresh chain.
The full suite passes at 266/266 in 24.28 s, `git diff --check` is clean, GPU
utilization is 0%, RAM availability is 101 GiB, and run 691 supersedes run 675
as the current local validation checkpoint.

Stage 11FQ: commit summary current validation refresh.

Run 692 refreshes the commit/PR summary after run 691. It supersedes run 689
for commit preparation, records run 691 as the current local validation
checkpoint, keeps run 688 as state audit, run 685 as manuscript validation, run
682 as archive coverage audit, run 648 as restart, and run 633 as the
checksum-valid but stale packaged archive.

Stage 11FR: next-action queue current validation refresh.

Run 693 refreshes the current next-action queue after run 692. It points local
validation to run 691, aggregate CLI smokes to runs 609 and 676, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 682, manuscript
validation to run 685, state audit to run 688, commit preparation to run 692,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11FS: coordinate confidence metadata/default hardening.

Run 694 fixes the remaining JSON-safety edges found in lightweight self-review.
The aggregate CLI now rejects non-finite or negative default Tx/Rx offsets, and
candidate-confidence numeric metadata is finite-normalized before
serialization. Validation passes with 19/19 focused candidate/aggregate tests,
13/13 objective diagnostic tests, and 268/268 full-suite tests.

Stage 11FT: coordinate aggregate invalid default smoke.

Run 695 validates run 694 through the real aggregate CLI. `nan`, `inf`, and
negative default Tx/Rx offsets are rejected before output allocation; a finite
20 mm default still writes strict JSON, CSV, manifest, plots, and figure notes
with zero non-finite output numerics and both plots nonblank.

Stage 11FU: commit summary coordinate default smoke refresh.

Run 696 refreshes the commit/PR summary after run 695. It supersedes run 692
for commit preparation, records run 694 as local validation and
metadata/default hardening, records run 695 as aggregate invalid-default CLI
smoke, and keeps run 688 as state audit, run 685 as manuscript validation, run
682 as archive coverage audit, run 648 as restart, and run 633 as the
checksum-valid but stale packaged archive.

Stage 11FV: next-action queue coordinate default smoke refresh.

Run 697 refreshes the current next-action queue after run 696. It points local
validation and metadata/default hardening to run 694, aggregate CLI smokes to
runs 609, 676, and 695, objective CLI smokes to runs 611, 642, and 669,
archive coverage to run 682, manuscript validation to run 685, state audit to
run 688, commit preparation to run 696, restart to run 648, archive handoff to
run 633, and leaves GPU work gated.

Stage 11FW: current coordinate default smoke state audit.

Run 698 audits runs 694-697. Their manifests parse, declared artifacts exist,
docs/experiments 227-230 and infrastructure symlinks are present, run 694
local validation and run 695 invalid-default CLI smoke pass, and run 697 points
local validation to run 694, aggregate CLI smokes to runs 609/676/695, and
commit preparation to run 696.

Stage 11FX: commit summary coordinate default audit refresh.

Run 699 refreshes the commit/PR summary after run 698. It supersedes run 696
for commit preparation, records run 698 as the current state audit, keeps run
694 as local validation and metadata/default hardening, run 695 as aggregate
invalid-default CLI smoke, run 685 as manuscript validation, run 682 as archive
coverage audit, run 648 as restart, and run 633 as the checksum-valid but stale
packaged archive.

Stage 11FY: next-action queue coordinate default audit refresh.

Run 700 refreshes the current next-action queue after run 699. It points local
validation and metadata/default hardening to run 694, aggregate CLI smokes to
runs 609, 676, and 695, objective CLI smokes to runs 611, 642, and 669,
archive coverage to run 682, manuscript validation to run 685, state audit to
run 698, commit preparation to run 699, restart to run 648, archive handoff to
run 633, and leaves GPU work gated.

Stage 11FZ: current coordinate default audit refresh state audit.

Run 701 audits runs 698-700. Their manifests parse, declared artifacts exist,
docs/experiments 231-233 and infrastructure symlinks are present, run 698
state audit and run 699 inventory are valid, and run 700 points state audit to
run 698 and commit preparation to run 699.

Stage 11GA: current precommit validation after coordinate default audit refresh.

Run 702 refreshes local validation after the run698-701 audit/commit/queue
chain. The full suite passes at 268/268 in 24.60 s, `git diff --check` is
clean, GPU utilization is 1%, RAM availability is 101 GiB, and run 702
supersedes run 694 as the current local validation checkpoint.

Stage 11GB: commit summary current validation after coordinate default audit
refresh.

Run 703 refreshes the commit/PR summary after run 702. It supersedes run 699
for commit preparation, records run 702 as the current local validation
checkpoint, keeps run 701 as state audit, run 695 as aggregate invalid-default
CLI smoke, run 685 as manuscript validation, run 682 as archive coverage
audit, run 648 as restart, and run 633 as the checksum-valid but stale
packaged archive.

Stage 11GC: next-action queue current validation after coordinate default audit
refresh.

Run 704 refreshes the current next-action queue after run 703. It points local
validation to run 702, metadata/default hardening to run 694, aggregate CLI
smokes to runs 609, 676, and 695, objective CLI smokes to runs 611, 642, and
669, archive coverage to run 682, manuscript validation to run 685, state audit
to run 701, commit preparation to run 703, restart to run 648, archive handoff
to run 633, and leaves GPU work gated.

Stage 11GD: current validation after coordinate default audit state audit.

Run 705 audits runs 702-704. Their manifests parse, declared artifacts exist,
docs/experiments 235-237 and infrastructure symlinks are present, run 702
local validation and run 703 inventory are valid, and run 704 points local
validation to run 702, state audit to run 701, and commit preparation to run
703.

Stage 11GE: code self-review current validation checkpoint.

Run 706 reviews the current candidate-confidence, coordinate aggregate,
objective diagnostic, and test diffs after run 702 validation and run 705
audit. It finds zero blocking runtime defects, makes no code edits, and records
the remaining manifest-helper JSON strictness note as covered by focused tests
and CLI smokes for the changed reporting paths.

Stage 11GF: commit summary current review refresh.

Run 707 refreshes the commit/PR summary after run 706. It supersedes run 703
for commit preparation, records run 706 as the current focused code self-review
checkpoint, keeps run 702 as local validation, run 705 as state audit, run 685
as manuscript validation, run 682 as archive coverage audit, run 648 as
restart, and run 633 as the checksum-valid but stale packaged archive.

Stage 11GG: next-action queue current review refresh.

Run 708 refreshes the current next-action queue after run 707. It points local
validation to run 702, code self-review to run 706, metadata/default hardening
to run 694, aggregate CLI smokes to runs 609, 676, and 695, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 682, manuscript
validation to run 685, state audit to run 705, commit preparation to run 707,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11GH: current review refresh state audit.

Run 709 audits runs 706-708. Their manifests parse, declared artifacts exist,
docs/experiments 239-241 and infrastructure symlinks are present, run 706 code
self-review has zero blocking findings, run 707 inventory is valid, and run 708
points code self-review to run 706 and commit preparation to run 707.

Stage 11GI: current state archive coverage audit refresh.

Run 710 refreshes archive coverage for current local state through run 709 and
docs/experiments/242 without building a new archive. Run 633 remains
checksum-valid with 805 entries, but is stale: the current base has 371 paths
and 947 files, with 156 paths and 364 files not covered by run 633. Archive
rebuilding remains gated to explicit external handoff need.

Stage 11GJ: commit summary current archive coverage refresh.

Run 711 refreshes the commit/PR summary after run 710. It supersedes run 707
for commit preparation, records run 710 as the current archive coverage audit,
keeps run 702 as local validation, run 706 as code self-review, run 709 as
state audit, run 685 as manuscript validation, run 648 as restart, and run 633
as the checksum-valid but stale packaged archive.

Stage 11GK: next-action queue current archive coverage refresh.

Run 712 refreshes the current next-action queue after run 711. It points local
validation to run 702, code self-review to run 706, metadata/default hardening
to run 694, aggregate CLI smokes to runs 609, 676, and 695, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 710, manuscript
validation to run 685, state audit to run 709, commit preparation to run 711,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11GL: current archive coverage refresh state audit.

Run 713 audits runs 710-712. Their manifests parse, declared artifacts exist,
docs/experiments 243-245 and infrastructure symlinks are present, run 710
archive coverage remains pass with the run 633 checksum verified, run 711
inventory is valid, and run 712 points archive coverage to run 710 and commit
preparation to run 711.

Stage 11GM: current precommit validation after archive coverage refresh.

Run 714 refreshes local validation after the run710-713 archive coverage audit
chain. The full suite passes at 268/268 in 24.41 s, `git diff --check` is
clean, GPU utilization is 1%, RAM availability is 101 GiB, and run 714
supersedes run 702 as the current local validation checkpoint.

Stage 11GN: commit summary current validation refresh.

Run 715 refreshes the commit/PR summary after run 714. It supersedes run 711
for commit preparation, records run 714 as the current local validation
checkpoint, keeps run 706 as code self-review, run 713 as state audit, run 710
as archive coverage audit, run 685 as manuscript validation, run 648 as
restart, and run 633 as the checksum-valid but stale packaged archive.

Stage 11GO: next-action queue current validation refresh.

Run 716 refreshes the current next-action queue after run 715. It points local
validation to run 714, code self-review to run 706, metadata/default hardening
to run 694, aggregate CLI smokes to runs 609, 676, and 695, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 710, manuscript
validation to run 685, state audit to run 713, commit preparation to run 715,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11GP: current validation refresh state audit.

Run 717 audits runs 714-716. Their manifests parse, declared artifacts exist,
docs/experiments 247-249 and infrastructure symlinks are present, run 714
local validation passes 268/268 with clean diff check, run 715 inventory is
valid, and run 716 points local validation to run 714 and commit preparation
to run 715.

Stage 11GQ: code self-review current validation refresh.

Run 718 reviews the current candidate-confidence, coordinate aggregate,
objective diagnostic, and test diffs after run 714 validation and run 717
audit. Focused tests pass at 32/32 in 0.30 s, zero blocking runtime defects
are found, and no code edits are made.

Stage 11GR: commit summary current review refresh.

Run 719 refreshes the commit/PR summary after run 718. It supersedes run 715
for commit preparation, records run 718 as the current focused code self-review
checkpoint, keeps run 714 as local validation, run 717 as state audit, run 710
as archive coverage audit, run 685 as manuscript validation, run 648 as
restart, and run 633 as the checksum-valid but stale packaged archive.

Stage 11GS: next-action queue current review refresh.

Run 720 refreshes the current next-action queue after run 719. It points local
validation to run 714, code self-review to run 718, metadata/default hardening
to run 694, aggregate CLI smokes to runs 609, 676, and 695, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 710, manuscript
validation to run 685, state audit to run 717, commit preparation to run 719,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11GT: current review refresh state audit.

Run 721 audits runs 718-720. Their manifests parse, declared artifacts exist,
docs/experiments 251-253 and infrastructure symlinks are present, run 718 code
self-review has zero blocking findings, run 719 inventory is valid, and run
720 points code self-review to run 718 and commit preparation to run 719.

Stage 11GU: current state archive coverage audit refresh.

Run 722 refreshes archive coverage for current local state through run 721 and
docs/experiments/254 without building a new archive. Run 633 remains
checksum-valid with 805 entries, but is stale: the current base has 395 paths
and 1003 files, with 180 paths and 420 files not covered by run 633. Archive
rebuilding remains gated to explicit external handoff need.

Stage 11GV: commit summary current archive coverage refresh.

Run 723 refreshes the commit/PR summary after run 722. It supersedes run 719
for commit preparation, records run 722 as the current archive coverage audit,
keeps run 714 as local validation, run 718 as code self-review, run 721 as
state audit, run 685 as manuscript validation, run 648 as restart, and run 633
as the checksum-valid but stale packaged archive.

Stage 11GW: next-action queue current archive coverage refresh.

Run 724 refreshes the current next-action queue after run 723. It points local
validation to run 714, code self-review to run 718, metadata/default hardening
to run 694, aggregate CLI smokes to runs 609, 676, and 695, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 722, manuscript
validation to run 685, state audit to run 721, commit preparation to run 723,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11GX: current archive coverage refresh state audit.

Run 725 audits runs 722-724. Their manifests parse, declared artifacts exist,
docs/experiments 255-257 and infrastructure symlinks are present, run 722
archive coverage remains pass with the run 633 checksum verified, run 723
inventory is valid, and run 724 points archive coverage to run 722 and commit
preparation to run 723.

Stage 11GY: current precommit validation after archive coverage audit refresh.

Run 726 refreshes local validation after the run722-725 archive coverage audit
chain. The full suite passes at 268/268 in 24.43 s, `git diff --check` is
clean, GPU utilization is 1%, RAM availability is 101 GiB, and run 726
supersedes run 714 as the current local validation checkpoint.

Stage 11GZ: commit summary current validation refresh.

Run 727 refreshes the commit/PR summary after run 726. It supersedes run 723
for commit preparation, records run 726 as the current local validation
checkpoint, keeps run 718 as code self-review, run 725 as state audit, run 722
as archive coverage audit, run 685 as manuscript validation, run 648 as
restart, and run 633 as the checksum-valid but stale packaged archive.

Stage 11HA: next-action queue current validation refresh.

Run 728 refreshes the current next-action queue after run 727. It points local
validation to run 726, code self-review to run 718, metadata/default hardening
to run 694, aggregate CLI smokes to runs 609, 676, and 695, objective CLI
smokes to runs 611, 642, and 669, archive coverage to run 722, manuscript
validation to run 685, state audit to run 725, commit preparation to run 727,
restart to run 648, archive handoff to run 633, and leaves GPU work gated.

Stage 11HB: current validation refresh state audit.

Run 729 audits runs 726-728. Their manifests parse, declared artifacts exist,
docs/experiments 259-261 and infrastructure symlinks are present, run 726
local validation passes 268/268 with clean diff check, run 727 inventory is
valid, and run 728 points local validation to run 726 and commit preparation
to run 727.

Stage 11HC: IMRAD manuscript current validation refresh.

Run 730 refreshes the run 562 IMRAD manuscript validation/archive and Data And
Code Availability pointers to the current run 718 code self-review, run 722
archive coverage, run 726 local validation, run 727 commit preparation, run
728 queue, and run 729 state audit. Structural lint passes with 68 referenced
runs, zero missing runs, seven resolved embedded figures, zero unresolved
editing markers, all five guardrails present, and `git diff --check` clean.
No scientific claim changed.

Stage 11HD: commit/PR summary current manuscript validation refresh.

Run 731 refreshes the commit/PR summary after run 730. It supersedes run 727
for commit preparation, records run 730 as the current manuscript validation
checkpoint, keeps run 726 as local validation, run 718 as code self-review,
run 729 as state audit, run 722 as archive coverage audit, run 648 as restart,
and run 633 as the checksum-valid but stale packaged archive. The diff check
is clean after the refresh.

Stage 11HE: next-action queue current manuscript validation refresh.

Run 732 refreshes the current next-action queue after run 731. It points
manuscript validation to run 730, local validation to run 726, code self-review
to run 718, state audit to run 729, archive coverage to run 722, commit
preparation to run 731, restart to run 648, archive handoff to run 633, and
leaves GPU work gated. Queue pointer checks pass at 11/11, and the diff check
is clean after the refresh.

Stage 11HF: current manuscript validation refresh state audit.

Run 733 audits runs 730-732. Their manifests parse, declared artifacts exist,
docs/experiments 263-265 and infrastructure symlinks are present, run 730
manuscript checks pass 7/7, run 731 summary checks pass 5/5, run 732 queue
pointer checks pass 11/11, planning doc pointer checks pass 3/3, and the diff
check is clean after the audit.

Stage 11HG: current state archive coverage audit refresh.

Run 734 refreshes archive coverage for current local state through run 733 and
docs/experiments/266 without building a new archive. Run 633 remains
checksum-valid with 805 entries, but is stale: the current base has 419 paths
and 1060 files, with 204 paths and 477 files not covered by run 633. Archive
rebuilding remains gated to explicit external handoff need, and the diff check
is clean after the audit.

Stage 11HH: commit/PR summary current archive coverage refresh.

Run 735 refreshes the commit/PR summary after run 734. It supersedes run 731
for commit preparation, records run 734 as the current archive coverage audit,
keeps run 726 as local validation, run 718 as code self-review, run 733 as
state audit, run 730 as manuscript validation, run 648 as restart, and run 633
as the checksum-valid but stale packaged archive. The diff check is clean
after the refresh.

Stage 11HI: next-action queue current archive coverage refresh.

Run 736 refreshes the current next-action queue after run 735. It points
archive coverage to run 734, commit preparation to run 735, manuscript
validation to run 730, local validation to run 726, code self-review to run
718, state audit to run 733, restart to run 648, archive handoff to run 633,
and leaves GPU work gated. Queue pointer checks pass at 11/11, and the diff
check is clean after the refresh.

Stage 11HJ: current archive coverage refresh state audit.

Run 737 audits runs 734-736. Their manifests parse, declared artifacts exist,
docs/experiments 267-269 and infrastructure symlinks are present, run 734
archive checks pass 9/9, run 735 summary checks pass 5/5, run 736 queue
pointer checks pass 11/11, planning doc pointer checks pass 3/3, and the diff
check is clean after the audit.

Stage 11HK: post-archive-coverage audit resume checkpoint.

Run 738 records the current crash-recovery checkpoint after the manuscript
validation and archive coverage refresh chain. It points local validation to
run 726, code self-review to run 718, manuscript validation to run 730,
archive coverage to run 734, state audit to run 737, commit preparation to run
735, next-action queue to run 736, archive handoff to run 633, and keeps GPU
work gated by default. The diff check is clean after the checkpoint.

Stage 11HL: experiment archive health report current.

Run 739 audits 738 numbered output folders to answer why runs 430-730, and
especially 535-730, completed much faster than the earlier archive. The result
confirms a run-style drift rather than a physics speedup: runs 431-534 remain
artifact-heavy with 104/104 data dirs, 101/104 figure dirs, and 101/104 figure
note folders, while runs 535-730 contain 169/196 reporting/audit/checkpoint
records, only 8 figure dirs, and only 7 figure-note folders. The corrective
policy is that future physical or diagnostic numbered runs require data and
figure notes when images exist, and checkpoint/queue/commit-summary records
should be rare rather than allowed to inflate the apparent experiment count.
Focused tests for the new archive-health runner pass 4/4, full pytest passes
272/272, and the diff check is clean after run 739.

Stage 11HM: seed21 target-0 Tx/Rx=50 fitted-ringdown diagnostic.

Run 740 restores the pre-crash substantive experiment style with a bounded GPU
CPML diagnostic rather than another checkpoint. It extends the variable-depth/
radius Tx/Rx=50 fitted-ringdown branch to an additional seed21 target-0
source-mismatch/noise stress. The base objective recovers exact truth
x=150 mm, z=80 mm, r=5 mm with a moderate 5.386e-04 gap against r=5.25 mm.
All diagnostic objectives preserve truth geometry; veryhigh is strongest for
this target-0 row at 6.734e-04 and 1.250x the base margin, while late and
late_high weaken target 0. This strengthens the existing branch-level rule:
base remains the production coordinate update, veryhigh remains target-0
reporting evidence when it preserves geometry, and late_high should not be
promoted for target 0. GPU utilization reached about 88% with RAM healthy, and
the diff check is clean after run 740.

Stage 11HN: seed21 target-2 Tx/Rx=50 fitted-ringdown diagnostic.

Run 741 applies the same seed21 fitted-ringdown stress to target 2. The base
objective again recovers exact truth x=350 mm, z=120 mm, r=8 mm with a
moderate 8.000e-04 gap against r=7.25 mm. All diagnostic variants preserve
truth geometry. Late_high is strongest for this target-2 row at 1.205e-03 and
1.506x the base margin; veryhigh also improves the row at 1.227x. Together,
runs 740-741 show the added seed21 stress does not expose target-0 or target-2
failure in the Tx/Rx=50 fitted-ringdown final-state branch, and they preserve
the target-specific reporting rule: veryhigh is best for target 0, late_high
is useful for target 2, and base remains the production update. The diff check
is clean after run 741.

Stage 11HO: seed21 target-1 Tx/Rx=50 fitted-ringdown diagnostic.

Run 742 completes the added seed21 all-target fitted-ringdown check with the
heavier center-target grid. The base objective recovers exact truth x=250 mm,
z=100 mm, r=6 mm with a moderate 7.176e-04 gap against r=6.25 mm. All
diagnostic variants preserve truth geometry. Late_high is strongest for the
center target at 9.180e-04 and 1.279x the base margin, while veryhigh is only
mildly above base at 1.018x. Runs 740-742 therefore add a fourth seed across
all targets without exposing a new failure: target 0, target 1, and target 2
are all exact/moderate under the source-mismatch ringdown025 noise10 seed21
stress. The next substantive analysis step should package these three runs
into a compact all-target seed21 summary rather than adding checkpoint churn.
The diff check is clean after run 742.

Stage 11HP: seed21 fitted-ringdown all-target summary.

Run 743 packages runs 740-742 into a compact all-target analysis artifact.
All three base production rows are exact and moderate under
source_mismatch_ringdown025_noise10_seed21: target 0 has a 5.386e-04 base gap,
target 1 has a 7.176e-04 base gap, and target 2 has a 8.000e-04 base gap.
The strongest truth-preserving diagnostic is veryhigh on target 0 at 1.250x
base, and late_high on targets 1 and 2 at 1.279x and 1.506x base. Across 15
diagnostic ratio rows, no diagnostic changes the selected truth geometry.
This strengthens the fitted-ringdown robustness claim while preserving the
production rule: base remains the coordinate update objective, and diagnostic
variants remain reporting evidence. Focused summary tests pass 3/3 and the
diff check is clean after run 743.
```

Stage 11HQ: seed89 target-0 Tx/Rx=50 fitted-ringdown diagnostic.

Run 744 extends the restored substantive GPU branch from seed21 to an
independent seed89 target-0 source-mismatch/noise stress. The base objective
again recovers exact truth x=150 mm, z=80 mm, r=5 mm with a moderate
5.798e-04 gap against r=5.25 mm, slightly above the seed21 target-0 base gap
of 5.386e-04. All diagnostic objectives preserve truth geometry. Veryhigh is
again the strongest target-0 diagnostic at 7.857e-04 and 1.355x the base
margin, while late and late_high weaken the row. This supports the same
branch-level rule as run 740: base remains the production coordinate update,
veryhigh remains target-0 reporting evidence when it preserves geometry, and
late_high should not be promoted for target 0. GPU utilization stayed around
87-88%, RAM remained healthy, and run744 should be followed by seed89 target 2
before packaging a seed89 all-target summary.

Stage 11HR: seed89 target-2 Tx/Rx=50 fitted-ringdown diagnostic.

Run 745 applies the same seed89 fitted-ringdown stress to target 2. The base
objective again recovers exact truth x=350 mm, z=120 mm, r=8 mm with a
moderate 9.936e-04 gap against r=7.25 mm, above the seed21 target-2 base gap
of 8.000e-04. All diagnostic variants preserve truth geometry. Late_high is
again strongest for target 2 at 1.507e-03 and 1.516x the base margin, with
veryhigh also improving the row at 1.367x. This strengthens the target-2
branch evidence while preserving the production rule: base remains the update
objective, late_high is target-2 reporting evidence, and target 1 should be
run next before packaging a seed89 all-target summary.

Stage 11HS: seed89 target-1 Tx/Rx=50 fitted-ringdown diagnostic.

Run 746 completes the seed89 target-specific fitted-ringdown replication with
the heavier center-target grid. The base objective recovers exact truth
x=250 mm, z=100 mm, r=6 mm with a moderate 5.983e-04 gap against r=6.25 mm.
This is lower than the seed21 target-1 base gap of 7.176e-04, so seed89 should
be reported as a real center-target sensitivity rather than hidden in an
aggregate. All diagnostic variants preserve truth geometry. Late_high is again
strongest for target 1 at 8.566e-04 and 1.432x the base margin, while
early_high weakens the row. Runs 744-746 now close the seed89 all-target set:
all three targets are exact/moderate, base remains the production update, and
the next step is a compact seed89 all-target summary comparable to run 743.

Stage 11HT: seed89 fitted-ringdown all-target summary.

Run 747 packages runs 744-746 into a compact seed89 all-target analysis
artifact using the generalized fitted-ringdown summary helper. All three base
production rows are exact and moderate under
source_mismatch_ringdown025_noise10_seed89: target 0 has a 5.798e-04 base
gap, target 1 has a 5.983e-04 base gap, and target 2 has a 9.936e-04 base
gap. The strongest truth-preserving diagnostic remains target-specific:
veryhigh on target 0 at 1.355x base, and late_high on targets 1 and 2 at
1.432x and 1.516x base. Across 15 diagnostic ratio rows, no diagnostic changes
the selected truth geometry. Compared with seed21, seed89 strengthens target 0
and target 2 base margins but weakens target 1, so the next useful
decision-grade step is a cross-seed fitted-ringdown robustness summary rather
than another target-specific seed89 run.

Stage 11HU: cross-seed fitted-ringdown summary.

Run 748 compares the seed21 and seed89 all-target summaries from runs 743 and
747. Across six seed-target base rows, all rows remain exact and moderate. The
best truth-preserving diagnostic objective is unchanged by seed on all targets:
veryhigh for target 0 and late_high for targets 1 and 2. Seed89 strengthens
the target-0 base margin to 1.077x seed21 and target-2 to 1.242x seed21, but
weakens target-1 to 0.834x seed21. This is the main residual uncertainty in
the added-seed fitted-ringdown branch. The production rule is still unchanged:
base remains the coordinate-update objective, and diagnostic variants remain
target-specific reporting evidence. The next GPU branch should use a different
bounded physics stress rather than another seed in this exact/moderate branch.

Stage 11HV: seed89 target-1 Tx/Rx=50 ringdown035 diagnostic.

Run 749 starts that next bounded physics stress by increasing the seed89
target-1 fitted-ringdown scale from 0.25 to 0.35 while preserving the same
Tx/Rx=50 final-state grid, source-fit grid, and diagnostic objectives. The base
objective recovers exact truth x=250 mm, z=100 mm, r=6 mm with a moderate
6.281e-04 gap against r=6.25 mm. This is slightly stronger than the ringdown025
seed89 target-1 base gap of 5.983e-04, so stronger fitted ringdown does not
worsen the center-target sensitivity found in run 748. Late_high remains the
strongest diagnostic at 9.564e-04 and 1.523x base. The next useful GPU check is
ringdown035 target 2 before deciding whether this stronger-ringdown branch
deserves an all-target package.

Stage 11HW: seed89 target-2 Tx/Rx=50 ringdown035 diagnostic.

Run 750 extends ringdown035 to target 2 with the same bounded target-2 grid as
run 745. The base objective recovers exact truth x=350 mm, z=120 mm, r=8 mm
with a strong 1.039e-03 gap against r=7.25 mm, improving over the ringdown025
seed89 target-2 base gap of 9.936e-04 and upgrading the confidence label from
moderate to strong. Late_high remains strongest at 1.682e-03 and 1.619x base,
while all diagnostics preserve truth geometry. Runs 749-750 therefore show
ringdown035 does not destabilize the center or deep targets. Target 0 remains
the open all-target gap and should be run next before packaging ringdown035.

Stage 11HX: seed89 target-0 Tx/Rx=50 ringdown035 diagnostic.

Run 751 completes the ringdown035 target-specific GPU set with the shallow
target. The base objective recovers exact truth x=150 mm, z=80 mm, r=5 mm
with a moderate 6.142e-04 gap against r=5.25 mm, improving over the
ringdown025 seed89 target-0 base gap of 5.798e-04. Veryhigh remains the
strongest target-0 diagnostic at 8.229e-04 and 1.340x base, while late and
late_high still weaken target 0. Runs 749-751 now close the stronger-ringdown
target set: target 0 is exact/moderate, target 1 is exact/moderate, and target
2 is exact/strong. The next step is a compact ringdown035 all-target summary.

Stage 11HY: ringdown035 fitted-ringdown all-target summary.

Run 752 packages the ringdown035 target-specific GPU branch from runs 749-751.
All three seed89 targets remain exact after increasing the fitted-ringdown
scale from 0.25 to 0.35. Target 0 has a moderate 6.142e-04 base gap, target 1
has a moderate 6.281e-04 base gap, and target 2 has a strong 1.039e-03 base
gap. Relative to the seed89 ringdown025 package, the base margins increase by
1.059x, 1.050x, and 1.046x for targets 0, 1, and 2 respectively. The
diagnostic pattern is unchanged: veryhigh remains strongest for target 0,
while late_high remains strongest for targets 1 and 2. Across 15 diagnostic
ratio rows, no diagnostic changes the selected truth geometry. The next
decision-grade step is a cross-condition fitted-ringdown summary comparing
seed89 ringdown025 and ringdown035 before starting another GPU physics branch.

Stage 11HZ: cross-condition fitted-ringdown summary.

Run 753 compares the seed89 ringdown025 and ringdown035 all-target summaries.
Across six condition-target base rows, all rows remain exact. Ringdown035 is
stronger than ringdown025 on all targets, with margin ratios of 1.059, 1.050,
and 1.046 for targets 0, 1, and 2. Target 2 upgrades from moderate to strong
confidence; targets 0 and 1 remain moderate. The best truth-preserving
diagnostic objective is unchanged across conditions: veryhigh for target 0 and
late_high for targets 1 and 2. This closes the stronger-ringdown branch as a
robustness confirmation rather than a new update-rule candidate. The next
substantive GPU branch should move to a different bounded physics stress while
keeping the same target table and objective-diagnostic reporting structure.

Stage 12A: seed89 target-1 Tx/Rx=60 ringdown025 acquisition diagnostic.

Run 754 starts the acquisition-geometry robustness branch by widening Tx/Rx
from 50 mm to 60 mm while preserving the seed89 ringdown025 source mismatch,
truth final state, source-fit grid, and objective-diagnostic matrix. The
center target remains exact at x=250 mm, z=100 mm, r=6 mm with a moderate
5.319e-04 base gap against r=6.25 mm. This is 0.889x the comparable Tx/Rx=50
seed89 target-1 base margin, so Tx/Rx=60 should be treated as a real
lower-margin acquisition sensitivity rather than hidden in an aggregate.
Late_high remains the strongest truth-preserving diagnostic at 7.784e-04 and
1.463x base. The next GPU row should be Tx/Rx=60 target 2 before packaging or
abandoning the acquisition-geometry branch.

Stage 12B: seed89 target-2 Tx/Rx=60 ringdown025 acquisition diagnostic.

Run 755 extends the Tx/Rx=60 branch to the deep target. The coordinate state
remains exact at x=350 mm, z=120 mm, r=8 mm, but the base margin drops to a
weak 4.319e-04 gap against r=8.75 mm. This is only 0.435x the comparable
Tx/Rx=50 seed89 target-2 base margin, and late_high also drops to 0.418x its
Tx/Rx=50 margin despite remaining the strongest truth-preserving diagnostic at
6.300e-04 and 1.459x base. This is the first weak confidence row in the
restored substantive branch and should be treated as an acquisition-geometry
robustness limit, not hidden by exact geometry. The next GPU row should be
Tx/Rx=60 target 0 so the branch can be interpreted across all targets.

Stage 12C: seed89 target-0 Tx/Rx=60 ringdown025 acquisition diagnostic.

Run 756 completes the Tx/Rx=60 target-specific acquisition branch with the
shallow target. The base objective remains exact at x=150 mm, z=80 mm, r=5 mm
with a moderate 5.193e-04 gap against r=5.25 mm, which is 0.896x the
comparable Tx/Rx=50 seed89 target-0 base margin. Veryhigh remains the
strongest truth-preserving target-0 diagnostic at 6.450e-04 and 1.242x base,
while late and late_high weaken the shallow row. Runs 754-756 now close the
Tx/Rx=60 target set: target 0 is exact/moderate, target 1 is exact/moderate,
and target 2 is exact/weak. The next step is a compact all-target Tx/Rx=60
summary that compares directly against the Tx/Rx=50 seed89 package.

Stage 12D: Tx/Rx=60 fitted-ringdown all-target summary.

Run 757 packages the Tx/Rx=60 target-specific acquisition branch from runs
754-756. All three seed89 targets remain exact after widening Tx/Rx from
50 mm to 60 mm, but the confidence profile degrades: target 0 is
exact/moderate with a 5.193e-04 base gap, target 1 is exact/moderate with a
5.319e-04 base gap, and target 2 is exact/weak with a 4.319e-04 base gap.
Relative to the Tx/Rx=50 seed89 package, the base margins are 0.896x, 0.889x,
and 0.435x for targets 0, 1, and 2. The best truth-preserving diagnostic
objective remains unchanged: veryhigh for target 0 and late_high for targets
1 and 2. This is an exact-but-margin-degraded acquisition result, with target
2 as the limiting row. The next CPU step should compare Tx/Rx=50 and Tx/Rx=60
packages directly before launching another GPU branch.

Stage 12E: cross-Tx/Rx condition fitted-ringdown summary.

Run 758 compares the seed89 Tx/Rx=50 and Tx/Rx=60 all-target packages. Across
six condition-target rows, all selected geometries remain exact, but Tx/Rx=60
is weaker on every target. The Tx/Rx60/Tx/Rx50 base-margin ratios are 0.896,
0.889, and 0.435 for targets 0, 1, and 2. The deep target is the limiting row:
it drops from moderate to weak confidence while preserving exact geometry. The
best truth-preserving diagnostic objective is unchanged across Tx/Rx
conditions, with veryhigh on target 0 and late_high on targets 1 and 2. This
closes the Tx/Rx=60 branch as an exact-but-weaker acquisition condition. Do
not widen Tx/Rx further before integrating this degradation.

Stage 12F: Tx/Rx=60 target-2 fine-radius diagnostic.

Run 759 tests whether the weak Tx/Rx=60 target-2 row is a coarse-grid artifact
by fixing target 2 at x=350 mm and z=120 mm and scanning radius from 7.5 mm to
9.5 mm in 0.125 mm steps. The base objective again selects the exact
r=8.0 mm truth radius, but the nearest fine-grid competitor is r=7.875 mm with
a weak 4.330e-04 gap. This closely matches the coarse run755 margin of
4.319e-04, confirming that the weak target-2 confidence is a genuine shallow
radius basin under Tx/Rx=60 rather than a discretization artifact. Late_high
remains strongest at 6.851e-04 and 1.582x base, but only as reporting evidence.
The next useful GPU check is an intermediate Tx/Rx=55 target-2 row to locate
where the confidence degradation begins between Tx/Rx=50 and Tx/Rx=60.

Stage 12G: seed89 target-2 Tx/Rx=55 ringdown025 acquisition diagnostic.

Run 760 tests the midpoint between the moderate Tx/Rx=50 target-2 result and
the weak Tx/Rx=60 target-2 result. The base objective remains exact at
x=350 mm, z=120 mm, r=8 mm, but the margin is weak at 4.605e-04 against
r=8.75 mm. This is only 0.463x the Tx/Rx=50 seed89 target-2 base margin and
only slightly stronger than Tx/Rx=60. Late_high remains strongest at
7.241e-04 and 1.573x base. The confidence transition therefore begins before
55 mm; the next bounded GPU point should be Tx/Rx=52.5 for target 2.

Stage 12H: seed89 target-2 Tx/Rx=52.5 ringdown025 acquisition diagnostic.

Run 761 tests the midpoint between Tx/Rx=50 and Tx/Rx=55 for the target-2
acquisition sensitivity. The base objective remains exact at x=350 mm,
z=120 mm, r=8 mm, but the margin is still weak at 4.725e-04 against r=8.75 mm.
This is only 0.475x the Tx/Rx=50 target-2 base margin, while late_high remains
strongest at 7.592e-04 and 1.607x base. The confidence transition is now
narrowed to 50-52.5 mm, and the margin drop appears sharp immediately beyond
50 mm rather than gradual across 52.5-60 mm. The next bounded GPU point should
be Tx/Rx=51.25 for target 2.

Stage 12I: seed89 target-2 Tx/Rx=51.25 ringdown025 acquisition diagnostic.

Run 762 tests the midpoint between Tx/Rx=50 and Tx/Rx=52.5. Target 2 again
remains exact at x=350 mm, z=120 mm, r=8 mm, but the base margin is weak at
4.753e-04 against r=8.75 mm. This is 0.478x the Tx/Rx=50 target-2 base margin
and nearly identical to the Tx/Rx=52.5 weak row. Late_high remains strongest
at 7.660e-04 and 1.612x base. The confidence transition is now constrained to
50-51.25 mm, indicating an abrupt margin drop immediately beyond the 50 mm
acquisition offset. The next bounded GPU point should be Tx/Rx=50.625 for
target 2.

Stage 12J: seed89 target-2 Tx/Rx=50.625 ringdown025 acquisition diagnostic.

Run 763 tests the midpoint between Tx/Rx=50 and Tx/Rx=51.25. Target 2 remains
exact at x=350 mm, z=120 mm, r=8 mm, but the base margin is weak at 4.753e-04
against r=8.75 mm, again 0.478x the Tx/Rx=50 target-2 base margin. The run is
numerically identical to Tx/Rx=51.25 because both requested offsets round to
the same effective 1 mm receiver-index layout: +51 receiver cells for the first
four source positions, with the fifth receiver clamped at the acquisition
boundary. The transition is therefore between effective receiver offsets of
+50 and +51 cells, not a smooth sub-millimeter Tx/Rx change. Do a CPU threshold
summary next before spending GPU time on more fractional offsets.

Stage 12K: seed89 target-2 Tx/Rx receiver-cell threshold summary.

Run 764 packages the comparable target-2 Tx/Rx branch from runs 745, 763, 762,
761, 760, and 755. All six rows preserve the exact target-2 geometry, but the
confidence pattern is moderate only at Tx/Rx=50 mm and weak for every tested
offset whose dominant receiver layout is +51 cells or wider. The first weak
row is Tx/Rx=50.625 mm with a 4.753e-04 base margin, 0.478x the Tx/Rx=50
margin. Tx/Rx=50.625 and 51.25 mm share the same receiver layout
51;51;51;51;49 and produce identical metrics, so further fractional bisection
is not justified under nearest grid-index receiver sampling. The next
substantive step should either change acquisition geometry enough to alter the
receiver indices or implement/test interpolated receiver sampling before
claiming sub-grid Tx/Rx behavior.

Stage 12L: linear receiver-sampling implementation and target-2 midpoint.

The coordinate optimizer now has a backward-compatible `--receiver-sampling`
option. `nearest` preserves the historical grid-index receiver recording, while
`linear` records a weighted x-interpolation between adjacent receiver cells.
Focused tests cover scan-position construction and the existing threshold
summary, a tiny GPU smoke verifies 6-entry linear receiver positions through
the gpu-cpml batch recorder, and the full suite passes with 288 tests.

Run 765 uses linear receiver sampling at Tx/Rx=50.3125 mm for the seed89
target-2 ringdown025 branch. The recovered state remains exact at x=350 mm,
z=120 mm, r=8 mm, but the base margin is weak at 4.769e-04 against r=8.75 mm.
This is 0.480x the nearest-grid Tx/Rx=50 margin and 1.0035x the nearest-grid
Tx/Rx=50.625/51.25 weak branch. Interpolated sampling therefore does not
restore the moderate Tx/Rx=50 confidence at this midpoint. Run the linear
Tx/Rx=50.000 baseline next before doing more sub-grid bisection.

Stage 12M: linear receiver-sampling target-2 smaller midpoint.

Before launching the next GPU job, the exact Tx/Rx=50.000 linear receiver
layout was audited and found to reduce to the same samples as nearest-grid
Tx/Rx=50.000, so that duplicate GPU baseline was skipped. Run 766 instead
tests linear Tx/Rx=50.15625. Target 2 remains exact at x=350 mm, z=120 mm,
r=8 mm, but the base margin is weak at 4.773e-04 against r=8.75 mm. This is
0.480x the nearest-grid Tx/Rx=50 margin and 1.0007x the linear Tx/Rx=50.3125
margin. The linear-sampling confidence transition is therefore very sharp near
the integer-cell Tx/Rx=50 baseline. The next bounded GPU point is linear
Tx/Rx=50.078125.

Stage 12N: linear receiver-sampling target-2 7.8125% midpoint.

Run 767 tests linear Tx/Rx=50.078125. Target 2 again remains exact at
x=350 mm, z=120 mm, r=8 mm, but the base margin is weak at 4.774e-04 against
r=8.75 mm. This is 0.4805x the nearest-grid Tx/Rx=50 margin, 1.0003x the
linear Tx/Rx=50.15625 margin, and 1.0010x the linear Tx/Rx=50.3125 margin.
The three nonzero linear offsets tested so far are effectively on the same weak
plateau. Create a compact linear-threshold summary before launching any
additional bisection, with Tx/Rx=50.0390625 as the next possible GPU point.

Stage 12O: linear receiver-sampling target-2 threshold summary.

Run 768 packages the nearest Tx/Rx=50 baseline, the three nonzero linear
receiver offsets, and the nearest +51-layout reference. All three nonzero
linear rows are exact/weak, with base-margin ratios to Tx/Rx=50 of 0.4805,
0.4804, and 0.4800. The nearest +51 reference is 0.4783x baseline. The linear
branch therefore sits on the same weak plateau for every tested nonzero
receiver perturbation, down to 0.078125 cells. A final Tx/Rx=50.0390625 GPU
point would only bound the onset below that value; the branch-level conclusion
is already exact-but-weak for tested nonzero +51 contribution.

Stage 12P: linear receiver-sampling target-2 final lower-bound bisection.

Run 769 tests linear Tx/Rx=50.0390625, half the smallest nonzero perturbation
from the previous summary. Target 2 remains exact at x=350 mm, z=120 mm,
r=8 mm, but the base margin is weak at 4.775e-04 against r=8.75 mm. This is
0.4806x the nearest-grid Tx/Rx=50 margin and 1.0002x the linear Tx/Rx=50.078125
margin. The practical bisection branch is now closed: every tested nonzero
linear receiver perturbation lies on the same weak plateau. Create one final
linear threshold summary including run 769, then stop sub-grid Tx/Rx bisection
for this target/case.

Stage 12Q: final linear receiver-sampling target-2 threshold summary.

Run 770 packages the final linear receiver threshold branch with nearest
Tx/Rx=50, linear Tx/Rx=50.0390625, 50.078125, 50.15625, 50.3125, and the
nearest +51-layout reference. The nearest Tx/Rx=50 row is exact/moderate.
Every tested nonzero linear row is exact/weak, with base-margin ratios of
0.4806, 0.4805, 0.4804, and 0.4800 relative to Tx/Rx=50. The nearest +51
layout is exact/weak at 0.4783x. Stop target-2 sub-grid Tx/Rx bisection for
this seed/case; the next substantive branch should change a different factor
instead of pushing below a 0.0390625-cell receiver perturbation.

Stage 12R: seed21 target-2 linear receiver-sampling replication.

Run 771 changes the seed/case factor while holding the final seed89 sub-grid
offset fixed at linear Tx/Rx=50.0390625. Target 2 remains exact at x=350 mm,
z=120 mm, r=8 mm, and the base margin is 5.770e-04 against r=8.75 mm. This is
a 0.721x drop relative to the seed21 nearest-grid Tx/Rx=50 baseline from run
741, but the confidence label remains moderate. The same linear offset was
weak for seed89, so the seed89 weak plateau should now be treated as
seed/case-sensitive rather than universal. The next bounded GPU check should
test seed21 at the larger linear Tx/Rx=50.3125 midpoint from run 765.

Stage 12S: seed21 target-2 larger linear receiver-sampling midpoint.

Run 772 tests seed21 target 2 at linear Tx/Rx=50.3125, matching the seed89
midpoint from run 765. The recovered geometry remains exact and the base margin
is 5.779e-04 against r=8.75 mm, again moderate. This is 0.722x the seed21
nearest-grid Tx/Rx=50 baseline and 1.0016x the run 771 lower-bound offset, so
seed21 forms a moderate plateau across the two tested nonzero linear offsets.
At the same Tx/Rx=50.3125 offset, seed89 was weak with a 4.769e-04 margin.
Create a compact cross-seed linear receiver comparison before spending another
GPU run on this branch.

Stage 12T: cross-seed linear receiver-sampling target-2 summary.

Run 773 summarizes the seed21 and seed89 target-2 linear receiver evidence.
Both seeds degrade under nonzero linear receiver sampling, but they separate
cleanly in classification. Seed21 has two exact/moderate nonzero-linear rows
at 0.721-0.722x its nearest-grid Tx/Rx=50 margin. Seed89 has two exact/weak
nonzero-linear rows at 0.480-0.481x its nearest-grid Tx/Rx=50 margin.
Late_high is the best truth-preserving diagnostic for every row. Stop
sub-grid offset bisection; the next GPU question is whether a third comparable
seed follows the seed21 moderate plateau or the seed89 weak plateau.

Stage 12U: seed13 target-2 linear receiver-sampling midpoint replication.

Run 774 tests a third comparable target-2 seed at linear Tx/Rx=50.3125. Seed13
remains exact at x=350 mm, z=120 mm, r=8 mm, and the base margin is
6.008e-04 against r=8.75 mm. This is 0.741x the seed13 nearest-grid Tx/Rx=50
baseline from run 521 and remains moderate. Seed13 therefore follows the
seed21 moderate plateau rather than the seed89 weak plateau. Unlike the
seed21/seed89 rows, `late` is narrowly the strongest truth-preserving
diagnostic. Update the cross-seed summary with seed13 included before launching
another GPU replication.

Stage 12V: three-seed cross-seed linear receiver-sampling summary.

Run 775 updates the cross-seed target-2 summary with seed13. The branch now has
eight rows across seed13, seed21, and seed89. All rows preserve exact geometry.
Seed13 has a nonzero-linear ratio of 0.741x and remains moderate, seed21 has
nonzero-linear ratios of 0.721-0.722x and remains moderate, and seed89 has
nonzero-linear ratios of 0.480-0.481x and is weak. The linear receiver effect
therefore degrades target-2 confidence but does not universally force weak
classification. Stop this sub-grid branch unless a fourth seed is needed for
frequency estimation; the next GPU branch should change a different factor.

Stage 12W: seed89 target-1 linear receiver-sampling midpoint.

Run 776 changes target while holding seed89 and linear Tx/Rx=50.3125 fixed.
The full 27-candidate target-1 grid remains exact at x=250 mm, z=100 mm,
r=6 mm, with a base margin of 5.986e-04 against r=6.25 mm. This is 1.0004x
the nearest-grid target-1 baseline from run 746 and remains moderate.
Therefore the seed89 nonzero-linear weak plateau is not an all-target
acquisition effect; it is currently specific to target 2. Late_high remains
the strongest truth-preserving target-1 diagnostic. The next GPU check should
be target 0 at the same linear Tx/Rx=50.3125 offset, or a compact target
sensitivity summary if GPU time is redirected.

Stage 12X: seed89 target-0 linear receiver-sampling midpoint.

Run 777 tests the remaining shallow target at linear Tx/Rx=50.3125. Target 0
remains exact at x=150 mm, z=80 mm, r=5 mm, with a base margin of 5.789e-04
against r=5.25 mm. This is 0.9985x the nearest-grid target-0 baseline from run
744 and remains moderate. Together with run 776, this confirms that the seed89
weak nonzero-linear plateau is target-2-specific among the three tested
targets. Veryhigh remains the strongest target-0 diagnostic. Create a compact
all-target seed89 linear receiver summary next.

Stage 12Y: seed89 all-target linear receiver-sampling summary.

Run 778 packages the seed89 all-target linear receiver comparison at
Tx/Rx=50.3125. Target 0 is exact/moderate at 0.998x its nearest-grid Tx/Rx=50
baseline, target 1 is exact/moderate at 1.000x, and target 2 is exact/weak at
0.480x. The target-2 weak plateau is therefore not shared by shallow or center
targets. Combined with the three-seed summary, the linear receiver sensitivity
is both seed-sensitive and target-specific. Move to a different acquisition or
source factor for target 2 before launching more sub-grid receiver runs.

Stage 12Z: seed89 target-2 ringdown035 linear receiver-sampling stress.

Run 779 tests the target-2 seed89 linear Tx/Rx=50.3125 midpoint under the
stronger ringdown035 source condition with a full 27-candidate local grid. The
truth remains exact at x=350 mm, z=120 mm, r=8 mm, but the base margin is only
4.945e-04 against the coupled z=121 mm, r=8.75 mm competitor. This is 0.476x
the nearest-sampled ringdown035 baseline from run 750 and remains weak, while
being only slightly larger than the ringdown025 linear margin from run 765.
Late_high is the strongest truth-preserving diagnostic at 1.689x base, but it
does not change the base confidence class. Stop small Tx/Rx bisection here
unless a reporting figure needs a compact cross-ringdown summary.

Stage 13A: seed89 target-2 source-density linear receiver-sampling rescue.

Run 780 repeats the seed89 target-2 linear Tx/Rx=50.3125 ringdown025 condition
with 7 sources and a full 27-candidate local grid. The truth remains exact and
the same z=121 mm, r=8.75 mm competitor remains second, but the base margin
rises to 6.453e-04. This is 1.353x the 5-source linear baseline from run 765
and changes the confidence label from weak to moderate. It is still only
0.649x the nearest-grid Tx/Rx=50 baseline from run 745, so source density
mitigates but does not eliminate the linear receiver ambiguity. The next
bounded source-density check is a single 9-source target-2 run at the same
condition.

Stage 13B: seed89 target-2 9-source source-density linear receiver check.

Run 781 repeats the target-2 linear Tx/Rx=50.3125 ringdown025 condition with 9
sources. The truth remains exact and the row stays moderate, but the base
margin is 5.439e-04, only 1.140x the 5-source linear baseline and 0.843x the
7-source margin from run 780. The source-density rescue is therefore real but
not monotonic; 7 sources is the best of the tested 5/7/9-source settings. Close
the ringdown025 source-density sweep and test the 7-source setting under
ringdown035 next.

Stage 13C: seed89 target-2 7-source ringdown035 linear receiver transfer.

Run 782 tests whether the 7-source rescue transfers to ringdown035. The truth
remains exact and the base row becomes moderate with a 6.320e-04 margin against
the same z=121 mm, r=8.75 mm competitor. This is 1.278x the 5-source
ringdown035 linear row from run 779 and 0.979x the 7-source ringdown025 row
from run 780. The rescue therefore transfers across the two tested ringdown
levels, but the margin remains only 0.608x the nearest-grid ringdown035
baseline from run 750. Close the target-2 linear receiver source-density branch
unless a compact decision figure is needed.

Stage 13D: seed89 target-2 7-source Tx/Rx=60 acquisition transfer.

Run 783 tests whether the 7-source mitigation also transfers to the separate
Tx/Rx=60 weak target-2 condition. The truth remains exact and the base row
crosses from weak in run 755 to moderate, with a 5.101e-04 margin against the
same z=121 mm, r=8.75 mm competitor. This is 1.181x the 5-source Tx/Rx=60
baseline but still only 0.513x the Tx/Rx=50 seed89 target-2 baseline from run
745. Source density therefore mitigates two independent weak target-2
conditions, but it should not be described as full recovery to the best
nearest-grid acquisition.

Stage 13E: seed89 target-0 7-source Tx/Rx=60 specificity check.

Run 784 tests whether the 7-source Tx/Rx=60 benefit is target-2-only. Target 0
remains exact/moderate and its base margin rises from 5.193e-04 in the
5-source baseline run 756 to 5.677e-04, a 1.093x improvement. This is a smaller
effect than the target-2 weak-to-moderate rescue from run 783, but it shows
that added source density also improves an already moderate shallow target.
Run target 1 at the same 7-source Tx/Rx=60 condition before creating an
all-target source-density comparison.

Stage 13F: seed89 target-1 7-source Tx/Rx=60 specificity check.

Run 785 completes the all-target 7-source Tx/Rx=60 check and is a negative
transfer result for the center target. The recovered state remains exact, but
the base target-1 margin drops to 3.489e-04, only 0.656x the 5-source target-1
baseline from run 754, and the confidence label changes from moderate to weak.
Together with runs 783 and 784, the branch is mixed: 7 sources rescues target 2
from weak to moderate and mildly improves target 0, but degrades target 1. Do
not summarize this as a monotonic source-density benefit. Run one bounded
target-1 source-count follow-up, preferably 9 sources on the same 12-candidate
grid, to determine whether the weak row is specific to the 7-source aperture or
to added Tx/Rx=60 source density more generally.

Stage 13G: seed89 target-1 9-source Tx/Rx=60 aperture follow-up.

Run 786 repeats the target-1 Tx/Rx=60 ringdown025 check with 9 sources. The
truth remains exact and the base margin recovers to 5.182e-04, which is 1.485x
the weak 7-source margin from run 785 and 0.974x the original 5-source baseline
from run 754. The row is moderate again. The target-1 failure in run 785 is
therefore aperture/source-placement sensitive rather than evidence that added
source density generally hurts target 1. Late_high is the strongest
truth-preserving diagnostic at 1.651x base. A compact source-density decision
summary is now justified, but avoid a summary-only numbered output unless it
adds a real comparison figure/table from runs 754-756 and 783-786.

Stage 13H: seed89 target-2 9-source Tx/Rx=60 source-density follow-up.

Run 787 tests whether the target-2 Tx/Rx=60 rescue from run 783 continues at 9
sources. The truth remains exact and the base margin rises to 5.780e-04,
1.339x the 5-source weak baseline from run 755 and 1.133x the 7-source
moderate row from run 783. This is still only 0.581x the Tx/Rx=50 target-2
baseline from run 745, so the recovery is real but incomplete. The
source-density behavior is acquisition dependent: Tx/Rx=60 target 2 improves
from 5 to 7 to 9 sources, while the linear Tx/Rx=50.3125 target-2 branch peaked
at 7 sources. Fix the coordinate-optimizer summary metadata scalar for
per-target radii before launching more target-2 optimizer runs.

Stage 13I: coordinate-optimizer single-target truth-radius metadata fix.

After run 787, the confidence CSV and vector truth radii were correct but the
summary JSON scalar `truth_radius_mm` still reflected the legacy common-radius
argument. Add `summary_truth_radius_mm()` so single-target optimizer summaries
write the targeted truth radius when `truth_radius_values_mm` is available,
while multi-target runs keep the legacy common scalar and the full vector.
Focused test coverage passes in `tests/test_multi_rebar_coordinate_optimizer.py`
and the full suite passes with 298 tests. Future single-target target-2 runs
will therefore report scalar `truth_radius_mm=8.0` instead of the default center
radius.

Stage 13J: seed89 target-0 9-source Tx/Rx=60 all-target completion.

Run 788 completes the all-target 9-source Tx/Rx=60 comparison after the
metadata fix. The scalar `truth_radius_mm` now correctly reports 5.0 mm for
target 0. The geometry remains exact, but the base margin drops to 4.631e-04
and the confidence label becomes weak. This is 0.892x the 5-source target-0
baseline from run 756 and 0.816x the 7-source target-0 row from run 784. The
all-target 9-source set is therefore mixed: target 2 improves, target 1
recovers from the 7-source weak row, and target 0 degrades. If another GPU
run is warranted, test an intermediate 8-source target-0 aperture; otherwise
create only a documentation-level source-density decision table.

Stage 13K: seed89 target-0 8-source Tx/Rx=60 aperture follow-up.

Run 789 tests the intermediate target-0 source count. The truth remains exact
and the base margin rises to 5.900e-04, which is 1.136x the 5-source target-0
baseline from run 756, 1.039x the 7-source row from run 784, and 1.274x the
weak 9-source row from run 788. The row is moderate. Therefore target 0 does
not degrade immediately above 7 sources; the weak result is specific to the
9-source aperture layout. Target-0 source-density behavior is nonmonotonic, so
the next bounded check is target 1 at 8 sources, where the branch currently has
weak at 7 and moderate at 9.

Stage 13L: seed89 target-1 8-source Tx/Rx=60 aperture follow-up.

Run 790 tests the intermediate target-1 source count. The truth remains exact,
but the base margin is 4.999e-04 and is still labelled weak, just below the
moderate cutoff. This is 1.433x the 7-source weak row from run 785, 0.965x the
9-source moderate row from run 786, and 0.940x the original 5-source baseline
from run 754. The center target therefore improves strongly from 7 to 8
sources but does not cross to moderate until 9 sources. Late_high is the
strongest truth-preserving diagnostic at 1.492x base. Run target 2 at 8 sources
only if the all-target 8-source set is needed before a compact
documentation-level source-density synthesis.

Stage 13M: seed89 target-2 8-source Tx/Rx=60 aperture follow-up.

Run 791 completes the all-target 8-source Tx/Rx=60 check. The truth remains
exact and the base target-2 margin is 5.243e-04, which is 1.214x the 5-source
weak baseline from run 755, 1.028x the 7-source moderate row from run 783, and
0.907x the 9-source moderate row from run 787. Target 2 is therefore the
smoothest of the three targets in the Tx/Rx=60 source-density branch: 5 sources
is weak, while 7, 8, and 9 sources are all moderate. This does not produce a
general monotonic rule, because target 0 peaks at 8 and dips at 9 while target
1 remains borderline weak at 8 and only returns to moderate at 9. Before
launching another GPU branch, create a compact source-density decision
synthesis from runs 754-756 and 783-791 so the next acquisition test is chosen
from the complete 5/7/8/9-source evidence rather than from a single target.

Stage 13N: Tx/Rx=60 source-density synthesis and custom aperture support.

The compact source-density synthesis across runs 754-756 and 783-791 shows no
uniform source count that gives moderate rows for all targets: 5 sources misses
target 2, 7 and 8 sources miss target 1, and 9 sources misses target 0. The
branch should therefore be treated as aperture-layout sensitive rather than a
monotonic source-density rule. Add a tested `--scan-x-values-mm` option to the
coordinate optimizer so the next GPU run can test a nonuniform aperture instead
of only integer uniform counts. The first custom layout should be the 8-source
scan plus an exact center shot at x=250 mm: [50, 106, 162, 218, 250, 274, 330,
386, 450] mm. Run target 1 first because it is the failing 8-source row; if it
becomes moderate, repeat target 0 and target 2 with the same custom aperture.

Stage 13O: seed89 target-1 custom 8+center Tx/Rx=60 aperture test.

Run 792 tests the first custom aperture, [50, 106, 162, 218, 250, 274, 330,
386, 450] mm. The final geometry remains exact but the base target-1 margin is
4.847e-04 and remains weak. This is 0.970x the plain 8-source row from run 790
and 0.935x the uniform 9-source moderate row from run 786. The result rejects
the simple hypothesis that target 1 only needed an exact x=250 mm source added
to the 8-source layout. Do not run target 0 or target 2 with this same custom
aperture. The next custom-layout test should isolate the useful uniform
9-source flank pattern or transfer the best existing uniform settings to a
new stress condition.

Stage 13P: seed89 target-1 custom wide-center Tx/Rx=60 aperture test.

Run 793 tests a second custom aperture, [50, 106, 162, 194, 250, 298, 330,
386, 450] mm, preserving the uniform 9-source center and wider inner flanks
while avoiding the uniform 9-source near-target flank positions. The final
geometry remains exact but the base target-1 margin is 4.841e-04 and remains
weak. This is effectively tied with run 792, 0.968x the plain 8-source row, and
0.934x the uniform 9-source row. Stop the hand-tuned custom target-1 aperture
branch unless an explicit aperture-selection metric is added; the two custom
layouts did not reproduce the uniform 9-source target-1 recovery.

Stage 13Q: seed89 target-1 9-source Tx/Rx=60 ringdown035 transfer.

Run 794 transfers the best target-1 uniform aperture to the stronger
ringdown035 source stress. The final geometry remains exact and the base
margin is 5.425e-04, which is 1.047x the ringdown025 9-source row from run 786
and 1.119-1.121x the two failed custom-aperture rows from runs 792-793. The row
is moderate. This confirms that target 1's useful aperture is the full uniform
9-source pattern, not just a center shot or wider center flanks, and it remains
stable when the fitted ringdown scale increases from 0.25 to 0.35. Continue
the ringdown035 transfer branch with target 0 at its best ringdown025 uniform
source count, 8 sources.

Stage 13R: seed89 target-0 8-source Tx/Rx=60 ringdown035 transfer.

Run 795 transfers target 0's best ringdown025 source count to ringdown035. The
final geometry remains exact and the base margin is 5.955e-04, 1.009x the
ringdown025 8-source row from run 789 and 1.286x the ringdown025 9-source weak
row from run 788. The row is moderate. Target 0's preference for the 8-source
aperture therefore survives the stronger ringdown stress. Complete the
best-source-count ringdown035 transfer set with target 2 at 9 sources.

Stage 13S: seed89 target-2 9-source Tx/Rx=60 ringdown035 transfer.

Run 796 completes the target-specific best-source-count transfer set. Target 2
remains exact/moderate with a 6.059e-04 base margin, which is 1.048x the
ringdown025 9-source row from run 787 and 1.403x the original 5-source weak row
from run 755. Runs 794-796 show positive transfer for target 1 at 9 sources,
target 0 at 8 sources, and target 2 at 9 sources. The next single-question GPU
run is target 0 at 9 sources under ringdown035, because target 1 and target 2
are already moderate at 9 sources and target 0 is the only unknown for whether
uniform 9 becomes viable for all targets under stronger ringdown.

Stage 13T: seed89 target-0 9-source Tx/Rx=60 ringdown035 viability check.

Run 797 tests whether uniform 9 becomes an all-target ringdown035 aperture.
Target 0 remains exact but the base margin is 4.975e-04 and is still weak,
just below the moderate cutoff. The margin improves 1.074x over the
ringdown025 9-source weak row from run 788, but it is only 0.835x the
ringdown035 8-source row from run 795. Therefore uniform 9 remains unsuitable
as a robust all-target base-policy setting even under stronger ringdown. If the
next all-target uniform-aperture question is needed, test target 1 at 8 sources
under ringdown035 because target 0 is already moderate at 8 sources.

Stage 13U: seed89 target-1 8-source Tx/Rx=60 ringdown035 viability check.

Run 798 tests whether uniform 8 becomes an all-target ringdown035 aperture.
Target 1 remains exact but weak, with a 4.925e-04 base margin. This is 0.985x
the ringdown025 8-source row from run 790 and 0.908x the ringdown035 9-source
row from run 794. Therefore stronger ringdown does not rescue target 1 at 8
sources. Together with run 797, this closes the simple uniform 8/9 all-target
source-count search under ringdown035: uniform 9 fails target 0, and uniform 8
fails target 1. The next branch should use a principled aperture-selection
criterion or move to a different acquisition variable rather than hand-testing
nearby uniform counts.

Stage 13V: seed89 target-0 9-source Tx/Rx=60 linear-receiver ringdown035 check.

Run 799 repeats the target-0 uniform 9-source ringdown035 row with
`receiver_sampling=linear`. The result is identical to run 797 to numerical
precision: exact geometry, 4.975e-04 base margin, weak label. This is a
no-effect control because the 60 mm Tx/Rx offset and integer-mm scan positions
lie on the 1 mm grid, so linear receiver interpolation has zero fractional
weight and collapses to nearest sampling. Do not count integer-grid linear
sampling as a separate acquisition condition. A true receiver-interpolation
test would need a fractional offset such as 60.5 mm, or the next branch should
move to a different acquisition variable.

Stage 13W: seed89 target-0 9-source Tx/Rx=60.5 linear-receiver ringdown035 check.

Run 800 performs the true fractional receiver-interpolation check by changing
the Tx/Rx offset to 60.5 mm while keeping the uniform 9-source ringdown035
target-0 setup. The final geometry remains exact, but the base radius margin is
4.963e-04 and remains weak. This is 0.998x the nearest/linear 60.0 mm rows from
runs 797/799 and only 0.833x the target-0 8-source ringdown035 row from run
795. Therefore the uniform 9-source target-0 weakness is robust to a small
fractional receiver-offset perturbation. Stop this receiver-sampling rescue
path; the next branch should move to a materially different acquisition offset
or use an explicit aperture-selection criterion.

Stage 13X: seed89 all-target union15 Tx/Rx=60 ringdown035 aperture check.

Run 801 tests a 15-position union aperture containing both the target-0
8-source positions and the target-1/target-2 9-source positions. The final
geometry remains exact for all targets, but the base labels are weak/moderate/
moderate: target 0 falls to 4.522e-04, target 1 is 5.561e-04, and target 2 is
5.822e-04. The union aperture improves target 1 slightly relative to run 794
and keeps target 2 moderate, but target 0 is worse than the weak 9-source rows
and only 0.759x the target-0 8-source ringdown035 row from run 795. Do not use
dense union apertures as the next common all-target policy. The next branch
should either use a formal target-0-preserving aperture-selection criterion or
stress the target-specific 8/9/9 policy under a new seed/case.

Stage 13Y: seed21 target-0 8-source Tx/Rx=60 ringdown035 replication.

Run 802 begins cross-seed replication of the target-specific Tx/Rx=60
source-count policy. Seed21 target 0 remains exact/moderate at 8 sources with a
5.445e-04 base margin. This is 0.914x the comparable seed89 ringdown035 row
from run 795, so seed21 is weaker than seed89 on this row but still above the
moderate threshold. It is also 1.204x the seed89 union15 target-0 row from run
801. Continue the seed21 policy replication with target 1 at 9 sources, then
target 2 at 9 sources if target 1 remains moderate.

Stage 13Z: seed21 target-1 9-source Tx/Rx=60 ringdown035 replication.

Run 803 continues the seed21 target-specific source-count replication. Target 1
remains exact/moderate at 9 sources with a 5.683e-04 base margin. This is
1.048x the comparable seed89 target-1 ringdown035 row from run 794 and 1.022x
the seed89 union15 target-1 row from run 801. Seed21 has now passed the first
two target-specific policy rows: target 0 at 8 sources and target 1 at
9 sources. Complete the seed21 replication with target 2 at 9 sources under
the same Tx/Rx=60 ringdown035 stress.

Stage 13AA: seed21 target-2 9-source Tx/Rx=60 ringdown035 replication.

Run 804 completes the seed21 target-specific 8/9/9 source-count replication.
Target 2 remains exact/moderate at 9 sources with a 5.338e-04 base margin. It
is weaker than the comparable seed89 target-2 ringdown035 row from run 796
(0.881x) but still above the moderate threshold. Runs 802-804 therefore show
positive seed21 transfer for the target-specific policy: target 0 at 8 sources
is 5.445e-04, target 1 at 9 sources is 5.683e-04, and target 2 at 9 sources is
5.338e-04. The next branch should either replicate the same policy on seed13 or
create one compact seed89-vs-seed21 policy summary before launching a third
seed.

Stage 13AB: seed13 target-0 8-source Tx/Rx=60 ringdown035 replication.

Run 805 begins seed13 replication of the target-specific Tx/Rx=60 source-count
policy. Target 0 remains exact/moderate at 8 sources with a 6.075e-04 base
margin. This is 1.020x the comparable seed89 target-0 ringdown035 row from run
795 and 1.116x the seed21 target-0 row from run 802. Seed13 therefore passes
the first target-specific policy row and is currently the strongest of the
three seeds on target 0. Continue seed13 replication with target 1 at
9 sources.

Stage 13AC: seed13 target-1 9-source Tx/Rx=60 ringdown035 replication.

Run 806 continues the seed13 target-specific source-count replication. Target 1
remains exact/moderate at 9 sources with a 5.109e-04 base margin. This is
0.942x the comparable seed89 target-1 ringdown035 row from run 794 and 0.899x
the seed21 target-1 row from run 803, so seed13 passes target 1 but with the
weakest margin of the three seeds. All diagnostic objective variants preserve
the true 6.0 mm radius, and late_high is the strongest margin row. Complete the
seed13 replication with target 2 at 9 sources before making a three-seed
target-specific 8/9/9 policy summary.

Stage 13AD: seed13 target-2 9-source Tx/Rx=60 ringdown035 replication.

Run 807 completes the seed13 target-specific source-count replication. Target 2
remains exact/moderate at 9 sources with a 5.646e-04 base margin. This is
0.932x the comparable seed89 target-2 ringdown035 row from run 796 and 1.058x
the seed21 target-2 row from run 804, so seed13 sits between the previous two
seeds for target 2. Runs 805-807 therefore replicate the 8/9/9 policy on a
third seed: all three targets remain exact/moderate under Tx/Rx=60,
ringdown035 source mismatch. Create a compact three-seed policy summary with a
real comparison table and figure before launching a new acquisition branch.

Stage 13AE: three-seed target-specific Tx/Rx=60 ringdown035 policy summary.

Run 808 aggregates the nine target-specific policy rows across seed89, seed21,
and seed13. Every base row is exact/moderate: target 0 at 8 sources, target 1
at 9 sources, and target 2 at 9 sources. The weakest replicated row is target 1
seed13 at 5.109e-04, barely above the moderate cutoff, while the strongest row
is target 0 seed13 at 6.075e-04. This supports the 8/9/9 target-specific
policy under Tx/Rx=60 ringdown035 source mismatch and closes same-policy seed
replication for now. The next GPU branch should stress the weakest replicated
row first, preferably seed13 target 1 at 9 sources under a stronger source
condition.

Stage 13AF: seed13 target-1 9-source Tx/Rx=60 ringdown045 stress.

Run 809 increases the true ringdown scale from 0.35 to 0.45 on the weakest
replicated policy row, seed13 target 1 at 9 sources. The recovered geometry
remains exact and the base confidence label remains moderate, but the margin is
only 5.030e-04, 0.985x the ringdown035 baseline from run 806 and just
3.049e-06 above the moderate cutoff. This is a near-threshold pass. Run one
more bounded check at ringdown050 on the same target before extending the
stronger-stress branch to other targets.

Stage 13AG: seed13 target-1 9-source Tx/Rx=60 ringdown050 bracket.

Run 810 preserves exact geometry but crosses the production confidence cutoff:
the base margin is 4.879e-04 and the row is weak with
`radius_weak_confidence`. Ringdown050 is therefore the first failed-margin row
in the stronger-ringdown bracket, while ringdown045 remains a near-threshold
pass. Diagnostic objectives still preserve truth and late_high remains the
strongest diagnostic, so the failure is a base-confidence margin failure rather
than a geometry-selection failure. Run one midpoint check at ringdown0475 to
tighten the bracket before summarizing or extending the branch.

Stage 13AH: seed13 target-1 9-source Tx/Rx=60 ringdown0475 midpoint.

Run 811 preserves exact geometry but remains weak at the midpoint between
ringdown045 and ringdown050. The base margin is 4.963e-04, only 3.698e-06
below the moderate cutoff, while ringdown045 is 3.049e-06 above the cutoff.
The target-1 base-confidence transition is now bracketed between ringdown045
and ringdown0475. Run one tighter midpoint at ringdown04625 if a numeric
threshold estimate is needed before summarizing the stronger-ringdown branch.

Stage 13AI: seed13 target-1 9-source Tx/Rx=60 ringdown04625 midpoint.

Run 812 preserves exact geometry and lands almost exactly on the production
base-confidence cutoff. The base margin is 4.999e-04, only 1.093e-07 below
the 5e-04 moderate threshold, so the row is labeled weak with
`radius_weak_confidence`. This is a boundary confidence-margin result rather
than a geometry-selection failure: all diagnostic objective variants preserve
the true 6.0 mm target-1 radius, with late_high again the strongest diagnostic
margin. The stronger-ringdown bracket is now ringdown045 pass and
ringdown04625 weak. Run one final midpoint at ringdown045625 to estimate the
threshold before summarizing the branch.

Stage 13AJ: seed13 target-1 9-source Tx/Rx=60 ringdown045625 midpoint.

Run 813 preserves exact geometry and remains moderate at ringdown045625. The
base margin is 5.015e-04, which is 1.525e-06 above the 5e-04 cutoff and
0.997x the ringdown045 pass from run 809. Together with the weak run 812 row
at ringdown04625, this narrows the target-1 production base-confidence
threshold to the interval 0.45625-0.4625 ringdown scale. All diagnostic
objective variants still preserve truth, so the threshold is still a
confidence-margin boundary rather than a geometry-selection boundary. Run one
quarter-point midpoint at ringdown0459375 before summarizing the
stronger-ringdown target-1 branch.

Stage 13AK: seed13 target-1 9-source Tx/Rx=60 ringdown0459375 quarter-point.

Run 814 preserves exact geometry and remains moderate at ringdown0459375. The
base margin is 5.007e-04, only 7.215e-07 above the 5e-04 cutoff. Together with
the weak ringdown04625 row from run 812, this brackets the target-1 production
base-confidence threshold between 0.459375 and 0.4625 ringdown scale. The
threshold midpoint is 0.4609375, and all diagnostic objective variants still
preserve truth. Create one compact threshold summary for runs 809-814, then
shift the stronger-ringdown stress to another target rather than continuing to
split a 0.003125-wide target-1 bracket.

Stage 13AL: seed13 target-1 stronger-ringdown threshold summary.

Run 815 aggregates runs 809-814 and closes the seed13 target-1
stronger-ringdown threshold branch. The final production base-confidence
bracket is run 814 passing at ringdown0459375 with a 5.007e-04 margin versus
run 812 weak at ringdown04625 with a 4.999e-04 margin. The bracket width is
0.003125 and the midpoint estimate is 0.4609375. All base rows preserve exact
geometry, all 36 diagnostic objective rows preserve the true target-1
geometry, and base margins strictly decrease with ringdown scale. Stop slicing
target 1 and move the stronger-ringdown stress to another target at the
highest passing target-1 stress level, starting with seed13 target 2 at
9 sources and Tx/Rx=60.

Stage 13AM: seed13 target-2 9-source Tx/Rx=60 ringdown0459375 stress.

Run 816 tests seed13 target 2 at the highest passing target-1 stress level.
Target 2 remains exact/moderate at 9 sources with a 5.534e-04 production base
margin. This is 0.980x the seed13 target-2 ringdown035 baseline from run 807
and 1.105x the target-1 ringdown0459375 margin from run 814. Early-high drops
below 5e-04 but still selects the true target-2 geometry, so the production
policy remains valid while early-window high-band separability is weaker.
Complete the ringdown0459375 all-target policy check with seed13 target 0 at
8 sources and Tx/Rx=60.

Stage 13AN: seed13 target-0 8-source Tx/Rx=60 ringdown0459375 stress.

Run 817 completes the seed13 all-target check at the highest passing target-1
stress level. Target 0 remains exact/moderate at 8 sources with a 5.804e-04
production base margin, about 0.955x the seed13 target-0 ringdown035 baseline
from run 805. The late diagnostic drops below 5e-04 but still selects the true
target-0 geometry. Runs 814, 816, and 817 therefore show that the target-specific
8/9/9 policy remains exact and production-moderate for all seed13 targets at
ringdown0459375. Create a compact all-target summary before choosing the next
stress branch.

Stage 13AO: seed13 all-target ringdown0459375 policy summary.

Run 818 aggregates runs 817, 814, and 816. The seed13 target-specific 8/9/9
policy remains exact and production-moderate for all targets at
ringdown0459375: target 0 is 5.804e-04, target 1 is 5.007e-04, and target 2 is
5.534e-04. Target 1 remains the limiting production row, while target 0 and
target 2 retain larger margins. All 18 diagnostic objective rows preserve the
true target geometry; two diagnostic rows fall below 5e-04 but are not
geometry failures. The next GPU branch should test cross-seed transfer of this
highest passing target-1 stress level, starting with seed89 target 1 at
9 sources and Tx/Rx=60.

Stage 13AP: seed89 target-1 9-source Tx/Rx=60 ringdown0459375 transfer.

Run 819 tests cross-seed transfer of the highest passing seed13 target-1
stress level. Seed89 target 1 remains exact/moderate at ringdown0459375 with a
5.314e-04 production base margin. This is 1.061x the seed13 target-1 margin
from run 814 at the same stress and 0.980x the seed89 ringdown035 baseline
from run 794. All diagnostic objective variants preserve the true target-1
geometry. Continue cross-seed transfer with seed21 target 1 at the same
ringdown0459375 stress before summarizing the target-1 transfer branch.

Stage 13AQ: seed21 target-1 9-source Tx/Rx=60 ringdown0459375 transfer.

Run 820 completes the target-1 cross-seed transfer set at ringdown0459375.
Seed21 target 1 remains exact/moderate with a 5.561e-04 production base
margin. This is 1.111x the seed13 target-1 margin from run 814, 1.046x the
seed89 target-1 margin from run 819, and 0.978x the seed21 ringdown035
baseline from run 803. All diagnostic objective variants preserve truth.
Create a three-seed target-1 transfer summary from runs 814, 819, and 820.

Stage 13AR: target-1 three-seed ringdown0459375 transfer summary.

Run 821 aggregates runs 819, 820, and 814. Target 1 remains exact and
production-moderate for seed89, seed21, and seed13 at ringdown0459375. Seed13
is the limiting seed with a 5.007e-04 base margin, only 7.215e-07 above the
cutoff, while seed89 is 5.314e-04 and seed21 is 5.561e-04. Retention relative
to each seed's ringdown035 target-1 baseline is tightly clustered at
0.978-0.980. This supports ringdown0459375 as a reproducible target-1 stress
level. Extend the ringdown0459375 cross-seed transfer branch to other targets,
starting with seed89 target 2 at 9 sources and Tx/Rx=60.

Stage 13AS: seed89 target-2 9-source Tx/Rx=60 ringdown0459375 transfer.

Run 822 extends the ringdown0459375 transfer branch to seed89 target 2. The
run remains exact/moderate with a 5.960e-04 production base margin, 9.601e-05
above the cutoff. It retains 0.984x of the seed89 target-2 ringdown035
baseline from run 796 and is 1.121x stronger than seed89 target 1 at the same
ringdown0459375 stress from run 819. All diagnostic objective variants
preserve the true target-2 geometry and remain above the production cutoff.
Complete the seed89 all-target ringdown0459375 transfer set with target 0 at 8
sources and Tx/Rx=60, then summarize seed89 targets 0, 1, and 2.

Stage 13AT: seed89 target-0 8-source Tx/Rx=60 ringdown0459375 transfer.

Run 823 completes the seed89 target-specific 8/9/9 transfer inputs at
ringdown0459375. Target 0 remains exact/moderate with a 5.649e-04 production
base margin, 6.485e-05 above the cutoff. It retains 0.949x of its seed89
target-0 ringdown035 baseline from run 795, is 1.063x the seed89 target-1
margin from run 819 at the same stress, and is 0.948x the seed89 target-2
margin from run 822. The late and late_high diagnostic rows fall below 5e-04
but preserve the true target-0 geometry. Create a seed89 all-target
ringdown0459375 transfer summary from runs 823, 819, and 822 before extending
the same all-target check to seed21.

Stage 13AU: seed89 all-target ringdown0459375 transfer summary.

Run 824 aggregates runs 823, 819, and 822. Seed89 passes the all-target
ringdown0459375 transfer check: target 0 is 5.649e-04, target 1 is 5.314e-04,
and target 2 is 5.960e-04 under the target-specific 8/9/9 source-count policy.
Target 1 remains the limiting production row, 3.144e-05 above the cutoff.
All 18 objective diagnostic rows preserve the true target geometry; only
target 0 under late and late_high drops below 5e-04. Extend the same all-target
transfer check to seed21, where target 1 already passes from run 820. Start
with seed21 target 2 at 9 sources and Tx/Rx=60, then complete target 0 at 8
sources.

Stage 13AV: seed21 target-2 9-source Tx/Rx=60 ringdown0459375 transfer.

Run 825 extends seed21 beyond the already passing target-1 row from run 820.
Target 2 remains exact/moderate at ringdown0459375 with a 5.252e-04 production
base margin, 2.522e-05 above the cutoff. It retains 0.984x of the seed21
target-2 ringdown035 baseline from run 804. The early_high diagnostic drops to
4.930e-04 but preserves the true target-2 geometry, matching the seed13
target-2 diagnostic fragility. Complete seed21 all-target transfer with target
0 at 8 sources and Tx/Rx=60, then summarize seed21 targets 0, 1, and 2.

Stage 13AW: seed21 target-0 8-source Tx/Rx=60 ringdown0459375 transfer.

Run 826 completes the seed21 all-target ringdown0459375 transfer inputs.
Target 0 remains exact/moderate with a 5.151e-04 production base margin, only
1.514e-05 above the cutoff. It retains 0.946x of the seed21 target-0
ringdown035 baseline from run 802 and is the limiting seed21 production row so
far, below target 1 from run 820 and target 2 from run 825. The late and
late_high diagnostics fall below 5e-04 but preserve the true target-0
geometry. Create a seed21 all-target summary from runs 826, 820, and 825.

Stage 13AX: seed21 all-target ringdown0459375 transfer summary.

Run 827 aggregates runs 826, 820, and 825. Seed21 passes the all-target
ringdown0459375 transfer check: target 0 is 5.151e-04, target 1 is 5.561e-04,
and target 2 is 5.252e-04 under the target-specific 8/9/9 policy. Target 0 is
the limiting production row, only 1.514e-05 above the cutoff. All 18 objective
diagnostic rows preserve the true target geometry; weak diagnostic rows are
target 0 under late and late_high plus target 2 under early_high. Create a
cross-seed all-target summary from seed13 run 818, seed89 run 824, and seed21
run 827 before increasing ringdown stress.

Stage 13AY: three-seed all-target ringdown0459375 transfer summary.

Run 828 aggregates seed13 run 818, seed89 run 824, and seed21 run 827. The
target-specific 8/9/9 policy passes across all three seeds and all three
targets at ringdown0459375: all nine production base rows are exact and
moderate. The global limiting row is seed13 target 1 from run 814 with a
5.007e-04 margin, only 7.215e-07 above the cutoff. Seed21 target 0 is the next
tight row at 5.151e-04. All 54 objective diagnostics preserve true geometry;
seven diagnostic rows fall below 5e-04, all truth-preserving. Treat
ringdown0459375 as a reproduced boundary-level pass. Before increasing
ringdown globally, investigate whether the limiting seed13 target-1 row can be
strengthened by acquisition or objective changes.

Stage 13AZ: seed13 target-1 5-source Tx/Rx=60 ringdown0459375 acquisition
alternative.

Run 829 tests a 5-source acquisition for the global limiting seed13 target-1
row. It remains exact/moderate and raises the production base margin to
5.428e-04, improving by 4.204e-05 over the 9-source run 814 at the same
ringdown0459375 stress. All objective diagnostics preserve the true target-1
geometry; early_high is the only weak diagnostic at 4.971e-04. The result
shows that source count, not only ringdown scale, controls the boundary. Test
the same 5-source aperture at ringdown04625, where the 9-source row was weak.

Stage 13BA: seed13 target-1 5-source Tx/Rx=60 ringdown04625 acquisition
rescue.

Run 830 tests the same 5-source aperture at ringdown04625. The row is
exact/moderate with a 5.419e-04 production base margin, improving by
4.202e-05 over weak 9-source run 812 at the same stress and sitting
4.191e-05 above the cutoff. It retains 0.998x of the 5-source ringdown0459375
margin from run 829, so the previous ringdown04625 weakness was acquisition
specific rather than an unavoidable scene limit. All six objective diagnostic
rows preserve truth; early_high remains just below cutoff at 4.989e-04. Probe
the 5-source upward bracket next at ringdown046875 before deciding on
cross-seed transfer.

Stage 13BB: seed13 target-1 5-source Tx/Rx=60 ringdown046875 upward stress
probe.

Run 831 remains exact/moderate at ringdown046875 with a 5.401e-04 production
base margin, 4.012e-05 above cutoff. It loses only 1.794e-06 relative to
5-source run 830 at ringdown04625 and is still 4.023e-05 stronger than weak
9-source run 812 at ringdown04625. All six objective diagnostic rows preserve
truth, and early_high now clears cutoff at 5.023e-04. Continue the 5-source
upward bracket with ringdown0475 before summarizing or transferring this
acquisition policy.

Stage 13BC: seed13 target-1 5-source Tx/Rx=60 ringdown0475 stress probe.

Run 832 remains exact/moderate at ringdown0475 with a 5.382e-04 production
base margin, 3.820e-05 above cutoff. It loses only 1.916e-06 relative to
5-source run 831 at ringdown046875 and is still 3.831e-05 stronger than weak
9-source run 812 at ringdown04625 despite the higher ringdown stress. All six
objective diagnostic rows preserve truth and clear cutoff; early_high remains
the limiting diagnostic at 5.056e-04. Summarize the 5-source target-1
acquisition branch against the 9-source boundary before choosing cross-seed
transfer or a larger upward seed13 probe.

Stage 13BD: seed13 target-1 5-source acquisition-boundary summary.

Run 833 aggregates the seed13 target-1 9-source branch from runs 809, 813,
814, 812, 811, and 810 with the 5-source branch from runs 829-832. The
9-source branch crosses cutoff between ringdown0459375 and ringdown04625,
while the 5-source branch remains exact/moderate through ringdown0475 with a
5.382e-04 margin. At shared stress points, the 5-source aperture improves the
margin by +4.204e-05 at 0.459375, +4.202e-05 at 0.4625, and +4.190e-05 at
0.475, a stable 1.084x ratio. All 60 compared objective diagnostic rows
preserve the true target-1 geometry. Before cross-seed transfer, test whether
the same 5-source gain rescues the old 9-source ringdown050 weak row.

Stage 13BE: seed13 target-1 5-source Tx/Rx=60 ringdown050 rescue probe.

Run 834 confirms the predicted rescue. Seed13 target 1 remains exact/moderate
at ringdown050 with a 5.294e-04 production base margin, improving by
4.146e-05 over weak 9-source run 810 at the same stress and preserving a
1.085x matched-stress ratio. The run remains 2.939e-05 above cutoff, and all
six diagnostic objective rows preserve truth and clear cutoff, with early_high
at 5.178e-04. Start cross-seed transfer of the 5-source ringdown050 target-1
policy with seed89 target 1.

Stage 13BF: seed89 target-1 5-source Tx/Rx=60 ringdown050 transfer.

Run 835 starts cross-seed transfer of the 5-source ringdown050 target-1
policy. Seed89 target 1 remains exact/moderate with a 5.591e-04 production
base margin, 5.908e-05 above cutoff. This is 1.056x the seed13 run 834 margin
at the same stress and 1.052x the seed89 9-source ringdown0459375 transfer row
from run 819 despite the higher ringdown scale. All six diagnostics preserve
truth and clear cutoff. Continue target-1 transfer with seed21 at the same
5-source ringdown050 policy.

Stage 13BG: seed21 target-1 5-source Tx/Rx=60 ringdown050 transfer.

Run 836 completes the three-seed target-1 transfer inputs for the 5-source
ringdown050 policy. Seed21 target 1 remains exact/moderate with a 5.799e-04
production base margin, 7.992e-05 above cutoff. It is 1.095x the seed13 run
834 row and 1.037x the seed89 run 835 row at the same policy, and it is
1.043x the seed21 9-source ringdown0459375 transfer row from run 820 despite
the higher stress. All six diagnostics preserve truth and clear cutoff. Create
a three-seed target-1 ringdown050 transfer summary before extending the policy
to other targets.

Stage 13BH: three-seed target-1 5-source ringdown050 transfer summary.

Run 837 aggregates runs 834, 835, and 836. The 5-source Tx/Rx=60 ringdown050
policy transfers across seed13, seed89, and seed21 for target 1: all three
base rows are exact/moderate, all 18 diagnostic objective rows preserve truth,
and all diagnostic margins clear cutoff. The limiting row is seed13 run 834 at
5.294e-04, 2.939e-05 above cutoff. Each higher-stress 5-source row also
exceeds that seed's prior 9-source ringdown0459375 transfer margin. Extend the
policy to target 2 next, starting with seed13 target 2.

Stage 13BI: seed13 target-2 5-source Tx/Rx=60 ringdown050 target extension.

Run 838 extends the 5-source ringdown050 policy to seed13 target 2. The row is
exact/moderate with a 5.883e-04 production base margin, 8.829e-05 above
cutoff. It is 1.063x the seed13 target-2 9-source ringdown0459375 row from
run 816 and 1.042x the seed13 target-2 9-source ringdown035 baseline from run
807, despite the higher ringdown stress. All six diagnostics preserve truth
and clear cutoff, although early_high is the limiting diagnostic at
5.084e-04. Complete seed13 all-target extension with target 0 under the same
5-source ringdown050 policy.

Stage 13BJ: seed13 target-0 5-source Tx/Rx=60 ringdown050 target extension.

Run 839 completes the fixed 5-source seed13 all-target inputs at ringdown050,
but target 0 is boundary-level. The production base row remains exact/moderate
with a 5.081e-04 margin, only 8.135e-06 above cutoff, while late and late_high
diagnostics drop below cutoff but preserve truth. Target 0 is 7.231e-05 below
the old 8-source ringdown0459375 target-0 row from run 817 and is much weaker
than seed13 target 1 and target 2 at ringdown050. Test target 0 with 8 sources
at the same stress before promoting any all-target policy.

Stage 13BK: seed13 target-0 8-source Tx/Rx=60 ringdown050 acquisition
strengthening.

Run 840 confirms that the weak target-0 run 839 was mostly acquisition
limited. Restoring 8 sources at Tx/Rx=60 and ringdown050 keeps the solution
exact/moderate and raises the production base margin to 5.626e-04, a
5.444e-05 improvement over the fixed 5-source target-0 row. All six
diagnostic objective rows preserve the true target-0 geometry; late_high moves
back above cutoff, and late remains the only sub-cutoff diagnostic at
4.583e-04. The seed13 ringdown050 policy should now be summarized as a
target-specific 8/5/5 source-count policy using runs 840, 834, and 838 before
cross-seed transfer.

Stage 13BL: seed13 all-target ringdown050 8/5/5 policy summary.

Run 841 aggregates seed13 runs 840, 834, and 838. The target-specific 8/5/5
source-count policy passes all three seed13 targets at ringdown050: target 0
is 5.626e-04, target 1 is 5.294e-04, and target 2 is 5.883e-04. All
production rows are exact/moderate and above cutoff, with target 1 now the
limiting row at 2.939e-05 above cutoff. All 18 diagnostic objective rows
preserve truth; only target 0 under the late objective remains below cutoff at
4.583e-04. Transfer the policy to seed89 starting with target 0 at 8 sources,
then target 2 at 5 sources if target 0 passes.

Stage 13BM: seed89 target-0 8-source Tx/Rx=60 ringdown050 transfer.

Run 842 starts seed89 transfer of the target-specific ringdown050 policy.
Target 0 remains exact/moderate with a 5.460e-04 production base margin,
4.604e-05 above cutoff. It is 1.882e-05 weaker than seed89 target-0
ringdown0459375 run 823 and 1.654e-05 weaker than seed13 target-0
ringdown050 run 840, but still a clean production pass. All six diagnostic
objective rows preserve truth; late and late_high remain below cutoff while
slightly improving relative to run 823. Continue seed89 transfer with target 2
at 5 sources, since seed89 target 1 already passed at ringdown050 in run 835.

Stage 13BN: seed89 target-2 5-source Tx/Rx=60 ringdown050 transfer.

Run 843 shows that the seed13 8/5/5 policy does not transfer cleanly to
seed89 target 2. The true geometry remains the best candidate, but the
production base margin is only 4.415e-04 and the confidence row is weak with
`radius_weak_confidence`. Four diagnostic objective rows clear cutoff and all
six preserve truth, but early_high also drops below cutoff at 3.970e-04.
Restore the old 9-source target-2 acquisition at the same seed and ringdown050
stress before any seed89 all-target summary.

Stage 13BO: seed89 target-2 9-source Tx/Rx=60 ringdown050 rescue.

Run 844 confirms that seed89 target-2 weakness at ringdown050 is acquisition
specific. Restoring 9 sources raises the production base margin to 5.821e-04,
an improvement of 1.406e-04 over weak 5-source run 843, and removes the weak
fallback. All six diagnostic objective rows preserve truth and clear cutoff.
Seed89 should be summarized with a target-specific 8/5/9 source-count policy:
run 842 for target 0, run 835 for target 1, and run 844 for target 2.

Stage 13BP: seed89 all-target ringdown050 8/5/9 policy summary.

Run 845 aggregates seed89 runs 842, 835, and 844 as the promoted
target-specific ringdown050 policy and keeps weak run 843 as a rejected
target-2 5-source branch. Seed89 passes all three production rows as
exact/moderate: target 0 is 5.460e-04, target 1 is 5.591e-04, and target 2 is
5.821e-04. Target 0 is the limiting production row at 4.604e-05 above cutoff.
All 18 promoted diagnostic objective rows preserve truth; target 0 late and
late_high remain below cutoff. Extend transfer to seed21 next, starting with
target 0 at 8 sources because seed21 target 1 already passed in run 836.

Stage 13BQ: seed21 target-0 8-source Tx/Rx=60 ringdown050 transfer.

Run 846 is exact but weak. Seed21 target 0 selects the true
`x=150 mm, z=80 mm, r=5.0 mm` geometry, but the production base margin is
4.975e-04, missing cutoff by 2.496e-06 and triggering
`radius_weak_confidence`. All six diagnostic objective rows preserve truth,
but late and late_high are well below cutoff. Test a 9-source acquisition at
the same seed and ringdown050 stress before lowering ringdown.

Stage 13BR: seed21 target-0 9-source Tx/Rx=60 ringdown050 rescue attempt.

Run 847 rejects the 9-source rescue. It remains exact but weak with a
4.718e-04 production base margin, 2.566e-05 below the 8-source run 846
near-miss. Highband, veryhigh, and early_high diagnostics clear cutoff, but
late and late_high remain weak. Return to the stronger 8-source acquisition
and bracket the ringdown threshold next, starting with ringdown0475.

Stage 13BS: seed21 target-0 8-source Tx/Rx=60 ringdown0475 threshold bracket.

Run 848 passes at ringdown0475 with an exact/moderate production base margin
of 5.087e-04, 8.688e-06 above cutoff. It is 1.118e-05 stronger than the
ringdown050 near-miss from run 846 and 6.457e-06 weaker than the lower-stress
ringdown0459375 pass from run 826. Late and late_high remain below cutoff but
truth-preserving. Bracket upward at ringdown049375 before deciding the seed21
target-0 stress limit.

Stage 13BT: seed21 target-0 8-source Tx/Rx=60 ringdown049375 upper bracket.

Run 849 passes at ringdown049375, but only by 3.891e-07 above cutoff. The row
is exact/moderate with a 5.004e-04 production base margin, while late and
late_high remain below cutoff but truth-preserving. Treat ringdown049375 as
the practical seed21 target-0 stress limit under the current policy, with
ringdown050 still rejected. Continue seed21 transfer by testing target 2 at
ringdown049375 with the stronger 9-source acquisition.

Stage 13BU: seed21 target-2 9-source Tx/Rx=60 ringdown049375 transfer.

Run 850 confirms that seed21 target 2 passes at the seed21 target-0 practical
stress boundary when using the 9-source Tx/Rx=60 acquisition. The production
base row is exact/moderate with a 5.151e-04 margin, 1.513e-05 above cutoff,
and all six diagnostic objective rows preserve truth and clear cutoff. The row
has more reserve than seed21 target 0 run 849, so target 0 remains the seed21
limiting row. Summarize the seed21 target-specific policy next using run 849
for target 0, run 836 as the higher-stress target-1 pass, and run 850 for
target 2, with an explicit note that ringdown050 is rejected only because of
target 0.

Stage 13BV: seed21 target-specific ringdown049375 8/5/9 policy summary.

Run 851 aggregates the accepted seed21 policy rows and the rejected
ringdown050 target-0 evidence. The promoted rows are run 849 for target 0
with 8 sources at ringdown049375, run 836 for target 1 with 5 sources at the
harder ringdown050 condition, and run 850 for target 2 with 9 sources at
ringdown049375. All three production rows are exact/moderate and above cutoff:
target 0 is 5.004e-04, target 1 is 5.799e-04, and target 2 is 5.151e-04.
Target 0 is the limiting row at only 3.891e-07 above cutoff, and target 0
also rejects ringdown050 in both the 8-source and 9-source attempts. Use this
summary as the seed21 input to cross-seed stress synthesis; do not describe
seed21 as a full ringdown050 transfer.

Stage 13BW: seed21 target-0 ringdown0496875 threshold refinement.

Run 852 tests the midpoint between accepted ringdown049375 run 849 and
rejected ringdown050 run 846. The geometry remains exact, but the production
base margin is 4.990e-04, missing cutoff by 1.046e-06 and triggering
`radius_weak_confidence`. The row is 1.436e-06 weaker than run 849 and
1.449e-06 stronger than run 846, so the seed21 target-0 threshold is now
tightly bracketed between ringdown049375 and ringdown0496875. Continue with
the lower midpoint ringdown04953125 before declaring the final seed21 target-0
threshold.

Stage 13BX: seed21 target-0 ringdown04953125 lower-midpoint bracket.

Run 853 is another exact but weak seed21 target-0 near-miss. The production
base margin is 4.997e-04, only 3.270e-07 below cutoff, and the row triggers
`radius_weak_confidence`. It is 7.160e-07 weaker than accepted run 849 and
7.195e-07 stronger than rejected run 852. The accepted/failed interval is now
`[0.49375, 0.4953125)`. Test the lower midpoint ringdown049453125 next before
freezing the practical seed21 target-0 threshold.

Stage 13BY: seed21 target-0 ringdown049453125 razor-edge pass.

Run 854 passes the lower midpoint, but only by 3.148e-08 above cutoff. The
geometry is exact/moderate with no fallback warning; late and late_high
diagnostics remain below cutoff but truth-preserving. The row is 3.576e-07
weaker than accepted run 849 and 3.585e-07 stronger than failed run 853. The
accepted/failed seed21 target-0 interval is now `[0.49453125, 0.4953125)`.
Run the upper midpoint ringdown0494921875 next to test whether the accepted
threshold can move above run 854.

Stage 13BZ: seed21 target-0 ringdown0494921875 upper-midpoint rejection.

Run 855 is exact but weak. The production base margin is 4.999e-04, missing
cutoff by 1.476e-07 and triggering `radius_weak_confidence`. It is
1.791e-07 weaker than accepted run 854 and 1.793e-07 stronger than rejected
run 853. The seed21 target-0 threshold is now bracketed to
`[0.49453125, 0.494921875)`. Test ringdown04947265625 if one more refinement
is needed before summarizing the final target-0 threshold.

Stage 13CA: seed21 target-0 ringdown04947265625 final close rejection.

Run 856 is exact but weak, missing cutoff by only 5.805e-08 at
ringdown04947265625. It is 8.953e-08 weaker than accepted run 854 and
8.959e-08 stronger than rejected run 855, narrowing the target-0 interval to
`[0.49453125, 0.4947265625)`. This is tight enough for a threshold summary:
run 854 is the highest accepted point, run 856 is the nearest rejected point,
and the accepted point should be reported as a razor-edge threshold rather
than a robust reserve.

Stage 13CB: seed21 target-0 ringdown threshold summary.

Run 857 summarizes the seed21 target-0 threshold branch. The highest accepted
8-source Tx/Rx=60 row is run 854 at ringdown049453125, with a production
margin of 5.000e-04 and only 3.148e-08 reserve above cutoff. The nearest
rejected 8-source row is run 856 at ringdown04947265625, with a 4.999e-04
margin and 5.805e-08 deficit. The final accepted/failed interval is
`[0.49453125, 0.4947265625)`. Ringdown050 remains rejected, and the 9-source
run 847 rescue is exact but weaker than the 8-source ringdown050 row. Use run
854 as the practical seed21 target-0 threshold point, with an explicit
razor-edge caution.

Stage 13CC: seed21 target-0 7-source ringdown050 rescue control.

Run 858 tests the remaining simple source-count control for seed21 target 0 at
ringdown050 by reducing the acquisition to 7 sources. The run is exact but
weak: the base margin is 4.426e-04, missing the 5e-04 cutoff by 5.741e-05.
It is weaker than both the rejected 8-source row from run 846 and the rejected
9-source rescue from run 847. This closes the 7/8/9 source-count rescue branch
and reinforces the run-857 interpretation that seed21 target 0 is governed by
the fitted ringdown-strength threshold rather than a simple source-count
adjustment at ringdown050.

Stage 13CD: seed34 target-0 8-source ringdown050 fourth-seed control.

Run 859 tests the target-0 ringdown050 row on a fourth noise seed while keeping
the 8-source Tx/Rx=60 acquisition and source-mismatch stress fixed. Seed34
passes with an exact/moderate base margin of 5.311e-04, 3.109e-05 above
cutoff. Together with seed13 run 840 and seed89 run 842, this shows that
seed21 run 846 is a lower-tail near-miss rather than a universal target-0
ringdown050 failure. Continue seed34 transfer with target 1 at the 5-source
ringdown050 policy before deciding whether seed34 follows 8/5/5 or needs a
target-2 rescue.

Stage 13CE: seed34 target-1 5-source ringdown050 transfer.

Run 860 passes seed34 target 1 at ringdown050 with the 5-source Tx/Rx=60
policy. The recovered state is exact, the target-specific truth radius is
6.0 mm, and the base margin is 5.326e-04, 3.260e-05 above cutoff. Target 1 now
has accepted 5-source ringdown050 rows for seeds 13, 89, 21, and 34. The
remaining seed34 policy question is target 2, where seed13 passed at 5 sources
but seed89 required a 9-source rescue.

Stage 13CF: seed34 target-2 5-source ringdown050 transfer check.

Run 861 tests seed34 target 2 with the 5-source Tx/Rx=60 ringdown050 policy.
The row is exact but weak: the true target-2 radius remains the best candidate,
but the base margin is 4.575e-04, missing cutoff by 4.249e-05 and triggering
`radius_weak_confidence`. Highband, late, late_high, and veryhigh diagnostics
clear cutoff while preserving truth, but the production row is rejected. This
matches the seed89 target-2 pattern and requires a 9-source rescue before
summarizing seed34.

Stage 13CG: seed34 target-2 9-source ringdown050 rescue.

Run 862 rescues seed34 target 2 by restoring the 9-source Tx/Rx=60 acquisition
at ringdown050. The row is exact/moderate with a 5.257e-04 base margin,
2.569e-05 above cutoff, and all six diagnostic objective rows preserve truth
above cutoff. The source-count change improves target 2 by 6.817e-05 over weak
5-source run 861. Seed34 therefore follows an 8/5/9 target-specific policy at
ringdown050: run 859 for target 0, run 860 for target 1, and run 862 for
target 2, with run 861 retained as the rejected target-2 5-source control.

Stage 13CH: seed34 ringdown050 target-specific policy summary.

Run 863 aggregates the seed34 branch. The promoted rows are target 0 run 859
with 8 sources, target 1 run 860 with 5 sources, and target 2 run 862 with
9 sources. All three production rows are exact/moderate and above cutoff; the
limiting row is target 2 at 5.257e-04, 2.569e-05 above cutoff. All 18
diagnostic objective rows preserve truth and 16 clear cutoff; the two
sub-cutoff diagnostics are target 0 late and target 1 early_high. Use this as
the seed34 input to a cross-seed ringdown050 synthesis.

Stage 13CI: seed21 target-2 practical-threshold consistency check.

Run 864 tests seed21 target 2 at the final target-0 practical threshold,
ringdown049453125, using the 9-source Tx/Rx=60 target-2 rescue policy. The
row is exact/moderate with a 5.149e-04 base margin, 1.486e-05 above cutoff,
and all six diagnostic objective rows preserve truth above cutoff. This
replaces run 850 as the seed21 target-2 policy row because it uses the same
ringdown strength as accepted target-0 threshold run 854. Seed21 remains
target-0 limited, but its practical 8/5/9 policy is now internally coherent:
target 0 run 854, target 1 run 836, and target 2 run 864.

Stage 13CJ: cross-seed ringdown050 target-specific policy synthesis.

Run 865 refreshes the cross-seed synthesis after run 864. Seeds 13, 89, and
34 pass all targets at full ringdown050 under policies 8/5/5, 8/5/9, and
8/5/9 respectively. Seed21 remains the target-0-limited practical-threshold
case: target 0 run 854 has only 3.148e-08 reserve above cutoff, target 1 run
836 passes at full ringdown050, and target 2 run 864 passes at
ringdown049453125 with 1.486e-05 reserve. The synthesis keeps the rejected
controls visible: seed21 target-0 source-count rescues at full ringdown050
remain weak, and seed89/seed34 target-2 5-source rows remain weak. The next
physical branch should refine whether 9 sources are strictly required for
target-2 full-ringdown050 rescues by testing an intermediate 7-source row.

Stage 13CK: seed34 target-2 7-source ringdown050 refinement.

Run 866 tests seed34 target 2 at full ringdown050 with 7 sources. The row is
exact but weak: the true 8.0 mm radius is selected, but the production base
margin is only 4.168e-04, 8.316e-05 below cutoff, with
`radius_weak_confidence`. Four of six diagnostic objectives clear cutoff while
all preserve truth; base and early_high remain below cutoff. Because the
7-source row is weaker than both the rejected 5-source row from run 861 and
the accepted 9-source row from run 862, source-count behavior is not monotonic
enough to infer the 8-source result. Run the direct 8-source check.

Stage 13CL: seed34 target-2 8-source ringdown050 refinement.

Run 867 tests seed34 target 2 at full ringdown050 with 8 sources. The row is
again exact but weak: the base margin is 4.722e-04, 2.780e-05 below cutoff,
with `radius_weak_confidence`. The same diagnostic pattern holds as in the
7-source run: highband, late, late_high, and veryhigh clear cutoff while base
and early_high remain below, all preserving truth. The 8-source row is the
strongest rejected intermediate but still 5.348e-05 weaker than accepted
9-source run 862, so seed34 target 2 must remain at 9 sources for the current
full-ringdown050 production policy. Move the intermediate source-count branch
to seed89 target 2.

Stage 13CM: seed89 target-2 7-source ringdown050 refinement.

Run 868 tests seed89 target 2 at full ringdown050 with 7 sources. The row is
exact but weak: the base margin is 4.616e-04, 3.838e-05 below cutoff, with
`radius_weak_confidence`. The diagnostic pattern matches seed34's rejected
intermediates: highband, late, late_high, and veryhigh clear cutoff while base
and early_high remain below, all preserving truth. Seven sources improve over
seed89's rejected 5-source control from run 843 but remain far below accepted
9-source run 844. Run the direct 8-source check before deciding whether seed89
also requires 9 sources for target 2.

Stage 13CN: seed89 target-2 8-source ringdown050 refinement.

Run 869 tests seed89 target 2 at full ringdown050 with 8 sources. The row is
exact but weak: the base margin is 4.605e-04, 3.950e-05 below cutoff, with
`radius_weak_confidence`. The diagnostic pattern again mirrors seed34:
highband, late, late_high, and veryhigh clear cutoff while base and early_high
remain below, all preserving truth. The 8-source row is slightly weaker than
the 7-source row and remains 1.216e-04 weaker than accepted 9-source run 844.
Seed89 target 2 therefore also requires 9 sources under the current
full-ringdown050 production objective. Move to a fifth-seed target-0
replication to test whether seed21's shallow-target near-miss is recurring.

Stage 13CO: seed55 target-0 8-source ringdown050 replication.

Run 870 tests a fifth noise seed on target 0 at full ringdown050. The row is
exact/moderate with a 5.079e-04 base margin, 7.905e-06 above cutoff. All six
diagnostic objective rows preserve truth; base, highband, veryhigh, and
early_high clear cutoff, while late and late_high are below cutoff. Seed55
therefore joins the full-ringdown050 target-0 pass group, but with the
smallest accepted reserve so far. Seed21 remains the only observed target-0
full-ringdown050 failure, while seed55 shows the lower tail is close enough to
avoid overclaiming robustness. Continue seed55 with target 2 at 5 sources.

Stage 13CP: seed55 target-2 5-source ringdown050 replication.

Run 871 tests seed55 target 2 at full ringdown050 with 5 sources. The row is
exact/moderate with a 5.677e-04 base margin, 6.772e-05 above cutoff. All
diagnostic objectives preserve truth, and five of six clear cutoff; only
early_high is slightly below. Seed55 therefore follows the seed13 target-2
5-source pass pattern rather than the seed89/seed34 9-source rescue pattern.
Complete the seed55 target-specific set with target 1 at 5 sources.

Stage 13CQ: seed55 target-1 5-source ringdown050 completion.

Run 872 tests seed55 target 1 at full ringdown050 with 5 sources. The row is
exact/moderate with a 5.506e-04 base margin, 5.063e-05 above cutoff, and all
six diagnostic objective rows preserve truth and clear cutoff. Seed55 now has
accepted rows for target 0 run 870 with 8 sources, target 1 run 872 with
5 sources, and target 2 run 871 with 5 sources. Seed55 therefore follows an
8/5/5 full-ringdown050 policy; the limiting seed55 row is target 0. Create a
seed55 policy summary and continue target-0 lower-tail replication.

Stage 13CR: seed144 target-0 8-source ringdown050 replication.

Run 873 tests a sixth noise seed on target 0 at full ringdown050. The row is
exact/moderate with a 6.144e-04 base margin, 1.144e-04 above cutoff, making it
the strongest target-0 8-source ringdown050 row in the current seed set. All
diagnostic objective rows preserve truth, and five of six clear cutoff; only
late is below. Seed144 is not a shallow-target lower-tail case. Continue
seed144 with target 2 at 5 sources.

Stage 13CS: seed55 ringdown050 target-specific policy summary.

Run 874 aggregates seed55 into an 8/5/5 full-ringdown050 policy. The promoted
rows are target 0 run 870 with 8 sources, target 1 run 872 with 5 sources, and
target 2 run 871 with 5 sources. All three production rows are exact/moderate
and above cutoff; the limiting row is target 0 at 5.079e-04, 7.905e-06 above
cutoff. All 18 diagnostic rows preserve truth and 15 clear cutoff. The target2
5-source cross-seed comparison now splits seed13/seed55 accepted versus
seed89/seed34 weak, reinforcing that the target2 source-count policy is
seed-dependent.

Stage 13CT: seed144 target-2 5-source ringdown050 replication.

Run 875 tests seed144 target 2 at full ringdown050 with 5 sources. The row is
exact/moderate with a 5.470e-04 base margin, 4.700e-05 above cutoff. All six
diagnostic objective rows preserve truth, and five of six clear cutoff; only
early_high is below. Seed144 target 2 therefore follows the seed13/seed55
5-source pass branch rather than the seed89/seed34 9-source rescue branch.
Complete seed144 with target 1 at 5 sources.

Stage 13CU: seed144 target-1 5-source ringdown050 completion.

Run 876 tests seed144 target 1 at full ringdown050 with 5 sources. The row is
exact/moderate with a 5.183e-04 base margin, 1.834e-05 above cutoff. All six
diagnostic objective rows preserve truth, and five of six clear cutoff; only
early_high is below. Seed144 therefore has accepted rows for target 0 run 873
with 8 sources, target 1 run 876 with 5 sources, and target 2 run 875 with
5 sources. Create a seed144 `8/5/5` policy summary with target 1 recorded as
the limiting row.

Stage 13CV: seed144 ringdown050 target-specific policy summary.

Run 877 aggregates seed144 into an 8/5/5 full-ringdown050 policy. The promoted
rows are target 0 run 873 with 8 sources, target 1 run 876 with 5 sources, and
target 2 run 875 with 5 sources. All three production rows are exact/moderate
and above cutoff; the limiting row is target 1 at 5.183e-04, 1.834e-05 above
cutoff. All 18 diagnostic rows preserve truth and 15 clear cutoff. The target2
5-source cross-seed comparison now splits seed13/seed55/seed144 accepted
versus seed89/seed34 weak. Refresh the cross-seed policy synthesis and continue
target-0 lower-tail replication on the next Fibonacci seed.

Stage 13CW: cross-seed ringdown050 target-specific policy synthesis v2.

Run 879 refreshes the cross-seed policy synthesis after adding seed55 and
seed144. The synthesis now has 18 promoted policy rows across six seeds, all
truth-preserving and above cutoff, plus nine rejected full-ringdown050 controls
that remain truth-preserving but below cutoff. Seeds 13, 55, and 144 pass at
8/5/5; seeds 89 and 34 require 8/5/9 because target 2 remains weak at 5, 7,
and 8 sources; seed21 remains a practical-threshold case at ringdown049453125
for target 0 and target 2. Continue the active seed233 target-0 lower-tail
replication.

Stage 13CX: seed233 target-0 8-source ringdown050 replication.

Run 878 tests the next Fibonacci noise seed on target 0 at full ringdown050.
The row is exact/moderate with a 5.434e-04 base margin, 4.342e-05 above cutoff.
All six diagnostic objective rows preserve truth; base, highband, veryhigh,
and early_high clear cutoff, while late and late_high are below. Seed233 is
therefore another target-0 full-ringdown050 pass and does not repeat seed21's
failure. Continue seed233 with target 2 at 5 sources.

Stage 13CY: seed233 target-2 5-source ringdown050 replication.

Run 880 tests seed233 target 2 at full ringdown050 with 5 sources. The row is
exact/moderate with a 5.879e-04 base margin, 8.788e-05 above cutoff. All six
diagnostic objective rows preserve truth and clear cutoff. Seed233 target 2
therefore joins seed13, seed55, and seed144 as a 5-source target-2 pass, rather
than following the seed89/seed34 9-source rescue branch. Complete seed233 with
target 1 at 5 sources.

Stage 13CZ: seed233 target-1 5-source ringdown050 completion.

Run 881 tests seed233 target 1 at full ringdown050 with 5 sources. The row is
exact/moderate with a 5.609e-04 base margin, 6.088e-05 above cutoff. All six
diagnostic objective rows preserve truth and clear cutoff. Seed233 now has
accepted rows for target 0 run 878 with 8 sources, target 1 run 881 with
5 sources, and target 2 run 880 with 5 sources.

Stage 13DA: seed233 ringdown050 target-specific policy summary.

Run 882 aggregates seed233 into an 8/5/5 full-ringdown050 policy. All three
production rows are exact/moderate and above cutoff; target 0 is limiting at
5.434e-04, 4.342e-05 above cutoff. All 18 diagnostic rows preserve truth and
16 clear cutoff, with only target0 late and target0 late_high below. Continue
target-0 lower-tail replication on seed377.

Stage 13DB: seed377 target-0 8-source ringdown050 replication.

Run 883 tests seed377 target 0 at full ringdown050 with 8 sources. The row is
exact/moderate with a 5.528e-04 base margin, 5.278e-05 above cutoff. All six
diagnostic objective rows preserve truth; base, highband, veryhigh, and
early_high clear cutoff, while late and late_high are below. Seed377 is another
target-0 full-ringdown050 pass, leaving seed21 as the only observed target-0
failure in the current Fibonacci seed sequence. Continue seed377 with target 2
at 5 sources.

Stage 13DC: seed377 target-2 5-source ringdown050 replication.

Run 884 tests seed377 target 2 at full ringdown050 with 5 sources. The row is
exact/moderate but low-reserve: the base margin is 5.096e-04, only 9.608e-06
above cutoff. All six diagnostic objective rows preserve truth; five of six
clear cutoff, with early_high below. Seed377 target 2 therefore passes at
5 sources but becomes the weakest accepted target-2 5-source row so far.
Complete seed377 with target 1 at 5 sources.

Stage 13DD: seed377 target-1 5-source ringdown050 completion.

Run 885 tests seed377 target 1 at full ringdown050 with 5 sources. The row is
exact/moderate with a 5.620e-04 base margin, 6.197e-05 above cutoff. All six
diagnostic objective rows preserve truth and clear cutoff. Seed377 now has
accepted rows for all three targets under the 8/5/5 policy, but target 2 is
the limiting low-reserve row.

Stage 13DE: seed377 ringdown050 target-specific policy summary.

Run 886 aggregates seed377 into an 8/5/5 full-ringdown050 policy. All three
production rows are exact/moderate and above cutoff; target 2 is limiting at
5.096e-04, 9.608e-06 above cutoff. All 18 diagnostic rows preserve truth and
15 clear cutoff, with target0 late, target0 late_high, and target2 early_high
below. Continue target-0 lower-tail replication with seed610.

Stage 13DF: seed610 target-0 8-source ringdown050 replication.

Run 887 tests seed610 target 0 at full ringdown050 with 8 sources. The row is
exact/moderate but razor-edge: the base margin is 5.006e-04, only 5.897e-07
above cutoff. All six diagnostic objective rows preserve truth; five of six
clear cutoff, with late below. Seed610 is therefore accepted but is the closest
target-0 pass observed so far. Continue seed610 with target 2 while preserving
the target-0 low-reserve warning.

Stage 13DG: seed610 target-2 5-source ringdown050 control.

Run 888 tests seed610 target 2 at full ringdown050 with 5 sources. The row is
truth-preserving but weak: the base margin is 4.635e-04, 3.649e-05 below the
5.0e-04 cutoff, and early_high is also below cutoff. All six diagnostic
objectives still select the true geometry, so this is a radius-separation
failure rather than a wrong-geometry failure. Treat run 888 as the rejected
5-source control and run a direct 9-source target-2 rescue, matching the
seed34/seed89 branch where 7- and 8-source intermediates also remained weak.

Stage 13DH: seed610 target-2 9-source ringdown050 rescue.

Run 889 tests the usual 9-source target-2 rescue for seed610. The row remains
truth-preserving but weak: the base margin is 4.802e-04, 1.976e-05 below the
5.0e-04 cutoff, and early_high is also below cutoff. The 9-source margin
improves run 888 by only 1.673e-05, so seed610 target 2 is harder than the
seed34/seed89 branch where 9 sources passed. Continue with an 11-source
target-2 acquisition-density test before changing ringdown severity or the
objective.

Stage 13DI: seed610 target-2 11-source ringdown050 density test.

Run 890 tests whether increasing seed610 target 2 to 11 sources rescues the
full ringdown050 row. It does not: the true geometry remains rank 1, but the
base margin drops to 3.970e-04, 1.030e-04 below cutoff, and only late and
late_high clear cutoff. This closes the simple source-density branch for
seed610 target 2. Keep 9 sources as the best full-ringdown050 source-count row
and move to a practical ringdown-threshold test at 0.49453125, matching the
seed21 threshold methodology.

Stage 13DJ: seed610 target-2 ringdown049453125 threshold test.

Run 891 tests seed610 target 2 with 9 sources at ringdown049453125. The row is
still truth-preserving but weak: base margin is 4.818e-04, 1.817e-05 below
cutoff, and early_high is also below cutoff. The margin improves the
full-ringdown 9-source row by only 1.587e-06, so fine threshold bisection near
0.49453125 is not informative. Continue with a coarser ringdown0475 bracket
using the same 9-source acquisition.

Stage 13DK: seed610 target-2 ringdown0475 bracket.

Run 892 tests seed610 target 2 with 9 sources at ringdown0475. The row remains
truth-preserving but weak: base margin is 4.869e-04, 1.307e-05 below cutoff,
with early_high also below. The stress reduction moves the margin in the right
direction but still does not produce an accepted row. Continue to the
previously studied ringdown0459375 point to establish whether seed610 target 2
has a lower practical threshold bracket.

Stage 13DL: seed610 target-2 ringdown0459375 bracket.

Run 893 tests seed610 target 2 with 9 sources at ringdown0459375. The row is
still exact but weak: base margin is 4.903e-04, 9.688e-06 below cutoff, and
early_high is below cutoff. The margin trend is improving but remains too
shallow for another fine step. Continue with a coarser ringdown040 lower-bound
test to find an accepted bracket efficiently.

Stage 13DM: seed610 target-2 ringdown040 lower-bound test.

Run 894 tests seed610 target 2 with 9 sources at ringdown040. The row is exact
and nearly accepted, but base margin is 4.969e-04, still 3.081e-06 below
cutoff. Highband, late, late_high, and veryhigh clear cutoff; early_high
remains below. Run ringdown035 next to establish a clear accepted lower bracket
before bisection.

Stage 13DN: seed610 target-2 ringdown035 lower-stress check.

Run 895 tests seed610 target 2 with 9 sources at ringdown035. The row remains
truth-preserving but weak, with base margin 4.942e-04, 5.774e-06 below cutoff,
and early_high below. Since this is weaker than the ringdown040 near miss, the
low-stress branch is non-monotone. Continue to the established ringdown025
condition before switching to objective or receiver-setting experiments.

Stage 13DO: seed610 target-2 ringdown025 low-stress check.

Run 896 tests seed610 target 2 with 9 sources at ringdown025. The row remains
truth-preserving but weak, with base margin 4.678e-04, 3.222e-05 below cutoff.
Highband also falls below cutoff, while late, late_high, and veryhigh preserve
reserve. Ringdown-only reduction does not rescue seed610 target 2. Stop the
ringdown-only target2 branch, complete seed610 target1 at full ringdown050,
and then decide whether target2 needs an aperture/objective follow-up.

Stage 13DP: seed610 target-1 5-source ringdown050 control.

Run 897 tests seed610 target 1 with the usual 5-source full-ringdown050
acquisition. The row is exact but weak: base margin is 4.677e-04, 3.226e-05
below cutoff, with early_high also below cutoff. This makes seed610 a broader
low-margin seed, not just a target2 outlier. Run a 9-source target1 rescue
before changing ringdown or objective settings.

Stage 13DQ: seed610 target-1 9-source ringdown050 rescue.

Run 898 tests seed610 target 1 with 9 sources at full ringdown050. The row is
exact but weaker than the 5-source control: base margin is 4.198e-04,
8.021e-05 below cutoff, while highband, late, late_high, and veryhigh clear
cutoff. Because source9 is not a rescue and the aperture response is
non-monotone, test the 8-source target1 layout before changing ringdown or
objective settings.

Stage 13DR: seed610 target-1 8-source ringdown050 rescue.

Run 899 tests seed610 target 1 with 8 sources at full ringdown050. The row is
exact but weak, with base margin 4.205e-04, 7.948e-05 below cutoff. The simple
target1 aperture branch is now closed: 5, 8, and 9 sources all preserve truth
but remain below cutoff. Create a seed610 unresolved-branch summary and then
continue GPU replication with the next Fibonacci seed target0.

Stage 13DS: seed610 unresolved-branch summary.

Run 901 aggregates seed610 runs 887-899. It confirms seed610 as a broad
low-margin seed: target0 is accepted only by 5.897e-07, target1 is best at the
5-source control but remains 3.226e-05 below cutoff, and target2 is best at
ringdown040 but remains 3.081e-06 below cutoff. All rejected rows preserve the
true geometry, so the unresolved issue is radius-margin reserve rather than
target assignment or coordinate recovery. Stop simple seed610 source-count and
ringdown-only extensions. Continue GPU replication with seed987 target0, and
revisit seed610 only through a specialized aperture/objective design if the
next cross-seed synthesis justifies it.

Stage 13DT: seed987 target0 8-source ringdown050 production row.

Run 900 starts the next Fibonacci seed. Seed987 target0 is exact and accepted:
the base margin is 5.112e-04, or 1.116e-05 above cutoff. The result has more
reserve than seed610 target0, but late and late_high diagnostic variants remain
below cutoff while preserving the true geometry. Continue the standard
target-specific policy with seed987 target2 at 5 sources and full ringdown050;
reserve a 9-source target2 rescue only if the 5-source row is weak.

Stage 13DU: seed987 target2 5-source ringdown050 control.

Run 902 tests seed987 target2 with the standard 5-source full-ringdown control.
It is exact and accepted with a base margin of 5.519e-04, or 5.190e-05 above
cutoff. Highband, late, late_high, and veryhigh also clear cutoff; only
early_high remains weak. Do not spend a 9-source rescue on seed987 target2.
Continue the target-specific branch with seed987 target1 at 5 sources and full
ringdown050.

Stage 13DV: seed987 target1 5-source ringdown050 control.

Run 903 tests seed987 target1 with the standard 5-source full-ringdown control.
It is exact and accepted with a base margin of 5.665e-04, or 6.647e-05 above
cutoff. All six diagnostic objective variants also clear cutoff while
preserving the true geometry. Create the seed987 8/5/5 summary and continue
with the next Fibonacci seed.

Stage 13DW: seed987 target-specific 8/5/5 summary.

Run 904 aggregates seed987 runs 900, 902, and 903. All three target-specific
rows are accepted: target0 passes by 1.116e-05, target2 by 5.190e-05, and
target1 by 6.647e-05. The summary contrasts seed987 with seed610: both seeds
are truth-preserving, but seed987 clears the production cutoff on all targets
without rescue runs. Continue full-ringdown replication with seed1597 target0.

Stage 13DX: seed1597 target0 8-source ringdown050 production row.

Run 905 starts seed1597. Target0 is exact and technically accepted, but only by
3.598e-07 above cutoff. Late and late_high objective variants remain below
cutoff while preserving the true geometry. Treat this as an accepted
low-reserve row, closer to seed610 target0 than seed987 target0, and continue
the seed1597 branch with target2 at 5 sources before deciding whether the seed
needs specialized follow-up.

Stage 13DY: seed1597 target2 5-source ringdown050 control.

Run 906 tests seed1597 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.228e-04, or
2.279e-05 above cutoff. Early_high remains weak, but the base, highband, late,
late_high, and veryhigh variants all clear cutoff. Do not run a 9-source
target2 rescue. Complete seed1597 with target1 at 5 sources before summarizing
the seed.

Stage 13DZ: seed1597 target1 5-source ringdown050 control.

Run 907 tests seed1597 target1 with the standard 5-source full-ringdown
control. The row is exact but weak: the base margin is 4.919e-04, or
8.052e-06 below cutoff, and early_high is also below cutoff. The true geometry
remains rank 1 for all objective variants. Run the established 9-source
target1 rescue before considering ringdown or objective-specialized controls.

Stage 13EA: seed1597 target1 9-source ringdown050 rescue.

Run 908 tests the seed1597 target1 9-source rescue. It is exact and accepted:
the base margin is 5.127e-04, or 1.271e-05 above cutoff, and all diagnostic
objective variants clear cutoff. This rescues the shallow 5-source miss from
run 907. Create a seed1597 rescue summary before moving to the next seed.

Stage 13EB: seed1597 target-specific rescue summary.

Run 909 aggregates seed1597 runs 905-908. Seed1597 is accepted but low-reserve:
target0 passes by only 3.598e-07, target2 passes by 2.279e-05, and target1
passes only after the 9-source rescue. The branch is truth-preserving on all
rows and unlike seed610 has a source-density rescue that brings every target
above cutoff. Continue full-ringdown replication with seed2584 target0.

Stage 13EC: seed2584 target0 8-source ringdown050 production row.

Run 910 starts seed2584. Target0 is exact but weak: the base margin is
4.823e-04, or 1.773e-05 below cutoff, with late and late_high also below
cutoff. The true geometry remains rank 1 for all objective variants. Run a
9-source target0 rescue before changing ringdown or objective settings.

Stage 13ED: seed2584 target0 9-source ringdown050 rescue.

Run 911 tests the seed2584 target0 9-source rescue. It is exact and accepted:
the base margin is 5.469e-04, or 4.688e-05 above cutoff. The late diagnostic
variant remains below cutoff, so the rescue is accepted but not uniformly
high-reserve. Continue the seed2584 branch with target2 at 5 sources and full
ringdown050.

Stage 13EE: seed2584 target2 5-source ringdown050 control.

Run 912 tests seed2584 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.529e-04, or
5.287e-05 above cutoff. Early_high remains weak, but base, highband, late,
late_high, and veryhigh clear cutoff. Do not run a target2 rescue; continue
with seed2584 target1 at 5 sources.

Stage 13EF: seed2584 target1 5-source ringdown050 control.

Run 913 tests seed2584 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.255e-04, or
2.545e-05 above cutoff. All six diagnostic objective variants clear cutoff
while preserving the true geometry. This completes the seed2584 physical branch
and leaves target0 as the only target that required source-density rescue.

Stage 13EG: seed2584 target-specific rescue summary.

Run 914 aggregates seed2584 runs 910-913. The branch is truth-preserving on all
rows: target0 fails at 8 sources but passes after a 9-source rescue, target2
passes at 5 sources, and target1 passes at 5 sources. Continue full-ringdown
replication with seed4181 target0 under the same targeted rescue policy.

Stage 13EH: seed4181 target0 8-source ringdown050 production row.

Run 915 starts seed4181. Target0 is exact and accepted with a base margin of
5.845e-04, or 8.446e-05 above cutoff. All six diagnostic objective variants
clear cutoff while preserving the true geometry. Do not run a target0 rescue;
continue the branch with target2 at 5 sources.

Stage 13EI: seed4181 target2 5-source ringdown050 control.

Run 916 tests seed4181 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.899e-04, or
8.987e-05 above cutoff. All six diagnostic objective variants clear cutoff.
Do not run a target2 rescue; continue the branch with target1 at 5 sources.

Stage 13EJ: seed4181 target1 5-source ringdown050 control.

Run 917 tests seed4181 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 6.807e-04, or
1.807e-04 above cutoff. All six diagnostic objective variants clear cutoff.
This completes the seed4181 physical branch with no rescue runs.

Stage 13EK: seed4181 target-specific 8/5/5 summary.

Run 918 aggregates seed4181 runs 915-917. The branch cleanly passes the
target-specific 8/5/5 full-ringdown policy: all targets are exact, all base
margins clear cutoff, and all 18 diagnostic objective rows clear cutoff.
Continue full-ringdown replication with seed6765 target0.

Stage 13EL: seed6765 target0 8-source ringdown050 production row.

Run 919 starts seed6765. Target0 is exact but weak: the base margin is
4.906e-04, or 9.416e-06 below cutoff, and the late diagnostic objective is
also below cutoff. The true geometry remains rank 1 for all objective variants.
Run a 9-source target0 rescue before moving to the other seed6765 targets.

Stage 13EM: seed6765 target0 9-source ringdown050 rescue.

Run 920 tests the seed6765 target0 9-source rescue. It is exact and accepted:
the base margin is 5.485e-04, or 4.854e-05 above cutoff. Late and late_high
diagnostic variants remain below cutoff, so the rescue is accepted but not
uniformly high-reserve. Continue the seed6765 branch with target2 at 5 sources.

Stage 13EN: seed6765 target2 5-source ringdown050 control.

Run 921 tests seed6765 target2 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 4.840e-04, or 1.595e-05
below cutoff, and early_high is also below cutoff. The true geometry remains
rank 1 for all objective variants. Run a 9-source target2 rescue before moving
to target1.

Stage 13EO: seed6765 target2 9-source ringdown050 rescue.

Run 922 tests the seed6765 target2 9-source rescue. It is exact and accepted,
but only by a razor margin: the base margin is 5.067e-04, or 6.698e-06 above
cutoff, and early_high is only 3.071e-06 above cutoff. Continue to target1, but
treat seed6765 as a low-reserve branch.

Stage 13EP: seed6765 target1 5-source ringdown050 control.

Run 923 tests seed6765 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 6.068e-04, or
1.068e-04 above cutoff. All six diagnostic objective variants clear cutoff.
Create a seed6765 rescue summary before moving to the next seed.

Stage 13EQ: seed6765 target-specific rescue summary.

Run 924 aggregates seed6765 runs 919-923. The branch is truth-preserving on all
rows but low-reserve: target0 and target2 require 9-source rescues, target2
passes by only 6.698e-06 after rescue, and target1 passes at 5 sources.
Continue full-ringdown replication with seed10946 target0.

Stage 13ER: seed10946 target0 8-source ringdown050 production row.

Run 925 starts seed10946. Target0 is exact but weak: the base margin is
4.749e-04, or 2.508e-05 below cutoff, and late and late_high diagnostic
variants are also below cutoff. The true geometry remains rank 1 for all
objective variants. Run a 9-source target0 rescue before moving to the other
seed10946 targets.

Stage 13ES: seed10946 target0 9-source ringdown050 rescue.

Run 926 tests the seed10946 target0 9-source rescue. It is exact and accepted
with a base margin of 5.207e-04, or 2.067e-05 above cutoff. Late and late_high
diagnostic variants remain below cutoff, so the rescue is accepted but
low-reserve. Continue the seed10946 branch with target2 at 5 sources.

Stage 13ET: seed10946 target2 5-source ringdown050 control.

Run 927 tests seed10946 target2 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 4.933e-04, or 6.730e-06
below cutoff, and early_high is also below cutoff. The true geometry remains
rank 1 for all objective variants. Run a 9-source target2 rescue before moving
to target1.

Stage 13EU: seed10946 target2 9-source ringdown050 rescue.

Run 928 tests the seed10946 target2 9-source rescue. It is exact and accepted
with a base margin of 5.593e-04, or 5.927e-05 above cutoff. Early_high remains
slightly below cutoff, but the base rescue is healthier than the seed6765
target2 rescue. Continue the branch with target1 at 5 sources.

Stage 13EV: seed10946 target1 5-source ringdown050 control.

Run 929 tests seed10946 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.980e-04, or
9.805e-05 above cutoff. All six diagnostic objective variants clear cutoff,
making target1 the healthiest seed10946 row. Create a seed10946 rescue summary
before moving to the next seed.

Stage 13EW: seed10946 target-specific rescue summary.

Run 930 aggregates seed10946 runs 925-929. The branch is truth-preserving on
all rows but target0 and target2 require 9-source rescues; target0 remains
low-reserve in late-window diagnostics after rescue, target2 clears base with
better reserve, and target1 passes cleanly at 5 sources. Continue Fibonacci
replication with seed17711 target0 at 8 sources.

Stage 13EX: seed17711 target0 8-source ringdown050 production row.

Run 931 starts seed17711. Target0 is exact but weak: the base margin is
4.846e-04, or 1.542e-05 below cutoff, and the late diagnostic objective is
also below cutoff. The true geometry remains rank 1 for all objective
variants. Run a 9-source target0 rescue before moving to the other seed17711
targets.

Stage 13EY: seed17711 target0 9-source ringdown050 rescue.

Run 932 tests the seed17711 target0 9-source rescue. It is exact and accepted
with a base margin of 5.525e-04, or 5.248e-05 above cutoff. Late remains
below cutoff, so the rescue is accepted but late-window low-reserve. Continue
the seed17711 branch with target2 at 5 sources.

Stage 13EZ: seed17711 target2 5-source ringdown050 control.

Run 933 tests seed17711 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.363e-04, or
3.628e-05 above cutoff. Early_high remains slightly below cutoff, but all
objective variants preserve the true target2 geometry. Continue the branch
with target1 at 5 sources.

Stage 13FA: seed17711 target1 5-source ringdown050 control.

Run 934 tests seed17711 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.806e-04, or
8.064e-05 above cutoff. All six diagnostic objective variants clear cutoff,
making target1 the healthiest seed17711 row. Create a seed17711 rescue summary
before moving to the next seed.

Stage 13FB: seed17711 target-specific rescue summary.

Run 935 aggregates seed17711 runs 931-934. The branch is truth-preserving on
all rows and accepted after one targeted rescue: target0 fails the 8-source
control but passes at 9 sources, while target2 and target1 pass at 5 sources.
Continue Fibonacci replication with seed28657 target0 at 8 sources.

Stage 13FC: seed28657 target0 8-source ringdown050 production row.

Run 936 starts seed28657. Target0 is exact and accepted with a base margin of
5.720e-04, or 7.203e-05 above cutoff. The late diagnostic objective remains
slightly below cutoff, but all objective variants preserve the true target0
geometry. Continue the branch with target2 at 5 sources.

Stage 13FD: seed28657 target2 5-source ringdown050 control.

Run 937 tests seed28657 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.257e-04, or
2.567e-05 above cutoff. Early_high remains slightly below cutoff, but all
objective variants preserve the true target2 geometry. Continue the branch
with target1 at 5 sources.

Stage 13FE: seed28657 target1 5-source ringdown050 control.

Run 938 tests seed28657 target1 with the standard 5-source full-ringdown
control. It is exact and accepted, but only by a razor base margin of
5.076e-04, or 7.605e-06 above cutoff. Early_high remains slightly below
cutoff. Create a seed28657 target-specific 8/5/5 summary before moving to the
next seed.

Stage 13FF: seed28657 target-specific 8/5/5 summary.

Run 939 aggregates seed28657 runs 936-938. The branch passes the 8/5/5 policy
without rescue, but it is low-reserve: target1 barely clears base cutoff,
target0 has a late-window diagnostic caveat, and target2/target1 carry
early_high caveats. Continue Fibonacci replication with seed46368 target0 at
8 sources.

Stage 13FG: seed46368 target0 8-source ringdown050 production row.

Run 940 starts seed46368. Target0 is exact and accepted, but only by a razor
base margin of 5.065e-04, or 6.516e-06 above cutoff. Late and late_high
diagnostic variants remain below cutoff, so the row is accepted but
low-reserve. Continue the branch with target2 at 5 sources.

Stage 13FH: seed46368 target2 5-source ringdown050 control.

Run 941 tests seed46368 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.165e-04, or
1.648e-05 above cutoff. Early_high remains below cutoff, but all objective
variants preserve the true target2 geometry. Continue the branch with target1
at 5 sources.

Stage 13FI: seed46368 target1 5-source ringdown050 control.

Run 942 tests seed46368 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.072e-04, or
7.231e-06 above cutoff. All six diagnostic objective variants clear cutoff,
making target1 internally clean but still razor-margin at the base objective.
Create the seed46368 target-specific 8/5/5 summary before moving to the next
seed.

Stage 13FJ: seed46368 target-specific 8/5/5 summary.

Run 943 aggregates seed46368 runs 940-942. The branch passes the 8/5/5 policy
without rescue, but all three base margins are close to cutoff: target0 clears
by 6.516e-06, target1 by 7.231e-06, and target2 by 1.648e-05. Target0 has
late and late_high caveats, target2 has an early_high caveat, and target1 is
base-razor despite clean diagnostics. Continue Fibonacci replication with
seed75025 target0 at 8 sources.

Stage 13FK: seed75025 target0 8-source ringdown050 production row.

Run 944 starts seed75025. Target0 is exact and accepted with a base margin of
5.720e-04, or 7.200e-05 above cutoff. The late objective remains below cutoff,
but all six objective variants keep the true target0 geometry at rank 1.
Continue the branch with target2 at 5 sources.

Stage 13FL: seed75025 target2 5-source ringdown050 control.

Run 945 tests seed75025 target2 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 4.473e-04, or 5.274e-05
below cutoff, and early_high also remains below cutoff. Because all objective
variants still rank the true target2 geometry first, run a 9-source target2
rescue before moving to target1.

Stage 13FM: seed75025 target2 9-source ringdown050 rescue.

Run 946 rescues seed75025 target2, but only by a razor margin. The final
geometry is exact and the base margin is 5.008e-04, just 8.40e-07 above
cutoff. Early_high remains below cutoff, so target2 is accepted with very low
reserve. Continue the branch with target1 at 5 sources.

Stage 13FN: seed75025 target1 5-source ringdown050 control.

Run 947 tests seed75025 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.110e-04, or
1.096e-05 above cutoff. Early_high remains just below cutoff. Create the
seed75025 target-specific rescue summary before moving to the next seed.

Stage 13FO: seed75025 target-specific rescue summary.

Run 948 aggregates seed75025 runs 944-947. The branch is accepted after a
target2 9-source rescue, but it is fragile: target2 clears cutoff by only
8.405e-07 after rescue, target1 clears base by 1.096e-05, and target0 keeps a
late-window caveat. Continue Fibonacci replication with seed121393 target0 at
8 sources.

Stage 13FP: seed121393 target0 8-source ringdown050 production row.

Run 949 starts seed121393. Target0 is exact but weak: the base margin is
4.651e-04, or 3.489e-05 below cutoff. Late and late_high diagnostics are also
below cutoff, but all objective variants preserve the true target0 geometry.
Run a 9-source target0 rescue before moving to target2.

Stage 13FQ: seed121393 target0 9-source ringdown050 rescue.

Run 950 tests the 9-source target0 rescue. It is exact but still weak: the
base margin improves to 4.912e-04 but remains 8.825e-06 below cutoff. Late and
late_high are also below cutoff, but all objective variants preserve truth.
Because the miss is now close to cutoff, run one 11-source escalation before
declaring seed121393 target0 unresolved.

Stage 13FR: seed121393 target0 11-source ringdown050 escalation.

Run 951 tests the 11-source target0 escalation. It is exact but weak, and the
base margin worsens to 4.385e-04, or 6.153e-05 below cutoff. Early_high also
falls below cutoff. Stop source-density escalation and summarize seed121393
target0 as unresolved.

Stage 13FS: seed121393 target0 unresolved source-density summary.

Run 952 aggregates seed121393 target0 runs 949-951. All three rows preserve
the true target0 geometry, but none passes the base cutoff. The best attempt is
the 9-source row at 4.912e-04, still 8.825e-06 below cutoff, while 11 sources
worsens the margin. Stop this seed and continue Fibonacci replication with
seed196418 target0 at 8 sources.

Stage 13FT: seed196418 target0 8-source ringdown050 production row.

Run 953 starts seed196418. Target0 is exact and accepted with a base margin of
6.120e-04, or 1.120e-04 above cutoff. All six diagnostic objective variants
also clear cutoff. Continue the branch with target2 at 5 sources.

Stage 13FU: seed196418 target2 5-source ringdown050 control.

Run 954 tests seed196418 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 6.785e-04, or
1.785e-04 above cutoff. All six diagnostic objective variants clear cutoff
and rank the true target2 geometry first. Continue the branch with target1 at
5 sources.

Stage 13FV: seed196418 target1 5-source ringdown050 control.

Run 955 tests seed196418 target1 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 4.809e-04, or 1.906e-05
below cutoff. Early_high is also below cutoff, but all six objective variants
rank the true target1 geometry first. Run a 9-source target1 rescue before
summarizing seed196418.

Stage 13FW: seed196418 target1 9-source ringdown050 rescue.

Run 956 rescues seed196418 target1. It is exact and accepted with a base
margin of 5.896e-04, or 8.956e-05 above cutoff. All six diagnostic objective
variants clear cutoff and rank the true target1 geometry first. Create the
seed196418 target-specific rescue summary before moving to the next seed.

Stage 13FX: seed196418 target-specific rescue summary.

Run 957 aggregates seed196418 runs 953-956. The branch is accepted after a
target1 9-source rescue: target0 passes at 8 sources, target2 passes at 5
sources, target1 fails the 5-source control by 1.906e-05 but passes the
9-source rescue by 8.956e-05. Continue Fibonacci replication with seed317811
target0 at 8 sources.

Stage 13FY: seed317811 target0 8-source ringdown050 production row.

Run 958 starts seed317811. Target0 is exact and accepted with a base margin of
5.876e-04, or 8.757e-05 above cutoff. Late and late_high diagnostic variants
remain below cutoff, but all objective variants rank the true target0 geometry
first. Continue the branch with target2 at 5 sources.

Stage 13FZ: seed317811 target2 5-source ringdown050 control.

Run 959 tests seed317811 target2 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 4.958e-04, or 4.193e-06
below cutoff. Early_high is also below cutoff, but all six objective variants
rank the true target2 geometry first. Run a 9-source target2 rescue before
moving to target1.

Stage 13GA: seed317811 target2 9-source ringdown050 rescue.

Run 960 rescues seed317811 target2, but only by a low reserve. The final
geometry is exact and the base margin is 5.096e-04, or 9.566e-06 above cutoff.
Early_high remains below cutoff, but all six objective variants rank the true
target2 geometry first. Continue the branch with target1 at 5 sources.

Stage 13GB: seed317811 target1 5-source ringdown050 control.

Run 961 tests seed317811 target1 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 6.017e-04, or
1.017e-04 above cutoff. All six diagnostic objective variants clear cutoff and
rank the true target1 geometry first. Create the seed317811 target-specific
rescue summary before moving to the next seed.

Stage 13GC: seed317811 target-specific rescue summary.

Run 962 aggregates seed317811 runs 958-961. The branch is accepted after a
target2 9-source rescue, but it is low-reserve: target0 has late-window
caveats and target2 clears base cutoff by only 9.566e-06 after rescue, with
early_high still below cutoff. Continue Fibonacci replication with seed514229
target0 at 8 sources.

Stage 13GD: seed514229 target0 8-source ringdown050 production row.

Run 963 starts seed514229. Target0 is exact and accepted with a base margin of
5.336e-04, or 3.336e-05 above cutoff. The late diagnostic variant remains
below cutoff, but all six objective variants rank the true target0 geometry
first. Continue the branch with target2 at 5 sources.

Stage 13GE: seed514229 target2 5-source ringdown050 control.

Run 964 tests seed514229 target2 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 4.482e-04, or 5.178e-05
below cutoff. Early_high is also below cutoff, but all six objective variants
rank the true target2 geometry first. Run a 9-source target2 rescue before
moving to target1.

Stage 13GF: seed514229 target2 9-source ringdown050 rescue.

Run 965 rescues seed514229 target2. It is exact and accepted with a base
margin of 5.347e-04, or 3.466e-05 above cutoff. Early_high remains just below
cutoff, but all six objective variants rank the true target2 geometry first.
Continue the branch with target1 at 5 sources.

Stage 13GG: seed514229 target1 5-source ringdown050 control.

Run 966 tests seed514229 target1 with the standard 5-source full-ringdown
control. It is exact and accepted, but only by a razor base reserve: the
margin is 5.006e-04, or 6.472e-07 above cutoff. Early_high remains below
cutoff, while all six objective variants still rank the true target1 geometry
first. Close the branch with a target-specific rescue summary.

Stage 13GH: seed514229 target-specific rescue summary.

Run 967 aggregates seed514229 runs 963-966. The branch is accepted after a
target2 9-source rescue, but it is low-reserve: target0 has a late-window
caveat, target2 needed rescue and keeps an early_high caveat, and target1
passes by only 6.472e-07 with early_high below cutoff. Continue Fibonacci
replication with seed832040 target0 at 8 sources.

Stage 13GI: seed832040 target0 8-source ringdown050 production row.

Run 968 starts seed832040. Target0 is exact and accepted with a base margin of
5.091e-04, or 9.071e-06 above cutoff. The late diagnostic variant remains
below cutoff, but all six objective variants rank the true target0 geometry
first. Continue the branch with target2 at 5 sources.

Stage 13GJ: seed832040 target2 5-source ringdown050 control.

Run 969 tests seed832040 target2 with the standard 5-source full-ringdown
control. It is exact and accepted with a base margin of 5.593e-04, or
5.930e-05 above cutoff. All six diagnostic objective variants clear cutoff
and rank the true target2 geometry first. Continue the branch with target1 at
5 sources.

Stage 13GK: seed832040 target1 5-source ringdown050 control.

Run 970 tests seed832040 target1 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 3.952e-04, or 1.048e-04
below cutoff. Veryhigh and early_high are also below cutoff, but all six
objective variants rank the true target1 geometry first. Run a 9-source
target1 rescue before summarizing seed832040.

Stage 13GL: seed832040 target1 9-source ringdown050 rescue.

Run 971 rescues seed832040 target1. It is exact and accepted with a base
margin of 5.167e-04, or 1.672e-05 above cutoff. All six diagnostic objective
variants clear cutoff and rank the true target1 geometry first. Create the
seed832040 target-specific rescue summary before moving to the next seed.

Stage 13GM: seed832040 target-specific rescue summary.

Run 972 aggregates seed832040 runs 968-971. The branch is accepted after a
target1 9-source rescue: target0 passes at 8 sources with a late-window
caveat, target2 passes cleanly at 5 sources, target1 fails the 5-source
control by 1.048e-04 but passes the 9-source rescue by 1.672e-05. Continue
Fibonacci replication with seed1346269 target0 at 8 sources.

Stage 13GN: seed1346269 target0 8-source ringdown050 production row.

Run 973 starts seed1346269. Target0 is exact but weak: the base margin is
4.992e-04, or 8.413e-07 below cutoff. Late and late_high are also below
cutoff, while all six objective variants rank the true target0 geometry first.
Run a 9-source target0 rescue before moving to target2.

Stage 13GO: seed1346269 target0 9-source ringdown050 rescue.

Run 974 tests the 9-source target0 rescue. It is exact but still weak, and the
base margin worsens to 4.728e-04, or 2.722e-05 below cutoff. Late and
late_high are also below cutoff, but all six objective variants rank the true
target0 geometry first. Because the 8-source row was within 8.413e-07 of
cutoff, run one 11-source escalation before declaring target0 unresolved.

Stage 13GP: seed1346269 target0 11-source ringdown050 escalation.

Run 975 rescues seed1346269 target0 after the 8- and 9-source rows failed. It
is exact and accepted with a base margin of 5.043e-04, or 4.309e-06 above
cutoff. Late and late_high remain below cutoff, but all six objective variants
rank the true target0 geometry first. Continue the branch with target2 at
5 sources.

Stage 13GQ: seed1346269 target2 5-source ringdown050 control.

Run 976 tests seed1346269 target2 with the standard 5-source full-ringdown
control. It is exact but weak: the base margin is 4.914e-04, or 8.624e-06
below cutoff. Early_high is also below cutoff, but all six objective variants
rank the true target2 geometry first. Run a 9-source target2 rescue before
moving to target1.

Stage 13GR: seed1346269 target2 9-source ringdown050 rescue.

Run 977 rescues seed1346269 target2. It is exact and accepted with a base
margin of 5.641e-04, or 6.405e-05 above cutoff. All six diagnostic objective
variants clear cutoff and rank the true target2 geometry first. Continue the
branch with target1 at 5 sources.

Stage 13GS: seed1346269 target1 5-source ringdown050 control.

Run 978 tests seed1346269 target1 after target0 and target2 needed
source-density rescue. It is exact and accepted at the standard 5-source
control with a base margin of 5.203e-04, or 2.026e-05 above cutoff. All six
diagnostic objective variants clear cutoff and rank the true target1 geometry
first. Summarize the seed1346269 branch before moving to the next seed.

Stage 13GT: seed1346269 target-specific rescue summary.

Run 979 aggregates runs 973-978. Seed1346269 is accepted after target-specific
source-density rescue: target0 requires 11 sources and retains late-window
caveats, target2 is cleanly rescued at 9 sources, and target1 passes at
5 sources. Continue full-ringdown target-specific replication with seed2178309
target0 at 8 sources.

Stage 13GU: seed2178309 target0 8-source ringdown050 control.

Run 980 starts the seed2178309 branch. It is exact and accepted with a base
margin of 5.177e-04, or 1.772e-05 above cutoff. Late and late_high diagnostic
objectives fall below cutoff, but all six objective variants rank the true
target0 geometry first. Continue the branch with target2 at 5 sources and keep
the late-window caveat for the seed summary.

Stage 13GV: seed2178309 target2 5-source ringdown050 control.

Run 981 tests seed2178309 target2. It is exact and accepted with a base margin
of 5.426e-04, or 4.256e-05 above cutoff. Early_high lands fractionally below
cutoff at 4.995e-04, but all six objective variants rank the true target2
geometry first. Continue the branch with target1 at 5 sources and keep the
early_high razor caveat for the seed summary.

Stage 13GW: seed2178309 target1 5-source ringdown050 control.

Run 982 tests seed2178309 target1. It is exact but weak, with a base margin of
4.821e-04, or 1.787e-05 below cutoff. Early_high also falls below cutoff at
4.647e-04, while the other four diagnostic variants clear and all six rank the
true target1 geometry first. Run a 9-source target1 rescue before summarizing
the seed2178309 branch.

Stage 13GX: seed2178309 target1 9-source ringdown050 rescue.

Run 983 tests whether higher source density rescues seed2178309 target1. It is
exact but still weak, with a base margin of 4.567e-04, or 4.328e-05 below
cutoff. Early_high also remains below cutoff, while the other four diagnostics
clear and all six rank the true target1 geometry first. Run an 11-source
target1 rescue before deciding the branch status.

Stage 13GY: seed2178309 target1 11-source ringdown050 escalation.

Run 984 tests one final source-density escalation for seed2178309 target1. It
is exact but still weak, with a base margin of 3.915e-04, or 1.085e-04 below
cutoff. Base, late, veryhigh, and early_high are below cutoff, while all six
objective variants still rank the true target1 geometry first. Do not continue
blind source-density escalation; summarize the branch and test receiver or
acquisition mechanics.

Stage 13GZ: seed2178309 target-specific unresolved summary.

Run 985 aggregates runs 980-984. Target0 and target2 are accepted with
diagnostic caveats, but target1 remains truth-preserving and below cutoff after
5, 9, and 11 sources. The target1 margin worsens with added sources, so the
next GPU test is a linear-receiver target1 mechanism check at the original
5-source Tx/Rx=60 setup.

Stage 13HA: seed2178309 target1 linear-receiver mechanism test.

Run 986 repeats the seed2178309 target1 5-source Tx/Rx=60 control with linear
receiver sampling. It is exact but weak with the same base margin as the
nearest-receiver run, 4.821e-04, or 1.787e-05 below cutoff. Receiver
interpolation is therefore not the target1 mechanism. Move to a Tx/Rx=50
acquisition-offset probe at 5 sources.

Stage 13HB: seed2178309 target1 Tx/Rx=50 acquisition-offset probe.

Run 987 reduces the seed2178309 target1 Tx/Rx offset from 60 mm to 50 mm at
5 sources. It is exact and accepted with a base margin of 5.057e-04, or
5.739e-06 above cutoff. Early_high remains below cutoff, but all six objective
variants rank the true target1 geometry first. Bracket with a Tx/Rx=45 probe
before deciding whether 50 mm is the practical remedy.

Stage 13HC: seed2178309 target1 Tx/Rx=45 acquisition-offset bracket.

Run 988 tests the lower Tx/Rx bracket. It is exact but weak, with a base margin
of 4.759e-04, or 2.408e-05 below cutoff. Early_high is also below cutoff, while
the other four diagnostics clear and all six rank the true target1 geometry
first. Run a Tx/Rx=55 upper bracket to test whether 50 mm is a narrow accepted
point or part of a band.

Stage 13HD: seed2178309 target1 Tx/Rx=55 acquisition-offset bracket.

Run 989 tests the upper Tx/Rx bracket. It is exact and accepted with a base
margin of 5.098e-04, or 9.819e-06 above cutoff. Early_high remains below
cutoff, but all six objective variants rank the true target1 geometry first.
Because Tx/Rx=60 is weak, run a Tx/Rx=57.5 upper-edge probe.

Stage 13HE: seed2178309 target1 Tx/Rx=57.5 upper-edge probe.

Run 990 tests the upper edge of the accepted Tx/Rx band. It is exact but weak,
with a base margin of 4.931e-04, or 6.916e-06 below cutoff. Early_high is also
below cutoff, while the other four diagnostics clear and all six rank the true
target1 geometry first. Run Tx/Rx=52.5 to sample the middle of the accepted
50-55 mm band before summarizing the mechanism.

Stage 13HF: seed2178309 target1 Tx/Rx=52.5 center-band probe.

Run 991 samples the center of the accepted target1 offset band. It is exact and
accepted with a base margin of 5.111e-04, or 1.112e-05 above cutoff. Early_high
remains below cutoff, but all six objective variants rank the true target1
geometry first. Test whether Tx/Rx=52.5 is safe for target0 before promoting it
as an acquisition remedy.

Stage 13HG: seed2178309 target0 Tx/Rx=52.5 acquisition validation.

Run 992 checks whether the Tx/Rx=52.5 target1 remedy is safe for target0. It is
exact and base-accepted with a margin of 5.059e-04, or 5.853e-06 above cutoff.
Late and late_high remain below cutoff, but all six objective variants rank the
true target0 geometry first. Continue the all-target Tx/Rx=52.5 validation with
target2.

Stage 13HH: seed2178309 target2 Tx/Rx=52.5 acquisition validation.

Run 993 completes the seed2178309 all-target Tx/Rx=52.5 check. Target2 is
exact and cleanly accepted with a base margin of 5.993e-04, or 9.932e-05 above
cutoff. All six diagnostic objective variants clear cutoff and rank the true
target2 geometry first. With runs 991 and 992, Tx/Rx=52.5 is base-accepted for
all three seed2178309 targets; summarize the acquisition policy before testing
cross-seed transfer.

Stage 13HI: seed2178309 Tx/Rx=52.5 acquisition-policy summary.

Run 994 aggregates runs 982 and 987-993. For seed2178309 target1, source
density did not rescue the Tx/Rx=60 weak margin, but Tx/Rx offset did: the
accepted band among tested offsets is 50-55 mm, with 52.5 mm the strongest
sampled point. At Tx/Rx=52.5, target0, target1, and target2 are all
truth-preserving and base-accepted. The remaining caveats are target0 late and
late_high deficits plus target1 early_high. Test cross-seed transfer next with
seed832040 target1 at 5 sources and Tx/Rx=52.5.

Stage 13HJ: seed832040 target1 Tx/Rx=52.5 cross-seed transfer probe.

Run 995 tests whether the seed2178309 Tx/Rx=52.5 acquisition remedy transfers
to seed832040 target1. It is exact but weak, with a base margin of 4.179e-04,
or 8.209e-05 below cutoff. Highband, late, and late_high clear cutoff, but
veryhigh and early_high remain below cutoff. The margin improves over the
seed832040 Tx/Rx=60 5-source control but does not replace the known 9-source
rescue. Continue the acquisition bracket with seed832040 target1 at Tx/Rx=50.

Stage 13HK: seed832040 target1 Tx/Rx=50 lower-bracket probe.

Run 996 tests the lower side of the seed2178309 accepted offset band. It is
exact but weak, with a base margin of 4.149e-04, or 8.513e-05 below cutoff.
Highband, late, and late_high remain above cutoff, while base, veryhigh, and
early_high remain below. Because Tx/Rx=50 is slightly worse than Tx/Rx=52.5,
complete the bracket with seed832040 target1 at Tx/Rx=55 before declaring
acquisition-only rescue exhausted.

Stage 13HL: seed832040 target1 Tx/Rx=55 upper-bracket probe.

Run 997 completes the 5-source acquisition-only bracket. It is exact but weak,
with a base margin of 4.156e-04, or 8.438e-05 below cutoff. The same diagnostic
pattern remains: highband, late, and late_high clear cutoff, but base,
veryhigh, and early_high are weak. Tx/Rx=52.5 is the best tested 5-source
offset, but acquisition alone does not replace the seed832040 9-source rescue.
Run a combined policy at 7 sources and Tx/Rx=52.5.

Stage 13HM: seed832040 target1 7-source Tx/Rx=52.5 combined-policy probe.

Run 998 tests whether the best 5-source offset can reduce the source-density
rescue requirement. It is exact but weak, with a base margin of 4.383e-04, or
6.173e-05 below cutoff. It improves over the 5-source Tx/Rx=52.5 row and
raises veryhigh above cutoff, but base and early_high remain weak. Run
9 sources at Tx/Rx=52.5 to compare with the known 9-source Tx/Rx=60 accepted
rescue.

Stage 13HN: seed832040 target1 9-source Tx/Rx=52.5 combined-policy rescue.

Run 999 cleanly rescues seed832040 target1. It is exact and accepted with a
base margin of 5.297e-04, or 2.970e-05 above cutoff. All six diagnostic
objective variants clear cutoff and rank the true target1 geometry first. This
improves the older 9-source Tx/Rx=60 rescue by about 1.30e-05, so Tx/Rx=52.5
does not replace source density for seed832040 but strengthens the accepted
9-source rescue. Test the same offset on seed1346269 target0, where Tx/Rx=60
required escalation from 8 to 11 sources.

Stage 13HO: seed1346269 target0 8-source Tx/Rx=52.5 acquisition rescue.

Run 1000 shows that Tx/Rx=52.5 rescues seed1346269 target0 at 8 sources. The
row is exact and base-accepted with a margin of 5.368e-04, or 3.682e-05 above
cutoff. Late and late_high remain below cutoff, so the result carries the
target0 late-window caveat, but it avoids the previous Tx/Rx=60 escalation to
11 sources. Test seed1346269 target2 at 5 sources and Tx/Rx=52.5 next.

Stage 13HP: seed1346269 target2 5-source Tx/Rx=52.5 transfer probe.

Run 1001 tests whether Tx/Rx=52.5 rescues seed1346269 target2 at 5 sources.
It is exact but weak, with a base margin of 4.859e-04, or 1.415e-05 below
cutoff. Highband, late, late_high, and veryhigh clear cutoff, but early_high
also remains weak. Since Tx/Rx=52.5 is not the 5-source remedy, bracket source
density at the original Tx/Rx=60 with a 7-source target2 run.

Stage 13HQ: seed1346269 target2 7-source Tx/Rx=60 source-density bracket.

Run 1002 rescues seed1346269 target2 at 7 sources and Tx/Rx=60. It is exact
and base-accepted with a margin of 5.181e-04, or 1.810e-05 above cutoff. All
diagnostic variants except early_high clear cutoff. This reduces the previous
9-source rescue requirement for base confidence, but the early_high caveat
means the old 9-source row remains cleaner. Check target1 at Tx/Rx=52.5 next
for offset safety.

Stage 13HR: seed1346269 target1 5-source Tx/Rx=52.5 offset safety check.

Run 1003 confirms that Tx/Rx=52.5 is safe for seed1346269 target1. It is exact
and cleanly accepted with a base margin of 5.427e-04, or 4.269e-05 above
cutoff, and all diagnostic objectives clear cutoff. Summarize the revised
seed1346269 policy while continuing the Fibonacci replication chain with
seed3524578 target0.

Stage 13HS: seed1346269 revised Tx/Rx=52.5/source-density policy summary.

Run 1005 aggregates runs 973-978 and 1000-1003. The revised seed1346269 policy
uses 8-source Tx/Rx=52.5 for target0, 7-source Tx/Rx=60 for target2, and
5-source Tx/Rx=52.5 for target1. Target0 keeps late-window caveats, target2
keeps an early_high caveat, and target1 is clean. Continue Fibonacci
replication with seed3524578 target0 under the original 8-source Tx/Rx=60
control.

Stage 13HT: seed3524578 target0 8-source Tx/Rx=60 control.

Run 1004 starts the seed3524578 branch. It is exact and cleanly accepted with
a base margin of 5.715e-04, or 7.154e-05 above cutoff. All six diagnostic
objective variants clear cutoff and rank the true target0 geometry first.
Continue the branch with target2 at 5 sources and Tx/Rx=60.

Stage 13HU: seed3524578 target2 5-source Tx/Rx=60 control.

Run 1006 continues the seed3524578 branch. It is exact and base-accepted with
a margin of 5.692e-04, or 6.918e-05 above cutoff. Highband, late, late_high,
and veryhigh clear cutoff; early_high is just below cutoff at 4.897e-04 while
still ranking the true target2 geometry first. Carry that early-window caveat
and continue with seed3524578 target1 at 5 sources and Tx/Rx=60.

Stage 13HV: seed3524578 target1 5-source Tx/Rx=60 control.

Run 1007 completes the seed3524578 target-specific branch. It is exact and
cleanly accepted with a base margin of 5.524e-04, or 5.240e-05 above cutoff,
and all diagnostic objective variants clear cutoff while ranking the true
target1 geometry first. Seed3524578 therefore needs no rescue beyond carrying
the run-1006 target2 early_high caveat. Continue the Fibonacci replication
chain with seed5702887 target0 at 8 sources and Tx/Rx=60.

Stage 13HW: seed5702887 target0 8-source Tx/Rx=60 control.

Run 1008 starts the seed5702887 branch. It is exact but weak, with a base
margin of 4.695e-04, or 3.052e-05 below cutoff. Highband and veryhigh clear
cutoff, but base, late, late_high, and early_high are below while all variants
still rank the true target0 geometry first. Because seed1346269 target0 was
rescued at the same source count by Tx/Rx=52.5, run the 8-source Tx/Rx=52.5
acquisition rescue before escalating source density.

Stage 13HX: seed5702887 target0 8-source Tx/Rx=52.5 acquisition rescue.

Run 1009 improves seed5702887 target0 from weak to marginally accepted. It is
exact with a base margin of 5.003e-04, only 2.552e-07 above cutoff. Highband,
veryhigh, and early_high clear cutoff, but late and late_high remain below by
about 1.0e-04. Because the base reserve is razor-thin, bracket the acquisition
remedy at Tx/Rx=50 before deciding between a lower-offset policy and source
density escalation.

Stage 13HY: seed5702887 target0 8-source Tx/Rx=50 acquisition bracket.

Run 1010 is exact and base-accepted with a margin of 5.105e-04, or 1.051e-05
above cutoff. It is stronger than both Tx/Rx=52.5 and Tx/Rx=60, and highband,
veryhigh, and early_high clear cutoff. Late and late_high remain below cutoff,
though with smaller deficits than the previous offsets. Run one lower-edge
Tx/Rx=45 bracket to test whether the lower-offset improvement continues.

Stage 13HZ: seed5702887 target0 8-source Tx/Rx=45 acquisition bracket.

Run 1011 is exact and base-accepted with a margin of 5.314e-04, or 3.138e-05
above cutoff. It is the strongest tested target0 8-source offset for
seed5702887. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain just below cutoff by 1.079e-05 and 7.469e-06. Stop the
target0 acquisition sweep here and continue with seed5702887 target2 at the
standard 5-source Tx/Rx=60 control.

Stage 13IA: seed5702887 target2 5-source Tx/Rx=60 control.

Run 1012 is exact but weak, with a base margin of 4.419e-04, or 5.581e-05
below cutoff. Highband, late, late_high, and veryhigh clear cutoff, but base
and early_high are weak. All variants still rank the true target2 geometry
first. Run a 7-source Tx/Rx=60 target2 rescue before considering 9 sources.

Stage 13IB: seed5702887 target2 7-source Tx/Rx=60 rescue.

Run 1013 is exact but still weak, with a base margin of 4.329e-04, or
6.706e-05 below cutoff. The 7-source run is worse than the 5-source control in
base and early_high, while highband and late-window variants clear cutoff.
Run 9 sources once to test whether source density recovers nonmonotonically;
if it fails, switch mechanism rather than continuing blind source escalation.

Stage 13IC: seed5702887 target2 9-source Tx/Rx=60 escalation.

Run 1014 is exact and close but still weak, with a base margin of 4.834e-04,
or 1.656e-05 below cutoff. Highband, late, late_high, and veryhigh are strong,
but base and early_high remain below cutoff. Since Tx/Rx=60 source density
alone has not accepted target2, switch mechanism by combining 9 sources with
the lower Tx/Rx=45 acquisition point that rescued seed5702887 target0.

Stage 13ID: seed5702887 target2 9-source Tx/Rx=45 combined rescue.

Run 1015 is exact but worse than the 9-source Tx/Rx=60 row, with a base margin
of 3.767e-04, or 1.233e-04 below cutoff. Highband also drops just below
cutoff, while late-window variants remain accepted. The lower-offset target0
policy does not transfer to target2. Bracket the target2 acquisition mechanism
on the wider side with 9 sources and Tx/Rx=65.

Stage 13IE: seed5702887 target2 9-source Tx/Rx=65 wider-aperture bracket.

Run 1016 is exact but still weak, with a base margin of 4.749e-04, or
2.506e-05 below cutoff. It is better than Tx/Rx=45 but worse than Tx/Rx=60.
The acquisition bracket did not beat the original aperture, so return to
Tx/Rx=60 and run one 11-source escalation before declaring target2 unresolved.

Stage 13IF: seed5702887 target2 11-source Tx/Rx=60 escalation.

Run 1017 is exact but still weak, with a base margin of 4.422e-04, or
5.578e-05 below cutoff. It is weaker than the 9-source Tx/Rx=60 row and does
not resolve target2. Since source density and acquisition brackets have both
failed to reach base confidence while preserving truth, stop target2 escalation
for this branch and run the seed5702887 target1 5-source Tx/Rx=60 control.

Stage 13IG: seed5702887 target1 5-source Tx/Rx=60 control and branch close.

Run 1018 closes the seed5702887 branch. Target1 is exact and accepted at the
original 5-source Tx/Rx=60 control, with a base margin of 5.235e-04, or
2.350e-05 above cutoff. All six diagnostic objectives rank the true target1
geometry first, although early_high is accepted by only 2.349e-07. The branch
policy is now: target0 uses 8 sources at Tx/Rx=45 with late-window caveats,
target2 remains exact but unresolved/weak after the tested source-density and
acquisition brackets, and target1 is accepted at the original control. Continue
the Fibonacci replication chain with seed9227465 target0 at 8 sources and
Tx/Rx=60.

Stage 13IH: seed9227465 target0 8-source Tx/Rx=60 control.

Run 1019 starts the seed9227465 branch. It is exact and base-accepted with a
margin of 5.252e-04, or 2.520e-05 above cutoff. Highband, veryhigh, and
early_high clear cutoff; late and late_high remain below cutoff while still
ranking the true target0 geometry first. Carry the target0 late-window caveat
and continue with seed9227465 target2 at the standard 5-source Tx/Rx=60
control.

Stage 13II: seed9227465 target2 5-source Tx/Rx=60 control.

Run 1020 is exact and cleanly accepted with a base margin of 5.770e-04, or
7.696e-05 above cutoff. All six diagnostic objectives clear cutoff and rank
the true target2 geometry first. This branch therefore does not repeat the
seed5702887 target2 weakness. Continue with seed9227465 target1 at the
standard 5-source Tx/Rx=60 control.

Stage 13IJ: seed9227465 target1 5-source Tx/Rx=60 control.

Run 1021 is exact but weak, with a base margin of 4.965e-04, or 3.540e-06
below cutoff. Highband, late, late_high, and veryhigh clear cutoff; base and
early_high are weak while all six variants still rank the true target1
geometry first. Because the base miss is narrow and prior target1 evidence
supports Tx/Rx=52.5 as a low-cost acquisition remedy, run seed9227465 target1
with 5 sources and Tx/Rx=52.5 before escalating source density.

Stage 13IK: seed9227465 target1 5-source Tx/Rx=52.5 rescue and branch close.

Run 1022 rescues seed9227465 target1 base confidence at 5 sources and
Tx/Rx=52.5. It is exact and accepted with a base margin of 5.044e-04, or
4.378e-06 above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high remains weak while still ranking the true geometry first. Close the
seed9227465 branch with these policies: target0 accepted at 8-source Tx/Rx=60
with late-window caveats, target2 clean at 5-source Tx/Rx=60, and target1
accepted at 5-source Tx/Rx=52.5 with an early_high caveat and small base
reserve. Continue the Fibonacci replication chain with seed14930352 target0.

Stage 13IL: seed14930352 target0 8-source Tx/Rx=60 control.

Run 1023 starts the seed14930352 branch. It is exact but weak, with a base
margin of 4.932e-04, or 6.777e-06 below cutoff. Highband, veryhigh, and
early_high clear cutoff; base, late, and late_high are weak while all six
variants still rank the true target0 geometry first. Follow the existing
target0 rescue policy and run the 8-source Tx/Rx=52.5 acquisition probe before
source-density escalation.

Stage 13IM: seed14930352 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1024 is exact but still weak, with a base margin of 4.843e-04, or
1.572e-05 below cutoff. Tx/Rx=52.5 worsens the base margin relative to
Tx/Rx=60 by about 8.94e-06. Highband, veryhigh, and early_high remain above
cutoff, but base, late, and late_high are weak. Since the first acquisition
probe moved the wrong direction on base confidence, switch mechanism to source
density at Tx/Rx=60 and run a 9-source target0 bracket.

Stage 13IN: seed14930352 target0 9-source Tx/Rx=60 source-density bracket.

Run 1025 is exact but still weak, with a base margin of 4.785e-04, or
2.154e-05 below cutoff. It is weaker than both 8-source rows, while highband,
veryhigh, and early_high clear cutoff and all variants preserve the true
geometry as rank 1. Because seed1346269 target0 accepted only after an
11-source escalation following weak 8- and 9-source rows, run one 11-source
Tx/Rx=60 escalation before declaring seed14930352 target0 unresolved.

Stage 13IO: seed14930352 target0 11-source Tx/Rx=60 escalation.

Run 1026 is exact but still weak, with a base margin of 4.500e-04, or
5.000e-05 below cutoff. It is the weakest tested target0 row in this branch.
Highband and veryhigh clear cutoff; base, late, late_high, and early_high are
weak while all variants still rank the true geometry first. Stop target0
escalation for seed14930352 under the tested mechanisms and continue the
branch with target2 at the standard 5-source Tx/Rx=60 control.

Stage 13IP: seed14930352 target2 5-source Tx/Rx=60 control.

Run 1027 is exact but weak, with a base margin of 4.965e-04, or 3.540e-06
below cutoff. Highband, late, late_high, and veryhigh clear cutoff; base and
early_high are weak while all variants rank the true target2 geometry first.
Run a 7-source Tx/Rx=60 source-density bracket before trying acquisition
offsets.

Stage 13IQ: seed14930352 target2 7-source Tx/Rx=60 rescue.

Run 1028 rescues seed14930352 target2 base confidence. It is exact and
accepted with a base margin of 5.148e-04, or 1.478e-05 above cutoff. Highband,
late, late_high, and veryhigh clear cutoff; early_high remains weak while
ranking the true geometry first. Carry the early_high caveat and continue the
branch with target1 at the standard 5-source Tx/Rx=60 control.

Stage 13IR: seed14930352 target1 5-source Tx/Rx=60 control and branch close.

Run 1029 cleanly accepts seed14930352 target1. It is exact with a base margin
of 5.259e-04, or 2.592e-05 above cutoff, and all diagnostic variants clear
cutoff while ranking the true geometry first. Close the seed14930352 branch:
target0 is exact but unresolved under the tested rescue mechanisms, target2
is accepted at 7-source Tx/Rx=60 with an early_high caveat, and target1 is
clean. Continue the Fibonacci replication chain with seed24157817 target0.

Stage 13IS: seed24157817 target0 8-source Tx/Rx=60 control.

Run 1030 starts the seed24157817 branch. It is exact and base-accepted with a
margin of 5.165e-04, or 1.651e-05 above cutoff. Highband, veryhigh, and
early_high also clear cutoff, while late and late_high remain below cutoff but
still rank the true target0 geometry first. Carry the target0 late-window
caveat and continue the branch with seed24157817 target2 at the standard
5-source Tx/Rx=60 control.

Stage 13IT: seed24157817 target2 5-source Tx/Rx=60 control.

Run 1031 cleanly accepts seed24157817 target2 at the standard control. It is
exact with a base margin of 5.904e-04, or 9.044e-05 above cutoff, and all six
diagnostic objectives clear cutoff while ranking the true target2 geometry
first. Continue the branch with seed24157817 target1 at the standard 5-source
Tx/Rx=60 control.

Stage 13IU: seed24157817 target1 5-source Tx/Rx=60 control.

Run 1032 is exact but weak. The base margin is 4.794e-04, or 2.058e-05 below
cutoff, and early_high is also weak. Highband, late, late_high, and veryhigh
clear cutoff, and all six diagnostics rank the true target1 geometry first.
This matches the seed9227465 target1 pattern, so run a 5-source Tx/Rx=52.5
acquisition rescue before escalating source density.

Stage 13IV: seed24157817 target1 5-source Tx/Rx=52.5 rescue and branch close.

Run 1033 rescues seed24157817 target1. It is exact and accepted with a base
margin of 5.592e-04, or 5.919e-05 above cutoff. All diagnostic variants clear
cutoff and rank the true geometry first, although early_high only clears by
about 2.69e-06. Close the seed24157817 branch with target0 accepted at
8-source Tx/Rx=60 with late-window caveats, target2 clean at 5-source
Tx/Rx=60, and target1 accepted at 5-source Tx/Rx=52.5 with a narrow early_high
reserve. Continue the Fibonacci replication chain with seed39088169 target0.

Stage 13IW: seed39088169 target0 8-source Tx/Rx=60 control.

Run 1034 starts the seed39088169 branch. It is exact and base-accepted with a
margin of 5.545e-04, or 5.453e-05 above cutoff. Highband, veryhigh, and
early_high also clear cutoff, while late and late_high remain below cutoff but
still rank the true target0 geometry first. Carry the target0 late-window
caveat and continue with seed39088169 target2 at the standard 5-source
Tx/Rx=60 control.

Stage 13IX: seed39088169 target2 5-source Tx/Rx=60 control.

Run 1035 accepts seed39088169 target2 at the standard control. It is exact
with a base margin of 5.147e-04, or 1.470e-05 above cutoff. Highband, late,
late_high, and veryhigh also clear cutoff, while early_high remains weak but
still ranks the true target2 geometry first. Carry the early_high caveat and
continue the branch with seed39088169 target1 at the standard 5-source
Tx/Rx=60 control.

Stage 13IY: seed39088169 target1 5-source Tx/Rx=60 control and branch close.

Run 1036 accepts seed39088169 target1 at the standard control. It is exact
with a base margin of 5.482e-04, or 4.819e-05 above cutoff. Highband, late,
late_high, and veryhigh also clear cutoff; early_high is barely weak, missing
cutoff by about 1.30e-06 while still ranking the true geometry first. Close the
seed39088169 branch with target0 accepted at 8-source Tx/Rx=60 with
late-window caveats, target2 accepted at 5-source Tx/Rx=60 with an early_high
caveat, and target1 accepted at 5-source Tx/Rx=60 with a narrow early_high
caveat. Continue the Fibonacci replication chain with seed63245986 target0.

Stage 13IZ: seed63245986 target0 8-source Tx/Rx=60 control.

Run 1037 starts the seed63245986 branch. It is exact and base-accepted with a
small margin of 5.107e-04, or 1.071e-05 above cutoff. Highband, veryhigh, and
early_high clear cutoff, while late and late_high remain below cutoff but rank
the true target0 geometry first. Carry both caveats, the small base reserve and
the late-window weakness, and continue with seed63245986 target2 at the
standard 5-source Tx/Rx=60 control.

Stage 13JA: seed63245986 target2 5-source Tx/Rx=60 control.

Run 1038 cleanly accepts seed63245986 target2 at the standard control. It is
exact with a base margin of 5.798e-04, or 7.979e-05 above cutoff, and all six
diagnostic objectives clear cutoff while ranking the true target2 geometry
first. Continue the branch with seed63245986 target1 at the standard 5-source
Tx/Rx=60 control.

Stage 13JB: seed63245986 target1 5-source Tx/Rx=60 control.

Run 1039 is exact but weak. The base margin is 4.746e-04, or 2.540e-05 below
cutoff, and early_high is also weak. Highband, late, late_high, and veryhigh
clear cutoff, and all six diagnostics rank the true target1 geometry first.
This matches the recurring target1 weak-control pattern, so run a 5-source
Tx/Rx=52.5 acquisition rescue before escalating source density.

Stage 13JC: seed63245986 target1 5-source Tx/Rx=52.5 rescue and branch close.

Run 1040 rescues seed63245986 target1 base confidence. It is exact and
accepted with a base margin of 5.381e-04, or 3.809e-05 above cutoff. Highband,
late, late_high, and veryhigh clear cutoff; early_high improves relative to
the weak control but remains slightly below cutoff while ranking the true
geometry first. Close the seed63245986 branch with target0 accepted at
8-source Tx/Rx=60 with small base reserve and late-window caveats, target2
clean at 5-source Tx/Rx=60, and target1 accepted at 5-source Tx/Rx=52.5 with
an early_high caveat. Continue the Fibonacci replication chain with
seed102334155 target0.

Stage 13JD: seed102334155 target0 8-source Tx/Rx=60 control.

Run 1041 starts the seed102334155 branch. It is exact and base-accepted with a
margin of 5.203e-04, or 2.030e-05 above cutoff. Highband, veryhigh, and
early_high clear cutoff, while late and late_high remain below cutoff but rank
the true target0 geometry first. Carry the target0 late-window caveat and
continue with seed102334155 target2 at the standard 5-source Tx/Rx=60 control.

Stage 13JE: seed102334155 target2 5-source Tx/Rx=60 control.

Run 1042 is exact but weak. The base margin is 4.591e-04, or 4.093e-05 below
cutoff, and early_high is also weak. Highband, late, late_high, and veryhigh
clear cutoff, and all six diagnostics rank the true target2 geometry first.
Run the established target2 source-density rescue with 7 sources at Tx/Rx=60
before trying acquisition offsets.

Stage 13JF: seed102334155 target2 7-source Tx/Rx=60 source-density rescue.

Run 1043 is exact but still weak. Base improves from 4.591e-04 to 4.777e-04,
but remains 2.223e-05 below cutoff; early_high is also weak. Since all
diagnostics still rank the true target2 geometry first and source density
moved the base margin in the right direction, run one 9-source Tx/Rx=60
escalation before trying acquisition offsets.

Stage 13JG: seed102334155 target2 9-source Tx/Rx=60 source-density escalation.

Run 1044 cleanly accepts seed102334155 target2. It is exact with a base margin
of 5.820e-04, or 8.199e-05 above cutoff, and all six diagnostic objectives
clear cutoff while ranking the true geometry first. The source-density path is
5-source weak, 7-source improved but weak, then 9-source accepted. Continue
the branch with seed102334155 target1 at the standard 5-source Tx/Rx=60
control.

Stage 13JH: seed102334155 target1 5-source Tx/Rx=60 control.

Run 1045 is exact but weak. The base margin is 4.860e-04, or 1.402e-05 below
cutoff, and early_high is also weak. Highband, late, late_high, and veryhigh
clear cutoff, and all six diagnostics rank the true target1 geometry first.
Run the standard 5-source Tx/Rx=52.5 target1 rescue.

Stage 13JI: seed102334155 target1 5-source Tx/Rx=52.5 acquisition rescue.

Run 1046 accepts the exact target1 geometry with a narrow base reserve. The
base margin is 5.044e-04, or 4.380e-06 above cutoff, improving over the
Tx/Rx=60 control by about 1.84e-05. Highband, late, late_high, and veryhigh
also clear cutoff; early_high remains weak at 4.589e-04 but still ranks the
true geometry first. This closes the seed102334155 branch: target0 is accepted
with late-window caveats, target2 is accepted cleanly after the 9-source
source-density rescue, and target1 is accepted by the Tx/Rx=52.5 acquisition
rescue. Advance to seed165580141 target0 with the standard 8-source Tx/Rx=60
control.

Stage 13JJ: seed165580141 target0 8-source Tx/Rx=60 control.

Run 1047 accepts the exact target0 geometry with a narrow base reserve. The
base margin is 5.049e-04, or 4.932e-06 above cutoff. Highband, veryhigh, and
early_high clear cutoff; late and late_high remain below cutoff at 3.970e-04
and 4.612e-04, respectively, while still ranking the true target0 geometry
first. Continue the branch with seed165580141 target2 at the standard
5-source Tx/Rx=60 control.

Stage 13JK: seed165580141 target2 5-source Tx/Rx=60 control.

Run 1048 accepts the exact target2 geometry at the standard 5-source control.
The base margin is 5.385e-04, or 3.853e-05 above cutoff. Highband, late,
late_high, and veryhigh also clear cutoff; early_high remains weak at
4.653e-04 but still ranks the true target2 geometry first. Continue the
branch with seed165580141 target1 at the standard 5-source Tx/Rx=60 control.

Stage 13JL: seed165580141 target1 5-source Tx/Rx=60 control.

Run 1049 accepts the exact target1 geometry cleanly at the standard control.
The base margin is 5.898e-04, or 8.979e-05 above cutoff, and all six
diagnostic objectives clear cutoff while ranking the true geometry first.
This closes seed165580141: target0 is accepted with late-window caveats,
target2 is accepted with an early_high caveat, and target1 is accepted
cleanly. Advance to seed267914296 target0 with the standard 8-source Tx/Rx=60
control.

Stage 13JM: seed267914296 target0 8-source Tx/Rx=60 control.

Run 1050 is exact but weak. The base margin is 4.964e-04, or 3.605e-06 below
cutoff. Highband, veryhigh, and early_high clear cutoff; late and late_high
remain below cutoff while still ranking the true target0 geometry first.
Follow the target0 weak-control policy by running the 8-source Tx/Rx=52.5
acquisition rescue before changing source density or advancing the branch.

Stage 13JN: seed267914296 target0 8-source Tx/Rx=52.5 acquisition rescue.

Run 1051 is exact but weak. Tx/Rx=52.5 worsens the base margin to
4.933e-04, or 6.692e-06 below cutoff, compared with 4.964e-04 at Tx/Rx=60.
Highband, veryhigh, and early_high remain above cutoff; late and late_high
remain below cutoff while ranking the true target0 geometry first. Because
the acquisition-offset probe moved base confidence in the wrong direction,
switch mechanism to a 9-source Tx/Rx=60 source-density bracket.

Stage 13JO: seed267914296 target0 9-source Tx/Rx=60 source-density bracket.

Run 1052 rescues the exact target0 geometry. The base margin is 5.319e-04, or
3.193e-05 above cutoff, improving over both 8-source Tx/Rx=60 and 8-source
Tx/Rx=52.5. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain below cutoff while ranking the true target0 geometry first.
Carry the target0 late-window caveat forward and continue the branch with
seed267914296 target2 at the standard 5-source Tx/Rx=60 control.

Stage 13JP: seed267914296 target2 5-source Tx/Rx=60 control.

Run 1053 is exact but weak. The base margin is 4.923e-04, or 7.706e-06 below
cutoff, and early_high is also weak at 4.230e-04. Highband, late, late_high,
and veryhigh clear cutoff, and all six objectives rank the true target2
geometry first. Run a 7-source Tx/Rx=60 source-density bracket before
considering a 9-source escalation.

Stage 13JQ: seed267914296 target2 7-source Tx/Rx=60 source-density bracket.

Run 1054 is exact but weak. The base margin worsens to 4.728e-04, or
2.718e-05 below cutoff, and early_high remains weak at 4.205e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six objectives rank the
true target2 geometry first. Since source density has not yet been tested at
the accepted 9-source level for this target, run a 9-source Tx/Rx=60
escalation before changing mechanism.

Stage 13JR: seed267914296 target2 9-source Tx/Rx=60 source-density escalation.

Run 1055 rescues the exact target2 geometry cleanly. The base margin is
5.183e-04, or 1.833e-05 above cutoff, and all six diagnostic objectives clear
cutoff while ranking the true geometry first. This closes the target2 rescue
path for seed267914296. Continue the branch with target1 at the standard
5-source Tx/Rx=60 control.

Stage 13JS: seed267914296 target1 5-source Tx/Rx=60 control.

Run 1056 is exact but weak. The base margin is 4.666e-04, or 3.339e-05 below
cutoff, and early_high is also weak at 4.418e-04. Highband, late, late_high,
and veryhigh clear cutoff, and all six objectives rank the true target1
geometry first. Run the standard 5-source Tx/Rx=52.5 acquisition rescue.

Stage 13JT: seed267914296 target1 5-source Tx/Rx=52.5 acquisition rescue.

Run 1057 is exact and improves every diagnostic margin over the Tx/Rx=60
control, but it remains weak. The base margin is 4.895e-04, or 1.053e-05
below cutoff; early_high is also weak at 4.470e-04. Highband, late,
late_high, and veryhigh clear cutoff, and all six objectives rank the true
target1 geometry first. Because prior seed832040 target1 evidence showed
that the 7-source Tx/Rx=52.5 intermediate remained weak while 9 sources
accepted cleanly, run the 9-source Tx/Rx=52.5 combined-policy rescue next.

Stage 13JU: seed267914296 target1 9-source Tx/Rx=52.5 combined rescue.

Run 1058 is exact and accepted. The base margin is 5.080e-04, or 7.956e-06
above cutoff, and all six diagnostic objectives rank the true target1
geometry first. Early_high clears cutoff by only about 1.49e-07, so carry a
tight early-window/high-band reserve caveat. Seed267914296 is accepted with
target0 late/late_high caveats, clean target2 rescue, and tight-reserve
target1 rescue. Advance to seed433494437 target0 with the standard
8-source Tx/Rx=60 control.

Stage 13JV: seed433494437 target0 8-source Tx/Rx=60 control.

Run 1059 is exact and accepted. The base margin is 5.408e-04, or 4.081e-05
above cutoff, and all six diagnostic objectives rank the true target0
geometry first. The late objective remains weak at 4.566e-04, so carry the
recurring target0 late-window caveat. Continue seed433494437 with target2 at
the standard 5-source Tx/Rx=60 control.

Stage 13JW: seed433494437 target2 5-source Tx/Rx=60 control.

Run 1060 is exact and accepted. The base margin is 5.170e-04, or 1.698e-05
above cutoff, and all six diagnostic objectives rank the true target2
geometry first. Early_high remains weak at 4.676e-04, so carry an
early-window/high-band caveat. Continue seed433494437 with target1 at the
standard 5-source Tx/Rx=60 control.

Stage 13JX: seed433494437 target1 5-source Tx/Rx=60 control.

Run 1061 is exact but weak. The base margin is 4.897e-04, or 1.031e-05 below
cutoff, and early_high is also weak at 4.380e-04. Highband, late, late_high,
and veryhigh clear cutoff, and all six diagnostic objectives rank the true
target1 geometry first. Run the established 5-source Tx/Rx=52.5 acquisition
rescue; do not create a separate branch-summary output folder before the
rescue result exists.

Stage 13JY: seed433494437 target1 5-source Tx/Rx=52.5 acquisition rescue.

Run 1062 is exact and accepted. The base margin is 5.144e-04, or 1.442e-05
above cutoff, and all six diagnostic objectives rank the true target1
geometry first. Early_high remains weak at 4.414e-04, so carry an
early-window/high-band caveat. This closes seed433494437 without a separate
numbered summary output folder: target0 accepted with a late-window caveat,
target2 accepted with an early_high caveat, and target1 accepted after the
Tx/Rx=52.5 acquisition rescue. Advance to seed701408733 target0 with the
standard 8-source Tx/Rx=60 control.

Stage 13JZ: seed701408733 target0 8-source Tx/Rx=60 control.

Run 1063 is exact but weak. The base margin is 4.854e-04, or 1.463e-05 below
cutoff; late and late_high are also weak. Highband, veryhigh, and early_high
clear cutoff, and all six diagnostic objectives rank the true target0
geometry first. Run the 8-source Tx/Rx=52.5 acquisition probe before any
source-density escalation.

Stage 13KA: seed701408733 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1064 is exact and accepted. The base margin is 5.137e-04, or 1.373e-05
above cutoff, and all six diagnostic objectives rank the true target0
geometry first. Late and late_high remain weak, so carry the recurring
late-window caveat. Continue seed701408733 with target2 at the standard
5-source Tx/Rx=60 control.

Stage 13KB: seed701408733 target2 5-source Tx/Rx=60 control.

Run 1065 is exact and clean. The base margin is 5.231e-04, or 2.312e-05
above cutoff, and all six diagnostic objectives clear cutoff while ranking
the true target2 geometry first. Continue seed701408733 with target1 at the
standard 5-source Tx/Rx=60 control.

Stage 13KC: seed701408733 target1 5-source Tx/Rx=60 control.

Run 1066 is exact and clean. The base margin is 5.057e-04, or 5.651e-06
above cutoff, and all six diagnostic objectives clear cutoff while ranking
the true target1 geometry first. This closes seed701408733 without a separate
numbered summary output folder: target0 accepted after Tx/Rx=52.5 with a
late-window caveat, target2 accepted cleanly, and target1 accepted cleanly.
Advance to seed1134903170 target0 with the standard 8-source Tx/Rx=60
control.

Stage 13KD: seed1134903170 target0 8-source Tx/Rx=60 control.

Run 1067 is exact and accepted. The base margin is 5.285e-04, or 2.849e-05
above cutoff, and all six diagnostic objectives rank the true target0
geometry first. Late and late_high remain weak, so carry the recurring
target0 late-window caveat. Continue seed1134903170 with target2 at the
standard 5-source Tx/Rx=60 control. Do not create a separate branch-summary
output folder before all branch targets have evidence.

Stage 13KE: seed1134903170 target2 5-source Tx/Rx=60 control.

Run 1068 is exact and accepted. The base margin is 5.769e-04, or 7.693e-05
above cutoff, and all six diagnostic objectives rank the true target2
geometry first. Early_high is narrowly weak at 4.960e-04, so carry a tight
early-window/high-band caveat. Continue seed1134903170 with target1 at the
standard 5-source Tx/Rx=60 control.

Stage 13KF: seed1134903170 target1 5-source Tx/Rx=60 control.

Run 1069 is exact and clean. The base margin is 6.601e-04, or 1.601e-04
above cutoff, and all six diagnostic objectives clear cutoff while ranking
the true target1 geometry first. This closes seed1134903170 without a
separate numbered summary output folder: target0 accepted with a late-window
caveat, target2 accepted with a tight early_high caveat, and target1 accepted
cleanly. Advance to seed1836311903 target0 with the standard 8-source Tx/Rx=60
control.

Stage 13KG: seed1836311903 target0 8-source Tx/Rx=60 control.

Run 1070 is exact and accepted. The base margin is 5.583e-04, or 5.832e-05
above cutoff, and all six diagnostic objectives rank the true target0
geometry first. Late remains weak at 4.290e-04, while late_high narrowly
clears cutoff. Continue seed1836311903 with target2 at the standard
5-source Tx/Rx=60 control.

Stage 13KH: seed1836311903 target2 5-source Tx/Rx=60 control.

Run 1071 is exact and accepted with a tight reserve. The base margin is
5.095e-04, or 9.513e-06 above cutoff, and all six diagnostic objectives rank
the true target2 geometry first. Early_high is weak at 4.353e-04, so carry a
tight early-window/high-band caveat. Continue seed1836311903 with target1 at
the standard 5-source Tx/Rx=60 control.

Stage 13KI: seed1836311903 target1 5-source Tx/Rx=60 control.

Run 1072 is exact and accepted. The base margin is 5.311e-04, or 3.113e-05
above cutoff, and all six diagnostic objectives rank the true target1
geometry first. Early_high is narrowly weak at 4.942e-04, so carry a tight
early-window/high-band caveat. This closes seed1836311903 without a separate
numbered summary output folder: target0 accepted with a late-window caveat,
target2 accepted with a tight early_high caveat, and target1 accepted with a
tight early_high caveat. Advance to seed2971215073 target0 with the standard
8-source Tx/Rx=60 control.

Stage 13KJ: seed2971215073 target0 8-source Tx/Rx=60 control.

Run 1073 is exact and accepted with a tight reserve. The base margin is
5.144e-04, or 1.441e-05 above cutoff, and all six diagnostic objectives rank
the true target0 geometry first. Late and late_high are weak, so carry the
recurring target0 late-window caveat. Continue seed2971215073 with target2 at
the standard 5-source Tx/Rx=60 control.

Stage 13KK: seed2971215073 target2 5-source Tx/Rx=60 control.

Run 1074 is exact and clean. The base margin is 6.000e-04, or 1.000e-04
above cutoff, and all six diagnostic objectives clear cutoff while ranking
the true target2 geometry first. Continue seed2971215073 with target1 at the
standard 5-source Tx/Rx=60 control.

Stage 13KL: seed2971215073 target1 5-source Tx/Rx=60 control.

Run 1075 is exact and clean. The base margin is 6.022e-04, or 1.022e-04
above cutoff, and all six diagnostic objectives clear cutoff while ranking
the true target1 geometry first. This closes seed2971215073 without a
separate numbered summary output folder: target0 accepted with a tight base
reserve and late-window caveat, target2 accepted cleanly, and target1 accepted
cleanly. The next Fibonacci value is 4807526976. Although this exceeds the
common 32-bit unsigned RNG seed limit, the current code path uses
`np.random.default_rng(seed)`, and the active Python environment accepts
`default_rng(4807526976)`. Continue with seed4807526976 target0 at the standard
8-source Tx/Rx=60 control.

Stage 13KM: seed4807526976 target0 8-source Tx/Rx=60 control.

Run 1076 is exact and accepted. The base margin is 5.332e-04, or 3.315e-05
above cutoff, and all six diagnostic objectives rank the true target0
geometry first. Late and late_high are weak, so carry the recurring target0
late-window caveat. Continue seed4807526976 with target2 at the standard
5-source Tx/Rx=60 control.

Stage 13KN: seed4807526976 target2 5-source Tx/Rx=60 control.

Run 1077 is exact and accepted. The base margin is 5.437e-04, or 4.374e-05
above cutoff, and all six diagnostic objectives rank the true target2
geometry first. Early_high is weak at 4.632e-04, so carry an early-window/high
band caveat. Continue seed4807526976 with target1 at the standard 5-source
Tx/Rx=60 control.

Stage 13KO: seed4807526976 target1 5-source Tx/Rx=60 control.

Run 1078 is exact and clean. The base margin is 5.467e-04, or 4.667e-05
above cutoff, and all six diagnostic objectives clear cutoff while ranking
the true target1 geometry first. This closes seed4807526976 without a
separate numbered summary output folder: target0 accepted with a late-window
caveat, target2 accepted with an early_high caveat, and target1 accepted
cleanly. Continue the Fibonacci replication chain with seed7778742049 target0
at the standard 8-source Tx/Rx=60 control.

Stage 13KP: seed7778742049 target0 8-source Tx/Rx=60 control.

Run 1079 is exact but weak. The base margin is 4.633e-04, or 3.669e-05 below
cutoff, while highband and veryhigh clear cutoff and all six diagnostic
objectives rank the true target0 geometry first. Base, late, late_high, and
early_high remain weak, so do not accept target0 yet. Run the established
8-source Tx/Rx=52.5 acquisition probe before moving to target2. No separate
numbered summary output folder was created for this decision.

Stage 13KQ: seed7778742049 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1080 is exact but weak. Tx/Rx=52.5 worsens the base margin to 4.436e-04,
or 5.636e-05 below cutoff, compared with 4.633e-04 at Tx/Rx=60. Highband and
veryhigh clear cutoff, but base, late, late_high, and early_high remain weak
while still ranking the true target0 geometry first. Follow the
seed267914296 precedent and switch mechanism to a 9-source Tx/Rx=60
source-density bracket. No separate numbered summary output folder was
created for this decision.

Stage 13KR: seed7778742049 target0 9-source Tx/Rx=60 source-density bracket.

Run 1081 rescues the exact target0 geometry. The base margin is 5.584e-04, or
5.837e-05 above cutoff, improving over both the 8-source Tx/Rx=60 control and
the 8-source Tx/Rx=52.5 acquisition probe. Highband, veryhigh, and early_high
clear cutoff; late and late_high remain below cutoff while ranking the true
target0 geometry first. Carry the target0 late-window caveat forward and
continue the seed7778742049 branch with target2 at the standard 5-source
Tx/Rx=60 control. No separate numbered summary output folder was created for
this decision.

Stage 13KS: seed7778742049 target2 5-source Tx/Rx=60 control.

Run 1082 is exact but weak. The base margin is 4.904e-04, or 9.637e-06 below
cutoff, and early_high is also weak at 4.450e-04. Highband, late, late_high,
and veryhigh clear cutoff, and all six objectives rank the true target2
geometry first. Follow the target2 weak-control policy by running a 7-source
Tx/Rx=60 source-density bracket before considering a 9-source escalation. No
separate numbered summary output folder was created for this decision.

Stage 13KT: seed7778742049 target2 7-source Tx/Rx=60 source-density bracket.

Run 1083 is exact but weak. The base margin worsens to 4.753e-04, or
2.470e-05 below cutoff, and early_high remains weak at 3.808e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six objectives rank the
true target2 geometry first. Since source density has not yet been tested at
the accepted 9-source level for this target, run one 9-source Tx/Rx=60
escalation before changing mechanism. No separate numbered summary output
folder was created for this decision.

Stage 13KU: seed7778742049 target2 9-source Tx/Rx=60 source-density escalation.

Run 1084 rescues the exact target2 geometry cleanly. The base margin is
5.516e-04, or 5.164e-05 above cutoff, and all six diagnostic objectives clear
cutoff while ranking the true geometry first. This closes the target2 rescue
path for seed7778742049. Continue the branch with target1 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13KV: seed7778742049 target1 5-source Tx/Rx=60 control.

Run 1085 is exact and clean. The base margin is 5.810e-04, or 8.097e-05 above
cutoff, and all six diagnostic objectives clear cutoff while ranking the true
target1 geometry first. This closes seed7778742049 without a separate
numbered summary output folder: target0 accepted at 9-source Tx/Rx=60 with a
late-window caveat, target2 accepted cleanly at 9-source Tx/Rx=60, and target1
accepted cleanly at 5-source Tx/Rx=60. Continue the Fibonacci replication
chain with seed12586269025 target0 after confirming the seed is accepted by
the active NumPy random generator.

Stage 13KW: seed12586269025 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(12586269025)` succeeds
in the active FNO environment. Run 1086 is exact and accepted. The base margin
is 5.673e-04, or 6.731e-05 above cutoff, and all six diagnostic objectives
rank the true target0 geometry first. Late is weak at 4.783e-04, so carry the
target0 late-window caveat, but no rescue is justified. Continue
seed12586269025 with target2 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13KX: seed12586269025 target2 5-source Tx/Rx=60 control.

Run 1087 is exact and clean. The base margin is 5.743e-04, or 7.432e-05 above
cutoff, and all six diagnostic objectives clear cutoff while ranking the true
target2 geometry first. No target2 rescue is justified. Continue
seed12586269025 with target1 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13KY: seed12586269025 target1 5-source Tx/Rx=60 control.

Run 1088 is exact and clean. The base margin is 6.019e-04, or 1.019e-04 above
cutoff, and all six diagnostic objectives clear cutoff while ranking the true
target1 geometry first. This closes seed12586269025 without a separate
numbered summary output folder: target0 accepted at 8-source Tx/Rx=60 with a
late-window caveat, target2 accepted cleanly at 5-source Tx/Rx=60, and target1
accepted cleanly at 5-source Tx/Rx=60. Continue the Fibonacci replication
chain with seed20365011074 target0 after confirming the seed is accepted by
the active NumPy random generator.

Stage 13KZ: seed20365011074 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(20365011074)` succeeds
in the active FNO environment. Run 1089 is exact and accepted but tight. The
base margin is 5.105e-04, or 1.052e-05 above cutoff, and all six diagnostic
objectives rank the true target0 geometry first. Late and late_high are weak
at 4.022e-04 and 4.122e-04, so carry the target0 late-window caveat, but no
rescue is justified before checking target2. Continue seed20365011074 with
target2 at the standard 5-source Tx/Rx=60 control. No separate numbered
summary output folder was created for this decision.

Stage 13LA: seed20365011074 target2 5-source Tx/Rx=60 control.

Run 1090 is exact but weak by the base confidence rule. The base margin is
4.964e-04, or 3.593e-06 below cutoff, and early_high is also weak at
4.836e-04. Highband, late, late_high, and veryhigh clear cutoff, and all six
diagnostic objectives rank the true target2 geometry first. Follow the
target2 weak-control policy by running a 7-source Tx/Rx=60 source-density
bracket before considering a 9-source escalation. No separate numbered summary
output folder was created for this decision.

Stage 13LB: seed20365011074 target2 7-source Tx/Rx=60 source-density bracket.

Run 1091 is exact but still weak. The base margin worsens to 4.743e-04, or
2.569e-05 below cutoff, and early_high remains weak at 4.036e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six diagnostic objectives
rank the true target2 geometry first. Since the 7-source bracket did not
rescue target2, run the 9-source Tx/Rx=60 source-density escalation before
moving to target1. No separate numbered summary output folder was created for
this decision.

Stage 13LC: seed20365011074 target2 9-source Tx/Rx=60 source-density escalation.

Run 1092 nearly rescues target2 but remains technically weak. The base margin
is 4.981e-04, or 1.871e-06 below cutoff. Highband, late, late_high, veryhigh,
and early_high all clear cutoff, and all six diagnostic objectives rank the
true target2 geometry first. Follow the seed610 precedent for weak 9-source
target2 rows by running one 11-source Tx/Rx=60 source-density test before
declaring the simple source-density path unresolved. No separate numbered
summary output folder was created for this decision.

Stage 13LD: seed20365011074 target2 11-source Tx/Rx=60 source-density test.

Run 1093 is exact but clearly weak. The base margin drops to 4.034e-04, or
9.662e-05 below cutoff, and veryhigh plus early_high also fall below cutoff.
Highband, late, and late_high clear cutoff, and all six diagnostic objectives
rank the true target2 geometry first. This closes the simple source-density
ladder for seed20365011074 target2: the best full-ringdown source-count row is
the 9-source near miss from run 1092, but target2 is not formally accepted by
the current base-confidence cutoff. Continue the branch with target1 at the
standard 5-source Tx/Rx=60 control. No separate numbered summary output folder
was created for this decision.

Stage 13LE: seed20365011074 target1 5-source Tx/Rx=60 control.

Run 1094 is exact and accepted. The base margin is 5.320e-04, or 3.200e-05
above cutoff, and all six diagnostic objectives clear cutoff while ranking the
true target1 geometry first. This closes seed20365011074 without a separate
numbered summary output folder: target0 accepted at 8-source Tx/Rx=60 with a
late-window caveat, target2 remains truth-preserving but formally unresolved
with the 9-source near miss as the best source-count row, and target1 accepted
cleanly at 5-source Tx/Rx=60. Continue the Fibonacci replication chain with
seed32951280099 target0 after confirming the seed is accepted by the active
NumPy random generator.

Stage 13LF: seed32951280099 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(32951280099)` succeeds
in the active FNO environment. Run 1095 is exact and accepted. The base margin
is 5.828e-04, or 8.285e-05 above cutoff, and all six diagnostic objectives
rank the true target0 geometry first. Late is weak at 4.522e-04, so carry the
recurring target0 late-window caveat, but no target0 rescue is justified.
Continue seed32951280099 with target2 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

Stage 13LG: seed32951280099 target2 5-source Tx/Rx=60 control.

Run 1096 is exact but weak. The base margin is 4.841e-04, or 1.589e-05 below
cutoff, and early_high is also weak at 3.965e-04. Highband, late, late_high,
and veryhigh clear cutoff, and all six diagnostic objectives rank the true
target2 geometry first. Follow the target2 weak-control policy by running a
7-source Tx/Rx=60 source-density bracket before considering 9 sources. No
separate numbered summary output folder was created for this decision.

Stage 13LH: seed32951280099 target2 7-source Tx/Rx=60 source-density bracket.

Run 1097 is exact but still weak. The base margin worsens to 4.392e-04, or
6.084e-05 below cutoff, and early_high remains weak at 3.812e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six diagnostic objectives
rank the true target2 geometry first. Since the 7-source bracket did not
rescue target2, run the 9-source Tx/Rx=60 source-density escalation before
moving to target1. No separate numbered summary output folder was created for
this decision.

Stage 13LI: seed32951280099 target2 9-source Tx/Rx=60 source-density escalation.

Run 1098 rescues the exact target2 geometry by the base confidence rule. The
base margin is 5.051e-04, or 5.124e-06 above cutoff. Highband, late,
late_high, and veryhigh clear cutoff; early_high remains weak at 4.896e-04.
All six diagnostic objectives rank the true target2 geometry first. Carry the
early_high caveat and continue the branch with target1 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13LJ: seed32951280099 target1 5-source Tx/Rx=60 control.

Run 1099 is exact and accepted. The base margin is 5.749e-04, or 7.490e-05
above cutoff, and all six diagnostic objectives clear cutoff while ranking the
true target1 geometry first. This closes seed32951280099 without a separate
numbered summary output folder: target0 accepted at 8-source Tx/Rx=60 with a
late-window caveat, target2 accepted at 9-source Tx/Rx=60 with an early_high
caveat, and target1 accepted cleanly at 5-source Tx/Rx=60. Continue the
Fibonacci replication chain with seed53316291173 target0 after confirming the
seed is accepted by the active NumPy random generator.

Stage 13LK: seed53316291173 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(53316291173)` succeeds
in the active FNO environment. Run 1100 is exact and accepted. The base margin
is 5.465e-04, or 4.646e-05 above cutoff, and all six diagnostic objectives
rank the true target0 geometry first. Late and late_high remain just below
cutoff at 4.870e-04 and 4.980e-04, so carry the recurring target0 late-window
caveat, but no target0 rescue is justified. Continue seed53316291173 with
target2 at the standard 5-source Tx/Rx=60 control. No separate numbered
summary output folder was created for this decision.

Stage 13LL: coordinate optimizer decision-context figure upgrade.

User review of the single-row `coordinate_confidence_margins.png` plot showed
that the old figure was mathematically sufficient but too context-poor for
reader-facing inspection. The coordinate optimizer now writes
`coordinate_radius_decision_panel.png` as the primary figure and
`coordinate_objective_radius_candidates.png` as an objective top-candidate
view, while keeping the legacy confidence-margin plot for compatibility. Runs
1090 and 1100 were refreshed in place from their existing CSV/JSON artifacts;
no new numbered experiment folder was created. This reporting change does not
alter solver math or any accept/reject decision. Resume seed53316291173 with
target2 at the standard 5-source Tx/Rx=60 control.

Stage 13LM: seed53316291173 target2 5-source Tx/Rx=60 control.

Run 1101 is exact but weak. The base margin is 4.001e-04, or 9.994e-05 below
cutoff. Highband and early_high are also weak at 4.682e-04 and 3.561e-04,
while late, late_high, and veryhigh clear cutoff. All six diagnostic
objectives rank the true target2 geometry first, so the issue is confidence
rather than a wrong geometry. Follow the target2 weak-control policy by
running a 7-source Tx/Rx=60 source-density bracket before considering a
9-source escalation. No separate numbered summary output folder was created
for this decision.

Stage 13LN: seed53316291173 target2 7-source Tx/Rx=60 bracket.

Run 1102 is exact but still weak. The base margin improves from 4.001e-04 to
4.206e-04, but remains 7.936e-05 below cutoff. Highband, late, late_high, and
veryhigh clear cutoff while early_high remains weak at 3.900e-04. All six
diagnostic objectives rank the true target2 geometry first. Since the
7-source bracket did not rescue the base row, run the standard 9-source
Tx/Rx=60 source-density escalation before moving to target1. No separate
numbered summary output folder was created for this decision.

Stage 13LO: seed53316291173 target2 9-source Tx/Rx=60 escalation.

Run 1103 is exact and a near miss. The base margin improves to 4.823e-04,
only 1.775e-05 below cutoff, and highband, late, late_high, and veryhigh all
clear cutoff. Early_high remains weak at 4.520e-04. All six diagnostic
objectives rank the true target2 geometry first. Follow the seed610/20365011074
precedent for weak 9-source target2 rows by running one 11-source Tx/Rx=60
test before closing the simple source-density ladder. No separate numbered
summary output folder was created for this decision.

Stage 13LP: seed53316291173 target2 11-source Tx/Rx=60 source-density closeout.

Run 1104 is exact but weak. The base margin drops to 3.695e-04, or
1.305e-04 below cutoff, so the 11-source escalation does not rescue target2.
Late and late_high clear cutoff, but base, highband, veryhigh, and early_high
remain weak; all six diagnostic objectives still rank the true target2
geometry first. Close the simple 5/7/9/11 source-density ladder for
seed53316291173 target2 as truth-preserving but formally unresolved, with
run 1103 remaining the best source-count row. Continue the seed with target1
at the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13LQ: seed53316291173 target1 5-source Tx/Rx=60 control.

Run 1105 is exact and accepted. The base margin is 5.775e-04, or
7.745e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed53316291173 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 remains
truth-preserving but formally unresolved with run 1103 as the best
source-count row, and target1 accepted cleanly at 5-source Tx/Rx=60.
Continue the Fibonacci replication chain with seed86267571272 target0 after
confirming the seed is accepted by the active NumPy random generator.

Stage 13LR: seed86267571272 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(86267571272)` succeeds
in the active FNO environment. Run 1106 is exact and accepted. The base margin
is 5.180e-04, or 1.803e-05 above cutoff, and all six diagnostic objectives
rank the true target0 geometry first. Late and late_high are weak at
3.727e-04 and 4.116e-04, so carry the recurring target0 late-window caveat,
but no target0 rescue is justified. Continue seed86267571272 with target2 at
the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13LS: seed86267571272 target2 5-source Tx/Rx=60 control.

Run 1107 is exact but weak. The base margin is 4.633e-04, or 3.674e-05 below
cutoff, and early_high is also weak at 3.765e-04. Highband, late, late_high,
and veryhigh clear cutoff, and all six diagnostic objectives rank the true
target2 geometry first. Follow the target2 weak-control policy by running a
7-source Tx/Rx=60 source-density bracket before considering a 9-source
escalation. No separate numbered summary output folder was created for this
decision.

Stage 13LT: seed86267571272 target2 7-source Tx/Rx=60 bracket.

Run 1108 is exact but still weak. The base margin falls to 4.412e-04, or
5.883e-05 below cutoff, and early_high remains weak at 4.021e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six diagnostic objectives
rank the true target2 geometry first. Since the 7-source bracket did not
rescue the base row, run the standard 9-source Tx/Rx=60 source-density
escalation before moving to target1. No separate numbered summary output
folder was created for this decision.

Stage 13LU: seed86267571272 target2 9-source Tx/Rx=60 escalation.

Run 1109 is exact and a near miss. The base margin improves to 4.758e-04, or
2.421e-05 below cutoff, and highband, late, late_high, and veryhigh all clear
cutoff. Early_high remains weak at 4.323e-04. All six diagnostic objectives
rank the true target2 geometry first. Follow the target2 near-miss precedent
by running one 11-source Tx/Rx=60 closeout test before moving to target1. No
separate numbered summary output folder was created for this decision.

Stage 13LV: seed86267571272 target2 11-source Tx/Rx=60 source-density closeout.

Run 1110 is exact but weak. The base margin drops to 3.971e-04, or
1.029e-04 below cutoff, and highband is also just below cutoff at 4.995e-04.
Late, late_high, and veryhigh clear cutoff while early_high remains weak at
3.594e-04. All six diagnostic objectives rank the true target2 geometry
first. Close the simple 5/7/9/11 source-density ladder for seed86267571272
target2 as truth-preserving but formally unresolved, with run 1109 remaining
the best source-count row. Continue the seed with target1 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13LW: seed86267571272 target1 5-source Tx/Rx=60 control.

Run 1111 is exact and accepted. The base margin is 5.219e-04, or
2.188e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed86267571272 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 remains
truth-preserving but formally unresolved with run 1109 as the best
source-count row, and target1 accepted at 5-source Tx/Rx=60. Continue the
Fibonacci replication chain with seed139583862445 target0 after confirming
the seed is accepted by the active NumPy random generator.

Stage 13LX: seed139583862445 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(139583862445)` succeeds
in the active FNO environment. Run 1112 is exact and accepted. The base margin
is 6.294e-04, or 1.294e-04 above cutoff, and all six diagnostic objectives
rank the true target0 geometry first. Late is weak at 4.751e-04 while
late_high clears, so carry the recurring target0 late-window caveat, but no
target0 rescue is justified. Continue seed139583862445 with target2 at the
standard 5-source Tx/Rx=60 control. No separate numbered summary output folder
was created for this decision.

Stage 13LY: seed139583862445 target2 5-source Tx/Rx=60 control.

Run 1113 is exact and accepted. The base margin is 5.401e-04, or
4.013e-05 above cutoff, and all six diagnostic objectives rank the true
target2 geometry first. Early_high is weak at 4.823e-04, so carry that caveat,
but no target2 rescue is justified. Continue seed139583862445 with target1 at
the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13LZ: seed139583862445 target1 5-source Tx/Rx=60 control.

Run 1114 is exact but weak. The base margin is 4.811e-04, or 1.889e-05 below
cutoff, and early_high is also weak at 4.652e-04. Highband, late, late_high,
and veryhigh clear cutoff, and all six diagnostic objectives rank the true
target1 geometry first. Follow the established target1 weak-control precedent
by running a 9-source Tx/Rx=60 rescue before closing this seed. No separate
numbered summary output folder was created for this decision.

Stage 13MA: seed139583862445 target1 9-source Tx/Rx=60 rescue.

Run 1115 is exact and accepted. The base margin is 5.084e-04, or
8.355e-06 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed139583862445 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 accepted at 5-source
Tx/Rx=60 with an early_high caveat, and target1 accepted by the 9-source
rescue. Continue the Fibonacci replication chain with seed225851433717 target0
after confirming the seed is accepted by the active NumPy random generator.

Stage 13MB: seed225851433717 target0 8-source Tx/Rx=60 control.

After the power interruption, the pre-existing run 1116 directory contained
only empty `data/` and `figures/` folders, so it was reused explicitly with
`--outdir`. Seed validation confirmed that
`np.random.default_rng(225851433717)` succeeds in the active FNO environment.
Run 1116 is exact and accepted. The base margin is 5.804e-04, or
8.039e-05 above cutoff, and all six diagnostic objectives rank the true
target0 geometry first. Late is weak at 4.655e-04 while late_high clears, so
carry the recurring target0 late-window caveat, but no target0 rescue is
justified. Continue seed225851433717 with target2 at the standard 5-source
Tx/Rx=60 control. No separate numbered summary output folder was created for
this decision.

Stage 13MC: seed225851433717 target2 5-source Tx/Rx=60 control.

Run 1117 is exact and accepted. The base margin is 5.302e-04, or
3.020e-05 above cutoff, and all six diagnostic objectives rank the true
target2 geometry first. Early_high is weak at 4.557e-04, so carry the usual
target2 early_high caveat, but no source-density rescue is justified because
the base rule passes. Continue seed225851433717 with target1 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13MD: seed225851433717 target1 5-source Tx/Rx=60 control.

Run 1118 is exact and accepted. The base margin is 5.489e-04, or
4.886e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed225851433717 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 accepted at 5-source
Tx/Rx=60 with an early_high caveat, and target1 accepted cleanly at 5-source
Tx/Rx=60. Continue the Fibonacci replication chain with seed365435296162
target0 after confirming the seed is accepted by the active NumPy random
generator.

Stage 13ME: scene visualization template and GSSI 51600S field-data intake plan.

Added `run_experiment_scene_visualization.py`, a reusable CPU-only scene/context
plotter that can read coordinate optimizer summaries or explicit geometry
lists. The coordinate optimizer now writes `system_scene_geometry.png` and
`system_scene_geometry_summary.json` automatically for future runs, and runs
1116-1118 were backfilled with the new figure plus figure-note sections. The
new GSSI 51600S data under `data/2026-06-09_GSSI_model_51600S` were inventoried
at the DZX/XML metadata level: files 013-015 have SIR4K DZX metadata with
512 samples/scan, 300 scans/m, 0.45 m display depth, and dielectric 2.25;
file 016 is missing its DZX sidecar. Keep the field-data branch gated behind a
CPU-only DZT import/QC stage and velocity calibration before using it for FWI
objective comparisons.

Stage 13MF: GSSI 51600S DZT import/QC and scene annotation refinement.

Installed `readgssi` 0.0.22 in the FNO environment and added
`run_gssi_dzt_qc.py`, a CPU-only importer/QC wrapper for the local GSSI DZT
profiles. Run 1119 imports four 51600S channel records: profiles 013 and 015
are about 2.7 m long, profiles 014 and 016 are about 0.91 m long, and profile
016 is the only missing-DZX case. The output writes raw and
median-background-removed B-scan figures, a field-profile QC context figure,
an inventory figure, CSV/JSON metadata, hashes, figure notes, and a manifest.
This is a field-data intake baseline only: the DZT profiles can support
profile-level QC, hyperbola/velocity picking, and later 2D/2.5D synthetic
comparison, but they do not make the current 2D solver a valid 3D FWI engine.
Also refined `run_experiment_scene_visualization.py` so cover arrows measure
bar-top cover and scene figures show an explicit Tx-Rx offset callout; runs
1115-1118 were regenerated with the improved annotation. Continue synthetic
replication at seed365435296162 target0 when returning to the GPU marathon,
while keeping measured-data inversion parked behind calibration and a 3D value
case.

Stage 13MG: seed365435296162 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(365435296162)` succeeds
in the active FNO environment. Run 1120 is exact but weak. The base margin is
4.624e-04, or 3.755e-05 below cutoff. Highband and veryhigh clear cutoff, but
late, late_high, and early_high are weak. All six diagnostic objectives rank
the true target0 geometry first, and the final state is exactly
`x=[150,250,350]`, `z=[80,100,120]`, `r=[5,6,8]` mm. Follow the recent
target0 weak-control policy from seeds701408733 and 7778742049 by running the
8-source Tx/Rx=52.5 acquisition probe before moving to target2. No separate
numbered summary output folder was created for this decision.

Stage 13MH: seed365435296162 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1121 is exact but still weak, although the acquisition probe substantially
improves the base margin from 4.624e-04 at Tx/Rx=60 to 4.943e-04 at
Tx/Rx=52.5. The remaining base deficit is only 5.719e-06 below cutoff.
Highband, veryhigh, and early_high clear cutoff; late and late_high remain
weak. All six diagnostic objectives rank the true target0 geometry first.
Because Tx/Rx=52.5 improved the row rather than worsening it, follow the
seed5702887 acquisition-bracket precedent and test the 8-source Tx/Rx=50 probe
before switching to source-density escalation. No separate numbered summary
output folder was created for this decision.

Stage 13MI: seed365435296162 target0 8-source Tx/Rx=50 acquisition bracket.

Run 1122 is exact and base-accepted. The base margin improves to 5.050e-04, or
4.956e-06 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, but all six diagnostic objectives rank the true
target0 geometry first. Because the accepted reserve is still small, follow
the seed5702887 lower-edge acquisition-bracket precedent by running one
8-source Tx/Rx=45 check before closing target0. No separate numbered summary
output folder was created for this decision.

Stage 13MJ: seed365435296162 target0 8-source Tx/Rx=45 lower-edge bracket.

Run 1123 is exact and accepted. The base margin improves to 5.282e-04, or
2.815e-05 above cutoff. Highband, late_high, veryhigh, and early_high clear
cutoff; only late remains weak at 4.580e-04. All six diagnostic objectives
rank the true target0 geometry first. Close seed365435296162 target0 at the
Tx/Rx=45 acquisition point with a residual late-window caveat, and continue the
seed with target2 at the standard 5-source Tx/Rx=60 control. No separate
numbered summary output folder was created for this decision.

Stage 13MK: seed365435296162 target2 5-source Tx/Rx=60 control.

Run 1124 is exact and accepted. The base margin is 6.158e-04, or 1.158e-04
above cutoff, and all six diagnostic objectives clear cutoff while ranking the
true target2 geometry first. No target2 rescue is justified. Continue
seed365435296162 with target1 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13ML: seed365435296162 target1 5-source Tx/Rx=60 control.

Run 1125 is exact and accepted. The base margin is 6.082e-04, or 1.082e-04
above cutoff, and all six diagnostic objectives clear cutoff while ranking the
true target1 geometry first. This closes seed365435296162 without a separate
numbered summary output folder: target0 accepted at 8-source Tx/Rx=45 with a
residual late-window caveat, target2 accepted cleanly at 5-source Tx/Rx=60, and
target1 accepted cleanly at 5-source Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(591286729879)` succeeds in the active FNO environment.
Continue the Fibonacci replication chain with seed591286729879 target0.

Stage 13MM: field experiment archive split and dataset-aware GSSI QC rerun.

Before launching the next GPU synthetic control, read `data/data_resarch.md`
and split measured/lab/public data outputs from the synthetic experiment
archive. The research note argues for a portfolio of data families rather than
one undifferentiated field-data stream: local GSSI 51600S, public lab rebar
datasets, public raw field `.dt` datasets, bridge-deck datasets, controlled
test-site radargrams, and synthetic FWI benchmarks have different parser,
geometry, label, and validation assumptions. Added `outputs/field_experiments/`
as the canonical measured/lab/public data root, with dataset-local numbering
under `outputs/field_experiments/<dataset_id>/NNN_run_name`.

Updated `run_gssi_dzt_qc.py` so its default output root is now
`outputs/field_experiments/local_gssi_51600s_2026_06_09/`, while preserving
`--outdir` as an exact override for historical backfills. Reran the local
GSSI 51600S import/QC into
`outputs/field_experiments/local_gssi_51600s_2026_06_09/001_gssi51600s_dzt_qc`.
The run imports the same four DZT channel records as historical run 1119:
profiles 013 and 015 are about 2.7 m, profiles 014 and 016 are about 0.91 m,
and profile 016 remains the missing-DZX case. This keeps `1119` as a
pre-split historical baseline and gives future field work a scalable archive
structure. Added `docs/field_experiments/` as the matching field-data tracker
root, with dataset-local tracker numbering mirroring the field output archive.
Continue seed591286729879 target0 after this documentation and validation
checkpoint.

Stage 13MN: seed591286729879 target0 8-source control.

Run 1126 is exact and accepted. The base margin is 5.491e-04, or
4.913e-05 above cutoff. Highband, veryhigh, and early_high clear cutoff;
late and late_high remain weak at 4.421e-04 and 4.585e-04, respectively.
All six diagnostic objectives rank the true target0 geometry first. This
matches prior accepted target0 controls where the base rule passed despite
late-window weakness, so no Tx/Rx acquisition probe is justified. Close
target0 with the recurring late-window caveat and continue seed591286729879
with target2 at the standard 5-source Tx/Rx=60 control. No separate numbered
summary output folder was created for this decision.

Stage 13MO: seed591286729879 target2 5-source Tx/Rx=60 control.

Run 1127 is exact and accepted. The base margin is 5.553e-04, or
5.530e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target2 geometry first. Early_high is the weakest diagnostic
at 5.039e-04, but it remains formally above cutoff. No target2 rescue is
justified. Continue seed591286729879 with target1 at the standard 5-source
Tx/Rx=60 control. No separate numbered summary output folder was created for
this decision.

Stage 13MP: seed591286729879 target1 5-source Tx/Rx=60 control.

Run 1128 is exact and accepted. The base margin is 5.931e-04, or
9.310e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed591286729879 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 accepted cleanly at
5-source Tx/Rx=60, and target1 accepted cleanly at 5-source Tx/Rx=60. Seed
validation confirmed that `np.random.default_rng(956722026041)` succeeds in
the active FNO environment. Continue the Fibonacci replication chain with
seed956722026041 target0.

Stage 13MQ: seed956722026041 target0 8-source Tx/Rx=60 control.

Run 1129 is exact and accepted. The base margin is 5.821e-04, or
8.212e-05 above cutoff, and all six diagnostic objectives rank the true
target0 geometry first. Late is weak at 4.546e-04 while late_high clears at
5.455e-04, so carry the recurring target0 late-window caveat, but no target0
rescue is justified. Continue seed956722026041 with target2 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13MR: seed956722026041 target2 5-source Tx/Rx=60 control.

Run 1130 is exact and accepted. The base margin is 5.322e-04, or
3.218e-05 above cutoff, and all six diagnostic objectives rank the true
target2 geometry first. Early_high is weak at 4.799e-04, so carry the usual
target2 early_high caveat, but no target2 rescue is justified because the
base rule passes and the diagnostic top candidates are exact. Continue
seed956722026041 with target1 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13MS: seed956722026041 target1 5-source Tx/Rx=60 control.

Run 1131 is exact and accepted. The base margin is 5.174e-04, or
1.736e-05 above cutoff, and all six diagnostic objectives rank the true
target1 geometry first. Early_high is weak at 4.789e-04, so carry an
early_high caveat, but no target1 rescue is justified because the base row
passes and the exact geometry is preserved across objectives. This closes
seed956722026041 without a separate numbered summary output folder: target0
accepted at 8-source Tx/Rx=60 with the recurring late-window caveat, target2
accepted at 5-source Tx/Rx=60 with an early_high caveat, and target1 accepted
at 5-source Tx/Rx=60 with an early_high caveat. Seed validation confirmed
that `np.random.default_rng(1548008755920)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with seed1548008755920
target0.

Stage 13MT: seed1548008755920 target0 8-source Tx/Rx=60 control.

Run 1132 is exact and accepted. The base margin is 5.515e-04, or
5.149e-05 above cutoff, and all six diagnostic objectives rank the true
target0 geometry first. Late is weak at 4.451e-04 while late_high clears at
5.366e-04, so carry the recurring target0 late-window caveat, but no target0
rescue is justified. Continue seed1548008755920 with target2 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13MU: seed1548008755920 target2 5-source Tx/Rx=60 control.

Run 1133 is exact but weak. The base margin is 4.738e-04, or
2.617e-05 below cutoff, and early_high is also weak at 4.222e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six diagnostic objectives
rank the true target2 geometry first. Follow the target2 weak-control policy
with a 7-source Tx/Rx=60 source-density bracket before considering 9 sources.
No separate numbered summary output folder was created for this decision.

Stage 13MV: seed1548008755920 target2 7-source Tx/Rx=60 bracket.

Run 1134 is exact and accepted, but with a razor-thin base reserve. The base
margin is 5.016e-04, only 1.588e-06 above cutoff, and early_high remains weak
at 4.025e-04. Highband, late, late_high, and veryhigh clear cutoff, and all
six diagnostic objectives rank the true target2 geometry first. Accept this
as the target2 rescue by the existing 7-source policy, but carry both caveats:
base reserve is extremely small and early_high is weak. Do not run an
immediate 9-source cleanup because the base row clears and the precedent is to
move to target1 once a source-density bracket accepts. Continue
seed1548008755920 with target1 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13MW: seed1548008755920 target1 5-source Tx/Rx=60 control.

Run 1135 is exact and accepted cleanly. The base margin is 6.623e-04, or
1.623e-04 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed1548008755920 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 accepted by the
7-source Tx/Rx=60 bracket with a razor-thin base reserve and early_high caveat,
and target1 accepted cleanly at 5-source Tx/Rx=60. Seed validation confirmed
that `np.random.default_rng(2504730781961)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with seed2504730781961
target0.

Stage 13MX: seed2504730781961 target0 8-source Tx/Rx=60 control.

Run 1136 selected the exact target0 geometry, but it is weak. The base margin
is 3.873e-04, or 1.127e-04 below cutoff, and every diagnostic objective also
falls below cutoff: highband 4.953e-04, late 2.736e-04, late_high 3.255e-04,
veryhigh 4.694e-04, and early_high 4.134e-04. All six diagnostic objectives
still rank the true target0 geometry first, so this is a radius-confidence
weakness rather than a location failure. Follow the target0 weak-control policy
with an 8-source Tx/Rx=52.5 mm acquisition probe. No separate numbered summary
output folder was created for this decision.

Stage 13MY: seed2504730781961 target0 8-source Tx/Rx=52.5 probe.

Run 1137 selected the exact target0 geometry but remained weak. The base
margin improved from 3.873e-04 at Tx/Rx=60 to 4.324e-04 at Tx/Rx=52.5, still
6.756e-05 below cutoff. Highband and veryhigh now clear cutoff at 5.653e-04
and 5.336e-04, respectively, while late, late_high, and early_high remain
weak. All six diagnostic objectives rank the true target0 geometry first.
Continue the spacing ladder with an 8-source Tx/Rx=50 mm probe before
considering source-density rescue. No separate numbered summary output folder
was created for this decision.

Stage 13MZ: seed2504730781961 target0 8-source Tx/Rx=50 probe.

Run 1138 selected the exact target0 geometry but remained weak. The base
margin improved only modestly from 4.324e-04 at Tx/Rx=52.5 to 4.477e-04 at
Tx/Rx=50, still 5.229e-05 below cutoff. Highband and veryhigh remain above
cutoff, while late, late_high, and early_high remain weak. All six diagnostic
objectives rank the true target0 geometry first. The spacing trend is
monotone but flattening; follow the seed5702887 target0 precedent with one
lower-edge 8-source Tx/Rx=45 mm bracket, then escalate source density if that
does not clear the base rule. No separate numbered summary output folder was
created for this decision.

Stage 13NA: seed2504730781961 target0 8-source Tx/Rx=45 lower-edge bracket.

Run 1139 selected the exact target0 geometry and produced the strongest
spacing result for this seed, but still missed the base cutoff. The base
margin is 4.843e-04, or 1.574e-05 below cutoff. Highband, veryhigh, and
early_high clear cutoff while late and late_high remain weak; all six
diagnostic objectives rank the true target0 geometry first. Since the
predeclared lower-edge spacing bracket did not pass, stop the simple spacing
ladder. Switch mechanism to a standard 9-source Tx/Rx=60 source-density
bracket so the source-count effect is measured against the canonical
acquisition spacing before trying any combined rescue. No separate numbered
summary output folder was created for this decision.

Stage 13NB: seed2504730781961 target0 9-source Tx/Rx=60 source-density bracket.

Run 1140 rescues target0. The final geometry is exact and the base margin is
5.296e-04, or 2.965e-05 above cutoff. The 9-source Tx/Rx=60 row improves over
both the original 8-source Tx/Rx=60 control and the best 8-source spacing row
at Tx/Rx=45. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain weak, so carry the recurring target0 late-window caveat. No
11-source cleanup is justified because the base rule passes and all objective
variants rank the true geometry first. Continue seed2504730781961 with target2
at the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13NC: seed2504730781961 target2 5-source Tx/Rx=60 control.

Run 1141 is exact and accepted. The base margin is 5.507e-04, or 5.070e-05
above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high is weak at 4.801e-04. All six diagnostic objectives rank the true
target2 geometry first, so no target2 source-density rescue is justified.
Continue seed2504730781961 with target1 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

Stage 13ND: seed2504730781961 target1 5-source Tx/Rx=60 control.

Run 1142 is exact and accepted. The base margin is 5.174e-04, or 1.736e-05
above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high is weak at 4.710e-04. All six diagnostic objectives rank the true
target1 geometry first. This closes seed2504730781961 without a separate
numbered summary output folder: target0 accepted by a 9-source Tx/Rx=60
source-density rescue with a late-window caveat, target2 accepted at 5-source
Tx/Rx=60 with an early_high caveat, and target1 accepted at 5-source Tx/Rx=60
with an early_high caveat. Seed validation confirmed that
`np.random.default_rng(4052739547881)` succeeds in the active FNO environment.
Continue the Fibonacci replication chain with seed4052739547881 target0.

Stage 13NE: seed4052739547881 target0 8-source Tx/Rx=60 control.

Run 1143 is exact and accepted. The base margin is 5.456e-04, or 4.560e-05
above cutoff. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain weak, so carry the recurring target0 late-window caveat. All
six diagnostic objectives rank the true target0 geometry first, so no rescue
branch is justified. Continue seed4052739547881 with target2 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13NF: seed4052739547881 target2 5-source Tx/Rx=60 control.

Run 1144 is exact and accepted cleanly. The base margin is 6.343e-04, or
1.343e-04 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target2 geometry first. No target2 rescue is justified.
Continue seed4052739547881 with target1 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

Stage 13NG: seed4052739547881 target1 5-source Tx/Rx=60 control.

Run 1145 is exact and accepted cleanly. The base margin is 5.236e-04, or
2.364e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed4052739547881 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 accepted cleanly at
5-source Tx/Rx=60, and target1 accepted cleanly at 5-source Tx/Rx=60. Seed
validation confirmed that `np.random.default_rng(6557470329842)` succeeds in
the active FNO environment. Continue the Fibonacci replication chain with
seed6557470329842 target0.

Stage 13NH: seed6557470329842 target0 8-source Tx/Rx=60 control.

Run 1146 is exact and accepted cleanly. The base margin is 5.921e-04, or
9.209e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target0 geometry first. Unlike many target0 rows, late and
late_high also clear cutoff, so no target0 caveat is needed. Continue
seed6557470329842 with target2 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13NI: seed6557470329842 target2 5-source Tx/Rx=60 control.

Run 1147 is exact and accepted, but the base reserve is razor-thin. The base
margin is 5.065e-04, only 6.508e-06 above cutoff. Highband, late, late_high,
and veryhigh clear cutoff, while early_high is weak at 4.472e-04. All six
diagnostic objectives rank the true target2 geometry first, so no source-
density rescue is justified. Carry the razor-thin base reserve and early_high
caveats, then continue seed6557470329842 with target1 at the standard 5-source
Tx/Rx=60 control. No separate numbered summary output folder was created for
this decision.

Stage 13NJ: seed6557470329842 target1 5-source Tx/Rx=60 control.

Run 1148 is exact and accepted. The base margin is 5.203e-04, or 2.029e-05
above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high is weak at 4.784e-04. All six diagnostic objectives rank the true
target1 geometry first. This closes seed6557470329842 without a separate
numbered summary output folder: target0 accepted cleanly at 8-source Tx/Rx=60,
target2 accepted at 5-source Tx/Rx=60 with a razor-thin base reserve and
early_high caveat, and target1 accepted at 5-source Tx/Rx=60 with an
early_high caveat. Seed validation confirmed that
`np.random.default_rng(10610209877723)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with seed10610209877723
target0.

Stage 13NK: seed10610209877723 target0 8-source Tx/Rx=60 control.

Run 1149 is exact and accepted. The base margin is 5.295e-04, or 2.946e-05
above cutoff. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain weak, so carry the recurring target0 late-window caveat. All
six diagnostic objectives rank the true target0 geometry first, so no rescue
branch is justified. Continue seed10610209877723 with target2 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13NL: seed10610209877723 target2 5-source Tx/Rx=60 control.

Run 1150 is exact but weak. The base margin is 4.719e-04, or 2.814e-05 below
cutoff, and early_high is weak at 3.987e-04. Highband, late, late_high, and
veryhigh clear cutoff, and all six diagnostic objectives rank the true target2
geometry first. Follow the recent target2 weak-control policy with a 7-source
Tx/Rx=60 source-density bracket before considering 9 sources. No separate
numbered summary output folder was created for this decision.

Stage 13NM: seed10610209877723 target2 7-source Tx/Rx=60 source-density bracket.

Run 1151 is exact but still weak. The base margin is 4.449e-04, or
5.508e-05 below cutoff, which is weaker than the 5-source control. Early_high
also remains weak at 3.656e-04. Highband, late, late_high, and veryhigh clear
cutoff, and all six diagnostic objectives rank the true target2 geometry
first. Since 9 sources is the accepted target2 source-density level in recent
branches, continue to a 9-source Tx/Rx=60 escalation before deciding whether
target2 is unresolved. No separate numbered summary output folder was created
for this decision.

Stage 13NN: seed10610209877723 target2 9-source Tx/Rx=60 escalation.

Run 1152 is exact and a target2 near miss. The base margin improves to
4.831e-04, or 1.686e-05 below cutoff. Highband, late, late_high, and veryhigh
clear cutoff, while early_high remains weak at 4.469e-04. All six diagnostic
objectives rank the true target2 geometry first. Follow the recent target2
near-miss precedent by running one 11-source Tx/Rx=60 closeout test before
declaring the simple source-density ladder unresolved. No separate numbered
summary output folder was created for this decision.

Stage 13NO: seed10610209877723 target2 11-source Tx/Rx=60 source-density closeout.

Run 1153 is exact but remains a weak-base result. The base margin is
4.076e-04, or 9.237e-05 below cutoff. Highband, late, late_high, and veryhigh
clear cutoff, while early_high is weak at 3.831e-04. All six diagnostic
objectives rank the true target2 geometry first, so the source-density ladder
preserves the true radius/depth across 5, 7, 9, and 11 sources even though it
does not yield moderate base confidence. Close this branch as a
truth-preserving weak-margin target2 case; a future revisit should change
aperture geometry, objective weighting, or interval reporting rather than
adding more simple source density. Continue seed10610209877723 with target1 at
the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13NP: seed10610209877723 target1 5-source Tx/Rx=60 control.

Run 1154 is exact and accepted cleanly. The base margin is 5.239e-04, or
2.387e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed10610209877723 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 preserved the true
geometry across 5/7/9/11 sources but remained weak-base, and target1 accepted
cleanly at 5-source Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(17167680207565)` succeeds in the active FNO environment.
Continue the Fibonacci replication chain with seed17167680207565 target0.

Stage 13NQ: seed17167680207565 target0 8-source Tx/Rx=60 control.

Run 1155 is exact and accepted. The base margin is 5.456e-04, or 4.555e-05
above cutoff. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain weak, so carry the recurring target0 late-window caveat. All
six diagnostic objectives rank the true target0 geometry first, so no rescue
branch is justified. Continue seed17167680207565 with target2 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13NR: seed17167680207565 target2 5-source Tx/Rx=60 control.

Run 1156 is exact but weak. The base margin is 4.571e-04, or 4.290e-05 below
cutoff, and early_high is weak at 4.574e-04. Highband, late, late_high, and
veryhigh clear cutoff, and all six diagnostic objectives rank the true target2
geometry first. Follow the current target2 weak-control policy with a 7-source
Tx/Rx=60 source-density bracket before considering 9 sources. No separate
numbered summary output folder was created for this decision.

Stage 13NS: seed17167680207565 target2 7-source Tx/Rx=60 source-density bracket.

Run 1157 is exact but still weak. The base margin is 4.380e-04, or
6.198e-05 below cutoff, which is weaker than the 5-source control. Early_high
also remains weak at 3.866e-04. Highband, late, late_high, and veryhigh clear
cutoff, and all six diagnostic objectives rank the true target2 geometry
first. Continue to the standard 9-source Tx/Rx=60 target2 escalation. No
separate numbered summary output folder was created for this decision.

Stage 13NT: seed17167680207565 target2 9-source Tx/Rx=60 escalation.

Run 1158 is exact and accepted cleanly. The base margin is 5.574e-04, or
5.740e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target2 geometry first. This 9-source run rescues the weak
5- and 7-source target2 controls, so no 11-source closeout is justified.
Continue seed17167680207565 with target1 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

Stage 13NU: seed17167680207565 target1 5-source Tx/Rx=60 control.

Run 1159 is exact but weak. The base margin is 4.758e-04, or 2.415e-05 below
cutoff, and early_high is weak at 4.441e-04. Highband, late, late_high, and
veryhigh clear cutoff, and all six diagnostic objectives rank the true target1
geometry first. Follow the current target1 weak-control precedent with a
9-source Tx/Rx=60 rescue before closing this seed. No separate numbered
summary output folder was created for this decision.

Stage 13NV: seed17167680207565 target1 9-source Tx/Rx=60 rescue.

Run 1160 is exact and accepted cleanly. The base margin is 5.549e-04, or
5.494e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed17167680207565 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 accepted by a clean
9-source rescue after weak 5/7-source controls, and target1 accepted by a
clean 9-source rescue after a weak 5-source control. Seed validation confirmed
that `np.random.default_rng(27777890085288)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with seed27777890085288
target0.

Stage 13NW: seed27777890085288 target0 8-source Tx/Rx=60 control.

Run 1161 is exact and accepted. The base margin is 5.579e-04, or 5.788e-05
above cutoff. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain weak, so carry the recurring target0 late-window caveat. All
six diagnostic objectives rank the true target0 geometry first, so no rescue
branch is justified. Continue seed27777890085288 with target2 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13NX: seed27777890085288 target2 5-source Tx/Rx=60 control.

Run 1162 is exact but weak by a razor-thin margin. The base margin is
4.980e-04, only 1.957e-06 below cutoff, and early_high is weak at 4.722e-04.
Highband, late, late_high, and veryhigh clear cutoff, and all six diagnostic
objectives rank the true target2 geometry first. Treat this as a near-miss
target2 weak control and run the standard 7-source Tx/Rx=60 source-density
bracket before accepting or escalating further. No separate numbered summary
output folder was created for this decision.

Stage 13NY: seed27777890085288 target2 7-source Tx/Rx=60 source-density bracket.

Run 1163 is exact but still weak. The base margin is 4.867e-04, or
1.328e-05 below cutoff, and early_high is weak at 4.103e-04. Highband, late,
late_high, and veryhigh clear cutoff, and all six diagnostic objectives rank
the true target2 geometry first. Continue to the standard 9-source Tx/Rx=60
target2 escalation. No separate numbered summary output folder was created for
this decision.

Stage 13NZ: seed27777890085288 target2 9-source Tx/Rx=60 escalation.

Run 1164 is exact and accepted. The base margin is 5.354e-04, or 3.544e-05
above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high is weak at 4.946e-04. All six diagnostic objectives rank the true
target2 geometry first. This 9-source run rescues the near-miss 5-source and
weak 7-source target2 controls, so no 11-source closeout is justified. Continue
seed27777890085288 with target1 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13OA: seed27777890085288 target1 5-source Tx/Rx=60 control.

Run 1165 is exact and accepted cleanly. The base margin is 6.080e-04, or
1.080e-04 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed27777890085288 without
a separate numbered summary output folder: target0 accepted at 8-source
Tx/Rx=60 with the recurring late-window caveat, target2 accepted by a 9-source
rescue after a near-miss 5-source control and weak 7-source bracket, and
target1 accepted cleanly at 5-source Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(44945570292853)` succeeds in the active FNO environment.
Continue the Fibonacci replication chain with seed44945570292853 target0.

Stage 13OB: seed44945570292853 target0 8-source Tx/Rx=60 control.

Run 1166 is exact but weak by a small margin. The base margin is 4.946e-04,
or 5.429e-06 below cutoff. Highband, veryhigh, and early_high clear cutoff;
late and late_high are weak. All six diagnostic objectives rank the true
target0 geometry first, so this is a radius-confidence weakness rather than a
geometry failure. Follow the target0 weak-control policy with an 8-source
Tx/Rx=52.5 mm acquisition probe before deciding whether tighter spacing or a
9-source Tx/Rx=60 source-density bracket is justified. No separate numbered
summary output folder was created for this decision.

Stage 13OC: seed44945570292853 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1167 is exact and accepted. The base margin is 5.400e-04, or
4.000e-05 above cutoff. Highband, veryhigh, and early_high clear cutoff;
late and late_high remain weak, so keep the recurring target0 late-window
caveat. All six diagnostic objectives rank the true target0 geometry first.
This Tx/Rx=52.5 acquisition probe rescues the near-miss 8-source Tx/Rx=60
control, so no further target0 rescue is justified for this seed. Continue
seed44945570292853 with target2 at the standard 5-source Tx/Rx=60 control. No
separate numbered summary output folder was created for this decision.

Stage 13OD: seed44945570292853 target2 5-source Tx/Rx=60 control.

Run 1168 is exact and accepted. The base margin is 5.391e-04, or
3.912e-05 above cutoff. Base, highband, late, late_high, and veryhigh clear
cutoff; early_high remains weak at 4.423e-04. All six diagnostic objectives
rank the true target2 geometry first. Treat this as an accepted target2
control with an isolated early-window caveat rather than a rescue case.
Continue seed44945570292853 with target1 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

Stage 13OE: seed44945570292853 target1 5-source Tx/Rx=60 control.

Run 1169 is exact and accepted cleanly. The base margin is 6.176e-04, or
1.176e-04 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed44945570292853
without a separate numbered summary output folder: target0 accepted after the
Tx/Rx=52.5 acquisition probe rescued the near-miss Tx/Rx=60 control, target2
accepted at 5-source Tx/Rx=60 with only an isolated early_high caveat, and
target1 accepted cleanly at 5-source Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(72723460378141)` succeeds in the active FNO environment.
Continue the Fibonacci replication chain with seed72723460378141 target0.

Stage 13OF: seed72723460378141 target0 8-source Tx/Rx=60 control.

Run 1170 is exact and accepted. The base margin is 5.212e-04, or
2.119e-05 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first, so no
target0 rescue branch is justified. Continue seed72723460378141 with target2
at the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13OG: seed72723460378141 target2 5-source Tx/Rx=60 control.

Run 1171 is exact and accepted by a thin margin. The base margin is 5.057e-04,
only 5.681e-06 above cutoff. Highband, late, late_high, and veryhigh clear
cutoff; early_high is weak at 4.751e-04. All six diagnostic objectives rank
the true target2 geometry first. Treat this as a near-threshold accepted
target2 control with an early-window caveat, not a source-density rescue case.
Continue seed72723460378141 with target1 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

Stage 13OH: seed72723460378141 target1 5-source Tx/Rx=60 control.

Run 1172 is exact but weak. The base margin is 4.343e-04, or 6.569e-05 below
cutoff, and early_high is weak at 4.350e-04. Highband, late, late_high, and
veryhigh clear cutoff, and all six diagnostic objectives rank the true target1
geometry first. Follow the current target1 weak-control precedent with a
9-source Tx/Rx=60 rescue before closing this seed. No separate numbered
summary output folder was created for this decision.

Stage 13OI: seed72723460378141 target1 9-source Tx/Rx=60 rescue.

Run 1173 is exact and accepted cleanly. The base margin is 5.446e-04, or
4.461e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed72723460378141
without a separate numbered summary output folder: target0 accepted at
8-source Tx/Rx=60 with the recurring late-window caveat, target2 accepted at
5-source Tx/Rx=60 by a thin margin with an early_high caveat, and target1
accepted cleanly after the 9-source rescue. Seed validation confirmed that
`np.random.default_rng(117669030670994)` succeeds in the active FNO environment.
Continue the Fibonacci replication chain with seed117669030670994 target0.

Stage 13OJ: seed117669030670994 target0 8-source Tx/Rx=60 control.

Run 1174 is exact and accepted. The base margin is 5.365e-04, or
3.651e-05 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first, so no
target0 rescue branch is justified. Continue seed117669030670994 with target2
at the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13OK: seed117669030670994 target2 5-source Tx/Rx=60 control.

Run 1175 is exact but weak by a small margin. The base margin is 4.937e-04,
or 6.266e-06 below cutoff, and early_high is weak at 4.108e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six diagnostic objectives
rank the true target2 geometry first. Treat this as a near-miss target2 weak
control and run the standard 7-source Tx/Rx=60 source-density bracket before
accepting or escalating further. No separate numbered summary output folder
was created for this decision.

Stage 13OL: seed117669030670994 target2 7-source Tx/Rx=60 source-density bracket.

Run 1176 is exact and accepted by a thin margin. The base margin is 5.037e-04,
only 3.657e-06 above cutoff. Highband, late, late_high, and veryhigh clear
cutoff; early_high is weak at 4.363e-04. All six diagnostic objectives rank
the true target2 geometry first. Treat this as a near-threshold accepted
7-source bracket with an early-window caveat, not an immediate 9-source
escalation. Continue seed117669030670994 with target1 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13OM: seed117669030670994 target1 5-source Tx/Rx=60 control.

Run 1177 is exact and accepted cleanly. The base margin is 5.748e-04, or
7.478e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed117669030670994
without a separate numbered summary output folder: target0 accepted at
8-source Tx/Rx=60 with the recurring late-window caveat, target2 accepted
after a near-threshold 7-source bracket with an early_high caveat, and target1
accepted cleanly at 5-source Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(190392491049135)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with seed190392491049135
target0.

Stage 13ON: seed190392491049135 target0 8-source Tx/Rx=60 control.

Run 1178 is exact but weak by an almost zero margin. The base margin is
4.999701e-04, only 2.991e-08 below cutoff. Highband, veryhigh, and early_high
clear cutoff; base, late, and late_high are weak. All six diagnostic
objectives rank the true target0 geometry first, so this is a radius-confidence
weakness rather than a geometry failure. Follow the target0 weak-control policy
with an 8-source Tx/Rx=52.5 mm acquisition probe before deciding whether any
further rescue is justified. No separate numbered summary output folder was
created for this decision.

Stage 13OO: seed190392491049135 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1179 is exact and accepted. The base margin is 5.126e-04, or
1.258e-05 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first. This
Tx/Rx=52.5 acquisition probe rescues the near-zero miss at Tx/Rx=60, so no
further target0 rescue is justified for this seed. Continue
seed190392491049135 with target2 at the standard 5-source Tx/Rx=60 control.
No separate numbered summary output folder was created for this decision.

Stage 13OP: seed190392491049135 target2 5-source Tx/Rx=60 control.

Run 1180 is exact and accepted. The base margin is 5.083e-04, or
8.330e-06 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target2 geometry first. Continue seed190392491049135 with
target1 at the standard 5-source Tx/Rx=60 control. No separate numbered
summary output folder was created for this decision.

Stage 13OQ: seed190392491049135 target1 5-source Tx/Rx=60 control.

Run 1181 is exact and accepted cleanly. The base margin is 5.328e-04, or
3.279e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed190392491049135
without a separate numbered summary output folder: target0 accepted after a
Tx/Rx=52.5 acquisition probe rescued the near-zero Tx/Rx=60 miss, target2
accepted cleanly at 5-source Tx/Rx=60, and target1 accepted at 5-source
Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(308061521720129)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with seed308061521720129
target0.

Stage 13OR: seed308061521720129 target0 8-source Tx/Rx=60 control.

Run 1182 is exact but weak. The base margin is 4.679e-04, or 3.208e-05 below
cutoff. Highband, veryhigh, and early_high clear cutoff; base, late, and
late_high are weak. All six diagnostic objectives rank the true target0
geometry first, so this is a radius-confidence weakness rather than a geometry
failure. Follow the target0 weak-control policy with an 8-source Tx/Rx=52.5 mm
acquisition probe. No separate numbered summary output folder was created for
this decision.

Stage 13OS: seed308061521720129 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1183 is exact and accepted. The base margin is 5.081e-04, or
8.141e-06 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first. This
Tx/Rx=52.5 acquisition probe rescues the weak Tx/Rx=60 target0 control, so no
further target0 rescue is justified for this seed. Continue
seed308061521720129 with target2 at the standard 5-source Tx/Rx=60 control.
No separate numbered summary output folder was created for this decision.

Stage 13OT: seed308061521720129 target2 5-source Tx/Rx=60 control.

Run 1184 is exact but weak by a small margin. The base margin is 4.909e-04,
or 9.117e-06 below cutoff, and early_high is weak at 4.250e-04. Highband,
late, late_high, and veryhigh clear cutoff, and all six diagnostic objectives
rank the true target2 geometry first. Treat this as a near-miss target2 weak
control and run the standard 7-source Tx/Rx=60 source-density bracket before
accepting or escalating further. No separate numbered summary output folder
was created for this decision.

Stage 13OU: seed308061521720129 target2 7-source Tx/Rx=60 source-density bracket.

Run 1185 is exact but remains weak. The base margin is 4.509e-04, or
4.913e-05 below cutoff, and early_high is weak at 3.922e-04. Highband, late,
late_high, and veryhigh clear cutoff, and all six diagnostic objectives rank
the true target2 geometry first. The 7-source bracket did not rescue target2
point-radius confidence and worsened the base gap relative to the 5-source
control. Escalate once to a 9-source Tx/Rx=60 bracket before deciding whether
this seed's target2 should be carried as an interval/weak point-radius result.
No separate numbered summary output folder was created for this decision.

Stage 13OV: seed308061521720129 target2 9-source Tx/Rx=60 source-density escalation.

Run 1186 is exact but remains weak. The base margin is 4.444e-04, or
5.564e-05 below cutoff, and early_high is weak at 4.161e-04. Highband, late,
late_high, and veryhigh clear cutoff, and all six diagnostic objectives rank
the true target2 geometry first. The 9-source escalation does not rescue the
point-radius confidence; across the 5-, 7-, and 9-source target2 probes, base
margins stay below cutoff (`4.91e-04`, `4.51e-04`, `4.44e-04`). Carry target2
as exact geometry with weak point-radius confidence and continue to target1 at
the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13OW: seed308061521720129 target1 5-source Tx/Rx=60 control.

Run 1187 is exact and accepted cleanly. The base margin is 6.214e-04, or
1.214e-04 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed308061521720129:
target0 accepted after a Tx/Rx=52.5 acquisition rescue, target2 carried as
exact geometry with weak point-radius confidence after 5-, 7-, and 9-source
probes, and target1 accepted cleanly at 5-source Tx/Rx=60. Seed validation
confirmed that `np.random.default_rng(498454012769264)` succeeds in the active
FNO environment. Continue the Fibonacci replication chain with
seed498454012769264 target0. No separate numbered summary output folder was
created for this decision.

Stage 13OX: seed498454012769264 target0 8-source Tx/Rx=60 control.

Run 1188 is exact but weak. The base margin is 4.689e-04, or 3.105e-05 below
cutoff. Highband, late_high, and veryhigh clear cutoff; base, late, and
early_high are weak. All six diagnostic objectives rank the true target0
geometry first, so this is a radius-confidence weakness rather than a geometry
failure. Follow the target0 weak-control policy with an 8-source Tx/Rx=52.5 mm
acquisition probe. No separate numbered summary output folder was created for
this decision.

Stage 13OY: seed498454012769264 target0 8-source Tx/Rx=52.5 acquisition probe.

Run 1189 is exact and accepted. The base margin is 5.271e-04, or
2.707e-05 above cutoff. Highband, late_high, veryhigh, and early_high clear
cutoff; late remains weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first. This
Tx/Rx=52.5 acquisition probe rescues the weak Tx/Rx=60 target0 control, so no
further target0 rescue is justified for this seed. Continue
seed498454012769264 with target2 at the standard 5-source Tx/Rx=60 control.
No separate numbered summary output folder was created for this decision.

Stage 13OZ: seed498454012769264 target2 5-source Tx/Rx=60 control.

Run 1190 is exact and formally accepted by the reporting cutoff, but only by
5.813e-08. The base margin is 5.001e-04, early_high is weak at 3.984e-04, and
the other four objective variants clear cutoff while ranking the true target2
geometry first. Treat this as a practical near-zero target2 control rather than
a robust acceptance. Run the standard 7-source Tx/Rx=60 source-density bracket
before deciding whether to accept with caveats or escalate further. No separate
numbered summary output folder was created for this decision.

Stage 13PA: seed498454012769264 target2 7-source Tx/Rx=60 source-density bracket.

Run 1191 is exact but weak. The base margin is 4.325e-04, or 6.754e-05 below
cutoff, and early_high is weak at 3.753e-04. Highband, late, late_high, and
veryhigh clear cutoff, and all six diagnostic objectives rank the true target2
geometry first. The 7-source bracket worsened the base gap relative to the
practical near-zero 5-source control. Escalate once to a 9-source Tx/Rx=60
bracket before deciding whether this seed's target2 should be carried as exact
geometry with weak point-radius confidence. No separate numbered summary
output folder was created for this decision.

Stage 13PB: seed498454012769264 target2 9-source Tx/Rx=60 source-density escalation.

Run 1192 is exact and accepted. The base margin is 5.422e-04, or
4.223e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target2 geometry first. This 9-source escalation rescues the
target2 branch after the practical near-zero 5-source control and weak
7-source bracket. Continue seed498454012769264 with target1 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13PC: seed498454012769264 target1 5-source Tx/Rx=60 control.

Run 1193 is exact and accepted cleanly. The base margin is 5.913e-04, or
9.126e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed498454012769264:
target0 accepted after a Tx/Rx=52.5 acquisition rescue, target2 accepted after
a 9-source rescue, and target1 accepted cleanly at 5-source Tx/Rx=60. Seed
validation confirmed that `np.random.default_rng(806515534489393)` succeeds in
the active FNO environment. Continue the Fibonacci replication chain with
seed806515534489393 target0. No separate numbered summary output folder was
created for this decision.

Stage 13PD: seed806515534489393 target0 8-source Tx/Rx=60 control.

Run 1194 is exact and accepted. The base margin is 5.088e-04, or
8.826e-06 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first, so no
target0 rescue branch is justified. Continue seed806515534489393 with target2
at the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13PE: seed806515534489393 target2 5-source Tx/Rx=60 control.

Run 1195 is exact but weak. The base margin is 4.626e-04, or 3.737e-05 below
cutoff, and early_high is weak at 4.161e-04. Highband, late, late_high, and
veryhigh clear cutoff, and all six diagnostic objectives rank the true target2
geometry first. Treat this as a target2 radius-confidence weakness and run the
standard 7-source Tx/Rx=60 source-density bracket. No separate numbered
summary output folder was created for this decision.

Stage 13PF: seed806515534489393 target2 7-source Tx/Rx=60 source-density bracket.

Run 1196 is exact but remains weak. The base margin is 4.151e-04, or
8.492e-05 below cutoff, and early_high is weak at 3.456e-04. Highband, late,
late_high, and veryhigh clear cutoff, and all six diagnostic objectives rank
the true target2 geometry first. The 7-source bracket worsens the base margin
relative to the 5-source control, so escalate once to a 9-source Tx/Rx=60
bracket before deciding whether target2 should be carried as exact geometry
with weak point-radius confidence. No separate numbered summary output folder
was created for this decision.

Stage 13PG: seed806515534489393 target2 9-source Tx/Rx=60 source-density escalation.

Run 1197 is exact and accepted. The base margin is 5.192e-04, or
1.917e-05 above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high remains weak at 4.841e-04, so carry an early-window caveat. All six
diagnostic objectives rank the true target2 geometry first. This 9-source
escalation rescues target2 after weak 5- and 7-source runs. Continue
seed806515534489393 with target1 at the standard 5-source Tx/Rx=60 control.
No separate numbered summary output folder was created for this decision.

Stage 13PH: seed806515534489393 target1 5-source Tx/Rx=60 control.

Run 1198 is exact and accepted cleanly. The base margin is 5.956e-04, or
9.562e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed806515534489393:
target0 accepted at 8-source Tx/Rx=60 with the recurring late-window caveat,
target2 accepted after a 9-source rescue with an early_high caveat, and target1
accepted cleanly at 5-source Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(1304969547258657)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with
seed1304969547258657 target0. No separate numbered summary output folder was
created for this decision.

Stage 13PI: seed1304969547258657 target0 8-source Tx/Rx=60 control.

Run 1199 is exact and accepted. The base margin is 5.511e-04, or
5.112e-05 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first, so no
target0 rescue branch is justified. Continue seed1304969547258657 with target2
at the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13PJ: seed1304969547258657 target2 5-source Tx/Rx=60 control.

Run 1200 is exact and accepted. The base margin is 5.649e-04, or
6.488e-05 above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high is weak at 4.971e-04, so carry an early-window caveat. All six
diagnostic objectives rank the true target2 geometry first. Continue
seed1304969547258657 with target1 at the standard 5-source Tx/Rx=60 control.
No separate numbered summary output folder was created for this decision.

Stage 13PK: seed1304969547258657 target1 5-source Tx/Rx=60 control.

Run 1201 is exact and accepted cleanly. The base margin is 5.588e-04, or
5.876e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed1304969547258657:
target0 accepted at 8-source Tx/Rx=60 with the recurring late-window caveat,
target2 accepted at 5-source Tx/Rx=60 with an early_high caveat, and target1
accepted cleanly at 5-source Tx/Rx=60. Seed validation confirmed that
`np.random.default_rng(2111485081748050)` succeeds in the active FNO
environment. Continue the Fibonacci replication chain with
seed2111485081748050 target0. No separate numbered summary output folder was
created for this decision.

Stage 13PL: seed2111485081748050 target0 8-source Tx/Rx=60 control.

Run 1202 is exact and accepted. The base margin is 5.423e-04, or
4.228e-05 above cutoff. Highband, veryhigh, and early_high clear cutoff; late
and late_high remain weak, so carry the recurring target0 late-window caveat.
All six diagnostic objectives rank the true target0 geometry first, so no
target0 rescue branch is justified. Continue seed2111485081748050 with target2
at the standard 5-source Tx/Rx=60 control. No separate numbered summary output
folder was created for this decision.

Stage 13PM: seed2111485081748050 target2 5-source Tx/Rx=60 control.

Run 1203 is exact but weak by a very small margin. The base margin is
4.994e-04, or 6.147e-07 below cutoff, and early_high is weak at 4.491e-04.
Highband, late, late_high, and veryhigh clear cutoff, and all six diagnostic
objectives rank the true target2 geometry first. Treat this as a near-miss
target2 weak control and run the standard 7-source Tx/Rx=60 source-density
bracket before accepting or escalating further. No separate numbered summary
output folder was created for this decision.

Stage 13PN: seed2111485081748050 target2 7-source Tx/Rx=60 source-density bracket.

Run 1204 is exact and accepted. The base margin is 5.313e-04, or
3.126e-05 above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high remains weak at 4.419e-04, so carry the target2 early-window
caveat. All six diagnostic objectives rank the true target2 geometry first,
and the 7-source bracket rescues the near-miss 5-source control without a
9-source escalation. Continue seed2111485081748050 with target1 at the standard
5-source Tx/Rx=60 control. No separate numbered summary output folder was
created for this decision.

Stage 13PO: seed2111485081748050 target1 5-source Tx/Rx=60 control.

Run 1205 is exact and accepted cleanly. The base margin is 6.224e-04, or
1.224e-04 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed2111485081748050:
target0 accepted at 8-source Tx/Rx=60 with the recurring late-window caveat,
target2 accepted after a 7-source rescue with an early_high caveat, and target1
accepted cleanly at 5-source Tx/Rx=60. Continue the Fibonacci replication
chain with seed3416454629006707 target0 after confirming the active NumPy
environment accepts the seed. No separate numbered summary output folder was
created for this decision.

Stage 13PP: seed3416454629006707 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(3416454629006707)`
succeeds in the active FNO environment. Run 1206 is exact and accepted. The
base margin is 5.540e-04, or 5.405e-05 above cutoff. Highband, veryhigh, and
early_high clear cutoff; late and late_high remain weak, so carry the
recurring target0 late-window caveat. All six diagnostic objectives rank the
true target0 geometry first, so no target0 rescue branch is justified. Continue
seed3416454629006707 with target2 at the standard 5-source Tx/Rx=60 control.
No separate numbered summary output folder was created for this decision.

Stage 13PQ: seed3416454629006707 target2 5-source Tx/Rx=60 control.

Run 1207 is exact but weak. The base margin is 4.242e-04, or
7.583e-05 below cutoff, and early_high is weak at 4.051e-04. Highband, late,
late_high, and veryhigh clear cutoff, and all six diagnostic objectives rank
the true target2 geometry first. Treat this as a weak exact-geometry target2
control and run the standard 7-source Tx/Rx=60 source-density bracket before
accepting or escalating further. No separate numbered summary output folder
was created for this decision.

Stage 13PR: seed3416454629006707 target2 7-source Tx/Rx=60 source-density bracket.

Run 1208 is exact but remains weak by a near-miss margin. The base margin is
4.936e-04, or 6.405e-06 below cutoff, and early_high is weak at 4.412e-04.
Highband, late, late_high, and veryhigh clear cutoff, and all six diagnostic
objectives rank the true target2 geometry first. Escalate to the standard
9-source Tx/Rx=60 bracket before accepting or carrying this target2 result. No
separate numbered summary output folder was created for this decision.

Stage 13PS: seed3416454629006707 target2 9-source Tx/Rx=60 source-density escalation.

Run 1209 is exact and accepted cleanly. The base margin is 5.601e-04, or
6.010e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target2 geometry first. This 9-source escalation rescues
target2 after weak 5- and 7-source runs. Continue seed3416454629006707 with
target1 at the standard 5-source Tx/Rx=60 control. No separate numbered summary
output folder was created for this decision.

Stage 13PT: seed3416454629006707 target1 5-source Tx/Rx=60 control.

Run 1210 is exact and accepted cleanly. The base margin is 5.707e-04, or
7.069e-05 above cutoff, and all six diagnostic objectives clear cutoff while
ranking the true target1 geometry first. This closes seed3416454629006707:
target0 accepted at 8-source Tx/Rx=60 with the recurring late-window caveat,
target2 accepted after a clean 9-source rescue, and target1 accepted cleanly at
5-source Tx/Rx=60. Continue the Fibonacci replication chain with
seed5527939710754757 target0 after confirming the active NumPy environment
accepts the seed. No separate numbered summary output folder was created for
this decision.

Stage 13PU: seed5527939710754757 target0 8-source Tx/Rx=60 control.

Seed validation confirmed that `np.random.default_rng(5527939710754757)`
succeeds in the active FNO environment. Run 1211 is exact but weak. The base
margin is 4.505e-04, or 4.948e-05 below cutoff. Highband, veryhigh, and
early_high clear cutoff; late and late_high remain weak. All six diagnostic
objectives rank the true target0 geometry first, so this is a weak confidence
case rather than a geometry failure. Run the established target0 Tx/Rx-offset
rescue branch with 8 sources at Tx/Rx=52.5 mm. No separate numbered summary
output folder was created for this decision.

Stage 13PV: seed5527939710754757 target0 8-source Tx/Rx=52.5 rescue.

Run 1212 is exact but remains weak by a near-miss margin. The base margin is
4.930e-04, or 6.993e-06 below cutoff, while highband, veryhigh, and early_high
clear cutoff and all six diagnostic objectives rank the true target0 geometry
first. Tx/Rx=52.5 improves the base margin by about 4.25e-05 over the Tx/Rx=60
control, so follow the established target0 acquisition-bracket policy and test
the 8-source Tx/Rx=50 mm probe before changing mechanism or carrying weak
confidence. No separate numbered summary output folder was created for this
decision.

Stage 13PW: seed5527939710754757 target0 8-source Tx/Rx=50 acquisition bracket.

Run 1213 is exact and base-accepted with small reserve. The base margin is
5.024e-04, or 2.431e-06 above cutoff. Highband, veryhigh, and early_high clear
cutoff; late and late_high remain weak. All six diagnostic objectives rank the
true target0 geometry first. Because the accepted reserve is very small, follow
the established lower-edge target0 acquisition-bracket policy and run one
Tx/Rx=45 check before closing target0. No separate numbered summary output
folder was created for this decision.

Stage 13PX: seed5527939710754757 target0 8-source Tx/Rx=45 lower-edge bracket.

Run 1214 is exact and accepted. The base margin is 5.150e-04, or
1.495e-05 above cutoff, and it is the strongest tested target0 acquisition
point for this seed. Highband, veryhigh, and early_high clear cutoff; late and
late_high remain weak. All six diagnostic objectives rank the true target0
geometry first. Stop the target0 acquisition sweep here, close target0 with the
late-window caveat, and continue seed5527939710754757 with target2 at the
standard 5-source Tx/Rx=60 control. No separate numbered summary output folder
was created for this decision.

Stage 13PY: seed5527939710754757 target2 5-source Tx/Rx=60 control.

Run 1215 is exact and accepted. The base margin is 5.875e-04, or
8.754e-05 above cutoff. Highband, late, late_high, and veryhigh clear cutoff;
early_high remains weak at 4.864e-04, so carry the target2 early-window caveat.
All six diagnostic objectives rank the true target2 geometry first, so no
source-density escalation is justified. Continue seed5527939710754757 with
target1 at the standard 5-source Tx/Rx=60 control. No separate numbered summary
output folder was created for this decision.

Stage 13PZ: seed5527939710754757 target1 5-source Tx/Rx=60 control.

Run 1216 is exact but weak. The base margin is 4.516e-04, or 4.838e-05 below
cutoff, and early_high is weak at 4.407e-04. Highband, late, late_high, and
veryhigh clear cutoff, and all six diagnostic objectives rank the true target1
geometry first. This is the recurring target1 weak-control pattern, so run the
established 9-source Tx/Rx=60 rescue. After that rescue is documented, stop for
a marathon-level evaluation before starting another seed or field-data goal. No
separate numbered summary output folder was created for this decision.

Stage 13QA: seed5527939710754757 target1 9-source Tx/Rx=60 rescue and stop-point evaluation.

Run 1217 is exact but remains weak by a near-miss margin. The base margin is
4.875e-04, or 1.254e-05 below cutoff. Highband, late, late_high, veryhigh, and
early_high all clear cutoff, and all six diagnostic objectives rank the true
target1 geometry first. Because the 9-source rescue improves but does not clear
the strict base cutoff, run an 11-source Tx/Rx=60 target1 escalation before
evaluating the branch. No separate numbered summary output folder was created
for this decision.

Stage 13QB: seed5527939710754757 target1 11-source Tx/Rx=60 escalation and stop-point evaluation.

Run 1218 is exact but weak, and it is a negative 11-source escalation. The
base margin drops to 3.632e-04, or 1.368e-04 below cutoff. Only late_high
clears cutoff; highband, late, veryhigh, and early_high are all below cutoff.
All six diagnostic objectives still rank the true target1 geometry first. This
means the seed5527939710754757 target1 source-density sequence peaks at the
9-source near-miss rather than resolving at 11 sources. Stop this branch as
exact geometry with unresolved target1 radius-confidence under the tested
Tx/Rx=60 source-density policy. No separate numbered summary output folder was
created for this decision.

Stop-point evaluation: pause new GPU experiments before starting another seed
or field-data goal. The next work item should be synthesis: summarize the
completed seed branches, identify rescue-policy failure modes, and decide
whether target1 unresolved cases should use acquisition-offset probes,
objective threshold revisions, or a broader geometry/noise model before more
Fibonacci seed replication.
