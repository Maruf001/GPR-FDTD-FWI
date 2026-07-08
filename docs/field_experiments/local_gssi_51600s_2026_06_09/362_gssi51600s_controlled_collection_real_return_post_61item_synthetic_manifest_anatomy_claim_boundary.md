# Field Experiment 362: Post-61-Item Synthetic Manifest Anatomy Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `359-361` synthetic manifest-anatomy result into the
controlled field claim boundary.

This is a claim-boundary update. It does not create measured field evidence,
accept provenance, accept a real archive, run field FWI, launch GPU work, or
run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/362_gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary.png
```

## Result

```text
claim boundary ready:              true
claims:                            18
guarded claims:                    14
blocked claims:                    4
base claims:                       17
base guarded claims:               13
base blocked claims:               4
manifest anatomy ready:            true
manifest anatomy sensitivity ready:true
synthetic packet files:            49
packet requirements:               61
duplicate-path requirements:       12
metadata files:                    24
metadata requirements:             36
metadata duplicate requirements:   12
measured-evidence payloads:        0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The new guarded claim explains the packet anatomy: 61 packet requirements map
to 49 synthetic files because metadata carries all 12 duplicate-path
requirements. This does not promote synthetic files into measured evidence.

## Decision

Use this as the current field claim boundary after the synthetic
manifest-anatomy block. Keep measured evidence, provenance, archive
acceptance, field FWI, GPU work, and field 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
3941x946, dynamic range=255
```
