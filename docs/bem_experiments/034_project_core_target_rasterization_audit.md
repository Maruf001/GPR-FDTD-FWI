# BEM Experiment 034: Project-Core Target Rasterization Audit

Date: 2026-06-25

## Purpose

Check whether the target-scattering failure from runs `032`-`033` can be
explained by gross circular-target rasterization error in the project-core
material grid.

This is a CPU-only material-grid audit. It does not run FDTD time stepping,
field data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/034_project_core_target_rasterization_audit
```

Key artifacts:

```text
data/project_core_target_rasterization_audit.csv
data/project_core_target_rasterization_summary.json
figures/project_core_target_rasterization_audit.png
docs/PROJECT_CORE_TARGET_RASTERIZATION_AUDIT.md
```

## Result

```text
subcell samples tested:           [1, 3, 5, 7, 9]
cylinder center:                  x=0.13 m, z=0.16 m
cylinder radius:                  0.025 m
grid spacing:                     0.002 m x 0.002 m
best radius error:                0.0013260133260549478 mm
worst radius error:               0.04776287834105941 mm
best centroid error:              0.0 mm
worst centroid error:             5.551115123125783e-14 mm
rasterization geometry ready:     true
```

## Interpretation

The in-range target is geometrically well represented on the project-core
material grid. The scattering failure from runs `032`-`033` is not explained by
gross area, equivalent-radius, or centroid error in the circular target
rasterization.

## Decision

Stop treating simple target geometry as the active blocker. The next
BEM/project-core bridge work should audit the discrete target-scattering
operator itself, such as a grid-aware/Born-style target surrogate or a
cell-level scattering comparison.

## Validation

```text
python -m py_compile run_project_core_target_rasterization_audit.py
python run_project_core_target_rasterization_audit.py
```

Figure check:

```text
project_core_target_rasterization_audit.png: nonblank
```
