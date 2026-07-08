# Experiment 1823: BEM Stage-1 Complex FDTD Live Approval Parser Positive Control Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1822` validator by damaging the saved run `1821`
positive-control state in controlled ways.

The sensitivity set checks source-readiness damage, template-readiness damage,
control-file damage, parser-row damage, parser-check failure, target-field
damage, false live-root promotion, false live approval, false live acceptance,
FDTD authorization/execution promotion, comparison promotion, field/3D
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1823_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control_validation_sensitivity
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

The exact output-local parser positive-control state passes. All damaged states
fail.

## Interpretation

The validator accepts only the exact non-live positive-control state and rejects
false promotion to live approval, FDTD authorization, comparison, field
transfer, or 3D/HPC.

## Decision

Use runs `1821-1823` as the guarded parser positive-control block. Keep FDTD
execution blocked until real live approval is supplied.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control_validation_sensitivity.py
8 passed
```

Figure check:

```text
3077x849, dynamic range=255
```
