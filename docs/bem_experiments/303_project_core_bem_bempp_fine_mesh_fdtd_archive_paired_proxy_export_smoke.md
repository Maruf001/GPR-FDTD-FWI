# BEM Experiment 303: Bempp Fine-Mesh FDTD Archive Paired Proxy Export Smoke

Date: 2026-06-28

## Purpose

Create an explicitly labeled 2D scalar target/background proxy export for the
Bempp fine-mesh matched-export path.

Run `300` showed that the run `107` archive B-scan could be converted into
target-side frequency rows. This run closes the adapter-only background gap by
generating a no-rebar background B-scan with the same grid, scan line, source
wavelet, and Tx/Rx convention.

This is a proxy adapter smoke. It does not create accepted run `293` 3D FDTD
evidence, run the real BEM/FDTD comparator, calibrate thresholds, validate 3D,
launch inversion-scale work, transfer to field evidence, launch GPU/HPC work
as a downstream claim, or run field FWI.

## Output

```text
outputs/bem_experiments/303_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_smoke
```

Key artifacts:

```text
data/generated_background_bscan.npz
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_target_frequency_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_background_frequency_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_scattered_frequency_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_metadata.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_smoke_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_smoke.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_PAIRED_PROXY_EXPORT_SMOKE.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_smoke.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
selected target source file:              outputs/experiments/107_detection_single_rebar_default_smoke/data/detection_bscan.npz
generated background file:                outputs/bem_experiments/303_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_smoke/data/generated_background_bscan.npz
background backend:                       gpu-cpml
background elapsed seconds:               14.702
time/scan grid match:                     true
locked receivers used:                    31
locked frequencies used:                  9
target proxy frequency rows:              279
background proxy frequency rows:          279
scattered proxy frequency rows:           279
target schema shaped like run 293:        true
background schema shaped like run 293:    true
paired scalar proxy export ready:         true
accepted run 293 source lock:             false
accepted run 293 receiver lock:           false
accepted target/background pair ready:    false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field FWI ready:                          false
```

## Interpretation

A same-grid 2D scalar target/background proxy pair can now be produced for the
archive target case. The adapter can write target, generated-background, and
scattered frequency-domain rows in the run `293` schema shape.

The result does not promote the real BEM/FDTD comparison. The source and
receiver conventions are still scalar 2D proxies rather than the accepted run
`293` 3D dipole convention, so source lock, receiver lock, accepted pair,
3D-validation, field-transfer, GPU/HPC, and field-FWI gates remain closed.

## Decision

Use run `303` as the paired scalar proxy export smoke. Validate and stress-test
it before using it in any proxy comparator. Do not treat it as accepted run
`293` FDTD evidence.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_smoke.py
4 passed
```

Figure validation:

```text
4790x920, dynamic range=255
```
