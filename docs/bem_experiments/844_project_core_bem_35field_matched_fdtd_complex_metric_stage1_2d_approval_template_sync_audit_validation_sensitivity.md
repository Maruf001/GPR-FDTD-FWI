# BEM Experiment 844: Stage-1 2D Approval Template Sync Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `843` validator by damaging the saved run `842` BEM/2D
approval-template synchronization audit in controlled ways.

The sensitivity set checks source-readiness damage, row-count damage, failed
sync checks, receiver/frequency damage, template-count damage, target-prefill
damage, blank-approval-field damage, live-approval promotion, acceptance
promotion, FDTD execution promotion, comparison promotion, field/3D promotion,
figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/844_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_approval_template_sync_audit_validation_sensitivity
```

## Result

```text
scenarios:                         17
expected passes:                    1
expected failures:                 16
observed passes:                    1
observed failures:                 16
unexpected outcomes:                0
damaged scenarios:                 16
damaged scenarios rejected:        16
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
gpu priority:                     none
```

The exact synchronized draft state passes. All damaged states fail.

## Interpretation

The validator accepts only the exact BEM/2D approval-template draft state and
rejects false promotion to live approval, FDTD execution, BEM/FDTD comparison,
field transfer, or 3D/HPC.

## Decision

Use runs `842-844` as the guarded BEM/2D approval-template synchronization
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_approval_template_sync_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_approval_template_sync_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_approval_template_sync_audit_validation_sensitivity.py
8 passed
```

Figure check:

```text
3005x851, dynamic range=255
```
