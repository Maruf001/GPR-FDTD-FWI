# Field Experiment 224: Controlled Archive Operator Collection Worksheet

Date: 2026-06-28

## Purpose

Convert the guarded operator manifest from runs `221-223` into a
collection-day worksheet with explicit operator signoff fields.

This run answers the practical field question:

```text
What should the operator fill out while staging the nine required real DZT files?
```

This is CPU-only worksheet synthesis. It does not contain real measured files,
execute shell commands, accept an archive, run field FWI, launch GPU/HPC work,
or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/224_gssi51600s_controlled_archive_operator_collection_worksheet
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_worksheet_rows.csv
data/field_controlled_archive_operator_collection_stage_rows.csv
data/field_controlled_archive_operator_collection_worksheet_summary.json
figures/field_controlled_archive_operator_collection_worksheet.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_WORKSHEET.md
scripts/run_gssi_field_controlled_archive_operator_collection_worksheet.py
scripts/test_gssi_field_controlled_archive_operator_collection_worksheet.py
```

## Result

```text
source manifest pack ready:              true
source manifest sensitivity ready:       true
worksheet rows:                          9
collection stages:                       6
archive directories:                     3
operator signoff fields:                 4
controlled profile repeat rows:          3
time-zero reference rows:                3
amplitude reference rows:                3
DZT minimum size guard:                  65536 bytes
DZT header prefix guard:                 ff07
planned checks:                          27
operator collection worksheet ready:     true
printable collection sheet ready:        true
real files present:                      false
commands executed:                       false
real archive acceptance ready:           false
checksum intake ready:                   false
controlled evidence ready:               false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The worksheet preserves the same nine required real-file slots:

| File role | Rows | Archive directory |
| --- | ---: | --- |
| Controlled profile repeat | 3 | `raw/profiles` |
| Time-zero reference | 3 | `raw/references/time_zero` |
| Amplitude reference | 3 | `raw/references/amplitude` |

It adds four operator-facing signoff fields to each row:

```text
operator_initials
collection_time_local
sha256_after_stage
notes
```

## Interpretation

The guarded operator manifest is now converted into a worksheet that can be
used during collection and archive staging. The worksheet keeps the required
file count, role grouping, archive-directory layout, DZT guards, and planned
check count intact while adding fields that make collection-day responsibility
explicit.

This still does not create measured field evidence. Every worksheet row is
pending a real file, every command remains unexecuted, and archive acceptance
remains blocked.

## Decision

Use run `224` as the collection-day worksheet companion to the operator
manifest. Real archive acceptance, checksum intake, controlled evidence, field
FWI, GPU work, and field 3D/HPC remain blocked until real files are staged and
the planned checks pass on those files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_worksheet.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_worksheet.png
2464x847, dynamic range=255
```
