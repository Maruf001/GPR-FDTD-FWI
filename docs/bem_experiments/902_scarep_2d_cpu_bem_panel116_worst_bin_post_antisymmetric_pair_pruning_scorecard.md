# BEM Experiment 902: Panel 116 Worst-Bin Post-Antisymmetric Pair-Pruning Scorecard

Date: 2026-07-01

## Purpose

Rank the remaining symmetric mirrored-pair residual after ideal antisymmetric
removal for the `2.3125 GHz` 116-panel worst bin.

This is an oracle pruning diagnostic. It does not promote a correction, hard
per-frequency endpoint, project-FDTD comparison, field transfer, or 3D/HPC
work.

## Output

```text
outputs/bem_experiments/902_scarep_2d_cpu_bem_panel116_worst_bin_post_antisymmetric_pair_pruning_scorecard
```

## Result

```text
post-antisymmetric remaining pair fraction:   0.2888732114593445
additional remaining pair fraction needed:    0.3927408115408598
top symmetric pair share of remaining:        0.5194987599183207
symmetric pair count needed to reach target:  1
target pair order:                            6
cumulative symmetric fraction at target:      0.5194987599183207
estimated relative L2 at target pruning:      0.000928076808180761
```

## Interpretation

After ideal antisymmetric removal, the remaining gap is concentrated in the
largest symmetric pair component. Pruning pair order `6` alone removes
`51.95%` of the post-antisymmetric residual, above the `39.27%` required, and
would estimate a worst-bin relative L2 of `0.000928076808180761`.

## Decision

Keep this as pair-level pruning evidence only. The result localizes the
remaining oracle gap but does not justify a physical correction or downstream
promotion.

## Validation

Focused tests:

```text
16 passed
```

Figure check:

```text
2104x846, dynamic range=255
```
