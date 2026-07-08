# Experiment 1828: BEM Stage-1 Complex FDTD Live Approval Action Rollup Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1827` action rollup.

The validator checks source readiness, row shape, absent live files, approval
field state, failed acceptance gates, blocked execution/downstream state,
figure validation, and script snapshots.

## Output

```text
outputs/experiments/1828_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
artifact rows:                           2
approval field rows:                     9
action rows:                             6
target fields prefilled:                 5
approval-provenance fields blank:        4
live artifacts required:                 2
live artifacts present:                  0
live artifacts missing:                  2
approval gates:                          6
gates passed:                            0
gates failed:                            6
accepted live approvals:                 0
actions complete:                        1
FDTD producer authorized now:        false
FDTD executed now:                   false
real BEM/FDTD comparison ready:      false
field transfer ready:                false
ready for 3D/HPC:                    false
gpu priority:                        none
```

## Interpretation

The action rollup validates the exact current missing-live-artifact state.

## Decision

Keep the BEM stage-1 FDTD producer blocked until the action rollup changes
through live evidence.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_action_rollup_validation_sensitivity.py
9 passed
```

Figure check:

```text
2213x863, dynamic range=255
```
