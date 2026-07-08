# Field Experiment 227: Controlled Archive Operator Collection Signoff Contract

Date: 2026-06-28

## Purpose

Define the completed-worksheet signoff fields required before future real
archive intake.

Runs `224-226` created and guarded the collection-day worksheet. This run turns
the blank signoff fields into an explicit intake contract for a future
completed worksheet.

It does not contain real measured files, fill real signoff values, accept an
archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/227_gssi51600s_controlled_archive_operator_collection_signoff_contract
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_signoff_contract_rows.csv
data/field_controlled_archive_operator_collection_signoff_contract_summary.json
figures/field_controlled_archive_operator_collection_signoff_contract.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_SIGNOFF_CONTRACT.md
scripts/run_gssi_field_controlled_archive_operator_collection_signoff_contract.py
scripts/test_gssi_field_controlled_archive_operator_collection_signoff_contract.py
```

## Result

```text
worksheet rows:                            9
signoff contract rows:                     36
required signoff fields per row:           3
optional signoff fields per row:           1
required signoff cells:                    27
optional signoff cells:                    9
blank current values:                      36
completed worksheet signoff contract ready: true
ready for completed worksheet intake:      true
real files present:                        false
completed signoff values present:          false
real archive acceptance ready:             false
checksum intake ready:                     false
controlled evidence ready:                 false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

Required completed-worksheet fields:

| Field | Cells | Rule |
| --- | ---: | --- |
| operator_initials | 9 | nonempty operator initials |
| collection_time_local | 9 | nonempty local collection timestamp |
| sha256_after_stage | 9 | 64-character SHA-256 after file staging |

Optional completed-worksheet field:

| Field | Cells | Rule |
| --- | ---: | --- |
| notes | 9 | optional operator notes |

## Interpretation

The completed-worksheet intake requirements are now explicit. Each of the nine
file rows needs operator initials, a local collection time, and a
64-character SHA-256 value after staging. Notes are optional.

The current worksheet remains blank and pending real files.

## Decision

Use run `227` as the signoff contract for future completed worksheet intake.
Real files, real signoff values, archive acceptance, checksum intake,
controlled evidence, field FWI, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_signoff_contract.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_signoff_contract.png
2500x843, dynamic range=255
```
