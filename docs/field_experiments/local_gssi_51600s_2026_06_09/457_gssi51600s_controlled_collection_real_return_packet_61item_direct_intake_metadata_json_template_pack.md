# Field Experiment 457: Direct-Intake Metadata JSON Template Pack

Date: 2026-06-30

## Purpose

Create fillable metadata JSON templates for the controlled field-intake packet.

Run `456` defines the receipt-check commands for the future measured files.
This run uses the metadata schema from run `440` to create the 24 required JSON
templates in the run output folder only. It does not write to the live staging
tree and does not accept field evidence.

This is CPU-only template generation. It does not create DZT files, copy
measured files, parse real field data, accept provenance, build an archive,
run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/457_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack
```

Key artifacts:

```text
data/metadata_json_templates/
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_manifest_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source schema ready:                       true
source command plan ready:                 true
metadata JSON templates:                   24
global metadata templates:                 15
per-file metadata templates:               9
required schema fields:                    129
template top-level fields:                 129
blank or null fields:                      96
JSON-parse-ready templates:                24
real metadata files:                       0
schema-accepted files:                     0
evidence-ready templates:                  0
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Interpretation

The field metadata burden is now concrete and fillable. The templates contain
the required keys and parse as JSON, but the real recorded values remain blank
or null. They are preparation artifacts only, not field evidence.

The measured DZT files and completed real metadata JSON files are still absent.

## Decision

Use run `457` as the metadata entry template pack for the controlled
collection. Complete the values from real field-session records, copy only
completed real JSON files into the live staging area, then rerun receipt,
parser, provenance, and archive gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack.py
4 passed
```

Figure check:

```text
2178x843, dynamic range=255
```
