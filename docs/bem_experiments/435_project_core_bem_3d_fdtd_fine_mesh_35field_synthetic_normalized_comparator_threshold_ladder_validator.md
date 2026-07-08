# BEM Experiment 435: 35-Field Synthetic Normalized-Comparator Threshold-Ladder Validator

Date: 2026-06-29

## Purpose

Validate run `434` from saved artifacts.

The validator checks source readiness, ladder shape, pass/fail threshold split,
row-level consistency, blocked downstream states, figure validation, and script
snapshots.

## Output

```text
outputs/bem_experiments/435_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
threshold-ladder validation ready: true
scenarios:                         9
pass scenarios:                    5
fail scenarios:                    4
perturbed score rows:              2511
pass rows:                         1395
fail rows:                         1116
max passing relative residual:     9.50339903422461e-13
min failing relative residual:     1.0501746923583452e-12
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Decision

Use this validator as the artifact guard for run `434`. Sensitivity testing
remains required before closing the threshold-ladder block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validator.py
4 passed as part of the 10-test focused set
```

Figure check:

```text
2645x840, dynamic range=255
```
