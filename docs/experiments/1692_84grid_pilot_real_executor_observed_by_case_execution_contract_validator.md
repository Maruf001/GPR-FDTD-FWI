# Experiment 1692: 84-Grid Pilot Real-Executor Observed-By-Case Execution Contract Validator

Date: 2026-06-30

## Purpose

Validate the run `1691` observed-by-case execution contract from saved
artifacts.

This run checks that the job plan, result schema, closure state,
execution/downstream block, figure, and script snapshots are consistent.

## Output

```text
outputs/experiments/1692_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validator.png
scripts/
```

## Result

```text
validation checks:                        6
passed checks:                            6
failed checks:                            0
planned jobs:                             10
expected FDTD trace solves:               80
result schema fields:                     16
closure items:                            3
executed commands:                        0
observed arrays materialized:             0
new FDTD executed:                        false
execution permitted:                      false
GPU work ready:                           false
field transfer ready:                     false
field FWI ready:                          false
ready for 3D/HPC:                         false
```

The six validation checks all pass:

```text
source contract ready
job plan shape
result schema shape
closure state
execution and downstream blocked
figure and scripts exist
```

## Interpretation

The observed-by-case execution contract is valid as a non-executing plan. It
does not provide observed arrays, finite difference time domain outputs, or
accepted result records.

## Decision

Use run `1692` as the artifact guard for run `1691`. Do not execute the planned
jobs until a separate materialization run is explicitly created and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validator.py

7 passed
```

Figure validation:

```text
2285x842, dynamic range=255
```
