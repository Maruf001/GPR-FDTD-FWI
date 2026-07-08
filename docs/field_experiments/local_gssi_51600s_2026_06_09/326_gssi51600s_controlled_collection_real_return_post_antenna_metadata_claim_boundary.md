# Field Experiment 326: Post-Antenna Metadata Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the controlled-field claim boundary after the guarded antenna aperture
metadata addendum.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/326_gssi51600s_controlled_collection_real_return_post_antenna_metadata_claim_boundary
```

## Result

```text
claim count:                         15
guarded claim count:                 11
blocked claim count:                 4
base claim count:                    14
base guarded claim count:            10
base blocked claim count:            4
antenna addendum sensitivity ready:  true
source packet items:                 57
updated packet items:                61
updated acceptance checks:           201
updated measured requirements:       54
updated metadata requirements:       36
antenna aperture metadata items:     4
BEM 3-sample aperture relative L2:   0.08009547612144642
missing packet items:                61
missing real DZT files:              9
missing metadata requirements:       36
missing checksum rows:               9
missing acceptance results:          7
provenance acceptance ready:         false
real archive acceptance ready:       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
claim boundary ready:                true
```

The new guarded claim states that the controlled-field return packet is updated
to 61 items and 36 metadata requirements, including four blocking antenna
aperture/coupling records.

## Interpretation

The current field packet target has changed. The previous 57-item packet is no
longer the preferred target because it did not explicitly encode antenna
aperture, phase-center, coupling, and positioning controls. The current target
is a 61-item measured return packet.

## Decision

Use run `326` as the current field claim boundary after the antenna metadata
addendum. Keep provenance acceptance, archive acceptance, controlled field
evidence, field FWI, field 3D/HPC, and GPU work blocked until the 61-item
measured packet is staged and validated.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_antenna_metadata_claim_boundary.py
3 passed
```

Figure check:

```text
3653x953, dynamic range=255
```
