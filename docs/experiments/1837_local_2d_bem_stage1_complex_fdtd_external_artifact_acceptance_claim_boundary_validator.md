# Experiment 1837: BEM Stage-1 Complex FDTD External Artifact Acceptance Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1836` external artifact acceptance claim boundary from
artifacts.

This validator does not write live approval files, write returned FDTD files,
run FDTD, compare BEM/FDTD, transfer to field, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1837_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validator_validation_rows.csv
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validator_summary.json
figures/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                    6
passed checks:                        6
failed checks:                        0
claims:                               8
guarded claims:                       3
blocked claims:                       5
required live files:                  2
present live files:                   0
accepted artifacts:                   0
FDTD producer authorized now:         false
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
3D/HPC ready:                         false
gpu priority:                         none
script snapshots:                     2
```

## Interpretation

The saved claim boundary validates as a guarded watchlist with two absent live
artifacts. All downstream execution, comparison, field-transfer, and 3D/HPC
states remain blocked.

## Decision

Use run `1837` before citing run `1836` as the current external artifact
acceptance claim boundary.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validator.py
3 passed
```

Figure check:

```text
2825x876, dynamic range=255
```
