# Field Experiment 343: 61-Item Return Packet Template Pack Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `342` validator with controlled damaged variants of the
run `341` corrected field template pack.

This run does not stage measured field files, pass the return-packet
acceptance gate, accept provenance, promote controlled field evidence, launch
field FWI, use GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/343_gssi51600s_controlled_collection_real_return_packet_61item_template_pack_validation_sensitivity
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
accepts exact run 341:               true
rejects damaged variants:            true
packet requirements:                 61
unique return paths:                 49
template files written:              50
duplicate-path requirements:         12
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

The exact run `341` artifacts pass. Twelve damaged variants fail as expected
for source-label drift, packet-count drift, unique-path count drift, false
template evidence promotion, duplicate-count drift, requirement-type drift,
antenna-count drift, downstream promotion, GPU-priority drift, figure drift,
script-snapshot drift, and written-template hash drift.

## Decision

Use runs `341-343` as the guarded corrected 61-item field template-pack block.

## Validation

Focused sensitivity test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_template_pack_validation_sensitivity.py
2 passed
```

Combined focused template-pack tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_template_pack.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_template_pack_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_template_pack_validation_sensitivity.py
7 passed
```

Figure validation:

```text
3473x886, dynamic range=255
```
