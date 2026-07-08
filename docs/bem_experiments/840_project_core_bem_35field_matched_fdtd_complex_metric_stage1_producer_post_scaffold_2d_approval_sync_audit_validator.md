# BEM Experiment 840: Stage-1 Producer Post-Scaffold 2D Approval Sync Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `839` BEM/2D post-scaffold synchronization audit from
artifacts.

The validator checks source readiness, sync-row shape, stage-1 identity,
live-file absence, blocked FDTD execution, blocked real BEM/FDTD comparison,
figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/840_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_post_scaffold_2d_approval_sync_audit_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
sync checks:                               7
receiver index:                           15
frequency:                      1000000000 Hz
live approval parent present:           true
live approval file present:            false
live approval fields missing:              9
stage-1 partial file present:           false
full external input file present:       false
FDTD executed now:                      false
real BEM/FDTD comparison ready:         false
gpu priority:                           none
```

## Interpretation

The synchronized BEM/2D handoff validates as a stable non-executed state. The
approval directory exists, but neither required live file has been accepted.

## Decision

Use this validator before treating the synchronized handoff state as current.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_post_scaffold_2d_approval_sync_audit_validator.py
8 passed with audit/sensitivity block
```

Figure check:

```text
2285x859, dynamic range=255
```
