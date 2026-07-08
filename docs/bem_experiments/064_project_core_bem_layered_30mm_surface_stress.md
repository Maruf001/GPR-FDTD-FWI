# BEM Experiment 064: Layered 30 mm Surface Stress

Date: 2026-06-25

## Purpose

Freshly stress-test the 7-sample `30mm_grid_only` layered surface policy found
in run `063`.

Run `063` showed that the 30 mm grid passed the original cached layered case
with L2 `0.704323503677739`. This run tests whether that compact policy
survives new layered project-core cases.

This is CPU-only project-core FDTD/BEM adapter validation. It does not use
field data, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/bem_experiments/064_project_core_bem_layered_30mm_surface_stress
```

Key artifacts:

```text
data/project_core_bem_layered_30mm_surface_stress.csv
data/project_core_bem_layered_30mm_surface_stress_summary.json
figures/project_core_bem_layered_30mm_surface_stress.png
docs/PROJECT_CORE_BEM_LAYERED_30MM_SURFACE_STRESS.md
```

## Result

```text
cases checked:                      4
ready cases:                        3
worst leave-one-scan L2:            0.8468025283677086
30 mm layered stress ready:         false
```

Case metrics:

| Case | epsr | x | z | Samples | LOO L2 | Ready |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| base_epsr9 | 9.0 | 0.13 | 0.09 | 7 | 0.704323503677739 | true |
| left_shift_epsr9 | 9.0 | 0.11 | 0.09 | 7 | 0.6161634288942388 | true |
| deep_z_epsr9 | 9.0 | 0.13 | 0.11 | 7 | 0.6750918323672064 | true |
| high_contrast_epsr12 | 12.0 | 0.13 | 0.09 | 7 | 0.8468025283677086 | false |

## Interpretation

The 7-sample 30 mm layered surface does not survive fresh layered stress. It
passes base, lateral-shifted, and deeper epsr-9 cases, but fails the epsr-12
high-contrast case.

The run `063` pass was therefore not enough for policy promotion.

## Decision

Keep the full 10 mm layered cache as the conservative default. Do not promote
30 mm layered sampling without additional repair or stress evidence.

This remains tabulated 2D project-core evidence only. It is not an analytic
layered Green replacement, measured-field claim, 3D claim, FWI launch gate, or
GPU/HPC escalation.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_layered_30mm_surface_stress.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_layered_30mm_surface_stress.py
pass
```

Figure check:

```text
project_core_bem_layered_30mm_surface_stress.png
1888x846, dynamic range=255
```
