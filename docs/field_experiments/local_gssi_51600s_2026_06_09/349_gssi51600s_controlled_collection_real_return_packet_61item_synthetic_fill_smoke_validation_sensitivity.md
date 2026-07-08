# Field Experiment 349: 61-Item Synthetic Fill Smoke Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `348` validator with damaged variants of the run `347`
synthetic-fill smoke.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/349_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_fill_smoke_validation_sensitivity
```

## Result

```text
scenarios:                           13
expected pass:                       1
observed pass:                       1
expected failures:                   12
observed failures:                   12
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 347:               true
rejects damaged variants:            true
packet requirements:                 61
unique return paths:                 49
synthetic packet files:              49
synthetic packet items present:      61
synthetic packet is measured:        false
real packet files present:           false
```

The damaged variants fail for count drift, false evidence promotion,
packet-presence drift, action-row drift, field-evidence gate promotion,
real-packet promotion, figure drift, and script-snapshot drift.

## Validation

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_fill_smoke.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_fill_smoke_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_fill_smoke_validation_sensitivity.py
8 passed
```

Figure validation:

```text
3581x886, dynamic range=255
```
