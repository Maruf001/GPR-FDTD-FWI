# BEM Experiment 424: 35-Field Synthetic Scattered Normalization Policy Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `423` validator with controlled damaged variants of the
run `422` normalization-policy artifacts.

## Output

```text
outputs/bem_experiments/424_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validation_sensitivity.png
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected failure scenarios:        17
observed pass scenarios:           1
observed failure scenarios:        17
unexpected outcomes:               0
normalization sensitivity ready:   true
validator accepts exact run 422:   true
validator rejects damaged variants:true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The validator accepts the exact run `422` normalization policy and rejects
controlled damage to readiness, counts, coefficient spread, policy roles,
downstream state, figure validation, and script snapshots.

## Decision

Use runs `422-424` as the guarded BEM synthetic scattered normalization-policy
block. Keep real BEM/FDTD comparison, 3D validation, GPU/HPC work, field
transfer, and field FWI blocked until real returned FDTD files replace the
synthetic packet.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x884, dynamic range=255
```
