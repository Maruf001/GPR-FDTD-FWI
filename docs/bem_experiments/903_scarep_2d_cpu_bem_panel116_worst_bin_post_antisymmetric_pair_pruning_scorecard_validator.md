# BEM Experiment 903: Panel 116 Worst-Bin Post-Antisymmetric Pair-Pruning Scorecard Validator

Date: 2026-07-01

## Purpose

Validate run `902` as an oracle-only pair-pruning diagnostic with stable row
shape, budget arithmetic, figure output, script snapshots, and blocked
downstream-promotion flags.

## Output

```text
outputs/bem_experiments/903_scarep_2d_cpu_bem_panel116_worst_bin_post_antisymmetric_pair_pruning_scorecard_validator
```

## Result

```text
validation checks:          5
passed checks:              5
failed checks:              0
pair rows:                  6
pairs needed to target:     1
estimated target L2:        0.000928076808180761
validation ready:           true
```

## Interpretation

The validator accepts the pair-pruning scorecard as a guarded oracle result:
the largest remaining symmetric pair component is sufficient to close the
post-antisymmetric budget gap, but no correction, project comparison, field,
or 3D claim is promoted.

## Decision

Use run `902` as guarded pair-level pruning evidence only.

## Validation

Focused tests:

```text
16 passed
```

Figure check:

```text
2105x784, dynamic range=255
```
