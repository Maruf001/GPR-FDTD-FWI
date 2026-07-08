# Experiment 1615: 84-Grid Contract-Check Command Execution Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `1614`, the executable contract-check smoke for the 84-grid screen.

Run `1614` wrote 84 contract-check JSON outputs without running FDTD. This
validator checks that the saved outputs are complete, hashed, non-FDTD, and
non-promotional.

## Output

```text
outputs/experiments/1615_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         4
validation checks passed:                  4
blocking failures:                         0
contract-check smoke validation ready:     true
command rows:                              84
contract-check JSON outputs:               84
contract-check passes:                     84
real execution command count:              0
real FDTD execution enabled:               false
execution permitted:                       false
new FDTD executed:                         false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
field FWI ready:                           false
3D/HPC ready:                              false
GPU priority:                              none
```

## Decision

Use run `1615` as the artifact guard for run `1614`. The 84-row branch is now
safe through contract-check command execution, but it still has no real FDTD
solver execution or physical result.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validator.py
8 passed
```

Figure check:

```text
2105x838, dynamic range=255
```
