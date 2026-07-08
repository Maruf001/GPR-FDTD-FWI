# Field Experiment 373: 61-Item Collection Execution Checklist Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `372` validator with controlled damaged variants of the
run `371` checklist artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/373_gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_validation_sensitivity.png
```

## Result

```text
scenarios:                         23
expected pass scenarios:           1
expected failure scenarios:        22
observed pass scenarios:           1
observed failure scenarios:        22
unexpected outcomes:               0
checklist sensitivity ready:       true
validator accepts exact run 371:   true
validator rejects damaged variants:true
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The validator accepts the exact run `371` checklist and rejects controlled
damage to source readiness, stage counts, dependencies, field-state promotion,
figure validation, and script snapshots.

## Decision

Use runs `371-373` as the guarded field collection-execution checklist block.
Keep provenance acceptance, archive acceptance, field evidence, field FWI, GPU
work, and field 3D/HPC blocked until real direct inputs exist and generated
outputs are regenerated from them.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_collection_execution_checklist_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x890, dynamic range=255
```
