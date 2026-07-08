# BEM Experiment 127: Fine-Mesh Comparator Threshold Boundary Audit

Date: 2026-06-27

## Purpose

Interpret the provisional `0.1` relative-L2 comparator threshold for the
preferred nine-frequency fine-mesh BEM/FDTD comparison path.

Run `126` showed which mismatch modes pass or fail. This run turns that into
tested boundary brackets for scattered-field amplitude error, scattered-field
phase rotation, and background-only incident-field bias.

This is a synthetic threshold audit. It does not install real FDTD returns, run
local 3D FDTD, make a 3D validation claim, launch GPU/HPC work, run field FWI,
or train neural networks.

## Output

```text
outputs/bem_experiments/127_project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_sweep_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_metric_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_validation_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_audit_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_audit.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_COMPARATOR_THRESHOLD_BOUNDARY_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
sweep point count:               37
frequency count:                 9
receiver count:                  31
rows per sweep point:            279
target synthetic rows:           10323
background synthetic rows:       10323
validation checks:               666
validation failed checks:        0
tested pass points:              17
tested fail points:              20
threshold boundary audit ready:  true
real FDTD data ready:            false
real BEM/FDTD comparison ready:  false
3D validation claim ready:       false
gpu/hpc ready:                   false
```

Boundary brackets:

| Sweep axis | Units | Largest tested pass | Smallest tested fail |
| --- | --- | ---: | ---: |
| background_only_bias_fraction | fraction of incident/background field | 0.0005 | 0.001 |
| scattered_amplitude_delta | fractional scattered-field amplitude delta | 0.095 | 0.105 |
| scattered_phase_degrees | degrees | 5.7 | 6.0 |

## Interpretation

For this fine-mesh reference, the `0.1` relative-L2 line is strict:

- global scattered-field amplitude errors are bracketed between 9.5% pass and
  10.5% fail;
- scattered-field phase rotation is bracketed between 5.7 degrees pass and
  6.0 degrees fail;
- background-only incident-field bias is bracketed between 0.0005 pass and
  0.001 fail as a fraction of the incident/background field.

The background-only bias boundary is much smaller than the scattered-field
amplitude boundary because the incident/background field can be much larger
than the scattered field.

## Decision

Use these boundary brackets when interpreting future real BEM/FDTD differences.
The threshold remains an investigation gate, not a publication validation
claim. Real comparison remains blocked until external FDTD target, background,
and metadata files pass the real preflight.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_audit.png
2500x1423, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_audit.py
sha256=bfa1b84d69bd4fa469563ba273647c9baea4760e65ee40c639bc5082238bd4e9

tests/test_project_core_bem_3d_fdtd_fine_mesh_comparator_threshold_boundary_audit.py
sha256=3b1a3b0717c006d784d53a113c7f235137e66522b5be27e68221c2df6ab108ae
```
