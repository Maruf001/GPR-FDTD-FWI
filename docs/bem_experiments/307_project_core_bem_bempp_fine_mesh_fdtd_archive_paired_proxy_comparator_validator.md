# BEM Experiment 307: Bempp Fine-Mesh FDTD Archive Paired Proxy Comparator Validator

Date: 2026-06-28

## Purpose

Validate the saved run `306` proxy-comparator smoke from output artifacts.

This run checks row counts, source readiness, per-frequency receiver counts,
scale diagnostics, shape-marker counts, finite receiver rows, figure
validation, script snapshots, and downstream gate states.

It does not run FDTD, execute a real BEM/FDTD comparison, calibrate scale,
validate 3D, transfer to field evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/307_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_PAIRED_PROXY_COMPARATOR_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                            8
passed checks:                    8
failed checks:                    0
validation ready:                 true
source smoke ready:               true
receiver comparison rows:         279
frequency summary rows:           9
scale-fit relative L2 max:        0.3700173321019876
shape marker frequency count:     7
raw amplitude comparison ready:   false
scale calibration ready:          false
real BEM/FDTD comparison ready:   false
3D validation claim ready:        false
field FWI ready:                  false
```

## Interpretation

The run `306` proxy-comparator smoke is internally consistent. Row counts,
scale diagnostics, shape-marker counts, figure validation, and closed
downstream gates match the saved artifact tables.

The validator keeps the conclusion narrow: this is a diagnostic comparator
smoke, not calibrated amplitude agreement or real BEM/FDTD validation.

## Decision

Use runs `306-307` as the validated proxy-comparator smoke. Sensitivity testing
remains required before treating the diagnostic validator as guarded.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_validator.py
4 passed
```

Figure validation:

```text
2897x884, dynamic range=255
```
