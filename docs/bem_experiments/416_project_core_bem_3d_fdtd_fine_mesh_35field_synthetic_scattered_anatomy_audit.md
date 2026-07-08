# BEM Experiment 416: 35-Field Synthetic Scattered Anatomy Audit

Date: 2026-06-29

## Purpose

Analyze the synthetic target-minus-background scattered table produced by run
`410`.

This is a consumer-diagnostic audit only. It does not create measured evidence,
run a real BEM/FDTD comparison, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/416_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_frequency_anatomy.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_receiver_anatomy.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_component_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_top_scattered_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit.png
```

## Result

```text
scattered anatomy ready:           true
receiver count:                    31
frequency count:                   9
scattered rows:                    279
scattered component cells:         1674
dominant component:                ez
dominant component energy fraction:0.6703296703296703
peak receiver index:               30
peak receiver y:                   0.08 m
peak frequency:                    3.0 GHz
peak scattered norm:               1.7743269146355192
edge-to-edge peak norm ratio:      31.000000000000004
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Interpretation

The synthetic scattered table is internally structured rather than random. In
this synthetic fill, scattered norm increases monotonically with frequency and
receiver index. The strongest row is receiver `30` at `3 GHz`, and the `ez`
component carries the largest energy fraction.

This is useful for designing future real-return acceptance checks, but it is
not evidence that a real BEM/FDTD comparison passes.

## Decision

Use this audit to understand the synthetic packet consumer output. Keep real
comparison, 3D validation, GPU/HPC, field transfer, and field FWI blocked until
real returned FDTD files replace the synthetic packet.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_anatomy_audit.py
4 passed
```

Figure check:

```text
3221x880, dynamic range=255
```
