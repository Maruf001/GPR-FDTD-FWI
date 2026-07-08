# Experiment 1634: 84-Grid Pilot Real-Execution Preflight Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1633` validator.

The exact run `1632` gap audit should pass. Damaged source readiness, probe
counts, refusal counts, accidental execution, design-level execution promotion,
action promotion/count drift, downstream promotion, figure damage, and
script-snapshot damage should fail.

## Output

```text
outputs/experiments/1634_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     11
expected pass scenarios:                   1
expected failure scenarios:                10
unexpected scenarios:                      0
gap-audit sensitivity ready:               true
exact source artifacts pass:               true
probe damage rejected:                     true
execution-permission promotion rejected:   true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
new FDTD executed:                         false
GPU priority:                              none
```

## Decision

Use runs `1632-1634` as the guarded real-execution preflight gap block. The
next 2D implementation task is a duplicated real pilot executor and output
validator, not full 84-row execution.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
