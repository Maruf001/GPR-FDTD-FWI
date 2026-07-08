# BEM Experiment 398: 35-Field Real-Return Template Pack

Date: 2026-06-29

## Purpose

Convert the guarded 35-field BEM/FDTD preflight closure plan into a concrete,
non-evidence template pack for a future external return.

This run does not stage returned FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, transfer to field evidence, launch GPU work, or make a
3D validation claim.

## Output

```text
outputs/bem_experiments/398_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack
```

Key artifacts:

```text
template_packet_root/project_core_bem_3d_fdtd_fine_mesh_target_frequency_bins.csv.template.csv
template_packet_root/project_core_bem_3d_fdtd_fine_mesh_background_frequency_bins.csv.template.csv
template_packet_root/project_core_bem_3d_fdtd_external_return_metadata.csv.template.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_template_file_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack.png
```

## Result

```text
template files written:              4
template packet files:               3
frequency template files:            2
metadata template files:             1
expected external files:             3
expected frequencies:                9
expected receivers:                  31
rows per frequency file:             279
frequency template rows total:       558
frequency schema columns:            12
blank frequency component cells:     3348
metadata fields:                     35
blocking metadata fields:            34
prefilled metadata values:           23
blank metadata values:               12
receiver-aperture addendum fields:   5
real comparison ready:               false
3D validation claim ready:           false
field FWI ready:                     false
GPU/HPC ready:                       false
```

## Interpretation

The future return is now concrete: two frequency-bin files are required, one
for the target case and one for the background case. Each file must contain 279
rows: nine frequencies by 31 receivers. The metadata ledger must contain 35
fields, including five receiver-aperture convention fields.

The templates are intentionally not evidence. They still contain 3348 blank
frequency-component cells and 12 blank metadata values that must be filled with
real returned values before the preflight can pass.

## Decision

Use this template pack as the external-return handoff artifact. Keep real
BEM/FDTD comparison, 3D validation, field transfer, field FWI, and GPU/HPC
blocked until real target, background, and metadata files replace the templates
and pass the 35-field preflight.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_35field_template_pack.py
3 passed
```

Figure validation:

```text
3508x898, dynamic range=255
```
