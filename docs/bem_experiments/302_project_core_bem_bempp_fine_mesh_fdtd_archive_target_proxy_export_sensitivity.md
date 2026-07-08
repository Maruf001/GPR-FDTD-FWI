# BEM Experiment 302: Bempp Fine-Mesh FDTD Archive Target Proxy Export Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `301` proxy-export validator with controlled damage cases.

This run checks whether the validator accepts only the exact run `300` proxy
export and rejects plausible artifact drift: row-count drift, schema drift,
non-finite values, receiver/frequency drift, provenance drift, proxy acceptance
promotion, downstream promotion, figure-validation drift, and script-snapshot
drift.

It does not accept the proxy as a real target/background pair, run the BEM/FDTD
comparator, set thresholds, launch GPU/HPC work, transfer to field evidence, or
run field FWI.

## Output

```text
outputs/bem_experiments/302_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_TARGET_PROXY_EXPORT_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                            43
expected pass scenarios:               1
observed pass scenarios:               1
expected failure scenarios:           42
observed failure scenarios:           42
unexpected outcomes:                   0
sensitivity ready:                  true
exact run 300 accepted:             true
damaged variants rejected:          true
accepted target/background pair:    false
real BEM/FDTD comparison ready:     false
GPU/HPC ready:                      false
field FWI ready:                    false
```

## Interpretation

The proxy-export validator accepts the exact run `300` artifacts and rejects
every damaged variant. The rejected cases cover row-count drift, schema drift,
non-finite values, receiver/frequency drift, provenance drift, proxy acceptance
promotion, downstream promotion, figure-validation drift, and script-snapshot
drift.

## Decision

Use runs `300-302` as a guarded target-side proxy export branch. The proxy
proves adapter mechanics only. Accepted target/background export, real BEM/FDTD
comparison, thresholds, 3D validation, field transfer, GPU/HPC, and field FWI
remain blocked.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_target_proxy_export_sensitivity.py
3 passed
```

Figure validation:

```text
4031x883, dynamic range=255
```
