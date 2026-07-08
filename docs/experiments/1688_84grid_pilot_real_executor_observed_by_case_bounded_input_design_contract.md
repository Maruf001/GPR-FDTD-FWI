# Experiment 1688: 84-Grid Pilot Real-Executor Observed-By-Case Bounded Input Design Contract

Date: 2026-06-30

## Purpose

Define the bounded input contract for the remaining `observed_by_case`
materialization step without running finite difference time domain solves.

Runs `1685-1687` showed that `observed_by_case` is the execution boundary
because its producer calls `simulate_bscan`. This run closes the non-execution
design part: the true model, case set, revised payload set, scan-position
budget, and remaining execution blockers.

## Output

```text
outputs/experiments/1688_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_true_model_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_case_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_payload_budget_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_remaining_blocker_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract.png
scripts/
```

## Result

```text
source preflight sensitivity ready:     true
source preflight audit ready:           true
source safe-array audit ready:          true
true model target count:                3
case count:                             2
payload count:                          5
payload 68 included:                    true
stale payload 86 included:              false
total scan positions:                   40
expected simulate_bscan calls:          10
expected FDTD trace solves:             80
remaining blockers:                     3
ready remaining blockers:               0
observed inputs defined:                true
observed_by_case materialized:          false
commands executed:                      false
new FDTD executed:                      false
bounded pilot execution ready:          false
gpu work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
ready for 3D/HPC:                       false
```

The bounded observed-data input contract uses:

| Component | Count | State |
| --- | ---: | --- |
| True targets | 3 | bound |
| Perturbation cases | 2 | bound |
| Revised payload rows | 5 | bound |
| Scan positions | 40 | bound |
| Future `simulate_bscan` calls | 10 | planned only |
| Future FDTD trace solves | 80 | planned only |
| Remaining blockers | 3 | unresolved |

The remaining blockers are:

| Order | Blocker |
| ---: | --- |
| 1 | solver execution approval |
| 2 | observed array cache/output contract |
| 3 | real-executor result writer |

## Interpretation

The observed-data step is now bounded rather than vague. A future pilot would
need ten controlled `simulate_bscan` calls, producing eighty trace solves across
the revised five-payload set and two perturbation cases.

This does not promote the pilot to executed evidence. No observed arrays were
materialized and no finite difference time domain solve was run.

## Decision

Keep observed-data materialization, real pilot execution, GPU work, field
transfer, field FWI, and 3D/HPC blocked until the solver approval, observed
array cache/output contract, and result writer are closed by a validated
execution contract.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract.py

4 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
