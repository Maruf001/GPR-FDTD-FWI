# BEM Experiment 037: BEM Scattering Adapter Contract

Date: 2026-06-25

## Purpose

Turn the positive grid-aware Born result from runs `035`-`036` into an
implementation contract for the next BEM/project-core bridge adapter.

This is a design artifact. It does not run FDTD time stepping, field data, GPU
work, FWI, 3D/HPC, neural networks, or the historical `outputs/experiments`
archive.

## Output

```text
outputs/bem_experiments/037_project_core_bem_scattering_adapter_contract
```

Key artifacts:

```text
data/project_core_bem_scattering_adapter_interface.csv
data/project_core_bem_scattering_adapter_gates.csv
data/project_core_bem_scattering_adapter_contract_summary.json
figures/project_core_bem_scattering_adapter_contract.png
docs/PROJECT_CORE_BEM_SCATTERING_ADAPTER_CONTRACT.md
```

## Result

```text
source run:                         outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
epsr values passed:                 [1.25, 2.0, 4.0]
worst discrete Born L2:             0.44601690298659386
interface items:                    7
gates:                              5
adapter contract ready:             true
```

The required adapter interface items are:

```text
project_grid_target_cells
target_cell_weights
tx_background_field_at_cells
rx_background_field_at_cells
source_spectrum
scattering_formula_variants
per_frequency_complex_scale
```

## Interpretation

The next BEM bridge should not compare continuous target scattering directly to
project-core traces. It should first produce project-grid target-cell
quantities compatible with the discrete Born operator that passed in run `036`.

## Decision

Use this contract as the implementation target for the next bridge adapter.
Field, historical synthetic 2D archive, and 3D claims remain blocked until the
adapter passes matched project-core cases.

## Validation

```text
python -m py_compile run_project_core_bem_scattering_adapter_contract.py
python run_project_core_bem_scattering_adapter_contract.py
```

Figure check:

```text
project_core_bem_scattering_adapter_contract.png: nonblank
```
