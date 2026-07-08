# Experiment 1691: 84-Grid Pilot Real-Executor Observed-By-Case Execution Contract

Date: 2026-06-30

## Purpose

Define the execution contract for the future `observed_by_case` materialization
step without running finite difference time domain solves.

Runs `1688-1690` validated the bounded inputs. This run defines the next layer:
ten planned payload/case jobs, one cache array and one result JSON per job, and
the result metadata fields required before any observed arrays can be accepted.

## Output

```text
outputs/experiments/1691_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_job_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_result_schema_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_closure_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract.png
scripts/
```

## Result

```text
source input contract ready:             true
source sensitivity ready:                true
planned jobs:                            10
payloads:                                5
cases:                                   2
planned cache files:                     10
planned result JSON files:               10
expected FDTD trace solves:              80
result schema fields:                    16
closure items:                           3
contract-defined closure items:          3
execution-ready closure items:           0
defined commands:                        10
executed commands:                       0
observed arrays materialized:            0
results written:                         0
observed_by_case materialized:           false
new FDTD executed:                       false
execution permitted:                     false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

The three remaining closure items are:

| Order | Blocker | Contract closure |
| ---: | --- | --- |
| 1 | solver execution approval | approve the bounded CPU-only run of 10 jobs and 80 trace solves |
| 2 | observed array cache/output contract | use one NPZ array and one result JSON per payload/case job |
| 3 | real-executor result writer | write result JSON with solver, hash, shape, and acceptance metadata |

## Interpretation

The observed-data execution step is now specified but not performed. The future
materialization workload is ten jobs and eighty trace solves, with one cached
array and one result record per payload/case pair.

## Decision

Do not execute the jobs from this contract. A separate approval/materialization
run must be created before finite difference time domain solves, observed
arrays, or result JSON files can become evidence.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validation_sensitivity.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_execution_contract.py

14 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
