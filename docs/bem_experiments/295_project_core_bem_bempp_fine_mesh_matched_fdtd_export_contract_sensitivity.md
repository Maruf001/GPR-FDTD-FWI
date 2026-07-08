# BEM Experiment 295: Bempp Fine-Mesh Matched FDTD Export Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `294` validator for the run `293` matched FDTD export
contract.

This run checks whether the validator accepts the exact saved run `293`
contract and rejects controlled damage to BEM reference rows, FDTD export
requirements, comparison blockers, schema fields, summary counts, source guard
readiness, downstream readiness, figure validation, and script snapshots.

It does not run FDTD, ingest real FDTD traces, compute a real BEM/FDTD
comparison, set thresholds, launch GPU/HPC work, transfer to field evidence, or
run field FWI.

## Output

```text
outputs/bem_experiments/295_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_MATCHED_FDTD_EXPORT_CONTRACT_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          34
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         33
observed failure scenarios:         33
unexpected outcomes:                0
sensitivity ready:                  true
exact run 293 accepted:             true
damaged variants rejected:          true
real BEM/FDTD comparison ready:     false
threshold calibration ready:        false
3D validation claim ready:          false
GPU/HPC ready:                      false
field FWI ready:                    false
```

## Interpretation

The matched-export validator accepts the exact run `293` contract and rejects
every damaged variant. The rejected cases cover BEM reference drift, FDTD
export promotion, comparison-blocker drift, schema drift, source-guard drift,
downstream promotion, figure validation drift, and script-snapshot drift.

## Decision

Use runs `293-295` as the guarded BEM/FDTD matched-export contract. Real
target/background FDTD exports and paired residual rows remain required before
any comparison, threshold, 3D, inversion, field, GPU, or FWI claim.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_sensitivity.py
3 passed
```

Figure validation:

```text
4031x891, dynamic range=255
```
