# Field Experiment 512: Return-Packet Post-Sandbox Live-Path Guard

Date: 2026-06-30

## Purpose

Guard the live external-return paths after run `509` completed the
collection-day return-packet contract inside an output-local sandbox.

Run `509` proved that the 33-file receipt mechanics can pass when the packet is
complete. This run checks the boundary condition: the sandbox completion must
not create files at the locked live return paths or promote measured field
evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/512_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_guard_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard.png
scripts/
```

## Result

```text
source sandbox smoke ready:            true
source validator ready:                true
source sensitivity ready:              true
guard rows:                            33
file families:                         5
live paths under return root:          33
live files present now:                0
source original live files present:    0
sandbox files present:                 33
sandbox nonempty files:                33
sandbox/live path overlaps:            0
sandbox files under live return root:  0
synthetic-only files:                  33
measured field evidence files:         0
templates accepted as live receipt:    0
live receipt-ready files:              0
live receipt ready:                    false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
```

## Interpretation

The run `509` sandbox completion stayed output-local. All 33 expected live
return paths are still empty, and none of the sandbox files overlap those live
paths or sit under the live external-return root.

This preserves the distinction between a receipt-mechanics pass and measured
field evidence. The real field packet is still missing the actual measured
return files.

## Decision

Keep live receipt, parser, provenance, archive promotion, field FWI, field
3D/HPC, and GPU work blocked until real measured files are copied into the
locked live return paths and pass the same 33-file contract.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard.py

3 passed
```

Figure check:

```text
2573x848, dynamic range=255
```
