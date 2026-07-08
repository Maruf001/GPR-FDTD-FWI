# Experiment 1722: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Post-Work-Split Approval-Token Template-Pack Validator

Date: 2026-06-30

## Purpose

Validate the run `1721` approval-token template pack from generated artifacts.

The validator checks that the template is output-local, follows the 12-field
approval-token schema, preserves four real approval placeholders, does not
overlap the locked external approval-token path, and does not promote
materialization or FDTD execution.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1722_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
templates:                      1
schema fields:                 12
prefilled fields:               8
placeholder fields:             4
external approval token present: 0
present external items:         0
accepted external items:        0
ready for materialization:      false
new FDTD executed:              false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
validation ready:               true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source template pack ready | pass |
| 2 | template row is output-local and schema shaped | pass |
| 3 | template payload matches approval-token schema | pass |
| 4 | materialization and downstream remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The approval-token template validates as preparation only. It can be used to
draft the real approval request, but it is not the locked external approval
token and it cannot authorize observed-by-case materialization.

## Decision

Use this validator as the artifact guard for run `1721`. Keep materialization
and FDTD execution blocked until the completed external approval token and all
planned materialization artifacts are present and accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validator.py

6 passed
```

Figure validation:

```text
2285x832, dynamic range=255
```
