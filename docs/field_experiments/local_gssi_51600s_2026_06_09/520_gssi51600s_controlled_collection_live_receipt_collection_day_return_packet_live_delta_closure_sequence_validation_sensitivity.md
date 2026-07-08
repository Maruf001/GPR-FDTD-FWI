# Field Experiment 520: Return-Packet Live Delta Closure Sequence Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `519` validator.

The sensitivity set keeps one exact source case and applies controlled damage
to source readiness, file count, action count, pre-collection accounting,
measurement-dependent accounting, DZT count, metadata count, group counts, fake
live-file arrival, fake complete action status, receipt readiness, parser
readiness, field FWI readiness, downstream readiness, figure validation, and
script snapshots.

This run does not create live field files or promote field processing.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/520_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                    true
sensitivity cases:                         18
expected pass cases:                       1
expected fail cases:                       17
actual pass cases:                         1
actual fail cases:                         17
unexpected cases:                          0
damaged cases:                             17
receipt gate ready:                        false
parser ready:                              false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Interpretation

The validator accepts only the exact current closure sequence and rejects count
drift, fake live-file arrival, fake action completion, and premature downstream
promotion.

## Decision

Treat runs `518-520` as the current guarded collection closure sequence. The
next field-processing action remains blocked until the complete 33-file live
packet exists.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_validation_sensitivity.py

10 passed
```

Figure check:

```text
2609x853, dynamic range=255
```
