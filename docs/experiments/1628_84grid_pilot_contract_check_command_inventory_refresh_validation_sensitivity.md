# Experiment 1628: 84-Grid Pilot Contract-Check Command Inventory Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1627` validator.

The exact run `1626` command inventory should pass. Source readiness damage,
command-count drift, probe failure, real-command promotion, command execution
promotion, FDTD execution promotion, downstream promotion, figure damage, and
script-snapshot damage should fail.

## Output

```text
outputs/experiments/1628_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     10
expected pass scenarios:                   1
expected failure scenarios:                9
unexpected scenarios:                      0
command inventory sensitivity ready:       true
exact source artifacts pass:               true
command inventory damage rejected:         true
real execution promotion rejected:         true
downstream promotion rejected:             true
new FDTD executed:                         false
GPU priority:                              none
```

## Decision

Use runs `1626-1628` as the guarded pilot contract-check command-inventory
block. The next 2D task is a pilot command execution smoke or a real-execution
implementation path; the full 84-row screen remains blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_inventory_refresh_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x858, dynamic range=255
```
