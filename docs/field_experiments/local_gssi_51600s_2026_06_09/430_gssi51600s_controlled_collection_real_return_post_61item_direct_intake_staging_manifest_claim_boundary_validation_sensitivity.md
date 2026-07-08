# Field Experiment 430: Post Direct-Intake Staging Manifest Claim Boundary Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `429` validator for the run `428` post-direct-intake field
claim boundary.

Run `429` validated the field claim boundary that includes the direct-intake
staging manifest. This run verifies that the validator rejects count drift,
claim-support drift, staged-file promotion, measured-evidence promotion,
downstream promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/430_gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                         10
expected pass scenarios:                       1
expected failure scenarios:                    9
unexpected scenarios:                          0
claim-boundary sensitivity ready:              true
exact source artifacts pass:                   true
staged-file promotion rejected:                true
downstream promotion rejected:                 true
real packet files present:                     false
controlled field evidence ready:               false
field FWI ready:                               false
field 3D/HPC ready:                            false
GPU priority:                                  none
```

The exact run `428` artifacts pass. Damaged variants fail as expected for claim
count drift, claim-support drift, DZT-count drift, staged-file promotion,
measured-evidence promotion, field-FWI promotion, blocked-row support drift,
figure damage, and script-snapshot damage.

## Decision

Use runs `428-430` as the guarded post-direct-intake field claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
2465x854, dynamic range=255
```
