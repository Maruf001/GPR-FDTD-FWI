# BEM Experiment 848: Stage-1 2D Live Approval Gate Sync Audit

Date: 2026-07-01

## Purpose

Audit whether the BEM stage-1 producer packet is synchronized with the 2D live
approval acceptance gate from run `1824`.

The audit checks that the BEM stage-1 target remains receiver `15` at
`1.0 GHz`, the 2D live approval gate is fail-closed, no live approval file is
present, no live approval is accepted, and the BEM producer remains
non-executed.

## Output

```text
outputs/bem_experiments/848_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_live_approval_gate_sync_audit
```

## Result

```text
source BEM packet ready:            true
source 2D gate fail-closed ready:   true
source 2D gate validation ready:    true
source 2D gate sensitivity ready:   true
audit checks:                          6
passed audit checks:                   6
failed audit checks:                   0
receiver index:                       15
frequency:                  1000000000 Hz
approval gates:                        6
approval gates passed:                 0
approval gates failed:                 6
live approval file present:        false
accepted live approvals:               0
FDTD producer authorized now:      false
FDTD executed now:                 false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
ready for 3D/HPC:                  false
gpu priority:                      none
```

## Interpretation

The BEM producer packet and the 2D live approval gate agree on the current
state. The gate is closed because the live approval file is absent, so the BEM
stage-1 producer must remain non-executed.

## Decision

Keep the BEM stage-1 producer non-executed until a real live approval JSON
passes the 2D gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_live_approval_gate_sync_audit.py
8 passed with validator/sensitivity block
```

Figure check:

```text
2681x857, dynamic range=255
```
