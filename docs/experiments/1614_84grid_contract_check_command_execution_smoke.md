# Experiment 1614: 84-Grid Contract-Check Command Execution Smoke

Date: 2026-06-30

## Purpose

Execute the run `1612` contract-check command inventory without running FDTD.

Run `1612` refreshed 84 planned command rows, and run `1613` validated that
inventory. This run writes one contract-check JSON output for each selected
payload row. It does not execute the FDTD solver, write trace fields, create
physical results, or promote downstream states.

## Output

```text
outputs/experiments/1614_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke
```

Key artifacts:

```text
data/contract_check_outputs/*.json
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_execution_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract-check execution smoke ready:   true
source command inventory ready:         true
source command validation ready:        true
command rows:                           84
contract-check JSON outputs:            84
contract-check passes:                  84
contract-check failures:                0
real execution command count:           0
executable real command count:          0
real FDTD execution enabled:            false
execution permitted:                    false
new FDTD executed:                      false
physical claim ready:                   false
GPU work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
GPU priority:                           none
```

## Decision

Use run `1614` as the executable contract-check smoke before any real row-level
FDTD executor work. The 84-row screen still has no physical FDTD outputs.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke.py
13 passed
```

Figure check:

```text
2429x846, dynamic range=255
```
