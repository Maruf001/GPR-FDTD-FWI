# Experiment 1815: BEM Stage-1 Complex FDTD Live Approval Post-Scaffold Live-State Refresh

Date: 2026-07-01

## Purpose

Refresh the BEM-specific 2D FDTD live-approval state after the empty approval
directory was created in run `1812`.

This run answers whether the directory scaffold changed the actual execution
state. It does not run FDTD, create a live approval JSON, create a partial
complex-field return CSV, merge a full BEM/FDTD comparison table, or promote
field/3D work.

## Output

```text
outputs/experiments/1815_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh
```

## Result

```text
source live-approval contract ready:       true
source directory scaffold ready:           true
state rows:                                  2
action rows:                                 5
live approval parent present:             true
live approval file present:               false
live approval fields missing:                9
BEM partial-return parent present:         true
BEM partial-return file present:          false
completed actions:                           1
FDTD producer authorized now:              false
FDTD executed now:                         false
real BEM/FDTD comparison ready:            false
field transfer ready:                      false
gpu priority:                              none
```

Only the approval directory action is complete. The live approval JSON is still
absent, all nine required approval fields are still missing, and the stage-1
partial complex-field return CSV is still absent.

## Interpretation

The scaffold closed the directory-existence blocker only. It did not provide
execution approval, measured/computed FDTD values, or a real BEM/FDTD
comparison.

## Decision

Keep FDTD execution and BEM/FDTD comparison blocked until both live files pass
intake: the approval JSON and the one-row stage-1 partial complex-field return.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_post_scaffold_live_state_refresh.py
9 passed with validator/sensitivity block
```

Figure check:

```text
2644x844, dynamic range=255
```
