# Experiment 1618: Post 84-Grid Contract-Check Execution Smoke Claim Boundary Validator

Date: 2026-06-30

## Purpose

Validate run `1617`, the local 2D claim boundary after the 84-grid
contract-check execution smoke.

Run `1617` added a guarded claim for 84 contract-check commands and zero real
FDTD execution. This validator confirms the claim row, metrics, blocked
downstream states, figure, and script snapshots from saved artifacts.

## Output

```text
outputs/experiments/1618_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation checks passed:                  5
blocking failures:                         0
claim-boundary validation ready:           true
claims:                                    31
guarded claims:                            28
blocked claims:                            3
command rows:                              84
contract-check JSON outputs:               84
contract-check passes:                     84
real execution commands:                   0
real FDTD execution enabled:               false
execution permitted:                       false
bounded CPU execution ready:               false
new FDTD executed:                         false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
field FWI ready:                           false
3D/HPC ready:                              false
GPU priority:                              none
```

## Decision

Use run `1618` as the artifact guard for run `1617`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validator.py
9 passed
```

Figure check:

```text
2141x839, dynamic range=255
```
