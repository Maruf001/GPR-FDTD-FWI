# Experiment 1555: Post Objective Taxonomy Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the local 2D claim boundary after the follow-up offset objective-failure
taxonomy audit.

## Output

```text
outputs/experiments/1555_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary
```

## Result

```text
claims:                              23
guarded claims:                      20
blocked claims:                      3
taxonomy sensitivity ready:          true
objectives:                          6
models:                              20
offsets:                             5
universally failing objectives:      2
universally passing objectives:      4
dominant failure pattern:            base;early_high
dominant-pattern model count:        20
all models share same pattern:       true
wide-window claim ready:             false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
3D/HPC ready:                        false
```

The new guarded claim records that all 20 follow-up models share the same
objective-failure pattern: `base` and `early_high` fail, while `highband`,
`late`, `late_high`, and `veryhigh` pass.

## Decision

Use this as the current local 2D claim boundary after the taxonomy audit. Keep
wide-window, monotonic, physical, GPU, field, and 3D claims blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_objective_taxonomy_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x924, dynamic range=255
```
