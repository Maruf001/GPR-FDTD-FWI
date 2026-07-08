# Field Experiment 352: Post-Synthetic-Fill-Smoke Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `351` validator with damaged variants of the run `350`
claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/352_gssi51600s_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                           16
expected pass:                       1
observed pass:                       1
expected failures:                   15
observed failures:                   15
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 350:               true
rejects damaged variants:            true
claims:                              16
guarded claims:                      12
blocked claims:                      4
packet requirements:                 61
unique return paths:                 49
synthetic packet files:              49
synthetic packet is measured:        false
field evidence ready:                false
```

The damaged variants fail for claim drift, packet-count drift, false evidence
promotion, blocked-support drift, downstream promotion, GPU-priority drift,
figure drift, and script-snapshot drift.

## Validation

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3653x886, dynamic range=255
```
