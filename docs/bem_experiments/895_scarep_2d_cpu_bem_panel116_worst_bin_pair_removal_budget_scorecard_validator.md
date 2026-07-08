# BEM Experiment 895: Panel 116 Worst-Bin Pair-Removal Budget Scorecard Validator

Date: 2026-07-01

## Purpose

Validate run `894` from artifacts.

## Output

```text
outputs/bem_experiments/895_scarep_2d_cpu_bem_panel116_worst_bin_pair_removal_budget_scorecard_validator
```

## Result

```text
validation checks:                    5
passed checks:                        5
failed checks:                        0
required pair removed fraction:       0.8245790880416128
antisymmetric removed pair fraction:  0.7111267885406555
gap after antisymmetric removal:      0.11345229950095737
remaining-pair fraction still needed: 0.3927408115408598
```

## Interpretation

The pair-removal budget scorecard validates as an oracle-only gap diagnostic
with no correction or downstream promotion.

## Decision

Use run `895` as the consumer-facing guard for citing run `894`.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_pair_removal_budget_scorecard_validator.py
3 passed
```

Figure check:

```text
2105x784, dynamic range=255
```
