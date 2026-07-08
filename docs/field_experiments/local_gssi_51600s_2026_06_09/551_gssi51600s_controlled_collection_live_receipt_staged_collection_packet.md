# Field Experiment 551: Live Receipt Staged Collection Packet

Date: 2026-07-01

## Purpose

Convert the integrated live-receipt frontier from run `545` and the synthetic
mechanics check from run `548` into a collection-day staged packet.

This run does not parse field data, accept live receipt, accept provenance,
promote an archive, run field FWI, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/551_gssi51600s_controlled_collection_live_receipt_staged_collection_packet
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_staged_collection_packet_item_rows.csv
data/gssi51600s_controlled_collection_live_receipt_staged_collection_packet_stage_rows.csv
data/staged_live_receipt_packet/
docs/FIELD_LIVE_RECEIPT_STAGED_PACKET.md
figures/gssi51600s_controlled_collection_live_receipt_staged_collection_packet.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stages:                              6
live receipt items:                  33
global metadata JSON files:          15
measured DZT files:                  9
per-file metadata JSON files:        9
required metadata value fields:      96
parent directories present:          33
live files present:                  0
accepted live receipt items:         0
pre-collection/setup items:          11
pre-collection/setup metadata fields:44
measurement-family items:            18
measurement-family metadata fields:  36
session-closeout items:              4
final cumulative receipt items:      33
final cumulative metadata fields:    96
live receipt ready:                  false
parser ready:                        false
provenance ready:                    false
archive ready:                       false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

Collection stages:

| Stage | Stage | Items | Metadata fields | Cumulative items |
| ---: | --- | ---: | ---: | ---: |
| 1 | pre-collection records | 7 | 28 | 7 |
| 2 | setup measurement controls | 4 | 16 | 11 |
| 3 | controlled profile repeats | 6 | 12 | 17 |
| 4 | time-zero references | 6 | 12 | 23 |
| 5 | amplitude references | 6 | 12 | 29 |
| 6 | session log closeout | 4 | 16 | 33 |

## Interpretation

The live field receipt blocker is now ordered as a collection-day sequence. The
first two stages cover eleven metadata items that can be prepared before or at
setup. The three measurement-family stages each require three measured `.DZT`
files and three paired metadata JSON files. The final stage closes the session
log metadata.

The packet creates stage-only and cumulative CSVs for each stage. It does not
accept any live files; it only organizes the real files and metadata required
by the existing live receipt gate.

## Decision

Use this packet as the controlled field collection return order. Keep live
receipt, parser, provenance, archive promotion, field FWI, and field 3D/HPC
blocked until all thirty-three live receipt items pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_staged_collection_packet.py
4 passed
```

Figure check:

```text
2536x883, dynamic range=255
```
