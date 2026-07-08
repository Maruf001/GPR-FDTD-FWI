# BEM Experiment 381: Fine-Mesh Receiver-Aperture Sensitivity Validator

Date: 2026-06-29

## Purpose

Validate the saved run `380` receiver-aperture sensitivity audit from
artifacts.

## Output

```text
outputs/bem_experiments/381_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validator
```

## Result

```text
validation checks:                        8
passed checks:                            8
failed checks:                            0
validation ready:                         true
source frequencies:                       9
source receiver count per frequency:      31
source aperture cases:                    5
source aperture comparisons:              45
source max 3-sample relative L2:          0.08009547612144642
source max 9-sample relative L2:          0.44166920910128993
source worst frequency:                   3.0 GHz
source worst aperture sample count:       9
finite-aperture metadata required:        true
finite-aperture operator required:        true
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
```

The validator checks source identity, row counts, point-receiver identity,
the first aperture crossing the 5% threshold, high-frequency worst-case
stability, monotonic aperture-growth behavior, blocked downstream states,
figure validation, and script snapshots.

## Decision

Use run `381` as the validator for the run `380` receiver-aperture sensitivity
result. Sensitivity hardening is required before closing the block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validator.py
3 passed
```

Figure check:

```text
3545x929, dynamic range=255
```
