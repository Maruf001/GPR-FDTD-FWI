# Field Experiment 391: Intake Completion Parser Contract Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `390` validator against controlled damage to the parser
contract.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/391_gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validation_sensitivity.png
```

## Result

```text
scenarios:                          29
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         28
observed failure scenarios:         28
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 389:    true
validator rejects damaged variants: true
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The damaged variants cover worksheet readiness drift, row-count drift,
completion-rule drift, parser-state promotion, current evidence promotion,
downstream promotion, GPU-priority drift, blank figures, and missing script
snapshots.

## Decision

Use runs `389-391` as the guarded field intake-completion parser-contract
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_completion_parser_contract.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x886, dynamic range=255
```
