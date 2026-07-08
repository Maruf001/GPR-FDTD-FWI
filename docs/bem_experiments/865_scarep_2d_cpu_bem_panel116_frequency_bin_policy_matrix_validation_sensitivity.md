# BEM Experiment 865: 116-Panel Frequency-Bin Policy Matrix Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `864` policy-matrix validator by damaging the saved run
`863` state in controlled ways.

The sensitivity set checks source-readiness damage, policy row/count damage,
frequency-bin count damage, worst-frequency damage, hard per-frequency
promotion, lower-panel promotion, project-FDTD promotion, real-3D promotion,
field-transfer/FWI promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/865_scarep_2d_cpu_bem_panel116_frequency_bin_policy_matrix_validation_sensitivity
```

## Result

```text
scenarios:                         16
expected passes:                    1
expected failures:                 15
observed passes:                    1
observed failures:                 15
unexpected outcomes:                0
damaged scenarios:                 15
damaged scenarios rejected:        15
project FDTD comparison ready:  false
real 3D validation ready:       false
field transfer ready:           false
gpu priority:                   none
```

## Decision

Use runs `863-865` as the guarded 116-panel frequency-bin policy matrix block.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_policy_matrix.py
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_policy_matrix_validator.py
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_policy_matrix_validation_sensitivity.py
8 passed
```

Figure check:

```text
2717x851, dynamic range=255
```
