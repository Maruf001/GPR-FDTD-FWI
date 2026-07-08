# Field Experiment 498: Controlled Collection Live Receipt Collection-Day Per-File Metadata Template-Pack Validator

Date: 2026-06-30

## Purpose

Validate the run `497` per-file metadata template pack from generated
artifacts.

The validator checks that all nine per-file metadata templates exist, each
template is paired with one expected measured DZT filename, each template keeps
the measured-value placeholders, and the templates remain output-local planning
artifacts rather than live receipt files.

This is a CPU-only artifact validation. It does not create live measured files,
parse DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/498_gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validator.png
scripts/
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
templates:                           9
template files written:              9
paired DZT templates:                 9
total required receipt checks:       54
value placeholders:                  36
templates requiring measured DZT:     9
current live files present:           0
current live receipt-ready files:      0
template/live path overlaps:          0
templates accepted as live receipt:    0
live receipt ready:                 false
parser ready:                       false
provenance ready:                   false
archive ready:                      false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
validation ready:                   true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source template pack ready | pass |
| 2 | template table matches per-file route | pass |
| 3 | template payloads require measured DZT | pass |
| 4 | templates remain output-local and non-receipt | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The per-file metadata templates validate as post-measurement preparation
artifacts. They are useful because each expected measured DZT file now has a
specific metadata form waiting for real values. They are not evidence files and
they cannot close live receipt without the measured DZT files.

## Decision

Use this validator as the artifact guard for run `497`. Keep live receipt,
parser, provenance, archive, field FWI, and field 3D/HPC blocked until the real
measured DZT files and completed metadata files are copied to the live external
return path and pass receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validator.py

6 passed
```

Figure validation:

```text
2285x840, dynamic range=255
```
