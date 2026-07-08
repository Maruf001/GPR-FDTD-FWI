# Experiment 1826: BEM Stage-1 Complex FDTD Live Approval Acceptance Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1825` validator by damaging the saved run `1824`
fail-closed live approval gate in controlled ways.

The sensitivity set checks source-readiness damage, gate-count damage,
gate-pass promotion, live-file promotion, accepted-approval promotion, FDTD
authorization/execution promotion, comparison promotion, field-transfer
promotion, 3D/HPC promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1826_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate_validation_sensitivity
```

## Result

```text
scenarios:                         13
expected passes:                    1
expected failures:                 12
observed passes:                    1
observed failures:                 12
unexpected outcomes:                0
damaged scenarios:                 12
damaged scenarios rejected:        12
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
field transfer ready:             false
ready for 3D/HPC:                 false
gpu priority:                     none
```

The exact absent-live-approval fail-closed state passes. All damaged states
fail.

## Interpretation

The validator accepts only the exact fail-closed state and rejects false live
approval, authorization, execution, comparison, field transfer, or 3D/HPC
promotion.

## Decision

Use runs `1824-1826` as the guarded live approval acceptance gate block.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate_validation_sensitivity.py
8 passed
```

Figure check:

```text
2645x848, dynamic range=255
```
