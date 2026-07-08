# BEM Experiment 385: Fine-Mesh Receiver-Aperture Metadata Addendum Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `384` receiver-aperture metadata addendum validator with
controlled damaged variants.

## Output

```text
outputs/bem_experiments/385_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validation_sensitivity
```

## Result

```text
scenarios:                                 14
expected pass scenarios:                   1
observed pass scenarios:                   1
expected failure scenarios:                13
observed failure scenarios:                13
unexpected outcomes:                       0
sensitivity ready:                         true
validator accepts exact run 383:           true
validator rejects damaged variants:        true
base metadata fields:                      30
receiver-aperture addendum fields:         5
full metadata fields:                      35
blocking metadata fields:                  34
receiver-aperture metadata required:       true
receiver-aperture operator required:       true
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
```

The damaged variants cover count drift, missing aperture rows, template drift,
sensitivity-evidence drift, metadata/operator removal, downstream promotion,
figure drift, and script-snapshot drift.

## Decision

Use runs `383-385` as the guarded receiver-aperture metadata-addendum block
before refreshing any real-return preflight.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validator.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validation_sensitivity.py

10 passed
```

Figure check:

```text
3653x913, dynamic range=255
```
