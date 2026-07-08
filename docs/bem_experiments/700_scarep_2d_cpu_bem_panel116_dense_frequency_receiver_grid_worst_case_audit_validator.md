# BEM Experiment 700: Dense-Frequency 116-Panel Receiver-Grid Audit Validator

Date: 2026-06-30

## Purpose

Validate run `699`, which repeated the controlling larger-radius analytic BEM
receiver-grid check for 116 panels on a denser 49-frequency grid.

This is a CPU-only validation wrapper around saved run `699` artifacts. It does
not run new BEM solves, compare against project FDTD outputs, run 3D Maxwell
BEM, launch GPU/HPC work, or promote field transfer.

## Output

```text
outputs/bem_experiments/700_scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validator_summary.json
figures/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
scan rows:                                 3
solve rows:                                3
frequency count:                           49
116-panel pass count:                      3
116-panel max high-band relative L2:       0.0007643703508458867
116-panel minimum margin to target:        0.00023562964915411328
dense-frequency validation ready:          true
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
```

The checks cover source readiness, dense scan/solve shape, target-case lock,
116-panel pass status, analytic-only claim boundary, figure output, and frozen
script snapshots.

## Interpretation

Run `699` validates cleanly as an analytic-only dense-frequency
receiver-grid robustness result. It supports the guarded 116-panel BEM policy
under the 49-frequency aggregate metric while preserving all project-FDTD, 3D,
GPU/HPC, field-transfer, and field-FWI blockers.

## Decision

Use run `699` as dense-frequency receiver-grid support for the guarded
116-panel analytic policy. Do not promote this result to project-FDTD, 3D, or
field evidence.

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
2357x836, dynamic range=255
```

