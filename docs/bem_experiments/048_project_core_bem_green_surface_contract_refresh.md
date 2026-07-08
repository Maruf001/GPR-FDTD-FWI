# BEM Experiment 048: Green-Surface Contract Refresh

Date: 2026-06-25

## Purpose

Refresh the Green-surface adapter contract after geometry, offset, and
layered-media stress probes.

This is a CPU-only packaging artifact. It does not run FDTD time stepping,
field data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/048_project_core_bem_green_surface_contract_refresh
```

Key artifacts:

```text
data/project_core_bem_green_surface_contract_refresh_gates.csv
data/project_core_bem_green_surface_contract_refresh_requirements.csv
data/project_core_bem_green_surface_contract_refresh_summary.json
figures/project_core_bem_green_surface_contract_refresh.png
docs/PROJECT_CORE_BEM_GREEN_SURFACE_CONTRACT_REFRESH.md
```

## Result

```text
contract ready:                     true
homogeneous extension ready:        true
layered conditional ready:          true
field claim ready:                  false
3D claim ready:                     false
gpu required:                       false
```

Gate summary:

| Gate | Run | Value | Status |
| --- | --- | ---: | --- |
| geometry_depth_radius_stress | 044 | 0.6390901970749561 | pass |
| tx_rx_offset_stress | 045 | 0.6858047703122613 | pass |
| layered_sparse_surface | 046 | 1.1770012780031571 | fail |
| layered_dense_surface | 047 | 0.697021169360853 | pass |
| field_claim |  |  | blocked |
| 3d_claim |  |  | blocked |

## Interpretation

The Green-surface contract now covers the tested homogeneous 2D geometry,
offset, depth, and radius envelope. Layered media are conditionally supported
only when the target-cell surface is densely sampled with no edge extrapolation.

## Decision

Use this as the current contract. The next BEM-side improvement is to test
whether BEM-derived fields can reproduce the project-domain target-cell
surface. Field and 3D claims remain blocked.

## Validation

```text
python -m py_compile run_project_core_bem_green_surface_contract_refresh.py
python run_project_core_bem_green_surface_contract_refresh.py
```

Figure check:

```text
project_core_bem_green_surface_contract_refresh.png: 1747x787, dynamic range=255
```
