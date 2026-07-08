# BEM Experiment 801: Complex-Metric FDTD Complex Adapter Contract Spec Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `800` validator with damaged versions of the run `799`
adapter contract.

The damaged scenarios include column damage, mapping damage, guard promotion,
adapter-implementation promotion, completed-output promotion, comparison
promotion, downstream promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/801_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_contract_spec_validation_sensitivity
```

## Result

```text
scenarios:                         17
expected pass scenarios:           1
expected fail scenarios:           16
observed pass scenarios:           1
observed fail scenarios:           16
unexpected outcomes:               0
damaged scenarios:                 16
damaged scenarios rejected:        16
gpu priority:                      none
```

The exact saved adapter contract passes. All sixteen damaged variants fail.

## Decision

Use this sensitivity run to keep the complex FDTD adapter contract fail-closed.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_contract_spec_validation_sensitivity.py
3 passed
```

Figure check:

```text
3256x897, dynamic range=255
```
