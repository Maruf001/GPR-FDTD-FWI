# BEM Experiment 804: Complex-Metric FDTD Complex Adapter Interface Guard Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `803` validator with damaged versions of the run `802`
interface guard.

The damaged scenarios include contract-hash damage, identity-payload damage,
interface-count damage, evidence promotion, real-input promotion, writer
promotion, completed-output promotion, comparison promotion, downstream
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/804_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_interface_guard_audit_validation_sensitivity
```

## Result

```text
scenarios:                         14
expected pass scenarios:           1
expected fail scenarios:           13
observed pass scenarios:           1
observed fail scenarios:           13
unexpected outcomes:               0
damaged scenarios:                 13
damaged scenarios rejected:        13
gpu priority:                      none
```

The exact saved interface guard passes. All thirteen damaged variants fail.

## Decision

Use this sensitivity run to keep the complex FDTD adapter interface guard
fail-closed.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_interface_guard_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
2824x855, dynamic range=255
```
