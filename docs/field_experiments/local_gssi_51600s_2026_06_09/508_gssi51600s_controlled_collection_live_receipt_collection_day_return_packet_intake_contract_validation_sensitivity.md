# Field Experiment 508: Return Packet Intake Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `507` validator for the run `506` collection-day
return-packet intake contract.

This run checks that the validator accepts only the exact 33-file contract and
rejects damaged states that change file counts, unlink metadata templates,
promote templates into live receipt, promote parser inputs, or prematurely
enable parser/provenance/archive, field FWI, or field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/508_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validation_sensitivity_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                true
sensitivity cases:                     23
expected pass cases:                   1
expected fail cases:                   22
actual pass cases:                     1
actual fail cases:                     22
unexpected outcomes:                   0
exact source passes:                   true
damaged cases rejected:                true
live-promotion cases rejected:         true
downstream-promotion cases rejected:   true
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

The rejected damage cases cover:

| Group | Examples |
| --- | --- |
| Source readiness | contract readiness and route readiness set false |
| Contract shape | row removal, family removal, DZT count damage, metadata count damage, receipt-check count damage |
| Metadata linkage | template unlinking, output-local count damage, template promoted to live receipt |
| Live receipt | live file present, receipt ready, parser input ready, accepted status |
| Downstream promotion | parser, provenance, archive, field FWI, and field 3D/HPC promoted |
| Artifact integrity | figure damage and missing script snapshots |

## Interpretation

Runs `506`-`508` now form a guarded field return-packet contract block. The
current actionable field requirement is still the same, but now it is captured
as a validated 33-file intake contract:

```text
9 measured DZT files
24 completed metadata JSON files
183 receipt checks
```

The current archive remains blocked for parser/provenance/archive promotion,
field FWI, and field 3D/HPC because no live return files are present.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_intake_contract.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validation_sensitivity.py

9 passed
```

Figure check:

```text
2716x885, dynamic range=255
```
