# Field Experiment 228: Controlled Archive Operator Collection Signoff Validator

Date: 2026-06-28

## Purpose

Validate the run `227` completed-worksheet signoff contract from a consumer
perspective.

It does not contain real measured files, fill real signoff values, accept an
archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/228_gssi51600s_controlled_archive_operator_collection_signoff_validator
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_signoff_validator_checks.csv
data/field_controlled_archive_operator_collection_signoff_validator_summary.json
figures/field_controlled_archive_operator_collection_signoff_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_SIGNOFF_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_operator_collection_signoff_validator.py
scripts/test_gssi_field_controlled_archive_operator_collection_signoff_validator.py
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
completed worksheet signoff validation:     true
source signoff rows:                       36
source required signoff cells:             27
source optional signoff cells:             9
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

The validator checks six requirements:

| Check | Passes |
| --- | ---: |
| source guards and contract ready | 1 |
| signoff cell counts match contract | 1 |
| signoff fields and rules are complete | 1 |
| worksheet rows and roles are complete | 1 |
| current values blank but completed intake ready | 1 |
| real archive and downstream states blocked | 1 |

## Interpretation

The completed-worksheet signoff contract is internally consistent: 36 signoff
cells cover nine worksheet rows, required and optional fields have the expected
validation rules, all current values are blank, and real archive states remain
blocked.

## Decision

Use run `228` as the positive validator for completed worksheet signoff intake.
Sensitivity remains required before treating the signoff contract as fully
guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_signoff_validator.py
7 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_signoff_validator.png
2555x840, dynamic range=255
```
