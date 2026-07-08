# Experiment 1806: BEM Stage-1 Complex FDTD Producer Request Boundary Audit

Date: 2026-07-01

## Purpose

Audit whether the current 2D FDTD approval-template branch can authorize the
new BEM stage-1 complex-field producer request.

This run does not execute FDTD, create external return files, create a BEM
partial return, run BEM/FDTD comparison, transfer to field data, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1806_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit
```

Key artifacts:

```text
data/local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit_boundary_rows.csv
data/local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit_summary.json
figures/local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit.png
```

## Result

```text
boundary rows:                         5
BEM requested rows:                    1
BEM requested receiver index:         15
BEM requested frequency:               1.0 GHz
BEM stage-1 partial file present:      false
BEM full external input present:       false
2D approval templates:                 1
2D approval payloads:                 10
2D approval token true:                false
2D accepted live approvals:            0
live 2D external files:                0
current 2D approval can authorize BEM: false
FDTD producer authorized now:          false
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
3D/HPC ready:                          false
```

## Interpretation

The BEM stage-1 one-row FDTD request is separate from the current 84-grid 2D
approval template. The current 2D template is draft-only and does not authorize
the BEM return.

## Decision

Create a BEM-specific live approval or producer execution path before generating
the first real center-frequency FDTD complex-field return.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_producer_request_boundary_audit.py
2 passed
```

Figure check:

```text
3293x915, dynamic range=255
```
