# BEM Experiment 495: Real Return-File Filesystem Gap-Audit Validator

Date: 2026-06-29

## Purpose

Validate the saved run `494` filesystem gap audit from artifacts.

## Output

```text
outputs/bem_experiments/495_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation passes:                           5
blocking failures:                           0
filesystem gap-audit validation ready:       true
required real return files:                  4
open filesystem gaps:                        4
matching filename candidates:                8
real return-file candidates:                 0
blank-template candidates:                   4
synthetic-reference candidates:              4
accepted real files:                         0
real BEM/FDTD comparison ready:              false
```

The validator confirms that the only matching filenames are non-evidence
template and synthetic files, and that no real-return candidate is present.

## Decision

Use this validator as the artifact guard for run `494`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validator.py
4 passed
```

Figure check:

```text
2789x863, dynamic range=255
```
