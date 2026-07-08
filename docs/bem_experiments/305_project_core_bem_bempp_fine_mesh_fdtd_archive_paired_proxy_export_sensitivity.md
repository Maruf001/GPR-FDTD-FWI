# BEM Experiment 305: Bempp Fine-Mesh FDTD Archive Paired Proxy Export Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `304` validator for the run `303` paired scalar proxy
export.

This run checks whether the validator accepts the exact saved run `303`
artifact set and rejects controlled damage to target/background/scattered
rows, schema fields, solver labels, pair identifiers, frequency/receiver keys,
finite values, scattered residuals, metadata provenance, summary counts,
downstream readiness flags, figure validation, and script snapshots.

It does not run FDTD, execute a real BEM/FDTD comparison, calibrate thresholds,
validate 3D, transfer to field evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/305_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_PAIRED_PROXY_EXPORT_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         44
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        43
observed failure scenarios:        43
unexpected outcomes:               0
sensitivity ready:                 true
exact run 303 accepted:            true
damaged variants rejected:         true
accepted run 293 source lock:      false
accepted run 293 receiver lock:    false
real BEM/FDTD comparison ready:    false
3D validation claim ready:         false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Interpretation

The paired-proxy validator accepts the exact run `303` artifact set and rejects
every damaged variant. The rejected variants cover row-count drift, schema
drift, solver and pair-id drift, frequency/receiver drift, non-finite values,
scattered residual drift, metadata/provenance drift, summary drift, downstream
promotion, figure-validation drift, and script-snapshot drift.

This closes the paired scalar proxy export as a guarded adapter artifact. It
can support a future proxy-comparator smoke, but it still does not unlock
accepted run `293` evidence or real BEM/FDTD comparison.

## Decision

Use runs `303-305` as the guarded paired scalar proxy export. Accepted run
`293` evidence, real BEM/FDTD comparison, 3D validation, field transfer,
GPU/HPC readiness, and field FWI remain blocked.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_export_sensitivity.py
3 passed
```

Figure validation:

```text
4391x899, dynamic range=255
```
