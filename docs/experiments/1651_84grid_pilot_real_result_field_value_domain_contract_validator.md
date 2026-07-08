# Experiment 1651: 84-Grid Pilot Real-Result Field Value-Domain Contract Validator

Date: 2026-06-30

## Purpose

Validate run `1650` from its saved artifacts.

This run checks the 50-field shape, five payloads, ten repeated required
fields, expected value-domain counts, zero accepted field values, blocked
actions, blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1651_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         4
validation passes:                         4
blocking failures:                         0
required field value contracts:            50
required field names:                      10
payloads:                                  5
value actions:                             3
field value-domain validation ready:       true
GPU priority:                              none
```

## Decision

Run `1650` validates as the current five-row pilot field value-domain contract.
It still accepts no real field values.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
