# BEM Experiment 384: Fine-Mesh Receiver-Aperture Metadata Addendum Validator

Date: 2026-06-29

## Purpose

Validate the saved run `383` receiver-aperture metadata addendum from
artifacts.

## Output

```text
outputs/bem_experiments/384_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validator
```

## Result

```text
validation checks:                         7
passed checks:                             7
failed checks:                             0
validation ready:                          true
source base metadata fields:               30
source aperture addendum fields:           5
source full metadata fields:               35
source blocking metadata fields:           34
source max 3-sample relative L2:           0.08009547612144642
source max 9-sample relative L2:           0.44166920910128993
receiver-aperture metadata required:       true
receiver-aperture operator required:       true
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
```

The validator checks source identity, metadata field counts, aperture
requirement rows, aperture template values, aperture sensitivity evidence,
blocked downstream states, figure validation, and script snapshots.

## Decision

Use run `384` as the validator for the run `383` receiver-aperture metadata
addendum. Sensitivity hardening is required before refreshing a preflight.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validator.py
3 passed
```

Figure check:

```text
3365x893, dynamic range=255
```
