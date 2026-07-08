# Experiment 1825: BEM Stage-1 Complex FDTD Live Approval Acceptance Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1824` live approval acceptance gate.

The validator checks source readiness, six-gate shape, zero passed gates, zero
accepted live approvals, absent live approval, blocked FDTD execution, blocked
BEM/FDTD comparison, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1825_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate_validator
```

## Result

```text
validation checks:                       5
checks passed:                           5
checks failed:                           0
approval gates:                          6
gates passed:                            0
gates failed:                            6
live approval file present:          false
accepted live approvals:                 0
FDTD producer authorized now:        false
FDTD executed now:                   false
real BEM/FDTD comparison ready:      false
field transfer ready:                false
ready for 3D/HPC:                    false
gpu priority:                        none
```

## Interpretation

The live approval gate validates as absent and fail-closed.

## Decision

Keep FDTD execution blocked until a real live approval JSON passes every gate.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_acceptance_gate_validation_sensitivity.py
8 passed
```

Figure check:

```text
2105x859, dynamic range=255
```
