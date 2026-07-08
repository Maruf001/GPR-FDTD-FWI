# Field Experiment 612: External Return Directory Scaffold Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `611` validator by damaging the saved run `610` directory
scaffold state in controlled ways.

The sensitivity set checks source-readiness damage, row-count damage,
directory-count damage, directory-presence damage, slot-count damage,
collection-coupled requirement damage, file-count promotion, created-file
promotion, live-file promotion, accepted-group promotion, field-evidence
promotion, field-FWI promotion, field-3D promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/612_gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_directory_scaffold_validation_sensitivity
```

## Result

```text
scenarios:                         16
expected passes:                    1
expected failures:                 15
observed passes:                    1
observed failures:                 15
unexpected outcomes:                0
damaged scenarios:                 15
damaged scenarios rejected:        15
controlled field evidence ready: false
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

The exact directory-only, no-file scaffold state passes. All damaged states
fail.

## Interpretation

The validator accepts only the exact directory-only state and rejects false
promotion to live files, field evidence, field FWI, or field 3D/HPC.

## Decision

Use runs `610-612` as the guarded external field-return directory scaffold
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_external_return_directory_scaffold.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_external_return_directory_scaffold_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_external_return_directory_scaffold_validation_sensitivity.py
9 passed
```

Figure check:

```text
3005x853, dynamic range=255
```
