# Experiment 1671: 84-Grid Pilot Real-Executor Creation Impact Audit

Date: 2026-06-30

## Purpose

Audit what would change if the real pilot executor script were created now.

Run `1670` defined the real-executor design contract. Before adding the
executor file, this run scans the current pilot scripts and tests for
assumptions that the proposed real executor does not exist.

This run does not create the executor script, execute FDTD, accept pilot
evidence, launch GPU work, transfer to field evidence, or promote 3D/HPC
readiness.

## Output

```text
outputs/experiments/1671_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_creation_impact_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_creation_impact_audit_impact_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_creation_impact_audit_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_creation_impact_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_creation_impact_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
real executor script exists:            false
impact rows:                            19
affected scripts:                       14
affected tests:                         5
direct refactor-required tests:         5
dynamic filesystem dependencies:        8
test absence assertions:                5
implementation without refactor ready:  false
real executor creation ready:           false
new FDTD executed:                      false
GPU work ready:                         false
field transfer ready:                   false
3D/HPC ready:                           false
impact audit ready:                     true
```

## Interpretation

Creating the real executor script immediately would change historical audits
and tests that currently encode the no-executor state. The impact is not only a
new implementation task; it is also a test-contract change.

The safe next step is to refactor or version the affected absence checks before
adding the executor file. Otherwise, adding the file would make several older
audit tests fail even before any FDTD execution is attempted.

## Decision

Do not create the real executor script as an unguarded edit. First separate
historical no-executor audits from current filesystem existence checks, then add
new tests for the future real executor.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_creation_impact_audit.py
4 passed
```

Figure check:

```text
2213x847, dynamic range=255
```
