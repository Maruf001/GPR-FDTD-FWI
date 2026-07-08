# Field Experiment 615: Post-Directory-Scaffold Live-State Refresh Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `614` validator by damaging the saved run `613`
post-directory-scaffold live-state refresh in controlled ways.

The sensitivity set checks source-readiness damage, directory-count damage,
directory-presence damage, row-count damage, slot-count damage,
collection-coupled requirement damage, live-file promotion, missing-count
damage, acceptance promotion, field-evidence promotion, field-FWI promotion,
field-3D promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/615_gssi51600s_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh_validation_sensitivity
```

## Result

```text
scenarios:                         15
expected passes:                    1
expected failures:                 14
observed passes:                    1
observed failures:                 14
unexpected outcomes:                0
damaged scenarios:                 14
damaged scenarios rejected:        14
controlled field evidence ready: false
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

The exact directory-present, live-file-absent state passes. All damaged states
fail.

## Interpretation

The validator accepts only the exact post-scaffold live-state refresh and
rejects false live-file, field-evidence, field-FWI, or field-3D promotion.

## Decision

Use runs `613-615` as the guarded post-directory-scaffold field live-state
refresh block.

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
2861x851, dynamic range=255
```
