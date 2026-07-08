# Experiment 1700: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token External Staging Guard

Date: 2026-06-30

## Purpose

Audit the external approval-token boundary after the approval-token schema and
template block in runs `1697-1699`.

Run `1697` wrote an output-local approval-token template. This run checks that
the template did not become an external approval token and that the planned
observed-by-case materialization artifacts remain absent.

This run does not create an approval token, materialize observed arrays,
execute commands, run FDTD, start GPU work, transfer to field work, or start
3D/HPC work.

## Output

```text
outputs/experiments/1700_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_template_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_external_token_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_artifact_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard.png
scripts/
```

## Result

```text
source schema ready:                    true
source validation ready:                true
source sensitivity ready:               true
source approval gate ready:             true
local template present:                 true
local template has placeholders:        true
template is external token:             false
external approval token present:        false
external approval token accepted:       false
materialization artifacts planned:      20
planned cache artifacts:                10
planned result artifacts:               10
present materialization artifacts:      0
accepted materialization artifacts:     0
ready for materialization:              false
observed-by-case materialized:          false
commands executed:                      false
new FDTD executed:                      false
gpu work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
```

## Interpretation

The approval template remains an incomplete, output-local template. It has not
been copied into the locked external approval-token location, and no cache
arrays or result JSON files from the future materialization run exist.

## Decision

Use run `1700` as the external approval-token staging guard. Keep
observed-by-case materialization and FDTD execution blocked until a real
external approval token is supplied and the approval gate is rerun.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
