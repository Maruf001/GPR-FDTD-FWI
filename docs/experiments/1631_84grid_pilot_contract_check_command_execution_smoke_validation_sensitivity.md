# Experiment 1631: 84-Grid Pilot Contract-Check Command Execution Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1630` validator.

The exact run `1629` command-execution smoke should pass. Damaged source
readiness, output counts, missing rows, output hashes, output payload flags,
real-command promotion, downstream promotion, figure damage, and missing script
snapshots should fail.

## Output

```text
outputs/experiments/1631_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     11
expected pass scenarios:                   1
expected failure scenarios:                10
unexpected scenarios:                      0
smoke validation sensitivity ready:        true
exact source artifacts pass:               true
source-chain damage rejected:              true
output-artifact damage rejected:           true
real-execution promotion rejected:         true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
new FDTD executed:                         false
GPU priority:                              none
```

Scenario outcome:

| Scenario | Expected pass | Actual pass | Failed checks |
| --- | --- | --- | --- |
| exact source artifacts | true | true |  |
| source chain not ready | false | false | source chain ready |
| output count drift | false | false | five hashed contract-check outputs |
| missing output row | false | false | five hashed contract-check outputs |
| output hash drift | false | false | five hashed contract-check outputs |
| output payload promotes real execution | false | false | five hashed contract-check outputs |
| row FDTD execution promotion | false | false | five hashed contract-check outputs; real execution stays blocked |
| real command promotion | false | false | real execution stays blocked |
| downstream promotion | false | false | real execution stays blocked |
| figure damage | false | false | figure and script snapshots present |
| script snapshot damage | false | false | figure and script snapshots present |

## Decision

Use runs `1629-1631` as the guarded no-FDTD command-smoke block for the
five-row pilot. The pilot command path is now validated through output files and
damage sensitivity. The next 2D task is a separate real pilot execution design,
not a full 84-row execution.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_validation_sensitivity.py
4 passed
```

Figure check:

```text
2645x837, dynamic range=255
```
