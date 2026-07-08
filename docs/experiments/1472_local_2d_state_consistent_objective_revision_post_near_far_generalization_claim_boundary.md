# Experiment 1472: Post Near/Far Generalization Claim Boundary

Date: 2026-06-28

## Purpose

Refresh the local 2D claim boundary after the guarded target-position and
target-depth generalization blocks.

This run consumes saved artifacts from:

```text
1465 post near/far interaction claim-boundary validator
1469 target-position generalization validator
1471 target-depth generalization validator
```

It is an artifact-only claim-boundary run. It does not run new FDTD
simulations, GPU work, field transfer, field FWI, neural-network training, or
3D/HPC work.

## Output

```text
outputs/experiments/1472_local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_NEAR_FAR_GENERALIZATION_CLAIM_BOUNDARY.md
```

## Result

```text
claims:                         7
guarded claims:                 4
blocked claims:                 3
position generalization ready:  true
depth generalization ready:     true
boundary ready:                 true
position dependent boundary:    true
depth dependent boundary:       true
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

## Interpretation

The near/far radius-error mechanism remains guarded as local synthetic
evidence. The generalization runs changed the claim boundary:

- target-position translation softened the severe all-objective failure pattern,
- shallower target depth removed failures in the tested grid,
- deeper target depth preserved severe failures only when far-neighbor radius
  error was present.

The severe all-objective boundary is therefore not position-invariant or
depth-invariant in the tested configurations.

## Decision

Use run `1472` as the current 2D claim boundary. Keep broad-radius tolerance,
physical-transfer, GPU, field-FWI, and 3D/HPC claims blocked until additional
spacing, source, acquisition, or measured-field evidence closes those gaps.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary.py
3 passed
```

Figure validation:

```text
3329x932, dynamic range=255
```
