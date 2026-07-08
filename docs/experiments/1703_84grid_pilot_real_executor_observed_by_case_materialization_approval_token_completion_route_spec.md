# Experiment 1703: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Completion Route Spec

Date: 2026-06-30

## Purpose

Convert the approval-token blocker from runs `1700-1702` into a completion
route.

Run `1697` defined a 12-field approval-token schema. Runs `1700-1702`
confirmed that the local template stayed output-local and incomplete. This run
identifies the four real values that must be completed before the token can be
copied to the locked external approval-token path.

This run does not create an approval token, materialize observed arrays,
execute commands, run FDTD, start GPU work, transfer to field work, or start
3D/HPC work.

## Output

```text
outputs/experiments/1703_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_completion_field_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_phase_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec.png
scripts/
```

## Result

```text
source external guard ready:          true
source validation ready:              true
source sensitivity ready:             true
source schema ready:                  true
completion fields:                    4
completed fields:                     0
route phases:                         4
ready phases:                         0
external approval token present:      false
external approval token accepted:     false
approval-token completion ready:      false
ready for materialization:            false
observed-by-case materialized:        false
new FDTD executed:                    false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

The four completion fields are:

| Order | Field | Acceptance rule |
| ---: | --- | --- |
| 1 | `approval_id` | non-empty unique approval identifier |
| 2 | `approval_created_at_utc` | ISO-8601 UTC timestamp |
| 3 | `approved_by` | non-empty approver identity |
| 4 | `approval_reason` | non-empty reason for materializing observed arrays |

## Interpretation

The next 2D execution blocker is not a missing script or a hidden compute
step. It is explicit approval. The approval token needs four real values, then
the completed JSON must be copied to the locked external path and the approval
gate rerun.

## Decision

Use run `1703` as the current 2D approval-token completion route. Keep
observed-by-case materialization and FDTD execution blocked until the approval
token is completed and the approval gate is rerun.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
