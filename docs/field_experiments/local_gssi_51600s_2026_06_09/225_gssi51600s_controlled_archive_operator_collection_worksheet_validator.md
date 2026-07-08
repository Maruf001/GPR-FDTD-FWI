# Field Experiment 225: Controlled Archive Operator Collection Worksheet Validator

Date: 2026-06-28

## Purpose

Validate the run `224` collection-day worksheet from a consumer perspective.

This run checks whether the worksheet can be safely used as a field-collection
and archive-staging aid without being mistaken for archive acceptance or field
evidence.

This is CPU-only validation. It does not ingest real field files, execute shell
commands, accept an archive, run field FWI, launch GPU/HPC work, or run field
3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/225_gssi51600s_controlled_archive_operator_collection_worksheet_validator
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_worksheet_validator_checks.csv
data/field_controlled_archive_operator_collection_worksheet_validator_summary.json
figures/field_controlled_archive_operator_collection_worksheet_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_WORKSHEET_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_operator_collection_worksheet_validator.py
scripts/test_gssi_field_controlled_archive_operator_collection_worksheet_validator.py
```

## Result

```text
validation checks:                         8
validation passes:                         8
blocking failures:                         0
worksheet validation ready:                true
source worksheet rows:                     9
source collection stages:                  6
source signoff fields:                     4
source planned checks:                     27
operator collection ready:                 true
printable collection sheet ready:          true
real files present:                        false
commands executed:                         false
real archive acceptance ready:             false
checksum intake ready:                     false
controlled evidence ready:                 false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

The eight checks validate:

| Check group | Outcome |
| --- | --- |
| Worksheet row count | 9 rows match the summary |
| File-role counts | 3 controlled profile, 3 time-zero, 3 amplitude rows |
| Stage sequence | 6 collection stages in expected order |
| Signoff fields | all pending rows keep blank operator signoff fields |
| Archive and DZT guards | 3 directories, `.DZT`, `65536` byte minimum, `ff07` header prefix, 27 planned checks |
| Acceptance boundary | worksheet is ready, archive acceptance remains false |
| Execution boundary | no real files and no commands executed |
| Downstream boundary | checksum, evidence, field FWI, and 3D/HPC remain false |

## Interpretation

The collection worksheet is internally consistent. It preserves the nine
pending real-file rows, three role groups, six collection stages, DZT guards,
planned checks, and blank operator signoff fields from run `224`.

The worksheet is ready for collection-day use, but it is not archive
acceptance. Real files are still absent, commands have not been executed, and
field evidence remains blocked.

## Decision

Use run `225` as the worksheet consumer validator. Sensitivity remains required
before treating the worksheet validator as guarded against common worksheet
drift.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_worksheet_validator.py
8 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_worksheet_validator.png
2645x840, dynamic range=255
```
