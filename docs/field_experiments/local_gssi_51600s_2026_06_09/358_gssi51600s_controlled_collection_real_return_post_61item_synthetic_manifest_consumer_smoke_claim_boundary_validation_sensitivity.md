# Field Experiment 358: Post 61-Item Synthetic Manifest Consumer-Smoke Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `357` validator with damaged variants of the run `356`
claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/358_gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                            14
expected pass:                        1
observed pass:                        1
expected failures:                    13
observed failures:                    13
unexpected outcomes:                  0
sensitivity ready:                    true
accepts exact run 356:                true
rejects damaged variants:             true
claims:                               17
guarded claims:                       13
blocked claims:                       4
packet requirements accounted for:    61
measured-evidence payloads:           0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

Damaged variants fail for source-label drift, claim-count drift,
manifest-claim support drift, manifest-claim evidence drift, file-count drift,
requirement-count drift, duplicate-count drift, measured-payload promotion,
measured-evidence promotion, blocked-support drift, downstream promotion,
figure drift, and script-snapshot drift.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3545x877, dynamic range=255
```
