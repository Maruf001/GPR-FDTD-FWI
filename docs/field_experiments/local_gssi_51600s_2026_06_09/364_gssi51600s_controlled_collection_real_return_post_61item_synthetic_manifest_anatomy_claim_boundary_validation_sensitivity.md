# Field Experiment 364: Post-61-Item Synthetic Manifest Anatomy Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `363` validator with controlled damaged variants of the
run `362` claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/364_gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected failure scenarios:        17
observed pass scenarios:           1
observed failure scenarios:        17
unexpected outcomes:               0
claim-boundary sensitivity ready:  true
validator accepts exact run 362:   true
validator rejects damaged variants:true
claims:                            18
guarded claims:                    14
blocked claims:                    4
measured-evidence payloads:        0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The validator accepts the exact run `362` boundary and rejects controlled
damage to counts, source readiness, anatomy readiness, evidence text, packet
metrics, blocked rows, downstream state, figure validation, and script
snapshots.

## Decision

Use runs `362-364` as the guarded field post-synthetic-manifest-anatomy
claim-boundary block. Measured evidence, provenance acceptance, archive
acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_anatomy_claim_boundary_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x885, dynamic range=255
```
