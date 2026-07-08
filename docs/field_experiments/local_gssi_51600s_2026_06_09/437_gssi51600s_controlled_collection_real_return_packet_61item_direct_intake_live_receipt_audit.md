# Field Experiment 437: Direct-Intake Live Receipt Audit

Date: 2026-06-30

## Purpose

Scan the live direct-intake scaffold after run `434`.

This run is read-only. It does not copy files, create templates, create
synthetic substitutes, parse DZT files, accept provenance, accept an archive,
run field FWI, or launch 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/437_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_directory_receipt_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_expected_file_receipt_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_unexpected_file_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source scaffold ready:                     true
source validation ready:                   true
source sensitivity ready:                  true
required directories:                      5
live directories present:                  5
expected files:                            33
expected files present:                    0
expected files missing:                    33
live receipt-ready files:                  0
live SHA-256 hashes present:               0
required measured DZT files:               9
live measured DZT files present:           0
required JSON files:                       24
live JSON files present:                   0
unexpected live files:                     0
blank live files:                          0
template/synthetic live files:             0
live receipt complete:                     false
live receipt audit ready:                  true
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

Directory receipt:

| Directory group | Expected slots | Present | Missing |
| --- | ---: | ---: | ---: |
| metadata files | 9 | 0 | 9 |
| global metadata | 15 | 0 | 15 |
| amplitude references | 3 | 0 | 3 |
| controlled profile repeats | 3 | 0 | 3 |
| time-zero references | 3 | 0 | 3 |

## Decision

The intake tree is correctly scaffolded and clean, but it is still empty. The
next field action remains copying the nine measured DZT files and writing the
24 metadata JSON files. Parser, provenance, archive, field FWI, and 3D/HPC
steps remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
