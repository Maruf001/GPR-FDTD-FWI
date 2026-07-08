# Experiment 1796: 84-Grid External Return Dependency Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1795` validator by applying damaged versions of the saved
run `1794` dependency audit.

The sensitivity cases include damaged counts, missing pair requirements, fake
producer-file promotion, fake core-preflight promotion, fake paired-job
promotion, fake action readiness, materialization promotion, FDTD promotion,
3D/HPC promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1796_local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_validation_sensitivity
```

## Result

```text
scenarios:                         20
expected pass scenarios:           1
expected fail scenarios:           19
observed pass scenarios:           1
observed fail scenarios:           19
unexpected outcomes:               0
damaged scenarios:                 19
damaged scenarios rejected:        19
gpu priority:                      none
```

The exact saved dependency audit passes. All nineteen damaged variants fail.

## Decision

Use this sensitivity run to keep the 84-grid external-return dependency map
fail-closed. The block still does not support observed-by-case materialization,
new FDTD execution, field transfer, or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
3436x892, dynamic range=255
```
