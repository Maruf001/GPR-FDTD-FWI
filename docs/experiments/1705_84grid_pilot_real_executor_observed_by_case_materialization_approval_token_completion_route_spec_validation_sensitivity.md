# Experiment 1705: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Completion Route Spec Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `1704`.

This run checks that the validator accepts the exact run `1703` route and
rejects damaged states that would falsely complete approval fields, promote an
external approval token, promote materialization, execute FDTD, promote
downstream work, or damage artifacts.

## Output

```text
outputs/experiments/1705_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:         true
cases:                          15
expected pass cases:            1
expected fail cases:            14
actual pass cases:              1
actual fail cases:              14
unexpected outcomes:            0
damaged cases:                  14
new FDTD executed:              false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

The damaged states cover source readiness removal, completion-field removal,
field-count damage, field-completion promotion, external-token presence or
acceptance, phase removal, phase-readiness promotion, approval-completion
promotion, materialization-readiness promotion, FDTD execution, GPU-readiness
promotion, figure damage, and script-snapshot damage.

## Interpretation

The completion-route validator is sensitive to the failure modes that would
matter before running observed-by-case materialization.

## Decision

Use runs `1703-1705` as the current closed 2D approval-token completion block.
Keep observed-by-case materialization blocked until a completed real approval
token passes the gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
