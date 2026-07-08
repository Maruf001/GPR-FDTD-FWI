# BEM Experiment 484: Synthetic Return-File Fill Smoke Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `483` validator against controlled damage to the run `482`
synthetic fill smoke.

## Output

```text
outputs/bem_experiments/484_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                         37
expected pass scenarios:                       1
observed pass scenarios:                       1
expected failure scenarios:                    36
observed failure scenarios:                    36
unexpected outcomes:                           0
validation sensitivity ready:                  true
validator accepts exact run 482:               true
validator rejects damaged variants:            true
real return files present:                     false
real BEM/FDTD comparison ready:                false
3D validation ready:                           false
GPU/HPC ready:                                 false
field transfer ready:                          false
field FWI ready:                               false
```

## Interpretation

The validator accepts the exact synthetic fill smoke and rejects damaged
variants for source-readiness drift, fill-count drift, scorecard-count drift,
hash drift, norm drift, evidence promotion, downstream promotion, figure drift,
and script-snapshot drift.

## Decision

Use runs `482-484` as the guarded synthetic return-file consumer smoke block.
This block proves the file-level handoff can be parsed and merged; it does not
create real comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validation_sensitivity.py
3 passed
```

Figure check:

```text
3761x900, dynamic range=255
```
