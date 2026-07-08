# BEM Experiment 418: 35-Field Synthetic Scattered Anatomy Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `417` validator with controlled damaged variants of the
run `416` scattered-anatomy audit.

## Output

```text
outputs/bem_experiments/418_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validation_sensitivity.png
```

## Result

```text
scenarios:                         20
expected pass scenarios:           1
expected failure scenarios:        19
observed pass scenarios:           1
observed failure scenarios:        19
unexpected outcomes:               0
scattered anatomy sensitivity ready:true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The validator accepts the exact run `416` anatomy audit and rejects controlled
damage to readiness, table shape, monotonicity, component dominance, peak
location, evidence promotion, figure validation, and script snapshots.

## Decision

Use runs `416-418` as the guarded synthetic scattered-anatomy block. Keep real
comparison, 3D validation, GPU/HPC, field transfer, and field FWI blocked until
real returned FDTD files replace the synthetic packet.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x887, dynamic range=255
```
