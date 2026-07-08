# Field Experiment 609: Collection-Day Post-Boundary Live-State Refresh Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `608` validator by damaging the saved run `607`
post-boundary live-state refresh in controlled ways.

The sensitivity set checks source-readiness damage, row-count damage, slot-count
damage, required-count damage, false live-file presence, missing-count damage,
false acceptance, field-evidence promotion, field FWI/3D promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/609_gssi51600s_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh_validation_sensitivity
```

## Result

```text
scenarios:                         13
expected passes:                    1
expected failures:                 12
observed passes:                    1
observed failures:                 12
unexpected outcomes:                0
damaged scenarios:                 12
damaged scenarios rejected:        12
controlled field evidence ready: false
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

The exact live-file-absent state passes. All damaged states fail.

## Interpretation

The validator accepts only the exact field live-file-absent state and rejects
false evidence or downstream promotion.

## Decision

Use runs `607-609` as the guarded field post-boundary live-state refresh block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh_validation_sensitivity.py
8 passed
```

Figure check:

```text
2537x851, dynamic range=255
```
