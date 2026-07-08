# BEM Experiment 406: 35-Field Template Synthetic Fill Smoke Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `405` validator with controlled damaged variants of the
run `404` synthetic-fill smoke.

This run does not stage real returned FDTD files, run a real BEM/FDTD
comparison, calibrate thresholds, transfer to field evidence, launch GPU work,
or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/406_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_validation_sensitivity
```

## Result

```text
scenarios:                           13
expected pass:                       1
observed pass:                       1
expected failures:                   12
observed failures:                   12
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 404:               true
rejects damaged variants:            true
frequency rows filled:               558
frequency component cells filled:    3348
metadata fields:                     35
preflight checks:                    25
synthetic packet is evidence:        false
real comparison ready:               false
3D validation claim ready:           false
GPU/HPC ready:                       false
```

The exact run `404` artifacts pass. Twelve damaged variants fail as expected
for source-label drift, fill-count drift, preflight-row drift, packet-root
drift, metadata-hash drift, false evidence promotion, downstream promotion,
figure-validation drift, and script-snapshot drift.

## Decision

Use runs `404-406` as the guarded synthetic consumer-smoke block for the
35-field BEM/FDTD return-template pack.

## Validation

Focused sensitivity test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_validation_sensitivity.py
2 passed
```

Combined focused synthetic-fill tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_validator.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_validation_sensitivity.py
8 passed
```

Figure validation:

```text
3509x891, dynamic range=255
```
