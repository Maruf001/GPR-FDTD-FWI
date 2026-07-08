# BEM Experiment 322: Receiver Operator Coefficient Stability Validator

Date: 2026-06-28

## Purpose

Validate the saved run `321` receiver-operator coefficient-stability audit from
artifacts.

This run uses saved artifacts only. It does not run Bempp, FDTD, GPU/HPC, field
transfer, field FWI, or 3D validation.

## Output

```text
outputs/bem_experiments/322_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_COEFFICIENT_STABILITY_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                       6
passed checks:                           6
failed checks:                           0
validation ready:                        true
coefficient series:                      8
series with sign flips:                  5
series above dynamic-range threshold:    8
stability concern series:                8
frequency-smooth operator ready:         false
receiver operator holdout ready:         false
physical claim ready:                    false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
field transfer ready:                    false
GPU/HPC ready:                           false
field FWI ready:                         false
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and counts | pass |
| stability metrics | pass |
| pass-all models are diagnostic only | pass |
| downstream states blocked | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The saved coefficient-stability audit validates: eight of eight coefficient
series have stability concerns, five change sign across frequency, and all
downstream physical-transfer claims remain blocked.

## Decision

Use run `322` as the validator for the BEM coefficient-stability no-promotion
audit. Keep the receiver-operator branch diagnostic-only until independent
no-refit holdout data exist.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_coefficient_stability_validator.py
3 passed
```

Figure validation:

```text
3437x868, dynamic range=255
```
