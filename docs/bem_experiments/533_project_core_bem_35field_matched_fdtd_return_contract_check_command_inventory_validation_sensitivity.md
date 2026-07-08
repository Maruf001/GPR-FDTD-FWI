# BEM Experiment 533: Matched FDTD Return Contract-Check Command Inventory Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `532` validator.

The exact run `531` command inventory should pass. Damaged source readiness,
command counts, missing command rows, probe hashes, probe payload flags, real
command promotion, downstream promotion, figure damage, and missing script
snapshots should fail.

## Output

```text
outputs/bem_experiments/533_project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     11
expected pass scenarios:                   1
expected failure scenarios:                10
unexpected scenarios:                      0
command-inventory sensitivity ready:       true
exact source artifacts pass:               true
source-chain damage rejected:              true
command-artifact damage rejected:          true
real-execution promotion rejected:         true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
GPU priority:                              none
```

Scenario outcome:

| Scenario | Expected pass | Actual pass | Failed checks |
| --- | --- | --- | --- |
| exact source artifacts | true | true |  |
| source chain not ready | false | false | source chain ready |
| command count drift | false | false | two hashed contract-check outputs |
| missing command row | false | false | two hashed contract-check outputs |
| probe hash drift | false | false | two hashed contract-check outputs |
| probe payload enables real export | false | false | two hashed contract-check outputs |
| row real values exported | false | false | two hashed contract-check outputs |
| real command promotion | false | false | real FDTD export stays blocked |
| downstream promotion | false | false | real FDTD export stays blocked |
| figure damage | false | false | figure and script snapshots present |
| script snapshot damage | false | false | figure and script snapshots present |

## Decision

Use runs `531-533` as the guarded matched-FDTD contract-check command block.
The next BEM-side implementation step is real FDTD return-value export, not an
accepted BEM/FDTD comparison yet.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validation_sensitivity.py
4 passed
```

Figure check:

```text
2645x837, dynamic range=255
```
