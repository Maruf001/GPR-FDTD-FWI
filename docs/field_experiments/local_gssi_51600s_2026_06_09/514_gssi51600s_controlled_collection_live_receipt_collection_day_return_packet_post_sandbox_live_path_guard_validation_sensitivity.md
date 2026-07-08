# Field Experiment 514: Return-Packet Post-Sandbox Live-Path Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `513` validator for the return-packet post-sandbox
live-path guard.

The validator should accept only the exact run `512` guard state and reject
damaged states that would blur the boundary between output-local sandbox files
and live measured field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/514_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validation_sensitivity_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:      true
sensitivity cases:           25
expected pass cases:         1
expected fail cases:         24
actual pass cases:           1
actual fail cases:           24
unexpected cases:            0
controlled evidence ready:   false
field FWI ready:             false
field 3D/HPC ready:          false
```

The exact run `512` source passes. All damaged cases fail, including live-file
promotion, sandbox/live path overlap, sandbox-under-live-root promotion,
measured-evidence promotion, template-as-live-receipt promotion, live-receipt
promotion, parser/provenance/archive promotion, field-FWI promotion,
field-3D/HPC promotion, figure damage, and missing script snapshots.

## Interpretation

Run `514` hardens the live-path guard. A field packet is not allowed to become
receipt-ready or analysis-ready through an output-local sandbox result, a path
overlap, or a downstream flag promotion.

## Decision

Use runs `512-514` as the current boundary guard after the positive sandbox
completion smoke. The field side remains blocked on real measured files at the
locked live return paths.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validation_sensitivity.py

9 passed
```

Figure check:

```text
2824x903, dynamic range=255
```
