# Field Experiment 517: Return-Packet Live Delta Monitor Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `516` validator for the live delta monitor.

The validator should accept only the exact run `515` monitor and reject damaged
states that change file counts, family counts, live-file presence, readiness
flags, figure validation, or frozen script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/517_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_validation_sensitivity_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:       true
sensitivity cases:            22
expected pass cases:          1
expected fail cases:          21
actual pass cases:            1
actual fail cases:            21
unexpected cases:             0
damaged cases rejected:       true
live receipt ready:           false
parser ready:                 false
field FWI ready:              false
field 3D/HPC ready:           false
```

The exact run `515` source passes. All damaged cases fail, including source
readiness damage, row-count damage, family-count damage, DZT-count damage,
metadata-count damage, live-file promotion, missing-count reduction,
family-complete promotion, parser/provenance/archive promotion, controlled
field-evidence promotion, field-FWI promotion, field-3D/HPC promotion,
downstream flag promotion, figure damage, and missing script snapshots.

## Interpretation

Run `517` hardens the live delta monitor. The field side cannot be accidentally
promoted by count drift, partial file presence, a readiness flag, or an artifact
failure.

## Decision

Use runs `515-517` as the current live collection-day readiness checkpoint.
The field stream remains blocked on the real 33-file return packet.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_validation_sensitivity.py

10 passed
```

Figure check:

```text
2572x868, dynamic range=255
```
