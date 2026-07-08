# Experiment 1721: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Post-Work-Split Approval-Token Template Pack

Date: 2026-06-30

## Purpose

Create an output-local fillable approval-token template after the run
`1718-1720` post-work-split external guard.

The template is tied to the existing 12-field approval-token schema and the
current external materialization guard. It is a preparation artifact only. It
is not the locked external approval token and it cannot authorize
observed-by-case materialization or FDTD execution.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1721_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack
```

Key artifacts:

```text
templates/approval_token/APPROVED_1691_OBSERVED_BY_CASE_EXECUTION.template.json
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_template_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack.png
scripts/
```

## Result

```text
source schema ready:                   true
source schema validation ready:        true
source schema sensitivity ready:       true
source external guard ready:           true
source guard validation ready:         true
source guard sensitivity ready:        true
templates:                              1
template files written:                 1
output-local templates:                 1
schema fields:                         12
prefilled fields:                       8
placeholder fields:                     4
external approval token present:        0
template/external path overlaps:        0
templates accepted as approval:         0
external items checked:                21
materialization artifacts:             20
present external items:                 0
accepted external items:                0
ready for materialization:             false
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
template pack ready:                   true
```

Template fields:

```text
approval_id
approval_label
source_execution_contract_run
source_approval_gate_run
planned_job_count
expected_fdtd_trace_solve_count
approved_scope
execution_mode
approval_created_at_utc
approved_by
approval_reason
downstream_permission
```

## Interpretation

The approval request can now be drafted from an output-local template. Four
fields remain blank for real approval values: approval ID, timestamp, approver,
and reason.

The template does not change the execution boundary. The locked external
approval token is still absent, all 20 planned materialization artifacts are
still absent, and observed-by-case materialization remains blocked.

## Decision

Use the template to prepare the approval request. Keep observed-by-case
materialization and FDTD execution blocked until the real external token is
completed, copied to the locked external approval path, and accepted by the
approval/materialization gates.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack.py

3 passed
```

Figure validation:

```text
2285x848, dynamic range=255
```
