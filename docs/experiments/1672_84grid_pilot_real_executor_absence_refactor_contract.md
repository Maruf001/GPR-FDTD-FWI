# Experiment 1672: 84-Grid Pilot Real-Executor Absence Refactor Contract

Date: 2026-06-30

## Purpose

Convert the run `1671` impact audit into a concrete refactor contract.

Run `1671` showed that creating the real executor script would affect existing
historical no-executor audits and tests. This run groups those required changes
so the executor can later be added without breaking the regression suite.

This run does not refactor the historical scripts, create the executor script,
execute FDTD, accept pilot evidence, launch GPU work, transfer to field
evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1672_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_contract_refactor_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source impact audit ready:             true
real executor script exists:           false
impact rows:                           19
affected scripts:                      14
affected tests:                        5
direct refactor-required tests:        5
refactor groups:                       4
ready refactor groups:                 0
required refactor items:               15
completed refactor items:              0
real executor creation ready:          false
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
3D/HPC ready:                          false
refactor contract ready:               true
```

Refactor groups:

| Group | Affected count | Required change |
| --- | ---: | --- |
| historical dynamic scripts | 8 | freeze historical no-executor state inside old audit scripts instead of reading live filesystem existence |
| historical absence tests | 5 | rename assertions as historical no-executor checks or assert generated historical summaries |
| future executor tests | 1 | add new tests for the future real executor script after it exists |
| suite validation | 1 | rerun focused executor tests and the full suite before creating the executor file |

## Interpretation

The real-executor blocker is now mostly a test-contract and historical-audit
versioning issue. The physics semantic blockers were closed by the revised
pilot, but adding the executor file would currently invalidate older
no-executor assumptions.

## Decision

Do not create the real executor file until the historical no-executor checks
are refactored or versioned. Use this contract as the next implementation
precondition.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_absence_refactor_contract.py
4 passed
```

Figure check:

```text
2213x847, dynamic range=255
```
