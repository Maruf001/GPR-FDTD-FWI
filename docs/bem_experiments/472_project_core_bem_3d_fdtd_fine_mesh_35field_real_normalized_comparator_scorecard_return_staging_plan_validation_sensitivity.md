# BEM Experiment 472: 35-Field Scorecard Return Staging Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `471` validator with controlled damage to staging counts,
stage grouping, action ordering, dependency edges, downstream states, figure
validation, and script snapshots.

## Output

```text
outputs/bem_experiments/472_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       22
expected passes:                             1
observed passes:                             1
expected failures:                           21
observed failures:                           21
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 470:             true
validator rejects damaged variants:          true
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Decision

Use runs `470-472` as the guarded BEM scorecard return staging-plan block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_validation_sensitivity.py
3 passed
```

Figure check:

```text
3401x906, dynamic range=255
```
