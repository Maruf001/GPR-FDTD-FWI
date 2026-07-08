# Field Experiment 518: Return-Packet Live Delta Closure Sequence

Date: 2026-06-30

## Purpose

Convert the empty live return-packet state from run `515` into an operational
collection closure sequence.

The earlier live monitor showed that all 33 required files are still missing.
This run answers the next practical question: which grouped actions close that
gap without pretending that parser, provenance, archive, field FWI, or field
3D/HPC work is ready?

This is CPU-only file and metadata planning. It does not parse DZT files, run
provenance promotion, run field FWI, launch GPU/HPC work, or create measured
field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/518_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_action_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source monitor ready:                      true
sequence files:                            33
sequence actions:                          5
file-producing closure actions:            4
final gate actions:                        1
pre-collection files:                      15
measurement-dependent files:               18
DZT files required:                        9
metadata files required:                   24
global metadata files:                     15
controlled profile packet files:           6
time-zero packet files:                    6
amplitude-reference packet files:          6
live files present:                        0
missing live files:                        33
complete closure actions:                  0
receipt gate ready:                        false
parser ready:                              false
provenance ready:                          false
archive ready:                             false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The five sequence actions are:

| Order | Action | Required files | DZT | Metadata | Timing |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | global metadata prefill | 15 | 0 | 15 | pre-collection |
| 2 | controlled profile repeats | 6 | 3 | 3 | during collection |
| 3 | time-zero references | 6 | 3 | 3 | during collection |
| 4 | amplitude references | 6 | 3 | 3 | during collection |
| 5 | final receipt gate | 33 | 9 | 24 | post-collection |

## Interpretation

The collection closure is now ordered. Fifteen global metadata files can be
prepared before collection. The remaining eighteen files depend on measured DZT
collection: three controlled profile repeats, three time-zero references, three
amplitude references, and one per-file metadata record for each measured DZT
file.

The final gate is not a new data collection step. It is the rerun point for
receipt, parser, provenance, and archive checks after all 33 live files exist.

## Decision

Use run `518` as the collection closure checklist. Do not run parser,
provenance, archive promotion, field FWI, or field 3D/HPC until the complete
33-file packet is present.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_live_delta_closure_sequence_validator.py

7 passed
```

Figure check:

```text
2572x852, dynamic range=255
```
