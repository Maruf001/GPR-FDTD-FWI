# BEM Experiment 054: Source-Convention Ladder

Date: 2026-06-25

## Purpose

Test whether simple analytic-source convention choices can close the
project-domain target-cell field-table replacement gap.

This is a CPU-only source-convention audit. It evaluates source height,
effective wave speed, scalar source spectrum, and distance-regularization
variants against the same project-domain target-cell field table. It does not
use field data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/054_project_core_bem_source_convention_ladder
```

Key artifacts:

```text
data/project_core_bem_source_convention_ladder.csv
data/project_core_bem_source_convention_ladder_summary.json
figures/project_core_bem_source_convention_ladder.png
docs/PROJECT_CORE_BEM_SOURCE_CONVENTION_LADDER.md
```

## Result

```text
variants checked:                   48
best per-cell leave-one-source L2:  0.7871631960439586
best global leave-one-source L2:    1.0589085317457976
best source z:                      0.046 m
best speed scale:                   1.05
best factor mode:                   ricker
source convention ready:            false
gpu required:                       false
```

## Interpretation

No simple source height, scalar source spectrum, effective wave speed, or
distance-regularization choice closes the held-out field-table gate.

The source-factor mode itself is absorbed by per-frequency scaling and does not
solve the spatial field-table mismatch.

## Decision

Do not spend more effort on scalar source-convention tweaks. The BEM replacement
needs a model with finite-domain boundary/source physics, or the project-domain
field table must remain the bridge.

## Validation

```text
python -m py_compile run_project_core_bem_source_convention_ladder.py
python run_project_core_bem_source_convention_ladder.py
```

Figure check:

```text
project_core_bem_source_convention_ladder.png: 1873x1093, dynamic range=255
```
