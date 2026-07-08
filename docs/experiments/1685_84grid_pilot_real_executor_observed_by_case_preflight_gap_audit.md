# Experiment 1685: 84-Grid Pilot Real-Executor Observed-By-Case Preflight Gap Audit

Date: 2026-06-30

## Purpose

Audit the remaining `observed_by_case` solver-array binding after runs
`1682-1684` safely materialized only `time_values`, `mute`, and
`scan_positions`.

This run asks whether `observed_by_case` can be materialized without crossing
into finite difference time domain execution.

## Output

```text
outputs/experiments/1685_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_producer_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_blocker_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit.png
scripts/
```

## Result

```text
source safe-materialization sensitivity ready:   true
source safe-materialization audit ready:          true
observed producer available:                      true
producer signature matches expected:              true
producer parameter count:                         6
simulate_bscan call detected:                     true
noise addition detected:                          true
safe to materialize without solver:               false
blockers:                                         5
ready blockers:                                   0
observed_by_case materialized:                    false
solver binding ready:                             false
new FDTD executed:                                false
bounded pilot execution ready:                    false
gpu work ready:                                   false
field transfer ready:                             false
field FWI ready:                                  false
ready for 3D/HPC:                                 false
```

The remaining blockers are:

| Order | Blocker |
| ---: | --- |
| 1 | true_model binding |
| 2 | case set binding |
| 3 | solver execution budget |
| 4 | observed array cache/output contract |
| 5 | real-executor result writer |

## Interpretation

The `observed_by_case` producer is real and callable, but it calls
`simulate_bscan`, which performs the FDTD solves needed to generate observed
traces. That means `observed_by_case` is not a safe array like `time_values`,
`mute`, or `scan_positions`; it is the execution boundary.

## Decision

Do not materialize `observed_by_case` or run FDTD from the revised five-row
pilot until the true model, case set, solver execution budget, cache/output
contract, and result writer are explicitly bounded and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validation_sensitivity.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit.py

14 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
