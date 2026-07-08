# BEM Experiment 876: Panel-116 Worst-Bin Aperture Complex-Bias Model Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `875` aperture complex-bias model scorecard from
artifacts.

This validator does not rerun BEM, FDTD, field processing, 3D/HPC work, or GPU
kernels.

## Output

```text
outputs/bem_experiments/876_scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard_validator
```

## Result

```text
validation checks:                      6
passed checks:                          6
failed checks:                          0
model rows:                             3
receiver rows:                          13
frequency:                              2.3125 GHz
target relative L2:                     0.001
uncorrected relative L2:                0.002030466081391074
best in-sample model:                   quadratic_aperture_complex_bias
best in-sample relative L2:             0.0018381250513289863
best in-sample reduction:               0.0947275267609073
best leave-one-out model:               constant_complex_bias
best leave-one-out relative L2:         0.0020966945192620154
best leave-one-out reduction:           -0.032617357402773446
any in-sample model passes target:      false
any leave-one-out model passes target:  false
all leave-one-out models worse:         true
smooth complex-bias repair ready:       false
project FDTD comparison ready:          false
field transfer ready:                   false
3D validation ready:                    false
```

## Interpretation

The saved complex-bias model scorecard validates as a no-repair and
no-holdout-support result.

## Decision

Use run `875` as the current smooth aperture-bias diagnostic for the worst
remaining 116-panel high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard_validator.py
3 passed
```

Figure check:

```text
2429x864, dynamic range=255
```
