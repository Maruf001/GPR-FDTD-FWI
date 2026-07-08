# Experiment 1581: Runtime Budget Scaling Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1580` validator for the run `1579` runtime budget scaling
audit.

## Output

```text
outputs/experiments/1581_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validation_sensitivity.png
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
validator accepts exact run 1579:   true
validator rejects damaged variants: true
new FDTD executed:                  false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The damaged variants cover readiness drift, scenario-count drift, forecast row
shape drift, measured-rate drift, false FDTD execution, downstream promotion,
figure drift, and script-snapshot drift.

## Decision

Use runs `1579-1581` as the guarded 2D runtime-budget scaling audit block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit.py
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validator.py
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x890, dynamic range=255
```
