# Experiment 1827: BEM Stage-1 Complex FDTD Live Approval Action Rollup

Date: 2026-07-01

## Purpose

Roll up the exact 2D-side actions required before the first BEM stage-1 FDTD
producer can be authorized.

The source template block is ready and the real acceptance gate is guarded as
fail-closed. This run keeps those states separate: the output-local template is
usable for preparation, but the live approval JSON and BEM partial-return CSV
are still missing from their live paths.

## Output

```text
outputs/experiments/1827_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup
```

## Result

```text
source contract ready:                 true
source template ready:                 true
source template sensitivity ready:     true
source gate fail-closed ready:         true
source gate validation ready:          true
source gate sensitivity ready:         true
live artifacts required:                  2
live artifacts present:                   0
live artifacts missing:                   2
approval fields:                          9
target fields prefilled:                  5
approval-provenance fields blank:         4
approval gates:                           6
gates passed:                             0
gates failed:                             6
accepted live approvals:                  0
actions complete:                         1
FDTD producer authorized now:         false
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
ready for 3D/HPC:                     false
gpu priority:                         none
```

## Interpretation

The output-local approval template is ready. The remaining live requirements
are four approval-provenance fields, the live approval JSON, the 12-column BEM
stage-1 partial-return CSV, and a rerun of the six-gate acceptance check.

## Decision

Keep FDTD execution blocked until both live artifacts exist and every live
approval gate passes.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup.py
9 passed with validator/sensitivity block
```

Figure check:

```text
2897x849, dynamic range=255
```
