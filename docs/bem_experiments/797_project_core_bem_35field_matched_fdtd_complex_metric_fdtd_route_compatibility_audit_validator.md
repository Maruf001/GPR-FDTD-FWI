# BEM Experiment 797: Complex-Metric FDTD Route Compatibility Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `796` compatibility audit.

The validator checks that the existing matched-FDTD route remains only partially
reusable: identity and strict hash guards are reusable, but direct completion of
the five-stage complex packet is blocked.

## Output

```text
outputs/bem_experiments/797_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_route_compatibility_audit_validator
```

## Result

```text
validation checks:                      7
passed checks:                          7
failed checks:                          0
compatibility dimensions:               7
direct-reuse dimensions:                3
blocking dimensions:                    4
partial stage files:                    5
partial metric rows:                    279
FDTD complex value cells required:      558
existing input rows:                    558
new complex FDTD adapter required:      true
direct existing exporter reuse ready:   false
real BEM/FDTD comparison ready:         false
3D/HPC ready:                           false
gpu priority:                           none
```

## Decision

Use this validator before citing run `796` as the complex FDTD adapter decision.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_route_compatibility_audit_validator.py
3 passed
```

Figure check:

```text
3365x931, dynamic range=255
```
