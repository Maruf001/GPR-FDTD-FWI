# Field Experiment 231: Controlled Archive Operator Collection Completed Worksheet Synthetic Validator

Date: 2026-06-28

## Purpose

Validate the run `230` synthetic completed-worksheet smoke from a consumer
perspective.

Run `230` showed that the worksheet can be filled with synthetic signoff
values and checked mechanically. This run verifies that the populated rows,
signoff checks, synthetic SHA-256 values, and synthetic-vs-real boundary are
internally consistent.

It does not contain real measured files, accept an archive, run field FWI,
launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/231_gssi51600s_controlled_archive_operator_collection_completed_worksheet_synthetic_validator
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_completed_worksheet_synthetic_validator_checks.csv
data/field_controlled_archive_operator_collection_completed_worksheet_synthetic_validator_summary.json
figures/field_controlled_archive_operator_collection_completed_worksheet_synthetic_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_COMPLETED_WORKSHEET_SYNTHETIC_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_validator.py
scripts/test_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_validator.py
```

## Result

```text
validation checks:                    5
validation passes:                    5
blocking failures:                    0
validation ready:                     true
source completed worksheet rows:      9
source signoff check rows:            36
unique synthetic SHA-256 values:      9
real archive acceptance ready:        false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

The validator checks:

| Check | Result |
| --- | --- |
| Source readiness and synthetic smoke are ready | pass |
| Completed rows preserve manifest roles | pass |
| Signoff checks are complete and passing | pass |
| Synthetic values are complete and unique | pass |
| Synthetic/real boundary and downstream states remain blocked | pass |

## Interpretation

The synthetic completed worksheet is internally consistent. It preserves the
nine manifest rows, passes all 36 signoff checks, has nine unique synthetic
SHA-256 values, and keeps the synthetic-vs-real boundary explicit.

This result validates the completed-worksheet intake mechanics, not the field
archive itself. The archive still needs real measured DZT files and real
operator signoff values before acceptance can be tested.

## Decision

Use run `231` as the positive validator for synthetic completed-worksheet
intake. Sensitivity remains required before treating this intake path as fully
guarded.

Real measured files, real completed signoff values, archive acceptance,
checksum intake, controlled evidence, field FWI, and field 3D/HPC remain
blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_validator.py
7 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_completed_worksheet_synthetic_validator.png
2555x840, dynamic range=255
```
