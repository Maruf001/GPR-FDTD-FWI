# Experiment 1693: 84-Grid Pilot Real-Executor Observed-By-Case Execution Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1692` validator with controlled damage to the run `1691`
execution contract.

This run checks that the validator fails when job identity, trace budget,
execution state, result state, schema state, closure state, downstream state,
figure metadata, or script snapshots are damaged.

## Output

```text
outputs/experiments/1693_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       16
expected pass cases:                     1
expected fail cases:                     15
actual pass cases:                       1
actual fail cases:                       15
unexpected cases:                        0
damaged cases:                           15
new FDTD executed:                       false
execution permitted:                     false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

The exact source contract passes. Damaged states fail for:

```text
source readiness removal
job removal
payload identity damage
case identity damage
trace-budget damage
command-execution promotion
observed-array materialization promotion
result-written promotion
schema-field removal
schema-value promotion
closure-readiness promotion
FDTD execution promotion
downstream GPU promotion
figure damage
missing script snapshots
```

## Interpretation

The execution-contract validator is sensitive to the intended failure modes. It
cannot silently treat a contract as executed evidence, and it rejects accidental
promotion of observed arrays, finite difference time domain execution, results,
or downstream readiness.

## Decision

Use runs `1691-1693` as the guarded non-executing observed-by-case execution
contract. A separate materialization run is still required before any FDTD
solve or observed array cache can be accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_validation_sensitivity.py

10 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
