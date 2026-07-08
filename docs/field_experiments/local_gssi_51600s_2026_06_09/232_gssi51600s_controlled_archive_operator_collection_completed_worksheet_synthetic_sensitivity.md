# Field Experiment 232: Controlled Archive Operator Collection Completed Worksheet Synthetic Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `231` synthetic completed-worksheet validator.

Run `231` validated the positive synthetic completed-worksheet smoke. This run
checks whether that validator fails closed when source readiness, row coverage,
signoff-check coverage, signoff field names, synthetic values, SHA-256
uniqueness, or downstream readiness states are damaged.

It does not contain real measured files, accept an archive, run field FWI,
launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/232_gssi51600s_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity_scenarios.csv
data/field_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity_summary.json
figures/field_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_COMPLETED_WORKSHEET_SYNTHETIC_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity.py
scripts/test_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity.py
```

## Result

```text
scenarios:                         36
expected pass scenarios:           1
expected failure scenarios:        35
observed pass scenarios:           1
observed failure scenarios:        35
unexpected outcomes:               0
sensitivity ready:                 true
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The exact run `230` synthetic smoke passes. All 35 damaged scenarios fail as
expected, including source-readiness drift, row-coverage drift, signoff-check
coverage drift, signoff-field drift, SHA-256 drift, synthetic/real boundary
drift, and false archive/checksum/evidence/FWI/3D promotion.

## Interpretation

The synthetic completed-worksheet validator accepts the exact smoke and rejects
controlled damage to the fields that matter for future intake. A signoff field
name drift case is included, so the validator now guards the exact expected
field vocabulary as well as counts and pass flags.

## Decision

Use runs `230-232` as the guarded synthetic completed-worksheet intake package.
Real files, real operator signoff values, archive acceptance, checksum intake,
controlled evidence, field FWI, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity.py
6 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_completed_worksheet_synthetic_sensitivity.png
3581x886, dynamic range=255
```
