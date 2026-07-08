# BEM Experiment 423: 35-Field Synthetic Scattered Normalization Policy Validator

Date: 2026-06-29

## Purpose

Validate run `422` from saved artifacts.

The validator checks source readiness, table shape, coefficient collapse,
raw-magnitude policy role, blocked real-pair state, figure validation, and
script snapshots.

## Output

```text
outputs/bem_experiments/423_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validator.png
```

## Result

```text
validation checks:                 6
passed checks:                     6
failed checks:                     0
normalization validation ready:    true
source policy ready:               true
scattered rows:                    279
receiver count:                    31
frequency count:                   9
raw norm span ratio:               232.50000000000006
normalized coefficient cv:         2.0884850334665626e-16
normalized coefficient range:      1.0408340855860843e-17
normalization collapses scaling:   true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Decision

Use this validator as the artifact guard for run `422`. Sensitivity testing
remains required before closing the normalization-policy block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x840, dynamic range=255
```
