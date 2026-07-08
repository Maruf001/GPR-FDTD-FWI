# Experiment 1802: 84-Grid External Return File-Slot Manifest Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1801` validator with damaged versions of the run `1800`
claim boundary.

The damaged scenarios include claim-count drift, missing guarded claims,
file-slot count damage, stage-shape damage, cache/result count damage, paired
job-count damage, false producer-file promotion, false paired-job readiness,
false materialization promotion, false FDTD promotion, false field/3D
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1802_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                      23
expected pass scenarios:        1
expected fail scenarios:        22
observed pass scenarios:        1
observed fail scenarios:        22
unexpected outcomes:            0
damaged scenarios:              22
damaged scenarios rejected:     22
gpu priority:                   none
```

The exact saved claim boundary passes. All twenty-two damaged variants fail.

## Decision

Use runs `1800-1802` as the current guarded 2D external-return file-slot
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_claim_boundary_validation_sensitivity.py

3 passed
```

Figure check:

```text
3761x884, dynamic range=255
```
