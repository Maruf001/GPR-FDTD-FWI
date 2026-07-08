# BEM Experiment 045: Green-Surface Offset Stress

Date: 2026-06-25

## Purpose

Stress-test the run `043` contract on Tx/Rx offset changes at epsr `4.0`.

This is a CPU-only stress test. It runs fresh project-core 2D FDTD target cases
for a bounded offset matrix, but it does not use field data, GPU work, FWI,
3D/HPC, neural networks, or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/045_project_core_bem_green_surface_offset_stress
```

Key artifacts:

```text
data/project_core_bem_green_surface_offset_stress.csv
data/project_core_bem_green_surface_offset_stress_summary.json
figures/project_core_bem_green_surface_offset_stress.png
docs/PROJECT_CORE_BEM_GREEN_SURFACE_OFFSET_STRESS.md
cases/offset_10mm_epsr4
cases/offset_30mm_epsr4
cases/offset_40mm_epsr4
```

## Result

```text
stress cases:                       3
worst interpolated-surface L2:      0.6858047703122613
worst exact-surface L2:             0.5561120922852676
worst project-grid best L2:         0.4475737608979965
offset stress ready:                true
gpu required:                       false
```

Stress metrics:

| Case | Offset m | Project-grid L2 | Interpolated surface L2 | Best variant | Ready |
| --- | ---: | ---: | ---: | --- | --- |
| offset_10mm_epsr4 | 0.01 | 0.41652920661270654 | 0.564376763207043 | receiver_conjugate_div_source | true |
| offset_30mm_epsr4 | 0.03 | 0.4475737608979965 | 0.6858047703122613 | receiver_conjugate_div_source | true |
| offset_40mm_epsr4 | 0.04 | 0.43534169321425303 | 0.5905234009631569 | product_div_source | true |

## Interpretation

The project-domain target-cell Green surface remains inside the adapter gate
for the tested Tx/Rx offsets at epsr `4.0`. This expands the contract beyond
the original 20 mm offset.

It does not yet cover layered/half-space media, BEM-derived replacement of the
project-domain field table, field provenance, or 3D finite-rebar modeling.

## Decision

Keep the project-domain surface as the active BEM/project-core bridge. The next
limit is layered/half-space media or BEM-derived replacement of the
project-domain field table.

## Validation

```text
python -m py_compile run_project_core_bem_green_surface_offset_stress.py
python run_project_core_bem_green_surface_offset_stress.py
```

Figure check:

```text
project_core_bem_green_surface_offset_stress.png: 1925x823, dynamic range=255
```
