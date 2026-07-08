# Field Experiment 589: Controlled Collection Return File-Slot Manifest

Date: 2026-07-01

## Purpose

Convert the run `586` dependency split into a per-file checklist for the
controlled collection return.

Runs `586-588` showed which records can be prepared separately and which records
must be produced during the same controlled field session. This run turns that
dependency map into one row per expected return file.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/589_gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_file_slot_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source dependency audit ready:             true
source validator ready:                    true
source sensitivity ready:                  true
file slots:                                33
stages:                                    6
metadata JSON slots:                       24
measured DZT slots:                        9
metadata preparable before collection:     15
metadata paired with DZT:                  9
measured DZT dependency slots:             9
collection-coupled slots:                  18
preflight-passed slots:                    0
ready slots:                               0
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

## Interpretation

The controlled collection return now has an explicit file-level structure:

| Slot class | Count | Collection implication |
| --- | ---: | --- |
| Metadata JSON preparable before collection | 15 | Can be filled before the field session where values are already known |
| Metadata JSON paired with measured DZT | 9 | Must be completed with the corresponding measured radar file |
| Measured DZT file | 9 | Must be collected during the controlled field session |

The eighteen collection-coupled slots are the three controlled profile repeats,
three time-zero references, three amplitude references, and the nine metadata
records paired with those measured files.

## Decision

Use this manifest as the per-file collection checklist. Keep controlled field
evidence, field FWI, and field 3D/HPC blocked until the measured DZT files and
paired metadata pass preflight together.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest.py

3 passed
```

Figure check:

```text
2824x882, dynamic range=255
```
