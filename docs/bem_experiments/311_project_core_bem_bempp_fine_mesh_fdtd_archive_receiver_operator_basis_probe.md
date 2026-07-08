# BEM Experiment 311: Bempp Fine-Mesh FDTD Archive Receiver Operator Basis Probe

Date: 2026-06-28

## Purpose

Test whether low-order receiver-line operators on the scalar proxy can explain
the run `309-310` shape mismatch.

This is a diagnostic fit over saved artifacts only. It does not run FDTD, run a
new BEM solve, validate a physical operator, calibrate BEM/FDTD amplitude
agreement, validate 3D physics, transfer to field evidence, launch GPU/HPC
work, or run field FWI.

## Output

```text
outputs/bem_experiments/311_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_probe
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_model_summary.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_probe_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_probe.png
scripts/script_snapshot_manifest.json
```

## Result

```text
operator models:                     10
frequency-model rows:                90
baseline model:                      identity_scale
baseline pass count:                 7 / 9
baseline mean fit L2:                0.138495
best model:                          edge_gradient_curvature
best model features:                 amp; amp_abs_y; grad; curv
best model pass count:               9 / 9
best model mean fit L2:              0.043696
best model max fit L2:               0.097397
minimum pass-all model:              edge_and_gradient
minimum pass-all features:           amp; amp_abs_y; grad
minimum pass-all mean fit L2:        0.058765
shape diagnostic ready:              true
physical operator claim ready:       false
needs holdout validation:            true
real BEM/FDTD comparison ready:      false
3D validation claim ready:           false
field FWI ready:                     false
```

Model ranking:

| Rank | Model | Features | Pass count | Mean fit L2 | Max fit L2 | Failure frequencies GHz |
| ---: | --- | --- | ---: | ---: | ---: | --- |
| 1 | edge_gradient_curvature | amp; amp_abs_y; grad; curv | 9 | 0.0437 | 0.0974 | none |
| 2 | edge_and_gradient | amp; amp_abs_y; grad | 9 | 0.0588 | 0.1411 | none |
| 3 | aperture_second_order | amp; amp_y2; curv | 8 | 0.0776 | 0.2355 | 0.4 |
| 4 | local_second_order | amp; grad; curv | 8 | 0.0777 | 0.1699 | 0.4 |
| 5 | identity_plus_curvature | amp; curv | 8 | 0.1040 | 0.2665 | 0.4 |
| 6 | polynomial_aperture | amp; amp_y2; amp_y4 | 8 | 0.1087 | 0.3683 | 0.4 |
| 7 | identity_plus_gradient | amp; grad | 7 | 0.1098 | 0.2472 | 0.4; 3 |
| 8 | identity_plus_quadratic_aperture | amp; amp_y2 | 7 | 0.1141 | 0.3691 | 0.4; 3 |
| 9 | identity_plus_edge_gain | amp; amp_abs_y | 7 | 0.1157 | 0.3686 | 0.4; 3 |
| 10 | identity_scale | amp | 7 | 0.1385 | 0.3700 | 0.4; 3 |

## Interpretation

Low-order receiver-line operators explain the shape mismatch much better than
component projection. The baseline identity-scale fit passes seven of nine
frequencies. An edge-plus-gradient operator is the simplest model that passes
all nine frequencies, while the edge-gradient-curvature model is the
lowest-error model.

This is evidence for a receiver-aperture/source-operator mismatch. It is not a
validated physical BEM/FDTD agreement, because the operator was fitted on the
same receiver grid and has not been tested on independent geometry or measured
data.

## Decision

Use run `311` as a diagnostic target for a future physically constrained
source/operator model and holdout validation. Do not promote calibrated
BEM/FDTD agreement, 3D validation, field transfer, GPU/HPC readiness, or field
FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_probe.py
3 passed
```

Figure validation:

```text
3076x1604, dynamic range=255
```
