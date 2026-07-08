# Experiment 1824: BEM Stage-1 Complex FDTD Live Approval Acceptance Gate

Date: 2026-07-01

## Purpose

Evaluate the real live approval gate for the first BEM stage-1 FDTD return.

Runs `1821-1823` proved that an output-local positive control has the expected
approval-payload shape. This run checks only the real live approval path. The
live approval file is absent, so all acceptance gates fail closed.

## Output

```text
outputs/experiments/1824_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate
```

## Result

```text
source positive control ready:          true
source positive control sensitivity:    true
live approval parent present:           true
live approval file present:            false
approval gates:                            6
gates passed:                              0
gates failed:                              6
accepted live approvals:                   0
FDTD producer authorized now:          false
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
ready for 3D/HPC:                      false
gpu priority:                          none
```

## Interpretation

The output-local positive control is not live approval. The acceptance gate
looks only at the real live approval location, finds no file, and fails closed.

## Decision

Keep FDTD execution blocked. A real live approval JSON must pass every gate
before the FDTD producer can be authorized.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate.py
8 passed with validator/sensitivity block
```

Figure check:

```text
2753x859, dynamic range=255
```
