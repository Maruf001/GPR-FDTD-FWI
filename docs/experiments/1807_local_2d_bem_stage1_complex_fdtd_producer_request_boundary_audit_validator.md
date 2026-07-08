# Experiment 1807: BEM Stage-1 Complex FDTD Producer Request Boundary Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1806` boundary audit from its written artifacts.

The validator checks that the BEM one-row request remains separate from the 2D
84-grid draft approval template and that no FDTD producer authorization,
execution, comparison, field transfer, or 3D/HPC state is promoted.

## Output

```text
outputs/experiments/1807_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit_validator
```

## Result

```text
validation checks:                 8
passed checks:                     8
failed checks:                     0
boundary rows:                     5
BEM requested rows:                1
BEM requested receiver index:     15
BEM requested frequency:           1.0 GHz
2D approval templates:             1
2D approval payloads:             10
live 2D external files:            0
FDTD producer authorized now:      false
FDTD executed now:                 false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
```

## Interpretation

The saved BEM/2D FDTD producer-request boundary validates and remains
non-authorizing.

## Decision

Use this validator before treating any 2D FDTD approval template as authority
for the BEM stage-1 return.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit.py
tests/test_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit_validator.py
5 passed
```

Figure check:

```text
3257x892, dynamic range=255
```
