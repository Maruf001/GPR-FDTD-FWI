# BEM Experiment 382: Fine-Mesh Receiver-Aperture Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `381` receiver-aperture sensitivity validator with
controlled damaged variants.

## Output

```text
outputs/bem_experiments/382_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validation_sensitivity
```

## Result

```text
scenarios:                                14
expected pass scenarios:                  1
observed pass scenarios:                  1
expected failure scenarios:               13
observed failure scenarios:               13
unexpected outcomes:                      0
sensitivity ready:                        true
validator accepts exact run 380:          true
validator rejects damaged variants:       true
finite-aperture metadata required:        true
finite-aperture operator required:        true
point receiver unconditional ready:       false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
```

The damaged variants cover source drift, count drift, point-receiver identity
drift, threshold drift, metadata/operator removal, worst-case drift, aperture
progression drift, downstream promotion, figure drift, and script-snapshot
drift.

## Decision

Use runs `380-382` as the guarded BEM receiver-aperture sensitivity block.
Future paired 3D BEM/FDTD returns must specify or match a receiver-aperture
operator before calibrated comparison or 3D validation can be claimed.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit.py
tests/test_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validator.py
tests/test_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validation_sensitivity.py

9 passed
```

Figure check:

```text
3653x912, dynamic range=255
```
