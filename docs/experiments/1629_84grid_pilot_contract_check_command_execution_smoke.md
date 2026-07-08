# Experiment 1629: 84-Grid Pilot Contract-Check Command Execution Smoke

Date: 2026-06-30

## Purpose

Execute the five pilot contract-check commands from run `1626` and verify that
they write concrete JSON outputs without running FDTD.

This run closes the command-smoke gap between the command inventory and any
future real pilot execution implementation.

## Output

```text
outputs/experiments/1629_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_execution_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke_summary.json
data/pilot_contract_check_outputs/payload_001_contract_check.json
data/pilot_contract_check_outputs/payload_023_contract_check.json
data/pilot_contract_check_outputs/payload_046_contract_check.json
data/pilot_contract_check_outputs/payload_072_contract_check.json
data/pilot_contract_check_outputs/payload_086_contract_check.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source inventory ready:                    true
source validation ready:                   true
source sensitivity ready:                  true
smoke ready:                               true
command rows:                              5
contract-check outputs written:            5
contract-check passes:                     5
contract-check failures:                   0
real execution command count:              0
executable real command count:             0
remaining pilot execution blockers:        1
new FDTD executed:                         false
GPU priority:                              none
```

All five selected pilot rows produced contract-check JSON files:

| Pilot order | Payload row | Exit code | Contract check ready | Real FDTD enabled | New FDTD executed | Pass |
| ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | 1 | 0 | true | false | false | true |
| 2 | 23 | 0 | true | false | false | true |
| 3 | 46 | 0 | true | false | false | true |
| 4 | 86 | 0 | true | false | false | true |
| 5 | 72 | 0 | true | false | false | true |

## Decision

Use run `1629` as the pilot command-execution smoke. It confirms that the
planned pilot commands can produce output artifacts, but it deliberately does
not enable real FDTD execution.

The remaining 2D blocker is now the real pilot execution implementation and
output validator.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_contract_check_command_execution_smoke.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
