# Field Experiment 614: Post-Directory-Scaffold Live-State Refresh Validator

Date: 2026-07-01

## Purpose

Validate the saved run `613` post-directory-scaffold live-state refresh.

The validator checks source readiness, directory presence, live-state row
shape, field-return slot counts, absent live files, blocked field evidence,
figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/614_gssi51600s_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh_validator
```

## Result

```text
validation checks:                       7
checks passed:                           7
checks failed:                           0
directory parents expected:              5
directory parents present:               5
live-state rows:                         6
total return slots:                     33
measured DZT files required:             9
paired metadata files required:          9
collection-coupled live files required: 18
live collection-coupled files:           0
missing collection-coupled files:       18
accepted live-state groups:              0
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                       none
```

## Interpretation

The post-scaffold refresh validates as directory-present, live-file absent, and
evidence-blocked.

## Decision

Keep field downstream work blocked until measured DZT and paired metadata files
pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh_validation_sensitivity.py
8 passed
```

Figure check:

```text
2429x854, dynamic range=255
```
