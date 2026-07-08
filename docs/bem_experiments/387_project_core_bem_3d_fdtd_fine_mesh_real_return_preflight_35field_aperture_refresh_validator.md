# BEM Experiment 387: 35-Field Real-Return Preflight Validator

Date: 2026-06-29

## Purpose

Validate the saved run `386` aperture-aware BEM/FDTD real-return preflight from
artifacts.

Run `386` refreshed the preferred real-return gate after the receiver-aperture
sensitivity result. This validator checks whether the saved gate is internally
consistent before treating it as the current handoff contract.

## Output

```text
outputs/bem_experiments/387_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
metadata fields:                    35
blocking metadata fields:           34
fine-mesh addendum fields:          5
receiver-aperture addendum fields:  5
preflight checks:                   10
blocking failures:                  10
target file present:                false
background file present:            false
metadata file present:              false
BEM reference export ready:          true
synthetic sensitivity ready:         true
receiver-aperture metadata required: true
receiver-aperture operator required: true
real comparison ready:              false
3D validation ready:                false
layered 3D model ready:             false
field FWI ready:                    false
GPU/HPC ready:                      false
```

The validator checks source identity, frequency/receiver counts, the 35-field
metadata contract, the three expected return files, the ten fail-closed
preflight rows, aperture metadata/operator requirements, downstream blocked
states, figure health, and script snapshots.

## Interpretation

The refreshed preflight is internally consistent. It correctly fails closed:
the BEM reference, synthetic sensitivity, and aperture metadata guards are
available, but the real target frequency-bin file, background frequency-bin
file, and metadata ledger are absent.

## Decision

Use run `387` as the validator for run `386`. Sensitivity hardening remains
required before closing the refreshed preflight block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh_validator.py
4 passed
```

Figure check:

```text
3545x931, dynamic range=255
```
