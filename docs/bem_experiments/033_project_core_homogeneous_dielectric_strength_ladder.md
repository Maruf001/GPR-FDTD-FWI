# BEM Experiment 033: Homogeneous Dielectric Strength Ladder

Date: 2026-06-25

## Purpose

Test whether the empirical direct-wave baseline from run `029` fixes
homogeneous target scattering for weaker dielectric contrasts.

This is an in-range CPU-only project-core FDTD ladder. It does not use field
data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/033_project_core_homogeneous_dielectric_strength_ladder
```

## Result

```text
epsr values:                       [1.25, 2.0, 4.0]
scan positions:                    5
best legacy scattered L2:          1.5415158197729195
best empirical scattered L2:       1.5332658067665847
worst empirical scattered L2:      1.6256015896432827
all empirical scattered ready:     false
any empirical scattered improves:  true
```

| epsr | Legacy scattered L2 | Empirical scattered L2 | Legacy total L2 | Empirical total L2 | Peak scattered |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1.25 | 1.5472037658996989 | 1.5332658067665847 | 0.2531760907824253 | 0.03651854818819029 | 0.0005043437377672006 |
| 2.0 | 1.6313894289625301 | 1.6256015896432827 | 0.2852526537141876 | 0.13899561896992846 | 0.0019199564388843707 |
| 4.0 | 1.5415158197729195 | 1.5524351934845986 | 0.4209214075178245 | 0.34919297169096886 | 0.005027122996891264 |

## Interpretation

Even weak target contrast fails in scattered-field comparison. The empirical
direct-wave baseline is useful for direct and total fields, but target
scattering remains wrong. The bridge blocker is now target-scattering transfer,
target rasterization/contrast, or the analytic-to-discrete target
representation.

## Decision

Stop direct-wave calibration work for now. The next BEM/project-core bridge
branch should audit discrete target representation and scattering, not source
normalization.

## Validation

```text
python -m py_compile run_project_core_homogeneous_dielectric_strength_ladder.py
python run_project_core_homogeneous_dielectric_strength_ladder.py
```

Figure check:

```text
project_core_homogeneous_dielectric_strength_ladder.png: nonblank
```
