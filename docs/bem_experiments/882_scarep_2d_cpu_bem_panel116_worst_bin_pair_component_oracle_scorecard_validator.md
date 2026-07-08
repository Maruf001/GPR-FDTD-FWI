# BEM Experiment 882: Panel-116 Worst-Bin Pair-Component Oracle Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `881` pair-component oracle scorecard.

The validator checks source readiness, scenario row shape, antisymmetric-only
no-repair behavior, the nonphysical all-pair lower-bound pass, blocked
downstream claim flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/882_scarep_2d_cpu_bem_panel116_worst_bin_pair_component_oracle_scorecard_validator
```

## Result

```text
validation checks:                         6
checks passed:                             6
checks failed:                             0
pair rows:                                 6
score rows:                                4
frequency:                                 2.3125 GHz
full relative L2:                          0.0020304660813910734
antisymmetric-removed relative L2:         0.001195683569955468
symmetric-removed relative L2:             0.0017403420910436734
all-pair removed center-only relative L2:  0.0005793593752068725
target requires more than antisym removal: true
project FDTD comparison ready:             false
real 3D validation ready:                  false
field transfer ready:                      false
```

## Decision

Use run `881` as a guarded oracle no-repair result for antisymmetric-only
pair-component removal.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_pair_component_oracle_scorecard_validator.py
3 passed
```

Figure check:

```text
2429x859, dynamic range=255
```
