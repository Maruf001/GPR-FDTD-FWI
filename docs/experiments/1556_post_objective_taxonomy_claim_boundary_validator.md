# Experiment 1556: Post Objective Taxonomy Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1555` local 2D claim boundary from artifacts.

## Output

```text
outputs/experiments/1556_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary_validator
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
claim-boundary validation ready:     true
claims:                              23
guarded claims:                      20
blocked claims:                      3
objectives:                          6
models:                              20
universally failing objectives:      2
universally passing objectives:      4
dominant failure pattern:            base;early_high
wide-window claim ready:             false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
3D/HPC ready:                        false
```

The validator confirms claim counts, the taxonomy claim row, taxonomy metrics,
blocked claim rows, blocked downstream states, figure validation, and script
snapshots.

## Decision

Use this validator as the artifact guard for run `1555`. Sensitivity hardening
remains required before closing the block.

## Validation

Focused validator test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3581x893, dynamic range=255
```
