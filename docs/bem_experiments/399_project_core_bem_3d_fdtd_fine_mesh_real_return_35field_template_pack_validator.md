# BEM Experiment 399: 35-Field Real-Return Template Pack Validator

Date: 2026-06-29

## Purpose

Validate the saved run `398` template pack from artifacts.

This run does not stage returned FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, transfer to field evidence, launch GPU work, or make a
3D validation claim.

## Output

```text
outputs/bem_experiments/399_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_validator
```

## Result

```text
validation checks:                   8
passed checks:                       8
failed checks:                       0
template-pack validation ready:      true
template packet files:               3
template files written:              4
rows per frequency file:             279
blank frequency component cells:     3348
metadata fields:                     35
blocking metadata fields:            34
blank metadata values:               12
receiver-aperture addendum fields:   5
real comparison ready:               false
3D validation claim ready:           false
```

The validator confirms source identity, template inventory, non-evidence
status, target/background frequency-template schema, metadata-template fields,
blocked downstream states, figure validation, written template hashes, and
script snapshots.

## Decision

Use this validator as the artifact guard for run `398`. Sensitivity hardening
remains required before closing the template-pack block.

## Validation

Focused validator test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_validator.py
2 passed
```

Figure validation:

```text
3149x898, dynamic range=255
```
