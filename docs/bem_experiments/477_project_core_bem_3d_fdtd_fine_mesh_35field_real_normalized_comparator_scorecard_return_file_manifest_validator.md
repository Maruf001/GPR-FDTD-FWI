# BEM Experiment 477: 35-Field Return-File Manifest Validator

Date: 2026-06-29

## Purpose

Validate the saved run `476` return-file manifest from artifacts.

## Output

```text
outputs/bem_experiments/477_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           6
validation checks passed:                    6
blocking failures:                           0
return-file manifest validation ready:       true
required files:                              4
template entries:                            1116
required real input cells:                   1116
source-hash template entries:                558
scattered-norm template entries:             558
real return files present:                   false
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field transfer ready:                        false
field FWI ready:                             false
```

The validator confirms the four expected file targets, 279 entries per file,
the 31-by-nine receiver/frequency grid, blank template values, template hashes,
figure validation, and script snapshots.

## Decision

Use this validator as the artifact guard for run `476`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validator.py
6 passed
```

Figure check:

```text
2825x859, dynamic range=255
```
