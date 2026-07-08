# Experiment 1473: Post Near/Far Generalization Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1472` claim-boundary artifact after the target-position
and target-depth near/far generalization blocks.

This is an artifact-only validator. It does not run new FDTD simulations, GPU
work, field transfer, field FWI, neural-network training, or 3D/HPC work.

## Output

```text
outputs/experiments/1473_local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_NEAR_FAR_GENERALIZATION_CLAIM_BOUNDARY_VALIDATOR.md
```

## Result

```text
validation checks:           6
passed checks:               6
failed checks:               0
validation ready:            true
claims:                      7
guarded claims:              4
blocked claims:              3
position dependent boundary: true
depth dependent boundary:    true
broad radius promoted:       false
physical claim ready:        false
GPU work ready:              false
field transfer ready:        false
field FWI ready:             false
3D/HPC ready:                false
```

## Interpretation

Run `1472` validates as the current local 2D near/far generalization claim
boundary. The near/far mechanism is guarded local evidence, but the severe
all-objective failure boundary is not position-invariant or depth-invariant in
the tested configurations.

## Decision

Use run `1473` as the validator for the current 2D near/far claim boundary.
Keep broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_near_far_generalization_claim_boundary_validator.py
6 passed
```

Figure validation:

```text
3401x896, dynamic range=255
```
