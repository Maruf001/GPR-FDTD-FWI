# Experiment 1557: Post Objective Taxonomy Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1556` validator with controlled damaged variants of the
run `1555` claim boundary.

## Output

```text
outputs/experiments/1557_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                           13
expected pass:                       1
observed pass:                       1
expected failures:                   12
observed failures:                   12
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 1555:              true
rejects damaged variants:            true
claims:                              23
objectives:                          6
dominant failure pattern:            base;early_high
physical claim ready:                false
field transfer ready:                false
3D/HPC ready:                        false
```

The exact run `1555` artifacts pass. Twelve damaged variants fail as expected
for source-label drift, claim-count drift, taxonomy-support drift,
taxonomy-evidence drift, objective-count drift, universal-failure count drift,
dominant-pattern drift, source-readiness demotion, blocked-support drift,
downstream promotion, figure drift, and script-snapshot drift.

## Decision

Use runs `1555-1557` as the current guarded 2D post-taxonomy claim-boundary
block.

## Validation

Focused sensitivity test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary_validation_sensitivity.py
2 passed
```

Combined focused boundary tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary_validator.py
tests/test_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3473x886, dynamic range=255
```
