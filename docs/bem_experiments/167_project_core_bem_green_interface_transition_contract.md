# BEM Experiment 167: Green/Interface Transition Contract

Date: 2026-06-27

## Purpose

Convert the fresh-case local-operator no-go into the next BEM transition
contract.

Run `166` showed that local scale, delay, target-weight, aperture, and trimming
variants do not close the project-core bridge. This run combines that decision
with the existing layered 2D payload and 3D external-FDTD request checkpoints.

This is a CPU-only synthesis from saved BEM-track artifacts. It does not rerun
FDTD or BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/167_project_core_bem_green_interface_transition_contract
```

Key artifacts:

```text
data/project_core_bem_green_interface_transition_rows.csv
data/project_core_bem_green_interface_transition_contract_summary.json
figures/project_core_bem_green_interface_transition_contract.png
docs/PROJECT_CORE_BEM_GREEN_INTERFACE_TRANSITION_CONTRACT.md
scripts/run_project_core_bem_green_interface_transition_contract.py
scripts/test_project_core_bem_green_interface_transition_contract.py
```

## Result

```text
transition tracks:                   4
scoped-ready tracks:                 3
next-experiment-ready tracks:        4
local operator tweaks exhausted:     true
layered payload scoped ready:        true
external 3D request ready:           true
real external 3D data present:       false
primary next branch:                 green_function_interface_physics_update
parallel next branch:                external_3d_fdtd_return_acquisition
project-core bridge ready:           false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
```

## Interpretation

The BEM path now has a clear split: local homogeneous tweaks are exhausted,
layered 2D payloads are scoped-ready, and the 3D validation path is ready for
external FDTD data but does not yet have real returns.

## Decision

Make Green-function/interface physics the primary BEM development branch and
pursue external 3D FDTD returns in parallel. Keep project-core bridge
promotion, 3D validation, GPU/HPC, and field FWI blocked until those gates
close.

## Validation

Focused tests:

```text
tests/test_project_core_bem_green_interface_transition_contract.py
2 passed
```

Figure validation:

```text
project_core_bem_green_interface_transition_contract.png
2897x859, dynamic range=255
```
