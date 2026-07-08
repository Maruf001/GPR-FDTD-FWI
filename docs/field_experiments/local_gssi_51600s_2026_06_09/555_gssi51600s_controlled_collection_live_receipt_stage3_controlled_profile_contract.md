# Field Experiment 555: Stage-3 Controlled Profile Contract

Date: 2026-07-01

## Purpose

Define the exact live receipt contract for controlled-collection stage `3`,
the controlled profile repeats.

This run extends the stage-2 setup metadata contract from run `554`. It does
not create measured field evidence, accept live field files, run DZT parsing,
promote provenance/archive state, launch field FWI, or launch field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/555_gssi51600s_controlled_collection_live_receipt_stage3_controlled_profile_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_stage3_controlled_profile_contract_contract_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage3_controlled_profile_contract_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage3_controlled_profile_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage-3 receipt items required:         6
controlled profile DZT files required: 3
paired metadata files required:        3
metadata value fields required:        12
stage-3 live parents present:          6
stage-3 live files present:            0
stage-3 accepted live receipt items:   0
cumulative receipt items through s3:   17
cumulative metadata fields through s3: 56
full live receipt items required:      33
full metadata value fields required:   96
live receipt ready:                    false
parser ready:                          false
provenance ready:                      false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
```

Expected live stage-3 files:

```text
controlled_profile_repeat_01.DZT
controlled_profile_repeat_02.DZT
controlled_profile_repeat_03.DZT
controlled_profile_repeat_01_metadata.json
controlled_profile_repeat_02_metadata.json
controlled_profile_repeat_03_metadata.json
```

The DZT files must pass the binary receipt guard: `.DZT` extension, minimum
size of `65536` bytes, `ff07` header prefix, and SHA-256 checksum recording.
Each metadata file must carry `value`, `units`, `recorded_by`, and
`recorded_at_utc`.

## Interpretation

The third live replacement stage is now exact: three measured controlled
profile repeats and three paired per-file metadata JSON records. This is the
first controlled-collection stage that requires measured radar files, not just
global setup metadata.

No live stage-3 files are present yet.

## Decision

Use this contract as the controlled profile repeat checklist after the
pre-collection and setup metadata files. Keep live receipt, parser/provenance,
controlled field evidence, field FWI, and field 3D/HPC blocked until real live
files pass the receipt gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage3_controlled_profile_contract.py
3 passed
```

Figure check:

```text
1924x844, dynamic range=255
```
