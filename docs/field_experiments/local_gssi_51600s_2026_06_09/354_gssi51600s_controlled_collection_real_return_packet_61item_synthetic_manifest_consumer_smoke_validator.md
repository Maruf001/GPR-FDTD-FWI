# Field Experiment 354: 61-Item Synthetic Manifest Consumer-Smoke Validator

Date: 2026-06-29

## Purpose

Validate the saved run `353` manifest-consumer smoke from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/354_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke_validator
```

## Result

```text
validation checks:                    8
passed checks:                        8
failed checks:                        0
validation ready:                     true
synthetic packet files:               49
packet requirements accounted for:    61
duplicate-path requirements:          12
synthetic payloads:                   49
measured-evidence payloads:           0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

The validator confirms source identity, payload inventory counts, payload
parsing, hash and size stability, synthetic/non-evidence flags, consumer-check
results, blocked downstream states, figure validation, and script snapshots.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke_validator.py
2 passed
```

Figure validation:

```text
3401x900, dynamic range=255
```
