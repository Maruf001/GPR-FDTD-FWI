# Field Experiment 550: Integrated Synthetic Receipt Mechanics Smoke Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `549` validator.

The damaged cases cover missing synthetic DZT files, missing metadata files,
signature failures, schema failures, blank values, receipt-count drift, false
live receipt acceptance, false live-file presence, loss of the synthetic-only
boundary, false receipt/FWI promotion, blank figure output, and missing script
snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/550_gssi51600s_controlled_collection_live_receipt_integrated_synthetic_mechanics_smoke_validation_sensitivity
```

## Result

```text
cases:                          16
expected pass:                  1
expected fail:                  15
actual pass:                    1
actual fail:                    15
unexpected outcomes:            0
live receipt ready:             false
field FWI ready:                false
field 3D/HPC ready:             false
```

## Decision

Runs `548-550` are guarded output-local positive-control coverage only. The
validator rejects damaged mechanics states and false live-evidence promotion.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_integrated_synthetic_mechanics_smoke_validation_sensitivity.py
3 passed
```

