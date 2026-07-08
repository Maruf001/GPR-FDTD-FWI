# BEM Experiment 881: Panel-116 Worst-Bin Pair-Component Oracle Scorecard

Date: 2026-07-01

## Purpose

Check whether an ideal removal of the antisymmetric mirrored-pair residual
component would repair the remaining `2.3125 GHz` worst-bin mismatch.

This run reads the saved run `878` receiver-pair symmetry audit and its
validator/sensitivity runs `879-880`. It does not rerun BEM, project FDTD,
field processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/881_scarep_2d_cpu_bem_panel116_worst_bin_pair_component_oracle_scorecard
```

## Result

```text
source pair audit ready:                 true
source validation ready:                 true
source sensitivity ready:                true
pair rows:                               6
score rows:                              4
frequency:                               2.3125 GHz
target relative L2:                      0.001
full relative L2:                        0.0020304660813910734
antisymmetric-removed relative L2:       0.001195683569955468
symmetric-removed relative L2:           0.0017403420910436734
all-pair removed center-only relative L2: 0.0005793593752068725
target residual-energy fraction:         0.2425540451374346
antisymmetric-removed energy fraction:   0.3467696219973218
antisymmetric-only oracle passes target: false
all-pair oracle passes target:           true
correction promoted:                     false
project FDTD comparison ready:           false
field transfer ready:                    false
3D validation ready:                     false
```

## Interpretation

Even a perfect antisymmetric-pair residual removal leaves the worst bin above
target. Only the nonphysical lower bound that removes all paired residual and
keeps the center receiver residual passes the target.

## Decision

Keep pair-component removal as oracle diagnostic evidence only. Do not promote
a pair-component correction, hard per-frequency endpoint, project-FDTD
comparison, field transfer, or 3D/HPC claim from this run.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_pair_component_oracle_scorecard.py
3 passed
```

Figure check:

```text
2068x840, dynamic range=255
```
