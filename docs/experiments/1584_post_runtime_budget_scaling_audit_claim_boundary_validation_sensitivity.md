# Experiment 1584: Post Runtime-Budget Scaling Audit Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1583` validator for the post-runtime-budget claim
boundary.

## Output

```text
outputs/experiments/1584_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                          23
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         22
observed failure scenarios:         22
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 1582:   true
validator rejects damaged variants: true
new FDTD executed:                  false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The damaged variants cover claim-count drift, runtime-budget claim drift,
budget metric drift, false new FDTD execution, downstream promotion, figure
drift, and script-snapshot drift.

## Decision

Use runs `1582-1584` as the current guarded 2D post-runtime-budget
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validator.py
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x885, dynamic range=255
```
