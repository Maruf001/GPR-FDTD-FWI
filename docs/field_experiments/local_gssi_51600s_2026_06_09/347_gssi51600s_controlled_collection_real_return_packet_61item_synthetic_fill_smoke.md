# Field Experiment 347: 61-Item Synthetic Fill Smoke

Date: 2026-06-29

## Purpose

Test whether the corrected 61-item field return-template pack can be filled
and checked in an isolated synthetic packet.

This run does not create measured field evidence, provenance acceptance, real
archive acceptance, field FWI, GPU work, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/347_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_fill_smoke
```

## Result

```text
synthetic fill smoke ready:          true
packet requirements:                 61
unique return paths:                 49
synthetic packet files:              49
duplicate-path requirements:         12
synthetic packet items present:      61
synthetic packet items missing:      0
action groups:                       7
open action groups:                  0
synthetic ready gates:               8
synthetic blocked gates:             1
synthetic packet structurally full:  true
synthetic packet is measured:        false
real packet files present:           false
field evidence ready:                false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

The template pack is internally fillable: 49 synthetic files cover all 61
packet requirements because 12 requirements intentionally share metadata paths.
This is a structural smoke only, not measured field evidence.

## Validation

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_fill_smoke.py
4 passed
```

Figure validation:

```text
3581x931, dynamic range=255
```
