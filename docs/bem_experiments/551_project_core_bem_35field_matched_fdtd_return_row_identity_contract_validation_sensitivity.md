# BEM Experiment 551: Matched-FDTD Return Row-Identity Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `550` validator with controlled damaged variants of the
run `549` artifacts.

The sensitivity set tests source readiness damage, missing row identities,
duplicate row identities, sequence-hash drift, staged-file promotion,
premature row acceptance, action promotion, downstream promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/551_project_core_bem_35field_matched_fdtd_return_row_identity_contract_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_row_identity_contract_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_row_identity_contract_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_row_identity_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source contract ready:                     true
source validator ready:                    true
sensitivity scenarios:                     11
expected pass scenarios:                   1
expected failure scenarios:                10
unexpected scenarios:                      0
source damage rejected:                    true
row damage rejected:                       true
sequence damage rejected:                  true
file promotion rejected:                   true
acceptance promotion rejected:             true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
sensitivity ready:                         true
GPU priority:                              none
```

## Decision

Runs `549-551` are the guarded BEM row-identity lock for future matched-FDTD
return CSV files. The next BEM step remains real FDTD return-file production or
intake, not comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_row_identity_contract_validation_sensitivity.py
2 passed
```

Figure check:

```text
2825x840, dynamic range=255
```
