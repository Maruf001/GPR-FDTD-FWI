# BEM Experiment 864: 116-Panel Frequency-Bin Policy Matrix Validator

Date: 2026-07-01

## Purpose

Validate the saved run `863` policy matrix.

The validator checks source readiness, five policy rows, exactly one accepted
policy, four blocked policies, the preserved high-band bin diagnostic counts,
blocked downstream claims, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/864_scarep_2d_cpu_bem_panel116_frequency_bin_policy_matrix_validator
```

## Result

```text
validation checks:                  5
checks passed:                      5
checks failed:                      0
policy rows:                        5
accepted policies:                  1
blocked policies:                   4
high-band bins:                    27
above-target bins:                  5
worst frequency GHz:           2.3125
project FDTD comparison ready:  false
real 3D validation ready:       false
field transfer ready:           false
```

## Decision

Use run `863` as the current policy matrix. Do not promote hard
per-frequency, lower-panel, project-FDTD, field, or 3D claims.

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
2105x855, dynamic range=255
```
