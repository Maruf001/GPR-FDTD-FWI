# BEM Experiment 796: Complex-Metric FDTD Route Compatibility Audit

Date: 2026-07-01

## Purpose

Check whether the existing matched-FDTD input-bound route can directly complete
the new complex-metric packet from run `790`.

The existing route is useful because it already has receiver/frequency identity
guards and strict contract-hash checks. The question is whether it can fill the
current five-stage packet that requires `fdtd_real` and `fdtd_imag` values.

## Output

```text
outputs/bem_experiments/796_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_route_compatibility_audit
```

## Result

```text
compatibility dimensions:               7
supported dimensions:                   3
direct-reuse dimensions:                3
blocking dimensions:                    4
partial stage files:                    5
partial metric rows:                    279
FDTD complex value cells required:      558
FDTD provenance/status cells required:  1395
existing route files:                   4
existing external input routes:         2
existing input rows:                    558
existing route value fields:            returned_fdtd_scattered_norm;returned_fdtd_source_hash
current required value fields:          fdtd_real;fdtd_imag
strict hash guard reusable:             true
identity guard reusable:                true
direct existing exporter reuse ready:   false
new complex FDTD adapter required:      true
real BEM/FDTD comparison ready:         false
field transfer ready:                   false
3D/HPC ready:                           false
gpu priority:                           none
```

## Decision

Reuse the existing receiver/frequency identity and strict contract-hash guard
logic, but do not treat the older scattered-norm/source-hash route as a direct
completion path for the run `790` complex packet. A new complex FDTD adapter is
required to fill `fdtd_real`, `fdtd_imag`, and the current stage-file
provenance/status fields.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_route_compatibility_audit.py
3 passed
```

Figure check:

```text
3365x931, dynamic range=255
```
