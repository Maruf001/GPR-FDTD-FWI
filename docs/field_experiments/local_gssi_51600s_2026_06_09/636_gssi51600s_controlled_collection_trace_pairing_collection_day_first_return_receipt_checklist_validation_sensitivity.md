# Field Experiment 636: First-Return Receipt Checklist Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `635` receipt checklist validator.

This run checks that the validator accepts only the exact blank pending receipt
checklist and rejects damaged or prematurely promoted states.

This is a CPU-only validation-sensitivity run. It does not create measured DZT
files, populate metadata JSON files, accept field evidence, launch field FWI,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/636_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_receipt_checklist_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             19
expected pass scenarios:               1
expected fail scenarios:               18
observed pass scenarios:               1
observed fail scenarios:               18
unexpected outcomes:                   0
damaged scenarios:                     18
damaged scenarios rejected:            18
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

Rejected damaged states include:

```text
checklist readiness damage
source-packet readiness damage
row removal
pair-count damage
pending-count damage
operator-initials fill
observed-hash fill
observed-file-size fill
ready-for-recheck promotion
DZT/metadata check-requirement damage
parent-directory damage
acceptance-command damage
field-evidence promotion
field-FWI promotion
field-3D/HPC promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The receipt checklist validator is fail-closed. It accepts the blank pending
receipt artifact and rejects tested states that would imply premature receipt
completion, recheck readiness, evidence acceptance, or downstream promotion.

## Decision

Use runs `634-636` as the guarded first-return receipt checklist block. Keep
controlled field evidence, field FWI, and field 3D/HPC blocked until real files
arrive and pass the guarded acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_checklist_validation_sensitivity.py
3 passed
```

Figure check:

```text
3131x889, dynamic range=255
```
