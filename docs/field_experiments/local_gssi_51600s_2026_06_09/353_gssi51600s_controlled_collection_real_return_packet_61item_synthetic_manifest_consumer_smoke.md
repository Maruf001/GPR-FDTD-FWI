# Field Experiment 353: 61-Item Synthetic Manifest Consumer Smoke

Date: 2026-06-29

## Purpose

Test whether the filled synthetic packet from run `347` can be parsed as a
manifest by a downstream consumer.

This run uses synthetic payloads only. It does not promote the packet to
measured field evidence, provenance acceptance, archive acceptance, field FWI,
GPU work, or field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/353_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke
```

## Result

```text
consumer checks:                      7
consumer passes:                      7
consumer failures:                    0
manifest consumer smoke ready:        true
synthetic packet files:               49
parsed payload files:                 49
packet requirements accounted for:    61
duplicate-path requirements:          12
measured-DZT payloads:                9
metadata payloads:                    24
checksum payloads:                    9
acceptance payloads:                  7
synthetic payloads:                   49
measured-evidence payloads:           0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

## Interpretation

All 49 synthetic files parse into a manifest, and the parsed payloads account
for all 61 packet requirements. Every parsed payload remains explicitly marked
as synthetic and not measured evidence.

This is a structural consumer check. It does not mean real measured field data
exist.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_consumer_smoke.py
4 passed
```

Figure validation:

```text
3581x931, dynamic range=255
```
