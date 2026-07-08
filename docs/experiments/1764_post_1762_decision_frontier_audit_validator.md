# Experiment 1764: Post-1762 Decision Frontier Audit Validator

Date: 2026-07-01

## Purpose

Validate run `1763` from saved artifacts.

## Output

```text
outputs/experiments/1764_local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit_validator
```

## Result

```text
checks:                         9
passed:                         9
failed:                         0
decision blocks:                8
frontier items:                 4
blocked frontier items:         3
84-row subset count:            84
pilot row count:                5
observed_by_case jobs:          10
blank approval fields:          4
new FDTD executed:              false
gpu work ready:                 false
field transfer ready:           false
3D/HPC ready:                   false
```

## Decision

Run `1763` is internally consistent and preserves the current 2D execution
blocker. Use it as the guarded current 2D decision-frontier artifact.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit_validator.py
3 passed
```

