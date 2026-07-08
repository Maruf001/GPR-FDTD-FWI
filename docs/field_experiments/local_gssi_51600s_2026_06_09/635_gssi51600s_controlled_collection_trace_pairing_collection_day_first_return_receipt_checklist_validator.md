# Field Experiment 635: First-Return Receipt Checklist Validator

Date: 2026-07-01

## Purpose

Validate the first-return receipt checklist from run `634`.

This run checks that the checklist is a blank, pending collection-day receipt
artifact with stable row counts, correct DZT/metadata check requirements, and
blocked downstream field-evidence states.

This is a CPU-only validator run. It does not create measured DZT files,
populate metadata JSON files, accept field evidence, launch field FWI, or start
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/635_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_receipt_checklist_validator
```

## Result

```text
validation checks:                     6
passed checks:                         6
failed checks:                         0
receipt rows:                          18
unique pairs:                          9
pending receipt rows:                  18
blank operator initials:               18
blank observed SHA-256 values:         18
blank observed file sizes:             18
ready for acceptance recheck:          0
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

The six validation checks cover:

```text
receipt checklist readiness
receipt-row shape
blank pending receipt fields
DZT/metadata check requirements
blocked downstream state
figure and script-snapshot validity
```

## Interpretation

The receipt checklist validates as a blank, pending collection-day receipt
artifact. It is ready to be filled after real files arrive, but it is not
field evidence by itself.

## Decision

Fill receipt fields only after real files arrive. Keep controlled field
evidence, field FWI, and field 3D/HPC blocked until the guarded acceptance gate
passes.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_checklist_validator.py
5 passed
```

Figure check:

```text
2141x842, dynamic range=255
```
