# Experiment 1686: 84-Grid Pilot Real-Executor Observed-By-Case Preflight Gap Audit Validator

Date: 2026-06-30

## Purpose

Validate run `1685` from saved artifacts.

This run checks that the `observed_by_case` preflight gap audit is internally
consistent and still blocks FDTD execution.

## Output

```text
outputs/experiments/1686_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validator.png
scripts/
```

## Result

```text
source audit ready:                 true
validation checks:                  6
failed checks:                      0
observed producer available:        true
simulate_bscan call detected:       true
safe to materialize without solver: false
blockers:                           5
ready blockers:                     0
observed_by_case materialized:      false
solver binding ready:               false
new FDTD executed:                  false
bounded pilot execution ready:      false
gpu work ready:                     false
field transfer ready:               false
field FWI ready:                    false
ready for 3D/HPC:                   false
```

The six checks validate source readiness, producer signature and execution
boundary, five preserved blockers, blocked observed/FDTD state, blocked
downstream state, and figure/script artifacts.

## Interpretation

Run `1685` is a valid preflight gap audit. The remaining `observed_by_case`
binding is not a harmless array materialization step; it is the FDTD execution
boundary for the revised five-row pilot.

## Decision

Keep `observed_by_case`, solver binding, bounded pilot execution, GPU work,
field transfer, field FWI, and 3D/HPC blocked until the five blockers identified
in run `1685` are explicitly closed.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validator.py

7 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
