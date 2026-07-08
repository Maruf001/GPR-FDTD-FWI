# BEM Experiment 554: Matched-FDTD Return Value-Domain Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `553` validator with controlled damaged variants of the
run `552` artifacts.

The sensitivity set tests source damage, missing value rows, value-domain
misclassification, premature value presence, premature value acceptance,
action promotion, comparison promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/bem_experiments/554_project_core_bem_35field_matched_fdtd_return_value_domain_contract_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_value_domain_contract_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_value_domain_contract_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_value_domain_contract_validation_sensitivity.png
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
value damage rejected:                     true
value promotion rejected:                  true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
sensitivity ready:                         true
GPU priority:                              none
```

## Decision

Runs `552-554` are the guarded BEM value-domain block after the row-identity
lock. The next comparison step still requires real matched-FDTD return files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_value_domain_contract_validation_sensitivity.py
2 passed
```

Figure check:

```text
2717x840, dynamic range=255
```
