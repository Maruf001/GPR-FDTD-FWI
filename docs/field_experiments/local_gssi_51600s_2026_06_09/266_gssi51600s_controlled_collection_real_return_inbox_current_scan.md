# Field Experiment 266: Controlled Collection Real-Return Inbox Current Scan

Date: 2026-06-28

## Purpose

Scan the guarded empty real-return intake layout from runs `263-265` to
determine whether real measured files, measured metadata, or checksums have
been staged.

This run does not create placeholder DZT files, ingest real data into an
accepted archive, run DZT preprocessing, run field FWI, launch GPU/HPC work, or
promote controlled field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/266_gssi51600s_controlled_collection_real_return_inbox_current_scan
```

Key artifacts:

```text
data/field_controlled_collection_real_return_inbox_file_scan.csv
data/field_controlled_collection_real_return_inbox_metadata_scan.csv
data/field_controlled_collection_real_return_inbox_checksum_scan.csv
data/field_controlled_collection_real_return_inbox_unexpected_files.csv
data/field_controlled_collection_real_return_inbox_current_scan_summary.json
figures/field_controlled_collection_real_return_inbox_current_scan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
required file slots:                9
real files present:                 0
missing real files:                 9
zero-byte placeholders:             0
global metadata rows:               11
file metadata rows:                 21
metadata values present:            0
checksum rows:                      9
checksums present:                  0
unexpected files:                   0
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The guarded return inbox is still empty except for README and template files.
No required DZT files, measured metadata values, or checksums have been staged.
The intake layout is valid as a waiting area, but it cannot pass provenance or
archive acceptance yet.

## Decision

Keep provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, field 3D/HPC, and GPU escalation blocked until nine real DZT files,
measured metadata values, and checksums are staged.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_inbox_current_scan.py
2 passed
```

Figure validation:

```text
2645x880, dynamic range=255
```
