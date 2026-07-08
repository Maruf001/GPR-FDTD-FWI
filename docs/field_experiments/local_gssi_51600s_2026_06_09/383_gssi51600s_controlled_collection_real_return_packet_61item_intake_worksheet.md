# Field Experiment 383: Controlled Collection Real-Return Intake Worksheet

Date: 2026-06-29

## Purpose

Convert the guarded operator handoff manifest from run `377` into a fillable
real-return packet intake worksheet.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/383_gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_worksheet_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_group_summary_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet.png
```

## Result

```text
source ready:                       true
intake worksheet ready:             true
worksheet rows:                     49
group summary rows:                 7
direct real-input rows:             33
generated follow-up rows:           16
blank completion cells:             294
completed intake rows:              0
measured-evidence rows:             0
measured DZT rows:                  9
metadata rows:                      24
checksum rows:                      9
acceptance rows:                    7
packet requirements:                61
duplicate-path requirements:        12
collection-day intake form ready:   true
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

All returned-file cells are intentionally blank. The worksheet is ready to be
filled during packet intake, but it is not measured evidence.

## Decision

Use this worksheet for collection-day packet intake. Do not promote it to
measured field evidence until the returned file path, hash, size, timestamp,
operator initials, and notes are filled from real files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_worksheet.py
3 passed
```

Figure check:

```text
3221x879, dynamic range=255
```
