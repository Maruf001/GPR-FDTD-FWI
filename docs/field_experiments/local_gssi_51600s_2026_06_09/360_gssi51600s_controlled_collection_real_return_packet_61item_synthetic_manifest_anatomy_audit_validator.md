# Field Experiment 360: 61-Item Synthetic Manifest Anatomy Audit Validator

Date: 2026-06-29

## Purpose

Validate run `359` from saved artifacts.

The validator checks source readiness, packet counts, group and prefix tables,
metadata duplicate-path anatomy, blocked field downstream states, figure
validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/360_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validator.png
```

## Result

```text
validation checks:                 7
passed checks:                     7
failed checks:                     0
manifest anatomy validation ready: true
synthetic packet files:            49
packet requirements:               61
duplicate-path requirements:       12
metadata requirements:             36
measured-evidence payloads:        0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Decision

Use this as the positive validator for run `359`. Sensitivity testing remains
required before closing the block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```
