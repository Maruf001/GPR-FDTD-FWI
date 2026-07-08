# BEM Experiment 055: Boundary-Image Ladder

Date: 2026-06-25

## Purpose

Test whether low-order finite-domain image-source corrections can close the
project-domain target-cell field-table replacement gap.

This is a CPU-only boundary-convention audit. It fits direct, vertical,
horizontal, and cardinal image-source component models under held-out source
validation. It does not use field data, GPU work, FWI, 3D/HPC, neural networks,
or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/055_project_core_bem_boundary_image_ladder
```

Key artifacts:

```text
data/project_core_bem_boundary_image_ladder.csv
data/project_core_bem_boundary_image_ladder_summary.json
figures/project_core_bem_boundary_image_ladder.png
docs/PROJECT_CORE_BEM_BOUNDARY_IMAGE_LADDER.md
```

## Result

```text
variants checked:                   36
best global image LOO L2:           0.3301113956330722
best per-cell image LOO L2:         0.1228536659883146
best global variant:                z=0.054 m, speed_scale=1.05, cardinal
best per-cell variant:              z=0.046 m, speed_scale=1.05, cardinal
boundary image ready:               true
gpu required:                       false
```

## Interpretation

A low-order boundary-image model closes the held-out field-table gate. This is
the first BEM-derived field-table replacement candidate that beats the `0.75`
gate.

The result does not yet prove a target-scattering replacement. It only proves a
field-table replacement candidate.

## Decision

Promote the best boundary-image model to a scattering replay gate before any
BEM field-table replacement claim.

## Validation

```text
python -m py_compile run_project_core_bem_boundary_image_ladder.py
python run_project_core_bem_boundary_image_ladder.py
```

Figure check:

```text
project_core_bem_boundary_image_ladder.png: 1891x1093, dynamic range=255
```
