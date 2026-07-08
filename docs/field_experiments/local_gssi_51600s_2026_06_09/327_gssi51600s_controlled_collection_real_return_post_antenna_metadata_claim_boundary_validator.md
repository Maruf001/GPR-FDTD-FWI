# Field Experiment 327: Post-Antenna Metadata Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `326` controlled-field post-antenna-metadata claim
boundary from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/327_gssi51600s_controlled_collection_real_return_post_antenna_metadata_claim_boundary_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
claim count:                        15
guarded claim count:                11
blocked claim count:                4
antenna addendum ready:             true
updated packet items:               61
updated metadata requirements:      36
antenna aperture metadata items:    4
missing packet items:               61
missing metadata requirements:      36
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The validator checks claim counts, the new antenna metadata claim row, updated
packet/missing-item metrics, blocked claim rows, downstream field states,
figure validation, and script snapshots.

## Interpretation

The run `326` claim boundary is internally consistent. It preserves the field
no-go state while updating the measured packet target to 61 items.

## Decision

Use run `327` as the validator for run `326`. Sensitivity hardening remains
required before closing the block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_antenna_metadata_claim_boundary_validator.py
3 passed
```

Figure check:

```text
3653x929, dynamic range=255
```
