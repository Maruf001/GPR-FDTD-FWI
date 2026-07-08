# BEM Experiment 802: Complex-Metric FDTD Complex Adapter Interface Guard Audit

Date: 2026-07-01

## Purpose

Create a guarded interface checkpoint for the complex FDTD adapter contract from
run `799`.

This run computes the canonical input contract hash for the 279 required
receiver-frequency identities and records which interface pieces are ready. It
does not consume real FDTD data, write completed stage files, or run a
BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/802_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_interface_guard_audit
```

## Result

```text
source contract ready:                    true
source contract sensitivity ready:        true
interface components:                     6
ready interface components:               3
evidence-producing components:            0
adapter input required columns:           12
completed stage output columns:           11
required identity rows:                   279
expected input contract SHA-256:          8c0e4be114e3c7d8703aa8b0afaa468c6dd33968c62742fdff01bc52a736339a
real FDTD complex input present:          false
completed stage file writer ready:        false
completed stage files ready:              false
real BEM/FDTD comparison ready:           false
field transfer ready:                     false
3D/HPC ready:                             false
gpu priority:                             none
```

## Decision

Use this interface guard before writing any completed stage files. Completed
outputs, real BEM/FDTD comparison, field transfer, and 3D/HPC remain blocked
until real FDTD input validates against the contract.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_interface_guard_audit.py
3 passed
```

Figure check:

```text
3185x935, dynamic range=255
```
