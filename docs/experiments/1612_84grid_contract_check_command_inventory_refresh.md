# Experiment 1612: 84-Grid Contract-Check Command Inventory Refresh

Date: 2026-06-30

## Purpose

Refresh the 84-grid planned command inventory so each selected payload row
targets the guarded contract-check interface from run `1610`.

This run does not execute FDTD. It rebuilds the command rows with
`--contract-check-only` and probes the executor interface in-process for all 84
selected rows.

## Output

```text
outputs/experiments/1612_local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_command_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_contract_probe_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source guard ready:                        true
source guard validation ready:             true
selected payload rows:                     84
refreshed command rows:                    84
contract-check probes:                     84
contract-check probes passed:              84
executor script available:                 true
contract-check command inventory ready:    true
contract-check batch ready:                true
command inventory refresh required:        false
real execution command count:              0
executable real command count:             0
real FDTD execution enabled:               false
execution permitted:                       false
new FDTD executed:                         false
physical claim ready:                      false
GPU priority:                              none
```

The stale command-inventory blocker is closed for contract checks. The
inventory is still not a real simulation queue: every command uses
`--contract-check-only`, and no real FDTD command is marked executable.

## Decision

Use this refreshed inventory as the guarded preflight queue for the 84-grid
screen. The next useful step is to validate this artifact, then decide whether a
real row-level FDTD executor should be implemented.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh.py
5 passed
```

Figure check:

```text
2429x846, dynamic range=255
```
