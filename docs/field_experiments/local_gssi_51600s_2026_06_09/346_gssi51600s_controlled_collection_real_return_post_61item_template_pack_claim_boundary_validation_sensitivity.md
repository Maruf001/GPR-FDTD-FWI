# Field Experiment 346: Post 61-Item Template Pack Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `345` validator with controlled damaged variants of the
run `344` claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/346_gssi51600s_controlled_collection_real_return_post_61item_template_pack_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                           15
expected pass:                       1
observed pass:                       1
expected failures:                   14
observed failures:                   14
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 344:               true
rejects damaged variants:            true
claims:                              15
packet requirements:                 61
unique return paths:                 49
template files written:              50
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

The exact run `344` artifacts pass. Fourteen damaged variants fail as expected
for source-label drift, claim-count drift, template-support drift,
template-evidence drift, packet-count drift, unique-path drift,
template-file-count drift, duplicate-count drift, source-readiness demotion,
blocked-support drift, downstream promotion, GPU-priority drift, figure drift,
and script-snapshot drift.

## Decision

Use runs `344-346` as the guarded current field claim-boundary block after the
corrected template pack.

## Validation

Focused sensitivity test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_template_pack_claim_boundary_validation_sensitivity.py
2 passed
```

Combined focused boundary tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_template_pack_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_template_pack_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_template_pack_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3581x886, dynamic range=255
```
