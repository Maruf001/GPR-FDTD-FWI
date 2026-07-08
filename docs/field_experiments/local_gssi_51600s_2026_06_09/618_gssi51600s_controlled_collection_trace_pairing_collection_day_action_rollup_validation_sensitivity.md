# Field Experiment 618: Collection-Day Action Rollup Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `617` action-rollup validator by damaging the saved run
`616` action rollup in controlled ways.

The sensitivity set checks false rollup readiness, action-count drift,
accepted-action drift, row-count and label damage, directory-count and
presence damage, slot-count damage, metadata and measured-file count damage,
false live-file promotion, missing-file count damage, field-evidence/FWI/3D
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/618_gssi51600s_controlled_collection_trace_pairing_collection_day_action_rollup_validation_sensitivity
```

## Result

```text
scenarios:                         19
expected passes:                    1
expected failures:                 18
observed passes:                    1
observed failures:                 18
unexpected outcomes:                0
damaged scenarios:                 18
damaged scenarios rejected:        18
live collection-coupled files:      0
controlled field evidence ready:false
field FWI ready:                false
field 3D/HPC ready:             false
gpu priority:                  none
```

## Interpretation

The validator accepts only the exact saved collection-day action rollup and
rejects damaged logistics counts or false field-analysis promotion.

## Decision

Use runs `616-618` as the guarded collection-day action rollup block. The
controlled field stream remains a logistics/collection-readiness track until
measured DZT files and paired metadata pass live intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_action_rollup.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_action_rollup_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_action_rollup_validation_sensitivity.py
6 passed
```

Figure check:

```text
3293x923, dynamic range=255
```
