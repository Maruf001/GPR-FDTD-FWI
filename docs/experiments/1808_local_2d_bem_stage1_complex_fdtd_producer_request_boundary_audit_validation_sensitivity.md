# Experiment 1808: BEM Stage-1 Complex FDTD Producer Request Boundary Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1807` validator by damaging the saved run `1806` boundary
audit in controlled ways.

The sensitivity set checks false source readiness, BEM request identity drift,
false 2D approval, false live-file presence, false FDTD authorization, false
FDTD execution, downstream promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1808_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit_validation_sensitivity
```

## Result

```text
scenarios:                         21
expected passes:                    1
expected failures:                 20
observed passes:                    1
observed failures:                 20
unexpected outcomes:                0
damaged scenarios:                 20
damaged scenarios rejected:        20
gpu priority:                    none
```

The exact saved boundary passes. All damaged states fail:

```text
policy-label damage
audit-readiness damage
source-readiness damage
boundary-shape damage
BEM receiver damage
BEM frequency damage
approval-token promotion
live-approval count promotion
live 2D file promotion
BEM partial-file promotion
BEM full-file promotion
row-authorization promotion
current 2D authorization promotion
FDTD authorization promotion
FDTD execution promotion
comparison promotion
field-transfer promotion
3D/HPC promotion
figure damage
script-snapshot damage
```

## Interpretation

The boundary validator accepts only the exact saved non-authorizing BEM/2D FDTD
state. It rejects controlled damage to source readiness, identity, approval,
live-file state, FDTD authorization, FDTD execution, downstream promotion,
figure validation, and script snapshots.

## Decision

Use runs `1806-1808` as the guarded 2D boundary for the BEM stage-1 FDTD
producer request.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit.py
tests/test_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit_validation_sensitivity.py
8 passed
```

Figure check:

```text
3797x885, dynamic range=255
```
