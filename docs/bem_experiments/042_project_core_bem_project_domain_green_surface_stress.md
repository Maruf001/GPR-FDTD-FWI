# BEM Experiment 042: Project-Domain Green Surface Stress

Date: 2026-06-25

## Purpose

Create fresh project-core target cases for a denser scan and shifted
high-contrast targets, then apply the run `041` target-cell Green-surface gate.

This is a CPU-only stress test. It runs fresh project-core 2D FDTD cases for
the bounded stress matrix, but it does not use field data, GPU work, FWI,
3D/HPC, neural networks, or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/042_project_core_bem_project_domain_green_surface_stress
```

Key artifacts:

```text
data/project_core_bem_project_domain_green_surface_stress.csv
data/project_core_bem_project_domain_green_surface_stress_summary.json
figures/project_core_bem_project_domain_green_surface_stress.png
docs/PROJECT_CORE_BEM_PROJECT_DOMAIN_GREEN_SURFACE_STRESS.md
cases/center_dense_epsr4
cases/left_shift_epsr4
cases/right_shift_epsr4
```

## Result

```text
stress cases:                       3
worst interpolated-surface L2:      0.5974979747759482
worst exact-surface L2:             0.5877080274855739
worst project-grid best L2:         0.47273720520920215
stress gate ready:                  true
gpu required:                       false
```

Stress metrics:

| Case | Scan count | Cylinder x | Project-grid L2 | Interpolated surface L2 | Best variant | Ready |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| center_dense_epsr4 | 7 | 0.13 | 0.4562437767492717 | 0.5902462225466304 | product_div_source | true |
| left_shift_epsr4 | 5 | 0.11 | 0.4282834683853741 | 0.5851469164265751 | product_div_source | true |
| right_shift_epsr4 | 5 | 0.15 | 0.47273720520920215 | 0.5974979747759482 | product_div_source | true |

## Interpretation

The project-domain target-cell Green surface remains inside the adapter gate
for a denser high-contrast scan and shifted high-contrast targets.

This strengthens the run `041` bridge: finite-domain target-cell surfaces are a
usable BEM/project-core coupling path for the tested 2D cases. It does not yet
justify field, 3D, or inversion claims.

## Decision

Keep the project-domain surface as the active bridge. The next branch should
package the reusable surface contract and define limits before connecting it to
field or 3D BEM/FDTD claims.

## Validation

```text
python -m py_compile run_project_core_bem_project_domain_green_surface_stress.py
python run_project_core_bem_project_domain_green_surface_stress.py
```

Figure check:

```text
project_core_bem_project_domain_green_surface_stress.png: 1979x843, dynamic range=255
```
