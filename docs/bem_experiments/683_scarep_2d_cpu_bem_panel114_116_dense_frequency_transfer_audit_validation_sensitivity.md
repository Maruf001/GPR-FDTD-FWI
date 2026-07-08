# BEM Experiment 683: 114/116 Dense-Frequency Transfer Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `682` dense-frequency validator.

The validator should accept only the exact run `681` output and reject damaged
states that change source readiness, case or solve counts, frequency count,
panel set, pass counts, guard counts, minimum or guarded panel, 116-panel
error, 116-panel margin, downstream claims, figure validation, or frozen script
snapshots.

## Output

```text
outputs/bem_experiments/683_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validation_sensitivity_cases.csv
data/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   21
expected pass cases:                 1
expected fail cases:                 20
actual pass cases:                   1
actual fail cases:                   20
unexpected cases:                    0
damaged cases rejected:              true
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `681` source passes. All damaged states fail, including source
readiness damage, case or solve row removal, frequency-count damage, panel-set
damage, 114/116/128 pass-count damage, 116 guard-count damage, minimum or
guarded panel damage, 116 error or margin damage, FDTD comparison promotion,
real-3D promotion, GPU/HPC promotion, field-transfer promotion, field-FWI
promotion, figure damage, and missing script snapshots.

## Interpretation

Run `683` hardens the dense-frequency support check. The result cannot be
accepted if its grid shape, panel set, pass boundary, guard margin, claim
boundary, figure, or frozen scripts are damaged.

## Decision

Keep runs `681-683` as the dense-frequency support block for the guarded
116-panel analytic transfer policy.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validation_sensitivity.py

10 passed
```

Figure check:

```text
2572x868, dynamic range=255
```
