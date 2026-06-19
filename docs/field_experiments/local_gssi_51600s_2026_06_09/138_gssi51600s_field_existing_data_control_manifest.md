# Field Experiment 138: Existing-Data Control Manifest

Date: 2026-06-18

## Purpose

Map the existing local GSSI 51600S archive against the run `137` controlled
acquisition requirements. This separates useful measured-field QC evidence from
missing controls needed before field inversion, heavy GPU work, or 3D/HPC field
claims could be defensible.

This is CPU-only synthesis of saved CSV/JSON artifacts. It does not run FDTD,
FWI, GPU kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/138_gssi51600s_field_existing_data_control_manifest
```

Key artifacts:

```text
data/field_existing_data_control_manifest_summary.json
data/field_existing_data_control_manifest_rows.csv
data/field_existing_data_control_manifest_gates.csv
data/field_existing_data_evidence_inventory.csv
```

## Result

```text
raw DZT files:                         4
inventory profile count:               4
total parsed profile length:           7.215945 m
geometry type:                         independent_2d_line_profiles
current archive is 3D survey:          false
requirements mapped:                   9
must-have requirements:                5
satisfied must-have requirements:      0
partial-QC must-have requirements:     5
current archive field FWI ready:       false
current archive heavy field ready:     false
new controlled 2D design ready:        true
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The current archive has useful measured-field QC evidence: raw DZT/DZX files,
relative short-pair timing, waveform morphology, short-anchor spatial residual
audits, and relative signal-contrast checks. It does not satisfy the five
must-have controls for inversion: absolute time zero, surveyed profile/target
geometry, known target radius/diameter, cover-depth plus dielectric/velocity
calibration, and amplitude reference calibration.

Use the archive for field QC/context only. Field FWI, heavy field GPU work, and
3D/HPC field claims remain blocked until a controlled 2D acquisition records
the missing calibration controls.

## Validation

Focused tests:

```text
tests/test_gssi_field_existing_data_control_manifest.py
tests/test_close_spacing_source_density_archive_map.py
4 passed
```
