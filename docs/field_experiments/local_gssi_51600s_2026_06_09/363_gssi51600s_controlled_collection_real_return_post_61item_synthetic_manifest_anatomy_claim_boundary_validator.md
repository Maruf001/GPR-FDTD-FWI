# Field Experiment 363: Post-61-Item Synthetic Manifest Anatomy Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `362` from saved artifacts.

The validator checks the updated claim counts, manifest-anatomy source
readiness, 61-requirement/49-file packet anatomy, blocked downstream field
states, figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/363_gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validator.png
```

## Result

```text
validation checks:                 6
passed checks:                     6
failed checks:                     0
claim-boundary validation ready:   true
claims:                            18
guarded claims:                    14
blocked claims:                    4
synthetic packet files:            49
packet requirements:               61
duplicate-path requirements:       12
metadata requirements:             36
measured-evidence payloads:        0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Decision

Use this validator as the artifact guard for run `362`. Sensitivity testing
remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x842, dynamic range=255
```
