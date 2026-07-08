# BEM Experiment 803: Complex-Metric FDTD Complex Adapter Interface Guard Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `802` complex FDTD adapter interface guard.

The validator checks the canonical input contract hash, the 279-row identity
payload, the six interface components, and the blocked real-input/writer/
comparison states.

## Output

```text
outputs/bem_experiments/803_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_interface_guard_audit_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
interface components:                      6
ready interface components:                3
evidence-producing components:             0
adapter input required columns:            12
completed stage output columns:            11
required identity rows:                    279
expected input contract SHA-256:           8c0e4be114e3c7d8703aa8b0afaa468c6dd33968c62742fdff01bc52a736339a
real FDTD complex input present:           false
completed stage file writer ready:         false
completed stage files ready:               false
real BEM/FDTD comparison ready:            false
3D/HPC ready:                              false
gpu priority:                              none
```

## Decision

Use this validator before adding a writer path to the complex FDTD adapter.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_interface_guard_audit_validator.py
3 passed
```

Figure check:

```text
2789x936, dynamic range=255
```
