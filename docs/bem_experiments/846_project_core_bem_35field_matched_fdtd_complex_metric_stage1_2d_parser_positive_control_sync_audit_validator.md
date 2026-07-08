# BEM Experiment 846: Stage-1 2D Parser Positive-Control Sync Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `845` BEM/2D parser positive-control synchronization
audit.

The validator checks source readiness, audit shape, receiver/frequency identity,
partial-return schema identity, positive-control parser state, non-live
approval placement, blocked FDTD execution, blocked BEM/FDTD comparison, figure
validation, and script snapshots.

## Output

```text
outputs/bem_experiments/846_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_parser_positive_control_sync_audit_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
audit checks:                            8
receiver index:                         15
frequency:                    1000000000 Hz
positive-control files:                  1
parser checks:                           5
parser checks passed:                    5
accepted as payload shape:            true
written under live approval root:     false
live approval file present:           false
accepted live approvals:                 0
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
ready for 3D/HPC:                     false
gpu priority:                         none
```

## Interpretation

The BEM/2D parser positive-control synchronization audit validates as a
shape-only, non-executed state.

## Decision

Keep FDTD execution blocked until a real live approval JSON is supplied.

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
2285x862, dynamic range=255
```
