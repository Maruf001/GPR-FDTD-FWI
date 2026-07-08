# BEM Experiment 117: Fine-Mesh BEM Reference Export

Date: 2026-06-27

## Purpose

Export the validated fine-mesh Bempp receiver fields from run `113` into the
same receiver/frequency-bin schema used by the external 3D FDTD return
templates from run `115`.

This run does not launch FDTD, install real returned files, perform BEM/FDTD
comparison, make a 3D validation claim, launch GPU/HPC work, or train neural
networks.

## Output

```text
outputs/bem_experiments/117_project_core_bem_3d_fdtd_fine_mesh_bem_reference_export
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_bem_total_target_reference.csv
data/project_core_bem_3d_fdtd_fine_mesh_bem_incident_background_reference.csv
data/project_core_bem_3d_fdtd_fine_mesh_bem_scattered_reference.csv
data/project_core_bem_3d_fdtd_fine_mesh_bem_reference_norms.csv
data/project_core_bem_3d_fdtd_fine_mesh_bem_reference_residuals.csv
data/project_core_bem_3d_fdtd_fine_mesh_bem_reference_export_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_BEM_REFERENCE_EXPORT.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.py
scripts/script_snapshot_manifest.json
```

## Result

```text
frequency count:                     9
receiver count:                      31
rows per reference file:             279
total target-reference rows:         279
incident background-reference rows:  279
scattered-reference rows:            279
component cells per reference file:  1674
all component cells finite:          true
schema matches frequency-bin gate:   true
keys match run 115 import template:  true
max total-background-scattered error: 2.2737367544323206e-12
BEM reference export ready:          true
real FDTD data ready:                false
comparison ready:                    false
3D validation claim ready:           false
layered 3D GPR forward model ready:  false
field FWI ready:                     false
GPU/HPC ready:                       false
```

## Interpretation

The BEM side of the preferred nine-bin comparison is now packaged in the same
shape as the expected external 3D FDTD return. The exported files include:

- a BEM total-field target reference,
- a BEM incident-field background reference,
- a BEM scattered-field reference.

The algebraic check confirms that target minus background reproduces the
scattered reference to numerical precision. The largest residual is about
`2.3e-12`, which is negligible relative to the field magnitudes in this export.

## Decision

Use this export as the BEM-side reference payload when real external 3D FDTD
target/background frequency-bin files arrive and pass the import gates.

This does not unblock the validation claim by itself. Real BEM/FDTD comparison,
3D validation, layered 3D GPR claims, field FWI, and GPU/HPC escalation remain
blocked until real returned FDTD data pass the metadata and frequency-bin gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.py
sha256: 343d75a6b4a02b1ba8d80e22a5e38010e4879a4aaf8781861e3c6b2dc433cb69

test_project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.py
sha256: 3a4e71bc4dfb0e55bd94bf49ae13f896fcec53b27dda005924c0f819fcbde5cd
```

Subsequent related BEM/FDTD comparison experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.png
2716x845, dynamic range=255
```
