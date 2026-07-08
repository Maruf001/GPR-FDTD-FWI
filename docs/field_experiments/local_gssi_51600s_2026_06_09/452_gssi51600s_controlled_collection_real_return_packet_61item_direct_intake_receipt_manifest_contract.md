# Field Experiment 452: Direct-Intake Receipt Manifest Contract

Date: 2026-06-30

## Purpose

Lock the expected receipt manifest for the controlled field-return packet.

Runs `446-451` defined the combined 33-file acceptance gate and verified that
the staging directories exist while all required files remain missing. This
run records the exact receipt identity for each future file: type, family,
staging path, required extension, required check count, and linked file where
applicable.

This run does not copy measured files, accept parser output, accept
provenance, archive the packet, run field FWI, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/452_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_receipt_manifest_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_directory_manifest_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gate ready:                         true
source filesystem gap ready:               true
source gap validation ready:               true
source gap sensitivity ready:              true
required receipt rows:                     33
unique receipt identities:                 33
DZT receipts:                              9
metadata JSON receipts:                    24
total required file-level checks:          183
required directories:                      5
present directories:                       5
unexpected files:                          0
present files:                             0
accepted files:                            0
receipt actions:                           4
receipt manifest contract ready:           true
GPU priority:                              none
```

## Decision

The field-return packet now has a locked receipt manifest. Future measured DZT
and metadata files must match these receipt identities before parser,
provenance, archive, field FWI, or field 3D/HPC work can be justified.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
