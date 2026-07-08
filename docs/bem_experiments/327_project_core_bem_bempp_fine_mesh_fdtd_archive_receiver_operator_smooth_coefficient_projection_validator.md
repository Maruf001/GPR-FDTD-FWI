# BEM Experiment 327: Receiver-Operator Smooth Coefficient Projection Validator

Date: 2026-06-28

## Purpose

Validate the saved run `326` smooth coefficient projection audit from artifacts.

This is an artifact-only validator. It does not run a new BEM solve, run FDTD,
launch GPU/HPC work, transfer to field evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/327_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_validator_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_SMOOTH_COEFFICIENT_PROJECTION_VALIDATOR.md
```

## Result

```text
validation checks:                 7
passed checks:                     7
failed checks:                     0
validation ready:                  true
smooth candidates:                 12
smooth candidates passing all:     0
smooth candidates ready:           0
best smooth model:                 edge_gradient_curvature
best smooth degree:                5
best smooth pass count:            7
best smooth max fit L2:            1.170343215108795
smooth projection preserves pass:  false
frequency-smooth operator ready:   false
physical operator claim ready:     false
field transfer ready:              false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Interpretation

Run `326` validates as a no-smoothing repair result. The saved smooth
coefficient candidates reduce coefficient variation in several cases, but none
preserves the all-frequency shape fit.

## Decision

Use runs `326-327` as the guarded smooth-coefficient no-repair block. Keep
physical BEM/FDTD agreement, 3D validation, field transfer, GPU/HPC, and field
FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_audit.py
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_smooth_coefficient_projection_validator.py

6 passed
```

Figure validation:

```text
3365x916, dynamic range=255
```
