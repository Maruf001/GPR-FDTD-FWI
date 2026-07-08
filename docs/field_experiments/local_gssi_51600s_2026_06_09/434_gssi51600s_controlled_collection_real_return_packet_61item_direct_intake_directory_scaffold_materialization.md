# Field Experiment 434: Direct Intake Directory Scaffold Materialization

Date: 2026-06-30

## Purpose

Close only the first pre-ingest action from run `431`: create the empty staging
directories required for direct field-return intake.

This run does not create DZT files, metadata JSON files, checksum records,
template substitutions, synthetic substitutions, packet acceptance, field
evidence, field FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/434_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_directory_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_file_state_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source contract ready:                     true
source validation ready:                   true
source sensitivity ready:                  true
pre-ingest rows:                           33
required directories:                      5
directories present after run:             5
directories created now:                   5
measured DZT rows:                         9
global metadata JSON rows:                 15
file metadata JSON rows:                   9
files present after scaffold:              0
SHA-256 records present after scaffold:    0
template/synthetic files created:          0
pre-ingest accepted rows:                  0
remaining pre-ingest blockers:             4
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

Directories created:

| Directory | Slots | DZT slots | JSON slots |
| --- | ---: | ---: | ---: |
| `metadata/files` | 9 | 0 | 9 |
| `metadata/global` | 15 | 0 | 15 |
| `real_return/amplitude_reference` | 3 | 3 | 0 |
| `real_return/controlled_profile_repeat` | 3 | 3 | 0 |
| `real_return/time_zero_reference` | 3 | 3 | 0 |

## Interpretation

The intake location is now ready for real files to be copied in. The field
evidence state has not changed: all 33 required files are still missing, and no
hash, parser, provenance, archive, or evidence acceptance can be claimed.

## Decision

Use this empty scaffold before copying measured DZT files or writing metadata
JSON files. The next field-side action is still real data placement and
metadata completion.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization.py
3 passed
```

Figure check:

```text
2645x846, dynamic range=255
```
