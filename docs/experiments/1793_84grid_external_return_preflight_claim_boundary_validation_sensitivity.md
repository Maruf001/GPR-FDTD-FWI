# Experiment 1793: 84-Grid External Return Preflight Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1792` claim-boundary validator by damaging the saved run
`1791` state in controlled ways.

This run checks whether false claim counts, false guarded or blocked states,
candidate-file promotion, preflight-pass promotion, materialization promotion,
FDTD promotion, downstream promotion, figure damage, and script-snapshot damage
are rejected.

## Output

```text
outputs/experiments/1793_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_claim_boundary_validation_sensitivity
```

## Result

```text
source validator ready:           true
scenarios:                        15
expected pass scenarios:          1
expected fail scenarios:          14
observed pass scenarios:          1
observed fail scenarios:          14
unexpected outcomes:              0
damaged scenarios rejected:       14
gpu priority:                     none
```

## Decision

Use runs `1791-1793` as the guarded post-preflight claim-boundary block for the
84-grid external-return branch.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_claim_boundary_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_claim_boundary_validation_sensitivity.py

9 passed
```

Figure check:

```text
2932x872, dynamic range=255
```
