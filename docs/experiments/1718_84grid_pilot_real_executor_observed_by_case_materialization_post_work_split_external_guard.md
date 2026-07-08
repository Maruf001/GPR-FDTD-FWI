# Experiment 1718: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Post-Work-Split External Guard

Date: 2026-06-30

## Purpose

Audit the locked external approval-token path and the 20 planned
materialization artifact paths after the run `1715-1717` work-split policy
block.

The goal is to confirm that the policy work did not create real external
approval, cache-array, or result-JSON files.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1718_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard.png
scripts/
```

## Result

```text
source policy ready:                    true
source validation ready:                true
source sensitivity ready:               true
external items checked:                 21
external approval-token paths:           1
materialization artifact paths:         20
cache artifact paths:                   10
result artifact paths:                  10
parent directories present:              0
present items:                           0
nonempty items:                          0
accepted items:                          0
ready for materialization:              false
new FDTD executed:                      false
GPU work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
external guard ready:                   true
```

## Interpretation

The 2D work-split block remained a planning artifact. It did not create the
locked external approval token and did not create any of the planned cache or
result artifacts.

The current state is therefore unchanged: observed-by-case materialization,
FDTD execution, GPU work, field transfer, field FWI, and 3D/HPC remain blocked.

## Decision

Keep observed-by-case materialization and FDTD execution blocked until the real
external approval token and all 20 planned materialization artifacts exist and
are accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard.py

3 passed
```

Figure validation:

```text
2285x848, dynamic range=255
```
