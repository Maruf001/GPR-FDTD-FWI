# Experiment 1583: Post Runtime-Budget Scaling Audit Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the post-runtime-budget claim boundary from run `1582`.

## Output

```text
outputs/experiments/1583_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validator.png
```

## Result

```text
validation checks:                  5
validation checks passed:           5
blocking failures:                  0
claim-boundary validation ready:    true
claims:                             27
guarded claims:                     24
blocked claims:                     3
forecast scenarios:                 5
largest forecast grid models:       200
longest forecast minutes:           130.42766666666668
new FDTD executed:                  false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The validator confirms claim counts, the runtime-budget claim support, the
budget metrics, blocked rows, downstream blocked states, figure output, and
script snapshots.

## Decision

Use this validator as the artifact guard for run `1582`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_validator.py
9 passed
```

Figure check:

```text
2645x832, dynamic range=255
```
