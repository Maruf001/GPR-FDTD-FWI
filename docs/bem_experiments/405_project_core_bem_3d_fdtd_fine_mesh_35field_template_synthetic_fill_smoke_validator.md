# BEM Experiment 405: 35-Field Template Synthetic Fill Smoke Validator

Date: 2026-06-29

## Purpose

Validate the saved run `404` synthetic template-fill smoke from artifacts.

This run does not stage real returned FDTD files, run a real BEM/FDTD
comparison, calibrate thresholds, transfer to field evidence, launch GPU work,
or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/405_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_validator
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
synthetic fill validation ready:     true
frequency rows filled:               558
frequency component cells filled:    3348
metadata fields:                     35
preflight checks:                    25
synthetic packet preflight ready:    true
synthetic packet is evidence:        false
real comparison ready:               false
3D validation claim ready:           false
GPU/HPC ready:                       false
```

The validator confirms fill counts, preflight rows, synthetic packet files,
target/background hashes in the metadata ledger, non-evidence status, figure
validation, and script snapshots.

## Decision

Use this validator as the artifact guard for run `404`. Sensitivity hardening
remains required before closing the synthetic-fill smoke block.

## Validation

Focused validator test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_validator.py
2 passed
```

Figure validation:

```text
3437x893, dynamic range=255
```
