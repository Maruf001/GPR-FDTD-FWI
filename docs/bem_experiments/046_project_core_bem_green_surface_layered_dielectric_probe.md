# BEM Experiment 046: Green-Surface Layered Dielectric Probe

Date: 2026-06-25

## Purpose

Probe the project-domain Green-surface bridge in an air/concrete layered
project-core case with a dielectric inclusion in concrete.

This is a CPU-only layered-media probe. It runs fresh project-core 2D FDTD
background and target traces plus layered background target-cell field
recordings. It does not use field data, GPU work, FWI, 3D/HPC, neural networks,
or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/046_project_core_bem_green_surface_layered_dielectric_probe
```

Key artifacts:

```text
data/project_core_bem_green_surface_layered_dielectric_probe.csv
data/project_core_bem_green_surface_layered_dielectric_probe_summary.json
data/project_core_bem_green_surface_layered_dielectric_probe_arrays.npz
figures/project_core_bem_green_surface_layered_dielectric_probe.png
docs/PROJECT_CORE_BEM_GREEN_SURFACE_LAYERED_DIELECTRIC_PROBE.md
```

## Result

```text
best all-scan L2:                   0.5220233499204818
best exact-surface LOO L2:          0.619762715748986
best interpolated-surface LOO L2:   1.1770012780031571
layered dielectric ready:           false
target cells:                       533
surface samples:                    10
edge extrapolated points:           4
gpu required:                       false
```

## Interpretation

The layered dielectric target-scattering operator is not the primary failure:
all-scan and exact leave-one-scan target-cell surface gates stay below `0.75`.

The sparse interpolated surface gate fails. The likely blocker is the target-cell
field surface interpolation across the air/concrete interface geometry,
especially at held-out edge points.

## Decision

Do not promote the contract into layered media yet. Diagnose whether denser
target-cell surface sampling fixes the interpolation failure before testing
field, 3D, or BEM-derived replacement claims.

## Validation

```text
python -m py_compile run_project_core_bem_green_surface_layered_dielectric_probe.py
python run_project_core_bem_green_surface_layered_dielectric_probe.py
```

Figure check:

```text
project_core_bem_green_surface_layered_dielectric_probe.png: 1817x770, dynamic range=255
```
