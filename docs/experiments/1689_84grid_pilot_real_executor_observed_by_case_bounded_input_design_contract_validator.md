# Experiment 1689: 84-Grid Pilot Real-Executor Observed-By-Case Bounded Input Design Contract Validator

Date: 2026-06-30

## Purpose

Validate the run `1688` bounded input design contract from saved artifacts.

This run checks that the true-model targets, perturbation cases, revised
payload budget, remaining blockers, execution state, downstream state, figure,
and script snapshots are all consistent before any observed-data execution
contract is proposed.

## Output

```text
outputs/experiments/1689_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validator.png
scripts/
```

## Result

```text
source contract ready:                    true
validation checks:                        8
passed checks:                            8
failed checks:                            0
true model target count:                  3
case count:                               2
payload count:                            5
total scan positions:                     40
expected simulate_bscan calls:            10
expected FDTD trace solves:               80
remaining blockers:                       3
ready remaining blockers:                 0
observed inputs defined:                  true
observed_by_case materialized:            false
commands executed:                        false
new FDTD executed:                        false
bounded pilot execution ready:            false
gpu work ready:                           false
field transfer ready:                     false
field FWI ready:                          false
ready for 3D/HPC:                         false
```

The eight validation checks all pass:

```text
source contract ready
true model targets bound
case set bound
revised payload budget bound
three blockers preserved
execution remains blocked
downstream remains blocked
figure and scripts exist
```

## Interpretation

The bounded input contract is internally valid. The next observed-data step is
no longer blocked by vague input identity or budget uncertainty.

The validator also confirms that the contract remains non-executing: no
observed arrays were materialized and no finite difference time domain solve
was run.

## Decision

Use run `1689` as the validated input-contract checkpoint. The next defensible
2D task is a separate execution-contract design for materializing
`observed_by_case` with explicit solver approval, cache/output metadata, and a
real-executor result writer.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validator.py

7 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
