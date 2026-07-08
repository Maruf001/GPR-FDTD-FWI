# BEM Experiment 447: Reference-Coefficient Precision-Budget Validator

Date: 2026-06-29

## Purpose

Validate the saved artifacts from run `446`.

## Output

```text
outputs/bem_experiments/447_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validator.png
```

## Result

```text
validation checks:                  5
validation checks passed:           5
blocking failures:                  0
precision-budget validation ready:  true
precision scenarios:                10
minimum passing significant digits: 13
maximum failing significant digits: 12
recommended significant digits:     13
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The validator confirms the exact 12-digit fail and 13-digit pass split, the
positive reference coefficient, the `1e-12` tolerance, nonblank figure output,
script snapshots, and blocked downstream states.

## Decision

Use this validator as the artifact guard for the precision-budget audit.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_validator.py
7 passed
```

Figure check:

```text
2645x834, dynamic range=255
```
