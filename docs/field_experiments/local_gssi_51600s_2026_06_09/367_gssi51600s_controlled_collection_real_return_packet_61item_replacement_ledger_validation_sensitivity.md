# Field Experiment 367: 61-Item Real-Return Replacement Ledger Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `366` validator with controlled damaged variants of the
run `365` replacement ledger.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/367_gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_validation_sensitivity.png
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected failure scenarios:        17
observed pass scenarios:           1
observed failure scenarios:        17
unexpected outcomes:               0
replacement sensitivity ready:     true
validator accepts exact run 365:   true
validator rejects damaged variants:true
field evidence ready:              false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The validator accepts the exact run `365` ledger and rejects controlled damage
to counts, replacement split, action rows, measured-payload promotion,
downstream promotion, figure validation, and script snapshots.

## Decision

Use runs `365-367` as the guarded field real-return replacement-ledger block.
Keep provenance, archive acceptance, controlled field evidence, field FWI, GPU
work, and field 3D/HPC blocked until real packet files replace the synthetic
payloads.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_replacement_ledger_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x885, dynamic range=255
```
