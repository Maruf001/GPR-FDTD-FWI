# BEM Experiment 841: Stage-1 Producer Post-Scaffold 2D Approval Sync Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `840` validator by damaging the saved run `839`
post-scaffold BEM/2D synchronization audit in controlled ways.

The sensitivity set checks source-readiness damage, sync-row damage, failed
sync checks, receiver/frequency damage, approval-directory damage, false
approval-file presence, false approval-field completion, false partial-return
presence, false full-input promotion, false FDTD execution, false comparison,
field/3D promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/841_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_post_scaffold_2d_approval_sync_audit_validation_sensitivity
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

The exact synchronized, non-executed state passes. All damaged states fail.

## Interpretation

The synchronization validator accepts only the exact BEM/2D handoff state and
rejects false promotion of approval, live files, FDTD execution, comparison,
field transfer, 3D/HPC, figures, and script snapshots.

## Decision

Use runs `839-841` as the guarded BEM/2D post-scaffold synchronization block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_post_scaffold_2d_approval_sync_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_post_scaffold_2d_approval_sync_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_post_scaffold_2d_approval_sync_audit_validation_sensitivity.py
8 passed
```

Figure check:

```text
3131x873, dynamic range=255
```
