# BEM Experiment 448: Reference-Coefficient Precision-Budget Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `447` validator against controlled damage to the
precision-budget artifacts.

## Output

```text
outputs/bem_experiments/448_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validation_sensitivity.png
```

## Result

```text
scenarios:                          22
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         21
observed failure scenarios:         21
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 446:    true
validator rejects damaged variants: true
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The damaged variants cover readiness drift, scenario-count drift, pass/fail
count drift, minimum/maximum/recommended significant-digit drift, false
12-digit and 13-digit threshold decisions, tolerance drift, zero reference
coefficient, downstream promotion, blank figures, and missing script snapshots.

## Decision

Use runs `446-448` as the guarded BEM reference-coefficient precision-budget
block. Keep real comparison, 3D validation, GPU/HPC, field transfer, and field
FWI blocked until real returned BEM/FDTD values and source hashes exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validator.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validation_sensitivity.py
10 passed
```

Figure check:

```text
3563x891, dynamic range=255
```
