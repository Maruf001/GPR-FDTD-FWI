# Experiment 831: Synthetic 2D Claim-Boundary Reconciliation

Date: 2026-06-18

## Purpose

Reconcile the current synthetic paper-facing figure bundle with the richer
claim-boundary table from the earlier close14/close50 claim refresh. This is
CPU-only reporting synthesis over existing outputs. It does not launch FDTD,
FWI, optimizer, or GPU experiments.

This tracker covers runs 1322-1323 as one research slice.

## Outputs

```text
outputs/experiments/1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation
outputs/experiments/1323_synthetic_2d_next_question_matrix_post_claim_boundary_reconciliation
```

Key artifacts:

```text
outputs/experiments/1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation/data/synthetic_2d_publication_claim_boundaries.csv
outputs/experiments/1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation/data/synthetic_2d_publication_figure_bundle_summary.json
outputs/experiments/1323_synthetic_2d_next_question_matrix_post_claim_boundary_reconciliation/data/synthetic_2d_next_question_matrix_summary.json
```

## Result

Run 1322 refreshes the paper-facing synthetic bundle:

```text
policy label:                    synthetic_2d_publication_bundle_current_resolution_target1_claims_ready_gpu_priority_none
figure count:                    9
validated figures:               9 / 9
claim boundaries:                11
target1 policy figures included: true
detailed claim boundaries:       true
ready for manuscript draft:      true
gpu priority:                    none
```

The reconciled claim-boundary CSV now includes:

```text
reporting_tiers
objective_uniqueness
target_specificity
target2_close14_objective_limit
target2_close50_linear29p5_seed_frequency
```

Run 1323 refreshes the synthetic next-question matrix:

```text
policy label:                  synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                10
cpu-first candidates:           0
immediate GPU candidates:       0
conditional GPU candidates:     0
top question:                  synthetic_publication_bundle_current
gpu priority:                  none_now
```

## Interpretation

This closes a reporting inconsistency: run 1320 was figure-current but carried
only six high-level claim boundaries, while the older claim refresh carried
the detailed close14/close50 boundaries. Run 1322 is now the paper-facing
synthetic bundle to use, because it combines the current figure set, target1
policy figures, close50 legacy midpoint evidence, and detailed claim
boundaries.

The reconciliation does not create a GPU queue. Run 1323 still reports zero
CPU-first, immediate-GPU, or conditional-GPU candidates under the current
questions.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_publication_figure_bundle.py
tests/test_synthetic_2d_next_question_matrix.py
16 passed
```

Figure validation:

```text
1322 synthetic_2d_publication_figure_bundle.png: 2738x903, dynamic range=255
1323 synthetic_2d_next_question_matrix.png: 2501x903, dynamic range=255
```
