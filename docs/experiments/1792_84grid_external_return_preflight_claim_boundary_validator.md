# Experiment 1792: 84-Grid External Return Preflight Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1791` 84-grid external-return preflight claim boundary.

This validator checks that the boundary has two guarded claims, three blocked
claims, zero candidate files, zero preflight-passed items, and no materialized
observed-by-case data, new FDTD execution, or 3D/HPC promotion.

## Output

```text
outputs/experiments/1792_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_claim_boundary_validator
```

## Result

```text
validation checks:                7
passed checks:                    7
failed checks:                    0
claims:                           5
guarded claims:                   2
blocked claims:                   3
preflight items:                  21
approval items:                   1
cache-array items:                10
result-JSON items:                10
candidate files present:          0
preflight-passed items:           0
observed-by-case materialized:    false
new FDTD executed:                false
3D/HPC ready:                     false
gpu priority:                     none
```

## Decision

Use run `1792` before citing run `1791` as the current 84-grid external-return
preflight claim boundary.

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
3329x935, dynamic range=255
```
