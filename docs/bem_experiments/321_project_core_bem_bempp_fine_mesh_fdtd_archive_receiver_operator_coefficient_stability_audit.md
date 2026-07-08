# BEM Experiment 321: Receiver Operator Coefficient Stability Audit

Date: 2026-06-28

## Purpose

Audit the frozen receiver-operator coefficients from the run `315` holdout
design packet.

Run `311` showed that low-order receiver-line operators can fit the saved
BEM/FDTD proxy shapes on the same data. Runs `315-320` correctly keep that
branch blocked until independent no-refit holdout data exist. This run asks a
smaller question:

```text
Do the frozen per-frequency operator coefficients look stable enough to support
a physical transfer-operator claim now?
```

This run uses saved artifacts only. It does not run Bempp, FDTD, GPU/HPC, field
transfer, field FWI, or 3D validation.

## Output

```text
outputs/bem_experiments/321_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_series.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_frequency_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_audit_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_audit.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_COEFFICIENT_STABILITY_AUDIT.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_audit.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
frozen operator rows:                  27
models:                                3
frequencies:                           9
coefficient series:                    8
series with sign flips:                5
series above dynamic-range threshold:  8
stability concern series:              8
dynamic-range threshold:               100x
max absolute dynamic range:            1471.2258002774788
median absolute dynamic range:         214.01903073512904
pass-all models:                       edge_gradient_curvature, edge_and_gradient
frequency-smooth operator ready:       false
receiver operator holdout ready:       false
physical claim ready:                  false
real BEM/FDTD comparison ready:        false
3D validation claim ready:             false
field transfer ready:                  false
GPU/HPC ready:                         false
field FWI ready:                       false
```

Coefficient-stability summary:

| Model | Feature | Dynamic range | Sign flips |
| --- | --- | ---: | ---: |
| edge and gradient | amplitude | 742.066 | 0 |
| edge and gradient | edge gain | 121.580 | 2 |
| edge and gradient | gradient | 100.312 | 4 |
| edge gradient curvature | amplitude | 906.699 | 0 |
| edge gradient curvature | edge gain | 155.464 | 2 |
| edge gradient curvature | gradient | 129.507 | 4 |
| edge gradient curvature | curvature | 1471.226 | 1 |
| identity scale | amplitude | 272.574 | 0 |

## Interpretation

The same-data receiver-operator fits remain useful diagnostics, but the frozen
per-frequency coefficients do not behave like a smooth physical transfer
operator. Every coefficient series spans at least `100x` in absolute magnitude,
and five of eight coefficient series change sign across frequency.

This strengthens the current boundary rather than weakening it: the
receiver-operator branch can explain shape mismatch on the saved proxy data,
but it should not be promoted to a physical BEM/FDTD agreement or transfer
claim without independent no-refit holdout evidence.

## Decision

Keep the receiver-operator branch as a diagnostic correction only. Do not
promote a physical operator, real BEM/FDTD comparison, 3D validation, field
transfer, GPU/HPC, or field-FWI claim until independent no-refit holdout data
exist.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_audit.py
3 passed
```

Figure validation:

```text
3400x916, dynamic range=255
```
