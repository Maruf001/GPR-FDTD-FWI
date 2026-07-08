# BEM Experiment 300: Bempp Fine-Mesh FDTD Archive Target Proxy Export Smoke

Date: 2026-06-28

## Purpose

Convert one selected 2D archive B-scan into target-side, schema-shaped
frequency rows as a guarded adapter smoke test.

This run uses the run `113` nine-frequency grid and 31-point receiver line,
interpolates the selected 2D B-scan onto that receiver line, and performs a
direct frequency extraction. It intentionally keeps the accepted BEM/FDTD pair
gate closed because the source convention, receiver convention, and background
export are not accepted run `293` inputs.

It does not create an accepted run `293` target/background FDTD pair, run the
BEM/FDTD comparator, set thresholds, launch GPU/HPC work, transfer to field
evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/300_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_smoke
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_frequency_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_metadata.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_smoke_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_smoke.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_TARGET_PROXY_EXPORT_SMOKE.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_smoke.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
selected source file:                    outputs/experiments/107_detection_single_rebar_default_smoke/data/detection_bscan.npz
source time samples:                     1885
source scan positions:                   101
locked receivers used:                   31
locked frequencies used:                 9
proxy target frequency rows:             279
finite proxy frequency rows:             279
schema shaped like run 293:              true
target proxy export ready:               true
accepted run 293 source lock:            false
accepted run 293 receiver lock:          false
background export present:               false
accepted target/background pair ready:   false
real BEM/FDTD comparison ready:          false
GPU/HPC ready:                           false
field FWI ready:                         false
```

## Interpretation

A selected 2D archive B-scan can be transformed into finite target-side
frequency rows using the locked nine-frequency grid and 31-point receiver line.
This is only a proxy adapter smoke: the source convention, receiver convention,
and missing background export keep the accepted run `293` pair gate closed.

## Decision

Use run `300` as the target-side archive adapter smoke. The next guarded step is
a validator for this proxy export, followed by a sensitivity test. Do not treat
the proxy as an accepted real BEM/FDTD comparison input.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_smoke.py
4 passed
```

Figure validation:

```text
3580x880, dynamic range=255
```
