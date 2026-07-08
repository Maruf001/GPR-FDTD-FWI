# BEM Experiment 798: Complex-Metric FDTD Route Compatibility Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `797` validator with damaged versions of the run `796`
compatibility audit.

The damaged scenarios include count damage, value-field promotion, topology
promotion, adapter-removal, direct exporter reuse promotion, comparison
promotion, downstream promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/798_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_route_compatibility_audit_validation_sensitivity
```

## Result

```text
scenarios:                         16
expected pass scenarios:           1
expected fail scenarios:           15
observed pass scenarios:           1
observed fail scenarios:           15
unexpected outcomes:               0
damaged scenarios:                 15
damaged scenarios rejected:        15
gpu priority:                      none
```

The exact saved compatibility audit passes. All fifteen damaged variants fail.

## Decision

Use this sensitivity run to keep the complex FDTD adapter requirement
fail-closed.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_route_compatibility_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
3112x897, dynamic range=255
```
