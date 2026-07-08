# BEM Experiment 294: Bempp Fine-Mesh Matched FDTD Export Contract Validator

Date: 2026-06-28

## Purpose

Validate the saved run `293` matched FDTD export contract from output
artifacts.

This run checks contract row counts, ready BEM reference rows, required
target/background FDTD export rows, paired-export schema fields, source guard
readiness, blocked real-comparison states, figure validation, and script
snapshots.

It does not run FDTD, ingest real FDTD traces, compute a real BEM/FDTD
comparison, set thresholds, launch GPU/HPC work, transfer to field evidence, or
run field FWI.

## Output

```text
outputs/bem_experiments/294_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_MATCHED_FDTD_EXPORT_CONTRACT_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              7
passed checks:                      7
failed checks:                      0
validation ready:                   true
source contract ready:              true
contract rows:                      9
schema fields:                      15
BEM reference-ready rows:           4
FDTD export-required rows:          2
real BEM/FDTD comparison ready:     false
threshold calibration ready:        false
3D validation claim ready:          false
GPU/HPC ready:                      false
field FWI ready:                    false
```

## Interpretation

The saved run `293` contract is internally consistent: the BEM reference and
metadata locks are ready, target/background FDTD exports are explicitly
required, the pairwise schema is present, and comparison/threshold/downstream
states remain blocked.

## Decision

Use runs `293-294` as the validated matched FDTD export contract. Sensitivity
testing remains required before treating the validator itself as guarded.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_validator.py
3 passed
```

Figure validation:

```text
2933x890, dynamic range=255
```
