# BEM Experiment 856: Stage-1 Readiness Rollup Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `855` validator by damaging the saved run `854` rollup in
controlled ways.

The sensitivity set checks false summary readiness, source-count damage,
row-count damage, row readiness damage, receiver/frequency damage, false live
approval, accepted approval, partial/full return promotion, producer
authorization, FDTD execution, BEM/FDTD comparison, field transfer, 3D/HPC
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/856_project_core_bem_35field_matched_fdtd_complex_metric_stage1_readiness_rollup_validation_sensitivity
```

## Result

```text
scenarios:                  18
expected passes:             1
expected failures:          17
observed passes:             1
observed failures:          17
unexpected outcomes:         0
damaged scenarios:          17
damaged scenarios rejected: 17
FDTD executed now:       false
real BEM/FDTD comparison:false
field transfer ready:    false
ready for 3D/HPC:        false
gpu priority:            none
```

## Interpretation

The validator accepts only the exact saved fail-closed rollup and rejects every
damaged or prematurely promoted state.

## Decision

Use runs `854-856` as the guarded BEM stage-1 readiness rollup block. The
producer remains non-executed until a real live approval JSON passes the 2D
acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_readiness_rollup.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_readiness_rollup_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_readiness_rollup_validation_sensitivity.py
6 passed
```

Figure check:

```text
3221x924, dynamic range=255
```
