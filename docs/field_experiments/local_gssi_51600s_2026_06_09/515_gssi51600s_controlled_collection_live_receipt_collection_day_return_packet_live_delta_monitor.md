# Field Experiment 515: Return-Packet Live Delta Monitor

Date: 2026-06-30

## Purpose

Create a collection-day monitor for the locked live return-packet paths after
the post-sandbox live-path guard.

Runs `512-514` proved that the output-local sandbox can complete the receipt
mechanics without creating measured field evidence. This run checks the actual
live paths again and records the current delta: which required files are still
missing before the parser, provenance gate, archive promotion, field FWI, or
field 3D/HPC can be considered.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/515_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_delta_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_family_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor.png
scripts/
```

## Result

```text
expected live files:          33
file families:                5
expected DZT files:           9
expected metadata files:      24
live files present now:       0
missing live files now:       33
complete families:            0
families ready for parser:    0
live receipt ready:           false
parser ready:                 false
provenance ready:             false
archive ready:                false
controlled evidence ready:    false
field FWI ready:              false
field 3D/HPC ready:           false
```

## Interpretation

The return-packet target is now a live delta view rather than only a static
contract. All 33 required files are still missing from the locked live paths:
three controlled profile repeat DZT files, three time-zero reference DZT
files, three amplitude-reference DZT files, fifteen global metadata JSON files,
and nine per-file metadata JSON files.

No file family is complete. The parser and all downstream field analysis remain
blocked.

## Decision

Use this monitor after collection-day file drops. A parser/provenance/archive
run is not justified until all 33 expected live files are present at the locked
paths.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_monitor.py
4 passed
```

Figure check:

```text
2500x852, dynamic range=255
```
