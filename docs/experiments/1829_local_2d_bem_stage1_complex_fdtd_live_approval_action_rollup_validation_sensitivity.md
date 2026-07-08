# Experiment 1829: BEM Stage-1 Complex FDTD Live Approval Action Rollup Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1828` validator by damaging the saved run `1827` action
rollup in controlled ways.

The sensitivity set checks source-readiness damage, row-shape damage, false
live-artifact promotion, approval-field damage, gate-pass promotion,
accepted-approval promotion, FDTD authorization/execution promotion, comparison
promotion, field-transfer promotion, 3D/HPC promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/experiments/1829_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup_validation_sensitivity
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
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
field transfer ready:             false
ready for 3D/HPC:                 false
gpu priority:                     none
```

The exact action-rollup state passes. All damaged states fail.

## Interpretation

The validator accepts only the exact missing-live-artifact state and rejects
false live-file, approval, authorization, execution, comparison, field-transfer,
or 3D/HPC promotion.

## Decision

Use runs `1827-1829` as the guarded BEM stage-1 live approval action rollup
block.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup_validation_sensitivity.py
9 passed
```

Figure check:

```text
2825x850, dynamic range=255
```
