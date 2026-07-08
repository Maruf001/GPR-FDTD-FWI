# BEM Experiment 432: Post 35-Field Synthetic Normalized Comparator Score Smoke Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `431` from saved artifacts.

The validator checks claim counts, score-claim insertion, score metrics,
blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/432_project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
boundary validation ready:         true
claims:                            24
guarded claims:                    21
blocked claims:                    3
score rows:                        279
axis score rows:                   40
score passes:                      279
score failures:                    0
max normalized residual:           3.6369686315440523e-16
max raw reconstruction error:      4.4336379508346526e-16
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Decision

Use this validator as the artifact guard for run `431`. Sensitivity testing
remains required before closing the post-score-smoke claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validator.py
4 passed as part of the 23-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```
