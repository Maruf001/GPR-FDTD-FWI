# Field Experiment 379: 61-Item Operator Handoff Manifest Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `378` validator with controlled damaged variants of the
run `377` operator handoff manifest.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/379_gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validation_sensitivity.png
```

## Result

```text
scenarios:                         25
expected pass scenarios:           1
expected failure scenarios:        24
observed pass scenarios:           1
observed failure scenarios:        24
unexpected outcomes:               0
handoff sensitivity ready:         true
validator accepts exact run 377:   true
validator rejects damaged variants:true
real packet files present:         false
provenance acceptance ready:       false
archive acceptance ready:          false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The validator accepts the exact run `377` handoff and rejects controlled damage
to row accounting, direct/generated split, operator sequencing, requirement
counts, measured-evidence state, downstream promotions, figure validation, and
script snapshots.

## Decision

Use runs `377-379` as the guarded field operator-handoff manifest block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_operator_handoff_manifest_validation_sensitivity.py
3 passed as part of the 10-test focused set
```

Figure check:

```text
3581x884, dynamic range=255
```
