# Experiment 1832: BEM Stage-1 Complex FDTD External Return Hygiene Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1831` validator with damaged or prematurely promoted
states.

## Output

```text
outputs/experiments/1832_local_2d_bem_stage1_complex_fdtd_external_return_hygiene_audit_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                14
expected pass scenarios:              1
expected fail scenarios:              13
observed pass scenarios:              1
observed fail scenarios:              13
unexpected outcomes:                  0
damaged scenarios:                    13
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
3D/HPC ready:                         false
```

## Decision

The validator accepts only the exact clean, non-authorizing state and rejects
false approval, false partial-return, FDTD execution, comparison, 3D, figure,
and script-snapshot promotion states. Use runs `1830-1832` as the guarded
no-data hygiene block for the BEM stage-1 2D external-return paths.

## Validation

Figure check:

```text
2646x849, dynamic range=255
```
