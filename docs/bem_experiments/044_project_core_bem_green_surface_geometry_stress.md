# BEM Experiment 044: Green-Surface Geometry Stress

Date: 2026-06-25

## Purpose

Stress-test the run `043` contract on target depth and radius changes at
epsr `4.0`.

This is a CPU-only stress test. It runs fresh project-core 2D FDTD target cases
for a bounded geometry matrix, but it does not use field data, GPU work, FWI,
3D/HPC, neural networks, or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/044_project_core_bem_green_surface_geometry_stress
```

Key artifacts:

```text
data/project_core_bem_green_surface_geometry_stress.csv
data/project_core_bem_green_surface_geometry_stress_summary.json
figures/project_core_bem_green_surface_geometry_stress.png
docs/PROJECT_CORE_BEM_GREEN_SURFACE_GEOMETRY_STRESS.md
cases/shallow_z_epsr4
cases/deep_z_epsr4
cases/small_radius_epsr4
cases/large_radius_epsr4
```

## Result

```text
stress cases:                       4
worst interpolated-surface L2:      0.6390901970749561
worst exact-surface L2:             0.560834960421517
worst project-grid best L2:         0.4676059535354029
geometry stress ready:              true
gpu required:                       false
```

Stress metrics:

| Case | z | radius | target cells | Project-grid L2 | Interpolated surface L2 | Best variant | Ready |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| shallow_z_epsr4 | 0.14 | 0.025 | 533 | 0.4676059535354029 | 0.6390901970749561 | product_div_source | true |
| deep_z_epsr4 | 0.18 | 0.025 | 533 | 0.43263904624975796 | 0.5362009817623262 | receiver_conjugate_div_source | true |
| small_radius_epsr4 | 0.16 | 0.02 | 349 | 0.33350467631625413 | 0.5277711345643809 | product_no_div | true |
| large_radius_epsr4 | 0.16 | 0.03 | 753 | 0.406172653375023 | 0.5155175528128514 | receiver_conjugate_div_source | true |

## Interpretation

The project-domain target-cell Green surface remains inside the adapter gate
for the tested depth and radius changes at epsr `4.0`.

This extends the contract beyond lateral shifts and denser scan positions. It
does not yet cover Tx/Rx offset variation, layered media, field provenance, or
3D finite-rebar modeling.

## Decision

Keep the project-domain surface as the active BEM/project-core bridge. The next
limit to test is Tx/Rx offset variation or layered/half-space media.

## Validation

```text
python -m py_compile run_project_core_bem_green_surface_geometry_stress.py
python run_project_core_bem_green_surface_geometry_stress.py
```

Figure check:

```text
project_core_bem_green_surface_geometry_stress.png: 2022x861, dynamic range=255
```
