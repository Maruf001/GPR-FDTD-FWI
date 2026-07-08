# Field Experiment 497: Controlled Collection Live Receipt Collection-Day Per-File Metadata Template Pack

Date: 2026-06-30

## Purpose

Create output-local templates for the nine per-file metadata JSON files that
must be completed after the measured DZT files exist.

The templates are planning artifacts only. Each template is paired with an
expected measured DZT filename and explicitly marked as requiring measured DZT.
They are not written to the live external return path and they do not count as
receipt-ready field files.

This is a CPU-only file-template run. It does not create live measured files,
parse DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/497_gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack
```

Key artifacts:

```text
templates/per_file/*.json
data/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_template_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack.png
scripts/
```

## Result

```text
source policy ready:                    true
source validation ready:                true
source sensitivity ready:               true
templates:                               9
per-file metadata templates:             9
paired DZT names:                         9
template files written:                  9
template JSON key count min:            12
template JSON key count max:            12
total required receipt checks:          54
value placeholders:                     36
templates requiring measured DZT:        9
current live files present:              0
current live receipt-ready files:         0
template/live path overlaps:             0
templates accepted as live receipt:       0
live receipt ready:                     false
parser ready:                           false
provenance ready:                       false
archive ready:                          false
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
gpu priority:                           none
template pack ready:                    true
```

Template fields:

```text
template_type
dataset_id
metadata_name
paired_dzt_name
status
acquisition_file_sha256
trace_count
time_zero_pick_ns
notes
source_live_staging_relative_path
requires_measured_dzt
do_not_promote_as_live_receipt
```

## Interpretation

The post-measurement metadata task is now concrete. There are nine metadata
templates, one for each expected measured DZT file. Each template names the DZT
file it belongs to and leaves the measured values blank.

These templates cannot be evidence by themselves. They become useful only after
the measured DZT files exist and the blanks are replaced with real
file-specific values.

## Decision

Use these templates to structure post-measurement per-file metadata. Keep live
receipt, parser, provenance, archive, field FWI, and field 3D/HPC blocked until
completed real files are copied to the live external return path and pass
receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack.py

3 passed
```

Figure validation:

```text
2285x848, dynamic range=255
```
