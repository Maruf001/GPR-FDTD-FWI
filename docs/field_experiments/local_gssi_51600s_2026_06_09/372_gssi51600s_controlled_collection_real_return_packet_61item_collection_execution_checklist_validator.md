# Field Experiment 372: 61-Item Collection Execution Checklist Validator

Date: 2026-06-29

## Purpose

Validate run `371` from saved artifacts.

The validator checks checklist readiness, stage sequence, file and requirement
counts, dependency rows, blocked downstream states, figure validation, and
script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/372_gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
checklist validation ready:        true
stages:                            4
dependency edges:                  6
direct collection input files:     33
generated verification files:      16
packet requirements:               61
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

## Decision

Use this validator as the artifact guard for run `371`. Sensitivity testing
remains required before closing the checklist block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_collection_execution_checklist_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x840, dynamic range=255
```
