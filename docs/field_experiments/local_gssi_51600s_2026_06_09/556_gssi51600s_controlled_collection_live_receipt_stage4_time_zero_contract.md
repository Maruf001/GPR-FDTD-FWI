# Field Experiment 556: Stage-4 Time-Zero Contract

Date: 2026-07-01

## Purpose

Define the exact live receipt contract for controlled-collection stage `4`,
the time-zero references.

This run extends the stage-3 controlled profile contract from run `555`. It
does not create measured field evidence, accept live field files, run DZT
parsing, promote provenance/archive state, launch field FWI, or launch field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/556_gssi51600s_controlled_collection_live_receipt_stage4_time_zero_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_stage4_time_zero_contract_contract_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage4_time_zero_contract_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage4_time_zero_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage-4 receipt items required:        6
time-zero DZT files required:          3
paired metadata files required:        3
metadata value fields required:        12
stage-4 live parents present:          6
stage-4 live files present:            0
stage-4 accepted live receipt items:   0
cumulative receipt items through s4:   23
cumulative metadata fields through s4: 68
full live receipt items required:      33
full metadata value fields required:   96
live receipt ready:                    false
parser ready:                          false
provenance ready:                      false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
```

Expected live stage-4 files:

```text
time_zero_reference_01.DZT
time_zero_reference_02.DZT
time_zero_reference_03.DZT
time_zero_reference_01_metadata.json
time_zero_reference_02_metadata.json
time_zero_reference_03_metadata.json
```

The DZT files must pass the binary receipt guard: `.DZT` extension, minimum
size of `65536` bytes, `ff07` header prefix, and SHA-256 checksum recording.
Each metadata file must carry `value`, `units`, `recorded_by`, and
`recorded_at_utc`.

## Interpretation

The fourth live replacement stage is now exact: three measured time-zero
references and three paired per-file metadata JSON records. These files are
required to tie the controlled profile measurements to an observed time-zero
reference rather than an assumed timing anchor.

No live stage-4 files are present yet.

## Decision

Use this contract as the time-zero reference checklist after the controlled
profile repeat stage. Keep live receipt, parser/provenance, controlled field
evidence, field FWI, and field 3D/HPC blocked until real live files pass the
receipt gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage4_time_zero_contract.py
3 passed
```

Figure check:

```text
1924x844, dynamic range=255
```
