# Field Experiment 559: Six-Stage Live Receipt Contract Ledger

Date: 2026-07-01

## Purpose

Combine the six controlled-collection live receipt stages into one checklist.

This run does not create measured field evidence, accept live field files, run
DZT parsing, promote provenance/archive state, launch field FWI, or launch
field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/559_gssi51600s_controlled_collection_live_receipt_six_stage_contract_ledger
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_six_stage_contract_ledger_stage_rows.csv
data/gssi51600s_controlled_collection_live_receipt_six_stage_contract_ledger_expected_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_six_stage_contract_ledger_summary.json
figures/gssi51600s_controlled_collection_live_receipt_six_stage_contract_ledger.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stages:                          6
expected live files:             33
live files present:              0
live parent directories present: 33
accepted live receipt items:     0
measured DZT files required:     9
metadata files required:         24
metadata value fields required:  96
stage item counts:               7, 4, 6, 6, 6, 4
stage metadata field counts:     28, 16, 12, 12, 12, 16
cumulative item counts:          7, 11, 17, 23, 29, 33
cumulative metadata fields:      28, 44, 56, 68, 80, 96
contract sequence closed:        true
live receipt ready:              false
controlled field evidence ready: false
field FWI ready:                 false
field 3D/HPC ready:              false
```

## Interpretation

The field collection receipt contract is now complete as a six-stage checklist:

| Stage | Contract block | Items | DZT files | Metadata files | Metadata fields | Cumulative items |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | pre-collection records | 7 | 0 | 7 | 28 | 7 |
| 2 | setup measurement controls | 4 | 0 | 4 | 16 | 11 |
| 3 | controlled profile repeats | 6 | 3 | 3 | 12 | 17 |
| 4 | time-zero references | 6 | 3 | 3 | 12 | 23 |
| 5 | amplitude references | 6 | 3 | 3 | 12 | 29 |
| 6 | session closeout | 4 | 0 | 4 | 16 | 33 |

All thirty-three expected live files have parent directories, but none of the
live files is present yet. The sequence is complete as a field collection
receipt checklist and incomplete as measured field evidence.

## Decision

Use this ledger as the complete controlled-collection receipt checklist. Keep
live receipt, parser/provenance, controlled field evidence, field FWI, and
field 3D/HPC blocked until all thirty-three live files pass the receipt gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_six_stage_contract_ledger.py
4 passed
```

Figure check:

```text
2140x846, dynamic range=255
```
