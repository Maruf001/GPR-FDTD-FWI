# Experiment 1715: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Work-Split Policy

Date: 2026-06-30

## Purpose

Convert the run `1712-1714` materialization artifact frontier into a practical
work-split policy.

The policy separates the blocked 2D observed-by-case materialization into one
external approval token, ten cache-array artifacts, ten result-JSON artifacts,
and one final all-artifact acceptance gate. It does not weaken the execution
boundary.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1715_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy.png
scripts/
```

## Result

```text
source frontier ready:                    true
source validation ready:                  true
source sensitivity ready:                 true
work stages:                              4
external approval token required:          1
planned jobs:                             10
planned payloads:                          5
planned variants:                          2
cache-array artifacts:                    10
result-JSON artifacts:                    10
materialization artifacts:                20
total required items:                     21
current present artifacts:                 0
current accepted artifacts:                0
all jobs required for completion:          true
all artifacts required for FDTD boundary:  true
partial artifacts promote FDTD:            false
ready for materialization:                 false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
field FWI ready:                           false
3D/HPC ready:                              false
```

Work split:

| Stage | Work block | Items | Artifacts | Requires approval | Requires execution |
| --- | --- | ---: | ---: | --- | --- |
| external_approval_token | approval | 1 | 0 | true | false |
| cache_array_materialization | materialization | 10 | 10 | true | true |
| result_json_materialization | materialization | 10 | 10 | true | true |
| final_artifact_acceptance_gate | acceptance | 0 | 0 | true | false |

## Interpretation

The materialization path has 21 required items: one real external approval
token plus 20 cache/result artifacts. The route is useful for planning, but it
does not make the current archive executable. No partial artifact delivery
authorizes FDTD execution.

## Decision

Keep observed-by-case materialization and FDTD execution blocked until the real
external approval token exists and all 20 planned artifacts are present and
accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy.py

3 passed
```

Figure validation:

```text
2428x847, dynamic range=255
```
