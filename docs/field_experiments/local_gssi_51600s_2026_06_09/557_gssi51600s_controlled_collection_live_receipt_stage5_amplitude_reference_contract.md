# Field Experiment 557: Stage-5 Amplitude Reference Contract

Date: 2026-07-01

## Purpose

Define the exact live receipt contract for controlled-collection stage `5`,
the amplitude references.

This run extends the stage-4 time-zero contract from run `556`. It does not
create measured field evidence, accept live field files, run DZT parsing,
promote provenance/archive state, launch field FWI, or launch field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/557_gssi51600s_controlled_collection_live_receipt_stage5_amplitude_reference_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_stage5_amplitude_reference_contract_contract_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage5_amplitude_reference_contract_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage5_amplitude_reference_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage-5 receipt items required:        6
amplitude DZT files required:          3
paired metadata files required:        3
metadata value fields required:        12
stage-5 live parents present:          6
stage-5 live files present:            0
stage-5 accepted live receipt items:   0
cumulative receipt items through s5:   29
cumulative metadata fields through s5: 80
full live receipt items required:      33
full metadata value fields required:   96
live receipt ready:                    false
parser ready:                          false
provenance ready:                      false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
```

Expected live stage-5 files:

```text
amplitude_reference_01.DZT
amplitude_reference_02.DZT
amplitude_reference_03.DZT
amplitude_reference_01_metadata.json
amplitude_reference_02_metadata.json
amplitude_reference_03_metadata.json
```

The DZT files must pass the binary receipt guard: `.DZT` extension, minimum
size of `65536` bytes, `ff07` header prefix, and SHA-256 checksum recording.
Each metadata file must carry `value`, `units`, `recorded_by`, and
`recorded_at_utc`.

## Interpretation

The fifth live replacement stage is now exact: three measured amplitude
references and three paired per-file metadata JSON records. These files are
required before the controlled field packet can support amplitude-aware field
evidence.

No live stage-5 files are present yet.

## Decision

Use this contract as the amplitude-reference checklist after the time-zero
reference stage. Keep live receipt, parser/provenance, controlled field
evidence, field FWI, and field 3D/HPC blocked until real live files pass the
receipt gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage5_amplitude_reference_contract.py
3 passed
```

Figure check:

```text
1924x844, dynamic range=255
```
