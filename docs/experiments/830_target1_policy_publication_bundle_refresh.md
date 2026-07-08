# Experiment 830: Target1 Policy Publication-Bundle Refresh

Date: 2026-06-18

## Purpose

Move the current target1 acquisition-confidence surface and source-density
exception map into the paper-facing synthetic 2D publication bundle, then
refresh the next-question matrix. This is CPU-only reporting synthesis over
existing outputs; it does not launch FDTD, FWI, optimizer, or GPU experiments.

This tracker covers runs 1320-1321 as one research slice.

Superseded endpoint note: experiment 831 / runs 1322-1323 keep the target1
policy figures from this tracker but reconcile the current paper-facing bundle
with the detailed close14/close50 claim-boundary rows. Run 1323 is the current
synthetic next-question matrix.

## Outputs

```text
outputs/experiments/1320_synthetic_2d_publication_figure_bundle_post_target1_policy_refresh
outputs/experiments/1321_synthetic_2d_next_question_matrix_post_target1_publication_bundle
```

Key artifacts:

```text
outputs/experiments/1320_synthetic_2d_publication_figure_bundle_post_target1_policy_refresh/data/synthetic_2d_publication_figure_rows.csv
outputs/experiments/1320_synthetic_2d_publication_figure_bundle_post_target1_policy_refresh/data/synthetic_2d_publication_claim_boundaries.csv
outputs/experiments/1320_synthetic_2d_publication_figure_bundle_post_target1_policy_refresh/figures/synthetic_2d_publication_figure_bundle.png
outputs/experiments/1321_synthetic_2d_next_question_matrix_post_target1_publication_bundle/data/synthetic_2d_next_question_matrix_summary.json
```

## Result

Run 1320 refreshes the paper-facing synthetic 2D bundle:

```text
policy label:                  synthetic_2d_publication_bundle_current_resolution_target1_ready_gpu_priority_none
figure count:                  9
validated figures:             9 / 9
claim boundaries:              6
target1 policy figures:        included
gpu priority:                  none
ready for manuscript draft:    true
```

The added target1 rows are:

```text
target1 acquisition-confidence surface:
  source run:                  1312
  canonical target1 rows:      133
  exact geometry rows:         133
  base weak-exact rows:         43
  late_high accepted:          132 / 133
  terminal 11-source worse:      2 / 2

target1 source-density exception map:
  source run:                  1314
  source-density series:        17
  modern exceptions:             0
  legacy exceptions:             1
  terminal 11-source worse:      2 / 2
  gpu priority:                none
```

Run 1321 refreshes the synthetic next-question matrix:

```text
policy label:                  synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                10
cpu-first candidates:           0
immediate GPU candidates:       0
conditional GPU candidates:     0
target1 surface included:       true
target1 exception map included: true
top question:                  synthetic_publication_bundle_current
gpu priority:                  none_now
```

## Interpretation

This refresh does not change the no-GPU posture. It makes the paper-facing
synthetic bundle current with the target1 result: target1 localization is not
the failure mode because all canonical target1 rows recover exact geometry.
The remaining target1 claim is about confidence policy and acquisition design:
canonical base confidence is acquisition-sensitive, source-density escalation
is nonmonotonic, and terminal 11-source branches get worse. The source-density
exception map closes the current target1 GPU branch with zero modern
exceptions and one legacy ringdown025 archive caveat.

Do not launch a target1 source-count rerun unless a new objective definition,
geometry, or acquisition hypothesis is stated first.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_publication_figure_bundle.py
tests/test_synthetic_2d_next_question_matrix.py
16 passed
```

Figure validation:

```text
1320 synthetic_2d_publication_figure_bundle.png: 2738x903, dynamic range=255
1321 synthetic_2d_next_question_matrix.png: 2501x903, dynamic range=255
```
