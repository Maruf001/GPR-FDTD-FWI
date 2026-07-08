# BEM Experiment 871: Panel-116 Worst-Bin Spatial Residual Anatomy Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `870` validator with damaged spatial-anatomy states and
premature promotion states.

This run reads saved artifacts only. It does not rerun BEM, FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/871_scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                 18
expected pass scenarios:               1
expected fail scenarios:               17
observed pass scenarios:               1
observed fail scenarios:               17
unexpected outcomes:                   0
damaged scenarios:                     17
scalar-gain correction promoted:       false
project FDTD comparison ready:         false
field transfer ready:                  false
3D validation ready:                   false
```

## Interpretation

The validator accepts only the exact saved spatial-anatomy state. It rejects
source-readiness damage, receiver-row damage, edge-classification damage,
worst-frequency damage, false target-passing demotion, edge-fraction damage,
single-spike promotion, scalar-gain promotion, hard per-frequency promotion,
project-FDTD promotion, field or 3D promotion, figure damage, and
script-snapshot damage.

## Decision

Use runs `869-871` as the guarded spatial residual diagnostic block for the
remaining 116-panel worst high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
2790x869, dynamic range=255
```
