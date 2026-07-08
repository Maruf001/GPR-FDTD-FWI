# Field Experiment 543: Metadata JSON Live Receipt Schema Gate Validator

Date: 2026-07-01

## Purpose

Validate run `542` as a fail-closed live metadata JSON receipt boundary.

This run is validation only. It does not stage metadata files, stage DZT files,
run parsers, rerun provenance/archive gates, run field FWI, run field 3D/HPC,
launch GPU work, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/543_gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validator_check_rows.csv
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validator_summary.json
figures/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                         8
passed checks:                  8
failed checks:                  0
metadata JSON slots:            24
global metadata JSON files:     15
per-file metadata JSON files:   9
required real value fields:     96
live metadata files present:    0
live metadata schema passes:    0
blank required value fields:    96
paired DZT signature passes:    0
live receipt ready:             false
field FWI ready:                false
field 3D/HPC ready:             false
validation ready:               true
```

Validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source metadata schema gate ready | pass |
| 2 | metadata schema gate shape | pass |
| 3 | JSON guard contract | pass |
| 4 | live metadata files absent | pass |
| 5 | values and DZT dependencies blocked | pass |
| 6 | metadata groups blocked | pass |
| 7 | downstream remains blocked | pass |
| 8 | figure and scripts exist | pass |

## Interpretation

The validator confirms that run `542` is a receipt contract, not a metadata
promotion. It verifies the 24-file shape, 96 required real value fields, empty
live-file state, zero paired DZT receipt passes, and blocked downstream states.

## Decision

Keep run `542` as the current metadata JSON receipt gate. Do not promote live
receipt or downstream field work until real metadata JSON files and paired real
DZT files pass the required gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_json_live_receipt_schema_gate_validator.py
3 passed
```

Figure check:

```text
2393x856, dynamic range=255
```
