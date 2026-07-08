# BEM Experiment 313: Bempp Fine-Mesh FDTD Archive Receiver Operator Basis Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `312` receiver-operator basis validator with controlled
damage cases.

This run does not run FDTD, run a new BEM solve, validate a physical operator,
calibrate BEM/FDTD amplitude agreement, validate 3D physics, transfer to field
evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/313_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_sensitivity_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         43
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        42
observed failure scenarios:        42
unexpected outcomes:               0
sensitivity ready:                 true
exact run 311 accepted:            true
damaged variants rejected:         true
physical operator claim ready:     false
needs holdout validation:          true
real BEM/FDTD comparison ready:    false
3D validation claim ready:         false
field FWI ready:                   false
```

Damage families rejected:

| Damage family | Examples |
| --- | --- |
| Operator-row drift | missing row, receiver-count drift, design-rank drift, non-finite fit |
| Model-summary drift | missing model, feature drift, baseline/best/minimum-pass-all metric drift |
| Gate drift | diagnostic disabled, physical-claim enabled, holdout requirement disabled |
| Downstream promotion | real comparison, 3D, field transfer, GPU/HPC, and field FWI flags forced true |
| Artifact drift | missing/weak figure validation and missing script snapshot hashes |

## Interpretation

The receiver-operator validator accepts the exact run `311` artifact set and
rejects every damaged variant. The guarded branch supports a diagnostic result:
receiver-line edge/gradient/curvature operators can explain the shape mismatch
better than scale or component projection.

It still does not validate a physical operator or calibrated BEM/FDTD
agreement.

## Decision

Use runs `311-313` as a guarded receiver-operator diagnostic branch only.
Physical operator claims, calibrated BEM/FDTD comparison, 3D validation, field
transfer, GPU/HPC readiness, and field FWI remain blocked until holdout
validation exists.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_sensitivity.py
3 passed
```

Figure validation:

```text
4211x919, dynamic range=255
```
