# Field Experiment 356: Post 61-Item Synthetic Manifest Consumer-Smoke Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic manifest-consumer result from runs `353-355` into
the current field claim boundary.

This run does not promote measured field evidence, provenance acceptance,
archive acceptance, field FWI, GPU work, or field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/356_gssi51600s_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary
```

## Result

```text
claims:                               17
guarded claims:                       13
blocked claims:                       4
manifest sensitivity ready:           true
manifest consumer smoke ready:        true
synthetic packet files:               49
packet requirements accounted for:    61
duplicate-path requirements:          12
synthetic payloads:                   49
measured-evidence payloads:           0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

## Interpretation

The field boundary now includes the manifest-consumer result: all synthetic
payload files parse and account for every packet requirement. The payloads
remain synthetic non-evidence.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_manifest_consumer_smoke_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x946, dynamic range=255
```
