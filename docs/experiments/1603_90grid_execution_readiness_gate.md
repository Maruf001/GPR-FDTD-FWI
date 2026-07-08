# Experiment 1603: 90-Grid Execution Readiness Gate

Date: 2026-06-29

## Purpose

Convert the 90-row dry-run payload manifest from run `1597` into an explicit
execution-readiness gate.

This run does not execute FDTD. It answers whether the current 90-grid plan is
safe to turn into a real CPU screen.

## Output

```text
outputs/experiments/1603_local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_requirement_rows.csv
data/local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_action_rows.csv
data/local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_summary.json
figures/local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source manifest guarded:                     true
payload rows:                                90
objective profiles:                          5
transition bins:                             18
budget:                                      60.0 minutes
estimated runtime:                           58.69245 minutes
budget headroom:                             1.30755 minutes
minimum required headroom:                   5.0 minutes
readiness requirements:                      10
requirements passed:                         4
blocking requirements:                       6
execution permitted:                         false
bounded CPU execution ready:                 false
commands executed:                           false
new FDTD executed:                           false
```

The six execution blockers are:

| Requirement | Current state |
| --- | --- |
| Minimum budget headroom | Fails: 1.30755 minutes available, 5.0 minutes required |
| Run-specific execution script | Missing |
| Executable command inventory | Missing |
| Output contract | Missing |
| Resume policy | Missing |
| Resource guard | Missing |

## Decision

Do not execute the 90-grid 2D CPU screen from the current manifest. The plan is
valid as a dry-run review artifact only.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate.py
5 passed
```

Figure check:

```text
3761x893, dynamic range=255
```
