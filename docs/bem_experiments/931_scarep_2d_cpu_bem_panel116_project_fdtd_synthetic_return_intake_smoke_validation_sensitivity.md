# BEM Experiment 931: Panel-116 Project-FDTD Synthetic Return Intake Smoke Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `930` synthetic return-intake smoke validator.

This run checks that the validator accepts only the exact synthetic-smoke state
and rejects damaged rows, missing synthetic provenance, false real-evidence
promotion, real-return acceptance promotion, FDTD execution promotion,
BEM/FDTD comparison promotion, field-transfer promotion, 3D promotion,
GPU-priority promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/931_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             19
expected pass scenarios:               1
expected fail scenarios:               18
observed pass scenarios:               1
observed fail scenarios:               18
unexpected outcomes:                   0
damaged scenarios:                     18
damaged scenarios rejected:            18
receiver-frequency rows:               325
synthetic return rows:                 325
real evidence rows:                    0
real return accepted:                  false
real BEM/FDTD comparison completed:    false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

Rejected damaged states include:

```text
smoke-not-ready state
row removal
receiver-index damage
complex-value damage
solver-provenance damage
synthetic-label damage
real-evidence promotion
real-return acceptance promotion
smoke-gate removal
smoke-gate failure
FDTD authorization promotion
FDTD execution promotion
BEM/FDTD comparison promotion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The synthetic-smoke validator is fail-closed. It accepts the exact synthetic
schema-smoke state and rejects every tested damaged or prematurely promoted
state.

## Decision

Use runs `930-931` as the guarded validation block for the synthetic return
intake smoke. Keep real BEM/FDTD comparison blocked until accepted real FDTD
return rows replace the synthetic rows.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke_validator.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke_validation_sensitivity.py
12 passed
```

Figure check:

```text
3221x888, dynamic range=255
```
