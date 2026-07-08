# BEM Experiment 845: Stage-1 2D Parser Positive-Control Sync Audit

Date: 2026-07-01

## Purpose

Audit whether the BEM stage-1 producer packet matches the 2D parser positive
control from run `1821`.

This run checks the same one-row FDTD return target as the BEM producer packet:
receiver `15`, frequency `1.0 GHz`, the expected partial-return CSV path, and
the required complex-field return columns. It also confirms that the parser
positive control is shape-only and not live approval.

## Output

```text
outputs/bem_experiments/845_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_parser_positive_control_sync_audit
```

## Result

```text
source BEM packet ready:             true
source 2D positive control ready:    true
source 2D control validation ready:  true
source 2D control sensitivity ready: true
audit checks:                           8
passed audit checks:                    8
failed audit checks:                    0
receiver index:                        15
frequency:                   1000000000 Hz
positive-control files:                 1
parser checks:                          5
parser checks passed:                   5
accepted as payload shape:           true
written under live approval root:    false
live approval file present:          false
accepted live approvals:                0
FDTD executed now:                   false
real BEM/FDTD comparison ready:      false
field transfer ready:                false
ready for 3D/HPC:                    false
gpu priority:                        none
```

## Interpretation

The BEM producer packet and the 2D parser positive control target the same
stage-1 complex-field return. The positive control confirms parser shape only;
it is not live approval and does not authorize FDTD.

## Decision

Keep FDTD execution blocked until a real live approval JSON is supplied.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_parser_positive_control_sync_audit.py
8 passed with validator/sensitivity block
```

Figure check:

```text
2825x855, dynamic range=255
```
