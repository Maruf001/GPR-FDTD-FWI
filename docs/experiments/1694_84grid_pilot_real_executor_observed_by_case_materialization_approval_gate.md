# Experiment 1694: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval Gate

Date: 2026-06-30

## Purpose

Define the final approval gate before any `observed_by_case` arrays are
materialized for the bounded 84-grid pilot.

Runs `1691-1693` define and validate a non-executing contract for ten future
payload/case jobs. This run checks the filesystem boundary that would permit
materialization: an explicit approval token plus the twenty expected per-job
artifacts.

## Output

```text
outputs/experiments/1694_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_approval_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_artifact_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate.png
scripts/
```

## Result

```text
source contract ready:                   true
source validation ready:                 true
source sensitivity ready:                true
planned jobs:                            10
future FDTD trace solves:                80
approval tokens required:                1
approval tokens present:                 0
approval tokens accepted:                0
planned artifacts:                       20
planned cache artifacts:                 10
planned result artifacts:                10
present artifacts:                       0
accepted artifacts:                      0
ready for materialization:               false
observed_by_case materialized:           false
commands executed:                       false
new FDTD executed:                       false
bounded CPU execution ready:             false
bounded pilot execution ready:           false
physical claim ready:                    false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

The required approval token is:

```text
outputs/experiments/_external_2d_returns/84grid_observed_by_case_pending/APPROVED_1691_OBSERVED_BY_CASE_EXECUTION.json
```

The planned artifacts are one cache array and one result JSON for each of the
ten payload/case jobs defined by run `1691`. None are present or accepted.

## Interpretation

The materialization boundary is now explicit. The current archive contains a
validated execution contract, but it does not contain authorization to run the
future finite difference time domain solves, observed arrays, or result JSON
files.

This prevents a planning artifact from being mistaken for executed physical
evidence.

## Decision

Do not materialize `observed_by_case` until an explicit approval token and a
separate execution run exist. Keep downstream bounded CPU execution, GPU work,
field transfer, field full waveform inversion, and 3D/HPC escalation blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract.py

14 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
