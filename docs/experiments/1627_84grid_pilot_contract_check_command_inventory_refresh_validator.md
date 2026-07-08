# Experiment 1627: 84-Grid Pilot Contract-Check Command Inventory Validator

Date: 2026-06-30

## Purpose

Validate run `1626` from saved artifacts.

The validator checks that the five pilot contract-check commands exist, all
five in-process probes pass, no real commands are executable, and downstream
execution states remain blocked.

## Output

```text
outputs/experiments/1627_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         4
validation passes:                         4
blocking failures:                         0
command inventory validation ready:        true
pilot command rows:                        5
contract-check probe passes:               5
remaining pilot execution blockers:        1
new FDTD executed:                         false
GPU priority:                              none
```

## Decision

Use this validator as the artifact guard for run `1626`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validator.py
3 passed
```

Figure check:

```text
1925x840, dynamic range=255
```
