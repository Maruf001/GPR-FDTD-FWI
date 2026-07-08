# BEM Experiment 394: 35-Field Real-Return Preflight Closure Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `393` artifact validator with controlled damaged variants.

This run does not stage external FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, launch GPU work, transfer to field evidence, or start 3D
validation.

## Output

```text
outputs/bem_experiments/394_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          11
expected pass:                      1
observed pass:                      1
expected failures:                  10
observed failures:                  10
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 392:              true
rejects damaged variants:           true
action groups:                      4
required external files:            3
required blocking metadata fields:  34
receiver-aperture addendum fields:  5
real comparison ready:              false
3D validation ready:                false
GPU/HPC ready:                      false
```

## Interpretation

The validator accepts the exact run `392` closure plan and rejects damaged
variants for count drift, action-row drift, source-file promotion, downstream
promotion, figure-validation drift, and script-snapshot drift.

## Decision

Use runs `392-394` as the guarded 35-field BEM/FDTD preflight closure block.
Real comparison remains blocked until target frequency bins, background
frequency bins, and the 34-field blocking metadata ledger are returned and pass
the preflight.

## Validation

Focused sensitivity test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_closure_plan_validation_sensitivity.py
2 passed
```

Figure validation:

```text
3365x891, dynamic range=255
```
