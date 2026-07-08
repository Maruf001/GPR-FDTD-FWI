# BEM Experiment 553: Matched-FDTD Return Value-Domain Contract Validator

Date: 2026-06-30

## Purpose

Validate run `552` from its saved artifacts.

This run checks the 558-row value-domain shape, the 279/279 split between
hash-string and positive-float rules, the zero-real-value state, blocked
actions, blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/553_project_core_bem_35field_matched_fdtd_return_value_domain_contract_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_value_domain_contract_validator_checks.csv
data/project_core_bem_35field_matched_fdtd_return_value_domain_contract_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_value_domain_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         4
validation passes:                         4
blocking failures:                         0
required value contracts:                  558
source-hash value contracts:               279
positive-float value contracts:            279
value actions:                             3
value-domain validation ready:             true
GPU priority:                              none
```

## Decision

Run `552` validates as the current BEM value-domain contract. It still accepts
no real FDTD return values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_value_domain_contract_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
