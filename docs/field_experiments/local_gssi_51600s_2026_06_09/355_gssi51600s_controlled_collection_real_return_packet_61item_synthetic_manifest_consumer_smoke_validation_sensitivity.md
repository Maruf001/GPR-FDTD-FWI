# Field Experiment 355: 61-Item Synthetic Manifest Consumer-Smoke Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `354` validator with damaged variants of the run `353`
manifest-consumer smoke.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/355_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke_validation_sensitivity
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
accepts exact run 353:                true
rejects damaged variants:             true
synthetic packet files:               49
packet requirements accounted for:    61
duplicate-path requirements:          12
measured-evidence payloads:           0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

Damaged variants fail for source-label drift, consumer-count drift,
file-count drift, requirement-count drift, duplicate-count drift, payload-parse
drift, hash drift, measured-payload promotion, measured-count promotion,
consumer-check failure, downstream promotion, figure drift, and script-snapshot
drift.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke_validation_sensitivity.py
8 passed
```

Figure validation:

```text
3491x886, dynamic range=255
```
