# BEM Experiment 850: Stage-1 2D Live Approval Gate Sync Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `849` validator by damaging the saved run `848` BEM/2D
live approval gate synchronization audit in controlled ways.

The sensitivity set checks source-readiness damage, row-count damage, failed
sync checks, receiver damage, gate-pass promotion, live-file promotion,
accepted-approval promotion, FDTD authorization/execution promotion,
comparison promotion, field-transfer promotion, 3D/HPC promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/850_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_live_approval_gate_sync_audit_validation_sensitivity
```

## Result

```text
scenarios:                         15
expected passes:                    1
expected failures:                 14
observed passes:                    1
observed failures:                 14
unexpected outcomes:                0
damaged scenarios:                 14
damaged scenarios rejected:        14
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
field transfer ready:             false
ready for 3D/HPC:                 false
gpu priority:                     none
```

The exact fail-closed live approval gate state passes. All damaged states fail.

## Interpretation

The validator accepts only the exact fail-closed BEM/2D live approval gate state
and rejects false approval, authorization, execution, comparison, field
transfer, or 3D/HPC promotion.

## Decision

Use runs `848-850` as the guarded BEM/2D live approval gate synchronization
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_live_approval_gate_sync_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_live_approval_gate_sync_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_live_approval_gate_sync_audit_validation_sensitivity.py
8 passed
```

Figure check:

```text
2861x851, dynamic range=255
```
