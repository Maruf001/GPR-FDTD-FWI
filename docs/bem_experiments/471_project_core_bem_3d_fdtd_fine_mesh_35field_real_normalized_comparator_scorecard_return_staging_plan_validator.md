# BEM Experiment 471: 35-Field Scorecard Return Staging Plan Validator

Date: 2026-06-29

## Purpose

Validate the run `470` return staging plan from saved artifacts.

## Output

```text
outputs/bem_experiments/471_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation passes:                           5
blocking failures:                           0
staging-plan validation ready:               true
required real-return cells:                  1116
stage actions:                               6
dependency edges:                            7
source-hash stage cells:                     558
scattered-norm stage cells:                  558
filled real-return cells:                    0
missing real-return cells:                   1116
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Decision

Use this validator as the artifact guard for run `470`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validator.py
5 passed
```

Figure check:

```text
2825x899, dynamic range=255
```
