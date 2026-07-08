# Experiment 1673: 84-Grid Pilot Real-Executor Absence Refactor Applied Audit

Date: 2026-06-30

## Purpose

Verify that historical no-executor audits no longer depend on the live
filesystem existence of the future real executor script.

Run `1672` defined the refactor contract. This run audits the applied refactor:
historical no-executor scripts now use frozen run-time status instead of live
`REAL_EXECUTOR_SCRIPT.exists()` or `PROPOSED_REAL_EXECUTOR.exists()` checks.

This run does not create the executor script, execute FDTD, accept pilot
evidence, launch GPU work, transfer to field evidence, or promote 3D/HPC
readiness.

## Output

```text
outputs/experiments/1673_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_applied_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_applied_audit_reference_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_applied_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_applied_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source refactor contract ready:          true
reference rows:                          6
scanner string references:               6
live filesystem dependencies:            0
follow-up required rows:                 0
historical absence refactor applied:     true
real executor creation ready:            false
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
3D/HPC ready:                            false
applied audit ready:                     true
```

## Interpretation

The historical no-executor audits are now stable against a future executor-file
creation. They preserve their original no-executor findings through explicit
run-time constants rather than by reading the current filesystem.

This does not make executor creation ready by itself. It removes one blocker:
future executor work can add new executor-specific tests without invalidating
older no-executor audit results.

## Decision

Use run `1673` as the applied refactor checkpoint. The next executor step can
add future-specific tests and then create the separate real executor script,
still without running FDTD until the executor writes and validates the five
required JSON outputs.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_applied_audit.py
4 passed
```

Figure check:

```text
2069x847, dynamic range=255
```
