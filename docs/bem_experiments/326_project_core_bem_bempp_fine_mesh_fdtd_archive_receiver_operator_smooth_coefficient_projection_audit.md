# BEM Experiment 326: Receiver-Operator Smooth Coefficient Projection Audit

Date: 2026-06-28

## Purpose

Test whether the pass-all receiver operators from run `311` can be replaced by
low-degree smooth coefficient curves across frequency.

This run follows the run `321` coefficient-stability audit and the run `324`
conditioning-attribution audit. It asks whether simple coefficient smoothing can
repair the instability while preserving the same-data shape fit.

This is an artifact-only BEM audit. It does not run a new BEM solve, run FDTD,
launch GPU/HPC work, transfer to field evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/326_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_audit_candidate_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_audit_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_audit.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_SMOOTH_COEFFICIENT_PROJECTION_AUDIT.md
```

## Result

```text
pass-all source models:                 2
smooth candidates:                      12
smooth candidates passing all:          0
smooth candidates under dynamic range:  10
smooth candidates ready:                0
original max fit L2:                    0.14108683403595518
best smooth model:                      edge_gradient_curvature
best smooth degree:                     5
best smooth pass count:                 7
best smooth max fit L2:                 1.170343215108795
best smooth coefficient L2 range:       80.89838643480518
smooth projection preserves pass-all:   false
frequency-smooth operator ready:        false
physical operator claim ready:          false
real BEM/FDTD comparison ready:         false
3D validation claim ready:              false
field FWI ready:                        false
```

## Interpretation

Simple smoothing is not enough. Many smooth polynomial candidates reduce
coefficient variation, but none preserves the all-frequency shape fit that made
the same-data receiver operators attractive. The best tested smooth projection
uses degree five and still passes only seven of nine frequencies, with a maximum
relative L2 fit error far above the `0.15` marker.

This means the current pass-all correction depends on flexible per-frequency
coefficients rather than a stable smooth transfer function.

## Decision

Do not promote a frequency-smooth receiver operator from the current same-data
archive. The next useful BEM step remains an independent no-refit holdout or a
new physically constrained operator family, not coefficient smoothing alone.

Physical BEM/FDTD agreement, 3D validation, field transfer, GPU/HPC, and field
FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_audit.py
3 passed
```

Figure validation:

```text
3363x954, dynamic range=255
```
