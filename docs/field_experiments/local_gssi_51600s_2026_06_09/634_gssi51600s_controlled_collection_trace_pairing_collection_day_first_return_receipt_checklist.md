# Field Experiment 634: First-Return Receipt Checklist

Date: 2026-07-01

## Purpose

Convert the guarded first-return operator packet from runs `631-633` into a
fillable receipt checklist.

The checklist has one row for each pending live-return file. It is designed to
capture file arrival, file size, SHA-256 checksum, operator signoff, DZT
signature checks, and metadata-schema checks after collection-day files are
placed.

This is a CPU-only checklist run. It does not create measured DZT files,
populate metadata JSON files, accept field evidence, launch field FWI, or start
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/634_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_receipt_checklist
```

## Result

```text
source operator packet ready:          true
source validation ready:               true
source sensitivity ready:              true
receipt rows:                          18
unique pairs:                          9
DZT receipt rows:                      9
metadata receipt rows:                 9
pending receipt rows:                  18
blank operator initials:               18
blank observed SHA-256 values:         18
blank observed file sizes:             18
ready for acceptance recheck:          0
parent directories ready:              18
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The field return path now has an explicit receipt checklist for the 18 pending
files: nine measured DZT files and nine paired metadata JSON files across the
three controlled profile repeats, three time-zero references, and three
amplitude references.

All receipt fields are intentionally blank. This means no field evidence has
been accepted yet. After files are placed and the receipt fields are filled,
the first-return pair acceptance gate must be rerun.

## Decision

Use this as a fillable receipt checklist only. Controlled field evidence, field
FWI, and field 3D/HPC remain blocked until real files and paired metadata pass
the guarded acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_checklist.py
4 passed
```

Figure check:

```text
1780x790, dynamic range=255
```
