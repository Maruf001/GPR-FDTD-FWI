# Experiment 1580: Runtime Budget Scaling Audit Validator

Date: 2026-06-29

## Purpose

Validate the runtime budget scaling audit from run `1579`.

## Output

```text
outputs/experiments/1580_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validator_checks.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validator.png
```

## Result

```text
validation checks:                  5
validation checks passed:           5
blocking failures:                  0
runtime budget validation ready:    true
forecast scenarios:                 5
largest forecast grid models:       200
longest forecast minutes:           130.42766666666668
new FDTD executed:                  false
bounded CPU planning ready:         true
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The validator confirms the forecast shape, measured-rate provenance,
20-grid replay match, 200-grid longest forecast, blocked downstream states,
figure output, and script snapshots.

## Decision

Use this validator as the artifact guard for run `1579`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit.py
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validator.py
9 passed
```

Figure check:

```text
2645x835, dynamic range=255
```
