# Experiment 1795: 84-Grid External Return Dependency Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved dependency audit from run `1794`.

The validator checks that the dependency map still contains one approval item,
ten cache-array NPZ files, ten result JSON files, ten paired artifact jobs, zero
producer files, zero ready pairs, and no materialization/FDTD/downstream
promotion.

## Output

```text
outputs/experiments/1795_local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_validator
```

## Result

```text
validation checks:                 8
passed checks:                     8
failed checks:                     0
required return items:             21
approval items:                    1
cache-array NPZ items:             10
result-JSON items:                 10
paired artifact jobs:              10
paired artifact required items:    20
producer files present:            0
core preflight-passed items:       0
paired artifact jobs ready:        0
preflight-passed items:            0
ready action groups:               0
ready for materialization:         false
new FDTD executed:                 false
3D/HPC ready:                      false
gpu priority:                      none
```

## Decision

Use this validator before citing run `1794` as the current 84-grid
external-return dependency map.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_validator.py
3 passed
```

Figure check:

```text
3365x923, dynamic range=255
```
