# BEM Experiment 532: Matched FDTD Return Contract-Check Command Inventory Validator

Date: 2026-06-30

## Purpose

Validate run `531` from saved artifacts.

The validator checks that both FDTD contract-check JSON outputs exist, their
hashes match the command table, the required row counts remain 279 per return
file, and real FDTD export remains disabled.

## Output

```text
outputs/bem_experiments/532_project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validator_checks.csv
data/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         4
validation passes:                         4
blocking failures:                         0
command-inventory validation ready:        true
FDTD contract-check commands:              2
FDTD contract-check probe passes:          2
required FDTD return entries:              558
remaining comparison blockers:             2
GPU priority:                              none
```

The validator passed all four checks:

| Check | Pass |
| --- | --- |
| source chain ready | true |
| two hashed contract-check outputs | true |
| real FDTD export stays blocked | true |
| figure and script snapshots present | true |

## Decision

Use run `532` as the artifact validator for the run `531` command inventory.
The matched FDTD return command path is validated, but real FDTD values and the
accepted comparison writer remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_validator.py
3 passed
```

Figure check:

```text
1925x841, dynamic range=255
```
