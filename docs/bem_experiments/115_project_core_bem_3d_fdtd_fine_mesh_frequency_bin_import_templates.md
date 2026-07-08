# BEM Experiment 115: Fine-Mesh Frequency-Bin Import Templates

Date: 2026-06-27

## Purpose

Write strict target/background CSV templates for the preferred nine-bin external
FDTD return defined by run `114`.

Run `114` kept the original four-bin FDTD request as the minimal acceptable
return, but it also defined a preferred nine-bin return if external FDTD cost
allows. This run makes that preferred return executable by pre-filling all
receiver and frequency keys from the run `113` fine-mesh BEM grid.

This run does not launch FDTD, install returned files, perform BEM/FDTD
comparison, make a 3D validation claim, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/115_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_target_frequency_bin_import_template.csv
data/project_core_bem_3d_fdtd_fine_mesh_background_frequency_bin_import_template.csv
data/project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_package.csv
data/project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_FREQUENCY_BIN_IMPORT_TEMPLATES.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.py
scripts/script_snapshot_manifest.json
```

## Result

```text
frequency count:                     9
receiver count:                      31
target template rows:                279
background template rows:            279
paired target/background rows:       558
required schema columns:             12
component columns to fill:           6
blank component cells:               3348
strict columns match comparator:     true
matches run 114 rows per file:       true
matches run 114 paired rows:         true
import templates ready:              true
real FDTD data ready:                false
comparison ready:                    false
3D validation claim ready:           false
layered 3D GPR model ready:          false
field FWI ready:                     false
GPU/HPC ready:                       false
```

The prefilled frequency grid is:

```text
0.4, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0 GHz
```

The receiver line has 31 points from y=-0.08 m to y=0.08 m at z=0.09 m.

## Interpretation

The preferred nine-bin external FDTD return now has concrete import templates.
The future FDTD operator should fill only the six complex field columns for
both the target-present and background files:

```text
field_ex_real, field_ex_imag
field_ey_real, field_ey_imag
field_ez_real, field_ez_imag
```

The templates contain no real FDTD data. They are ready for handoff, but they
do not change the validation boundary.

## Decision

Use these templates if the external FDTD operator can return the preferred full
fine-mesh frequency grid.

Keep BEM/FDTD comparison, 3D validation, local 3D FDTD launch, and GPU/HPC work
blocked until the six complex field columns are filled for both target and
background and all return gates pass.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.py
sha256: be914a1dc8d68c49bbd02fddfd1e737154e7ab276af0ec2c6a9aedcaf2a4b02f

test_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.py
sha256: f8415ab522eb347a876e7ba6743e35e7c1d0108e39f4e8454622b7429078beaa
```

Subsequent related BEM 3D return-intake experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.py
3 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.png
2500x810, dynamic range=255
```
