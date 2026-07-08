# BEM Experiment 092: Project-Core Run089 Grid-Aware Adapter Contract

Date: 2026-06-25

## Purpose

Convert the positive run `091` grid-aware scattering replay into a concrete
adapter contract for the next reusable BEM/project-core smoke run.

Runs `089` and `090` showed that the continuous analytic-cylinder bridge and
simple alignment diagnostics do not close the project-core scattering gap. Run
`091` showed that the same geometry becomes acceptable when scattering is
computed from target cells and project-core background fields on the actual
grid. This run captures that decision boundary as an implementation contract.

This is CPU-only contract synthesis. It does not rerun FDTD time stepping,
field data processing, GPU kernels, FWI, 3D/HPC work, or neural-network
training.

## Output

```text
outputs/bem_experiments/092_project_core_run089_grid_aware_adapter_contract
```

Key artifacts:

```text
data/project_core_run089_grid_aware_adapter_contract_summary.json
data/project_core_run089_grid_aware_adapter_interface.csv
data/project_core_run089_grid_aware_adapter_gates.csv
figures/project_core_run089_grid_aware_adapter_contract.png
docs/PROJECT_CORE_RUN089_GRID_AWARE_ADAPTER_CONTRACT.md
scripts/run_project_core_run089_grid_aware_adapter_contract.py
scripts/test_project_core_run089_grid_aware_adapter_contract.py
scripts/script_snapshot_manifest.json
```

## Result

```text
continuous analytic-cylinder bridge L2:   1.5075838091082052
best alignment replay L2:                 1.0629842444792676
grid-aware run-089 replay L2:             0.5800814918790829
best grid-aware variant:                  receiver_conjugate_div_source
target cells:                             753
selected frequency bins:                  17
interface items:                          8
contract gates:                           6
adapter contract ready:                   true
ready for adapter smoke:                  true
ready for half-space promotion:           false
ready for outputs/experiments promotion:  false
ready for field transfer:                 false
ready for 3D validation:                  false
ready for GPU work:                       false
```

Required interface items:

```text
project_grid_target_cells
target_cell_weights
tx_background_field_at_cells
rx_background_field_at_cells
source_spectrum
grid_aware_scattering_formula
per_frequency_complex_scale_policy
adapter_output_frequency_bins
```

Gate summary:

| Gate | Source run | Value | Status |
| --- | --- | ---: | --- |
| continuous analytic-cylinder bridge | 089 | 1.5075838091082052 | fail |
| simple alignment replay | 090 | 1.0629842444792676 | fail |
| grid-aware run-089 replay | 091 | 0.5800814918790829 | pass |
| adapter contract schema | 092 | 8 items | pass |
| half-space or layered promotion | - | - | blocked |
| field/archive/3D/GPU claim | - | - | blocked |

## Interpretation

The current positive path is not a raw continuous-BEM replacement of the
project-core traces. The accepted path is a grid-aware adapter: target cells,
target-cell weights, Tx/Rx fields at those cells, selected frequency bins, and
a controlled per-frequency calibration policy.

This contract protects the narrow result from overclaiming. It permits a
smoke implementation of the reusable adapter, but it does not permit
half-space promotion, field transfer, historical archive promotion, 3D
validation, or GPU work.

## Decision

Use this as the implementation contract for the next duplicated-script smoke
run. The next branch should prove that a reusable adapter can emit the eight
interface quantities and replay the run `091` gate before testing fresh
geometries or layered cases.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test:

```text
scripts/run_project_core_run089_grid_aware_adapter_contract.py
scripts/test_project_core_run089_grid_aware_adapter_contract.py
scripts/script_snapshot_manifest.json
```

Recorded SHA-256 values:

```text
run_project_core_run089_grid_aware_adapter_contract.py
bbf7fc0c9d4151091a526ded5befc3ceeafcb57e3e6c6c3e0e1e030024ece34e

test_project_core_run089_grid_aware_adapter_contract.py
1db2173c152ffa87b0b80ba180e157dbeb2b93840d65bd32024d79834391d6b6
```

## Validation

Focused tests:

```text
tests/test_project_core_run089_grid_aware_adapter_contract.py
3 passed
```

Figure check:

```text
project_core_run089_grid_aware_adapter_contract.png  2315x772, dynamic range=255
```
