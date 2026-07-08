# Experiment 1619: Post 84-Grid Contract-Check Execution Smoke Claim Boundary Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1618` validator for the local 2D claim boundary after the
84-grid contract-check execution smoke.

Run `1617` added a guarded claim for 84 contract-check commands and zero real
FDTD execution. Run `1618` validated that boundary from saved artifacts. This
run verifies that the validator accepts the exact saved state and rejects
damaged or prematurely promoted states.

## Output

```text
outputs/experiments/1619_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                    10
expected pass scenarios:                  1
expected failure scenarios:               9
unexpected scenarios:                     0
claim-boundary sensitivity ready:         true
exact source artifacts pass:              true
real-command promotion rejected:          true
downstream promotion rejected:            true
execution permitted:                      false
new FDTD executed:                        false
physical claim ready:                     false
GPU work ready:                           false
field transfer ready:                     false
field FWI ready:                          false
3D/HPC ready:                             false
GPU priority:                             none
```

The exact run `1617` boundary passes. Nine damaged variants fail as expected:

| Scenario | Expected result | Failed check |
| --- | --- | --- |
| claim count drift | fail | claim boundary counts |
| claim support drift | fail | smoke claim support |
| output count drift | fail | contract-check smoke metrics |
| real command promotion | fail | contract-check smoke metrics |
| hidden FDTD promotion | fail | blocked downstream states |
| downstream GPU promotion | fail | blocked downstream states |
| blocked support drift | fail | blocked-row support |
| figure damage | fail | figure and script snapshots |
| script snapshot damage | fail | figure and script snapshots |

## Decision

Use runs `1617-1619` as the guarded post-contract-check-smoke local 2D
claim-boundary block. The block supports a validated non-execution claim only:
84 contract-check commands can be generated and checked, but real 2D FDTD
execution and downstream physical claims remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validator.py
tests/test_local_2d_state_consistent_objective_revision_post_84grid_contract_check_execution_smoke_claim_boundary_validation_sensitivity.py
13 passed
```

Figure check:

```text
2465x851, dynamic range=255
```
