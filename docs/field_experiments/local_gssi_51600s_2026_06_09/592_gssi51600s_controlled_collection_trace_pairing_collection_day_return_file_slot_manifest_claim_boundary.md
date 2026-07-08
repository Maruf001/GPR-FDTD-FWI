# Field Experiment 592: Collection Return File-Slot Manifest Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the controlled-collection file-slot manifest.

Runs `589-591` defined and hardened the per-file collection checklist. This run
states what that checklist supports and what still requires real measured field
files.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/592_gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary
```

## Result

```text
claims:                         5
guarded claims:                 2
blocked claims:                 3
source manifest ready:          true
source validation ready:         true
source sensitivity ready:        true
file slots:                     33
stage shape:                    7,4,6,6,6,4
metadata JSON slots:            24
measured DZT slots:             9
preparable metadata slots:      15
paired metadata slots:          9
measured DZT dependency slots:  9
collection-coupled slots:       18
preflight-passed slots:         0
ready slots:                    0
controlled field evidence:      false
field FWI ready:                false
field 3D/HPC ready:             false
gpu priority:                   none
```

The two guarded claims are:

| Claim | Supporting runs | Status |
| --- | --- | --- |
| controlled collection file-slot manifest | 589-591 | guarded |
| collection dependency split | 586-591 | guarded |

The blocked claims are measured radar scan files, paired collection metadata,
and controlled field evidence or downstream escalation.

## Interpretation

The collection-day package is now concrete at the file level. Fifteen metadata
records can be prepared before collection, while nine measured DZT files and
nine paired metadata records must be produced together during collection. No
slot has passed preflight, so this is a checklist boundary rather than measured
field evidence.

## Decision

Use this boundary as the current field collection checklist boundary. Keep field
FWI and field 3D/HPC blocked until real files pass preflight.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary_validation_sensitivity.py

9 passed
```

Figure check:

```text
3581x933, dynamic range=255
```
