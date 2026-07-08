# Field Experiment 222: Controlled Archive Operator Manifest Validator

Date: 2026-06-28

## Purpose

Validate the run `221` operator manifest pack from a consumer perspective.

This run checks whether the manifest tables and summary agree on the file
slots, archive directories, planned intake checks, DZT guard values, and
downstream no-go states.

It does not ingest real field files, execute command templates, accept a real
archive, run field FWI, launch GPU/HPC work, or run field 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/222_gssi51600s_controlled_archive_operator_manifest_validator
```

Key artifacts:

```text
data/field_controlled_archive_operator_manifest_validator_checks.csv
data/field_controlled_archive_operator_manifest_validator_summary.json
figures/field_controlled_archive_operator_manifest_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_MANIFEST_VALIDATOR.md
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
manifest validation ready:          true
source file slots:                  9
source directories:                 3
source planned checks:              27
operator collection ready:          true
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The validator confirms:

| Check | Result |
| --- | --- |
| nine manifest file slots | pass |
| three required files per role | pass |
| three archive directories with three files each | pass |
| 27 planned checks with three checks per file | pass |
| DZT guard values fixed at 65536 bytes and `ff07` header prefix | pass |
| operator collection ready while archive acceptance remains false | pass |
| no real files and no executed checks in this run | pass |
| checksum intake, evidence, field FWI, and field 3D/HPC blocked | pass |

## Interpretation

The operator manifest is internally consistent. Its tables and summary all
agree on nine required DZT files, three archive directories, and 27 planned
intake checks.

The result validates the manifest as a collection and staging artifact only. It
does not promote real archive acceptance or downstream field processing.

## Decision

Use run `222` as the manifest consumer validator. Sensitivity remains required
before treating the validator as guarded against common manifest drift.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_manifest_validator.py
6 passed
```

Compile check:

```text
run_gssi_field_controlled_archive_operator_manifest_validator.py: pass
tests/test_gssi_field_controlled_archive_operator_manifest_validator.py: pass
```

Figure check:

```text
field_controlled_archive_operator_manifest_validator.png
2645x840, dynamic range=255
```
