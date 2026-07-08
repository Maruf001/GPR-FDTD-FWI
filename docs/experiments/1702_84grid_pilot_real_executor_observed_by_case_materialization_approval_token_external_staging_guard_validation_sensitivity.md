# Experiment 1702: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token External Staging Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `1701`.

This run checks that the validator accepts the exact run `1700` guard and
rejects damaged states that would falsely promote an approval token,
materialization artifact, FDTD execution, downstream readiness, or damaged
artifacts.

## Output

```text
outputs/experiments/1702_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
cases:                               17
expected pass cases:                 1
expected fail cases:                 16
actual pass cases:                   1
actual fail cases:                   16
unexpected outcomes:                 0
damaged cases:                       16
commands executed:                   false
new FDTD executed:                   false
gpu work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The damaged states cover source-chain damage, template removal, template
promotion to an external token, template acceptance as approval, external
token presence, external-token acceptance, artifact-row removal, planned
cache/result count damage, materialization-artifact promotion,
materialization-readiness promotion, FDTD execution promotion, GPU-readiness
promotion, figure damage, and script-snapshot damage.

## Interpretation

The validator is sensitive to the failure modes that would matter before
materializing observed-by-case arrays. It does not permit an incomplete local
template to act as approval, and it does not permit planned artifacts to be
promoted as real execution outputs.

## Decision

Use runs `1700-1702` as the closed approval-token external staging boundary.
Keep observed-by-case materialization and FDTD execution blocked until a real
external approval token passes the guarded schema and gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
