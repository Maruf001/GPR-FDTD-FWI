# BEM Experiment 312: Bempp Fine-Mesh FDTD Archive Receiver Operator Basis Validator

Date: 2026-06-28

## Purpose

Validate the saved run `311` receiver-operator basis probe from its output
artifacts.

This run does not run FDTD, run a new BEM solve, validate a physical operator,
calibrate BEM/FDTD amplitude agreement, validate 3D physics, transfer to field
evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/312_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_validation_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_validator_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
validation ready:                   true
source shape diagnostic ready:      true
physical operator claim ready:      false
needs holdout validation:           true
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
field FWI ready:                    false
```

Validated checks:

| Check | Result |
| --- | --- |
| Policy, counts, and source readiness | pass |
| Expected model/feature contract | pass |
| Frequency rows match model contract | pass |
| Summary matches baseline, best, and minimum pass-all models | pass |
| Diagnostic ready but physical claim blocked | pass |
| Downstream states blocked | pass |
| Figure validation present | pass |
| Script snapshots present | pass |

## Interpretation

The saved receiver-operator basis probe is internally consistent. The
validation confirms the model contract, baseline/best/minimum pass-all metrics,
diagnostic-only gate state, figure output, and script snapshots.

## Decision

Treat run `311` as a validated diagnostic target, not as a physical operator or
calibrated BEM/FDTD agreement. Sensitivity testing remains required before this
validator branch is guarded.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_basis_validator.py
2 passed
```

Figure validation:

```text
2825x910, dynamic range=255
```
