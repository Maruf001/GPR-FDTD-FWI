# Field Experiment 542: Metadata JSON Live Receipt Schema Gate

Date: 2026-07-01

## Purpose

Bind the controlled field packet metadata live-return paths to a JSON receipt
schema gate.

This run does not create or stage metadata JSON files, copy measured DZT files,
run parsers, rerun provenance/archive gates, run field FWI, run field 3D/HPC,
launch GPU work, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/542_gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_metadata_rows.csv
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_group_rows.csv
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_action_rows.csv
data/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate_summary.json
figures/gssi51600s_controlled_collection_metadata_json_live_receipt_schema_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source global metadata template pack ready:  true
source per-file metadata audit ready:        true
source DZT receipt gate ready:               true
metadata JSON slots:                         24
global metadata JSON files:                  15
per-file metadata JSON files:                9
required real value fields:                  96
parent directories present:                  24
.json extension slots:                       24
live metadata files present:                 0
live metadata JSON parseable:                0
live metadata schema passes:                 0
live metadata SHA-256 hashes observed:       0
blank required value fields:                 96
paired per-file DZT signature passes:        0
complete actions:                            0
live receipt ready:                          false
parser ready:                                false
provenance ready:                            false
archive ready:                               false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gate artifact ready:                         true
```

The metadata live-return packet contains:

| Metadata group | Files | Required real value fields | Current schema passes |
| --- | ---: | ---: | ---: |
| Global metadata | 15 | 60 | 0 |
| Per-file metadata | 9 | 36 | 0 |

Global metadata requires real `value`, `units`, `recorded_by`, and
`recorded_at_utc` fields. Per-file metadata requires real
`acquisition_file_sha256`, `trace_count`, `time_zero_pick_ns`, and `notes`
fields after the paired DZT file passes receipt.

## Interpretation

The live metadata destinations and schema expectations are now explicit. The
current live return state still has zero metadata JSON files present, so no
metadata can pass receipt or support provenance/archive acceptance.

## Decision

Use this run as the current metadata JSON live receipt boundary. Keep live
receipt, parser, provenance, archive acceptance, field FWI, field 3D/HPC, GPU
work, and neural-network training blocked until all 24 real metadata JSON files
pass this gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_json_live_receipt_schema_gate.py
3 passed
```

Figure check:

```text
2896x851, dynamic range=255
```
