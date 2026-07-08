# Experiment 1643: 84-Grid Pilot Real-Result File Acceptance Gate Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1642` validator.

The exact run `1641` artifacts should pass. Damaged source readiness, file
counts, live-file promotion, nonempty-file promotion, JSON-parse promotion,
result acceptance, FDTD execution, template substitution, field-count drift,
field acceptance, action damage, downstream promotion, figure damage, and
script-snapshot damage should fail.

## Output

```text
outputs/experiments/1643_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     16
expected pass scenarios:                   1
expected failure scenarios:                15
unexpected scenarios:                      0
result-file gate sensitivity ready:        true
exact source artifacts pass:               true
file damage rejected:                      true
field damage rejected:                     true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
new FDTD executed:                         false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
file_count_drift
file_present_promotion
file_nonempty_promotion
json_parse_promotion
result_acceptance_promotion
fdtd_execution_promotion
template_allowed_promotion
field_count_drift
field_acceptance_promotion
action_ready_promotion
action_count_drift
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `1641-1643` as the result-file acceptance gate before any real
five-row pilot evidence. The next useful implementation step is the bounded
real pilot executor.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validation_sensitivity.py
4 passed
```

Figure check:

```text
3077x840, dynamic range=255
```
