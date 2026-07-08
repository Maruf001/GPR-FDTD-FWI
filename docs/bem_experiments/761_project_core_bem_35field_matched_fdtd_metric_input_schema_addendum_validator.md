# BEM Experiment 761: Metric Input Schema Addendum Validator

Date: 2026-07-01

## Purpose

Validate run `760` from saved outputs.

This run checks that the real numeric addendum schema is internally
consistent: five addendum files are represented, the stage row shape covers all
279 receiver-frequency pairs, the required cell counts are preserved, every
file has the required thirteen columns, and real comparison remains blocked
because the addendum files are not filled.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/761_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source addendum ready:                    true
validation checks:                        7
passed validation checks:                 7
failed validation checks:                 0
addendum files:                           5
addendum required rows:                   279
required fields per row:                  13
required metric cells:                    3627
required complex component cells:         1116
schema addendum filled:                   false
real BEM/FDTD comparison ready:           false
gpu priority:                             none
```

Saved-output validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source addendum ready | pass |
| 2 | five addendum files are represented | pass |
| 3 | stage row shape covers all pairs | pass |
| 4 | required cell counts are preserved | pass |
| 5 | all required columns are present in each addendum file | pass |
| 6 | schema remains unfilled and comparison blocked | pass |
| 7 | figure and script snapshots are present | pass |

## Interpretation

The addendum schema is reproducible from saved artifacts and preserves the
intended full comparison shape.

The validation does not make a real BEM/FDTD agreement claim because the five
addendum files are still absent.

## Decision

Use runs `759-761` as the real numeric schema-definition block. Keep real
comparison, 3D validation, GPU/HPC, field transfer, and field FWI blocked until
the addendum files contain accepted real numeric values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validator.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
