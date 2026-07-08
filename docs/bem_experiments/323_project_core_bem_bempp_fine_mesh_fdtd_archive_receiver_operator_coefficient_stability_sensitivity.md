# BEM Experiment 323: Receiver Operator Coefficient Stability Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `322` validator for the saved run `321` receiver-operator
coefficient-stability audit.

This is an artifact-only sensitivity run. It mutates saved coefficient-series
rows, frequency rows, summary values, figure metadata, and script snapshots in
memory. It does not run Bempp, FDTD, GPU/HPC, field transfer, field FWI, or 3D
validation.

## Output

```text
outputs/bem_experiments/323_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_COEFFICIENT_STABILITY_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         13
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        12
observed failure scenarios:        12
unexpected outcomes:               0
sensitivity ready:                 true
exact run 321 accepted:            true
damaged variants rejected:         true
frequency-smooth operator ready:   false
physical claim ready:              false
3D validation claim ready:         false
field transfer ready:              false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The damaged variants cover coefficient-row drift, frequency-row drift, summary
count drift, sign-flip drift, dynamic-range drift, stability-concern drift,
pass-all model drift, false downstream promotion, figure drift, and
script-snapshot drift.

## Interpretation

The coefficient-stability validator accepts the exact run `321` audit and
rejects every damaged variant tested here, including false physical-transfer
promotion.

## Decision

Use runs `321-323` as the guarded BEM coefficient-stability no-promotion block.
Keep the receiver-operator branch diagnostic-only until independent no-refit
holdout data exist.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_sensitivity.py
3 passed
```

Figure validation:

```text
3437x889, dynamic range=255
```
