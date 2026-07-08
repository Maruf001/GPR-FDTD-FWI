# Field Experiment 385: Controlled Collection Real-Return Intake Worksheet Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `384` validator for the run `383` intake worksheet.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/385_gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validation_sensitivity.png
```

## Result

```text
scenarios:                          30
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         29
observed failure scenarios:         29
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 383:    true
validator rejects damaged variants: true
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The damaged variants cover worksheet shape drift, blank-cell drift, completed
row drift, measured-evidence promotion, default status drift, packet count
drift, downstream promotion, GPU-priority drift, blank figures, and missing
script snapshots.

## Decision

Use runs `383-385` as the guarded field real-return intake-worksheet block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_worksheet.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_worksheet_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_worksheet_validation_sensitivity.py
11 passed
```

Figure check:

```text
3581x886, dynamic range=255
```
