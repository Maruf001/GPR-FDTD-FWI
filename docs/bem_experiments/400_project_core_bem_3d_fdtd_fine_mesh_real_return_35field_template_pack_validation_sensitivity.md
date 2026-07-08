# BEM Experiment 400: 35-Field Real-Return Template Pack Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `399` validator with controlled damaged variants of the
run `398` template pack.

This run does not stage returned FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, transfer to field evidence, launch GPU work, or make a
3D validation claim.

## Output

```text
outputs/bem_experiments/400_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_validation_sensitivity
```

## Result

```text
scenarios:                           12
expected pass:                       1
observed pass:                       1
expected failures:                   11
observed failures:                   11
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 398:               true
rejects damaged variants:            true
template packet files:               3
rows per frequency file:             279
metadata fields:                     35
blocking metadata fields:            34
real comparison ready:               false
3D validation claim ready:           false
```

The exact run `398` artifacts pass. Eleven damaged variants fail as expected
for source-label drift, template-count drift, false evidence promotion,
frequency-row drift, blank-component count drift, metadata-field drift,
receiver-aperture key removal, downstream promotion, figure drift, script
snapshot drift, and written-template hash drift.

## Decision

Use runs `398-400` as the guarded non-evidence 35-field BEM/FDTD
return-template block.

## Validation

Focused sensitivity test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_validation_sensitivity.py
2 passed
```

Combined focused template-pack tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_validator.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_validation_sensitivity.py
7 passed
```

Figure validation:

```text
3401x886, dynamic range=255
```
