# Field Experiment 479: Live Receipt Collection-Day Route Spec

Date: 2026-06-30

## Purpose

Convert the validated live field closure block into a collection-day route
specification.

Runs `476-478` prove that no live field files have been created or accepted.
This run records the exact file-production phases, file counts, and receipt
checks required before the packet can move from collection staging to parser,
provenance, archive, field FWI, or field 3D/HPC work.

This run does not copy field files, accept receipts, run the parser, accept
provenance, build an archive, run field FWI, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/479_gssi51600s_controlled_collection_live_receipt_collection_day_route_spec
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_route_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_phase_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec.png
scripts/
```

## Result

```text
source guard ready:                  true
source validation ready:             true
source sensitivity ready:            true
routes:                              33
phases:                              6
DZT routes:                          9
metadata JSON routes:                24
controlled profile routes:           3
time-zero reference routes:          3
amplitude-reference routes:          3
global metadata routes:              15
per-file metadata routes:            9
total required receipt checks:       183
current present files:               0
current receipt-ready files:         0
ready phases:                        0
parser ready:                        false
provenance ready:                    false
archive ready:                       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

The six route phases are:

| Phase | Name | Required files | Receipt checks |
| ---: | --- | ---: | ---: |
| 1 | copy measured controlled profile repeat DZT files | 3 | 18 |
| 2 | copy measured time-zero reference DZT files | 3 | 18 |
| 3 | copy measured amplitude-reference DZT files | 3 | 18 |
| 4 | copy completed global session metadata JSON files | 15 | 75 |
| 5 | copy completed per-file metadata JSON files | 9 | 54 |
| 6 | rerun receipt, parser, provenance, and archive gates | 33 | 183 |

## Interpretation

The collection-day task is explicit. The field packet needs nine measured DZT
files and 24 completed metadata JSON files, then the receipt, parser,
provenance, and archive gates must be rerun. No current live files are present
or accepted.

## Decision

Use run `479` as the current field collection-day route specification. Keep
field FWI, GPU work, and field 3D/HPC blocked until all 33 files pass receipt
and downstream acceptance gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_spec.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
