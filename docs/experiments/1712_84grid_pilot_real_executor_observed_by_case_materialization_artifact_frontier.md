# Experiment 1712: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Artifact Frontier

Date: 2026-06-30

## Purpose

Simulate the observed-by-case materialization artifact frontier after the
post-synthetic approval-token guard in runs `1709-1711`.

The planned materialization has 10 observed-by-case jobs: five payload IDs and
two variants per payload. Each job requires one cache array and one result JSON,
for 20 artifacts total. This run enumerates all 1024 possible job-completion
subsets and checks which subsets satisfy the conservative materialization
artifact gate.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1712_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_job_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_frontier_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier.png
scripts/
```

## Result

```text
source guard ready:                      true
source validation ready:                 true
source sensitivity ready:                true
observed-by-case jobs:                   10
payloads:                                5
variants:                                2
required artifacts:                      20
current present artifacts:               0
current accepted artifacts:              0
job-subset scenarios:                    1024
current-state scenarios:                 1
partial scenarios:                       1022
artifact-complete scenarios:             1
partial artifact-complete scenarios:     0
minimum jobs for artifact completion:    10
ready for materialization:               false
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
3D/HPC ready:                            false
```

Required jobs:

| Payload | Variant | Required artifacts |
| --- | --- | ---: |
| payload_001 | nominal | 2 |
| payload_001 | time_shift_only | 2 |
| payload_023 | nominal | 2 |
| payload_023 | time_shift_only | 2 |
| payload_046 | nominal | 2 |
| payload_046 | time_shift_only | 2 |
| payload_068 | nominal | 2 |
| payload_068 | time_shift_only | 2 |
| payload_072 | nominal | 2 |
| payload_072 | time_shift_only | 2 |

## Interpretation

No partial observed-by-case job subset completes the conservative
materialization artifact gate. The only artifact-complete scenario is the
all-job case: all 10 jobs and all 20 cache/result artifacts are present and
accepted.

The current live state remains unchanged: zero planned artifacts are present,
zero artifacts are accepted, and the real external approval token is still
absent.

## Decision

Use run `1712` as the materialization artifact frontier. Keep materialization,
FDTD execution, GPU work, field transfer, field FWI, and 3D/HPC blocked until
the real external approval token exists and all planned cache/result artifacts
are produced and accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier.py

3 passed
```

Figure validation:

```text
2428x845, dynamic range=255
```
