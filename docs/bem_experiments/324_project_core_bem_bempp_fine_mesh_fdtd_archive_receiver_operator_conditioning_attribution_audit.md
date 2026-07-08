# BEM Experiment 324: Receiver-Operator Conditioning Attribution Audit

Date: 2026-06-28

## Purpose

Audit whether the unstable receiver-operator coefficients from run `321` are
mainly caused by ill-conditioned same-data operator fits from run `311`.

Runs `311-313` showed that fitted receiver-line operators can improve the
same-data BEM/FDTD proxy comparison. Runs `321-323` showed that the fitted
coefficients are unstable across frequency. This run checks whether simple
condition-number repair is the right next BEM branch.

This is an artifact-only audit. It does not run a new BEM solve, run FDTD,
launch GPU/HPC work, transfer to field evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/324_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_by_model.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_audit_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_audit.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_CONDITIONING_ATTRIBUTION_AUDIT.md
```

## Result

```text
operator frequency rows:                  90
operator models:                          10
pass-all models:                          edge_and_gradient, edge_gradient_curvature
condition threshold:                      100
max condition number:                     14.402570318619736
rows above condition threshold:           0
pass-all models with >100x coeff range:   2
stability concern series from run 321:    8
instability explained by conditioning:    false
conditioning audit ready:                 true
physical operator claim ready:            false
field transfer ready:                     false
GPU/HPC ready:                            false
field FWI ready:                          false
```

## Interpretation

The receiver-operator design matrices are not ill-conditioned under the
selected threshold. No operator-frequency row exceeds a condition number of
`100`, and the worst observed condition number is about `14.4`.

The coefficient problem therefore remains after removing the simple
conditioning explanation. Both pass-all models still have coefficient dynamic
ranges above `100x`. The instability is more consistent with a missing physical
source/receiver/operator model or missing independent holdout validation than
with a numerical conditioning failure in the small least-squares fits.

## Decision

Do not spend the next BEM branch on condition-number repair alone. The useful
next BEM paths are either:

1. stage an independent no-refit BEM/FDTD holdout pair, or
2. design a physically constrained smooth operator and still validate it on a
   no-refit holdout.

Physical BEM/FDTD agreement, 3D validation, field transfer, GPU/HPC, and field
FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_audit.py
3 passed
```

Figure validation:

```text
3363x953, dynamic range=255
```
