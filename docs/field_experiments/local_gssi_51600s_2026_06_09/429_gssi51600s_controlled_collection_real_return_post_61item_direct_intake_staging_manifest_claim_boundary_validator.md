# Field Experiment 429: Post Direct-Intake Staging Manifest Claim Boundary Validator

Date: 2026-06-30

## Purpose

Validate run `428`, the field claim boundary after the direct-intake staging
manifest.

Run `428` added the guarded staging-manifest claim to the field boundary. This
validator confirms that the saved boundary preserves the 33-slot intake split,
the zero-evidence state, and the blocked downstream states.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/429_gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation checks passed:                  5
blocking failures:                         0
claim-boundary validation ready:           true
claims:                                    29
guarded claims:                            25
blocked claims:                            4
direct real-input slots:                   33
measured DZT files required:               9
global metadata JSON files required:       15
per-file metadata JSON files required:     9
staged real files:                         0
accepted measured-evidence files:          0
real packet files present:                 false
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The validator confirms the new guarded claim, the 9/15/9 direct-intake split,
zero staged real files, zero accepted measured-evidence files, four blocked
field-evidence claims, and no downstream promotion.

## Decision

Use run `429` as the artifact guard for run `428`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validator.py
8 passed
```

Figure check:

```text
2141x839, dynamic range=255
```
