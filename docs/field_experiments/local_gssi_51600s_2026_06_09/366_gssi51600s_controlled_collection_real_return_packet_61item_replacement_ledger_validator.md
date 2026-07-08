# Field Experiment 366: 61-Item Real-Return Replacement Ledger Validator

Date: 2026-06-29

## Purpose

Validate run `365` from saved artifacts.

The validator checks source readiness, file and requirement counts, the
33-input/16-generated-output split, blocked downstream field states, figure
validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/366_gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validator.png
```

## Result

```text
validation checks:                 5
passed checks:                     5
failed checks:                     0
replacement ledger validation ready:true
unique packet files:               49
packet requirements:               61
direct collection input files:     33
generated verification files:      16
current measured-evidence payloads:0
field evidence ready:              false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Decision

Use this validator as the artifact guard for run `365`. Sensitivity testing
remains required before closing the replacement-ledger block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_replacement_ledger_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x840, dynamic range=255
```
