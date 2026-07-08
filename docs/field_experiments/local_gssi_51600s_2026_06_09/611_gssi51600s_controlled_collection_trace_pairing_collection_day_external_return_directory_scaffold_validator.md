# Field Experiment 611: External Return Directory Scaffold Validator

Date: 2026-07-01

## Purpose

Validate the saved run `610` external return directory scaffold.

The validator checks that the scaffold is source-backed, the five target
directories exist, the 33 field-return slots are preserved, the 18
collection-coupled live file requirement is unchanged, no live files were
created, and field evidence/downstream states remain blocked.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/611_gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_directory_scaffold_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
directories checked:                     5
directories present after scaffold:      5
total return slots:                     33
required collection-coupled live files: 18
expected live files after scaffold:      0
live collection-coupled files after:     0
files created by scaffold:               0
accepted live-state groups:              0
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                       none
```

## Interpretation

The scaffold validates as directory-only and evidence-blocked.

## Decision

Keep field downstream work blocked until real measured DZT files and paired
metadata files pass intake.

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
2285x863, dynamic range=255
```
