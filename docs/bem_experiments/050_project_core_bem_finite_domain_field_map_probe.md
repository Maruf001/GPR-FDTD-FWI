# BEM Experiment 050: Finite-Domain Field-Map Probe

Date: 2026-06-25

## Purpose

Test whether a per-target-cell finite-domain transfer map can convert raw
analytic Green fields into project-domain target-cell fields under
leave-one-source validation.

This is a CPU-only field-map probe. It records project-core background
target-cell fields and compares them to analytic `scarep` Green fields. It does
not use field data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/050_project_core_bem_finite_domain_field_map_probe
```

Key artifacts:

```text
data/project_core_bem_finite_domain_field_map_probe.csv
data/project_core_bem_finite_domain_field_map_frequency.csv
data/project_core_bem_finite_domain_field_map_probe_summary.json
data/project_core_bem_finite_domain_field_map_probe_arrays.npz
figures/project_core_bem_finite_domain_field_map_probe.png
docs/PROJECT_CORE_BEM_FINITE_DOMAIN_FIELD_MAP_PROBE.md
```

## Result

```text
raw global field L2:                1.0419444002374967
raw per-source field L2:            0.817994101096804
raw leave-one-source field L2:      1.0723419515425194
per-cell all-source field L2:       0.7242401633347877
per-cell leave-one-source L2:       0.8005360330027802
finite-domain field map ready:      false
gpu required:                       false
```

## Interpretation

Per-cell finite-domain calibration substantially reduces the raw analytic-field
gap, but it does not generalize below the `0.75` gate under leave-one-source
validation.

This is a near miss, not a promotion.

## Decision

Do not replace the project-domain field table with raw or simply calibrated
analytic Green fields. The next diagnostic is a denser finite-domain calibration
surface to determine whether the remaining gap is sparse sampling or a deeper
field-model limit.

## Validation

```text
python -m py_compile run_project_core_bem_finite_domain_field_map_probe.py
python run_project_core_bem_finite_domain_field_map_probe.py
```

Figure check:

```text
project_core_bem_finite_domain_field_map_probe.png: 1673x788, dynamic range=255
```
