# Experiment 1587: Runtime Budget Triage Policy Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1586` validator against controlled damage to the runtime
budget triage policy.

## Output

```text
outputs/experiments/1587_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validation_sensitivity.png
```

## Result

```text
scenarios:                          27
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         26
observed failure scenarios:         26
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 1585:   true
validator rejects damaged variants: true
new FDTD executed:                  false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The damaged variants cover source-readiness drift, budget-tier drift, default
decision drift, two-hour decision drift, false FDTD execution, downstream
promotion, blank figures, and missing script snapshots.

## Decision

Use runs `1585-1587` as the guarded 2D runtime-budget triage-policy block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy.py
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validator.py
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x886, dynamic range=255
```
