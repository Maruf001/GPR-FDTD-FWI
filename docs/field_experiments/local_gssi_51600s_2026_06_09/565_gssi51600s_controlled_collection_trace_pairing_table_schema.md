# Field Experiment 565: Controlled Collection Trace-Pairing Table Schema

Date: 2026-07-01

## Purpose

Define the parser table that will connect controlled profile repeats to their
time-zero references, amplitude references, per-file metadata, and shared
global metadata.

Runs `559-564` define and guard the live receipt path. This run defines the
next table shape without accepting field evidence or parsing measured radar
files.

This is CPU-only schema work. It does not parse DZT files, promote provenance,
accept controlled field evidence, run field FWI, run field 3D/HPC, or launch
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/565_gssi51600s_controlled_collection_trace_pairing_table_schema
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_table_schema_schema_columns.csv
data/gssi51600s_controlled_collection_trace_pairing_table_schema_pairing_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_table_schema_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_table_schema.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                  true
source parser guard ready:            true
trace-pairing rows:                   3
schema columns:                       18
linked measured DZT files:            9
linked per-file metadata records:     9
shared global metadata records:       15
linked live files present:            0
linked live files missing:            18
trace-pairing rows ready:             0
full live receipt files required:     33
full metadata value fields required:  96
field table schema defined:           true
field table filled:                   false
parser ready:                         false
provenance ready:                     false
archive ready:                        false
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

Pairing rows:

| Repeat | Profile DZT | Time-zero DZT | Amplitude DZT | Live files present | Row ready |
| ---: | --- | --- | --- | ---: | --- |
| 1 | controlled_profile_repeat_01.DZT | time_zero_reference_01.DZT | amplitude_reference_01.DZT | 0 | false |
| 2 | controlled_profile_repeat_02.DZT | time_zero_reference_02.DZT | amplitude_reference_02.DZT | 0 | false |
| 3 | controlled_profile_repeat_03.DZT | time_zero_reference_03.DZT | amplitude_reference_03.DZT | 0 | false |

Core table columns include:

```text
profile_dzt_path
profile_metadata_path
time_zero_reference_path
time_zero_metadata_path
amplitude_reference_path
amplitude_metadata_path
target_truth_reference
scan_line_geometry_reference
time_zero_correction_ns
amplitude_scale_reference
trace_count
sample_count
parser_status
```

## Interpretation

The field parser table can now be stated concretely. Each profile repeat must
be paired with its matching time-zero reference and amplitude reference before
the radar trace can be interpreted.

The table is not filled because the measured DZT files and per-file metadata
are absent. This keeps parser, provenance, field evidence, and field FWI
blocked.

## Decision

Use run `565` as the table schema for future field parsing. Keep parser,
provenance/archive promotion, controlled field evidence, field FWI, and field
3D/HPC blocked until the live receipt files arrive and the trace-pairing rows
are filled.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_table_schema.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_table_schema.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_table_schema.py: pass
```

Figure check:

```text
1744x844, dynamic range=255
```
