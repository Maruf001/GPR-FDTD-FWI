# Field Experiment 269: Controlled Collection Real-Return Collection-Day Fill Packet

Date: 2026-06-28

## Purpose

Convert the guarded empty real-return inbox scan into a collection-day fill
packet.

This run does not create placeholder DZT files, ingest real field data, run
field FWI, launch 3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/269_gssi51600s_controlled_collection_real_return_collection_day_fill_packet
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_file_fill_worklist.csv
data/field_controlled_collection_real_return_collection_day_metadata_fill_worklist.csv
data/field_controlled_collection_real_return_collection_day_checksum_worklist.csv
data/field_controlled_collection_real_return_collection_day_acceptance_gates.csv
data/field_controlled_collection_real_return_collection_day_fill_packet_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_collection_day_fill_packet.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_FILL_PACKET.md
scripts/run_gssi_field_controlled_collection_real_return_collection_day_fill_packet.py
scripts/test_gssi_field_controlled_collection_real_return_collection_day_fill_packet.py
scripts/script_snapshot_manifest.json
```

## Result

```text
file fill rows:                    9
metadata fill rows:                32
checksum fill rows:                9
acceptance gates:                  7
real files currently present:      0
real files still required:         9
metadata values currently present: 0
metadata values still required:    32
checksums currently present:       0
checksums still required:          9
fill packet ready:                 true
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The file worklist contains the nine required measured DZT slots:

| Group | Count |
| --- | ---: |
| controlled profile repeats | 3 |
| time-zero references | 3 |
| amplitude references | 3 |

The metadata worklist contains 32 measured values:

| Metadata type | Count |
| --- | ---: |
| global/session and target metadata | 11 |
| per-file metadata values | 21 |

## Interpretation

The field-side next action is now operational rather than abstract: copy nine
measured DZT files into the existing inbox slots, fill 32 measured metadata
values, and record nine checksums. The packet is ready as a worklist, but the
current archive remains empty and cannot pass provenance or archive acceptance.

## Decision

Use run `269` as the collection-day fill packet. Do not promote provenance
acceptance, real archive acceptance, controlled field evidence, field FWI,
field 3D/HPC, or GPU work until the worklist is completed with real measured
files and values.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_fill_packet.py
3 passed
```

Figure validation:

```text
2825x865, dynamic range=255
```
