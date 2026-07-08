# Field Experiment 378: 61-Item Operator Handoff Manifest Validator

Date: 2026-06-29

## Purpose

Validate run `377` from saved artifacts.

The validator checks row shape, direct/generated split, operator-item
sequencing, type and requirement accounting, blocked downstream states, figure
validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/378_gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
handoff validation ready:          true
stages:                            4
handoff rows:                      49
direct operator items:             33
generated follow-up items:         16
packet requirements:               61
duplicate-path requirements:       12
current measured-evidence payloads:0
real packet files present:         false
provenance acceptance ready:       false
archive acceptance ready:          false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

## Decision

Use this validator as the artifact guard for run `377`. Sensitivity testing
remains required before closing the handoff block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validator.py
4 passed as part of the 10-test focused set
```

Figure check:

```text
2645x841, dynamic range=255
```
