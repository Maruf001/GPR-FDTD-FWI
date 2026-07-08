# BEM Experiment 036: Project-Core Discrete Born Strength Ladder

Date: 2026-06-25

## Purpose

Test how far the grid-aware Born surrogate from run `035` remains useful as
homogeneous dielectric target contrast increases.

This is a CPU-only project-core FDTD/Born ladder. It does not use field data,
GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
```

Key artifacts:

```text
data/project_core_discrete_born_strength_ladder.csv
data/project_core_discrete_born_strength_ladder_summary.json
figures/project_core_discrete_born_strength_ladder.png
cases/epsr_1p25
cases/epsr_2p0
cases/epsr_4p0
```

## Result

```text
epsr values:                       [1.25, 2.0, 4.0]
scan positions:                    5
best Born time L2:                 0.0989465314024021
worst Born time L2:                0.44601690298659386
ready epsr count:                  3 / 3
all discrete Born ready:           true
```

| epsr | Analytic scattered L2 | Best Born L2 | Best Born variant | Ready |
| ---: | ---: | ---: | --- | --- |
| 1.25 | 1.5472037658996989 | 0.0989465314024021 | product_div_source | true |
| 2.0 | 1.6313894289625301 | 0.23018542478328735 | product_div_source | true |
| 4.0 | 1.5415158197729195 | 0.44601690298659386 | receiver_conjugate_div_source | true |

## Interpretation

The grid-aware Born surrogate stays inside the acceptance gate for all tested
dielectric contrasts. This is a strong project-core bridge result: target
scattering can be explained when modeled on the project grid, while the
continuous analytic-cylinder bridge fails.

## Decision

Use this as the current scattering-operator checkpoint. The next BEM bridge
step should translate the continuous BEM target representation into a
project-grid-aware scattering/operator adapter rather than revisiting
direct-wave calibration.

## Validation

```text
python -m py_compile run_project_core_discrete_born_strength_ladder.py
python run_project_core_discrete_born_strength_ladder.py
```

Figure check:

```text
project_core_discrete_born_strength_ladder.png: nonblank
```
