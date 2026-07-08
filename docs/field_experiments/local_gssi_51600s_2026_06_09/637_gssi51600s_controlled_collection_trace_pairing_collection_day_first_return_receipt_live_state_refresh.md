# Field Experiment 637: First-Return Receipt Live-State Refresh

Date: 2026-07-01

## Purpose

Refresh the live file state for the first-return receipt checklist from run
`634`.

This run scans the expected receipt paths, records whether each file exists
now, and computes hash/size fields only for files that are actually present.
It does not create measured radar files, accept field evidence, run field FWI,
or start 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/637_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh
```

## Result

```text
source receipt checklist ready:        true
source validator ready:                true
source sensitivity ready:              true
receipt rows:                          18
unique measured pairs:                 9
DZT receipt rows:                      9
metadata receipt rows:                 9
live files found:                      0
missing files:                         18
live DZT files:                        0
live metadata files:                   0
observed SHA-256 values:               0
observed file-size values:             0
metadata JSON parseable files:         0
DZT signature candidates:              0
ready for acceptance-gate rerun:       0
accepted field-evidence rows:          0
acceptance-gate rerun required:        false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The receipt structure is ready, but no expected first-return files are present
yet. The current state still contains no measured DZT files, no paired metadata
JSON files, no observed checksums, and no file sizes.

## Decision

Keep controlled field evidence, field FWI, and field 3D/HPC blocked. Rerun the
first-return acceptance gate only after real files appear and preliminary
receipt checks are populated.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh.py
4 passed
```

Figure check:

```text
3077x844, dynamic range=255
```
