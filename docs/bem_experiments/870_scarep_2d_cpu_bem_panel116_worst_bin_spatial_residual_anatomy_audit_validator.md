# BEM Experiment 870: Panel-116 Worst-Bin Spatial Residual Anatomy Validator

Date: 2026-07-01

## Purpose

Validate the saved run `869` spatial residual anatomy from artifacts.

This validator does not rerun BEM, FDTD, field processing, 3D/HPC work, or GPU
kernels.

## Output

```text
outputs/bem_experiments/870_scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit_validator
```

## Result

```text
validation checks:                      6
passed checks:                          6
failed checks:                          0
receiver rows:                          13
frequency:                              2.3125 GHz
complex relative L2 at frequency:       0.0020304660813910734
edge-quarter scan count:                8
edge-quarter residual energy fraction:  0.5923362105102755
center-half residual energy fraction:   0.40766378948972465
max/median local error ratio:           1.2785395313575958
worst scan order:                       3
edge-concentrated residual:             true
scalar-gain correction promoted:        false
project FDTD comparison ready:          false
field transfer ready:                   false
3D validation ready:                    false
```

## Interpretation

The saved spatial anatomy validates as edge-biased but not a single-receiver
spike. The diagnostic remains analytic-only and does not support project-FDTD,
field, or 3D promotion.

## Decision

Use run `869` as the current spatial diagnostic for the worst remaining
116-panel high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit_validator.py
3 passed
```

Figure check:

```text
2430x833, dynamic range=255
```
