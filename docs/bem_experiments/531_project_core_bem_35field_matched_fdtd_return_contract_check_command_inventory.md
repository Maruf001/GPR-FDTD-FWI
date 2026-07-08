# BEM Experiment 531: Matched FDTD Return Contract-Check Command Inventory

Date: 2026-06-30

## Purpose

Convert the matched FDTD handoff from run `528` into concrete contract-check
commands for the guarded FDTD return exporter.

This run does not export real FDTD values. It only verifies that the two
required FDTD return-file keys can be checked and that the real export path
remains disabled.

## Output

```text
outputs/bem_experiments/531_project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_command_rows.csv
data/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory_summary.json
data/fdtd_return_contract_check_outputs/fdtd_source_hash_manifest_contract_check.json
data/fdtd_return_contract_check_outputs/fdtd_scattered_norm_values_contract_check.json
figures/project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source handoff ready:                      true
source handoff validation ready:           true
source handoff sensitivity ready:          true
FDTD contract-check commands:              2
FDTD contract-check probe passes:          2
FDTD contract-check outputs:               2
required FDTD return files:                2
required FDTD return entries:              558
required FDTD source-hash rows:            279
required FDTD scattered-norm rows:         279
real FDTD export commands:                 0
executable real FDTD export commands:      0
FDTD values ready:                         false
comparison-ready rows:                     0
remaining comparison blockers:             2
GPU priority:                              none
```

Command inventory:

| File key | Required rows | Probe exit code | Contract ready | Real values exported | Pass |
| --- | ---: | ---: | --- | --- | --- |
| fdtd_source_hash_manifest | 279 | 0 | true | false | true |
| fdtd_scattered_norm_values | 279 | 0 | true | false | true |

## Decision

Use run `531` as the guarded command inventory before any real matched FDTD
return-value exporter is implemented.

The BEM side has 8x20 fine-mesh candidate values, and the FDTD side now has
explicit contract-check commands. The comparison remains blocked until real
matched FDTD values exist and an accepted evidence writer is run.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_contract_check_command_inventory.py
4 passed
```

Figure check:

```text
2465x842, dynamic range=255
```
