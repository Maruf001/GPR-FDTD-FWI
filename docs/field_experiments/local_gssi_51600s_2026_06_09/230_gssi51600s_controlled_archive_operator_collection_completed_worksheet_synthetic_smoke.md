# Field Experiment 230: Controlled Archive Operator Collection Completed Worksheet Synthetic Smoke

Date: 2026-06-28

## Purpose

Exercise the completed-worksheet intake mechanics with a fully populated
synthetic worksheet.

Runs `227-229` defined, validated, and stress-tested the signoff contract for
future completed worksheet intake. This run creates a positive synthetic smoke:
the same nine worksheet rows are filled with deterministic synthetic operator
initials, local timestamps, SHA-256 strings, and notes.

It does not contain real measured files, accept an archive, run field FWI,
launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/230_gssi51600s_controlled_archive_operator_collection_completed_worksheet_synthetic_smoke
```

Key artifacts:

```text
data/field_controlled_archive_operator_collection_completed_worksheet_synthetic_rows.csv
data/field_controlled_archive_operator_collection_completed_worksheet_synthetic_signoff_checks.csv
data/field_controlled_archive_operator_collection_completed_worksheet_synthetic_smoke_summary.json
figures/field_controlled_archive_operator_collection_completed_worksheet_synthetic_smoke.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_COLLECTION_COMPLETED_WORKSHEET_SYNTHETIC_SMOKE.md
scripts/run_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_smoke.py
scripts/test_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_smoke.py
```

## Result

```text
completed worksheet rows:              9
signoff check rows:                    36
required signoff checks:               27
required signoff passes:               27
optional signoff checks:               9
optional signoff passes:               9
unique synthetic SHA-256 values:       9
synthetic completed worksheet ready:   true
real files present:                    false
real completed signoff values present: false
real archive acceptance ready:         false
field FWI ready:                       false
field 3D/HPC ready:                    false
```

## Interpretation

The completed-worksheet intake mechanics can consume a fully populated
worksheet shape. All nine rows have synthetic initials, local timestamps,
unique 64-character SHA-256 values, and optional notes.

The synthetic row state is explicitly separated from real measured files. This
run proves the intake mechanics can handle completed signoff fields, but it
does not prove field evidence, checksum intake on real files, archive
acceptance, field FWI readiness, or field 3D/HPC readiness.

## Decision

Use run `230` as the positive synthetic smoke for completed-worksheet intake
mechanics. Real measured files, real completed signoff values, archive
acceptance, checksum intake, controlled evidence, field FWI, and field 3D/HPC
remain blocked.

Validator and sensitivity coverage remain required before treating the
synthetic completed-worksheet intake path as fully guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_collection_completed_worksheet_synthetic_smoke.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_operator_collection_completed_worksheet_synthetic_smoke.png
2536x843, dynamic range=255
```
