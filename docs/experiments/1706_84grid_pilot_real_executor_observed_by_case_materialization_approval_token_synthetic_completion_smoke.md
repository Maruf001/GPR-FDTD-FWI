# Experiment 1706: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Synthetic Completion Smoke

Date: 2026-06-30

## Purpose

Test whether the approval-token schema from runs `1697-1705` can be completed
mechanically without creating a real approval token or running FDTD.

This run writes a synthetic completed token inside its own output directory
only. It does not copy anything to the locked external approval-token path and
does not approve observed-by-case materialization.

## Output

```text
outputs/experiments/1706_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke
```

Key artifacts:

```text
data/synthetic_approval_token/APPROVED_1691_OBSERVED_BY_CASE_EXECUTION.synthetic.json
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_synthetic_token_validation_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke.png
scripts/
```

## Result

```text
source route ready:                 true
source schema ready:                true
completion fields required:         4
synthetic completion fields filled: 4
schema fields checked:              12
schema rules passed:                12
synthetic token written:            true
synthetic token is output-local:     true
synthetic token is external token:   false
external approval token present:     false
approval completion ready:           false
ready for materialization:           false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The four synthetic fields are `approval_id`, `approval_created_at_utc`,
`approved_by`, and `approval_reason`. All fixed schema fields remain locked to
the earlier execution contract, including 10 planned jobs, 80 expected FDTD
trace solves, `observed_by_case_materialization_only`, `bounded_cpu`, and
`downstream_permission=false`.

## Interpretation

The approval-token schema itself is not the blocker. The blocker is the real
approval boundary: a real completed token must be placed at the locked external
path and then the approval gate must be rerun.

## Decision

Use run `1706` as a schema smoke test only. Keep observed-by-case
materialization, FDTD execution, GPU work, field transfer, field FWI, and
3D/HPC blocked until a real external approval token exists and passes the gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke.py

4 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
