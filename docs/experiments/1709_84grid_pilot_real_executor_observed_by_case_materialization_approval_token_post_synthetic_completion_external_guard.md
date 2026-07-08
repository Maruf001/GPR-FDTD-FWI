# Experiment 1709: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Post-Synthetic Completion External Guard

Date: 2026-06-30

## Purpose

Audit the external approval boundary after the synthetic approval-token smoke
in runs `1706-1708`.

Run `1706` proved that the approval-token schema can be filled in an
output-local synthetic token. This run checks that the synthetic token did not
become the real external approval token and that no observed-by-case
materialization artifacts appeared.

This run does not create a real approval token, materialize arrays, execute
commands, run FDTD, start GPU work, transfer to field work, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1709_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_token_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_artifact_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard.png
scripts/
```

## Result

```text
source synthetic smoke ready:        true
source validation ready:             true
source sensitivity ready:            true
synthetic token present:             true
synthetic token is external token:    false
synthetic token under external root:  false
external approval token present:      false
external approval token accepted:     false
approval token completion ready:      false
materialization artifacts planned:    20
planned cache artifacts:              10
planned result artifacts:             10
present materialization artifacts:    0
accepted materialization artifacts:   0
ready for materialization:            false
observed-by-case materialized:        false
commands executed:                    false
new FDTD executed:                    false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

## Interpretation

The synthetic token is useful only as a schema smoke test. It stays inside run
`1706` and does not occupy the locked external approval-token path. The planned
materialization payload still has zero cache arrays and zero result JSON files.

## Decision

Use run `1709` as the post-synthetic external guard. Keep observed-by-case
materialization, FDTD execution, GPU work, field transfer, field FWI, and
3D/HPC blocked until a real external approval token exists and passes the gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
