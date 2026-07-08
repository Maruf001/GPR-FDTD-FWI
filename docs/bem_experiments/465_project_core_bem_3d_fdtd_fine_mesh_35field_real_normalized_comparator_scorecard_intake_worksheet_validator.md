# BEM Experiment 465: 35-Field Scorecard Intake Worksheet Validator

Date: 2026-06-29

## Purpose

Validate the run `464` intake worksheet from saved artifacts.

## Output

```text
outputs/bem_experiments/465_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                          6
validation passes:                          6
blocking failures:                          0
worksheet validation ready:                 true
worksheet rows:                             279
required real-return cells:                 1116
filled real-return cells:                   0
missing real-return cells:                  1116
hash requirements:                          558
norm requirements:                          558
preferred storage rows:                     279
real return values present:                 false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
```

## Decision

Use this validator as the artifact guard for run `464`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validator.py
5 passed
```

Figure check:

```text
3509x895, dynamic range=255
```
