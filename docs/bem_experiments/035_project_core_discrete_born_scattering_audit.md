# BEM Experiment 035: Project-Core Discrete Born Scattering Audit

Date: 2026-06-25

## Purpose

Test whether a grid-aware first-order Born-style surrogate built from
project-core background fields at the actual target cells explains the weak
in-range dielectric scattered response.

This run uses project-core FDTD background recordings and the actual rasterized
target cells. It does not use field data, GPU work, FWI, 3D/HPC, neural
networks, or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/035_project_core_discrete_born_scattering_audit
```

Key artifacts:

```text
data/project_core_discrete_born_scattering_variants.csv
data/project_core_discrete_born_scattering_frequency.csv
data/project_core_discrete_born_scattering_summary.json
figures/project_core_discrete_born_scattering_audit.png
docs/PROJECT_CORE_DISCRETE_BORN_SCATTERING_AUDIT.md
```

## Result

```text
cylinder epsr:                     1.25
target cell count:                 533
legacy analytic time L2:           1.5472037658996989
best Born variant:                 product_div_source
best Born time L2:                 0.0989465314024021
best Born spectral L2:             0.09894653140240213
discrete Born scattering ready:    true
```

| Variant | Scattered time L2 | Improves over analytic |
| --- | ---: | --- |
| analytic cylinder direct-calibrated | 1.5472037658996989 | false |
| product / source | 0.0989465314024021 | true |
| product, no source division | 0.09894653140240213 | true |
| receiver-conjugate / source | 0.6019464335550444 | true |

## Interpretation

This is the first positive target-scattering bridge result. The project-core
weak dielectric target scattering is explained when the surrogate uses the
actual project-grid background fields and rasterized target cells.

The earlier failure was not direct-wave normalization, gross target geometry,
or FDTD target physics. It was the continuous analytic-cylinder to discrete
project-grid scattering bridge.

## Decision

Use this as the current positive scattering-operator checkpoint. The next
branch is a discrete Born strength ladder.

## Validation

```text
python -m py_compile run_project_core_discrete_born_scattering_audit.py
python run_project_core_discrete_born_scattering_audit.py
```

Figure check:

```text
project_core_discrete_born_scattering_audit.png: 2533x712, dynamic range=255
```

