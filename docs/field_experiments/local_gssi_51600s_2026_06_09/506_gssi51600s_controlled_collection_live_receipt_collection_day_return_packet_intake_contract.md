# Field Experiment 506: Collection-Day Return Packet Intake Contract

Date: 2026-06-30

## Purpose

Join the validated field route specification and metadata-template bundle into
one collection-day return-packet contract.

The field stream already established three facts:

1. The live collection route requires 33 files.
2. The metadata templates are prepared output-locally, not live receipt files.
3. The live external return paths are still empty.

This run converts those facts into one intake table for the real return packet:
nine measured DZT files and twenty-four completed metadata JSON files.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/506_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_contract_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_family_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract.png
scripts/
```

## Result

```text
return-packet contract files:        33
DZT files required:                  9
metadata JSON files required:        24
controlled profile repeats:          3
time-zero references:                3
amplitude references:                3
global metadata files:               15
per-file metadata files:             9
pre-collection metadata files:       15
post-measurement metadata files:     9
metadata templates linked:           24
metadata templates unlinked:         0
template files written locally:      24
templates accepted as live receipt:  0
required receipt checks:             183
current live files present:          0
current live receipt-ready files:    0
parser input-ready files:            0
all files required before parser:    true
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

Family-level contract:

| File family | Files | Receipt checks | Linked templates | Live files present | Receipt ready |
| --- | ---: | ---: | ---: | ---: | ---: |
| controlled profile repeat | 3 | 18 | 0 | 0 | 0 |
| time-zero reference | 3 | 18 | 0 | 0 | 0 |
| amplitude reference | 3 | 18 | 0 | 0 | 0 |
| global metadata | 15 | 75 | 15 | 0 | 0 |
| per-file metadata | 9 | 54 | 9 | 0 | 0 |

## Interpretation

The field return requirement is now a single 33-file contract. The prepared
metadata templates are useful collection-day preparation files, but they do not
count as live receipt. The parser, provenance gate, archive promotion, field
FWI, and field 3D/HPC remain blocked until all 33 live files exist and pass
receipt.

The practical collection-day checklist is:

```text
3 controlled profile repeat DZT files
3 time-zero reference DZT files
3 amplitude-reference DZT files
15 completed global metadata JSON files
9 completed per-file metadata JSON files
```

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_intake_contract.py

3 passed
```

Figure check:

```text
2464x878, dynamic range=255
```
