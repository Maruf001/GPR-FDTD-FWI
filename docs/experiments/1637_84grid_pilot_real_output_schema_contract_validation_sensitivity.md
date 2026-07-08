# Experiment 1637: 84-Grid Pilot Real-Output Schema Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1636` validator.

The exact run `1635` schema contract should pass. Damaged source readiness,
output counts, required fields, real-output promotion, schema acceptance,
FDTD-execution promotion, template substitution, action readiness, downstream
promotion, figure damage, and script-snapshot damage should fail.

## Output

```text
outputs/experiments/1637_local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     13
expected pass scenarios:                   1
expected failure scenarios:                12
unexpected scenarios:                      0
schema validation sensitivity ready:       true
exact source artifacts pass:               true
count or field damage rejected:            true
file or acceptance promotion rejected:     true
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
output_file_count_drift
field_requirement_count_drift
required_field_damage
real_output_file_promotion
schema_acceptance_promotion
fdtd_execution_promotion
template_allowed_promotion
action_damage
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `1635-1637` as the guarded real-output schema block before
implementing any real five-row pilot executor. The next 2D task is a bounded
real-pilot executor implementation that writes to this schema, not full 84-row
execution.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validation_sensitivity.py
4 passed
```

Figure check:

```text
2825x839, dynamic range=255
```
