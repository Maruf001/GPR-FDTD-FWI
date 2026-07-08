# Experiment 1605: 90-Grid Execution Readiness Gate Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1604` validator against controlled damage to the
execution-readiness gate.

## Output

```text
outputs/experiments/1605_local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       23
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  22
observed failure scenarios:                  22
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 1603:            true
validator rejects damaged variants:          true
execution permitted:                         false
bounded CPU execution ready:                 false
commands executed:                           false
new FDTD executed:                           false
```

The damaged variants cover execution promotion, source-metric drift, budget
headroom promotion, execution-contract promotion, hidden execution, downstream
promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `1603-1605` as the guarded execution-readiness block before any
90-grid 2D CPU screen is run.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_90grid_execution_readiness_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x904, dynamic range=255
```
