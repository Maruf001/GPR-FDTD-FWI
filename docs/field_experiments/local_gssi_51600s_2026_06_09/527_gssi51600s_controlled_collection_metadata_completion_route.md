# Field Experiment 527: Metadata Completion Route

Date: 2026-06-30

## Purpose

Combine the global metadata and per-file metadata fillability audits into one
controlled-collection metadata completion route.

This is an output-local preparation route. It does not create live field
receipt files, parse DZT files, promote controlled field evidence, run field
FWI, launch GPU/HPC work, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/527_gssi51600s_controlled_collection_metadata_completion_route
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_completion_route_route_rows.csv
data/gssi51600s_controlled_collection_metadata_completion_route_summary.json
figures/gssi51600s_controlled_collection_metadata_completion_route.png
scripts/script_snapshot_manifest.json
```

## Result

```text
route rows:                                5
global metadata files:                     15
per-file metadata files:                   9
total metadata files:                      24
record-based global metadata files:        7
collection-day global metadata files:      8
per-file metadata fields:                  36
paired measured-DZT dependencies:          9
metadata values/fields to complete:        51
current metadata values ready:             0
current metadata live files present:       0
current paired DZT live files present:     0
complete routes now:                       0
live receipt ready:                        false
field FWI ready:                           false
field 3D/HPC ready:                        false
metadata completion route ready:           true
```

Route table:

| Route | Timing | Metadata files | DZT dependencies | Values/fields | Complete now |
| --- | --- | ---: | ---: | ---: | --- |
| record-based global metadata | before collection | 7 | 0 | 7 | false |
| collection-day global metadata | setup and collection-day log | 8 | 0 | 8 | false |
| measured DZT dependencies | during collection | 0 | 9 | 0 | false |
| post-measurement per-file metadata | after DZT receipt | 9 | 9 | 36 | false |
| final metadata receipt gate | post collection | 24 | 9 | 51 | false |

## Interpretation

The controlled collection now has a single metadata route. Seven global
metadata files can be prepared from existing records, eight global metadata
files require collection-day verification or logging, and nine per-file
metadata files require paired measured DZT files before their 36 field values
can be completed.

No metadata file or DZT dependency is currently live or ready.

## Decision

Use this route as the metadata completion order. Keep live receipt,
parser/provenance/archive readiness, field FWI, and field 3D/HPC blocked until
real files are returned.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_completion_route.py
tests/test_gssi_field_controlled_collection_metadata_completion_route_validator.py
tests/test_gssi_field_controlled_collection_metadata_completion_route_validation_sensitivity.py
9 passed
```

Figure check:

```text
2644x863, dynamic range=255
```

