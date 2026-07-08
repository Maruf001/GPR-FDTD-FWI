# BEM Experiment 404: 35-Field Template Synthetic Fill Smoke

Date: 2026-06-29

## Purpose

Test whether the 35-field BEM/FDTD return templates from run `398` can be
filled and parsed by the existing preflight without using the real pending
external-return folder.

This run uses deterministic synthetic fill values only. It does not stage real
returned FDTD files, run a real BEM/FDTD comparison, calibrate thresholds,
transfer to field evidence, launch GPU work, or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/404_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke
```

Key artifacts:

```text
synthetic_packet_root/project_core_bem_3d_fdtd_fine_mesh_target_frequency_bins.csv
synthetic_packet_root/project_core_bem_3d_fdtd_fine_mesh_background_frequency_bins.csv
synthetic_packet_root/project_core_bem_3d_fdtd_external_return_metadata.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_preflight_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke.png
```

## Result

```text
synthetic template-fill smoke ready:       true
synthetic packet files:                    3
frequency rows filled:                     558
frequency component cells filled:          3348
blank component cells after fill:          0
nonfinite component cells after fill:      0
metadata fields:                           35
blank metadata values after fill:          0
preflight checks:                          25
preflight passes:                          25
preflight failures:                        0
synthetic packet preflight ready:          true
synthetic packet is evidence:              false
real external FDTD data ready:             false
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
```

## Interpretation

The handoff template is internally usable: when copied into an isolated
synthetic packet and filled with finite values, all frequency-bin and metadata
preflight checks pass.

This is a consumer smoke only. Passing this run means the template structure is
fillable and machine-checkable. It does not mean real FDTD data exist.

## Decision

Use run `404` as a template-consumer smoke for the 35-field handoff. Keep real
BEM/FDTD comparison, 3D validation, field transfer, field FWI, and GPU/HPC
blocked until real target, background, and metadata files replace the synthetic
packet.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_template_synthetic_fill_smoke.py
4 passed
```

Figure validation:

```text
3436x880, dynamic range=255
```
