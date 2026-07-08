# BEM Experiment 460: Real Normalized-Comparator Scorecard Storage Refresh Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `459` validator against controlled damage to the
storage-refreshed scorecard template.

## Output

```text
outputs/bem_experiments/460_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                         30
expected pass scenarios:                       1
observed pass scenarios:                       1
expected failure scenarios:                    29
observed failure scenarios:                    29
unexpected outcomes:                           0
validation sensitivity ready:                  true
validator accepts exact run 458:               true
validator rejects damaged variants:            true
real BEM/FDTD comparison ready:                false
3D validation ready:                           false
GPU/HPC ready:                                 false
field FWI ready:                               false
```

The validator accepts the exact run `458` artifact set and rejects controlled
damage to source readiness, row/grid counts, storage digits/text, blank return
cells, generated score cells, evidence flags, downstream states, figure
validation, and script snapshots.

## Decision

Use runs `458-460` as the guarded storage-refreshed real-return scorecard
template block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x884, dynamic range=255
```
