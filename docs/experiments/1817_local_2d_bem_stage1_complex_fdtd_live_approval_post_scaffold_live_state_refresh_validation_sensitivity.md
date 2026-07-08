# Experiment 1817: BEM Stage-1 Complex FDTD Live Approval Post-Scaffold Live-State Refresh Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1816` validator by damaging the saved run `1815`
post-scaffold live-state refresh in controlled ways.

The sensitivity set checks source-readiness damage, state/action row damage,
approval-directory absence, false approval-file presence, false approval-field
completion, false approval acceptance, partial-return path damage, false
partial-return presence, false action completion, FDTD authorization/execution
promotion, BEM/FDTD comparison promotion, field/3D promotion, figure damage,
and script-snapshot damage.

## Output

```text
outputs/experiments/1817_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh_validation_sensitivity
```

## Result

```text
scenarios:                         18
expected passes:                    1
expected failures:                 17
observed passes:                    1
observed failures:                 17
unexpected outcomes:                0
damaged scenarios:                 17
damaged scenarios rejected:        17
FDTD producer authorized now:     false
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
gpu priority:                     none
```

The exact saved post-scaffold state passes. All damaged states fail.

## Interpretation

The validator accepts only the exact directory-present, live-files-absent state
and rejects false promotion of approval, FDTD execution, BEM/FDTD comparison,
field transfer, 3D/HPC, figures, and script snapshots.

## Decision

Use runs `1815-1817` as the guarded BEM stage-1 post-scaffold live-state refresh
block.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh_validation_sensitivity.py
9 passed
```

Figure check:

```text
3131x871, dynamic range=255
```
