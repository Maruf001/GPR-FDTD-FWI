# BEM Experiment 896: Panel 116 Worst-Bin Pair-Removal Budget Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `895` validator.

## Output

```text
outputs/bem_experiments/896_scarep_2d_cpu_bem_panel116_worst_bin_pair_removal_budget_scorecard_validation_sensitivity
```

## Result

```text
source validator ready:       true
scenarios:                    17
expected pass scenarios:      1
expected fail scenarios:      16
observed pass scenarios:      1
observed fail scenarios:      16
unexpected outcomes:          0
damaged scenarios rejected:   16
```

Damaged states include readiness demotion, row/metric drift, false gap closure,
false correction promotion, false endpoint/project/field promotion,
GPU-priority promotion, figure damage, and snapshot damage.

## Decision

Use runs `894-896` as the guarded pair-removal budget block. Keep it
diagnostic-only.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_pair_removal_budget_scorecard_validation_sensitivity.py
3 passed
```

Figure check:

```text
2897x851, dynamic range=255
```
