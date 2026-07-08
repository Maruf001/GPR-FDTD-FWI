# Experiment 1652: 84-Grid Pilot Real-Result Field Value-Domain Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1651` validator with controlled damaged variants of the
run `1650` artifacts.

The sensitivity set tests source damage, missing field rows, field-domain
misclassification, premature field presence, premature field acceptance,
action promotion, FDTD promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1652_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source contract ready:                     true
source validator ready:                    true
sensitivity scenarios:                     10
expected pass scenarios:                   1
expected failure scenarios:                9
unexpected scenarios:                      0
source damage rejected:                    true
field damage rejected:                     true
field promotion rejected:                  true
FDTD promotion rejected:                   true
figure damage rejected:                    true
script-snapshot damage rejected:           true
sensitivity ready:                         true
GPU priority:                              none
```

## Decision

Runs `1650-1652` are the guarded five-row pilot field value-domain block after
the file-identity lock. The next 2D implementation step remains writing real
five-row pilot result JSON files and rerunning acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validation_sensitivity.py
2 passed
```

Figure check:

```text
2717x840, dynamic range=255
```
