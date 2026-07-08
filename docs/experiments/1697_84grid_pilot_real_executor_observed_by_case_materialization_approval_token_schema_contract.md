# Experiment 1697: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval Token Schema Contract

Date: 2026-06-30

## Purpose

Define the exact approval-token schema required before `observed_by_case`
materialization can be accepted.

Runs `1694-1696` define and guard the approval gate. This run adds the token
schema and an output-local template, without creating the external approval
token or allowing any execution.

## Output

```text
outputs/experiments/1697_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract
```

Key artifacts:

```text
data/approval_token_template/APPROVED_1691_OBSERVED_BY_CASE_EXECUTION.template.json
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_schema_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract.png
scripts/
```

## Result

```text
source gate ready:                       true
source validation ready:                 true
source sensitivity ready:                true
schema fields:                           12
required schema fields:                  12
placeholder fields:                      4
template written:                        true
external approval token present:         false
external approval token accepted:        false
actions:                                 3
ready actions:                           0
ready for materialization:               false
observed_by_case materialized:           false
commands executed:                       false
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

The template requires real values for:

```text
approval_id
approval_created_at_utc
approved_by
approval_reason
```

The token is explicitly scoped to `observed_by_case_materialization_only`, with
`downstream_permission` set to `false`.

## Interpretation

The approval boundary is now concrete. A future materialization run cannot be
accepted by the presence of an arbitrary file; it must satisfy this 12-field
schema and then pass the guarded approval gate again.

## Decision

Do not materialize `observed_by_case` until the locked external approval token
is completed, copied, and the approval gate is rerun. This schema does not
permit GPU work, field transfer, field FWI, or 3D/HPC escalation.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract.py

4 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
