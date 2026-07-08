# Experiment 1613: 84-Grid Contract-Check Command Inventory Refresh Validator

Date: 2026-06-30

## Purpose

Validate run `1612`, the refreshed contract-check command inventory for the
84-grid CPU screen.

Run `1612` rebuilt all selected command rows against the guarded executor
interface and probed all 84 selected rows without executing FDTD. This validator
checks that the saved command inventory is contract-check only and remains
non-executing.

## Output

```text
outputs/experiments/1613_local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                          5
validation checks passed:                   5
blocking failures:                          0
contract-check inventory validation ready:  true
selected payload rows:                      84
refreshed command rows:                     84
contract-check probes passed:               84
real execution command count:               0
executable real command count:              0
real FDTD execution enabled:                false
execution permitted:                        false
new FDTD executed:                          false
physical claim ready:                       false
GPU priority:                               none
```

The validator confirms that all 84 command rows are contract-check only, all 84
probes passed, and no command or downstream state was promoted to real FDTD
execution.

## Decision

Use run `1613` as the artifact guard for the refreshed command inventory. The
remaining decision is no longer command-inventory consistency; it is whether a
real row-level FDTD executor should be implemented and run.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_inventory_refresh_validator.py
9 passed
```

Figure check:

```text
2177x834, dynamic range=255
```
