# Experiment 1633: 84-Grid Pilot Real-Execution Preflight Gap Audit Validator

Date: 2026-06-30

## Purpose

Validate run `1632` from saved artifacts.

The validator checks that the source chain is ready, all five real-mode probes
are refused, the four implementation blockers remain, no execution/downstream
state is promoted, and the figure and script snapshots are present.

## Output

```text
outputs/experiments/1633_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
gap-audit validation ready:                true
pilot rows:                                5
real-mode refusals:                        5
implementation actions:                    4
remaining real-pilot blockers:             4
new FDTD executed:                         false
GPU priority:                              none
```

## Decision

Use run `1633` as the artifact validator for the run `1632` real-execution
preflight gap audit. The current five-row pilot path remains guarded and
non-executing.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validator.py
3 passed
```

Figure check:

```text
2285x840, dynamic range=255
```
