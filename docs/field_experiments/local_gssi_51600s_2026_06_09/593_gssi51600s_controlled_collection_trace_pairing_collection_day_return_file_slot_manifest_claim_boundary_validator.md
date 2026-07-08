# Field Experiment 593: Collection Return File-Slot Manifest Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `592` field file-slot manifest claim boundary.

The validator checks the claim shape, guarded claim content, file-slot counts,
dependency split, blocked downstream states, figure validation, and script
snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/593_gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary_validator
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
claims:                         5
guarded claims:                 2
blocked claims:                 3
file slots:                     33
metadata JSON slots:            24
measured DZT slots:             9
preparable metadata slots:      15
collection-coupled slots:       18
preflight-passed slots:         0
ready slots:                    0
controlled field evidence:      false
field FWI ready:                false
field 3D/HPC ready:             false
gpu priority:                   none
```

## Interpretation

The saved file-slot manifest claim boundary validates from artifacts. It keeps
the per-file checklist separate from measured field evidence.

## Decision

Use this validator before treating the file-slot manifest as the current field
collection boundary.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary_validator.py

3 passed
```

Figure check:

```text
3293x894, dynamic range=255
```
