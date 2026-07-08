# BEM Experiment 293: Bempp Fine-Mesh Matched FDTD Export Contract

Date: 2026-06-28

## Purpose

Consume the guarded Bempp fine-mesh reference from runs `290-292` and define
the future matched FDTD export/comparison contract.

This run specifies the BEM reference rows, required FDTD target/background
exports, paired residual table, threshold metadata, and blocked downstream
state.

It does not run FDTD, ingest real FDTD traces, compute a real BEM/FDTD
comparison, set thresholds, launch GPU/HPC work, transfer to field evidence, or
run field FWI.

## Output

```text
outputs/bem_experiments/293_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_rows.csv
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_schema.csv
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_MATCHED_FDTD_EXPORT_CONTRACT.md
scripts/run_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract.py
scripts/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract.py
scripts/script_snapshot_manifest.json
```

## Result

```text
contract rows:                       9
schema fields:                       15
BEM reference-ready rows:            4
FDTD export-required rows:           2
comparison-required rows:            1
threshold-required rows:             1
downstream-blocked rows:             1
matched export contract ready:       true
real FDTD target export present:     false
real FDTD background export present: false
real BEM/FDTD comparison ready:      false
threshold calibration ready:         false
3D validation claim ready:           false
GPU/HPC ready:                       false
field FWI ready:                     false
```

## Interpretation

The guarded 8x20 Bempp reference now has a matched FDTD export contract: BEM
mesh, frequency grid, source metadata, receiver metadata, target/background
FDTD exports, paired residual rows, and threshold metadata have explicit roles.
Real FDTD exports and real comparison rows remain absent.

## Decision

Use run `293` as the BEM/FDTD export contract for the future first matched
pair. Do not promote real BEM/FDTD agreement, threshold calibration, 3D
validation, inversion scale, field transfer, GPU/HPC, or field FWI until
target/background FDTD exports and paired residuals exist.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_contract.py
3 passed
```

Figure validation:

```text
2861x869, dynamic range=255
```
