# Experiment 1608: 84-Grid Execution Contract Skeleton

Date: 2026-06-29

## Purpose

Materialize the non-budget execution contracts for the run `1606` 84-grid
subset without executing FDTD.

Run `1607` validated that the 84-grid subset satisfies the one-hour budget with
the required five-minute reserve. This run adds deterministic output paths,
planned command rows, resume policy, and resource guards. It still keeps the
screen blocked because the actual row executor does not exist.

## Output

```text
outputs/experiments/1608_local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton_output_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton_command_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton_resume_policy_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton_resource_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source subset ready:                         true
source subset validation ready:              true
selected payload rows:                       84
planned output-contract rows:                84
planned command rows:                        84
resume-policy rows:                          4
resource-guard rows:                         5
run-specific execution script available:     false
planned command inventory available:         true
executable command count:                    0
output contract available:                   true
resume policy available:                     true
resource guard available:                    true
remaining execution-contract blockers:       2
execution contract skeleton ready:           true
execution permitted:                         false
bounded CPU execution ready:                 false
new FDTD executed:                           false
GPU priority:                                none
```

The two remaining blockers are now narrow: the row executor script must exist,
and the planned command rows must become executable. No command was executed.

## Decision

Use this skeleton as the next execution-contract input. Do not run the 84-grid
screen until a real row executor exists and the command rows validate as
executable.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_execution_contract_skeleton.py
3 passed
```

Figure check:

```text
2429x846, dynamic range=255
```
