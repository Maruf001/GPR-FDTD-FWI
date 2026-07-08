# Experiment 1630: 84-Grid Pilot Contract-Check Command Execution Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `1629` from saved artifacts.

The validator checks that the five contract-check JSON outputs exist, their
hashes match the execution table, no FDTD execution was enabled, the downstream
states remain blocked, and the figure and script snapshots are present.

## Output

```text
outputs/experiments/1630_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         4
validation passes:                         4
blocking failures:                         0
smoke validation ready:                    true
command rows:                              5
contract-check outputs:                    5
contract-check passes:                     5
remaining pilot execution blockers:        1
new FDTD executed:                         false
GPU priority:                              none
```

The validator passed all four checks:

| Check | Pass |
| --- | --- |
| source chain ready | true |
| five hashed contract-check outputs | true |
| real execution stays blocked | true |
| figure and script snapshots present | true |

## Decision

Use run `1630` as the artifact validator for the run `1629` command-execution
smoke. The five-row pilot has a validated no-FDTD command smoke, but real pilot
execution still needs a separate implementation and output validator.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validator.py
3 passed
```

Figure check:

```text
1925x841, dynamic range=255
```
