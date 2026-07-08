# Experiment 1616: 84-Grid Contract-Check Command Execution Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1615` validator for the run `1614` 84-grid
contract-check command execution smoke.

Run `1615` validated that 84 contract-check commands wrote 84 JSON outputs
without running FDTD. This run verifies that the validator rejects missing rows,
output-count drift, bad hashes, hidden FDTD execution, real-command promotion,
downstream promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1616_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                    10
expected pass scenarios:                  1
expected failure scenarios:               9
unexpected scenarios:                     0
validation sensitivity ready:             true
exact source artifacts pass:              true
hidden FDTD execution rejected:           true
real-command promotion rejected:          true
execution permitted:                      false
bounded CPU execution ready:              false
new FDTD executed:                        false
physical claim ready:                     false
GPU work ready:                           false
field transfer ready:                     false
field FWI ready:                          false
3D/HPC ready:                             false
GPU priority:                             none
```

The exact run `1614` artifacts pass. Damaged variants fail as expected for
command-count drift, missing execution rows, output-count drift, output-hash
damage, hidden FDTD execution, real-command promotion, physical-claim
promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `1614-1616` as the guarded 84-grid contract-check execution-smoke
block. This branch has validated command plumbing only; it has not run FDTD and
does not support a physical, GPU, field-transfer, field-FWI, or 3D/HPC claim.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validation_sensitivity.py
12 passed
```

Figure check:

```text
2465x852, dynamic range=255
```
