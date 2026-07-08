# BEM Experiment 038: BEM Scattering Adapter Smoke Test

Date: 2026-06-25

## Purpose

Turn the run `037` BEM/project-grid scattering adapter contract into an
executable smoke test using the run `036` discrete Born ladder artifacts.

This is a contract validation artifact. It does not run FDTD time stepping,
field data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/038_project_core_bem_scattering_adapter_smoke
```

Key artifacts:

```text
data/project_core_bem_scattering_adapter_interface_check.csv
data/project_core_bem_scattering_adapter_smoke_metrics.csv
data/project_core_bem_scattering_adapter_smoke_summary.json
figures/project_core_bem_scattering_adapter_smoke.png
docs/PROJECT_CORE_BEM_SCATTERING_ADAPTER_SMOKE.md
```

## Result

```text
contract run:                       outputs/bem_experiments/037_project_core_bem_scattering_adapter_contract
source run:                         outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
cases checked:                      3
interface items checked:            7
missing interface items:            0
worst selected adapter L2:          0.44601690298659386
adapter smoke ready:                true
```

Selected adapter metrics:

| epsr | Selected variant | Selected L2 |
| ---: | --- | ---: |
| 1.25 | product_div_source | 0.0989465314024021 |
| 2.0 | product_div_source | 0.23018542478328735 |
| 4.0 | receiver_conjugate_div_source | 0.44601690298659386 |

## Interpretation

The run `037` adapter contract can be replayed as an executable schema over
the run `036` cases. This is still using project-core generated fields, but it
gives the BEM side a concrete interface and acceptance gate.

## Decision

Use this smoke test as the adapter harness. The next implementation step is to
replace the project-core generated target-cell fields with BEM-derived or
BEM-compatible fields while keeping the same interface and gates.

## Validation

```text
python -m py_compile run_project_core_bem_scattering_adapter_smoke.py
python run_project_core_bem_scattering_adapter_smoke.py
```

Figure check:

```text
project_core_bem_scattering_adapter_smoke.png: 1708x769, dynamic range=255
```
