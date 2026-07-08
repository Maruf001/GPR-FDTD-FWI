# Experiment 1765: Post-1762 Decision Frontier Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1764` validator.

The sensitivity cases damage the source count, objective result, acquisition
edge, follow-up failure count, 84-row subset count, pilot count, FDTD trace
budget, approval state, materialization state, FDTD/GPU readiness, broad-claim
state, frontier shape, figure output, and script snapshots.

## Output

```text
outputs/experiments/1765_local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit_validation_sensitivity
```

## Result

```text
cases:                          17
expected pass:                  1
expected fail:                  16
actual pass:                    1
actual fail:                    16
unexpected outcomes:            0
new FDTD executed:              false
gpu work ready:                 false
field transfer ready:           false
3D/HPC ready:                   false
```

## Decision

Runs `1763-1765` are the guarded current 2D decision-frontier block. The
validator rejects false broad-claim promotion, false execution promotion, false
approval promotion, and artifact-shape damage.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit_validation_sensitivity.py
3 passed
```

