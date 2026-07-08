# Experiment 1805: 84-Grid External Return Approval Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1804` validator with damaged versions of the run `1803`
approval template pack.

Damaged cases include policy-label damage, source-readiness damage,
template-row-count damage, template-file-presence damage, payload-count damage,
payload-identity damage, approval-token promotion, approver-field promotion,
approval-time promotion, payload-status promotion, external-root damage,
live-approval promotion, artifact-intake promotion, materialization promotion,
FDTD-execution promotion, field-transfer promotion, 3D promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1805_local_2d_state_consistent_objective_revision_84grid_external_return_approval_template_pack_validation_sensitivity
```

## Result

```text
scenarios:                    22
expected pass scenarios:       1
expected fail scenarios:      21
observed pass scenarios:       1
observed fail scenarios:      21
unexpected outcomes:           0
damaged scenarios:            21
damaged scenarios rejected:   21
gpu priority:                 none
```

## Interpretation

The validator fails closed. The exact saved draft approval template passes,
while all damaged or falsely promoted variants fail.

## Decision

Use runs `1803-1805` as the guarded 84-grid approval-template block. The block
prepares the approval form but does not authorize artifact intake,
materialization, new FDTD execution, field transfer, or 3D/HPC.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_approval_template_pack_validation_sensitivity.py
```

Figure check:

```text
3761x884, dynamic range=255
```
