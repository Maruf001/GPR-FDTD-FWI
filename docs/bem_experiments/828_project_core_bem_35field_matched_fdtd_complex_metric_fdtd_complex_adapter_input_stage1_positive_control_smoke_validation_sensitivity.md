# BEM Experiment 828: Complex FDTD Adapter Input Stage-1 Positive Control Smoke Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `827` validator with damaged versions of the run `826`
stage-1 positive-control state.

Damaged cases include policy-label damage, row rejection, full-row-count
damage, synthetic-flag damage, full-input promotion, external-file promotion,
real-acceptance promotion, comparison promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/bem_experiments/828_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke_validation_sensitivity
```

## Result

```text
scenarios:                         11
expected pass scenarios:           1
expected fail scenarios:           10
observed pass scenarios:           1
observed fail scenarios:           10
unexpected outcomes:               0
damaged scenarios:                 10
damaged scenarios rejected:        10
gpu priority:                      none
```

## Interpretation

The validator fails closed. The exact saved stage-1 positive control passes,
while all damaged and falsely promoted states fail.

## Decision

Use this sensitivity block to prevent the one-row synthetic smoke from being
treated as full real external input or real BEM/FDTD comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke_validation_sensitivity.py
```

Figure check:

```text
3329x929, dynamic range=255
```
