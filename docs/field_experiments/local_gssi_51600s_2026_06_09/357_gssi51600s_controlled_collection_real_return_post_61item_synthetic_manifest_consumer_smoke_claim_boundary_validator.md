# Field Experiment 357: Post 61-Item Synthetic Manifest Consumer-Smoke Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `356` claim boundary from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/357_gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary_validator
```

## Result

```text
validation checks:                    7
passed checks:                        7
failed checks:                        0
validation ready:                     true
claims:                               17
guarded claims:                       13
blocked claims:                       4
synthetic packet files:               49
packet requirements accounted for:    61
duplicate-path requirements:          12
measured-evidence payloads:           0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

The validator confirms claim counts, the new manifest-consumer claim row,
manifest metrics, blocked claim rows, blocked downstream states, figure
validation, and script snapshots.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3581x893, dynamic range=255
```
