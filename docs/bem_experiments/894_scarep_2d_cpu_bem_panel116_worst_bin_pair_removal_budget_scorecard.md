# BEM Experiment 894: Panel 116 Worst-Bin Pair-Removal Budget Scorecard

Date: 2026-07-01

## Purpose

Quantify how much mirrored-pair residual energy must be removed for the
`2.3125 GHz` 116-panel worst bin to reach the `0.001` relative-L2 target.

This is an oracle budget diagnostic. It does not promote a correction, hard
per-frequency endpoint, project-FDTD comparison, field transfer, or 3D/HPC
work.

## Output

```text
outputs/bem_experiments/894_scarep_2d_cpu_bem_panel116_worst_bin_pair_removal_budget_scorecard
```

## Result

```text
target total energy fraction:                 0.2425540451374346
center floor energy fraction:                 0.08141503241185702
allowed pair energy fraction:                 0.16113901272557757
required pair removed fraction:               0.8245790880416128
antisymmetric removed pair fraction:          0.7111267885406555
symmetric removed pair fraction:              0.28887321145934464
gap after antisymmetric removal:              0.11345229950095737
remaining-pair fraction still needed:         0.3927408115408598
```

## Interpretation

The target requires removing `82.46%` of pair residual energy. Ideal
antisymmetric removal removes `71.11%`, leaving an `11.35` percentage-point
pair-removal gap. Closing the gap would require removing `39.27%` of the
remaining post-antisymmetric pair residual.

## Decision

Keep this as pair-removal budget evidence only. It narrows the residual
mechanism but does not justify a correction or downstream promotion.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_pair_removal_budget_scorecard.py
3 passed
```

Figure check:

```text
2536x875, dynamic range=255
```
