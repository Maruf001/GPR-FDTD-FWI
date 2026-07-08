# Field Experiment 440: Direct-Intake Metadata JSON Schema Contract

Date: 2026-06-30

## Purpose

Define the required JSON content contract for the 24 missing metadata files in
the controlled field-intake packet.

This run does not create metadata JSON files in the live intake tree. It only
writes schema requirement tables under the field experiment output folder.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/440_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_schema_file_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_schema_field_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source receipt ready:                      true
source validation ready:                   true
source sensitivity ready:                  true
metadata JSON files:                       24
global metadata JSON files:                15
per-file metadata JSON files:              9
schema field requirements:                 129
JSON files present now:                    0
JSON parse-ready now:                      0
schema acceptance-ready now:               0
template/synthetic allowed:                0
remaining metadata blockers:               3
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

Global metadata files require five top-level fields:

```text
metadata_key
value
source
recorded_at_utc
provenance_note
```

Per-file metadata files require those five fields plus:

```text
linked_dzt_filename
```

## Decision

Use this schema contract before writing the 24 metadata JSON files. Parser,
provenance, archive acceptance, controlled field evidence, field FWI, and field
3D/HPC remain blocked until real DZT files and schema-valid real metadata are
present.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
