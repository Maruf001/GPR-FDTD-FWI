# BEM Experiment 930: Panel-116 Project-FDTD Synthetic Return Intake Smoke Validator

Date: 2026-07-01

## Purpose

Validate the run `924` synthetic return-intake smoke from saved artifacts.

This run confirms that the synthetic file exercises the receiver-frequency
schema and solver-provenance columns, while preserving the boundary that it is
not real FDTD evidence and cannot support a real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/930_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke_validator
```

## Result

```text
validation checks:                     6
passed checks:                         6
failed checks:                         0
receiver-frequency rows:               325
complex FDTD-value rows:               325
solver-provenance rows:                325
synthetic return rows:                 325
real evidence rows:                    0
schema smoke passed:                   true
real return accepted:                  false
FDTD execution authorized now:         false
FDTD executed now:                     false
real BEM/FDTD comparison completed:    false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

## Interpretation

The synthetic return file is useful as a schema and downstream-consumer smoke.
It is not measured FDTD output and does not change the real comparison state.

## Decision

Keep the real BEM/FDTD comparison blocked until accepted real FDTD return rows
replace the synthetic smoke rows.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke_validator.py
9 passed
```

Figure check:

```text
2681x858, dynamic range=255
```
