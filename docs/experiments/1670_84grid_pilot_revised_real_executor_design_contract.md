# Experiment 1670: 84-Grid Pilot Revised Real-Executor Design Contract

Date: 2026-06-30

## Purpose

Define the concrete implementation contract for the revised five-row real
pilot executor.

Run `1669` showed that the revised pilot has closed the semantic gap and is
blocked by implementation only. This run binds the revised payload rows,
transition-bin mapper, result templates, command checks, command-line
interface, and implementation steps into one executor design contract.

This run does not create the real executor script, execute FDTD, accept pilot
evidence, launch GPU work, transfer to field evidence, or promote 3D/HPC
readiness.

## Output

```text
outputs/experiments/1670_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_executor_design_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_executor_design_contract_payload_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_executor_design_contract_cli_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_executor_design_contract_implementation_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_executor_design_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_executor_design_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source closure ready:                  true
design payloads:                       5
required payload IDs:                  1;23;46;68;72
contains payload 68:                   true
contains stale payload 86:             false
objective profiles:                    4
mapper-bound payloads:                 5
template-bound payloads:               5
command-bound payloads:                5
direct-offset payloads:                2
payloads at/above crossing:            1
CLI arguments:                         6
required CLI arguments:                5
implementation steps:                  8
steps ready before execution:          3
real executor script available:        false
real result files:                     0
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
3D/HPC ready:                          false
design contract ready:                 true
```

Payload binding:

| Payload row | Objective profile | Transition bin | Candidate Tx/Rx offset (mm) |
| ---: | --- | ---: | ---: |
| 1 | highband | 0 | 40.000 |
| 23 | late | 4 | 41.176 |
| 46 | late_high | 9 | 42.647 |
| 68 | veryhigh | 13 | 43.824 |
| 72 | veryhigh | 17 | 45.000 |

## Interpretation

The real executor now has a concrete implementation target. Each revised
payload is bound to a candidate Tx/Rx offset, a standard objective definition,
a result-template path, a staged result path, and a JSON parse/checksum command.

This is still a design contract. The executable script does not exist, and no
real FDTD result file exists.

## Decision

Use run `1670` as the real-executor implementation contract. The next 2D task
can be implementing the separate real executor against this contract, while
keeping FDTD execution blocked until the executor writes and validates the five
required JSON outputs.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_executor_design_contract.py
5 passed
```

Figure check:

```text
2321x847, dynamic range=255
```
