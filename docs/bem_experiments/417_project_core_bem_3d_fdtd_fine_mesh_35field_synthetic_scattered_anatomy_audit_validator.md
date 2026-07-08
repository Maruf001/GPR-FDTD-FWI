# BEM Experiment 417: 35-Field Synthetic Scattered Anatomy Audit Validator

Date: 2026-06-29

## Purpose

Validate run `416` from saved artifacts.

The validator checks source readiness, table shape, monotonic frequency and
receiver norms, dominant component identity, peak location, blocked downstream
claims, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/417_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validator.png
```

## Result

```text
validation checks:                 6
passed checks:                     6
failed checks:                     0
scattered anatomy validation ready:true
receiver count:                    31
frequency count:                   9
dominant component:                ez
peak receiver index:               30
peak frequency:                    3.0 GHz
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Decision

Use this as the positive validator for run `416`. Sensitivity testing remains
required before closing the scattered-anatomy block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```
