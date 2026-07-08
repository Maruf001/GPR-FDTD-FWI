# Experiment 1589: Post Runtime-Budget Triage Policy Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved claim-boundary artifacts from run `1588`.

## Output

```text
outputs/experiments/1589_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validator.png
```

## Result

```text
validation checks:                    5
validation checks passed:             5
blocking failures:                    0
claim-boundary validation ready:      true
claims:                               28
guarded claims:                       25
blocked claims:                       3
default recommended grid models:      90
two-hour recommended grid models:     90
first budget allowing 200-grid screen: 150 min
new FDTD executed:                    false
GPU work ready:                       false
field FWI ready:                      false
3D/HPC ready:                         false
```

The validator confirms the claim counts, triage-claim support, budget metrics,
blocked downstream states, nonblank figure output, and script snapshots.

## Decision

Use this validator as the artifact guard for run `1588`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_validator.py
9 passed
```

Figure check:

```text
2645x832, dynamic range=255
```
