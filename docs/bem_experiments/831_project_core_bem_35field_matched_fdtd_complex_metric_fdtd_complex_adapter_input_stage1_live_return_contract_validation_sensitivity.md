# BEM Experiment 831: Complex FDTD Adapter Input Stage-1 Live Return Contract Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `830` validator with damaged versions of the run `829`
stage-1 live return contract.

Damaged cases include policy-label damage, contract row-count damage, receiver
identity damage, required-column damage, false partial-file presence, false
full-file presence, full-row-count damage, acceptance promotion, action
completion promotion, comparison promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/bem_experiments/831_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract_validation_sensitivity
```

## Result

```text
scenarios:                         13
expected pass scenarios:           1
expected fail scenarios:           12
observed pass scenarios:           1
observed fail scenarios:           12
unexpected outcomes:               0
damaged scenarios:                 12
damaged scenarios rejected:        12
gpu priority:                      none
```

## Interpretation

The validator fails closed. The exact saved contract passes, while all damaged
or falsely promoted variants fail.

## Decision

Use this sensitivity block to keep the stage-1 live contract from being treated
as full external preflight or real BEM/FDTD comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract_validation_sensitivity.py
```

Figure check:

```text
3581x931, dynamic range=255
```
