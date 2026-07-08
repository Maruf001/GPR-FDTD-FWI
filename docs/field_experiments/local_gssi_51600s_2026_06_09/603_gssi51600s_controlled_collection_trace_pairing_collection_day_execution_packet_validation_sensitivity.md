# Field Experiment 603: Collection-Day Execution Packet Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `602` validator with damaged versions of the run `601`
collection-day execution packet.

Damaged cases include policy-label damage, packet-readiness damage,
source-readiness damage, slot-count damage, template-count damage, measured-DZT
count damage, live-return-count damage, action-shape damage, action-count
damage, live-DZT promotion, live-metadata promotion, row-level live-file
promotion, accepted-action promotion, evidence promotion, field-FWI promotion,
field-3D promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/603_gssi51600s_controlled_collection_trace_pairing_collection_day_execution_packet_validation_sensitivity
```

## Result

```text
scenarios:                    20
expected pass scenarios:       1
expected fail scenarios:      19
observed pass scenarios:       1
observed fail scenarios:      19
unexpected outcomes:           0
damaged scenarios:            19
damaged scenarios rejected:   19
gpu priority:                 none
```

## Interpretation

The validator fails closed. The exact saved collection-day checklist passes,
while all damaged or falsely promoted variants fail.

## Decision

Use runs `601-603` as the guarded collection-day execution packet block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_validation_sensitivity.py
3 passed
```

Figure check:

```text
3617x886, dynamic range=255
```
