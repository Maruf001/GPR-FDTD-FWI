# Experiment 1816: BEM Stage-1 Complex FDTD Live Approval Post-Scaffold Live-State Refresh Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1815` post-scaffold live-state refresh from artifacts.

The validator checks source readiness, row shape, approval-directory presence,
approval-file absence, required approval-field absence, partial-return absence,
the single completed directory action, blocked FDTD execution, blocked real
BEM/FDTD comparison, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1816_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh_validator
```

## Result

```text
validation checks:                           7
passed checks:                               7
failed checks:                               0
state rows:                                  2
action rows:                                 5
live approval parent present:             true
live approval file present:               false
live approval fields missing:                9
BEM partial-return parent present:         true
BEM partial-return file present:          false
completed actions:                           1
FDTD producer authorized now:              false
FDTD executed now:                         false
real BEM/FDTD comparison ready:            false
gpu priority:                              none
```

## Interpretation

The saved post-scaffold state is internally consistent: the drop directory is
ready for a future live approval file, but no execution approval or FDTD return
has been accepted.

## Decision

Use this validator before treating the post-scaffold live state as an accepted
handoff state.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh_validator.py
9 passed with refresh/sensitivity block
```

Figure check:

```text
2501x864, dynamic range=255
```
