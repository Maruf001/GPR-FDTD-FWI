# BEM Experiment 438: Post Threshold-Ladder Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `437` from saved artifacts.

The validator checks claim counts, threshold-claim support, threshold metrics,
blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/438_project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
threshold-boundary validation ready:true
claims:                            25
guarded claims:                    22
blocked claims:                    3
threshold ladder ready:            true
scenarios:                         9
pass scenarios:                    5
fail scenarios:                    4
perturbed score rows:              2511
pass rows:                         1395
fail rows:                         1116
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Decision

Use this validator as the artifact guard for run `437`. Sensitivity testing
remains required before closing the post-threshold-ladder claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validator.py
5 passed as part of the 12-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```
