# BEM Experiment 168: Layered Payload Extended Stress Design Contract

Date: 2026-06-27

## Purpose

Define the next extended stress ladder for the scoped layered payload branch.

Run `167` identified Green-function/interface physics as the primary BEM
development branch. This run fixes four extended layered stress cases before
spending CPU on execution.

This is a CPU-only design contract. It does not rerun FDTD or BEM solvers,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/168_project_core_bem_layered_payload_extended_stress_design_contract
```

Key artifacts:

```text
data/project_core_bem_layered_payload_extended_stress_design_cases.csv
data/project_core_bem_layered_payload_extended_stress_design_contract_summary.json
figures/project_core_bem_layered_payload_extended_stress_design_contract.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_EXTENDED_STRESS_DESIGN_CONTRACT.md
scripts/run_project_core_bem_layered_payload_extended_stress_design_contract.py
scripts/test_project_core_bem_layered_payload_extended_stress_design_contract.py
```

## Result

```text
extended cases:                    4
acceptance L2:                     0.75
varied dimensions:                 cylinder_epsr;cylinder_radius_m;cylinder_z_m;lower_epsr
ready for execution:               true
layered payload claim ready:       false
project-core bridge ready:         false
3D validation ready:               false
field FWI ready:                   false
GPU/HPC ready:                     false
```

| Case | Purpose | z m | radius m | target epsr | lower epsr |
| --- | --- | ---: | ---: | ---: | ---: |
| shallow_z_epsr9 | test shallower target coupling near the interface | 0.075 | 0.025 | 9.0 | 6.0 |
| larger_radius_epsr9 | test larger target footprint with same dielectric contrast | 0.09 | 0.035 | 9.0 | 6.0 |
| low_contrast_epsr6 | test lower target contrast | 0.09 | 0.025 | 6.0 | 6.0 |
| high_interface_epsr12 | test stronger lower-halfspace dielectric contrast | 0.09 | 0.025 | 9.0 | 12.0 |

## Interpretation

The extended stress ladder is defined across target depth, target radius,
target contrast, and lower-halfspace contrast. It is ready to execute as a
scoped layered 2D payload stress test.

## Decision

Run this extended ladder before making any broader layered payload claim. Keep
project-core bridge promotion, measured-field transfer, 3D validation, GPU/HPC,
and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_extended_stress_design_contract.py
3 passed
```

Figure validation:

```text
project_core_bem_layered_payload_extended_stress_design_contract.png
2896x844, dynamic range=255
```
