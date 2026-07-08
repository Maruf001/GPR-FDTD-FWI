# Experiment 1586: Runtime Budget Triage Policy Validator

Date: 2026-06-29

## Purpose

Validate the saved runtime-budget triage policy from run `1585`.

## Output

```text
outputs/experiments/1586_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validator_checks.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validator_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validator.png
```

## Result

```text
validation checks:                    5
validation checks passed:             5
blocking failures:                    0
triage-policy validation ready:       true
budget tiers:                         5
default budget:                       60 min
default recommended grid models:      90
two-hour recommended grid models:     90
first budget allowing 200-grid screen: 150 min
new FDTD executed:                    false
GPU work ready:                       false
field FWI ready:                      false
3D/HPC ready:                         false
```

The validator confirms the five budget tiers, the one-hour and two-hour
decisions, no new FDTD execution, blocked downstream states, nonblank figure
output, and script snapshots.

## Decision

Use this validator as the artifact guard for run `1585`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy.py
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validator.py
9 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
