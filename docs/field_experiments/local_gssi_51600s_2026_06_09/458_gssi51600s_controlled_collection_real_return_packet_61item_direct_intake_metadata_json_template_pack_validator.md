# Field Experiment 458: Direct-Intake Metadata JSON Template Pack Validator

Date: 2026-06-30

## Purpose

Validate the metadata JSON template pack from run `457`.

The validator checks that the template pack is ready, includes 24 parseable JSON
templates with 129 top-level fields, keeps required real values blank or null,
promotes no real packet or field evidence, and includes a nonblank figure plus
frozen scripts.

This run does not copy measured files, accept metadata, accept provenance,
build a field archive, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/458_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:                true
validation checks:                         5
passed checks:                             5
failed checks:                             0
metadata templates:                        24
template top-level fields:                 129
blank or null fields:                      96
real metadata files:                       0
schema-accepted files:                     0
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
validation ready:                          true
```

## Interpretation

The metadata templates are valid preparation files and not field evidence. They
are ready for manual completion from real field-session records.

## Decision

Use runs `457-458` as the guarded metadata-template block. Keep field evidence
blocked until completed real metadata JSON files and measured DZT files are
copied into live staging and the receipt, parser, provenance, and archive gates
are rerun.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_template_pack_validator.py
8 passed
```

Figure check:

```text
2142x843, dynamic range=255
```
