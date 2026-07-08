# BEM Experiment 904: Panel 116 Worst-Bin Post-Antisymmetric Pair-Pruning Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Sensitivity-test the run `903` validator against damaged row shape, false
target closure, weakened budget arithmetic, figure/script damage, and
premature downstream-promotion flags.

## Output

```text
outputs/bem_experiments/904_scarep_2d_cpu_bem_panel116_worst_bin_post_antisymmetric_pair_pruning_scorecard_validation_sensitivity
```

## Result

```text
scenarios:                  15
expected pass:              1
expected fail:              14
observed pass:              1
observed fail:              14
unexpected outcomes:        0
damaged scenarios rejected: 14
sensitivity ready:          true
```

## Interpretation

Only the exact pair-pruning scorecard passes. The validator rejects false
target closure, row-count damage, weakened budget conditions, figure or script
snapshot damage, and any premature correction, field, project-comparison, GPU,
or 3D promotion.

## Decision

Use runs `902-904` as a guarded oracle-only pair-pruning block.

## Validation

Focused tests:

```text
16 passed
```

Figure check:

```text
2717x850, dynamic range=255
```
