# BEM Experiment 304: Bempp Fine-Mesh FDTD Archive Paired Proxy Export Validator

Date: 2026-06-28

## Purpose

Validate the saved run `303` paired scalar proxy export from output artifacts.

This run checks the target, generated-background, and scattered frequency-row
files; the metadata ledger; the generated background B-scan hash; the locked
frequency/receiver grid; figure validation; script snapshots; and downstream
gate states.

It does not run FDTD, execute a real BEM/FDTD comparison, calibrate thresholds,
validate 3D, transfer to field evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/304_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_PAIRED_PROXY_EXPORT_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              10
passed checks:                      10
failed checks:                      0
validation ready:                   true
source paired proxy ready:          true
target proxy rows:                  279
background proxy rows:              279
scattered proxy rows:               279
time/scan grid match:               true
accepted source lock:               false
accepted receiver lock:             false
accepted target/background pair:    false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
GPU/HPC ready:                      false
field FWI ready:                    false
```

## Interpretation

The run `303` paired scalar proxy export is internally consistent. Target,
generated-background, and scattered rows share the locked frequency/receiver
grid, all values are finite, and scattered values equal target minus
background. The generated no-rebar background also matches the target time and
scan grid.

The validator keeps the real BEM/FDTD gate closed. The proxy is useful for
adapter and comparator plumbing, not as accepted run `293` FDTD evidence.

## Decision

Use runs `303-304` as the validated paired scalar proxy export. Sensitivity
testing remains required before using it in a proxy comparator.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_validator.py
4 passed
```

Figure validation:

```text
3041x898, dynamic range=255
```
