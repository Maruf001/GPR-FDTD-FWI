# Experiment 1590: Post Runtime-Budget Triage Policy Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1589` validator against controlled damage to the
post-runtime-budget-triage claim boundary.

## Output

```text
outputs/experiments/1590_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                          26
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         25
observed failure scenarios:         25
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 1588:   true
validator rejects damaged variants: true
new FDTD executed:                  false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The damaged variants cover claim-count drift, triage-claim drift, budget
metric drift, false FDTD execution, downstream promotion, blank figures, and
missing script snapshots.

## Decision

Use runs `1588-1590` as the current guarded 2D post-runtime-budget-triage
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validator.py
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x885, dynamic range=255
```
