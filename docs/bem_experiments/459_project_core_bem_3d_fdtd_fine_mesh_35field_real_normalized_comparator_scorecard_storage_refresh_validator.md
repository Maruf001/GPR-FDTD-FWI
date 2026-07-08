# BEM Experiment 459: Real Normalized-Comparator Scorecard Storage Refresh Validator

Date: 2026-06-29

## Purpose

Validate the storage-refreshed scorecard template from run `458` using saved
artifacts.

## Output

```text
outputs/bem_experiments/459_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                             6
validation checks passed:                      6
blocking failures:                             0
scorecard storage-refresh validation ready:    true
scorecard rows:                                279
preferred-storage rows:                        279
minimum-safe-digit rows:                       279
filled real input cells:                       0
filled generated score cells:                  0
template rows currently evidence:              0
real BEM/FDTD comparison ready:                false
3D validation ready:                           false
GPU/HPC ready:                                 false
field FWI ready:                               false
```

The validator confirms the grid shape, coefficient storage coverage, blank
real-return cells, blank generated score cells, non-evidence status, downstream
blocked states, figure, and script snapshots.

## Decision

Use this validator as the artifact guard for run `458`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_validator.py
5 passed
```

Figure check:

```text
2609x832, dynamic range=255
```
