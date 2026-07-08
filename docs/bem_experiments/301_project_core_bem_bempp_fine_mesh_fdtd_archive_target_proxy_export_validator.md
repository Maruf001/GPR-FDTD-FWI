# BEM Experiment 301: Bempp Fine-Mesh FDTD Archive Target Proxy Export Validator

Date: 2026-06-28

## Purpose

Validate the saved run `300` target-side archive proxy export from artifacts.

This run checks the row count, schema, finite values, locked frequency grid,
locked receiver grid, source archive provenance, closed acceptance gate, blocked
downstream states, figure validation, and script snapshots.

It does not accept the proxy as a real target/background pair, run the BEM/FDTD
comparator, set thresholds, launch GPU/HPC work, transfer to field evidence, or
run field FWI.

## Output

```text
outputs/bem_experiments/301_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_TARGET_PROXY_EXPORT_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                                10
passed checks:                         10
failed checks:                          0
validation ready:                    true
source target proxy export ready:    true
proxy target frequency rows:          279
locked receivers:                      31
locked frequencies:                     9
accepted source lock:                false
accepted receiver lock:              false
background export present:           false
accepted target/background pair:      false
real BEM/FDTD comparison ready:       false
GPU/HPC ready:                        false
field FWI ready:                      false
```

## Interpretation

The saved run `300` target-side proxy export is internally consistent: row
count, schema, frequency grid, receiver grid, finite values, source provenance,
figure output, and script snapshots validate. The accepted run `293` pair gate
remains closed because source lock, receiver lock, and background export are
not accepted.

## Decision

Use runs `300-301` as a validated target-side proxy export smoke. Sensitivity
testing remains required before treating the proxy validator as guarded. Do not
run the real BEM/FDTD comparator from this proxy.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_validator.py
3 passed
```

Figure validation:

```text
2969x873, dynamic range=255
```
