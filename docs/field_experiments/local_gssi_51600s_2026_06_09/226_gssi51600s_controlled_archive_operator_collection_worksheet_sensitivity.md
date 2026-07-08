# Field Experiment 226: Controlled Archive Operator Collection Worksheet Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `225` collection worksheet validator against controlled
damage cases.

This run checks whether the validator accepts only the exact worksheet and
rejects common worksheet corruption, premature completion, premature archive
acceptance, and downstream promotion.

This is CPU-only sensitivity validation. It does not ingest real field files,
execute shell commands, accept an archive, run field FWI, launch GPU/HPC work,
or run field 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/226_gssi51600s_controlled_archive_operator_collection_worksheet_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_worksheet_sensitivity_scenarios.csv
data/field_controlled_archive_operator_collection_worksheet_sensitivity_summary.json
figures/field_controlled_archive_operator_collection_worksheet_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_WORKSHEET_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_operator_collection_worksheet_sensitivity.py
scripts/test_gssi_field_controlled_archive_operator_collection_worksheet_sensitivity.py
```

## Result

```text
scenarios:                                  28
expected pass scenarios:                    1
expected failure scenarios:                 27
observed pass scenarios:                    1
observed failure scenarios:                 27
unexpected outcomes:                        0
worksheet sensitivity ready:                true
operator collection ready:                  true
printable collection sheet ready:           true
real archive acceptance ready:              false
checksum intake ready:                      false
controlled evidence ready:                  false
field FWI ready:                            false
field 3D/HPC ready:                         false
gpu priority:                               none
```

The exact worksheet passes. The 27 damaged variants fail as expected:

| Damage family | Examples |
| --- | --- |
| Row and role drift | row-count drift, missing worksheet row, role-count drift |
| Stage drift | stage-count drift, missing stage, wrong stage name |
| Signoff drift | signoff-field count drift, filled initials, row marked complete |
| Archive and DZT guard drift | wrong directory count, wrong role-directory assignment, wrong extension, DZT size/header drift, planned-check drift |
| Readiness drift | worksheet not ready, printable sheet not ready, row not ready |
| Premature execution or acceptance | real files present, commands executed, real archive acceptance ready |
| Downstream promotion | checksum intake, controlled evidence, field FWI, and field 3D/HPC marked ready |

## Interpretation

The worksheet validator now catches the important worksheet failure modes. One
guard gap was found during generation: changing a row to the wrong archive
directory was not detected when the overall directory set remained unchanged.
The validator was tightened to require the correct directory for each file
role, and the corrected sensitivity run has zero unexpected outcomes.

The worksheet package is guarded for collection-day use, but it remains an
operator worksheet, not real archive acceptance.

## Decision

Use runs `224-226` as the guarded field operator worksheet package for
collection-day execution. Real archive acceptance, checksum intake, controlled
evidence, field FWI, GPU work, and field 3D/HPC remain blocked until real
measured files pass the staged checks.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_worksheet_validator.py
tests/test_gssi_field_controlled_archive_operator_collection_worksheet_sensitivity.py
16 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_worksheet_sensitivity.png
3437x893, dynamic range=255
```
