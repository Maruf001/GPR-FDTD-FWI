# Experiment 1617: Post 84-Grid Contract-Check Execution Smoke Claim Boundary

Date: 2026-06-30

## Purpose

Fold the guarded 84-grid contract-check execution-smoke block into the local 2D
claim boundary.

Runs `1614-1616` show that all 84 contract-check commands can run and produce
hashable JSON outputs without running FDTD. This run records that as a guarded
engineering claim while keeping real FDTD execution and downstream scientific
claims blocked.

## Output

```text
outputs/experiments/1617_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claim boundary ready:                     true
claims:                                   31
guarded claims:                           28
blocked claims:                           3
contract-check smoke ready:               true
contract-check sensitivity ready:         true
command rows:                             84
contract-check JSON outputs:              84
contract-check passes:                    84
contract-check failures:                  0
real execution commands:                  0
executable real commands:                 0
real FDTD execution enabled:              false
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

The new guarded claim records command-plumbing readiness only: 84 contract-check
commands, 84 JSON outputs, 84 passes, and zero real execution commands. No FDTD
solver run was launched.

## Decision

Use run `1617` as the current local 2D claim boundary after the 84-grid
contract-check execution smoke. This does not support a physical result, GPU
run, field transfer, field FWI, or 3D/HPC escalation.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_contract_check_command_execution_smoke_validation_sensitivity.py
tests/test_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary.py
17 passed
```

Figure check:

```text
3941x894, dynamic range=255
```
