# BEM Experiment 847: Stage-1 2D Parser Positive-Control Sync Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `846` validator by damaging the saved run `845` BEM/2D
parser positive-control synchronization audit in controlled ways.

The sensitivity set checks source-readiness damage, row-count damage, failed
sync checks, receiver/frequency damage, positive-control count damage,
parser-count damage, parser-pass damage, payload-shape damage, live-root
promotion, live-approval promotion, acceptance promotion, FDTD execution
promotion, comparison promotion, field/3D promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/bem_experiments/847_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_parser_positive_control_sync_audit_validation_sensitivity
```

## Result

```text
scenarios:                         19
expected passes:                    1
expected failures:                 18
observed passes:                    1
observed failures:                 18
unexpected outcomes:                0
damaged scenarios:                 18
damaged scenarios rejected:        18
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
field transfer ready:             false
ready for 3D/HPC:                 false
gpu priority:                     none
```

The exact synchronized parser positive-control state passes. All damaged states
fail.

## Interpretation

The validator accepts only the exact BEM/2D parser positive-control non-live
state and rejects false promotion to live approval, FDTD execution, BEM/FDTD
comparison, field transfer, or 3D/HPC.

## Decision

Use runs `845-847` as the guarded BEM/2D parser positive-control
synchronization block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_parser_positive_control_sync_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_parser_positive_control_sync_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_parser_positive_control_sync_audit_validation_sensitivity.py
8 passed
```

Figure check:

```text
3257x843, dynamic range=255
```
