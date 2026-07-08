# Experiment 1821: BEM Stage-1 Complex FDTD Live Approval Parser Positive Control

Date: 2026-07-01

## Purpose

Create an output-local positive control for the BEM stage-1 FDTD approval
parser.

Run `1818` created a draft approval template. This run fills the approval-shape
fields with positive-control values so the parser can be tested on a complete
payload without creating live approval, authorizing FDTD, or promoting a
BEM/FDTD comparison.

## Output

```text
outputs/experiments/1821_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control
```

Key artifact:

```text
data/positive_control/APPROVED_BEM_STAGE1_COMPLEX_FDTD_RETURN.positive_control.json
```

## Result

```text
source template ready:                 true
source template sensitivity ready:     true
positive-control files:                   1
parser checks:                            5
parser checks passed:                     5
accepted as payload shape:             true
written under live approval root:      false
live approval file present:            false
accepted live approvals:                  0
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
ready for 3D/HPC:                      false
gpu priority:                          none
```

## Interpretation

The parser positive control proves that the approval parser can recognize the
expected complete JSON shape for the one-row BEM stage-1 FDTD return.

It does not prove execution readiness. The positive-control file is kept inside
the run output, outside the live approval location, and is explicitly not
accepted as live approval.

## Decision

Use this only to test parser shape. Keep FDTD execution blocked until a real
live approval JSON is supplied in the live approval location.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control.py
8 passed with validator/sensitivity block
```

Figure check:

```text
1925x847, dynamic range=255
```
