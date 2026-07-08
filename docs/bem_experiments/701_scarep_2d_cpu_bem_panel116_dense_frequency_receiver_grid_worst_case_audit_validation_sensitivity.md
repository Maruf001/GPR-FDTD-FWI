# BEM Experiment 701: Dense-Frequency 116-Panel Receiver-Grid Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `700` validator by confirming that it accepts the exact run
`699` dense-frequency audit and rejects damaged alternatives.

This is a CPU-only validation-sensitivity wrapper around saved artifacts. It
does not run new BEM solves, compare against project FDTD outputs, run 3D
Maxwell BEM, launch GPU/HPC work, or promote field transfer.

## Output

```text
outputs/bem_experiments/701_scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validation_sensitivity_case_rows.csv
data/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                         16
expected pass cases:                       1
expected fail cases:                       15
actual pass cases:                         1
actual fail cases:                         15
unexpected cases:                          0
damaged cases:                             15
validation sensitivity ready:              true
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
```

The damaged cases cover source readiness, scan rows, solve rows, scan-count
metadata, frequency-count metadata, target identity, 116-panel pass status,
target-margin status, project-FDTD promotion, 3D promotion, GPU/HPC promotion,
field promotion, figure damage, and missing script snapshots.

## Interpretation

The validator accepts only the exact dense-frequency audit and rejects all
damaged states tested here. This hardens the claim boundary around run `699`:
the result is valid for analytic BEM dense-frequency receiver-grid robustness,
not for project-FDTD comparison, real 3D validation, GPU/HPC escalation, or
field transfer.

## Decision

Keep run `699` as analytic-only dense-frequency support for the guarded
116-panel policy.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit.py
tests/test_scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validation_sensitivity.py
9 passed
```

Figure check:

```text
2645x850, dynamic range=255
```

