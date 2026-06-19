# Experiment 759: 2D Target1 Policy Boundary And Field Separation

Date: 2026-06-17

## Purpose

Continue the local 2D synthetic confidence-policy work after experiment 758
without launching new optimizer, FDTD, FWI, figure-generation, or GPU commands.

This note makes the current seed `5527939710754757` target1 branch decision
explicit and keeps the field data stream separate. It does not close the full
2D synthetic program. Field-data synthesis belongs under
`docs/field_experiments/local_gssi_51600s_2026_06_09/`, not in this synthetic
tracker sequence.

## Inputs Read

```text
docs/experiments/758_target1_confidence_policy_synthesis.md
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/coordinate_run_summary_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/target1_source_density_policy_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/txrx_target_policy_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/objective_variant_summary_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/rank1_candidate_summary_700_1218.csv
docs/field_experiments/local_gssi_51600s_2026_06_09/004_gssi51600s_common_offset_sweep.md
```

## CPU Recheck

The restored holistic tables still support the experiment 758 interpretation:

```text
target1 coordinate rows:             127
target1 accepted rows:                90
target1 weak rows:                    37
target1 weak rows with exact geometry: 37
```

Target1 weak rows by acquisition setting:

| Sources | Tx/Rx mm | Weak rows |
| ---: | ---: | ---: |
| 5 | 45.0 | 1 |
| 5 | 50.0 | 1 |
| 5 | 52.5 | 2 |
| 5 | 55.0 | 1 |
| 5 | 57.5 | 1 |
| 5 | 60.0 | 16 |
| 7 | 52.5 | 1 |
| 7 | 60.0 | 1 |
| 8 | 60.0 | 3 |
| 9 | 60.0 | 8 |
| 11 | 60.0 | 2 |

The weak target1 problem remains a confidence-margin problem, not a tested
bounded-geometry localization failure.

## Current Decision Branch

For seed `5527939710754757` target1:

| Run | Sources | Tx/Rx mm | Base margin | Offset from cutoff | Label |
| --- | ---: | ---: | ---: | ---: | --- |
| 1216 | 5 | 60.0 | 4.516e-4 | -4.838e-5 | weak |
| 1217 | 9 | 60.0 | 4.875e-4 | -1.254e-5 | weak near-miss |
| 1218 | 11 | 60.0 | 3.632e-4 | -1.368e-4 | weak negative escalation |
| 1223 | 5 | 52.5 | 4.432e-4 | -5.568e-5 | weak acquisition-offset probe |

Run 1217 remains the best existing row for this branch. Its base objective is
just below the strict `5.0e-4` cutoff, while five of six objective variants
clear the cutoff:

| Run | Objective | Margin | Offset from cutoff |
| --- | --- | ---: | ---: |
| 1217 | base | 4.875e-4 | -1.254e-5 |
| 1217 | early_high | 5.020e-4 | 2.021e-6 |
| 1217 | highband | 6.847e-4 | 1.847e-4 |
| 1217 | late | 7.245e-4 | 2.245e-4 |
| 1217 | late_high | 9.346e-4 | 4.346e-4 |
| 1217 | veryhigh | 6.524e-4 | 1.524e-4 |

Run 1218 is a useful negative control: increasing source count to 11 made the
base margin worse and left only `late_high` above cutoff.

Run 1223 tested the one narrow Tx/Rx=52.5 mm acquisition-offset probe supported
by experiment 758. It preserved exact rank-1 geometry, but its base margin
remained weak and only four of six objective variants cleared the cutoff. This
does not support additional source-count or Tx/Rx escalation for this specific
branch without a new objective-policy hypothesis.

## Branch Policy

The current branch policy should be:

1. Do not run broad source-density escalation for target1.
2. Do not reinterpret exact-but-weak as accepted.
3. Carry run 1217 as exact geometry with strict target1 radius confidence
   unresolved.
4. Run no additional GPU work for this seed branch unless a new objective-policy
   hypothesis is defined first.

The one synthetic probe supported by the CPU policy has now been run:

```text
seed:     5527939710754757
target:   target1
sources:  5
Tx/Rx:    52.5 mm
ringdown: 0.50
purpose:  one target1 acquisition-offset rescue after source-density escalation
          failed
run:      1223
result:   exact rank-1 x/z/r geometry, weak base margin 4.432e-4
```

The branch should be carried as exact-but-unresolved. This is a branch-level
decision only; other 2D synthetic hypotheses and field-data work remain active.

## What To Do Next On The 2D Side

CPU-safe next actions:

1. Convert the target1 policy into manuscript language:
   exact geometry, weak margin, unresolved confidence, and near-best competitor
   branch should be described separately.
2. Add a small table in the paper draft or final report that shows the
   run 1216/1217/1218 progression and the objective-variant margins for 1217.
3. Add a target-specific acquisition-policy paragraph:
   target1 52.5 mm has useful evidence, but target1 source count is not
   monotonic and 11 sources is not a default rescue.
4. Keep current target1 weak rows in the confidence-policy dataset; do not drop
   them as failures because they are the evidence for ambiguity labeling.
5. Continue field-data work in the field tracker stream only.

GPU-gated next action:

1. Do not repeat source-count or Tx/Rx perturbations for this seed branch.
2. Use any future GPU work for a new, documented hypothesis, such as a changed
   objective policy or a separate close-spacing branch.

## Boundary With Field Data

The field stream should inform acquisition hypotheses, not alter synthetic
truth labels. The local GSSI common-offset sweep currently suggests that a
60 mm effective Tx/Rx offset is a useful measured-data overlay hypothesis, but
that field result is not calibrated cover depth and not a synthetic target1
confidence result.

The synthetic conclusion remains based on known-truth 2D archive rows. Field
notes should remain in:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/
outputs/field_experiments/local_gssi_51600s_2026_06_09/
```
