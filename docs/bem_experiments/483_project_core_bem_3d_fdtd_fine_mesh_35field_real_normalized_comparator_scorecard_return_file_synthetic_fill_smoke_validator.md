# BEM Experiment 483: Synthetic Return-File Fill Smoke Validator

Date: 2026-06-29

## Purpose

Validate run `482` from saved artifacts.

## Output

```text
outputs/bem_experiments/483_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                              6
validation checks passed:                       6
blocking failures:                              0
synthetic fill-smoke validation ready:          true
synthetic return files:                         4
filled synthetic entries:                       1116
scorecard rows:                                 279
source-hash entries:                            558
scattered-norm entries:                         558
synthetic return values are evidence:           false
real return files present:                      false
real BEM/FDTD comparison ready:                 false
3D validation ready:                            false
GPU/HPC ready:                                  false
field transfer ready:                           false
field FWI ready:                                false
```

## Interpretation

The validator confirms the run `482` counts, file keys, fill flags, hash
syntax, finite norm values, scorecard merge, downstream blocks, figure, and
script snapshots.

## Decision

Use this validator as the artifact guard for run `482`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_validator.py
4 passed
```

Figure check:

```text
2897x860, dynamic range=255
```
