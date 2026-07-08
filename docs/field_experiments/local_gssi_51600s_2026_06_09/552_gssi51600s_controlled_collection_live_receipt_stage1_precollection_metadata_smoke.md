# Field Experiment 552: Stage-1 Pre-Collection Metadata Smoke

Date: 2026-07-01

## Purpose

Exercise stage 1 of the staged collection packet from run `551` with an
output-local synthetic metadata fill.

This run does not create live field evidence, accept live receipt, parse field
data, accept provenance, promote an archive, run field FWI, or run field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/552_gssi51600s_controlled_collection_live_receipt_stage1_precollection_metadata_smoke
```

Key artifacts:

```text
data/stage_one_precollection_metadata_sandbox/
data/gssi51600s_controlled_collection_live_receipt_stage1_precollection_metadata_smoke_metadata_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage1_precollection_metadata_smoke_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage1_precollection_metadata_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage-1 metadata JSON files:       7
stage-1 metadata schema passes:    7
stage-1 required value fields:     28
stage-1 blank required values:     0
full live receipt items:           33
full metadata value fields:        96
stage-1 share of receipt items:    0.212121
stage-1 share of metadata fields:  0.291667
accepted live receipt items:       0
live files present:                0
live receipt ready:                false
parser ready:                      false
provenance ready:                  false
archive ready:                     false
field FWI ready:                   false
field 3D/HPC ready:                false
```

## Interpretation

The first field collection stage can be filled and checked locally: seven
pre-collection metadata files and twenty-eight required values pass the
output-local schema check.

This is only mechanics coverage. It does not satisfy live receipt because it
does not include live external files, measured DZT files, setup metadata,
per-file metadata, or session-closeout metadata.

## Decision

Use this as stage-1 metadata mechanics coverage only. Keep live receipt,
parser, provenance, archive promotion, field FWI, and field 3D/HPC blocked
until real live files pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage1_precollection_metadata_smoke.py
3 passed
```

Figure check:

```text
1924x808, dynamic range=255
```
